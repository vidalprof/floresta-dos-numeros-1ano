#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""LIGA AS PEÇAS AO MOTOR — sem reescrever nenhuma das duas.

O problema: a peça é uma **mini-atividade** (monta a própria tela, chama
`limpa()`, `setProg()` e termina em `mostraBanner`). O motor quer uma **fase**
(recebe o `cen` pronto e chama `fim()`). Reescrever 78 peças para virarem fases
seria jogar fora o teste de cada uma — e reintroduzir os 31 defeitos que elas já
custaram.

A ponte: cada peça entra num **fechamento** com ajudantes trocados por versões
que servem à fase. A peça continua achando que está sozinha; o motor continua
mandando. Ninguém reescreve nada.

  limpa()          → limpa só o `cen` da fase (não a tela do motor)
  setProg(t,p)     → não faz nada (quem manda na barra é o motor)
  app              → o `cen` da fase
  mostraBanner(m,c)→ comemora e chama `fim()` (o motor leva à fase seguinte)
  ajuda / regFase  → os do motor (andaime e medição de verdade)

⚠️ O CSS da peça também vem junto, com o nome dela na frente de cada regra, para
   duas peças não brigarem por causa da mesma classe (`.opt`, `.pc`, `.zona`).

Uso:  python3 _padrao/ESQUELETO/integrar.py            → lista o que dá para ligar
      python3 _padrao/ESQUELETO/integrar.py --escrever → escreve pecas.js/pecas.css
"""
import io
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
PECAS = os.path.join(RAIZ, "_padrao", "pecas")

MARCA_CSS = "CSS DESTA"          # onde começa o CSS próprio da peça, no molde
MARCA_JS = "A PE"                # "A PEÇA COMEÇA AQUI"


_KF_ABRE = re.compile(r"@(?:-webkit-|-moz-|-o-)?keyframes\s+[\w-]+\s*\{", re.I)


def tira_keyframes(css):
    u"""arranca os `@keyframes` INTEIROS antes de quebrar a folha em regras.

    ⚠️⚠️ AQUI MORAVA O DEFEITO (ago/2026, achado ao redesenhar a `ligar-pontos`,
    e o rastro levou até este ponto): o `regras()` conhecia `@media` e mais nada.
    O cabeçalho `@keyframes pulso{` não casava com alternativa nenhuma e era
    PULADO; os `0%` e `100%` de dentro sobravam soltos e viravam "regras" com
    seletor `0%`. Ou seja: a animação era desmontada antes mesmo de chegar ao
    prefixador — **60 das 77 peças perdiam TODAS as animações ao entrar numa
    atividade montada**, e na peça avulsa tudo continuava lindo, que é onde a
    gente olhava.

    Nada quebrava: sem erro de JS, sem portão reprovando, print igual. A tela só
    ficava morta — o avesso do que o Marcos pede o tempo todo ("mais visual").

    O bloco sai daqui inteiro, do `@` até a chave que o fecha, e segue como uma
    peça só até o fim da esteira."""
    # ⚠️⚠️ SEGUNDA LICAO PAGA NO MESMO DIA, e e a MESMA de tres paragrafos
    #    acima: COMENTARIO NAO E CODIGO. Uma peca explicava, num comentario, o
    #    proprio defeito das animacoes — e a frase citava `@-webkit-keyframes
    #    kf-completar-treme{`. Este extrator leu a citacao como bloco de verdade,
    #    arrancou dali ate a primeira chave que fechasse, e ENTORTOU a folha
    #    inteira a partir daquele ponto.
    #    O estrago medido no navegador: das milhares de regras das 79 pecas, o
    #    Chrome so conseguiu ler **405** — o resto foi descartado em silencio.
    #    Era essa a causa dos alto-falantes sem desenho, dos quadrados brancos
    #    atras das figuras e do texto sem cor: nao eram tres defeitos, era UM.
    #    Escrever a lição no comentário criou o defeito que a lição descrevia.
    vaos = []
    j = 0
    while True:
        a_ = css.find("/*", j)
        if a_ < 0:
            break
        b_ = css.find("*/", a_ + 2)
        if b_ < 0:
            vaos.append((a_, len(css)))
            break
        vaos.append((a_, b_ + 2))
        j = b_ + 2

    def em_comentario(pos):
        return any(x <= pos < y for x, y in vaos)

    pedacos, blocos, i = [], [], 0
    for m in _KF_ABRE.finditer(css):
        if m.start() < i or em_comentario(m.start()):
            continue
        prof, k = 0, m.end() - 1
        while k < len(css):
            if css[k] == "{":
                prof += 1
            elif css[k] == "}":
                prof -= 1
                if prof == 0:
                    break
            k += 1
        pedacos.append(css[i:m.start()])
        blocos.append(css[m.start():k + 1])
        i = k + 1
    pedacos.append(css[i:])
    return "".join(pedacos), blocos


def regras(css):
    u"""quebra a folha em regras (seletor, corpo) — inclusive dentro de @media."""
    css, keyframes = tira_keyframes(css)
    # o bloco de animação entra como corpo SEM seletor: quem reconstrói a folha
    # (`css_da_peca`) escreve `sel + corpo` e ele sai inteiro, do jeito que veio.
    # Vem com `media=""` porque animação não mora dentro de `@media` aqui.
    fora, media = [("", "", b) for b in keyframes], ""
    for m in re.finditer(r"(@media[^{]*\{)|(\})|([^{}]+)(\{[^{}]*\})", css, re.S):
        ab, fe, sel, corpo = m.groups()
        if ab:
            media = re.sub(r"\s+", " ", ab).strip()
        elif fe:
            media = ""
        elif sel is not None:
            s = re.sub(r"/\*.*?\*/", " ", sel, flags=re.S).strip()
            if s and not s.startswith("@"):
                fora.append((media, re.sub(r"\s+", " ", s),
                             re.sub(r"\s+", " ", corpo or "").strip()))
    return fora


_MOLDE = [None]


def css_do_molde():
    if _MOLDE[0] is None:
        cam = os.path.join(PECAS, "MOLDE.html")
        h = io.open(cam, encoding="utf-8").read() if os.path.exists(cam) else ""
        st = re.findall(r"<style>(.*?)</style>", h, re.S)
        _MOLDE[0] = set((a, b, c) for a, b, c in regras(st[0] if st else ""))
    return _MOLDE[0]


def css_da_peca(html):
    u"""SÓ o que a peça acrescentou — o CSS do molde já está no motor.

    ⚠️ LIÇÃO PAGA: isto procurava o comentário `/* ==== CSS DESTA PEÇA ==== */`.
    Só que **28 das 74 peças não têm essa marca** — o CSS próprio delas mora
    misturado ao do molde, no mesmo bloco. Resultado: 28 mecânicas entravam na
    atividade **sem o estilo delas**. A memória perdia a virada 3D e as cartas
    viravam retângulos (e o portão das dinâmicas ainda disse, em voz alta, "não
    achei o rotateY" — eu é que li como defeito da peça).

    Agora não depende de marca nenhuma: **tira o que é igual ao MOLDE**. O que
    sobra é da peça, tenha ela comentário ou não. Regra que a peça redefine (o
    `.opt` dela, diferente do do molde) continua vindo — e, prefixada com
    `.mec-<nome>`, ganha do molde por especificidade, que é o que se quer."""
    st = re.findall(r"<style>(.*?)</style>", html, re.S)
    if not st:
        return ""
    # ⚠️⚠️ O COMENTARIO SAI AQUI, ANTES DE QUALQUER LEITURA (ago/2026).
    #    Esta e a TERCEIRA vez que comentario de peca vira codigo nesta esteira
    #    — e da terceira vez ele derrubou a folha inteira: o Chrome leu 405
    #    regras das milhares das 79 pecas, e o resto sumiu calado (alto-falante
    #    sem desenho, quadrado branco atras da figura, texto sem cor).
    #    A causa e sempre a mesma: as pecas EXPLICAM defeitos de CSS nos
    #    comentarios, entao os comentarios contem `{`, `}`, `25%` e ate
    #    `@keyframes ...{`. Qualquer varredor que conte chaves se perde neles.
    #    O `prefixa_css` ja sabia disso e guardava os comentarios; so que ele e
    #    o ULTIMO da fila — `regras()` e `tira_keyframes()` vem antes.
    #    A regra que fica: comentario de peca NAO viaja para a atividade. Ele
    #    serve a quem edita a peca, nao ao PC da escola — e ainda pesa no
    #    arquivo que a crianca baixa.
    folha = _COMENT.sub(" ", st[0])
    st = [folha]
    molde = css_do_molde()
    saida, media_aberta = [], ""
    for media, sel, corpo in regras(st[0]):
        if (media, sel, corpo) in molde:
            continue
        if media != media_aberta:
            if media_aberta:
                saida.append("}")
            if media:
                saida.append("\n" + media)
            media_aberta = media
        saida.append("\n" + sel + corpo)
    if media_aberta:
        saida.append("}")
    return "".join(saida)


def js_da_peca(html):
    u"""o segundo <script>: o corpo da mecânica."""
    sc = re.findall(r"<script>(.*?)</script>", html, re.S)
    return sc[1] if len(sc) > 1 else ""


def entrada(js):
    u"""a função que a peça chama sozinha no fim do arquivo — é a porta dela."""
    m = None
    for m in re.finditer(r"^\s*([\w$]+)\s*\(\s*\)\s*;\s*$", js, re.M):
        pass
    return m.group(1) if m else None


def _ate_o_fim(js, i):
    u"""do `[` ou `{` em `i` ate o fechamento dele."""
    k, prof = i, 0
    while k < len(js):
        if js[k] in "[{":
            prof += 1
        elif js[k] in "]}":
            prof -= 1
            if prof == 0:
                return k + 1
        k += 1
    return len(js)


# nomes que sao ARTE ou CONFIGURACAO, nunca conteudo da fase
NAO_E_CONTEUDO = set("""ARTE VERSO CORES COR PALETA SVG IMG IMGS AC CFG CONFIG
    ESTILO FIG FIGS SONS TEMPO""".split())


def gaveta(js):
    u"""A GAVETA DE CONTEÚDO da peça — o que faz a atividade virar dado.

    O integrador troca o conteúdo de exemplo da peça pelo desta fase (`f.dados`)
    **sem tocar na peça** — que é o ponto: a peça já foi testada, e reescrevê-la
    é reintroduzir os defeitos que ela custou.

    ⚠️ LIÇÃO PAGA, e das perigosas: a regra era *"a primeira `var` do topo"*.
    No jogo da memória a primeira é **`ARTE`** — o desenho do verso da carta —
    e o conteúdo é `PARES`, logo abaixo. Injetar `f.dados` teria trocado o
    DESENHO DO VERSO pelos pares da atividade: nenhum erro de JS, nenhuma tela
    branca, e um jogo de memória com o verso quebrado e as cartas de exemplo.
    O tipo de defeito que só aparece com a criança na frente.

    A ordem de confiança agora é:
      1. a **marca escrita na peça** (*"troque APENAS este bloco"*) — 32 das 74
         a têm, e onde ela existe é a palavra final do autor;
      2. o primeiro **vetor** do topo — conteúdo é quase sempre uma LISTA de
         rodadas; arte e configuração costumam ser objeto;
      3. o primeiro objeto, se não houver vetor nenhum.
    Em qualquer caso, nomes que são arte ou configuração ficam de fora.

    ⚠️ E ALGUMAS MECANICAS TEM MAIS DE UMA GAVETA. No "ache o que mudou" a cena
    esta em `CENA_A` e os erros em `MUDA`: injetar so uma da METADE do conteudo —
    a atividade abre, nao da erro, e mostra a cena da fase com os erros de
    exemplo. Por isso a funcao devolve tambem TODAS as vars de conteudo, e o
    conteudo.json pode preencher as outras por `dadosExtra`.

    Devolve `(nome, exemplo, regra, todas)` — a regra vai para o `pecas.json`
    para o escolhido poder ser conferido, em vez de acreditado.

    ⚠️ LICAO PAGA (ago/2026) — AVISO QUE GRITA A TOA. Nem toda gaveta e texto
    que a crianca le: `LETRAS`/`ALFA` sao o alfabeto do teclado, `FEITOS` nasce
    vazia e a peca preenche jogando, `FORCA_FIG`/`MODO` sao opcoes com padrao
    legitimo. Deixar essas no exemplo e o CERTO, e mesmo assim o montador
    reclamava delas — dez avisos numa montagem so, o que ensina a passar o olho
    e perder o aviso que importava (foi assim que o `MODO` do caca-palavras
    ficou em "lista" com as definicoes ja escritas: a pista existia e nao
    aparecia). O montador tinha uma LISTA de nomes conhecidos, que so crescia e
    so depois do defeito. Agora quem sabe e a PECA: escrever `/*TECNICA*/` na
    linha da `var` marca a gaveta como tecnica e ela sai dos avisos."""
    achados = []
    # ⚠️ LICAO PAGA (Solidos, ago/2026 — o Marcos: "a fase 'qual nao e' nao tem
    #    nada a ver com solidos"): o INTRUSO declara a gaveta como
    #    `var RODADAS= /*TECNICA*/[...]` — o comentario TECNICA entre o `=` e o
    #    `[`. A regex parava em `=\s*[` e NAO enxergava o `[` depois do
    #    comentario, entao a gaveta nao era detectada, `f.dados` nao entrava, e a
    #    peca rodava com o EXEMPLO dela (frutas: banana/uva/maca/cenoura) dentro
    #    de uma atividade de SOLIDOS. Agora a regex pula um comentario opcional
    #    entre o `=` e o vetor/objeto. Vale para qualquer peca que marque a
    #    gaveta assim.
    for m in re.finditer(r"^var\s+([A-Za-z_$][\w$]*)\s*=\s*(?:/\*[^*]*\*/\s*)?([\[{])", js, re.M):
        if m.group(1) in NAO_E_CONTEUDO:
            continue
        i = m.end() - 1
        achados.append((m.group(1), i, _ate_o_fim(js, i), m.group(2)))
    # ⚠️ so MAIUSCULA e conteudo. A convencao da casa em todas as pecas: dado
    #    que a crianca ve nasce em CAIXA ALTA (`PARES`, `CENA_A`, `RODADAS`), e
    #    o estado do jogo em minuscula (`cels`, `vagas`, `sombras`). Sem este
    #    corte, o autor do conteudo receberia uma lista com o estado interno da
    #    peca no meio — e mexer nele nao e trocar conteudo, e quebrar a peca.
    # ⚠️ LICAO PAGA (ago/2026): a busca so enxergava `var X = [` e `var X = {`.
    #    So que CONTEUDO tambem e TEXTO — o enunciado da peça, por exemplo. O
    #    `classificar` trazia o balao cravado no corpo ("Cada ficha conta uma
    #    tarefa da PLANTA", resto do Jardim do Broto) e viajava assim para toda
    #    atividade que usasse a mecanica; ao mover o texto para uma gaveta
    #    `var ENUN="..."`, o montador respondeu "ENUN nao e gaveta". Nao era
    #    mesmo: o detector nao sabia ler texto.
    #    Gaveta de TEXTO nunca e a principal (a principal e a lista de rodadas)
    #    — ela entra so na lista das OUTRAS, que e quem o `dadosExtra` preenche.
    textos = []
    for m in re.finditer(r"^var\s+([A-Z][A-Z0-9_$]*)\s*=\s*(\"[^\"\n]*\"|'[^'\n]*')\s*;",
                         js, re.M):
        if m.group(1) in NAO_E_CONTEUDO:
            continue
        textos.append((m.group(1), m.group(2)))
    todas = [a[0] for a in achados if a[0].upper() == a[0]] + [t[0] for t in textos]
    # o exemplo de CADA gaveta, nao so o da principal: e o que permite conferir
    # o formato do `dadosExtra` (foi por falta disso que um `MUDA` no formato
    # errado passou e a fase saiu com ZERO diferencas, dando-se por concluida)
    exemplos = dict((n, js[i:f]) for n, i, f, _t in achados if n.upper() == n)
    for n, v in textos:
        exemplos[n] = v
    # ⭐ as gavetas que a PROPRIA peca declara como tecnicas (ver a licao acima).
    #    A marca fica na linha da `var`, onde quem le a peca a enxerga junto com
    #    o valor: `var LETRAS="ABC..."; /*TECNICA*/`
    tecnicas = sorted(set(
        m.group(1) for m in
        re.finditer(r"^var\s+([A-Z][A-Z0-9_$]*)\s*=[^\n]*/\*\s*TECNICA\s*\*/",
                    js, re.M)))

    if not achados:
        return None, "", "nenhuma", [], {}, tecnicas

    marca = re.search(r"troque APENAS|CONTE[UÚ]DO [EÉ] S[OÓ] EXEMPLO", js, re.I)
    if marca:
        for nome, i, f, _t in achados:
            if i > marca.start():
                return nome, js[i:f], "marca na peca", todas, exemplos, tecnicas
    for nome, i, f, t in achados:
        if t == "[":
            return nome, js[i:f], "primeiro vetor", todas, exemplos, tecnicas
    nome, i, f, _t = achados[0]
    return nome, js[i:f], "primeiro objeto", todas, exemplos, tecnicas


# ⚠️ LIÇÃO PAGA (ago/2026) — PROSA VIRANDO SELETOR, e o defeito era MUDO.
# Escrevi um comentário novo logo abaixo de um comentário que já tinha fechado,
# então o `*/` do meu ficou sobrando e o texto virou CSS. O escopador não tem
# como saber o que é prosa: prefixou tudo e gerou
#     `.mec-ouvir-achar ⚠️ E ELE ERA DESENHADO A BORDA (corpo no `:after`, ... {...}`
# — seletor inválido, que o navegador DESCARTA junto com a regra seguinte. Ou
# seja: a minha regra do alto-falante simplesmente não existia. Nada quebrou,
# nada avisou; só o desenho é que sumiu, e eu só descobri fotografando.
# O portão: seletor de verdade só tem um punhado de caracteres. Qualquer coisa
# fora disso (acento, crase, `⚠`, travessão) é prosa vazada — para tudo e diz
# a linha, em vez de gerar um arquivo com uma regra fantasma dentro.
# (o `%` está na lista porque `0%`/`50%`/`100%` dentro de `@keyframes` são
#  seletores de verdade — foi o primeiro falso-positivo que este portão deu.)
SELETOR_OK = re.compile(r'^[A-Za-z0-9_\-.#>+~*:()\[\]="\'&%\s]*$')
SELETORES_TORTOS = []


# ⚠️ LIÇÃO PAGA (ago/2026) — COMENTÁRIO COM CHAVE DENTRO, o irmão do defeito
# acima e o que o portão novo encontrou sozinho em DUAS peças já no repositório
# (`criar-desafio` e `investigar-fonte`). O escopador quebrava o CSS por CHAVE,
# sem saber o que é comentário. Aí um comentário que EXPLICA uma regra, e por
# isso cita a regra —  `.balao + *{margin-top:13px}` — traz um par de chaves
# dentro de si: a quebra corta o comentário no meio, a primeira metade some e a
# SEGUNDA metade vira o seletor da regra seguinte. Resultado: a regra explicada
# pelo comentário nunca existiu. Mudo, como sempre; `.regra` e `.if_placar`
# estavam mortas havia semanas.
# O conserto: guardar os comentários ANTES de quebrar e devolvê-los depois —
# assim eles nunca participam da conta das chaves.
_COMENT = re.compile(r"/\*.*?\*/", re.S)
_MARCA_COM = re.compile(u"\x00C(\\d+)\x00")

# ⚠️⚠️ LIÇÃO PAGA, e das grandes (ago/2026, achada ao redesenhar a
# `ligar-pontos`): ESTA FUNÇÃO ENGOLIA OS `@keyframes` — TODOS, de TODAS as
# peças. O varredor de blocos só sabia abrir `@media`; o `@keyframes fade{`
# não casava com nenhuma alternativa da expressão, então a linha do cabeçalho
# era simplesmente PULADA (o `finditer` anda para a frente e não avisa), e os
# `0%` / `100%` de dentro viravam SELETORES: `.mec-x 0%{opacity:0}`.
# Resultado medido: **nenhuma peça tinha animação dentro de uma atividade
# montada**. Na peça avulsa tudo animava lindamente — e era só ali que a gente
# olhava. O `@supports` caía no mesmo buraco, e pior: o invólucro sumia e a
# regra de RESERVA passava a valer SEMPRE (era o caso do `:has` na PONTE).
#
# Ninguém pegou porque falta de animação não quebra nada: não há erro de JS,
# nenhum portão reprova, o print fica igual. A tela só fica mais morta — o
# avesso exato do que o Marcos pede ("mais visual"). É o mesmo parentesco do
# comentário que comia a regra seguinte, três parágrafos acima: uma expressão
# regular que não conhece um caso e não tem como dizer que não conhece.
_ABRE_AT = re.compile(
    r"@(?:media|supports|(?:-webkit-|-moz-|-o-)?keyframes)[^{]*\{", re.I)
_KF_NOME = re.compile(
    r"@((?:-webkit-|-moz-|-o-)?)keyframes\s+([A-Za-z0-9_\-]+)", re.I)
_DECL_ANIM = re.compile(
    r"((?:^|[;{\s])(?:-webkit-|-moz-|-o-)?animation(?:-name)?\s*:)([^;}]*)", re.I)


def renomeia_keyframes(css, nome):
    u"""`fade` da peça A e `fade` da peça B são a MESMA animação no arquivo
    final — o CSS não tem escopo para `@keyframes`. A última declarada ganha e
    a outra peça anima errado, calada. Aqui cada uma leva o nome da sua peça."""
    nomes = set(m.group(2) for m in _KF_NOME.finditer(css))
    if not nomes:
        return css

    def novo(n):
        return u"kf-%s-%s" % (nome, n)

    css = _KF_NOME.sub(
        lambda m: u"@%skeyframes %s" % (m.group(1), novo(m.group(2))), css)

    def _troca(m):
        valor = m.group(2)
        for n in nomes:
            valor = re.sub(r"(?<![\w-])%s(?![\w-])" % re.escape(n),
                           novo(n), valor)
        return m.group(1) + valor

    # só dentro de `animation:`/`animation-name:` — o nome da animação pode ser
    # uma palavra comum ("pulso"), e trocar solto reescreveria classe alheia.
    return _DECL_ANIM.sub(_troca, css)


def prefixa_css(css, nome):
    u"""`.opt{...}` vira `.mec-escolher .opt{...}` — duas peças não brigam."""
    # ⚠️ `@media(max-height:520px)` — SEM o espaco — e sintaxe que o navegador
    #    tem o direito de recusar, e recusar uma at-rule faz o parser andar
    #    ate conseguir se reencontrar, comendo regras boas pelo caminho. Vinte
    #    delas moravam nas pecas. Um espaco resolve, e nao muda nada quando ja
    #    estava certo.
    css = re.sub(r"@(media|supports)\(", r"@\1 (", css)
    css = renomeia_keyframes(css, nome)
    guardados = []

    def _guarda(m):
        guardados.append(m.group(0))
        return u"\x00C%d\x00" % (len(guardados) - 1)

    css = _COMENT.sub(_guarda, css)
    saida, pilha = [], []
    # a alternativa do @-bloco vem PRIMEIRO de propósito: se a regra comum
    # viesse antes, um `@supports ... {` sem chave interna seria lido como
    # seletor e prefixado. Ordem aqui é comportamento, não estilo.
    varre = re.finditer(
        r"(@(?:media|supports|(?:-webkit-|-moz-|-o-)?keyframes)[^{]*\{)"
        r"|([^{}]+)(\{[^{}]*\})|(\})", css, re.S)
    for pedaco in varre:
        abre, sel, corpo, fecha = pedaco.groups()
        if abre:
            saida.append(abre)
            pilha.append("kf" if _KF_NOME.match(abre.strip()) else "at")
        elif fecha:
            saida.append("}")
            if pilha:
                pilha.pop()
        elif sel is not None and pilha and pilha[-1] == "kf":
            # DENTRO de um @keyframes, `0%` e `from` são marcos de tempo, não
            # seletores: prefixar é o que produzia `.mec-x 0%{...}`, regra
            # inválida que o navegador descarta inteira.
            saida.append(sel + (corpo or ""))
        elif sel is not None:
            # os comentários que vêm ANTES do seletor saem na frente, inteiros:
            # se entrassem no seletor virariam `.mec-x \x00C3\x00 .regra`.
            cab = re.match(u"^((?:\x00C\\d+\x00|\\s)*)", sel)
            antes, s = sel[:cab.end()], sel[cab.end():].strip()
            if not s or s.startswith("@"):
                saida.append(sel + (corpo or ""))
                continue
            for x in s.split(","):
                if not SELETOR_OK.match(x.strip()):
                    SELETORES_TORTOS.append((nome, " ".join(x.split())[:90]))
            novo = ", ".join(
                (".mec-%s %s" % (nome, x.strip())) if not x.strip().startswith("@") else x
                for x in s.split(","))
            saida.append(antes + "\n" + novo + (corpo or ""))
    return _MARCA_COM.sub(lambda m: guardados[int(m.group(1))], "".join(saida))


u"""⚠️ LIÇÃO PAGA (a marca que o montador procura): a primeira marca era
`/* ---------- nome ---------- */`, e as PRÓPRIAS peças usam esse traço nos
comentários delas ("a regra da fase", "as TRÊS portas de entrada"...). Eram 163
marcas para 74 peças. O `recorta()` do montador partia a peça no meio do primeiro
comentário interno e escrevia meia mecânica na atividade — JS quebrado na mão da
criança. A marca agora é `==== PECA: nome ====`, que nenhuma peça escreve."""
MARCA = u"/* ==== PECA: %s ==== */"

PONTE = u'''
/* ==== PECA: %(nome)s ==== */
MEC["%(nome)s"] = function(f, cen, fim){
  cen.className = cen.className + " mec-%(nome)s";
  /* ⚠️⚠️ LICAO PAGA, e a mais silenciosa de todas: a peca da MEMORIA declara a
     PROPRIA `function fim()`. Como o corpo dela entra dentro do fechamento, esse
     `fim` SOMBREAVA o parametro da ponte — e o `mostraBanner` daqui, que devia
     levar a fase seguinte, chamava a peca de volta. Laco infinito, sem erro de
     JS nenhum: o jogador so ficava PRESO, com todos os pares ja fechados e a
     medalha da peca na tela. Por isso a continuacao mora AQUI FORA, com um nome
     que o integrador confere que nenhuma peca usa (ver `confere_contra_motor`).
     E ela so dispara UMA vez: peca que chama o banner duas vezes pularia fase. */
  var _seguir = function(){ if(_seguir.ja) return; _seguir.ja = 1; fim(); };
  /* recolhe o enunciado da fase assim que a peca puser o balao dela (ver CSS) */
  setTimeout(function(){
    var b = cen.getElementsByClassName("pecabox")[0];
    if(b && b.getElementsByClassName("balao").length)
      cen.className = cen.className + " tembalaopeca";
  }, 120);
  (function(){
    /* a peca acha que esta sozinha; estes ajudantes fazem o meio de campo */
    var app = cen;
    /* o `ac()` DESTA peca: destrava o som (o motor chama isso de `arma()`) e
       devolve o AudioContext do motor. Fica local, dentro do fechamento, para
       nao brigar com o `var ac` do motor — que e o objeto, nao a funcao. */
    function ac(){ if(typeof arma === "function") arma(); return window.ac; }
    function limpa(){ var g = cen.getElementsByClassName("pecabox")[0];
      if(g) g.innerHTML = ""; else { g = document.createElement("div");
      g.className = "pecabox"; cen.appendChild(g); } app = g; }
    /* ⚠️ LICAO PAGA: este ajudante era um VAZIO — "quem manda na barra e o
       motor". So que o caca-palavras faz `setProg(t,0)` e depois PEGA A BARRA
       DE VOLTA (`t.getElementsByTagName("i")[0]`) para mostrar quantas palavras
       ja achou. Com o vazio, ele pegava `undefined` e estourava no primeiro
       toque: 446 erros de JS numa partida. Regra: o ajudante da ponte tem que
       FAZER o que o de verdade faz — nao pode so nao atrapalhar.
       A barra da PECA e a de dentro da fase (5 palavras achadas de 8); a do
       MOTOR e a da atividade (fase 4 de 32). As duas informam coisas
       diferentes, entao as duas ficam — a de dentro, menorzinha (ver CSS). */
    function setProg(t, p){
      if(!t || !t.appendChild) return;
      var pr = document.createElement("div"); pr.className = "prog progpeca";
      var i = document.createElement("i"); i.style.width = (p || 0) + "%%";
      pr.appendChild(i); t.appendChild(pr);
    }
    /* ⚠️⚠️ LICAO PAGA (ago/2026), pega pelo Marcos JOGANDO: *"esta passando de
       fase sem aquele botao azul que aparecia com a palavra proximo... tem que
       ser parecida com a atividade do Broto"*.

       Esta ponte comemorava e PULAVA para a fase seguinte sozinha, 420ms
       depois. A crianca terminava uma fase e era JOGADA na outra: sem a tela de
       parabens, sem o mascote dizendo o que ela conseguiu, sem o botao para ela
       decidir quando seguir. No Broto — que e o modelo — cada fase fecha com o
       banner e a crianca TOCA para continuar. Era o fecho de toda fase de toda
       atividade montada que estava faltando.

       Agora a ponte chama o banner DE VERDADE do motor (`window.mostraBanner`,
       que a funcao local aqui dentro sombreia) e entrega o `_seguir` como o
       botao. A peca continua so avisando que acabou; quem manda no caminho
       segue sendo o motor — mas com a comemoracao no meio. */
    function mostraBanner(msg, cb){
      if(typeof festa === "function") festa();
      /* ⚠️⚠️ LICAO PAGA (Teatro, ago/2026), o Marcos jogando: uma fase fechava
         com um "QUADRADO GRANDE desconfigurado" em vez do aviso fininho das
         outras. Causa: 7 pecas (pintar, pintar-canvas, memoria, sete-erros,
         achar-na-cena, camadas-mapa, tracar-caminho) mandam no aviso de fim
         `<div class="medal">★</div>`. No motor a `.medal` e a MEDALHA DE 190px
         do FIM da atividade (imagem do mascote), entao o motor inflava aquilo
         num quadradao verde vazio com uma estrelinha. O aviso de FASE nao leva
         medalha — o motor ja comemora com confete. Tiro a medalha do aviso de
         fase aqui (conserto central: pega as 7 de uma vez). */
      if(msg) msg = msg.replace(/<div[^>]*class=["']?[^"'>]*\bmedal\b[^"'>]*["']?[^>]*>[\s\S]*?<\/div>/gi, "");
      if(typeof window.mostraBanner === "function"){
        window.mostraBanner(msg || "Muito bem!", _seguir); return;
      }
      setTimeout(_seguir, 420);
    }
    /* ⚠️⚠️ LICAO PAGA (ago/2026), e foi o Marcos quem ouviu: *"onde tenho que
       ouvir a palavra nao funciona; o enunciado funciona, os sons das opcoes
       funcionam"*. So o botao OUVIR A PALAVRA era mudo.
       A causa: a peca sozinha nao tem gravacao nenhuma, entao ela fala pela
       VOZ ROBO do navegador (`speechSynthesis`). No PC da escola essa voz
       simplesmente nao existe (nao ha voz pt-BR instalada) — e falha CALADA,
       sem erro nenhum. O enunciado e as opcoes funcionavam porque passam pelo
       motor, que toca MP3 gravado.
       Aqui a ponte reaponta o `diz` da peca para a voz da casa. A conta da
       chave ignora maiusculas (`chaveVoz` faz `toLowerCase`), entao a palavra
       "pao" acha a gravacao feita para "PAO" — a mesma que o alto-falante da
       opcao ja usa. So cai na voz do navegador se nao houver gravacao. */
    var diz = function(txt){
      try{
        /* ⚠️⚠️ LICAO PAGA (ago/2026), e foi o Marcos quem OUVIU: *"o da padaria
           agora e falado duas vezes juntos, soa estranho"*.
           Varias pecas ganharam, no mesmo dia, a boa ideia de NARRAR SOZINHAS ao
           abrir — porque na bancada, sem motor, a fase ficava muda. So que dentro
           da atividade quem narra o balao e o MOTOR, sempre narrou. As duas vozes
           partiam juntas e se atropelavam.
           A peca nao tem como saber se esta na bancada ou na atividade; quem sabe
           e a ponte. Entao e AQUI que se decide: se o texto pedido e o mesmo que o
           motor ja esta dizendo (ou acabou de dizer, na meia janela de abertura da
           fase), a peca cala — o motor ja cumpriu o pedido dela. Qualquer outra
           fala (a palavra, a silaba, a dica) passa normalmente. */
        var _limpa = function(s){ return String(s||"").replace(/<[^>]*>/g," ")
          .replace(/&[a-z]+;|&#\d+;/gi," ").replace(/\s+/g," ").trim().toLowerCase(); };
        var _agora = _limpa(txt);
        if(_agora && window.__dizMotor && window.__dizMotor === _agora) return;
        try{
          var _b = document.getElementsByClassName("balao")[0];
          if(_b && _limpa(_b.textContent) === _agora){
            window.__dizMotor = _agora;
            setTimeout(function(){ window.__dizMotor = null; }, 1200);
            return;
          }
        }catch(_e){}
        var k = (typeof temVoz === "function") ? temVoz(txt) : null;
        if(k && typeof tocaVoz === "function"){ tocaVoz(k); return; }
        if(!window.speechSynthesis || !window.SpeechSynthesisUtterance) return;
        var u = new SpeechSynthesisUtterance(txt);
        u.lang = "pt-BR"; u.rate = .9; u.pitch = 1.05;
        window.speechSynthesis.cancel(); window.speechSynthesis.speak(u);
      }catch(e){}
    };
    limpa();
%(corpo)s
  })();
};
'''


CSS_PONTE = u'''
/* ⭐ O BOTAO "PROXIMO" generico (ver o FERRAMENTAS). Mesmo desenho do Broto:
   azul, grande, com a sombra embaixo que afunda ao apertar. */
.pxprox{display:block;margin:14px auto 10px;min-height:52px;padding:13px 30px;border:0;
  border-radius:26px;font-size:19px;font-weight:800;color:#fff;cursor:pointer;
  background:-webkit-gradient(linear,left top,left bottom,from(#3aa0f5),to(#2472c8));
  background:linear-gradient(#3aa0f5,#2472c8);box-shadow:0 5px 0 #1a5698;
  -webkit-animation:pxentra .28s ease;animation:pxentra .28s ease}
.pxprox:active{-webkit-transform:translateY(4px);transform:translateY(4px);box-shadow:0 1px 0 #1a5698}
@-webkit-keyframes pxentra{from{-webkit-transform:translateY(10px);opacity:0}}
@keyframes pxentra{from{transform:translateY(10px);opacity:0}}
@media (prefers-reduced-motion:reduce){ .pxprox{-webkit-animation:none;animation:none} }

/* ⭐ A FESTA DO ACERTO — o CSS da comemoracao generica (ver o olheiro no
   FERRAMENTAS). Vale para as 76 mecanicas: quem ganha a marca de certo pula, e
   sobem faisquinhas. Cobranca do Marcos: "nao tem a comemoracao quando acerta
   como no Broto". */
.pfaisca{position:fixed;width:9px;height:9px;border-radius:50%;pointer-events:none;
  z-index:60;-webkit-animation:pfsobe .95s ease-out forwards;animation:pfsobe .95s ease-out forwards}
@-webkit-keyframes pfsobe{0%{-webkit-transform:translateY(0) scale(.4);opacity:0}
  25%{opacity:1}100%{-webkit-transform:translateY(-58px) scale(1.15);opacity:0}}
@keyframes pfsobe{0%{transform:translateY(0) scale(.4);opacity:0}
  25%{opacity:1}100%{transform:translateY(-58px) scale(1.15);opacity:0}}
.pfesta{-webkit-animation:pfpula .5s ease;animation:pfpula .5s ease}
@-webkit-keyframes pfpula{0%,100%{-webkit-transform:scale(1)}40%{-webkit-transform:scale(1.07)}}
@keyframes pfpula{0%,100%{transform:scale(1)}40%{transform:scale(1.07)}}
@media (prefers-reduced-motion:reduce){
  .pfaisca{display:none}
  .pfesta{-webkit-animation:none;animation:none}
}

/* ============================================================
   ⭐⭐ O JEITO DO BROTO — o molde visual da casa, para as 76 pecas.

   Ordem do Marcos (ago/2026), depois de abrir a Padaria: *"quero atividade
   bonita tipo app como o broto, o visual tem que ser mais caprichado"* e
   *"a atividade tem que ser nos moldes do que a gente vinha fazendo por
   ultimo, com o molde do broto"*.

   ⚠️ O QUE EU TINHA ERRADO: extrai do Broto a MOLDURA (capa, cracha, barra,
   banner, boletim) e deixei as FASES com o visual de cada peca, que nasceu na
   bancada — cartao branco chapado, borda fina, tudo encostado a esquerda. Por
   fora era o Broto; por dentro, nao. Todos os defeitos visuais que ele apontou
   numa noite (nome fora do quadro, letra pela metade, quadrado desalinhado,
   silaba sem cor) sao ESTE unico problema.

   Os valores abaixo NAO foram inventados: sao os do proprio `_jardim/index.html`
   — a mesma paleta, o mesmo raio, a mesma sombra, e a assinatura da casa, que e
   a BORDA DE BAIXO MAIS GROSSA (5px). E ela que da o ar de app, de peca que da
   para apertar.

   Especificidade: as regras da peca entram como `.mec-<nome> .opt` (0,2,0).
   Estas usam tres classes (0,3,0) de proposito — precisam ganhar, e sem
   `!important`, que seria pior de depurar.
   ============================================================ */
/* ⚠️⚠️ LICAO PAGA (ago/2026) — ERA ESTA REGRA que punha o QUADRADO BRANCO
   atras das figuras. Ela unifica o cartao de TODAS as pecas (e por isso usa
   tres classes, para ganhar das regras da peca) — e por isso mesmo o creme
   OPACO dela chegava tambem no cartao que segura uma figura RECORTADA. O
   portao 5b acusou em duas atividades, em quatro tamanhos de tela cada.
   Eu tinha "consertado" nas pecas, uma a uma, e nao adiantou: a regra da peca
   e (0,2,0) e esta e (0,3,0) — quem manda e aqui.
   `.88` continua sendo um cartao creme (a tinta escura passa folgada) e deixa
   a figura assentar na cena em vez de flutuar num retangulo branco. */
.centro .pecabox .opt,.centro .pecabox .pc,.centro .pecabox .ficha,.centro .pecabox .cx{
  background:rgba(255,253,246,.88);border:2px solid #e6dcc6;border-bottom-width:5px;
  border-radius:18px;color:#3a3020;font-weight:600;
  -webkit-box-shadow:0 5px 12px rgba(30,50,20,.16);box-shadow:0 5px 12px rgba(30,50,20,.16)}
.centro .pecabox .opt.ok,.centro .pecabox .pc.ok{border-color:#5bbf3a;background:#eafce0}
.centro .pecabox .opt.no{border-color:#ff7a6b;background:#fff0ee}
.centro .pecabox .balao{background:rgba(255,253,246,.95);border:0;border-radius:22px;
  padding:13px 18px;font-size:17px;font-weight:600;line-height:1.35;
  -webkit-box-shadow:0 6px 18px rgba(30,50,20,.22);box-shadow:0 6px 18px rgba(30,50,20,.22)}
.centro .pecabox .selo{background:#7d3fe0;color:#fff;font-size:13px;font-weight:700;
  padding:5px 12px;border-radius:999px}
/* ⚠️ `background-color`, NUNCA o atalho `background:` — o desenho do
   alto-falante e um SVG que mora no `background-image` do `.zap` (motor). O
   atalho zera o `background-image` junto, e o botao fica um circulo VAZIO.
   Foi exatamente o que aconteceu no dia em que o SVG entrou: no cartao da
   `ouvir-achar` o desenho aparecia, e nas fases de `completar` — que passam
   por esta ponte — o circulo saia em branco. */
.centro .pecabox .zap{width:30px;height:30px;border-radius:50%;
  background-color:rgba(58,48,32,.09);border:0;opacity:.62;padding:0}
/* ⚠️ .55 DE PRATO NAO SEGURA LETRA BRANCA (medido, ago/2026): sobre o ceu
   claro da atividade a mistura dava 3,7:1 — abaixo dos 4,5 — em 14 fases.
   Prato translucido nao e cor: e uma MEDIA com o que estiver atras, e o que
   esta atras muda de tela para tela. Opacidade suficiente para o pior caso
   (fundo branco) e a unica que vale nos dois temas. */
.centro .pecabox .hint{color:#fffdf6;background:rgba(58,48,32,.86);border-radius:999px;
  padding:6px 14px;display:inline-block;font-size:14px}

/* ⭐ O ALTO-FALANTE NAO PODE ESCAPAR DO CARTAO (medido, ago/2026)
   Achado pelo `_qa/vaza.js` — o portao que o Marcos fez nascer quando viu *"o
   dizer da figura fica fora do quadrado branco, ficou feio"*. Ele estava
   pronto ha semanas e NUNCA rodava sozinho: nao estava na banca. Ligado,
   achou na primeira corrida.
   O caso: pecas como a `arrastar-lugar` desenham um cartao de tamanho FIXO
   (74x70px). O motor poe dentro dele o alto-falante da resposta (30px + 8px
   de margem), porque `.pc` esta na lista das respostas tocaveis — e o botao
   sobrava 18px para fora, em TODOS os tamanhos de tela.
   O conserto certo nao e encolher o alto-falante (ele e alvo de dedo de
   crianca e ja esta no minimo): e o cartao CRESCER para caber o que puseram
   dentro dele. Largura e altura viram minimo, e o conteudo manda. */
.centro .pecabox .pc:has(> .zap){width:auto;height:auto;
  min-width:74px;min-height:70px;padding-right:6px}
/* queda para o Chrome 109 da escola, que nao tem `:has()`: ali o cartao ganha
   a folga sempre — dois pixels a mais num cartao sem alto-falante nao fazem
   mal a ninguem, e botao pela metade faz. */
@supports not (selector(:has(*))){
  .centro .pecabox .mec-arrastar-lugar .pc{width:auto;height:auto;
    min-width:74px;min-height:70px}
}

/* ⭐⭐ TEXTO SOLTO SOBRE O FUNDO TEM QUE TER PLACA (medido, ago/2026)
   Pedido do Marcos: *"sempre verificar se nao ha um contraste nas cores, para
   que nao aconteca de a crianca nao conseguir enxergar"*.

   O defeito e de PARENTESCO, nao de descuido: na bancada a peca roda sobre um
   fundo LISO e escuro (#2b2118), e ali o creme e o amarelo dela passam
   folgado. Dentro da atividade o mesmo texto cai sobre a FOTO — a madeira da
   padaria, o ceu do observatorio — e a razao despenca. Medido na Padaria
   depois que o portao do contraste passou a enxergar as fases: 45 textos
   abaixo do minimo, o pior a 1,95:1 ("A PALAVRA E / PAO" em cima da estante).
   Nenhum deles aparecia antes, porque o portao so media as telas de nome.

   A regra da casa: rotulo, contador e frase que ficam DIRETO sobre o fundo
   ganham uma placa escura translucida — o cartao ja tem a dele. A lista cresce
   quando o portao achar um caso novo (agora ele acha).                        */
.centro .pecabox .cont,.centro .pecabox .palv,.centro .pecabox .palvr,
.centro .pecabox .bsVazio,.centro .pecabox .csDiz,.centro .pecabox .csConta,
.centro .pecabox .csEsc,.centro .pecabox .frase,.centro .pecabox .m2_placar{
  display:inline-block;background:rgba(38,28,20,.78);color:#fdf7ec;
  border-radius:14px;padding:5px 14px;opacity:1}
/* a vaga de arrastar tambem: a placa escura faz o numero aparecer E marca melhor
   o lugar onde a peca entra. */
.centro .pecabox .cam{background:rgba(38,28,20,.62);color:#fdf7ec}
/* ⚠️ O BOTAO CLARO DA PECA (o "Recomecar" do pintar) — 1,24:1 medido, creme
   sobre creme. `.btn` e vocabulario COMUM: a regra da peca nao e prefixada e
   quem manda na cor e o tema da atividade, que pinta a letra de creme para a
   madeira escura. So que `.bclaro` troca o fundo para bege e a letra creme
   some. Quem muda o FUNDO tem que mudar a LETRA junto. */
.centro .pecabox .bclaro{color:#3a2a12;text-shadow:0 1px 0 rgba(255,245,220,.55)}

/* ⭐ O MEDALHAO: no Broto a figura da rodada e GRANDE, redonda e centrada — a
   arte e a estrela da tela, nao um selinho no canto do cartao. */
.centro .pecabox .medalhao{width:168px;height:168px;margin:12px auto 4px;border-radius:50%;
  background:rgba(255,253,246,.97);border:4px solid rgba(255,255,255,.75);padding:14px;
  display:-webkit-box;display:flex;-webkit-box-align:center;align-items:center;
  -webkit-box-pack:center;justify-content:center;
  -webkit-box-shadow:0 8px 22px rgba(30,50,20,.24);box-shadow:0 8px 22px rgba(30,50,20,.24)}
.centro .pecabox .medalhao img{width:100%;height:100%;object-fit:contain;display:block}
@media (max-height:620px){ .centro .pecabox .medalhao{width:124px;height:124px;padding:10px} }

/* ==== O QUE A PONTE PRECISA (vale para todas as mecanicas) ==== */
/* a barra de DENTRO da fase (quantas palavras achou, que rodada e esta) — a de
   cima, do motor, e a da atividade inteira. Duas informacoes diferentes, entao
   as duas ficam; esta e menorzinha para nao competir com a de cima.          */
.progpeca{height:6px;margin:2px 0 10px;opacity:.85}
/* ⚠️ o SELO da peca e o mesmo rotulo que o motor ja poe em cima, vindo do
   conteudo.json: duas plaquinhas iguais, uma embaixo da outra, so ocupam a tela
   da crianca. O BALAO da peca FICA — nele mora a pergunta da rodada, que muda
   dentro da fase e nao esta no enunciado.                                    */
.pecabox .selo{display:none}
/* ⚠️ LICAO PAGA, medida: com o enunciado da FASE em cima e o balao da PECA
   logo abaixo, o tabuleiro do jogo da memoria comecava tao baixo que 4 das 8
   cartas caiam fora da tela de 640px do monitor da escola. Da para rolar, mas
   memoria e um jogo de VER o tabuleiro: metade escondida acaba com a mecanica.
   E o dobro de enunciado tambem e defeito por si so — a regra da casa e uma
   ideia por tela, enunciado curto (carga cognitiva).
   Entao: quando a peca escreve o balao DELA (a pergunta da rodada), o
   enunciado da fase recolhe. Ele ja foi FALADO na abertura da fase, e o botao
   "Ouvir de novo" continua repetindo — nao se perde nada, ganha-se a tela. */
.centro.tembalaopeca > .balao{display:none}
/* ⚠️⚠️ A COLISAO DE CSS QUE DESMONTAVA O TABULEIRO. Toda peca constroi a tela
   dela com `el("div","tela")` e `el("div","centro")` — os mesmos nomes do
   motor, o que ate aqui era uma vantagem (por isso nenhuma peca precisou ser
   reescrita). So que no motor `.tela` e uma CAMADA ABSOLUTA DE TELA CHEIA
   (`position:absolute;inset:0`) em coluna. Dentro da fase, a tela da peca
   virava uma camada solta por cima de tudo, sem largura propria — e o
   tabuleiro do jogo da memoria, que devia ficar em 3 colunas, empilhava as 8
   cartas numa coluna so, 950px de altura: quatro delas fora da tela do
   monitor da escola. Medido: as 8 cartas no MESMO x.
   Aqui a tela da peca volta a ser o que ela e por dentro da fase: um bloco
   comum. O CSS proprio da peca (com `.mec-<nome>` na frente) manda no resto. */
.pecabox{width:100%}
.pecabox > .tela{position:static;inset:auto;display:block;padding:0;
  -webkit-animation:none;animation:none;height:auto;overflow:visible}
.pecabox > .tela > .centro{width:100%}
'''


FERRAMENTAS = u'''
/* ⭐⭐ UMA VOZ SO. ⚠️ LICAO PAGA (ago/2026), pega pelo Marcos jogando: *"nas
   atividades tem duas vozes falando ao mesmo tempo"*.

   15 das 76 pecas usam a voz do NAVEGADOR (`speechSynthesis`) para nao ficarem
   mudas quando sao testadas SOZINHAS na bancada — o que e certo la. Mas dentro
   de uma atividade montada quem fala e o MOTOR, com o mp3 do Edge TTS: as duas
   vozes saem juntas, uma por cima da outra. So duas pecas tinham o guarda.

   Aqui a voz do navegador e DESLIGADA de uma vez, para as 76: numa atividade
   montada existe o mp3, e voz de navegador nunca vai para a crianca (regra da
   casa). O que a peca queria dizer continua sendo dito — pelo olheiro do balao,
   com a voz de verdade. */
/* ⚠️⚠️ LICAO PAGA (ago/2026), e o Marcos pegou NO CELULAR, nao no PC:
   *"tem voz do navegador junto com a voz do Antonio e as vezes os dois falam ao
   mesmo tempo"*. No meu teste de mesa a medicao dava ZERO chamadas — e dava
   mesmo. A primeira versao deste guarda fazia
       window.speechSynthesis.speak = vazio;
   que e uma atribuicao de propriedade PROPRIA num objeto do navegador. No
   Chrome de mesa ela cria a sombra e funciona; no celular (e no Safari) o
   objeto costuma recusar a propriedade nova **em silencio** — sem erro, sem
   excecao — e o `speak` original continua ali, falando por cima do mp3 do
   Antonio.
   Por isso agora sao TRES camadas, e basta uma pegar:
     1. trocar o `window.speechSynthesis` inteiro por um objeto inerte;
     2. neutralizar o `speak` no PROTOTIPO (pega quem guardou a referencia);
     3. deixar o `SpeechSynthesisUtterance` sem texto — sem fala para enfileirar.
   A licao geral: guarda que depende de UMA atribuicao funcionar nao e guarda.
   E teste de mesa nao prova celular — o navegador de la e outro bicho. */
(function(){
  var vazio = function(){};
  var inerte = {
    speak: vazio, cancel: vazio, pause: vazio, resume: vazio,
    getVoices: function(){ return []; },
    speaking: false, pending: false, paused: false
  };
  /* 1) o objeto inteiro */
  try{ if(window.speechSynthesis) window.speechSynthesis.cancel(); }catch(e){}
  try{ Object.defineProperty(window, "speechSynthesis", {
         configurable: true, get: function(){ return inerte; } }); }catch(e){}
  /* 2) o prototipo — pega quem guardou a referencia antes de mim */
  try{ if(window.SpeechSynthesis && window.SpeechSynthesis.prototype){
         window.SpeechSynthesis.prototype.speak = vazio;
         window.SpeechSynthesis.prototype.cancel = vazio; } }catch(e){}
  /* 3) a propria fala nasce vazia */
  try{ if(window.SpeechSynthesisUtterance){
         var U = window.SpeechSynthesisUtterance;
         window.SpeechSynthesisUtterance = function(){ var u = new U(""); u.text = ""; return u; };
         window.SpeechSynthesisUtterance.prototype = U.prototype; } }catch(e){}
  /* 4) ultima linha: se ainda assim algo falar, cala na hora */
  try{ setInterval(function(){
         try{ if(inerte.speaking) inerte.cancel(); }catch(e){}
       }, 1500); }catch(e){}
})();

/* ==== A VOZ DA RODADA ====
   ⭐ O pilar SONORO, medido pela banca: *"16 fase(s) MUDA(S), sem nenhuma
   narracao"* e *"16 perguntas que mudam na tela sem mudar a voz — quem nao le
   aperta o alto-falante e ouve outra coisa"*.

   Por que acontecia: o motor narra o ENUNCIADO DA FASE (o do conteudo.json).
   Mas a peca troca a pergunta DENTRO da fase, a cada rodada, e essa troca o
   motor nao via. A crianca de 2o ano ouvia a instrucao da 1a rodada e, da 2a
   em diante, ficava sem instrucao nenhuma. E o botao "Ouvir de novo" repetia a
   fala da fase, nao a pergunta que estava na tela — pior que silencio.

   O conserto nao e por mecanica (seriam 74): e um olheiro no balao. Toda vez
   que o texto do balao de dentro da fase muda, se existir voz gravada para
   AQUELE texto (a conta e o sha do proprio texto, a mesma do alto-falante das
   respostas), ele fala. Como o `falas.json` sai do proprio `dados`, a voz e o
   texto nao tem COMO divergir.                                              */
(function(){
  var ultimo = "";
  function olha(){
    var box = document.getElementsByClassName("pecabox")[0];
    if(!box) { ultimo = ""; return; }
    var bs = box.getElementsByClassName("balao");
    if(!bs.length) return;
    var b = bs[0], txt = (b.textContent || "").replace(/\s+/g, " ").replace(/^ | $/g, "");
    if(!txt || txt === ultimo) return;
    ultimo = txt;
    /* ⭐ a voz de CADA RODADA e so para quem nao le (ate o 2o ano). Do 3o em
       diante a instrucao da fase ja foi narrada uma vez e o resto e por botao —
       repetir a cada rodada e o que o Marcos disse que os maiores nao gostam. */
    if(typeof ID === "object" && ID.narrar !== "tudo") return;
    if(typeof temVoz !== "function") return;
    var k = temVoz(txt);
    /* sem voz gravada nao inventa nada: ficar calado e melhor que falar
       outra coisa (foi esse o defeito que o Marcos cobrou tres vezes). */
    /* ⚠️ SEM ECO: o motor ja le o balao ao abrir a fase e fala. Se o olheiro
       falar o MESMO texto, o audio reinicia e a crianca ouve o comeco duas
       vezes — foi o que o Marcos ouviu. O olheiro so entra quando a pergunta
       MUDA dentro da fase, que e para isso que ele existe. */
    if(k && k === window.__falouAgora) return;
    window.__falouAgora = k;
    /* o arquivo gravado e `op_<conta>.mp3` — ver o mesmo conserto no motor */
    if(k && typeof falaDaTela === "function") falaDaTela("op_" + k);
  }
  if(window.MutationObserver){
    var alvo = document.getElementById("app");
    if(alvo) new MutationObserver(function(){ setTimeout(olha, 70); })
      .observe(alvo, {childList:true, subtree:true, characterData:true});
  }
})();

/* ⭐⭐ A COMEMORACAO DO ACERTO — PARA AS 76 MECANICAS DE UMA VEZ.

   Cobranca do Marcos (ago/2026), testando no celular: *"nao tem a comemoracao
   quando acerta como no Broto"*. Eu tinha consertado na peca que ele testou —
   e ele respondeu "com certeza" quando ofereci levar para as outras.

   ⚠️ POR QUE AQUI E NAO EM CADA PECA: sao 76 pecas, cada uma com o seu jeito de
   marcar o acerto. Consertar uma a uma seria 76 chances de esquecer uma, e a
   proxima peca nasceria sem festa de novo. Aqui e UM lugar: o olheiro ja
   observa o `#app` inteiro, entao ele tambem VE o momento em que um elemento
   ganha a marca de certo — `ok`, `certa`, `acerto`, `feito` — e comemora.

   O que a crianca ve: o alvo PULA e sobem faisquinhas coloridas em volta. Sem
   imagem, sem biblioteca, some sozinha em 1s. Respeita quem pediu menos
   animacao (`prefers-reduced-motion`), que e acessibilidade e nao enfeite. */
(function(){
  if(!window.MutationObserver) return;
  var app = document.getElementById("app");
  if(!app) return;
  /* ⚠️ cada mecanica chama o acerto pelo SEU nome. Medido nas 11 da Padaria:
     `ok`/`certa` (escolher, ordenar), `cheia` (vaga preenchida em juntar-silabas
     e pintar), `par` (memoria). Sem esta lista a festa so aparecia em 5 das 11 —
     e eu quase reportei "vale para todas".
     ⚠️ `usada` FICA DE FORA de proposito: em `ouvir-achar` ela marca a opcao JA
     TENTADA, ou seja, um ERRO. Comemorar erro e pior que nao comemorar. */
  var MARCA = /(^|\s)(ok|certa|acerto|acertou|feito|cheia|par|casada|encaixou)(\s|$)/;
  var vistos = "__jaFestejou";
  /* ⚠️ LICAO PAGA: isto era lido UMA VEZ, no carregamento, e guardado. Se o
     navegador respondesse "reduce" naquele instante — ou se a leitura falhasse
     — a comemoracao ficava desligada para SEMPRE naquela sessao, sem nenhum
     sinal. Preferencia do usuario se pergunta NA HORA de usar, nao se congela
     no boot. */
  function menosAnimacao(){
    try{ return !!(window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion:reduce)").matches); }catch(e){ return false; }
  }

  /* ⭐⭐ A COMEMORACAO E A DO BROTO — a mesma, nao uma parecida.
     Cobranca do Marcos: *"veja a comemoracao do Broto nos acertos, quero
     igual, como estavamos fazendo ate agora"*.
     ⚠️ Eu tinha escrito faisquinhas de CSS. Ficou parecido e nao era igual — e
     o pior: o confete DE VERDADE ja estava no motor (o canvas `#conf`, o
     `faisca()`, o `festa()`, o `sCerto()` de tres notas e o `elogio()` falado),
     herdado do Broto. Faltava so CHAMAR. Reescrever o que ja existe e o erro
     que o CLONAR-MOTOR.md manda evitar; aqui ele apareceu na forma mais boba,
     a de imitar em CSS o que ja estava pronto em canvas. */
  function faiscas(el){
    if(menosAnimacao()) return;
    try{
      var r = el.getBoundingClientRect();
      if(!(r.width > 4)) return;
      var x = r.left + r.width / 2, y = r.top + r.height / 2;
      /* as mesmas cores e a mesma quantidade do Broto */
      if(typeof faisca === "function"){
        faisca(x, y, "#8be05a", 12);
        faisca(x, y, "#ffd43b", 8);
      }
    }catch(e){}
  }

  /* o som e a voz do acerto, tambem os do Broto */
  var _ultElogio = 0;
  function somDoAcerto(){
    /* ⚠️ O GUARDA "UMA VOZ POR VEZ" DO MOTOR NAO PEGA ESTE CASO, e foi por isso
       que ele escapou: o motor compara o NOME do audio (`_ultVoz.k`), e o
       elogio sorteia um arquivo diferente a cada vez (`ce_acerto2`,
       `ce_acerto3`). Dois elogios seguidos sao dois nomes diferentes — para o
       guarda, duas falas legitimas. Aqui quem manda e o RELOGIO: elogiar duas
       vezes em menos de um segundo nao e reforco, e atropelo.
       (A peca pode marcar o segundo elemento um instante depois do primeiro,
       entao a varredura roda duas vezes e cada uma acha UM elemento novo —
       contar por varredura, sozinho, nao bastava.) */
    var ag = (new Date()).getTime();
    if(ag - _ultElogio < 1000) return;
    _ultElogio = ag;
    try{ if(typeof sCerto === "function") sCerto(); }catch(e){}
    try{ if(typeof elogio === "function") elogio(); }catch(e){}
  }

  function olhaAcerto(){
    var todos = app.querySelectorAll("*"), i, achou = 0;
    for(i = 0; i < todos.length; i++){
      var e = todos[i];
      if(e[vistos]) continue;
      if(!MARCA.test(" " + (e.className || "") + " ")) continue;
      var r = e.getBoundingClientRect();
      /* so o que a crianca TOCA e ve: alvo de verdade, nao um marcador de 2px */
      if(r.width < 28 || r.height < 24) continue;
      e[vistos] = 1;
      e.className = e.className + " pfesta";
      faiscas(e);
      achou++;
      (function(x){ setTimeout(function(){
        x.className = String(x.className).replace(/\s*pfesta/, ""); }, 620); })(e);
    }
    /* ⚠️ LICAO PAGA (ago/2026), e e a TERCEIRA da familia "duas vozes juntas",
       que o Marcos ja ouviu duas vezes: *"o da padaria agora e falado duas
       vezes juntos, soa estranho"*. O elogio estava DENTRO do laco, entao um
       unico toque que marca DOIS elementos de uma vez — o `completar` acende a
       lacuna E a palavra escolhida — disparava `ce_acerto1` e `ce_acerto2` no
       mesmo instante. A FAISCA e de cada peca que acendeu (o olho aguenta duas);
       o ELOGIO e do ACERTO, que e um so. Um por varredura, sempre. */
    if(achou) somDoAcerto();
  }
  /* ⚠️ AQUI MOROU, POR UMA HORA, UM "PROXIMO" GENERICO — e ele foi DESFEITO.
     A ideia: segurar o `setTimeout` que a peca marca depois do acerto e pendurar
     o botao no lugar dele. Funciona em teoria e eu nao consegui PROVAR que
     funciona nas mecanicas de arrastar — o meu teste nao sabe acertar nelas.
     Deixar no ar um codigo que mexe no RELOGIO das 76 pecas sem medicao seria
     apostar com a aula do Marcos. A regra da casa vale para mim tambem: nao se
     entrega o que nao se mediu.
     O caminho certo e por PECA, uma a uma, cada uma com o seu teste — como foi
     feito na `ouvir-achar`, onde o botao esta medido e funcionando. */
  new MutationObserver(function(){ setTimeout(olhaAcerto, 60); })
    .observe(app, {childList:true, subtree:true, attributes:true,
                   attributeFilter:["class"]});
})();
/* ==== FERRAMENTAS QUE AS PECAS USAM E O MOTOR NAO TINHA ====
   ⚠️ LICAO PAGA (achada pelo auditor-jogador, na 3a fase): o integrador so
   trazia o SEGUNDO <script> da peca (a mecanica). O PRIMEIRO — o motorzinho do
   MOLDE — ficava para tras, e com ele o `nota()` que faz o som. A peca escolher
   passou, a completar passou, e a MEMORIA morreu no primeiro som de carta
   virando. O motor tem `tom()`, mas as pecas foram afinadas com estes numeros
   (PESQUISA-SOM-E-GAMEFEEL), entao o `nota` vem junto.

   ⚠️⚠️ E A SEGUNDA METADE DA MESMA LICAO: o `ac` da peca e uma FUNCAO (destrava
   o som), e o `ac` do motor e o OBJETO AudioContext — o mesmo que alimenta o
   lip-sync do mascote. Declarar a funcao aqui NAO deu erro nenhum: o `var ac=`
   do motor simplesmente sobrescreveu, e a memoria voltou a morrer, agora com
   'ac is not a function'. Nome igual e TIPO diferente e a colisao que nao
   aparece. Solucao: `nota` usa o AudioContext do motor direto, e cada peca
   ganha o SEU `ac()` local dentro do fechamento (ver PONTE) — que destrava com
   `arma()`, o nome que o motor usa para isso, e devolve o contexto.

   Todo o resto do motorzinho (el, limpa, setProg, mostraDica, mostraBanner,
   baguncar, sCerto, sErro, sTap, festa) o motor ja tem com o MESMO nome E o
   mesmo tipo — e por isso a peca nunca precisou ser reescrita. */
function nota(f, dur, vol, tipo, atraso){
  if(typeof arma === "function") arma();
  var c = window.ac; if(!c || !c.createOscillator) return;
  try{
    var o = c.createOscillator(), g = c.createGain(), t = c.currentTime + (atraso||0);
    o.type = tipo || "triangle"; o.frequency.value = f;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol || 0.18, t + 0.014);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); g.connect(c.destination); o.start(t); o.stop(t + dur + 0.02);
  }catch(e){}
}
/* ⭐ CONFETE — o Marcos pediu a memoria "fantastica, com confetes" (ago/2026).
   ⚠️ LICAO PAGA: a peca definia `confete` no PRIMEIRO <script> (o motorzinho de
   bancada), que o integrador NAO traz — entao no jogo montado o `confete(20)`
   da mecanica estourava "confete is not defined", calado, so com a crianca na
   frente. Como e util a qualquer mecanica (nao so a memoria), mora aqui, no
   motor, e traz o proprio @keyframes injetado uma vez — sem depender do CSS da
   peca (que tambem pode nao vir). DOM puro, se limpa sozinho. */
function confete(n){
  try{
    if(!document.getElementById("kf-confete")){
      var s=document.createElement("style"); s.id="kf-confete";
      s.textContent="@-webkit-keyframes mcai{to{-webkit-transform:translateY(112vh) rotate(680deg);transform:translateY(112vh) rotate(680deg);opacity:.2}}@keyframes mcai{to{-webkit-transform:translateY(112vh) rotate(680deg);transform:translateY(112vh) rotate(680deg);opacity:.2}}";
      document.head.appendChild(s);
    }
    var cores=["#ff5252","#ffd54a","#59c24b","#3c9bff","#c58bf0","#ff9f43","#26d0b0"];
    var box=document.createElement("div");
    box.style.cssText="position:fixed;left:0;top:0;right:0;bottom:0;pointer-events:none;z-index:9999;overflow:hidden";
    var i,N=n||36;
    for(i=0;i<N;i++){
      var p=document.createElement("i"),c=cores[i%cores.length];
      var L=Math.random()*100, dur=1.1+Math.random()*1.2, del=Math.random()*.25, sz=6+Math.random()*8;
      p.style.cssText="position:absolute;top:-16px;left:"+L+"%;width:"+sz+"px;height:"+(sz*0.6)+
        "px;background:"+c+";border-radius:2px;opacity:.96;"+
        "-webkit-animation:mcai "+dur+"s "+del+"s ease-in forwards;animation:mcai "+dur+"s "+del+"s ease-in forwards";
      box.appendChild(p);
    }
    document.body.appendChild(box);
    setTimeout(function(){ if(box.parentNode) box.parentNode.removeChild(box); }, 2700);
  }catch(e){}
}
'''


def sem_comentario(s):
    u"""⚠️ A ORDEM É O DEFEITO. Tirando `//...` ANTES das aspas, um `"http://"`
    no meio do código apaga o resto da linha — e, se a aspa de fechar for junto,
    o estrago desce em cascata pelo arquivo. Foi assim que este mesmo portão
    acusou 24 funções de "não existir" estando todas declaradas: bloco →
    aspas → linha."""
    s = re.sub(r"/\*.*?\*/", " ", s, flags=re.S)
    s = re.sub(r'"(?:[^"\\\n]|\\.)*"', ' "" ', s)
    s = re.sub(r"'(?:[^'\\\n]|\\.)*'", " '' ", s)
    return re.sub(r"(?m)//.*$", " ", s)



# ============================================================
#  ⭐⭐ FECHAR A PORTA DA COLISÃO DE NOMES (ago/2026)
#
#  ⚠️ A FAMÍLIA DE DEFEITOS QUE CUSTOU UMA NOITE INTEIRA, e que o Marcos pegou
#  jogando, um a um: as duas vozes falando juntas, o botão CONTINUAR que sumiu,
#  o alto-falante apagado das respostas e — o pior de ver — o cartão da resposta
#  com 82px cravados, quadrado branco e o nome pendurado para fora.
#
#  A causa era SEMPRE a mesma: **a peça e o motor usam o mesmo nome para coisas
#  diferentes.** O `.fig` da peça é a opção de resposta; o `.fig` do motor é a
#  figurinha do crachá (82x82, quadrada). No mesmo documento, o crachá do Broto
#  caía em cima da resposta. Medido: **67 das 76 peças** definem pelo menos uma
#  classe com nome que o motor também usa — 40 nomes em disputa.
#
#  O prefixo do CSS (`.mec-<nome> .fig`) NÃO resolvia: ele evita que duas PEÇAS
#  briguem entre si, mas a regra do MOTOR (`.fig{...}`) continua valendo por
#  baixo, e o que a peça não declara vem de lá.
#
#  Aqui a porta se fecha de verdade: a classe em disputa é RENOMEADA — no CSS e
#  no JavaScript, no mesmo passo. `.fig` da peça `ouvir-achar` vira `.oa1_fig`.
#  Nenhuma peça pode mais colidir com o motor nem com outra peça, e isso é
#  VERIFICÁVEL, não uma promessa de cuidado.
#
#  ⚠️ O que NÃO se renomeia: o vocabulário que a peça compartilha DE PROPÓSITO
#  para herdar o visual da casa (`balao`, `selo`, `opt`, `hint`, `tela`...).
#  Renomear isso quebraria o "jeito do Broto" que a ponte aplica.
# ============================================================
VOCABULARIO_COMUM = set("""balao selo opt opts hint tela centro prog dica btn
    banner medal pecabox progpeca show ok no sel usada cheia agora acesa pulsa
    feito certo errado tembalaopeca mec
    zap fone tocando
    pc cam lig par pchip peca qcpc qcvaga mcarta
    csb fichaq""".split())
# ⚠️⚠️ A SEGUNDA LICAO DO `zap`, e ela e MAIOR: o vocabulario dos AUDITORES
#    tambem e contrato. O integrador renomeou `.pc` para `.o_pc` na peca de
#    ordenar — renomeacao correta, sem colisao nenhuma — e com isso o
#    auditor-jogador, que procura `.pc` para saber o que arrastar, achou ZERO
#    pecas e deu "PRESO em EM ORDEM". A tela estava PERFEITA: as prateleiras
#    1o..5o, as letras D B A E C, tudo desenhado e clicavel. Quem ficou cego
#    foi o auditor.
#    Custo real: a banca reprovou uma atividade correta, e eu quase fui
#    "consertar" uma fase que nao tinha defeito.
#    Regra: classe pela qual um portao PEGA a atividade nao se renomeia. As
#    daqui saem de `grep` no _qa/jogador.js e no _qa/errador.js — quando um
#    auditor novo passar a depender de uma classe, ela entra nesta lista NO
#    MESMO COMMIT.
# ⚠️ `zap` entrou nesta lista DEPOIS de eu quebrar a atividade com ele: o
#    alto-falante e do MOTOR (ele cria, estiliza e gerencia pelo `poeZap`). Ao
#    renomear para `oa_zap`, a peca ficou com um botao que o motor nao reconhece
#    e o CSS nao pinta — e as 4 respostas voltaram a ficar SEM SOM, que e o
#    defeito que mais dooi no 1o ano. Renomear e bom; renomear o que e do motor
#    de proposito e tiro no pe.


def classes_do_motor():
    motor = os.path.join(AQUI, "motor.html")
    if not os.path.exists(motor):
        return set()
    mcss = "".join(re.findall(r"<style>(.*?)</style>",
                              io.open(motor, encoding="utf-8").read(), re.S))
    fora = set()
    for _m, sel, _c in regras(mcss):
        fora.update(re.findall(r"\.([\w-]+)", sel))
    return fora


def sigla(nome, usadas):
    u"""uma sigla curta e única por peça: `ouvir-achar` -> `oa`, e se já existir,
    `oa2`. Curta de propósito: ela entra em todo nome de classe do arquivo."""
    base = "".join(x[0] for x in re.split(r"[-_]", nome) if x)[:3] or "p"
    s, n = base, 1
    while s in usadas:
        n += 1
        s = "%s%d" % (base, n)
    usadas.add(s)
    return s


def renomeia_classes(css, js, nome, sg, do_motor):
    u"""renomeia, no CSS e no JS, toda classe que a peça define e que o motor
    também usa. Devolve (css, js, lista_do_que_mudou)."""
    delas = set()
    for _m, sel, _c in regras(css):
        delas.update(re.findall(r"\.([\w-]+)", sel))
    trocar = sorted((delas & do_motor) - VOCABULARIO_COMUM)
    if not trocar:
        return css, js, []
    mapa = dict((c, "%s_%s" % (sg, c)) for c in trocar)
    for velho, novo in mapa.items():
        # CSS: só em SELETOR (`.velho`), nunca dentro do corpo da regra
        css = re.sub(r"\.%s\b" % re.escape(velho), "." + novo, css)
        # JS: a classe viaja dentro de TEXTO — `el("div","velho")`,
        # `className="a velho b"`, `getElementsByClassName("velho")`,
        # `indexOf("velho")`, `querySelector(".velho")`. Troco a PALAVRA inteira
        # dentro de literais de texto, que é onde nome de classe mora.
        def troca(m):
            asp, dentro = m.group(1), m.group(2)
            # ⚠️⚠️ LICAO PAGA (ago/2026) — A RENOMEACAO ENTROU NA PROSA.
            #    A peca `caca-palavras` diz a crianca: *"Leia cada pista, pense
            #    na palavra e ache ela na GRADE."* A peca tambem tem uma classe
            #    `.grade`, que colide com o motor e por isso e renomeada. O
            #    trocador mexia em QUALQUER literal de texto — entao a frase
            #    virou *"ache ela na cp_grade"*, e foi isso que a crianca do 6o
            #    ano leu na tela. Nao ha erro de JS, o layout fica perfeito, e
            #    o defeito so existe para quem esta LENDO.
            #    A regra: nome de classe mora em string de CLASSE, e string de
            #    classe nao tem pontuacao de frase, nem acento, nem tag. Se o
            #    literal inteiro nao for uma lista de classes (ou um seletor),
            #    ele e texto para gente — e texto para gente nao se renomeia.
            if not re.match(r"^[.#]?[\w\- ]+$", dentro):
                return m.group(0)
            if not re.search(r"(^|[\s.])%s($|[\s,.:\[])" % re.escape(velho), dentro):
                return m.group(0)
            return asp + re.sub(r"(^|[\s.])%s($|[\s,.:\[])" % re.escape(velho),
                                lambda x: x.group(1) + novo + x.group(2), dentro) + asp
        js = re.sub(r"([\"\'])((?:[^\"\'\\\n]|\\.)*)\1", troca, js)
    return css, js, trocar

def classes_que_vazam(css_out):
    u"""⚠️ A COLISAO DE CSS, que e a irma da colisao de nomes em JS.

    A peca usa os MESMOS nomes de classe do motor — e isso e proposital: e por
    isso que nenhuma peca precisou ser reescrita. O preco: quando o motor tem
    uma regra para a mesma classe, **o que a peca nao declara vem de la**. A
    regra da peca ganha por especificidade, mas so nas propriedades que ela
    escreve.

    Foi assim que o jogo da memoria empilhou: o `.mcartas` da peca fecha a
    conta com 48% + margem de 1%, e o `.mcartas` do MOTOR tem `gap:10px`. O gap
    entrou de carona, duas cartas passaram de 100%, e o tabuleiro virou uma
    coluna de 950px — quatro das oito cartas fora da tela de 640px da escola.
    Nenhum erro, nenhum aviso: so um jogo de memoria em que nao da para ver o
    tabuleiro.

    Aqui a lista sai em aviso, para eu olhar quando uma conta de largura nao
    fechar — em vez de passar duas horas medindo, como passei nesta."""
    motor = os.path.join(AQUI, "motor.html")
    if not os.path.exists(motor):
        return []
    mcss = "".join(re.findall(r"<style>(.*?)</style>",
                              io.open(motor, encoding="utf-8").read(), re.S))
    do_motor = set()
    for _m, sel, _c in regras(mcss):
        do_motor.update(re.findall(r"\.([\w-]+)", sel))
    das_pecas = set()
    for bloco in css_out:
        for _m, sel, _c in regras(bloco):
            das_pecas.update(re.findall(r"\.([\w-]+)", sel))
    return sorted((das_pecas & do_motor) - set(["mec-" + x for x in das_pecas]))


def confere_contra_motor(js_out):
    u"""⭐ O PORTÃO QUE FALTAVA — as duas metades da mesma lição.

    Metade 1 (**falta**): a peça chama um nome que o motor não tem. Foi o
    `nota()`: a memória morria no primeiro som de carta virando.

    Metade 2 (**colisão de tipo**): o motor TEM o nome, mas com outro tipo — o
    `ac` da peça é uma função (destrava o som) e o do motor é o objeto
    AudioContext. Esta é a pior das duas, porque declarar a função aqui não deu
    erro nenhum: o `var ac=` do motor simplesmente sobrescreveu, e a memória
    voltou a morrer, agora com "ac is not a function".

    As duas só apareciam JOGANDO. Agora aparecem ao integrar — antes de existir
    atividade, quanto mais criança."""
    motor = os.path.join(AQUI, "motor.html")
    if not os.path.exists(motor):
        return [], []
    mjs = sem_comentario("".join(re.findall(
        r"<script>(.*?)</script>",
        io.open(motor, encoding="utf-8").read(), re.S)))
    funcoes = set(re.findall(r"function\s+([\w$]+)", mjs))
    valores = set(re.findall(r"(?:^|[,;{]\s*|var\s+)([A-Za-z_$][\w$]*)\s*=(?!=)",
                             mjs, re.M)) - funcoes
    embutidos = set("""window document Math Date JSON String Number Array Object
        parseInt parseFloat setTimeout setInterval clearInterval clearTimeout
        isNaN navigator location Image RegExp Audio alert Boolean Error
        encodeURIComponent decodeURIComponent requestAnimationFrame
        SpeechSynthesisUtterance speechSynthesis Promise MutationObserver
        localStorage sessionStorage AudioContext webkitAudioContext""".split())
    kw = set("""if for while switch catch return typeof function new else do try
        in of delete void instanceof throw case break continue""".split())

    todo = sem_comentario("".join(js_out)) + sem_comentario(FERRAMENTAS)
    chamados = set(re.findall(r"(?<![\w.$])([a-zA-Z_$][\w$]*)\s*\(", todo))
    locais = (set(re.findall(r"function\s+([\w$]+)", todo))
              | set(re.findall(r"var\s+([\w$]+)", todo)))
    # ⚠️ os PARAMETROS também são nomes locais: `function montaBotoes(c,aoTocar)`
    #    chama `aoTocar(k)` lá dentro, e sem isto o portão acusa o inocente.
    for args in re.findall(r"function\s*[\w$]*\s*\(([^)]*)\)", todo):
        for a in args.split(","):
            a = a.strip()
            if a:
                locais.add(a)
    resta = chamados - locais - kw - embutidos
    faltando, colidindo = sorted(resta - funcoes - valores), sorted(resta & valores)

    # ⚠️ A TERCEIRA METADE DA MESMA LICAO: a peca pode declarar um nome que a
    #    PONTE usa para si. Foi o `fim` da memoria — o `mostraBanner` da ponte
    #    chamava a peca de volta em laco infinito, SEM ERRO NENHUM. O nome da
    #    continuacao (`_seguir`) mora fora do fechamento justamente para isto,
    #    mas se alguem declarar `_seguir` dentro de uma peca, volta tudo.
    for m in re.finditer(r"/\* ==== PECA: ([\w-]+) ==== \*/(.*?)(?=/\* ==== PECA: |$)",
                         "".join(js_out), re.S):
        corpo = sem_comentario(m.group(2))
        # so o corpo da peca (depois do `limpa();` que abre o fechamento)
        i = corpo.find("limpa();")
        corpo = corpo[i:] if i >= 0 else corpo
        for nome in ("_seguir", "cen", "fim"):
            if re.search(r"\b(?:var|function)\s+%s\b" % nome, corpo):
                if nome == "_seguir":
                    colidindo.append(u"%s declara `_seguir` (o nome da ponte)"
                                     % m.group(1))
    return faltando, colidindo


def main():
    escrever = "--escrever" in sys.argv
    prontas, sem_porta, sem_gaveta, sem_css = [], [], [], []
    gaveta_perdida = []   # TECNICA que é array/objeto mas escapou da detecção (bug do intruso)
    gavetas = {}
    _do_motor = classes_do_motor()
    _siglas = set()
    renomeadas = {}
    js_out, css_out = [], []
    kf_fonte = [0]   # quantas @keyframes as pecas declaram (ver o portao abaixo)

    for arq in sorted(os.listdir(PECAS)):
        if not arq.endswith(".html") or arq == "MOLDE.html":
            continue
        nome = arq[:-5]
        html = io.open(os.path.join(PECAS, arq), encoding="utf-8").read()
        js = js_da_peca(html)
        porta = entrada(js)
        if not porta:
            sem_porta.append(nome)
            continue
        gav, exemplo, regra, todas, exemplos, tecnicas = gaveta(js)
        # ⭐ GUARDA (Sólidos, ago/2026 — o bug do intruso): uma gaveta marcada
        #    `/*TECNICA*/` cujo valor é ARRAY/OBJETO É conteúdo e TEM que ser
        #    detectada (entrar em `todas`). Se escapar, a peça roda com o EXEMPLO
        #    dela dentro da atividade (frutas nos sólidos), sem erro de JS nenhum.
        #    Aqui o build GRITA — é a "regra em _qa" que faltava para o defeito
        #    não voltar por outra peça.
        for _t in tecnicas:
            if _t in todas:
                continue
            if re.search(r"^var\s+%s\s*=\s*(?:/\*[^*]*\*/\s*)?[\[{]" % re.escape(_t),
                         js, re.M):
                gaveta_perdida.append("%s:%s" % (nome, _t))
        # ⭐ AQUI a atividade deixa de ser código: a última linha da peça (a
        #    chamada dela mesma) vira "troque o conteúdo de exemplo pelo desta
        #    fase, DEPOIS comece". A peça não sabe de nada; nada nela mudou.
        # ⚠️⚠️ LICAO PAGA (ago/2026), e a mais grave que a fabrica ja teve: a
        #    peca fecha em `fimDaPeca()`, que e a tela de BANCADA dela — "PECA
        #    FECHADA", a medalha da peca e um botao "Jogar de novo". Dentro da
        #    atividade montada isso e um BECO: a crianca termina a fase 3 de 32,
        #    cai numa tela que diz "esta e a peca O INTRUSO" e o unico caminho e
        #    recomecar a MESMA fase. Para sempre.
        #    A ponte ja cuidava do caminho pelo `mostraBanner`, mas TRINTA das
        #    78 pecas chamam `fimDaPeca()` DIRETO — e essa chamada nao passava
        #    por lugar nenhum. Aqui a funcao e reapontada para a continuacao do
        #    motor logo antes de a peca comecar: quem chamar `fimDaPeca` a partir
        #    de agora esta, na verdade, indo para a fase seguinte.
        abre = ('    try{ fimDaPeca = _seguir; }catch(_e){}\n'
                "    " + porta + "();")
        if gav:
            linhas = ["    if(f && f.dados) %s = f.dados;" % gav]
            outras = [v for v in todas if v != gav]
            # ⚠️ LICAO PAGA (ago/2026, SOIMG do escolher): a injecao so percorria
            #    as GAVETAS de conteudo (arrays/strings). Uma TECNICA booleana
            #    (`var SOIMG=false; /*TECNICA*/`) nunca entra em `todas`, entao
            #    NUNCA era injetada — o `dadosExtra:{SOIMG:true}` nao fazia nada
            #    (o `LETRAS` do digitar so escapou por ser string, logo em `todas`).
            #    As tecnicas sao, por definicao, o que o `dadosExtra` liga: injeta-las.
            extra = outras + [t for t in tecnicas if t != gav and t not in outras]
            if extra:
                # ⚠️ as OUTRAS gavetas desta peca: o `sete-erros` guarda a cena
                #    em CENA_A e os erros em MUDA. Sem isto, a fase saia com a
                #    cena da atividade e os erros do exemplo — sem erro nenhum.
                linhas.append("    if(f && f.dadosExtra){ var _d = f.dadosExtra;")
                for v in extra:
                    linhas.append("      if(_d.%s !== undefined) %s = _d.%s;" % (v, v, v))
                linhas.append("    }")
            abre = "\n".join(linhas) + "\n" + abre
        else:
            sem_gaveta.append(nome)
        corpo = re.sub(r"^\s*%s\s*\(\s*\)\s*;\s*$" % re.escape(porta),
                       abre, js, flags=re.M)
        gavetas[nome] = {"var": gav,
                         # QUAL regra escolheu esta gaveta — para o escolhido
                         # poder ser CONFERIDO, em vez de acreditado
                         "regra": regra,
                         # TODAS as gavetas de conteudo desta peca: as que nao
                         # sao a principal se preenchem por `dadosExtra`
                         "gavetas": todas,
                         # as que a peca marcou com `/*TECNICA*/`: alfabeto,
                         # estado que nasce vazio, opcao com padrao legitimo.
                         # Ficar com o exemplo nelas e o CERTO — o montador nao
                         # avisa (ver a licao em `gaveta()`).
                         "tecnicas": tecnicas,
                         # o exemplo de CADA gaveta (o autor precisa do formato
                         # do `MUDA` tanto quanto o do `CENA_A`)
                         "exemplos": exemplos,
                         # o exemplo cru da peça: é o molde do que vai em `dados`
                         # ⚠️ LICAO PAGA: isto vinha cortado em 900 caracteres, e
                         #    em varias mecanicas o exemplo terminava no meio de
                         #    uma frase. Quem vai escrever o conteudo NAO consegue
                         #    ler a forma num exemplo pela metade — e era esse o
                         #    unico proposito do arquivo. Este JSON e ferramenta
                         #    de bancada, nao vai para o PC da escola: cabe
                         #    inteiro.
                         "exemplo": exemplo or ""}
        # ⭐ FECHA A PORTA: a classe que colide com o motor e RENOMEADA aqui,
        #    no CSS e no JS ao mesmo tempo, antes de a peca virar MEC[...].
        _css_bruto = css_da_peca(html)
        sg = sigla(nome, _siglas)
        _css_bruto, corpo, _trocadas = renomeia_classes(_css_bruto, corpo, nome, sg, _do_motor)
        if _trocadas:
            renomeadas[nome] = (sg, _trocadas)
        js_out.append(PONTE % {"nome": nome, "corpo": corpo})
        # o CSS leva a MESMA marca: o montador recorta peça inteira, nunca
        # regra a regra (um `@media{` que perdesse as regras de dentro deixaria
        # um `}` solto e derrubaria a folha inteira da atividade)
        propria = _css_bruto
        if len(propria.strip()) < 40:
            # peca que nao acrescenta estilo nenhum e suspeita: quase toda
            # mecanica tem pelo menos a classe da peca dela
            sem_css.append(nome)
        kf_fonte[0] += len(_KF_NOME.findall(propria))
        css_out.append((MARCA % nome) + u"\n" + prefixa_css(propria, nome))
        prontas.append(nome)

    faltando, colidindo = confere_contra_motor(js_out)
    vazam = classes_que_vazam(css_out)

    # ⭐ O PORTÃO QUE FALTAVA: a animação some e NADA reclama.
    # Foi assim que as `@keyframes` de 77 peças morreram caladas por semanas —
    # nenhum erro de JS, nenhum print diferente, só a tela mais morta. A conta
    # é boba de propósito: quantas animações as peças declaram, quantas
    # chegaram no arquivo final. Se some uma, o integrador GRITA.
    kf_saida = len(_KF_NOME.findall(u"\n".join(css_out)))

    print(u"INTEGRACAO DAS PECAS")
    if renomeadas:
        _n = sum(len(v[1]) for v in renomeadas.values())
        print(u"  🔒 %d classe(s) renomeada(s) em %d peca(s) — a porta da colisao "
              u"com o motor esta FECHADA" % (_n, len(renomeadas)))
    print(u"  %d peca(s) com porta de entrada -> viram MEC[...]" % len(prontas))
    if kf_fonte[0] != kf_saida:
        print(u"  \u26d4 %d ANIMACAO(OES) SUMIRAM na integracao (%d nas pecas, "
              u"%d no arquivo final). Animacao que some nao da erro nenhum: "
              u"a tela so fica morta. Ver `prefixa_css`."
              % (kf_fonte[0] - kf_saida, kf_fonte[0], kf_saida))
        return 1
    print(u"  %d animacao(oes) das pecas preservada(s) e renomeada(s) por peca"
          % kf_saida)

    # ⚠️⚠️ PORTAO DA PROSA RENOMEADA (ago/2026). A troca de classes mexia em
    #    QUALQUER literal de texto, e a crianca do 6o ano leu na tela *"ache ela
    #    na cp_grade"* — a peca `caca-palavras` tem uma classe `.grade` e a
    #    frase falava em "grade". Na `balanca` acontecia o mesmo com "prato".
    #    Nao ha erro de JS, o leiaute fica perfeito, e o defeito so existe para
    #    quem esta LENDO. Consertado no `troca()`; aqui fica a MEDIDA, porque
    #    conserto sem medida volta com outra cara.
    #    Como se reconhece: um pedaco `sigla_palavra` dentro de um literal que
    #    e FRASE (tem espaco e pontuacao de gente). Nome de classe nunca mora
    #    numa frase.
    # ⚠️⚠️ PORTAO DA GAVETA QUE SO ACEITA FUNCAO (ago/2026). O exemplo da peca
    #    `escrever-legenda` guardava a foto como REFERENCIA DE FUNCAO
    #    (`svg:svgPraca`). Funciona na bancada e e impossivel de vir do
    #    `conteudo.json` — JSON nao carrega funcao. A atividade do 6o ano
    #    preencheu tudo o que dava, o campo ficou vazio, e a fase estourou com
    #    `f.svg is not a function`: o jogador travou em 61% e a crianca ficaria
    #    presa ali. Nada antes disso reclamou, porque o `JSON.stringify` do
    #    exemplo simplesmente APAGA a chave de funcao — o montador nem chega a
    #    ver que ela existe. Quem enxerga e aqui, que le o texto cru.
    _so_funcao = []
    for _nome, _info in gavetas.items():
        _ex = _info.get("exemplo") or ""
        _js_peca = "\n".join(js_out)
        for _k, _v in re.findall(r"([A-Za-z_$][\w$]*)\s*:\s*([A-Za-z_$][\w$]*)\s*[,}]", _ex):
            if not re.search(r"function\s+%s\s*\(" % re.escape(_v), _js_peca):
                continue
            # ⚠️ APARADA: ter funcao no exemplo nao e o defeito — o defeito e
            #    CHAMAR sem guarda. Peca que faz `typeof x.svg==="function"` e
            #    aceita um `img` no lugar esta certa, e acusa-la ensinaria a
            #    ignorar o portao (a mesma licao do `beco_peca`).
            if re.search(r'typeof\s+[\w.$]*\.%s\s*===?\s*"function"' % re.escape(_k),
                         _js_peca):
                continue
            _so_funcao.append((_nome, _k, _v))
    if _so_funcao:
        print(u"  \u26d4 %d GAVETA(S) QUE SO ACEITAM FUNCAO — o conteudo.json nao "
              u"consegue preencher, e a fase estoura na mao da crianca:"
              % len(set(_so_funcao)))
        for _n, _k, _v in sorted(set(_so_funcao))[:8]:
            print(u"     %s: `%s: %s` (funcao). A peca precisa aceitar tambem um "
                  u"NOME de arte (`img`) e so chamar a funcao se ela existir."
                  % (_n, _k, _v))
        return 1

    # ⚠️⚠️ PORTAO DO NOME QUE NAO VIAJA (ago/2026). O integrador leva para a
    #    atividade o SEGUNDO <script> da peca — o primeiro e o motorzinho da
    #    bancada, que o motor de verdade ja tem. Declarei o `figEl` no primeiro
    #    e ele nao viajou: na bancada a peca passava (la o arquivo inteiro
    #    roda), e DENTRO da atividade a fase estourava com "figEl is not
    #    defined", com a crianca presa na fase. Aconteceu em QUATRO pecas de
    #    uma vez, e nenhum portao viu — porque cada um olhava um arquivo
    #    inteiro, e o defeito mora no RECORTE entre os dois.
    #    Aqui e barato: o que o bloco USA tem que estar declarado no bloco.
    _orfaos = []
    _todo = "\n".join(js_out)
    for _m in re.finditer(r'MEC\["([a-z0-9\-]+)"\] = function', _todo):
        _n = _m.group(1)
        _i = _m.start()
        _j = _todo.find('\nMEC["', _i + 10)
        _bloco = _todo[_i:_j if _j > 0 else len(_todo)]
        for _var in ("figEl",):
            if (_var + "(") in _bloco and not re.search(r"var\s+%s\s*=" % _var, _bloco):
                _orfaos.append((_n, _var))
    if _orfaos:
        print(u"  \u26d4 %d PECA(S) USAM UM NOME QUE FICOU NO <script> QUE NAO VIAJA:"
              % len(_orfaos))
        for _n, _v in _orfaos:
            print(u"     %s usa `%s` e nao o declara. Na bancada passa (o arquivo "
                  u"inteiro roda); na atividade estoura." % (_n, _v))
        print(u"     Tudo o que a MECANICA usa mora no SEGUNDO <script>.")
        return 1

    _prosa = []
    for _m in re.finditer(r'"((?:[^"\\\n]|\\.){14,})"', "\n".join(js_out)):
        _t = _m.group(1)
        if " " not in _t or not re.search(r"[.!?,;]|&#", _t):
            continue
        for _s, _tr in renomeadas.values():
            for _c in _tr:
                if ("%s_%s" % (_s, _c)) in _t:
                    _prosa.append(_t[:70])
                    break
    if _prosa:
        print(u"  \u26d4 %d FRASE(S) COM NOME DE CLASSE RENOMEADO NO MEIO — e "
              u"isso a crianca LE na tela:" % len(_prosa))
        for _t in sorted(set(_prosa))[:8]:
            print(u"     \"%s\"" % _t)
        print(u"     A troca de classes so pode mexer em string de CLASSE. "
              u"Ver o `troca()` em `renomeia_classes`.")
        return 1
    if faltando:
        print(u"  ✗ AS PECAS CHAMAM %d NOME(S) QUE NAO EXISTEM NO MOTOR: %s"
              % (len(faltando), ", ".join(faltando)))
        print(u"    -> ponha em FERRAMENTAS (a peca nao se reescreve)")
    if colidindo:
        print(u"  ✗ COLISAO DE TIPO com o motor (%d): %s"
              % (len(colidindo), ", ".join(colidindo)))
        print(u"    -> o motor declara este nome como VALOR e a peca o chama "
              u"como FUNCAO (foi o caso do `ac`). Da um `ac()` local na PONTE.")
    if faltando or colidindo:
        return 1
    print(u"  %d com gaveta de conteudo (aceitam `dados` do conteudo.json)"
          % (len(prontas) - len(sem_gaveta)))
    if sem_porta:
        print(u"  %d sem porta (nao chamam a propria funcao no fim): %s"
              % (len(sem_porta), ", ".join(sem_porta)))
    if gaveta_perdida:
        print(u"  ❌ GAVETA TECNICA NAO DETECTADA (a peca vai rodar com o EXEMPLO"
              u" dela — foi o bug do intruso/frutas nos solidos): %s"
              % ", ".join(gaveta_perdida))
        print(u"     -> conteudo da atividade nao entra; conserte a deteccao em "
              u"`gaveta()` antes de publicar.")
    if vazam:
        print(u"  ⚠️ %d CLASSE(S) QUE O MOTOR TAMBEM ESTILIZA — o que a peca nao"
              u" declara vem de la: %s" % (len(vazam), ", ".join(vazam[:12])))
        print(u"    -> se a conta de largura da peca nao fechar, e por aqui "
              u"(foi o `gap:10px` do motor empilhando o jogo da memoria)")
    if sem_css:
        print(u"  ⚠️ %d SEM CSS PROPRIO — a mecanica vai entrar sem estilo: %s"
              % (len(sem_css), ", ".join(sem_css)))
    if sem_gaveta:
        print(u"  %d SEM GAVETA — vao rodar com o conteudo de EXEMPLO delas: %s"
              % (len(sem_gaveta), ", ".join(sem_gaveta)))
    if not escrever:
        print(u"  (--escrever para gerar pecas.js e pecas.css)")
        return 0

    # PORTÃO DO CSS VAZADO (ver a lição em `SELETOR_OK`): prosa que virou
    # seletor apaga a regra dela E a de baixo, sem erro nenhum. Não escrever.
    if SELETORES_TORTOS:
        print(u"  ⛔ CSS VAZADO — texto virou seletor (comentário sem abrir/fechar?):")
        for nome_p, trecho in SELETORES_TORTOS[:8]:
            print(u"     %s -> %s" % (nome_p, trecho))
        print(u"     conserte o comentario na peca; nada foi escrito.")
        return 1

    # o mapa das gavetas: é ele que o autor do conteudo.json consulta para saber
    # o formato de `dados` de cada mecânica (sem abrir 74 arquivos)
    io.open(os.path.join(AQUI, "pecas.json"), "w", encoding="utf-8").write(
        json.dumps({
            "_leia": u"O FORMATO DE `dados` DE CADA MECANICA. Ao escrever o "
                     u"conteudo.json, a fase pode trazer um campo `dados` com "
                     u"o conteudo dela; o formato e o mesmo do `exemplo` aqui, "
                     u"que e o proprio bloco de exemplo da peca. Sem `dados`, a "
                     u"fase roda com o exemplo — util para ver a mecanica "
                     u"funcionando, NUNCA para entregar ao Marcos.",
            "gavetas": gavetas}, ensure_ascii=False, indent=1, sort_keys=True))

    io.open(os.path.join(AQUI, "pecas.js"), "w", encoding="utf-8").write(
        u"/* GERADO por integrar.py — nao editar a mao */\n" + FERRAMENTAS
        + "".join(js_out))
    io.open(os.path.join(AQUI, "pecas.css"), "w", encoding="utf-8").write(
        u"/* GERADO por integrar.py — nao editar a mao */\n" + CSS_PONTE + "\n".join(css_out))
    print(u"  escrito: pecas.js (%d KB) e pecas.css (%d KB)"
          % (sum(len(x) for x in js_out) // 1024,
             sum(len(x) for x in css_out) // 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
