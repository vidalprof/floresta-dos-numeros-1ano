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

# >>> OS BLOCOS DE FASE ENTRAM AQUI (em construção — próximos commits) <<<

CONTEUDO[u"fases"] = fases
io.open(os.path.join(PASTA, u"conteudo.json"), u"w", encoding=u"utf-8").write(
    json.dumps(CONTEUDO, ensure_ascii=False, indent=1))
print(u"conteudo.json: %d fases (EM CONSTRUÇÃO)" % len(fases))
