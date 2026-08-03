# -*- coding: utf-8 -*-
# ============================================================
#  AUDITOR DE PROGRESSAO — "a barra anda sempre para a frente?"
#
#  Nasceu de um achado do Marcos (ago/2026), quando ele perguntou se as
#  atividades estavam "didaticas, com progressao". Fui medir e descobri que
#  em TRES delas a barra ANDAVA PARA TRAS no meio do percurso:
#     Legenda do Clique   68% -> 48%   (a pior: a crianca sente que perdeu tudo)
#     Plantao na Redacao  50% -> 46%  e  82% -> 80%
#     Doceria do Cacau    92% -> 91%
#  Acontece sempre pelo mesmo motivo: fases sao inseridas depois e ninguem
#  renumera o setProg das vizinhas. Nenhum print pega isso — so comparando a
#  ORDEM REAL das fases com o numero que cada uma pinta na barra.
#
#  Como funciona: acha toda funcao-tela (a que chama limpa()), le o setProg
#  dela e segue os mostraBanner(msg, proximaTela). Se alguma transicao cair
#  para um numero MENOR, reprova.
#
#  Uso: python3 _qa/progressao.py <arquivo.html>
# ============================================================
import io, re, sys

arq = sys.argv[1] if len(sys.argv) > 1 else ""
if not arq:
    print("uso: python3 _qa/progressao.py <arquivo.html>")
    sys.exit(2)

html = io.open(arq, encoding="utf-8").read()
js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))

# 1) corpo de cada tela (funcao que chama limpa())
corpos = {}
for m in re.finditer(r"^function\s+([A-Za-z_$][\w$]*)\s*\(", js, re.M):
    nome = m.group(1)
    ini = js.find("{", m.end())
    prof, k = 0, ini
    while k < len(js):
        if js[k] == "{":
            prof += 1
        elif js[k] == "}":
            prof -= 1
            if prof == 0:
                break
        k += 1
    corpo = js[ini:k]
    if re.search(r"\blimpa\(\)", corpo):
        corpos[nome] = corpo

# 2) numero que cada tela pinta na barra
prog = {}
for nome, corpo in corpos.items():
    m = re.search(r"setProg\(\s*\w+\s*,\s*(\d+)", corpo)
    prog[nome] = int(m.group(1)) if m else None

# 3) transicoes: o banner do fim de fase diz qual e a proxima
ruins = []
for nome, corpo in corpos.items():
    if prog[nome] is None:
        continue
    for alvo in sorted(set(re.findall(r"mostraBanner\([^,]+,\s*([A-Za-z_$][\w$]*)\s*\)", corpo))):
        if alvo in corpos and prog[alvo] is not None and prog[alvo] < prog[nome]:
            ruins.append((nome, prog[nome], alvo, prog[alvo]))

print("%s -> %d telas com barra de progresso" % (arq, len([p for p in prog.values() if p is not None])))
if not ruins:
    print("   progressao ok: a barra so anda para a frente")
    sys.exit(0)
print("   %d TRANSICAO(OES) EM QUE A BARRA VOLTA (a crianca acha que perdeu o que fez):" % len(ruins))
for nome, pn, alvo, pa in sorted(ruins, key=lambda x: x[1] - x[3], reverse=True):
    print("    %s (%d%%) -> %s (%d%%)   caiu %d pontos" % (nome, pn, alvo, pa, pn - pa))
print("   conserte renumerando o setProg das telas na ORDEM REAL em que elas aparecem.")
sys.exit(1)
