# -*- coding: utf-8 -*-
# ============================================================
#  AUDITOR DE PROMESSA — "o mascote prometeu; a tela cumpriu?"
#
#  Nasceu de um defeito real que o Marcos pegou (ago/2026), na Fábrica do
#  Bento, fase "Quadro do Estoque": a criança errava, o Bento dizia
#  "deixa eu pôr os brinquedos na mesa para você contar comigo" — e NADA
#  aparecia na mesa. A criança esperava os brinquedos que nunca vinham.
#
#  A causa é sempre a mesma e NÃO dá erro nenhum: o motor tem um ajudante
#      function ajuda(n,ops){
#        ...
#        else if(n===2){ if(ops.concreto) ops.concreto(); falar("dc_ajuda2"); }
#      }
#  onde a AÇÃO é opcional (`if(ops.concreto)`) mas a FALA que promete a ação
#  toca sempre. Quando uma fase esquece de passar o `concreto` (típico de
#  motor clonado — ver _padrao/CLONAR-MOTOR.md), a voz promete e a tela não
#  cumpre. O `node --check` passa, o print fica perfeito, e o defeito só
#  existe com a criança errando na frente.
#
#  O que este auditor faz: acha os ajudantes `f(n,ops)`, descobre quais
#  chaves de `ops` cada ramo USA, vê quais falas tocam FORA do `if` dessa
#  chave (= falas amarradas à chave) e então exige essa chave em TODOS os
#  pontos que chamam o ajudante. Falta a chave num ponto -> reprova.
#  Fala dentro do `else` do `if(ops.X)` não exige nada (é justamente a
#  saída honesta: quando não há X, fala outra coisa).
#
#  Uso: python3 _qa/promessa.py _fabrica/index.html
# ============================================================
import re, sys

arq = sys.argv[1] if len(sys.argv) > 1 else ""
if not arq:
    print("uso: python3 _qa/promessa.py <arquivo.html>")
    sys.exit(2)

html = open(arq, encoding="utf-8").read()
js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))


def sem_comentarios(s):
    """tira /* */ e // mas MANTÉM os textos entre aspas (preciso dos ids das falas)"""
    fora, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == "/" and i + 1 < n and s[i + 1] == "*":
            j = s.find("*/", i + 2)
            fora.append(" " * ((n if j < 0 else j + 2) - i))
            i = n if j < 0 else j + 2
            continue
        if c == "/" and i + 1 < n and s[i + 1] == "/":
            j = s.find("\n", i)
            j = n if j < 0 else j
            fora.append(" " * (j - i))
            i = j
            continue
        if c in "\"'":
            j = i + 1
            while j < n:
                if s[j] == "\\":
                    j += 2
                    continue
                if s[j] == c:
                    break
                j += 1
            fora.append(s[i:j + 1])
            i = j + 1
            continue
        fora.append(c)
        i += 1
    return "".join(fora)


js = sem_comentarios(js)


def fecha(s, i, ab, fe):
    """i aponta para o 'ab'; devolve o índice do par que fecha (ou -1)"""
    d = 0
    while i < len(s):
        if s[i] == ab:
            d += 1
        elif s[i] == fe:
            d -= 1
            if d == 0:
                return i
        i += 1
    return -1


# ---------- 1) achar os ajudantes: function nome(n, ops){ ... } ----------
# ⚠️⚠️ LICAO PAGA (ago/2026) — ESTE PORTAO RODAVA CEGO EM TODA ATIVIDADE
# MONTADA, e a propria banca avisava ("mediu ZERO") sem que eu conferisse.
# Ele procurava a forma do Broto — `function ajuda(n,ops){` —, uma DECLARACAO.
# So que o esqueleto escreve `window.ajuda = function(n, ops){`, uma
# ATRIBUICAO: a expressao regular nunca casava e o portao dizia "nada a
# conferir" com a maior calma. Mesma familia do `srcDe` no portao das imagens:
# o auditor procurando a forma de UMA atividade em vez do que o codigo FAZ.
# E a "fala" tambem mudou de nome: no esqueleto quem promete e o `consolo()`
# (que toca a voz de erro) e o `mostraDica()` (que ESCREVE a promessa na tela).
# Promessa escrita e promessa igual — a crianca le e espera.
FALAS = ("falar(", "consolo(", "mostraDica(")
ajudantes = []
for m in re.finditer(r"(?:function\s+(\w+)|(?:window\.)?(\w+)\s*=\s*function)"
                     r"\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)\s*\{", js):
    nome, ops = (m.group(1) or m.group(2)), m.group(4)
    ab = js.index("{", m.end() - 1)
    fim = fecha(js, ab, "{", "}")
    if fim < 0:
        continue
    corpo = js[ab + 1:fim]
    if not any(f in corpo for f in FALAS) or (ops + ".") not in corpo:
        continue
    ajudantes.append((nome, ops, corpo))

if not ajudantes:
    print(arq + " -> promessa: nenhum ajudante f(n,ops) com fala. Nada a conferir.")
    sys.exit(0)


# ---------- 2) por ajudante: quais chaves cada fala EXIGE ----------
def ramos(corpo):
    """quebra o ajudante nos seus RAMOS de 1º nível — if(n===1){...} else if(n===2){...}
       Sem isso, uma chave usada só no ramo 3 seria cobrada da fala do ramo 1."""
    fora, i, n = [], 0, len(corpo)
    while i < n:
        if corpo[i] == "{":
            f = fecha(corpo, i, "{", "}")
            if f < 0:
                break
            fora.append(corpo[i + 1:f])
            i = f + 1
            continue
        i += 1
    return fora or [corpo]


def exigencias_ramo(corpo, ops):
    """devolve {chave: [falas que tocam sem a chave estar garantida]} num ramo"""
    usadas = set(re.findall(re.escape(ops) + r"\.(\w+)", corpo))
    pilha = []          # (chaves, fim) — guardas ativas
    ultimo_if = None    # (chaves, fim_do_bloco) — p/ o 'else' herdar
    exige = {}
    i, n = 0, len(corpo)
    while i < n:
        pilha = [g for g in pilha if i < g[1]]

        mi = re.match(r"\bif\s*\(", corpo[i:])
        if mi:
            p = i + mi.end() - 1
            pf = fecha(corpo, p, "(", ")")
            if pf < 0:
                break
            cond = corpo[p:pf + 1]
            chaves = set(re.findall(re.escape(ops) + r"\.(\w+)", cond))
            j = pf + 1
            while j < n and corpo[j] in " \t\r\n":
                j += 1
            if j < n and corpo[j] == "{":
                fb = fecha(corpo, j, "{", "}")
                fim = fb if fb > 0 else n
            else:
                fb = corpo.find(";", j)
                fim = (fb if fb > 0 else n) + 1
            if chaves:
                pilha.append((chaves, fim))
                ultimo_if = (chaves, fim)
            i = pf + 1
            continue

        me = re.match(r"\belse\b", corpo[i:])
        if me:
            j = i + me.end()
            while j < n and corpo[j] in " \t\r\n":
                j += 1
            # o else de um if(ops.X) também é "condicionado a X" -> não exige X
            if ultimo_if and j < n and corpo[j] == "{":
                fb = fecha(corpo, j, "{", "}")
                if fb > 0:
                    pilha.append((ultimo_if[0], fb))
            i = j
            continue

        mf = re.match(r"\bfalar\s*\(\s*[\"']([\w\-]+)[\"']", corpo[i:])
        if mf:
            garantidas = set()
            for ch, _f in pilha:
                garantidas |= ch
            for k in usadas - garantidas:
                exige.setdefault(k, []).append(mf.group(1))
            i += mf.end()
            continue
        i += 1
    return exige


def exigencias(corpo, ops):
    junta = {}
    for r in ramos(corpo):
        for k, v in exigencias_ramo(r, ops).items():
            junta.setdefault(k, []).extend(v)
    return junta


# ---------- 3) conferir os pontos de chamada ----------
def chaves_do_objeto(txt):
    """chaves de 1º nível de um literal { a:..., b:... }"""
    fora, d, i, n = [], 0, 0, len(txt)
    while i < n:
        c = txt[i]
        if c in "{[(":
            d += 1
        elif c in "}])":
            d -= 1
        elif c in "\"'":
            j = i + 1
            while j < n:
                if txt[j] == "\\":
                    j += 2
                    continue
                if txt[j] == c:
                    break
                j += 1
            i = j + 1
            continue
        if d == 1:
            mk = re.match(r"\s*(\w+)\s*:", txt[i:])
            if mk and (i == 0 or txt[i - 1] in "{,"):
                fora.append(mk.group(1))
        i += 1
    return set(fora)


falhas, conferidos = [], 0
for nome, ops, corpo in ajudantes:
    exige = exigencias(corpo, ops)
    if not exige:
        continue
    for m in re.finditer(r"\b" + re.escape(nome) + r"\s*\(", js):
        p = m.end() - 1
        if js[max(0, m.start() - 9):m.start()].rstrip().endswith("function"):
            continue
        pf = fecha(js, p, "(", ")")
        if pf < 0:
            continue
        args = js[p:pf + 1]
        ob = args.find("{")
        if ob < 0:
            continue
        tem = chaves_do_objeto(args[ob:])
        conferidos += 1
        linha = js[:m.start()].count("\n") + 1
        for k, falas in exige.items():
            if k not in tem:
                falhas.append(
                    "%s() na linha ~%d do JS chama sem \"%s\" — mas a voz %s promete isso"
                    % (nome, linha, k, "/".join(sorted(set(falas))))
                )

print(arq + " -> promessa: %d ponto(s) de ajuda conferido(s) em %d ajudante(s)"
      % (conferidos, len(ajudantes)))
for nome, ops, corpo in ajudantes:
    ex = exigencias(corpo, ops)
    if ex:
        print("  %s() exige: %s" % (nome, ", ".join(sorted(ex.keys()))))
if not falhas:
    print("  promessa ok: toda fala de ajuda tem a acao correspondente na tela")
    sys.exit(0)
print("  %d PROMESSA(S) SEM CUMPRIR:" % len(falhas))
for f in falhas:
    print("   " + f)
sys.exit(1)
