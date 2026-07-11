#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDITOR DE PEDAGOGIA / NEUROCIÊNCIA DO APRENDIZADO — o "profissional" que cobre a
frente de APRENDER DE VERDADE + QUERER FAZER (engajamento). Como os outros
auditores, ele vira BARREIRA: procura, no HTML da atividade, os MARCADORES das
técnicas com base em evidência (retrieval practice, espaçamento, intercalação,
feedback elaborativo, mentalidade de crescimento, codificação dupla, competência
visível, autonomia, curiosidade, carga cognitiva baixa).

É HEURÍSTICO (procura sinais no código) — não substitui o olhar humano, mas
impede que uma atividade "quiz puro e chato" passe sem os ingredientes que fazem
a criança aprender e QUERER fazer. Cada item ausente é um AVISO a resolver.

Uso:  python3 _circo/auditar-pedagogia.py <arquivo.html> [--rigoroso]
      (--rigoroso: sai != 0 se faltar item essencial)
"""
import sys, re, os

# marcador: (chave, essencial?, descrição, lista de regex — basta 1 casar)
CHECKS = [
    ("retrieval", True,
     "Recuperação ativa (a criança PRODUZ a resposta, não só relê)",
     [r'compConfere|montarConfere|forcaChute|responder|conferir', r'opcoes\s*:', r'MASCOTE_POSES|desafio']),
    ("feedback_explica", True,
     "Feedback imediato e ELABORATIVO (explica o PORQUÊ do erro/acerto)",
     [r'\bexplica\b', r'dd\.explica']),
    ("erro_sem_punir", True,
     "Erro sem punir + mentalidade de crescimento (elogia esforço, normaliza o erro)",
     [r'vamos contar juntos', r'errar e treinar', r'[Nn]ão foi dessa vez',
      r'tentar de novo', r'[Qq]uase!', r'sem punir|com carinho']),
    ("espacamento", True,
     "Revisão ESPAÇADA dos erros (reforço reapresenta o que a criança errou, depois)",
     [r'[Rr]efor[çc]o', r'guardarErro|dEfase|revis|STATS|errad']),
    ("intercalacao", False,
     "Intercalação (embaralha tipos/itens em vez de blocos iguais)",
     [r'embaralhar|montarMix|MIX_FIXO|shuffle|Math\.random']),
    ("dual_coding", True,
     "Codificação dupla (palavra + IMAGEM juntas — duas rotas de memória)",
     [r'figura\(|IMG\[|data:image|svg[A-Z]|MASCOTE|<img|img/|\.png']),
    ("competencia", True,
     "Competência VISÍVEL (progresso: barra, X de N, níveis, medalhas, selos)",
     [r'barra|progress|NIVEIS|nivel|medalha|selo|emblema|PONTOS|contarFeitas']),
    ("autonomia", False,
     "Autonomia (a criança ESCOLHE algo: ordem, aceitar o Extra, o nome)",
     [r'desafioExtra|desafio_extra|escolh|campoNome|nomeAluno']),
    ("personalizacao", False,
     "Pertencimento/personalização (mascote fala com a criança; usa o NOME)",
     [r'nomeAluno', r'MASCOTE|mascote']),
    ("curiosidade", False,
     "Curiosidade/novidade (gancho de história p/ a próxima tela; surpresa)",
     [r'GANCHOS|ganchoDe|gancho', r'cena|historia|história|enredo']),
    ("celebracao", True,
     "Feedback 'juicy' + celebração (som + animação + confete no acerto; grande final)",
     [r'confete|comemorar|somAcerto|fanfarra|grandeFinal']),
    ("carga_cognitiva", False,
     "Carga cognitiva baixa (narração curta/1ª vez, uma ideia por tela — anti-cansaço)",
     [r'narrarTela|_telasNarradas|VOZ_EXPLICA|FAIXA|falarComposto|_gatearAvanco']),
    ("adaptativo", False,
     "Dificuldade desejável / adaptativa (Extra p/ quem vai bem, Reforço p/ quem erra)",
     [r'desafioExtra|Extra|[Rr]efor[çc]o|nivelAtual']),
]


def auditar(src):
    h = open(src, encoding="utf-8").read()
    # MODO PROVA (avaliacao): NAO mostra certo/errado nem explica o erro DE PROPOSITO.
    # Nesse caso feedback/erro-sem-punir/espacamento/adaptativo sao intencionalmente
    # ausentes — nao contam como falha essencial (mas retrieval, dual coding,
    # competencia, celebracao e carga cognitiva continuam valendo).
    modo_prova = bool(re.search(r'URL_PLANILHA|FIREBASE_DB|enviarResultado|enviarPlanilha|\bprova\b|avalia', h, re.I))
    RELAXA = {"feedback_explica", "erro_sem_punir", "espacamento", "adaptativo"}
    presentes, faltando_ess, faltando_op = [], [], []
    for chave, essencial, desc, regexes in CHECKS:
        achou = any(re.search(rx, h) for rx in regexes)
        ess = essencial and not (modo_prova and chave in RELAXA)
        if achou:
            presentes.append((chave, desc))
        elif ess:
            faltando_ess.append((chave, desc))
        else:
            faltando_op.append((chave, desc + (" [modo prova: opcional]" if (modo_prova and chave in RELAXA) else "")))
    return presentes, faltando_ess, faltando_op, modo_prova


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    rigoroso = "--rigoroso" in sys.argv
    if not args:
        print("uso: python3 _circo/auditar-pedagogia.py <arquivo.html> [--rigoroso]")
        sys.exit(2)
    src = args[0]
    if not os.path.exists(src):
        print("arquivo nao encontrado:", src); sys.exit(2)

    presentes, faltando_ess, faltando_op, modo_prova = auditar(src)
    total = len(CHECKS)
    print("  🧠 NEUROCIÊNCIA DO APRENDIZADO%s — %d/%d marcadores presentes" % (
        " (MODO PROVA)" if modo_prova else "", len(presentes), total))
    for _, d in presentes:
        print("    ✓", d)
    for _, d in faltando_op:
        print("    ~ (recomendado, ausente):", d)
    for _, d in faltando_ess:
        print("    ✗ FALTA (essencial):", d)
    ok = not faltando_ess
    print("== RESUMO PEDAGOGIA: %s ==" % (
        "APROVADO (ingredientes de aprendizado+engajamento presentes)" if ok
        else "REVISAR — %d ingrediente(s) ESSENCIAL(is) ausente(s)" % len(faltando_ess)))
    # por padrão só AVISA (heurístico); com --rigoroso vira barreira dura
    sys.exit(1 if (rigoroso and not ok) else 0)


if __name__ == "__main__":
    main()
