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
    # ⚠️ LICAO PAGA (Teatro, ago/2026): o `limpa()` tirava comentario e string,
    #    mas NAO entendia LITERAL DE REGEX (`/<div[^>]*>/gi`). Uma `"` ou `'`
    #    dentro do regex abria uma "string" que so fechava paginas depois, e todo
    #    o texto no meio — inclusive os ENUNCIADOS ("Ache os adjetivos (todas as
    #    direcoes)") — deixava de ser reconhecido como string. As palavras
    #    seguidas de "(" viravam "funcao que nao existe" e o portao reprovava
    #    conteudo correto. Agora ele PULA o regex literal inteiro.
    fora, i, n, lastsig = [], 0, len(s), ""
    ctx = set("(,=:[!&|?{;}") | set([""])   # apos estes, "/" comeca REGEX (nao divisao)
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
        if c == "/" and lastsig in ctx:
            # literal de regex: anda ate a "/" de fecho (respeita \ e [classe])
            j, inclass, ok = i + 1, False, False
            while j < n:
                d = s[j]
                if d == "\\":
                    j += 2; continue
                if d == "\n":
                    break                      # regex nao cruza linha: nao era regex
                if d == "[":
                    inclass = True
                elif d == "]":
                    inclass = False
                elif d == "/" and not inclass:
                    ok = True; break
                j += 1
            if ok:
                fora.append(" ")               # some com o regex inteiro
                lastsig = ")"                  # depois do regex, contexto de valor
                i = j + 1
                continue
            # nao fechou na linha -> era divisao mesmo: cai no tratamento normal
        if c in "\"'":
            j = i + 1
            while j < n:
                if s[j] == "\\":
                    j += 2; continue
                if s[j] == c:
                    break
                j += 1
            fora.append('""')
            lastsig = '"'
            i = j + 1
            continue
        fora.append(c)
        if not c.isspace():
            lastsig = c
        i += 1
    return "".join(fora)

# ⚠️ a lista de PROTEGIDAS tem de sair do texto CRU: o `limpa()` apaga as
# strings, e é dentro de uma string que mora o `"function"` do guarda.
JS_CRU = js
js = limpa(js)

# ---- o que o arquivo declara
declara = set(re.findall(r"function\s+([A-Za-z_$][\w$]*)", js))
# ⚠️⚠️ LICAO PAGA (ago/2026) — O LIMPADOR PERDE O FIO E O PORTAO ACUSA INOCENTE.
#    Ele acusou `caixaFig()` de nao existir na Central de Entregas. Existe: esta
#    declarada na peca `forca`, em coluna zero. O que aconteceu foi o limpador
#    perder a conta das aspas muito antes — ele nao entende LITERAL DE REGEX
#    (`/<[^>]+>/g`), entao uma aspa dentro de um regex vira abertura de string e
#    tudo dali para a frente e engolido: 5 mil caracteres, com a declaracao no
#    meio. E a MESMA familia do comentario que engoliu as animacoes no
#    integrador — scanner que anda pelo arquivo sem entender uma das formas.
#    Reescrever o limpador para entender regex e caro e arriscado. Aqui basta
#    uma segunda leitura, no texto CRU: declaracao de funcao nesta casa comeca
#    a LINHA. Isto so ACRESCENTA nomes, entao so pode apagar acusacao falsa —
#    e para esconder uma de verdade seria preciso um `function X(` comecando
#    uma linha dentro de uma string, que nao existe.
declara |= set(re.findall(r"^\s*function\s+([A-Za-z_$][\w$]*)\s*\(",
                          JS_CRU, re.M))
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
# ⚠️ LICAO PAGA (ago/2026): faltava o `getComputedStyle` — o motor passou a usa-lo
# para ler o TEXTO VISIVEL da resposta (pular o andaime escondido) e este portao
# reprovou a atividade inteira por 'funcao que nao existe'. E API de navegador,
# de graca desde sempre. Lista de globais incompleta acusa inocente; toda vez que
# uma API nova entrar no motor, ela entra AQUI no mesmo commit.
getComputedStyle matchMedia scrollTo scrollBy getSelection structuredClone queueMicrotask
# ⚠️ `url` NAO e funcao de JS: e funcao de CSS (`background-image:url("data:...")`),
# e chega aqui porque o limpador perde o fio nos literais de regex e deixa
# escapar pedaco de CSS que mora dentro de string. Enquanto o limpador nao
# entender regex, `url` fica aqui — melhor um nome a mais na lista do que a
# banca inteira reprovada por um pedaco de folha de estilo.
url
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
