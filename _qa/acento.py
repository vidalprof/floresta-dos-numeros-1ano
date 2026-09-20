# -*- coding: utf-8 -*-
# ============================================================
#  AUDITOR DE ACENTO — "a voz vai ler a palavra CERTA?"
#
#  Nasceu de um erro bobo que se repetia SEMPRE (Marcos, set/2026:
#  *"esses erros bobos se repetem sempre"*): a grade de caça-palavras (e a
#  forca, a cruzadinha, as letras-escondidas) NAO carrega cedilha nem acento,
#  entao a palavra vinha escrita crua — "ROCA" — e o rotulo E a voz liam esse
#  texto cru: a voz dizia "roca" (a de fiar) no lugar de "roca" (o campo).
#
#  O conserto ANTIGO era uma LISTA de 15 palavras no montar.py. Lista feita a
#  mao SEMPRE fica pra tras: o proximo erro e uma palavra NOVA que nao esta
#  nela. Este portao NAO tem lista: ele APRENDE o vocabulario do proprio
#  projeto — toda palavra acentuada que qualquer atividade ja escreveu — e
#  cobra a forma acentuada quando a grade traz a versao crua.
#
#  Como a peca agora DOBRA o acento so na grade (Ç->C), a palavra DEVE ser
#  escrita acentuada: o chip mostra e a voz le com acento; a grade fica ASCII
#  sozinha. Este portao garante que ninguem esqueca de acentuar.
#
#  Uso (banca):    python3 _qa/acento.py <pasta|conteudo.json|index.html>
#  Uso (montador): from acento import checa_conteudo; checa_conteudo(conteudo)
# ============================================================
import collections
import glob
import io
import json
import os
import re
import sys
import unicodedata

# as mecanicas que tiram o acento por CONSTRUCAO (letra/grade em ASCII). So
# nelas a palavra crua e defeito — em prosa o acento e natural.
FAMILIA_GRADE = ("caca-palavras", "forca", "cruzadinha", "letras-escondidas")

_ACENTO = re.compile(u"[À-ſ]")   # tem algum caractere acentuado?
_PAL = re.compile(u"[A-Za-zÀ-ſ]{2,}")


def _tira(s):
    u"""remove acento/cedilha, mantendo a letra base."""
    return u"".join(c for c in unicodedata.normalize("NFD", s)
                    if unicodedata.category(c) != "Mn")


def _raiz():
    u"""a raiz do projeto (onde moram as pastas _*/)."""
    aqui = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(aqui, ".."))


def constroi_vocabulario():
    u"""Le TODAS as falas/conteudos do projeto e devolve dois mapas:
       mp[ascii_maiusculo] = Counter(forma_acentuada) — o que o projeto usa;
       cru[ascii_maiusculo] = quantas vezes a palavra aparece SEM acento
       (para nao acusar palavra que tambem existe crua de verdade)."""
    raiz = _raiz()
    mp = collections.defaultdict(collections.Counter)
    cru = collections.Counter()
    arqs = (glob.glob(os.path.join(raiz, "_*", "falas.json")) +
            glob.glob(os.path.join(raiz, "_*", "conteudo.json")))
    for a in arqs:
        try:
            txt = io.open(a, encoding="utf-8").read()
        except Exception:                                      # noqa: BLE001
            continue
        for w in _PAL.findall(txt):
            wu = w.upper()
            if _ACENTO.search(w):
                mp[_tira(wu)][wu] += 1
            else:
                cru[wu] += 1
    return mp, cru


def _palavras_de_grade(fase):
    u"""as palavras que a peca de grade poe letra a letra (o campo `dados`)."""
    out = []
    dados = fase.get("dados")
    if isinstance(dados, list):
        for x in dados:
            if isinstance(x, str):
                out.append(x)
            elif isinstance(x, dict):
                for k in ("palavra", "p", "w", "resp", "resposta"):
                    if isinstance(x.get(k), str):
                        out.append(x[k])
                        break
    return out


def checa_conteudo(conteudo, mp=None, cru=None):
    u"""Confere um conteudo.json (dict ou lista de fases) e devolve os achados
    como tuplas (fase_id, mec, crua, acentuada). Lista vazia = ok. E a MESMA
    funcao que o montar.py chama, fonte unica de verdade."""
    if mp is None or cru is None:
        mp, cru = constroi_vocabulario()
    fases = conteudo.get("fases", conteudo) if isinstance(conteudo, dict) else conteudo
    if not isinstance(fases, list):
        return []
    achados = []
    for f in fases:
        if not isinstance(f, dict) or f.get("mec") not in FAMILIA_GRADE:
            continue
        for w in _palavras_de_grade(f):
            if _ACENTO.search(w):
                continue                        # ja acentuada
            wu = w.upper()
            cand = mp.get(_tira(wu))
            if not cand:
                continue
            acent = cand.most_common(1)[0][0]
            if acent == wu:
                continue
            n_ac = sum(cand.values())
            n_cru = cru.get(wu, 0)
            # so acusa quando a forma acentuada e a REGRA no projeto (>=2 usos)
            # e a crua nao e mais comum que ela (senao e palavra ambigua legitima)
            if n_ac >= 2 and n_ac >= n_cru:
                achados.append((f.get("id", "?"), f.get("mec"), wu, acent))
    return achados


def constroi_vocabulario_fora(pasta):
    u"""o vocabulario do projeto SEM a pasta que esta sendo medida.

    ⚠️ Sem isto o portao se envenena: as proprias falas cruas do caderno em
       exame entram na contagem `cru` e passam a defender o erro que ele devia
       acusar. Quanto mais palavra errada, menos o portao reclama.
    """
    import glob as _g
    raiz = _raiz()
    alvo = os.path.normpath(os.path.abspath(pasta))
    mp = collections.defaultdict(collections.Counter)
    cru = collections.Counter()
    arqs = (_g.glob(os.path.join(raiz, "_*", "falas.json")) +
            _g.glob(os.path.join(raiz, "_*", "conteudo.json")))
    for a in arqs:
        if os.path.normpath(os.path.dirname(os.path.abspath(a))) == alvo:
            continue
        try:
            txt = io.open(a, encoding="utf-8").read()
        except Exception:                                      # noqa: BLE001
            continue
        for w in _PAL.findall(txt):
            wu = w.upper()
            if _ACENTO.search(w):
                mp[_tira(wu)][wu] += 1
            else:
                cru[wu] += 1
    return mp, cru


def checa_prosa(pasta):
    u"""FOLHA VIVA: a PROSA que a crianca le e a voz diz esta acentuada?

    ⚠️ POR QUE ESTE SEGUNDO OLHO EXISTE (20/set/2026). O portao nasceu olhando
       a GRADE — palavra crua num caca-palavras, que a voz lia errado. Mas ele
       so sabe ler `conteudo.json`, e CADERNO DE FOLHA VIVA NAO TEM
       `conteudo.json`: em todos eles ele respondia "NAO MEDI (fora do
       padrao)". Resultado medido no `_corpo5`: CINQUENTA frases foram para a
       tela e para a voz sem acento — "por onde a digestao comeca", "o orgao
       que tem parte delgada", "Isso! O CORACAO bombeia o sangue". Quem achou
       fui eu, OLHANDO uma foto da folha 8 — nenhum dos 35 portoes viu.
       Aqui a pergunta e a inversa da outra: na grade, palavra crua e o certo
       (a grade nao carrega acento); na PROSA, palavra crua e defeito.
       A regra de prova e a mesma da outra metade: so acusa quando a forma
       acentuada e a REGRA no resto do projeto (>=2 usos) e a crua nao e mais
       comum que ela — assim "para", "e", "ate mais" e companhia nao viram
       alarme falso.
    """
    cam = os.path.join(pasta, "falas.json")
    if not os.path.exists(cam):
        return None
    try:
        falas = json.load(io.open(cam, encoding="utf-8"))
    except Exception:                                          # noqa: BLE001
        return None
    if not isinstance(falas, list):
        return None
    mp, cru = constroi_vocabulario_fora(pasta)
    achados, vistos = [], set()
    for it in falas:
        txt = it.get("texto") if isinstance(it, dict) else None
        if not txt:
            continue
        # ⚠️ A FALA QUE FALA DA GRADE cita a forma crua DE PROPOSITO — "na grade
        #    as palavras estao sem o til: procure PORTAO". Acusar isso seria
        #    mandar consertar o que esta certo. (Mede-se: dos onze achados da
        #    estreia, tres eram exatamente este caso.)
        baixo = txt.lower()
        if (u"na grade" in baixo or u"sem acento" in baixo or u"sem o til" in baixo
                or u"sem acentos" in baixo or u"nao ha acento" in baixo
                or u"não há acento" in baixo):
            continue
        for w in _PAL.findall(txt):
            if _ACENTO.search(w):
                continue
            wu = w.upper()
            if wu in vistos:
                continue
            cand = mp.get(_tira(wu))
            if not cand:
                continue
            acent = cand.most_common(1)[0][0]
            if acent == wu:
                continue
            n_ac = sum(cand.values())
            n_cru = cru.get(wu, 0)
            # ⚠️ O LIMIAR SAIU DE MEDIDA, nao de cabeca (20/set/2026, contado no
            #    projeto inteiro menos a pasta em exame). A palavra so e acusada
            #    quando a forma crua e RARA ao lado da acentuada — ate 5%:
            #      NAO  1442 acentuadas x    8 cruas (0,6%)   -> acusa, e certo
            #      ATE   355 x 2 (0,6%) · TRES 1497 x 3 (0,2%) · SAO 1023 x 1
            #      AGUA  170 x 1 (0,6%) · VOCE 2024 x 0 · CORACAO 30 x 0
            #    e nao e acusada quando as DUAS formas sao palavra de verdade:
            #      ESTA 1069 acentuadas x 340 cruas (32%) — "esta frase" existe
            #      PORQUE   3 x 304 — "porque" e a forma comum
            #    A folga entre os dois grupos e de 50x (0,6% contra 32%): nao e
            #    fio de navalha. Lista de excecao a mao envelhece; conta, nao.
            if n_ac >= 2 and n_cru <= 0.05 * n_ac:
                vistos.add(wu)
                achados.append((it.get("id", "?"), wu, acent, txt[:70]))
    return achados


def _acha_conteudo(alvo):
    u"""aceita pasta, conteudo.json ou index.html e devolve o conteudo.json."""
    if os.path.isdir(alvo):
        return os.path.join(alvo, "conteudo.json")
    if alvo.endswith("conteudo.json"):
        return alvo
    # index.html -> conteudo.json ao lado
    c = os.path.join(os.path.dirname(os.path.abspath(alvo)), "conteudo.json")
    return c


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/acento.py <pasta|conteudo.json|index.html>")
        return 2
    alvo = sys.argv[1].rstrip(u"/")
    cj = _acha_conteudo(alvo)
    if not os.path.exists(cj):
        # sem conteudo.json: pode ser CADERNO DE FOLHA VIVA — ali o que se mede
        # e a PROSA (ver `checa_prosa`), nao a grade.
        pasta = alvo if os.path.isdir(alvo) else os.path.dirname(os.path.abspath(alvo))
        pr = checa_prosa(pasta)
        if pr is None:
            print(u"acento: sem conteudo.json e sem falas.json em %s — NAO MEDI." % alvo)
            return 2
        if not pr:
            print(u"   acento ok: a prosa que a voz le esta acentuada")
            return 0
        # ⚠️ ISTO E AVISO, NAO REPROVACAO — e a razao esta medida. Rodado nos 30
        #    cadernos de folha viva, este olho achou onze palavras: TRES eram
        #    defeito de verdade (LAMPADA, XICARA, AMANHA — a voz le errado) e as
        #    outras oito eram inocentes de quatro familias que ele ainda nao sabe
        #    separar: o nome da LETRA ("jota"), a SILABA solta ("lan"), o
        #    HOMOGRAFO legitimo ("os pais" != "o pais"), a terminacao citada
        #    ("as duas terminam com ate") e a frase em OUTRA LINGUA ("sailed to
        #    America"). Nenhuma contagem separa os dois grupos — a razao entre
        #    forma crua e acentuada e praticamente a mesma nos dois (0,00 a 0,05).
        #    Portao que acusa inocente e portao que a gente aprende a pular
        #    (regra da casa), entao aqui ele FALA e nao barra. O que ele resolve
        #    e o caso que me custou caro no `_corpo5`: CINQUENTA frases inteiras
        #    sem acento, que nenhum outro portao viu e so o olho pegou.
        print(u"   AVISO (nao reprova): %d palavra(s) de prosa podem estar sem acento —" % len(pr))
        print(u"   OLHAR uma a uma. Ha inocentes conhecidos: nome de letra, silaba")
        print(u"   solta, homografo ('os pais'), terminacao citada e outra lingua.")
        for fid, crua, acent, trecho in pr[:20]:
            print(u'      %s: "%s" -> "%s"?   (%s)' % (fid, crua, acent, trecho))
        if len(pr) > 20:
            print(u"      ... e mais %d" % (len(pr) - 20))
        return 0
    try:
        conteudo = json.load(io.open(cj, encoding="utf-8"))
    except Exception as e:                                     # noqa: BLE001
        print(u"acento: nao consegui ler %s (%s)" % (cj, str(e)[:80]))
        return 2
    achados = checa_conteudo(conteudo)
    if not achados:
        print(u"   acento ok: toda palavra de grade que a voz le esta acentuada")
        return 0
    print(u"   %d PALAVRA(S) DE GRADE SEM ACENTO — a VOZ vai ler errado:" % len(achados))
    for fid, mec, crua, acent in achados:
        print(u'      fase %s (%s): "%s" -> escreva "%s" '
              u"(a grade dobra o acento sozinha)" % (fid, mec, crua, acent))
    return 1


if __name__ == "__main__":
    sys.exit(main())
