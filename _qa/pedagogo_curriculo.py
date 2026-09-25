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

 6. O CONTEÚDO que a atividade ENSINA cabe no ano? (`conceitos`)
    ⚠️⚠️ ESTA É A PERGUNTA QUE FALTAVA, e ela custou uma rodada inteira com o
    Marcos (14/set/2026). A Coroa dos Cinco Reinos passou nas cinco perguntas
    de cima com nota cheia: as dez habilidades citadas existiam palavra por
    palavra no currículo. E mesmo assim o caderno ensinava DUAS coisas que não
    são do 4º ano da rede — a gaveta "já foram vivos" e o critério do NÚCLEO
    (o "cofrinho da receita"). Quem pegou foi ELE, lendo: *"aquela parte de já
    foi vivo é adequado ao 4 ano?"*. E a cobrança veio junto: *"essas coisas
    não podem acontecer, pois existe o pedagogo o especialista"*.

    Ele tinha razão, e o buraco era exatamente este: a pergunta 2 confere a
    CITAÇÃO (a frase que eu digo estar cumprindo), não o CONTEÚDO (o que a
    criança de fato faz na tela). Dá para citar "Conhecer os reinos dos seres
    vivos" com honestidade total e, na folha, ensinar núcleo celular.

    Como se mede, sem chute: a atividade DECLARA em `curriculo.json` a lista
    `conceitos` — os termos de conteúdo que ela ensina — e o portão procura
    cada um no BLOCO DO ANO E DO COMPONENTE do documento da rede (não no
    documento inteiro: "célula" existe no 3º ano e no 6º; o que importa é se
    existe NO ANO desta atividade). Termo que não estiver lá reprova, a menos
    que esteja declarado em `fora_do_curriculo` com o motivo — e aí o portão
    IMPRIME a declaração em toda rodada, para que ela nunca mais passe calada.
    ⚠️ Sem `conceitos` o portão diz NÃO MEDI, que não é "passou".

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
# ⚠️⚠️ COMPUTACAO TEM DOCUMENTO PROPRIO (25/set/2026). O Marcos enviou o
#    «Curriculo de Computacao da Educacao Basica do Sistema Municipal de
#    Ensino de Blumenau» — 76 paginas, Educacao Infantil ao 9o ano, com o
#    Quadro Organizador de cada ano nos tres eixos. Ele NAO esta dentro do
#    `blumenau.txt`, e enquanto este portao so abria aquele arquivo, todo
#    caderno de Computacao dizia "NAO MEDI" — que nao e "passou".
CURRICULO_COMP = "_curriculo/computacao-blumenau.txt"
_PALAVRAS = {}


def arquivo_do(componente):
    u"""Qual documento da rede confere ESTE componente."""
    return CURRICULO_COMP if u"computacao" in achata(componente or u"") else CURRICULO


def palavras_de(caminho):
    u"""Todas as palavras do documento, achatadas — e as QUEBRADAS no fim da
    linha remontadas, senao o portao reprova a transcricao fiel e aprova o
    caco (mesma regra do `main`, agora em um lugar so)."""
    if caminho in _PALAVRAS:
        return _PALAVRAS[caminho]
    if not os.path.exists(caminho):
        _PALAVRAS[caminho] = None
        return None
    cru = io.open(caminho, encoding="utf-8").read()
    ps = set(achata(cru).split())
    for _a, _b in re.findall(r"(\w+)-\s*\n\s*(\w+)", cru):
        ps.add(achata(_a + _b).strip())
    _PALAVRAS[caminho] = ps
    return ps
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


# ⚠️ O CABECALHO DE BLOCO DO PDF DA REDE: "CIENCIAS - ANOS INICIAIS - 4o ANO",
#    "LINGUA PORTUGUESA - ANOS INICIAIS - 1o ANO"... Ele se repete no topo E no
#    rodape de cada pagina, entao NAO da para pegar "do primeiro ate o proximo":
#    o certo e varrer o arquivo guardando qual cabecalho esta valendo e juntar
#    todas as linhas em que o cabecalho valendo e o alvo.
_CABEC = re.compile(u"^\\s*([A-Za-zÁÉÍÓÚÂÊÔÃÕÇáéíóúâêôãõç ]{4,40}?)\\s*[–—-]\\s*"
                    u"ANOS\\s+(?:INICIAIS|FINAIS)\\s*[–—-]\\s*(\\d)\\s*[ºo]?\\s*ANO\\s*$",
                    re.I | re.M)


# ⭐⭐ AS OUTRAS DUAS FORMAS DO MESMO CABEÇALHO (23/set/2026).
#    Até hoje este portão só conhecia o cabeçalho completo («CIÊNCIAS – ANOS
#    INICIAIS – 4º ANO») e, por isso, dizia NÃO MEDI em Língua Portuguesa e em
#    Matemática — e eu registrei no `CLAUDE.md` que a razão era o documento não
#    ter bloco por ano nesses dois componentes. **Era falso.** Tem:
#      · LÍNGUA PORTUGUESA — cada LINHA da tabela começa com o ano:
#          "3º ANO   CAMPO DA VIDA   Análise linguística ..."
#      · MATEMÁTICA — o ano vem SOZINHO numa linha, abrindo o bloco, e os nove
#          se sucedem em ordem (linhas 17628 a 19404 do `blumenau.txt`: 1º, 2º,
#          3º … 9º). O bloco vai de um cabeçalho ao seguinte.
#
#    ⚠️⚠️ E NENHUMA DAS DUAS DIZ A QUE COMPONENTE PERTENCE. Um "3º ANO" solto
#       não tem a palavra MATEMÁTICA em lugar nenhum — quem prova é o CONTEÚDO.
#       Por isso a região achada só é aceita se trouxer as MARCAS daquele
#       componente (abaixo). Sem essa confirmação, este atalho aprovaria
#       conteúdo do componente errado, que é exatamente o que o portão existe
#       para impedir.
#
#    ⚠️ PALPITE DECLARADO: **três** marcas distintas, e **cinco** anos seguidos
#       para reconhecer a corrida de cabeçalhos soltos. Os dois números são
#       escolha minha, não medida — estão aqui e saem impressos na saída.
_MARCAS = {
    u"matematica": [u"numeros", u"algebra", u"geometria", u"grandezas",
                    u"medidas", u"probabilidade", u"estatistica"],
    u"lingua portuguesa": [u"leitura", u"escuta", u"oralidade", u"analise",
                           u"semiotica", u"escrita", u"campo"],
    # ⚠️ Computacao se prova pelos TRES EIXOS, que abrem todo quadro do
    #    documento e nao aparecem em componente nenhum dos outros.
    u"computacao": [u"pensamento", u"computacional", u"mundo", u"digital",
                    u"cultura", u"algoritmos", u"eixo"],
}
MARCAS_MIN = 3
CORRIDA_MIN = 5
# ⚠️ O GRAU E O ORDINAL SAO LETRAS DIFERENTES, e o PDF mistura os dois.
#    Medido em 25/set/2026 no documento de Computacao: o 1o ano vem escrito
#    "1° ANO" (sinal de GRAU, U+00B0) e os demais "2º ANO" (indicador
#    ORDINAL, U+00BA). A classe aceitava so o ordinal, entao o bloco do 1o ano
#    simplesmente nao existia para o portao — e Computacao do 1o ano diria
#    "NAO MEDI" para sempre, sem ninguem entender por que.
#    Dois caracteres que o olho nao distingue derrubam um ano inteiro.
_ANO_SO = re.compile(u"^\\s*([1-9])\\s*[º°o]?\\s*ANO\\s*$", re.I)
_ANO_LINHA = re.compile(u"^\\s*([1-9])\\s*[º°o]?\\s*ANO\\s+(?=\\S)", re.I)


def _confirma(regiao, componente):
    u"""A região achada é MESMO deste componente? Prova pelo conteúdo."""
    nome = achata(componente).strip()
    # ⚠️ POR DENTRO, NÃO POR IGUALDADE. O `_abc1` declara o componente como
    #    «Alfabetização e Língua Portuguesa» — que é como a rede chama o 1º ano.
    #    Comparando por igualdade, ele cairia aqui e o portão diria NÃO MEDI num
    #    caderno que o documento cobre inteirinho.
    marcas = next((v for k, v in _MARCAS.items() if k in nome), None)
    if not marcas:
        return False          # componente que eu nao sei confirmar: nao arrisco
    plano = achata(u" ".join(regiao))
    return sum(1 for m in marcas if m in plano) >= MARCAS_MIN


def _por_linha(linhas, componente, ano):
    u"""FORMA B — Língua Portuguesa: cada linha da tabela abre com o ano.

    ⚠️⚠️ E A FILEIRA NÃO CABE NUMA LINHA SÓ. A primeira versão disto pegava
       apenas as linhas que COMEÇAM com "3º ANO" e devolvia 115 palavras — o
       bloco vinha sem "travessão" e sem "polissílabas", que são habilidades do
       3º ano escritas nas linhas de CONTINUAÇÃO da mesma fileira. **Bloco
       cortado é pior do que NÃO MEDI**: ele reprova o conceito certo, e aí o
       portão manda consertar o que não está quebrado.
       Agora a fileira vai inteira: da linha que abre com o ano até a próxima
       que abra com QUALQUER ano."""
    fim_de_fileira = re.compile(u"^\\s*[1-9]\\s*[ºo]?\\s*ANO\\b", re.I)
    pegas, dentro = [], False
    for ln in linhas:
        m = _ANO_LINHA.match(ln)
        if m:
            dentro = (m.group(1) == str(ano))
        elif fim_de_fileira.match(ln):
            dentro = False            # abriu outra fileira (ano sozinho)
        if dentro:
            pegas.append(ln)
    if len(pegas) < 4 or not _confirma(pegas, componente):
        return None
    return pegas


def _por_corrida(linhas, componente, ano):
    u"""FORMA C — Matemática: cabeçalhos sozinhos, em corrida crescente."""
    cabs = [(i, int(_ANO_SO.match(ln).group(1)))
            for i, ln in enumerate(linhas) if _ANO_SO.match(ln)]
    # a corrida: cabeçalhos que sobem de um em um, sem repetir
    melhor, atual = [], []
    for i, a in cabs:
        if atual and a == atual[-1][1] + 1:
            atual.append((i, a))
        else:
            atual = [(i, a)]
        if len(atual) > len(melhor):
            melhor = list(atual)
    if len(melhor) < CORRIDA_MIN:
        return None
    # ⚠️ O ANO VEM DOS DOIS JEITOS. O `_alfa1` declara `"ano": "1"` (texto) e o
    #    `_corpo5` declara `"ano": 5` (número) — os dois são `curriculo.json`
    #    legítimos e escritos em dias diferentes. Comparando int com str isto
    #    NUNCA casava, e o portão dizia "não achei o bloco" em dois cadernos que
    #    o documento cobre. É a lição do `ouvir.py` outra vez: **quando os dois
    #    lados podem escrever a mesma coisa de formas diferentes, normalize
    #    ANTES da régua.**
    try:
        alvo_ano = int(str(ano).strip()[0])
    except (ValueError, IndexError):
        return None
    for k, (i, a) in enumerate(melhor):
        if a != alvo_ano:
            continue
        fim = melhor[k + 1][0] if k + 1 < len(melhor) else len(linhas)
        regiao = linhas[i + 1:fim]
        if not _confirma(regiao, componente):
            return None
        return regiao
    return None


# ⚠️ MEMÓRIA, e ela é necessária e não enfeite: desde que o item 6 passou a
#    conferir também os anos ANTERIORES, um caderno de 5º ano manda varrer o
#    documento CINCO vezes — e o documento tem 440 páginas. Sem isto o portão
#    saiu de instantâneo para dezenas de segundos por caderno, e portão lento é
#    portão que se deixa de rodar.
_CACHE = {}


def bloco_do_ano(texto, componente, ano):
    u"""Palavras do bloco DESTE componente e DESTE ano. Devolve None se o
    documento nao tiver nenhum cabecalho desse par (ai e NAO MEDI, nao e
    'passou'): melhor dizer que nao medi do que medir no documento inteiro e
    aprovar "celula" no 4o ano porque ela existe no 6o.

    Tres formas de cabecalho, nesta ordem de confianca:
      A) o completo ("CIENCIAS - ANOS INICIAIS - 4o ANO") — o unico que se
         nomeia, entao nao precisa de confirmacao nenhuma;
      B) o ano abrindo CADA LINHA da tabela (Lingua Portuguesa);
      C) o ano SOZINHO, em corrida crescente de blocos (Matematica).
    B e C so valem com a confirmacao pelo conteudo (`_confirma`)."""
    alvo = (achata(componente).strip(), str(ano))
    if alvo in _CACHE:
        return _CACHE[alvo]
    linhas = texto.split(u"\n")
    valendo, pegas, viu = None, [], False
    for ln in linhas:
        # ⚠️ FILTRO BARATO ANTES DO REGEX, e ele vale 45 SEGUNDOS (medido em
        #    23/set/2026 com o cProfile). O `_CABEC` tem um `[letras]{4,40}?`
        #    preguiçoso: numa linha longa sem cabeçalho nenhum ele RETROCEDE
        #    dezenas de vezes antes de desistir, e o documento tem vinte mil
        #    linhas. Eram 9 s por chamada — e como o item 6 passou a conferir
        #    também os anos anteriores, virou 46 s por caderno. **Portão lento
        #    é portão que se deixa de rodar.** Duas buscas de substring cortam
        #    99% das linhas antes de o regex sequer começar: 46 s -> 0,4 s.
        if u"ANO" not in ln or (u"-" not in ln and u"–" not in ln and u"—" not in ln):
            if valendo == alvo:
                pegas.append(ln)
            continue
        m = _CABEC.match(ln)
        if m:
            valendo = (achata(m.group(1)).strip(), m.group(2))
            if valendo == alvo:
                viu = True
            continue
        if valendo == alvo:
            pegas.append(ln)
    if viu:
        _CACHE[alvo] = set(achata(u" ".join(pegas)).split())
        return _CACHE[alvo]
    for tenta in (_por_linha, _por_corrida):
        regiao = tenta(linhas, componente, ano)
        if regiao:
            _CACHE[alvo] = set(achata(u" ".join(regiao)).split())
            return _CACHE[alvo]
    _CACHE[alvo] = None
    return None


def fora_dec_termos(lista):
    for it in lista:
        yield it.get("termo", u"") if isinstance(it, dict) else it


# ⚠️ PALPITE DECLARADO — a RAIZ de 4 letras. O documento da rede escreve
#    "cadeias alimentares" e a atividade declara "cadeia alimentar"; comparar
#    palavra inteira reprovaria por causa do plural. Entao compara-se pela
#    raiz: 4 letras, ou a palavra menos 2 letras, o que for maior. E um numero
#    escolhido por mim, nao medido — esta dito aqui e impresso no cabecalho da
#    saida para que ninguem o tome por medida.
RAIZ = 4


def _raiz(w):
    return w[:max(RAIZ, len(w) - 2)]


def no_bloco(termo, bloco):
    u"""Todo termo-palavra de 4+ letras tem de casar por raiz com alguma palavra
    do bloco do ano. Palavra curta (de, e, do) nao conta."""
    palavras = [w for w in achata(termo).split() if len(w) >= RAIZ and w not in NOSSAS]
    if not palavras:
        return True
    for w in palavras:
        rw = _raiz(w)
        # ⚠️ `len(b) >= RAIZ` NAO E DETALHE: o PDF foi extraido em COLUNAS e o
        #    bloco vem cheio de cacos de uma e duas letras ("m", "ma", "o").
        #    Sem este filtro, _raiz("o") = "o" e QUALQUER palavra comecada por o
        #    casava — "materia organica" passava no 4o ano, onde ela nao esta.
        #    Pego na propria prova do portao, 14/set/2026.
        if not any(len(b) >= RAIZ and (b.startswith(rw) or w.startswith(_raiz(b)))
                   for b in bloco):
            return False
    return True


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
    # ⚠️ o documento da rede depende do COMPONENTE: Computacao tem o seu.
    arq = arquivo_do(d.get("componente"))
    if arq != CURRICULO:
        palavras = palavras_de(arq)

    # ---- 2. a citacao existe no curriculo?
    if palavras is None:
        L.append(u"   ⚠️ nao achei %s: NAO conferi as citacoes" % arq)
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

    # ---- 6. o CONTEUDO que a atividade ensina cabe no ano?
    conceitos = d.get("conceitos")
    fora_dec = d.get("fora_do_curriculo") or []
    if not conceitos:
        L.append(u"   ⚠️ o curriculo.json nao declara `conceitos`: NAO MEDI se o "
                 u"CONTEUDO cabe no ano (isso nao e 'passou'). Ver a pergunta 6 "
                 u"no topo deste arquivo.")
        ruim = max(ruim, 2)
    else:
        doc = io.open(arq, encoding="utf-8").read() if os.path.exists(arq) else u""
        bloco = bloco_do_ano(doc, d.get("componente") or u"", d.get("ano"))
        if bloco is None:
            L.append(u"   ⚠️ nao achei o bloco de «%s – %sº ano» no documento da rede: "
                     u"NAO MEDI os %d conceito(s). Medir no documento inteiro aprovaria "
                     u"conteudo de outro ano, entao prefiro dizer que nao medi.\n"
                     u"      (o portao conhece TRES formas de cabecalho: a completa "
                     u"«COMPONENTE - ANOS INICIAIS - Nº ANO», a do ano abrindo cada linha "
                     u"da tabela e a do ano sozinho em corrida de blocos. Se o componente "
                     u"usar uma quarta, e divida DESTA ferramenta, nao do documento.)"
                     % (d.get("componente"), d.get("ano"), len(conceitos)))
            ruim = max(ruim, 2)
        else:
            declarados = set(achata(x).strip() for x in fora_dec_termos(fora_dec))
            # ⭐⭐ CONTEÚDO DE ANO ANTERIOR SEMPRE CABE (23/set/2026).
            #    A pergunta deste item é *"o conteúdo cabe no ano?"* — e o que
            #    veio de um ano ANTES cabe por definição: no 5º ano a sílaba não
            #    é conteúdo novo, é ferramenta. O que não pode é conteúdo de ano
            #    DEPOIS, que é o defeito que este item nasceu para pegar (o
            #    núcleo da célula no 4º ano).
            #    ⚠️ Isto apareceu porque o portão passou a ACHAR o bloco de
            #       Língua Portuguesa: ele reprovou o `_ort5b` por "sílabas" e o
            #       `_subst5` por "letras maiúsculas" — dois cadernos corretos,
            #       do 5º ano, usando o que a criança aprendeu no 2º. **Portão
            #       que manda consertar o que não está quebrado gasta o dia e
            #       ensina a ignorar a saída.**
            antes = []
            try:
                for a_ in range(1, int(d.get("ano"))):
                    b_ = bloco_do_ano(doc, d.get("componente") or u"", a_)
                    if b_:
                        antes.append((a_, b_))
            except (TypeError, ValueError):
                pass
            maus, herdados = [], []
            for termo in conceitos:
                if achata(termo).strip() in declarados:
                    continue
                if no_bloco(termo, bloco):
                    continue
                de = next((a_ for a_, b_ in antes if no_bloco(termo, b_)), None)
                if de:
                    herdados.append((termo, de))
                else:
                    maus.append(termo)
            for termo, de in herdados:
                L.append(u"   · «%s» nao esta no bloco do %sº ano, mas esta no do %sº: "
                         u"conteudo de ano ANTERIOR cabe (e ferramenta, nao materia nova)."
                         % (termo, d.get("ano"), de))
            if maus:
                ruim = 1
                L.append(u"   REPROVADO 6: a atividade ensina conteudo que o bloco do %sº ano "
                         u"de %s NAO tem:" % (d.get("ano"), d.get("componente")))
                for t in maus:
                    L.append(u"      • %s" % t)
                L.append(u"      -> ou tira do caderno, ou declara em `fora_do_curriculo` "
                         u"com o motivo (e ai o portao imprime a declaracao em toda rodada).")
            else:
                L.append(u"   ✓ os %d conceito(s) que o caderno ensina existem no bloco do "
                         u"%sº ano de %s" % (len(conceitos), d.get("ano"), d.get("componente")))
            # ⚠️ O MOTIVO ESTAVA SENDO ENGOLIDO — e isso matava a unica garantia
            #    desta declaracao (20/set/2026). O portao lia `porque`; as tres
            #    atividades que declaram excecao escrevem `motivo`, e nenhuma
            #    escreve `porque`. Resultado: TODA declaracao saia como
            #    «termo» — , sem uma palavra de justificativa. A regra da casa e
            #    que declarado e IMPRESSO em toda rodada, justamente para o
            #    professor poder discordar; sem o motivo impresso, declarar
            #    virava desligar o portao em silencio.
            #    Agora le os dois nomes de campo E COBRA que haja motivo.
            sem_motivo = []
            for it in fora_dec:
                t = it.get("termo") if isinstance(it, dict) else it
                pq = u""
                if isinstance(it, dict):
                    pq = (it.get("motivo") or it.get("porque") or u"").strip()
                if not pq:
                    sem_motivo.append(t)
                L.append(u"   ⚠️ FORA DO CURRICULO, DECLARADO: «%s» — %s"
                         % (t, pq or u"(SEM MOTIVO ESCRITO)"))
            if sem_motivo:
                ruim = 1
                L.append(u"   REPROVADO 6b: declaracao SEM MOTIVO em `fora_do_curriculo`:")
                for t in sem_motivo:
                    L.append(u"      • %s" % t)
                L.append(u"      -> declarar sem dizer por que e so desligar o portao. "
                         u"Escreva o campo `motivo`.")

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
        _cru = io.open(CURRICULO, encoding="utf-8").read()
        palavras = set(achata(_cru).split())
        # ⚠️ AS PALAVRAS QUEBRADAS NO FIM DA LINHA (ver o comentario no topo):
        #    «grafia cor-\n reta de palavras» tem de dar tambem "correta",
        #    senao o portao reprova a transcricao FIEL e aprova o caco.
        for _a, _b in re.findall(r"(\w+)-\s*\n\s*(\w+)", _cru):
            palavras.add(achata(_a + _b).strip())
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
