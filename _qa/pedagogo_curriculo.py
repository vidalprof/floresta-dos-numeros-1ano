# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO DO PEDAGOGO — A PARTE DO CURRÍCULO ("está mesmo alinhada à rede?")

 ⭐ PERGUNTA DO MARCOS (set/2026): *"o pedagogo está bem criterioso quanto ao
    currículo e didática? Ele está especialista? Preciso que quando um professor
    olhe e analise a atividade ele veja que está ótima"*.

 ⚠️ ESTE PORTÃO É O IRMÃO DO `_qa/pedagogo.py`, NÃO O SUBSTITUTO. São as duas
    metades da mesma pergunta, e é importante não confundir:
      • `_qa/pedagogo.py` (0a)  -> a **DIDÁTICA**: concreto → figural →
        simbólico, o andaime que cresce, o aquecimento no meio, o problema antes
        do conceito. Essa metade já era medida desde ago/2026.
      • `_qa/pedagogo_curriculo.py` (0b9, este) -> o **CURRÍCULO**: a habilidade
        que a atividade diz cumprir existe mesmo no documento da rede, e o
        professor consegue VER isso sem depender da minha palavra.

 A segunda metade é que faltava. O que havia: `_qa/curriculo.py` só sabe de
 MATEMÁTICA (que tabuada cabe em que ano) e fica fora da banca automática;
 `_qa/curriculo_verbatim.py` confere citação, mas só em atividade montada; e o
 parecer pedagógico de cada caderno morava num `.md` do repositório — que
 professor nenhum abre.

 ────────────────────────────────────────────────────────────
 AS CINCO PERGUNTAS QUE ELE FAZ (cada uma nasce de um defeito real)

 1. A atividade DECLARA o currículo?  (`<pasta>/curriculo.json`)
    Sem declaração não há o que auditar, e o professor fica com "confie em mim".

 2. Cada habilidade citada EXISTE no currículo, palavra por palavra?
    ⚠️ Lição paga na Padaria das Letras: sete objetivos marcados "verbatim",
    dois deles escritos por MIM. Citação falsa de currículo é o único defeito
    que o professor não tem como pegar sozinho — ele teria que abrir 440
    páginas de PDF. Mesma regra do `_qa/curriculo_verbatim.py`: toda palavra
    marcante (5+ letras) da citação tem que existir no documento. Não se
    procura a frase inteira porque o PDF foi extraído em COLUNAS e chega aqui
    partida — portão que acusa inocente é portão que se aprende a ignorar.

 3. Os objetivos do RELATÓRIO e os do CURRÍCULO batem um a um?
    Nome por nome, folha por folha. Se alguém mexer no relatório e esquecer o
    `curriculo.json`, o dossiê passa a mentir para o professor — e ele é
    exatamente quem não tem como conferir.

 4. Toda folha com item é medida por ALGUM objetivo?
    Folha que nenhum objetivo cobre é trabalho que a criança faz e que não
    aparece no relatório: o professor lê "dominou" sobre metade do caderno.

 5. O DOSSIÊ está dentro da atividade, e mostrando ESTES dados?
    De nada adianta declarar num json que só o repositório vê. O `var
    CURRICULO` do index.html tem que ser o mesmo do `curriculo.json`, e o
    código do dossiê tem que estar no `folhas.js` — e a janela dele tem que vir
    ANTES do `<script src="folhas.js">` (ver o porquê lá embaixo).

 ────────────────────────────────────────────────────────────
 Uso:  python3 _qa/pedagogo_curriculo.py <pasta> [<pasta> ...]
 Código 0 = passou · 1 = REPROVADO · 2 = não deu para medir (não é "passou").
============================================================
"""
import io
import json
import os
import re
import sys
import unicodedata

CURRICULO = "_curriculo/blumenau.txt"
TAMANHO_MINIMO = 5

# rótulo nosso ao redor da citação, que legitimamente pode não estar no documento
NOSSAS = set(u"""habilidade habilidades objeto conhecimento conceitos conteudos
    campos atuacao analise linguistica semiotica alfabetizacao ano lingua
    portuguesa blumenau todos""".split())

_CITACAO = re.compile(u'HABILIDADE\\s*:\\s*[“"]([^”"]+)[”"]')
_OBJ = re.compile(r'\{n:\s*"([^"]+)",\s*f:\s*\[([^\]]*)\]', re.S)


def achata(s):
    s = unicodedata.normalize("NFD", s or u"")
    s = u"".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", u" ", s.lower())


def objetivos_do_relatorio(js):
    m = re.search(r"var OBJETIVOS = \[(.*?)\n\];", js, re.S)
    if not m:
        return None
    fora = []
    for n, f in _OBJ.findall(m.group(1)):
        fora.append((n, [int(x) for x in f.replace(" ", "").split(",") if x.strip()]))
    return fora


def confere(pasta, palavras):
    u"""devolve (codigo, [linhas]) para uma pasta."""
    pasta = pasta.rstrip("/")
    L = []
    ih = os.path.join(pasta, "index.html")
    fj = os.path.join(pasta, "folhas.js")
    cj = os.path.join(pasta, "curriculo.json")

    if not os.path.exists(fj) or not os.path.exists(ih):
        return 2, [u"   nao e um caderno de folha viva (sem index.html + folhas.js): NAO MEDI"]

    js = io.open(fj, encoding="utf-8").read()
    rel = objetivos_do_relatorio(js)
    if rel is None:
        return 2, [u"   sem `var OBJETIVOS` no folhas.js: NAO MEDI (isso nao e 'passou')"]

    # ---- 1. declarou?
    if not os.path.exists(cj):
        return 1, [u"   REPROVADO 1: o caderno tem relatorio com %d objetivos mas NAO declara"
                   u" o curriculo (falta %s). O professor fica sem como conferir o alinhamento."
                   % (len(rel), cj)]
    d = json.load(io.open(cj, encoding="utf-8"))
    objs = d.get("objetivos") or []
    ruim = 0

    # ---- 2. a citacao existe no curriculo?
    if palavras is None:
        L.append(u"   ⚠️ nao achei %s: NAO conferi as citacoes" % CURRICULO)
        ruim = max(ruim, 2)
    else:
        maus = []
        for o in objs:
            achou = _CITACAO.findall(o.get("habilidade") or u"")
            if not achou:
                maus.append((o.get("objetivo"), u"(sem citacao entre aspas)", []))
                continue
            for frase in achou:
                fora = [p for p in achata(frase).split()
                        if len(p) >= TAMANHO_MINIMO and p not in NOSSAS
                        and p not in palavras]
                if fora:
                    maus.append((o.get("objetivo"), frase, sorted(set(fora))))
        if maus:
            ruim = 1
            L.append(u"   REPROVADO 2: habilidade citada que o curriculo NAO tem:")
            for nome, frase, fora in maus:
                L.append(u"      • %s -> %s" % (nome, frase[:70]))
                if fora:
                    L.append(u"        palavras que nao existem no documento: %s"
                             % u", ".join(fora))
        else:
            L.append(u"   ✓ %d habilidade(s) citada(s) conferem com o curriculo, palavra por palavra"
                     % len(objs))

    # ---- 3. relatorio x curriculo, um a um
    nrel = [n for n, _ in rel]
    ncur = [o.get("objetivo") for o in objs]
    if nrel != ncur:
        ruim = 1
        L.append(u"   REPROVADO 3: os objetivos do relatorio e os do curriculo.json nao batem.")
        so_rel = [n for n in nrel if n not in ncur]
        so_cur = [n for n in ncur if n not in nrel]
        if so_rel:
            L.append(u"      so no relatorio: %s" % u"; ".join(so_rel))
        if so_cur:
            L.append(u"      so no curriculo.json: %s" % u"; ".join(so_cur))
        if not so_rel and not so_cur:
            L.append(u"      mesmos nomes, ORDEM diferente — o dossie listaria fora de ordem")
    else:
        dif = [(n, f, o.get("folhas"))
               for (n, f), o in zip(rel, objs) if list(f) != list(o.get("folhas") or [])]
        if dif:
            ruim = 1
            L.append(u"   REPROVADO 3: objetivo declarando folhas diferentes das que o relatorio mede:")
            for n, f, g in dif:
                L.append(u"      • %s -> relatorio %s, curriculo.json %s" % (n, f, g))
        else:
            L.append(u"   ✓ os %d objetivos do relatorio e do curriculo batem, nome e folhas"
                     % len(objs))

    # ---- 4. toda folha com item e medida
    ihtxt = io.open(ih, encoding="utf-8").read()
    mn = re.search(r"var NOMES = \[(.*?)\];", ihtxt, re.S)
    if mn:
        nomes = re.findall(r'"([^"]*)"', mn.group(1))
        # a ULTIMA folha e o mural/fecho: nao tem item, entao nao se mede
        deviam = set(range(1, len(nomes)))
        medidas = set()
        for _, f in rel:
            medidas |= set(f)
        soltas = sorted(deviam - medidas)
        if soltas:
            ruim = 1
            L.append(u"   REPROVADO 4: folha(s) que nenhum objetivo mede — a crianca "
                     u"trabalha e o relatorio nao conta: %s"
                     % u", ".join(u"%d (%s)" % (i, nomes[i - 1]) for i in soltas))
        else:
            L.append(u"   ✓ todas as %d folhas de trabalho aparecem em algum objetivo"
                     % len(deviam))
    else:
        L.append(u"   ⚠️ sem `var NOMES`: nao conferi a cobertura das folhas")
        ruim = max(ruim, 2)

    # ---- 5. o dossie esta na atividade e mostra ESTES dados
    falta = []
    if u"var CURRICULO" not in ihtxt:
        falta.append(u"`var CURRICULO` no index.html")
    if u"dossieHTML" not in js:
        falta.append(u"o codigo do dossie no folhas.js")
    if u'id="dossie"' not in ihtxt:
        falta.append(u"a janela #dossie")
    if u'id="bDossie"' not in ihtxt:
        falta.append(u"o botao do dossie no menu do professor")
    # ⚠️ ORDEM NO DOM, e ela e silenciosa: o codigo do dossie amarra o botao
    #    Fechar e o clique no fundo no momento em que carrega. Se a janela
    #    estiver DEPOIS do <script src="folhas.js">, os dois saem nulos e o
    #    dossie abre SEM COMO FECHAR. Aconteceu na estreia (11/set/2026) e o
    #    print nao mostrava: a janela aparecia bonita, so nao fechava.
    ja = ihtxt.find(u'id="dossie"')
    sc = ihtxt.find(u'<script src="folhas.js">')
    if ja > -1 and sc > -1 and ja > sc:
        falta.append(u'a janela #dossie ANTES do <script src="folhas.js"> '
                     u"(depois dele, o botao Fechar nasce sem funcao)")
    if falta:
        ruim = 1
        L.append(u"   REPROVADO 5: o professor nao ve o dossie dentro da atividade — falta %s."
                 u" Rode: python3 _padrao/dossie_professor.py %s" % (u"; ".join(falta), pasta))
    else:
        mc = re.search(r"var CURRICULO = (\{.*?\n\});", ihtxt, re.S)
        try:
            emtela = json.loads(mc.group(1)) if mc else None
        except Exception:
            emtela = None
        if emtela is None:
            ruim = 1
            L.append(u"   REPROVADO 5: nao consegui ler o `var CURRICULO` do index.html")
        elif emtela != d:
            ruim = 1
            L.append(u"   REPROVADO 5: o dossie na TELA esta diferente do curriculo.json "
                     u"(alguem mexeu num e nao no outro). Rode: python3 "
                     u"_padrao/dossie_professor.py %s" % pasta)
        else:
            L.append(u"   ✓ o dossie esta na atividade e mostra exatamente o curriculo.json")

    return ruim, L


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/pedagogo_curriculo.py <pasta> [<pasta> ...]")
        return 2
    palavras = None
    if os.path.exists(CURRICULO):
        palavras = set(achata(io.open(CURRICULO, encoding="utf-8").read()).split())
    pior = 0
    for pasta in sys.argv[1:]:
        c, linhas = confere(pasta, palavras)
        marca = u"OK" if c == 0 else (u"REPROVADO" if c == 1 else u"NAO MEDI")
        print(u"%s -> %s" % (pasta.rstrip("/"), marca))
        for l in linhas:
            print(l)
        pior = 1 if (pior == 1 or c == 1) else max(pior, c)
    return pior


if __name__ == "__main__":
    sys.exit(main())
