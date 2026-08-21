# -*- coding: utf-8 -*-
u"""Gera _detetive/conteudo.json — A AGÊNCIA DOS DETETIVES DAS PALAVRAS (5º ano, Português).

REVISÃO / REFORÇO de assuntos já estudados (pedido do Marcos):
  · PRONOMES (pessoais, possessivos, demonstrativos, de tratamento);
  · INTERPRETAÇÃO de textos NARRATIVOS (quem, o quê, quando, sequência, causa);
  · INTERPRETAÇÃO de textos INJUNTIVOS (finalidade, passos, verbos de comando);
  · MAU (com U = adjetivo, o contrário de BOM) × MAL (com L = advérbio, o
    contrário de BEM).

ENREDO (o "porquê" — EDUVERSE): a criança é um(a) DETETIVE JÚNIOR da agência da
raposa Vera. Cada caso só se resolve LENDO o texto e usando as palavras certas —
o problema vem ANTES do conceito; a gramática é ferramenta do detetive, nunca
prova. Fecho com gancho (um novo caso na caixa de correio).

PIPELINE (padrão ESQUELETO — vale para QUALQUER atividade; ver CLAUDE.md):
  1) este build_conteudo.py escreve conteudo.json (CONTEUDO + fases DADO);
  2) python3 _padrao/ESQUELETO/integrar.py --escrever  (compila as peças);
  3) python3 _padrao/ESQUELETO/montar.py _detetive      (gera index.html,
     falas.json, arte.json, sw.js — o motor blindado já vem embutido);
  4) gerar a ARTE (o Marcos gera pelos prompts; o Claude consulta o _banco antes
     e só pede o que faltar — REGRA DO BANCO, CLAUDE.md);
  5) bancada (bash _qa/auditar.sh) + revisor + publicar por entregar.yml.

⚠️ REGRA DO BANCO (nova, ago/2026): antes de pedir arte, CONSULTAR o _banco
   (o montador reporta no_banco × gerar); reusar o que existe; o que faltar, o
   Marcos gera pelos prompts abaixo. Mascote/cenário/medalha desta atividade são
   NOVOS (o Marcos autorizou gerar).
"""
import io, json, os

PASTA = os.path.dirname(os.path.abspath(__file__))

# ---- BNCC 5º ano (revisão) — habilidades-âncora do parecer do professor ----
HAB = (u"Reconhecer e usar pronomes (pessoais, possessivos, demonstrativos e de "
       u"tratamento) na coesão do texto; localizar informações e inferir sentidos "
       u"em textos narrativos e injuntivos; e empregar corretamente MAU/MAL "
       u"conforme a classe (adjetivo × advérbio). EF05LP a EF35LP (revisão).")

CONTEUDO = {
 u"titulo": u"A Agência dos Detetives das Palavras",
 u"sub": u"Português · 5º ano · Pronomes, interpretação (narrativo/injuntivo), mau × mal",
 u"ano": u"5º ano",
 u"prefixo": u"dp",
 u"mascote": u"raposa",
 u"mascoteNome": u"Detetive Vera",
 u"crachas": 6,
 u"fundo": u"dp_fundo",
 u"voz": u"feminina",
 u"abertura": (u"Bem-vindo(a) à Agência! Sou a detetive Vera. Cada caso só se "
               u"resolve LENDO com atenção e usando as palavras certas. Vamos?"),
 u"fim": u"Caso encerrado, detetive! Você lê como quem enxerga o que os outros não veem.",
 # os rótulos que o RELATÓRIO do professor mostra (conceito -> nome de criança)
 u"conceitos": {
   u"objetivo1": u"Pronomes (pessoais, possessivos, demonstrativos, tratamento)",
   u"objetivo2": u"Interpretar texto narrativo (quem, o quê, sequência)",
   u"objetivo3": u"Interpretar texto injuntivo (finalidade e passos)",
   u"objetivo4": u"Mau (adjetivo) × Mal (advérbio)",
 },
 u"curriculo": HAB,
 u"fases": [],   # <- preenchido pelos blocos abaixo (em construção)
}

# ============================================================
#  PLANO DE FASES (o roteiro — variedade de gestos, ~4 blocos)
#  Cada fase é DADO; ~2–3 rodadas para encher a aula sem arte nova.
#  Gestos previstos (leque grande, nenhum > 40%): escolher, ligar,
#  classificar, completar, ordenar, quem-sou-eu, caca-palavras, intruso,
#  memoria, digitar/forca.
#
#  BLOCO 1 — PRONOMES (objetivo1)
#   f01 escolher     — qual pronome substitui o nome grifado
#   f02 ligar        — pronome ↔ palavra que ele substitui
#   f03 classificar  — gavetas: pessoal / possessivo / demonstrativo / tratamento
#   f04 completar    — preencher a lacuna com o pronome certo (coesão)
#   f05 caca-palavras— achar pronomes escondidos
#
#  BLOCO 2 — TEXTO NARRATIVO (objetivo2)
#   f06 (texto curto) escolher — quem/o quê/quando
#   f07 ordenar      — pôr os fatos na ordem em que aconteceram
#   f08 quem-sou-eu  — descobrir o personagem pelas pistas do texto
#   f09 escolher     — inferência (por que o personagem fez X)
#
#  BLOCO 3 — TEXTO INJUNTIVO (objetivo3)  [receita / regras / manual]
#   f10 escolher     — qual a FINALIDADE do texto (para que serve)
#   f11 ordenar      — pôr os PASSOS na ordem certa
#   f12 intruso      — qual frase NÃO é uma instrução (verbo de comando)
#   f13 completar    — completar o passo com o verbo no imperativo
#
#  BLOCO 4 — MAU × MAL (objetivo4)
#   f14 escolher     — mau ou mal na frase (troca por bom/bem para decidir)
#   f15 classificar  — gavetas MAU (adjetivo, = bom) / MAL (advérbio, = bem)
#   f16 completar    — preencher com mau/mal
#   f17 digitar/forca— escrever mau/mal certo
#   AQUECIMENTO      — revisão espaçada no meio (mistura pronome + mau/mal)
#
#  FIM: boletim animado + relatório do professor (FIM-DE-ATIVIDADE.md) +
#       gancho (um novo caso na caixa de correio).
# ============================================================

fases = []
def add(**k): fases.append(k)

def esc(p, c, e, d):
    u"""escolher só de texto (gramática): sem imagem."""
    return {u"img":u"", u"p":p, u"c":c, u"e":e, u"d":d}

# ============================================================
# BLOCO 1 — PRONOMES (objetivo1)
# ============================================================

# f01 — ESCOLHER: qual pronome PESSOAL substitui o nome
add(id=u"f01", mec=u"escolher", selo=u"CASO 1: O PRONOME CERTO", conceito=u"objetivo1",
    enunciado=u"Leia a pista e escolha o <b>pronome</b> que substitui a palavra grifada.",
    dica=u"Pronome pessoal troca o nome: ele, ela, nós, eles...",
    dados=[
      esc(u"<b>Ana</b> achou a pista. ___ sorriu.", u"ELA", [u"ELE", u"NÓS"],
          [u"Ana é uma menina, no singular.", u"Uma pessoa, feminino: qual serve?",
           u"É <b>ELA</b>. Toque para seguir."]),
      esc(u"<b>Os detetives</b> voltaram. ___ resolveram o caso.", u"ELES", [u"ELE", u"ELA"],
          [u"São vários, no masculino.", u"Vários homens: plural masculino.",
           u"É <b>ELES</b>. Toque para seguir."]),
      esc(u"<b>Eu e você</b> vamos investigar. ___ formamos a dupla.", u"NÓS", [u"ELES", u"VOCÊS"],
          [u"Eu + você = a gente, juntos.", u"Quem inclui quem fala: nós.",
           u"É <b>NÓS</b>. Toque para seguir."]),
    ], dadosExtra={u"TITULO":u"O PRONOME CERTO", u"FECHO":u"Você trocou os nomes pelos pronomes certos!"})

# f02 — LIGAR: pronome <-> a palavra que ele substitui
add(id=u"f02", mec=u"ligar", selo=u"CASO 1: LIGUE AS PISTAS", conceito=u"objetivo1",
    enunciado=u"Ligue cada <b>pronome</b> à palavra que ele substitui.",
    dica=u"Veja o número (singular/plural) e o gênero (masculino/feminino).",
    dados=[{u"k":u"p0", u"t":u"ELA", u"s":u"a menina"},
           {u"k":u"p1", u"t":u"ELE", u"s":u"o cachorro"},
           {u"k":u"p2", u"t":u"ELES", u"s":u"os meninos"},
           {u"k":u"p3", u"t":u"NÓS", u"s":u"eu e você"}],
    dadosExtra={u"DICAS":[u"Pense em quantos são e se é menino ou menina.",
                          u"ELA = uma menina; ELES = vários; NÓS = eu + você.",
                          u"A resposta certa acende no fim da linha. Toque nela."],
                u"FEITOS":[], u"ENUN":u"Ligue o pronome à palavra que ele substitui.",
                u"FECHO":u"Cada pronome no lugar certo!"})

# f03 — CLASSIFICAR: os TIPOS de pronome (gavetas)
add(id=u"f03", mec=u"classificar", selo=u"CASO 1: SEPARE OS PRONOMES", conceito=u"objetivo1",
    enunciado=u"Cada <b>pronome</b> na sua gaveta: pessoal, possessivo ou demonstrativo?",
    dica=u"Pessoal = quem fala/ouve (eu, tu, ele); possessivo = de quem é (meu, teu); demonstrativo = onde está (este, esse, aquele).",
    dados=[{u"k":u"pes", u"n":u"PESSOAL", u"img":u"", u"voz":u"pessoal", u"rot":False},
           {u"k":u"pos", u"n":u"POSSESSIVO", u"img":u"", u"voz":u"possessivo", u"rot":False},
           {u"k":u"dem", u"n":u"DEMONSTRATIVO", u"img":u"", u"voz":u"demonstrativo", u"rot":False}],
    dadosExtra={u"FICHAS":[
      {u"t":u"EU", u"alvo":u"pes"}, {u"t":u"ELE", u"alvo":u"pes"},
      {u"t":u"MEU", u"alvo":u"pos"}, {u"t":u"NOSSO", u"alvo":u"pos"},
      {u"t":u"ESTE", u"alvo":u"dem"}, {u"t":u"AQUELE", u"alvo":u"dem"}],
      u"DICAS":[u"EU e ELE dizem QUEM; MEU e NOSSO dizem DE QUEM; ESTE e AQUELE dizem ONDE.",
                u"Possessivo combina com 'é meu, é nosso'. Demonstrativo com 'este aqui, aquele lá'.",
                u"Olhe a gaveta com a borda amarela: é ali que esta ficha mora."],
      u"ENUN":u"Toque no <b>pronome</b>. Depois toque na <b>gaveta do tipo</b> dele."})

# f04 — COMPLETAR: o pronome que dá coesão à frase
add(id=u"f04", mec=u"completar", selo=u"CASO 1: COMPLETE A PISTA", conceito=u"objetivo1",
    enunciado=u"Complete a frase com o <b>pronome</b> que falta.",
    dica=u"O pronome tem que combinar com a palavra que ele substitui.",
    dados=[{u"img":u"", u"ante":u"Cadê o meu caderno? ", u"dep":u" está na mochila.",
            u"cer":u"Ele", u"out":[u"Ela", u"Eles"], u"dic":u"Caderno é 'o' — masculino, singular."},
           {u"img":u"", u"ante":u"As lupas são novas. ", u"dep":u" brilham.",
            u"cer":u"Elas", u"out":[u"Ele", u"Eles"], u"dic":u"Lupas são 'as' — feminino, plural."},
           {u"img":u"", u"ante":u"Esta é a casa de vocês? Sim, ", u"dep":u" é nossa.",
            u"cer":u"ela", u"out":[u"ele", u"eles"], u"dic":u"Casa é 'a' — feminino, singular."}],
    dadosExtra={u"ENUN":u"Toque no pedaço que <b>falta</b> na frase.",
                u"DEPOIS":u"Leia a frase inteira antes de escolher.",
                u"FECHO":u"Você completou as pistas com os pronomes!"})

# f05 — CAÇA-PALAVRAS: achar pronomes escondidos
add(id=u"f05", mec=u"caca-palavras", selo=u"CASO 1: PRONOMES ESCONDIDOS", conceito=u"objetivo1",
    enunciado=u"Ache os <b>pronomes</b> escondidos no quadro.",
    dica=u"Estão deitados (→) e em pé (↓): EU, ELE, ELA, MEU, ESTE.",
    dados=[u"EU", u"ELE", u"ELA", u"MEU", u"ESTE"],
    dadosExtra={u"MODO":u"lista", u"TITULO":u"PRONOMES ESCONDIDOS",
                u"LETRAS":u"ABCDEHILMNOPRSTU", u"DIFICIL":u"",
                u"CORP":[u"p1", u"p2", u"p3", u"p4", u"p5"]})

CONTEUDO[u"fases"] = fases
io.open(os.path.join(PASTA, u"conteudo.json"), u"w", encoding=u"utf-8").write(
    json.dumps(CONTEUDO, ensure_ascii=False, indent=1))
print(u"conteudo.json: %d fases (EM CONSTRUÇÃO)" % len(fases))
