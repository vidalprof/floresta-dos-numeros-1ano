# -*- coding: utf-8 -*-
# ============================================================
#  AUDITOR DE FUNÇÃO QUE NÃO EXISTE — "isso vai estourar na mão da criança?"
#
#  Nasceu de um defeito real (ago/2026): na Legenda do Clique, a última fase
#  ("Escreva a legenda") chamava `normal(...)` — uma função que NUNCA foi
#  copiada para o arquivo. O `node --check` passava (sintaxe está certa), a
#  tela abria bonita, mas ao apertar "Publicar" o app estourava
#  "normal is not defined" e a criança FICAVA PRESA ali, sem nenhum aviso.
#
#  O `node --check` não pega isso, porque não é erro de sintaxe: é uma função
#  que só falta na hora de rodar. Este auditor pega antes.
#
#  Como funciona: tira comentários e textos entre aspas (senão qualquer palavra
#  escrita num comentário viraria "chamada"), junta tudo que é chamado como
#  `nome(` e compara com tudo que é declarado no arquivo + a lista do navegador.
#
#  Uso: python3 _qa/funcoes.py _nomes/index.html
# ============================================================
import re, sys

arq = sys.argv[1] if len(sys.argv) > 1 else ""
if not arq:
    print("uso: python3 _qa/funcoes.py <arquivo.html>")
    sys.exit(2)

html = open(arq, encoding="utf-8").read()
js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))

# ---- tirar comentários e textos entre aspas (inclusive regex literais simples)
def limpa(s):
    fora, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == "/" and i + 1 < n and s[i+1] == "*":
            j = s.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        if c == "/" and i + 1 < n and s[i+1] == "/":
            j = s.find("\n", i)
            i = n if j < 0 else j
            continue
        if c in "\"'":
            j = i + 1
            while j < n:
                if s[j] == "\\":
                    j += 2; continue
                if s[j] == c:
                    break
                j += 1
            fora.append('""')
            i = j + 1
            continue
        fora.append(c)
        i += 1
    return "".join(fora)

# ⚠️ a lista de PROTEGIDAS tem de sair do texto CRU: o `limpa()` apaga as
# strings, e é dentro de uma string que mora o `"function"` do guarda.
JS_CRU = js
js = limpa(js)

# ---- o que o arquivo declara
declara = set(re.findall(r"function\s+([A-Za-z_$][\w$]*)", js))
declara |= set(re.findall(r"(?:var|let|const)\s+([A-Za-z_$][\w$]*)\s*=\s*function", js))
# var a=1,b=2 — qualquer var pode guardar função vinda de fora
declara |= set(re.findall(r"(?:var|let|const)\s+([A-Za-z_$][\w$]*)", js))
# parâmetros de função (um callback chamado dentro dela)
for p in re.findall(r"function[^(]*\(([^)]*)\)", js):
    declara |= set(x.strip() for x in p.split(",") if x.strip())

# ---- o que o navegador já dá de graça
GLOBAIS = set("""
if for while switch catch return typeof function new delete void in of do else try instanceof
JSON Math Date Array String Number Object Boolean RegExp Error Promise Map Set Symbol
parseInt parseFloat isNaN isFinite encodeURIComponent decodeURIComponent encodeURI decodeURI
setTimeout setInterval clearTimeout clearInterval requestAnimationFrame cancelAnimationFrame
alert confirm prompt fetch btoa atob Image Audio Event CustomEvent AudioContext webkitAudioContext
MutationObserver URL URLSearchParams FileReader Blob XMLHttpRequest SpeechSynthesisUtterance
Uint8Array Uint8ClampedArray Uint16Array Uint32Array Int8Array Int16Array Int32Array Float32Array Float64Array ArrayBuffer DataView
WeakMap WeakSet Proxy Reflect Intl TextEncoder TextDecoder Worker Notification IntersectionObserver ResizeObserver Function eval
console document window navigator localStorage sessionStorage location history screen speechSynthesis
""".split())

# ---- o que é chamado (ignora metodo: algo.metodo() )
chamadas = set(re.findall(r"(?<![\w$.])([A-Za-z_$][\w$]*)\s*\(", js))

# ⚠️ LICAO PAGA (ago/2026): a PECA roda sozinha na bancada, mas dentro da
# atividade ela ganha os ajudantes do MOTOR (sPega, sPoe, mascoteFesteja...).
# A casa ja tem o idioma certo para isso — `if(typeof sPega==="function")
# sPega();` —, so que este portao contava a chamada e reprovava a peca por
# "funcao que nao existe". Chamada PROTEGIDA por `typeof` nao estoura na mao
# da crianca: e exatamente o contrario, e o cuidado de quem sabe que ela pode
# faltar. Entao ela nao conta.
protegidas = set(re.findall(
    r'typeof\s+([A-Za-z_$][\w$]*)\s*[!=]==?\s*["\']function["\']', JS_CRU))
faltando = sorted(c for c in chamadas - declara - GLOBAIS - protegidas)

print("%s -> %d nomes chamados, %d declarados" % (arq, len(chamadas), len(declara)))
if not faltando:
    print("   funcoes ok: tudo que e chamado existe no arquivo")
    sys.exit(0)
print("   %d FUNCAO(OES) CHAMADA(S) QUE NAO EXISTEM (estoura na mao da crianca):" % len(faltando))
for f in faltando:
    linha = 0
    m = re.search(r"(?<![\w$.])" + re.escape(f) + r"\s*\(", js)
    if m:
        linha = js[:m.start()].count("\n") + 1
    print("    %s()   (1a chamada por volta da linha %d do JS)" % (f, linha))
sys.exit(1)
