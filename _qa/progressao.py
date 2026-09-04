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

# 3) transicoes. Duas formas de passar de fase, e as DUAS contam:
#    - mostraBanner(mensagem, proximaTela)  -> o caminho comum
#    - proximaTela()                        -> chamada direta (sem banner)
#    A primeira versao deste auditor so olhava o banner e por isso NAO viu as
#    quedas do Plantao na Redacao (56% -> 36%). Agora olha as duas.
REINICIO = ("telaCapa", "telaMenu")   # "jogar de novo" e voltar ao menu nao contam
ruins = []
for nome, corpo in corpos.items():
    if prog[nome] is None:
        continue
    alvos = set(re.findall(r"mostraBanner\([^,]+,\s*([A-Za-z_$][\w$]*)\s*\)", corpo))
    alvos |= set(re.findall(r"(?:^|[^\w.$])([A-Za-z_$][\w$]*)\(\)\s*;", corpo))
    for alvo in sorted(alvos):
        if alvo == nome or alvo in REINICIO:
            continue
        # ⚠️ LICAO PAGA (ago/2026, Lojinha): "JOGAR DE NOVO" da PECA. A tela de
        #    fim (100%) tem um botao que chama a ENTRADA da peca (pecaLigar,
        #    pecaEscolher...) para recomecar do 0%. Isso e REPLAY — a mesma coisa
        #    que telaCapa, escolha da crianca, nao "perdi o que fiz". E numa
        #    atividade MONTADA esse loop e codigo MORTO: o motor avanca as fases,
        #    o botao e trocado. So o telaCapa estava isento; a entrada da peca
        #    (pecaX, indo de ~100% de volta a 0%) e o mesmo caso.
        # ⚠️ LICAO PAGA (set/2026, peca `divisao-dourado`): este `prog[alvo]`
        #    supunha que toda funcao `pecaX` estivesse na tabela — e a tabela
        #    so tem as telas que CHAMAM `setProg`. A entrada da peca nova nao
        #    chama (quem desenha a barra la e o motor), entao o portao ESTOUROU
        #    com KeyError em vez de medir. Portao que quebra e portao que nao
        #    mede: pior que reprovar. Agora pergunta antes de ler.
        if re.match(r"peca[A-Z]", alvo) and prog.get(alvo) == 0 and prog[nome] >= 95:
            continue
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
