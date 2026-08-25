#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""O MONTADOR — conteúdo entra, atividade sai.

Meta do Marcos (ago/2026): *"precisamos otimizar o processo a ponto de conseguir
deixar uma atividade inteira com o esqueleto em minutos e não em horas — e claro
que fique profissional e fantástica"*.

O que fazia levar horas era eu **escrever o motor de novo** em cada atividade: o
caça-palavras, a memória, o arrastar, o teclado. É aí que iam as horas, e é de lá
que saíam os defeitos que chegavam nele.

Aqui a atividade deixa de ser código e passa a ser **conteúdo**:

    conteudo.json  ──▶  montar.py  ──▶  index.html   (a atividade)
                                        falas.json   (as vozes)
                                        arte.json    (o que falta desenhar)

⭐ O GANHO QUE NÃO É TEMPO: **o `falas.json` é gerado do próprio enunciado.**
   Fica impossível a voz dizer coisa diferente da tela — o defeito que ele cobrou
   três vezes num só dia deixa de existir por construção, não por eu lembrar de
   conferir.

⭐ E NÃO HÁ DE ONDE CLONAR. O motor é o mesmo para todas; o conteúdo é novo. A
   família inteira de "resto de clone" (a pré-carga da origem, o alto-falante da
   origem, os conceitos da origem) desaparece.

O MODELO É O JARDIM DO BROTO (ordem dele): capa → crachá → fases → boletim com
medalha → relatório do professor escondido. Ver `CONTRATO.md`.

Uso:
  python3 _padrao/ESQUELETO/montar.py <pasta>          # monta a atividade
  python3 _padrao/ESQUELETO/montar.py <pasta> --so-ver # só confere, não escreve
"""
import collections
import io
import json
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))

# as mecânicas que existem na oficina (a fonte da verdade é a pasta de peças)
def mecanicas():
    d = os.path.join(RAIZ, "_padrao", "pecas")
    if not os.path.isdir(d):
        return set()
    return set(f[:-5] for f in os.listdir(d)
               if f.endswith(".html") and f != "MOLDE.html")


def simples(s):
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def texto_limpo(h):
    u"""o que a criança OUVE é o que ela LÊ — sem marcação, sem entidade."""
    s = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), h or "")
    s = s.replace("&amp;", "&").replace("&nbsp;", " ")
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()


# ------------------------------------------------------------------ conferência
def confere(c, mecs):
    u"""O montador é o primeiro portão: erro de conteúdo não vira HTML."""
    p, avisos = [], []
    for campo in ("titulo", "ano", "mascote", "prefixo", "fases"):
        if not c.get(campo):
            p.append(u"falta o campo obrigatorio '%s'" % campo)
    if p:
        return p, avisos

    fases = c["fases"]
    n = len(fases)
    if n < 8:
        p.append(u"so %d fase(s): o combinado sao 32 (ou perto disso)" % n)

    ano = str(c.get("ano", "")).lower()
    pequeno = any(x in ano for x in ("pre", "pré", "1", "2"))
    # ⭐ NOVO PADRAO DA CASA (decisao do Marcos, ago/2026): *"eu quero so 6 ou 7
    #    mecanicas com 6 fases cada... as atividades serao assim de agora em
    #    diante para ser mais rapido"*. A regra antiga (10 p/ pequeno, 16 p/
    #    maior) vinha da queixa contra repeticao, mas o Marcos decidiu trocar
    #    VARIEDADE-por-QUANTIDADE por VELOCIDADE-de-producao: menos mecanicas,
    #    cada uma com mais fases (a dificuldade sobe DENTRO da mecanica). O teto
    #    de 40%/gesto, o "nada de gesto colado" e o minimo de 4 gestos do
    #    `_qa/padrao.py` continuam protegendo a variedade — com 6 mecanicas x 6
    #    fases cada uma fica em ~17%, bem abaixo do teto. Piso agora: 6.
    minimo = 6
    # ⭐ ATIVIDADE CRIATIVA (colorir/ateliê): gênero de PRODUÇÃO, não de treino.
    #    A peça pintar-canvas não tem certo nem errado — a criança CRIA. Um livro
    #    de colorir é legitimamente mono-mecânica (10 páginas de pintar), e as
    #    regras de VARIEDADE (mínimo de gestos, teto 40%, nada colado) e o
    #    AQUECIMENTO são para atividades de treino, não para criação. Declarar
    #    `"tipo":"criativa"` no conteudo isenta SÓ essas regras — todo o resto
    #    (ids, voz, currículo, campos das peças) continua valendo. (Marcos,
    #    ago/2026: atividade de colorir do Pré.)
    criativa = str(c.get("tipo", "")).strip().lower() in ("criativa", "livre", "colorir")

    # ⚠️⚠️ LICAO PAGA (ago/2026) — ID REPETIDO, e o defeito e MUDO.
    #    Ao trocar 6 fases da Padaria eu escrevi os `id` novos de cabeça
    #    (`f03`, `f09`, `f18`, `f19`) sem conferir se ja existiam. Existiam. E
    #    o `id` e a CHAVE DA VOZ: `pd_f03_dica`. Duas fases com o mesmo id
    #    disputam o mesmo mp3 — a que grava por ultimo ganha, e a outra passa a
    #    FALAR A DICA DA VIZINHA. Nada quebra: o arquivo existe, o audio toca,
    #    e a crianca ouve uma dica que nao tem nada a ver com a tela dela.
    #    Quem pegou foi o portao 0j (voz da dica), depois de gravar 83 vozes —
    #    ou seja, tarde e caro. Aqui e barato: o montador ve antes de gerar.
    ids = [f.get("id") for f in fases if f.get("id")]
    for k, q in sorted(collections.Counter(ids).items()):
        if q > 1:
            onde = [str(i + 1) for i, f in enumerate(fases) if f.get("id") == k]
            p.append(u"o id '%s' esta em %d fases (%s). O id e a CHAVE DA VOZ "
                     u"(`<pre>_%s_dica`): repetido, uma fase fala a dica da outra."
                     % (k, q, ", ".join(onde), k))

    vistos, ordem = {}, []
    for i, f in enumerate(fases):
        onde = u"fase %d (%s)" % (i + 1, f.get("id") or "sem id")
        for campo in ("id", "mec", "selo", "enunciado"):
            if not f.get(campo):
                p.append(u"%s: falta '%s'" % (onde, campo))
        m = f.get("mec")
        if m and mecs and m not in mecs:
            p.append(u"%s: a mecanica '%s' nao existe na oficina "
                     u"(_padrao/pecas/). Escreva a peca dela antes." % (onde, m))
        if m:
            vistos[m] = vistos.get(m, 0) + 1
            ordem.append(m)
        if not f.get("dica"):
            avisos.append(u"%s: sem dica — o 1o degrau do andaime fica vazio" % onde)
        if not f.get("conceito"):
            avisos.append(u"%s: sem conceito — esta fase nao entra no parecer "
                          u"do professor" % onde)

    # ⭐⭐ O CRIVO DO CURRICULO E DA MESA (ordem do Marcos, ago/2026).
    #    "é preciso averiguar o currículo de Blumenau e passar pelo crivo do
    #    pedagogo especialista". Isso estava nos manuais e o esqueleto nao
    #    cobrava — entao dependia de eu lembrar, e ja se viu no que da.
    #    Agora: sem a habilidade do curriculo escrita, nao vira HTML.
    if not c.get("mesa") or u"«" in str(c.get("mesa", "")):
        p.append(u"falta dizer QUEM SENTOU NA MESA (campo 'mesa'): ate o 5o ano "
                 u"manda o PEDAGOGO; do 6o ao 9o, o ESPECIALISTA DA DISCIPLINA "
                 u"(ver _padrao/RECEITA.md)")
    # ⭐⭐ A VOZ SEGUE O MASCOTE (cobranca do Marcos, ago/2026: *"o mascote sera
    #    feminino? melhor tracar para masculino pois sera a voz do Antonio
    #    lembra? quando for feminino tem que pegar voz feminina"*).
    #    O `entregar.yml` tinha `pt-BR-AntonioNeural` FIXO no codigo: toda
    #    atividade, sempre, voz masculina. Com um mascote feminino a crianca ve
    #    uma personagem e ouve outra — e isso nenhum portao pegava porque o
    #    audio "existe" e o texto "bate". Agora a atividade DECLARA, e sem a
    #    declaracao nao vira HTML.
    voz = str(c.get("voz", "")).strip().lower()
    if voz not in ("masculina", "feminina"):
        p.append(u"falta dizer a VOZ do mascote (campo 'voz': \"masculina\" ou "
                 u"\"feminina\"). Mascote feminino com voz masculina e a crianca "
                 u"vendo uma personagem e ouvindo outra.")

    # ⚠️ LICAO PAGA (Detetive, ago/2026): o campo `fundo` vai DIRETO no CSS do
    #    motor (`url(img/<fundo>)`), sem acrescentar extensao — ao contrario do
    #    `imgEl`, que poe `.png` sozinho. Com `fundo:"dp_fundo"` (sem extensao) o
    #    navegador buscava `img/dp_fundo` e o pano de fundo NAO carregava (a
    #    crianca via um quadradinho vazio); so o portao 1e pegava, tarde, depois
    #    de publicar. Agora o montador cobra a extensao aqui.
    fundo = c.get("fundo")
    if fundo and isinstance(fundo, str) and "." not in fundo:
        p.append(u"o campo 'fundo' precisa da EXTENSAO do arquivo (ex.: "
                 u"\"%s.png\"). Sem ela o motor busca 'img/%s' e o pano de fundo "
                 u"nao carrega." % (fundo, fundo))

    cur = c.get("curriculo") or {}
    usados = sorted(set(f.get("conceito") for f in fases if f.get("conceito")))
    for k in usados:
        hab = cur.get(k, "")
        if not hab or u"«" in hab:
            p.append(u"o objetivo '%s' nao diz que HABILIDADE do curriculo ele "
                     u"serve. Abra o _curriculo/blumenau.txt, ache a linha do "
                     u"ano/disciplina e copie — nao resuma de cabeca." % k)
        elif len(hab) < 25:
            avisos.append(u"a habilidade de '%s' esta curta demais (%d letras) — "
                          u"copiada do curriculo ou escrita de memoria?" % (k, len(hab)))

    # ⚠️ a regra que o Marcos pediu: variedade contada por GESTO
    #    (isenta em atividade criativa — ver flag `criativa` acima)
    if not criativa:
        if len(vistos) < minimo:
            p.append(u"so %d mecanica(s) diferente(s); o combinado para este ano sao "
                     u"%d (ver CONTRATO.md)" % (len(vistos), minimo))
        for m, q in sorted(vistos.items()):
            if n and q / float(n) > 0.40:
                p.append(u"a mecanica '%s' ocupa %d%% das fases (teto: 40%%)"
                         % (m, round(100.0 * q / n)))
        # ⭐ REGRA VIRADA (Marcos, ago/2026): "as repeticoes das interatividades
        #    tem que ser SEGUIDAS e nao ESPACADAS — as criancas me dizem 'mas
        #    professor isso eu ja fiz, to fazendo de novo'". ANTES este portao
        #    cobrava o CONTRARIO: mecanica igual colada era erro e tinha que
        #    espacar. O espacamento e JUSTAMENTE o que faz a crianca sentir que
        #    voltou. Agora: cada mecanica que se repete tem que aparecer em
        #    BLOCO (fases seguidas, subindo um degrau a cada vez). Reaparecer
        #    depois de outra mecanica no meio = o "ja fiz isso". EXCECAO unica: o
        #    AQUECIMENTO — revisao proposital e ANUNCIADA como tal, pode reusar
        #    uma mecanica anterior fora do bloco (por isso sai da contagem aqui).
        def _e_aquecimento(f):
            alvo = (f.get("id", "") + f.get("mec", "")).lower()
            return "quec" in alvo or "quec" in texto_limpo(f.get("selo", "")).lower()
        posicoes = {}
        for i, f in enumerate(fases):
            if _e_aquecimento(f):
                continue
            m = f.get("mec")
            if m:
                posicoes.setdefault(m, []).append(i)
        for m, idxs in sorted(posicoes.items()):
            if len(idxs) >= 2 and (max(idxs) - min(idxs) + 1) != len(idxs):
                p.append(u"a mecanica '%s' aparece ESPACADA (fases %s) — as "
                         u"repeticoes tem que vir SEGUIDAS, em bloco, subindo um "
                         u"degrau a cada vez. Espacada, a crianca sente que esta "
                         u"'fazendo de novo'. Junte-as." %
                         (m, ", ".join(str(j + 1) for j in idxs)))
        # aquecimento no meio
        aq = next((i for i, f in enumerate(fases)
                   if "quec" in (f.get("id", "") + f.get("mec", "")).lower()
                   or "quec" in texto_limpo(f.get("selo", "")).lower()), None)
        if aq is None:
            avisos.append(u"nao ha AQUECIMENTO (a revisao no meio da aula) — e ela "
                          u"que faz o aprendido ficar")
        else:
            pos = (aq + 1) / float(n)
            if pos < 0.25 or pos > 0.65:
                p.append(u"o AQUECIMENTO esta em %d%% do caminho; ele vai no MEIO "
                         u"(entre 25%% e 65%%)" % round(pos * 100))
    return p, avisos


# ------------------------------------------------------------ o formato do dado
# ⚠️ MAPA DE DADOS (Lojinha bingo, ago/2026): campo cujo VALOR e um dicionario
#    valor->coisa (ex.: `imgs:{5:"lb_nota5", 10:"lb_nota10"}` no bingo do
#    dinheiro). As CHAVES de dentro (5, 10, 50...) sao DADOS escolhidos pela
#    atividade, NAO campos que a peca le. Sem isto o validador recursava e
#    acusava "campo que a peca NAO le: 5, 10, 50..." e ABORTAVA a montagem.
MAPA_DE_DADOS = {"imgs"}

def chaves_de(v, fundo=None):
    u"""todos os nomes de campo que aparecem dentro de uma estrutura."""
    fundo = set() if fundo is None else fundo
    if isinstance(v, dict):
        for k, x in v.items():
            fundo.add(k)
            if k in MAPA_DE_DADOS:
                continue          # a chave conta como campo; as de DENTRO sao dados
            chaves_de(x, fundo)
    elif isinstance(v, list):
        for x in v:
            chaves_de(x, fundo)
    return fundo



def eh_catalogo(v):
    u"""⚠️ GAVETA-CATÁLOGO: um dicionário cujas CHAVES são nomes escolhidos por
    quem escreve o conteúdo (`{pd_pao:{...}, B:{...}}`), e não campos que a peça
    lê. Comparar essas chaves com as do exemplo NUNCA vai bater — a peça de
    exemplo tem `sol`, `casa`, `lua`, e a atividade nova tem os nomes DELA.

    Sem esta distinção o montador acusava 29 "campos que a peça não lê" numa
    gaveta perfeitamente correta. Portão que acusa o inocente ensina a ignorar
    portão — e aqui ele chegou a IMPEDIR a montagem."""
    return (isinstance(v, dict) and v and
            all(isinstance(x, dict) for x in v.values()))


def chaves_uteis(v):
    u"""os campos que importam: num catálogo, os de DENTRO de cada item."""
    if eh_catalogo(v):
        fundo = set()
        for x in v.values():
            chaves_de(x, fundo)
        return fundo
    return chaves_de(v)

def literal(crua):
    u"""le um literal JS (o exemplo da peca) e devolve o valor, ou None."""
    if not crua:
        return None
    try:
        import subprocess
        r = subprocess.run(["node", "-e",
                            "console.log(JSON.stringify((%s)))" % crua],
                           capture_output=True, text=True, timeout=15)
        return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None
    except Exception:
        return None


def campos_no_texto(exemplo):
    u"""os campos do PRIMEIRO objeto do exemplo, lidos no TEXTO CRU.

    ⚠️⚠️ LICAO PAGA (ago/2026), e ela deixou SETE mecanicas passando sem
    conferencia nenhuma. O `literal()` manda o exemplo para o `node`; quando o
    exemplo cita um desenho por NOME (`svg:SVG_JANELA_SOL`, `arte:svgPonte`) o
    node estoura com "is not defined", o `literal()` devolve `None` — e o
    montador simplesmente PULAVA aquela mecanica, calado.

    Foi assim que duas fases chegaram ao jogador quebradas na mesma noite: a
    `autoexplicacao` sem o campo `esc` (as escolhas!) e a `escrever-legenda`
    sem a foto. Nenhum erro na montagem, nenhum aviso: a fase morria com a
    crianca na frente. **Portao que pula calado e pior que portao que falta**,
    porque ele parece ter olhado.

    Aqui a leitura e boba de proposito: acha o primeiro `{`, anda pelo mesmo
    nivel e anota `chave:` e se o valor abre `[` ou `{` (campo ESTRUTURAL — a
    peca vai percorre-lo, entao a fase sem ele nasce vazia).
    Devolve {chave: True se estrutural}."""
    if not exemplo:
        return {}
    # ⚠️ LICAO PAGA (ago/2026, prova de montagem das 81): esta leitura boba lia
    #    o exemplo CRU — COM comentario. O `simetria` tem
    #    `/* metade da esquerda: [linha, coluna] */`, e "esquerda:" seguido de
    #    "[" era detectado como CAMPO ESTRUTURAL obrigatorio. Resultado: o
    #    montador exigia `esquerda` (que a peca NUNCA le — ela le `modelo`) e o
    #    `simetria` ficava IMPOSSIVEL de montar. Portao que le prosa mede prosa:
    #    tira comentario /* */ e // ANTES de varrer.
    exemplo = re.sub(r"/\*.*?\*/", " ", exemplo, flags=re.S)
    exemplo = re.sub(r"//[^\n]*", " ", exemplo)
    i = exemplo.find("{")
    if i < 0:
        return {}
    prof, k, campos, chave = 0, i, {}, None
    while k < len(exemplo):
        ch = exemplo[k]
        if ch in "[{":
            prof += 1
            if prof == 2 and chave:
                campos[chave] = True
                chave = None
        elif ch in "]}":
            prof -= 1
            if prof == 0:
                break
        elif prof == 1:
            m = re.match(r"\s*([A-Za-z_$][\w$]*)\s*:", exemplo[k:])
            if m:
                chave = m.group(1)
                campos.setdefault(chave, False)
                k += m.end() - 1
        k += 1
    return campos


def confere_dados(c, oficina):
    u"""⭐ CONTEUDO NO FORMATO ERRADO NAO DA ERRO — DA FASE VAZIA.

    Escrevi, num teste, `MUDA` como `{i:1, como:"some"}` quando a peca do "ache
    o que mudou" espera `{sp:2, acao:"sumir"}`. Nao houve erro de JS, nao houve
    tela branca: a fase abriu, anunciou **"as duas cenas tem 0 diferencas"** e se
    deu por concluida sozinha. Uma fase inteira da aula virou fumaca, e nada no
    caminho reclamou.

    O `pecas.json` guarda o exemplo de cada mecanica, e o exemplo diz quais
    campos a peca LE. Entao da para conferir de graca: campo que a peca nao
    conhece e conteudo que ela vai ignorar."""
    cam = os.path.join(AQUI, "pecas.json")
    if not os.path.exists(cam):
        return [], []
    g = json.load(io.open(cam, encoding="utf-8")).get("gavetas") or {}
    ruins, avisos = [], []
    for i, f in enumerate(c["fases"]):
        mec = f.get("mec")
        info = g.get(mec)
        if not info or not f.get("dados"):
            continue
        # ⚠️ limite de LEITURA, nao so de grade: caca-palavras com palavra de
        #    12+ letras fica ilegivel na tela de 640px da escola, e a peca teria
        #    de abrir tanto a grade que a letra encolheria demais. Isto vem ANTES
        #    da conferencia de formato: a lista de palavras nao tem campo
        #    nomeado, entao aquela conferencia saia fora antes de chegar aqui.
        if mec == "caca-palavras" and isinstance(f["dados"], list):
            longas = [w for w in f["dados"]
                      if isinstance(w, str) and len(w) > 12]
            if longas:
                ruins.append(u"fase %d (%s): palavra(s) longa(s) demais para o "
                             u"caca-palavras (max 12 letras): %s"
                             % (i + 1, f.get("id"), ", ".join(longas)))

        # ⚠️⚠️ GAVETA QUE SO FUNCIONA COM A CHAVE DA OUTRA (ago/2026). Escrevi
        #    as cinco definicoes de genero em `PALDEF` — bula, edital, conto —
        #    e a fase abriu mostrando as PALAVRAS, como sempre. Nao havia erro:
        #    a peca so olha o `PALDEF` quando `MODO="definicoes"`, e o `MODO`
        #    ficou no padrao. Trabalho escrito, revisado, e invisivel para a
        #    crianca. Como `MODO` tem padrao legitimo, ele nao pode entrar na
        #    lista de avisos — o que pega o caso e a DEPENDENCIA, dita aqui.
        DEPENDE = {("caca-palavras", "PALDEF"): ("MODO", "definicoes")}
        de = f.get("dadosExtra") or {}
        for (m_, gav_), (chave, valor) in DEPENDE.items():
            if mec == m_ and gav_ in de and de.get(chave) != valor:
                ruins.append(u"fase %d (%s): voce preencheu '%s' mas '%s' nao "
                             u"esta em \"%s\" — a peca vai IGNORAR o que voce "
                             u"escreveu e a fase abre como se a gaveta estivesse "
                             u"vazia." % (i + 1, f.get("id"), gav_, chave, valor))

        # ⚠️ GAVETA MEIA-CHEIA DEIXA A FASE SEM SAIDA. O "separe nas gavetas" tem
        #    TRES: as gavetas (com as chaves), as fichas (que APONTAM para essas
        #    chaves) e as dicas. Preenchendo so as gavetas, as chaves deixam de
        #    casar e nenhuma ficha pode ser posta — a crianca fica presa, e nao ha
        #    erro de JS nenhum. Foi o auditor-jogador que pegou, travado em 22%.
        # ⚠️ AVISO QUE GRITA A TOA ENSINA A IGNORAR AVISO (ago/2026). Nem toda
        #    gaveta e CONTEUDO: `NUM` e a tabela dos nomes dos numeros, `FEITAS`
        #    e `GALERIA` sao ESTADO (nascem vazias e a peca preenche jogando),
        #    `TINTAS` e a paleta, `LETRAS`/`ALFA` sao o teclado, `FORCA_FIG` e
        #    `MODO` sao opcoes com padrao legitimo. Deixar essas no exemplo e o
        #    CERTO — e mesmo assim eu levava DEZ avisos numa montagem so, o que
        #    faz a gente passar o olho e perder o aviso que importava.
        # ⚠️ SEGUNDA LICAO, a que consertou de verdade: isto aqui era uma LISTA
        #    DE NOMES no montador, que so crescia DEPOIS de o defeito aparecer,
        #    e que nao sabia nada da peca. Agora quem declara e a PECA, com
        #    `/*TECNICA*/` na linha da `var` — o montador so le. A lista abaixo
        #    fica como rede para peca antiga que ainda nao tenha a marca.
        ESTADO = set("NUM FEITAS GALERIA TINTAS DIRS LIN COL ROT NOMEH NOMEM "
                     "CORES PALETA POSFRU POSJAN".split())
        ESTADO |= set(info.get("tecnicas") or [])

        # ⚠️ GAVETA DEPENDENTE FORA DE CONDICAO NAO E "MEIA-CHEIA" — E IRRELEVANTE
        #    (ago/2026). O `PALDEF` so vale com `MODO="definicoes"`; numa fase em
        #    modo "lista" ele nao deve nem estar preenchido. O guarda `DEPENDE`
        #    acima ja reprova PALDEF+MODO-errado; aqui, o lado espelho: quando a
        #    condicao NAO bate, a gaveta some da conta do "voce deixou X com o
        #    exemplo" — senao a atividade correta (sem PALDEF, modo lista) nascia
        #    avisada a toa, e aviso a toa ensina a ignorar aviso. Mesma regra do
        #    esboco.py (`DEPENDE`), para o esboco nao voltar reprovado por aqui.
        def _dep_ativa(v):
            dep = DEPENDE.get((mec, v))
            if not dep:
                return True
            chave, valor = dep
            return de.get(chave) == valor

        outras = [v for v in (info.get("gavetas") or [])
                  if v != info.get("var") and v not in ESTADO and _dep_ativa(v)]
        faltando = [v for v in outras if v not in (f.get("dadosExtra") or {})]
        if outras and faltando:
            avisos.append(u"fase %d (%s), mecanica '%s': voce preencheu '%s' mas "
                          u"deixou %s com o conteudo de EXEMPLO. Se uma gaveta "
                          u"aponta para a outra (chave/alvo), a fase fica SEM "
                          u"SAIDA e nada reclama — confira em pecas.json"
                          % (i + 1, f.get("id"), mec, info.get("var"),
                             " e ".join("'%s'" % v for v in faltando)))

        # ⚠️ LICAO PAGA (Museu, ago/2026, o Marcos: "nao deixa a abelha ir na
        #    gaveta dos invertebrados"). O gerador casava a ficha por uma tupla de
        #    tamanho errado -> TODAS as fichas nasciam com o MESMO `alvo` -> uma
        #    gaveta ficava vazia e o invertebrado nao entrava na dela. Nenhum erro
        #    de JS, o jogador-auditor ate "completa" (poe tudo na unica gaveta com
        #    ficha). So um humano percebe. Agora o montador REPROVA: numa
        #    classificacao com 2+ gavetas, as fichas TEM que usar 2+ alvos, e todo
        #    `alvo` precisa casar com uma gaveta existente.
        if mec == "classificar":
            fichas = (de.get("FICHAS") or []) if isinstance(de, dict) else []
            ks = [x.get("k") for x in (f.get("dados") or []) if isinstance(x, dict) and "k" in x]
            alvos = [x.get("alvo") for x in fichas if isinstance(x, dict) and x.get("alvo")]
            if len(ks) >= 2 and alvos:
                if len(set(alvos)) < 2:
                    ruins.append(u"fase %d (%s), classificar: TODAS as %d fichas "
                                 u"apontam para a MESMA gaveta ('%s') — as outras "
                                 u"ficam vazias e a crianca nao consegue guardar o "
                                 u"resto. Confira o 'alvo' de cada ficha."
                                 % (i + 1, f.get("id"), len(alvos), alvos[0]))
                orfaos = sorted(set(a for a in alvos if a not in ks))
                if orfaos:
                    ruins.append(u"fase %d (%s), classificar: ficha(s) com alvo %s "
                                 u"que nao e nenhuma gaveta (%s) — nunca encaixam."
                                 % (i + 1, f.get("id"),
                                    ", ".join("'%s'" % a for a in orfaos),
                                    ", ".join("'%s'" % k for k in ks)))

        # ⚠️ CAMPO ESTRUTURAL QUE FALTA = FASE VAZIA. O checador de formato so
        #    olhava campo A MAIS ("a peca nao le isto"). Campo A MENOS e pior:
        #    a peca percorre uma lista que nao existe e a fase morre na mao da
        #    crianca (aconteceu com `esc` na autoexplicacao e com a foto na
        #    escrever-legenda, as duas na mesma noite). Escalar que falta
        #    costuma ser opcional; ESTRUTURA que falta, nunca.
        _campos = campos_no_texto(info.get("exemplo"))
        _prim = f["dados"][0] if isinstance(f.get("dados"), list) and f["dados"] else None
        if isinstance(_prim, dict) and _campos:
            _falta = sorted(k for k, estrut in _campos.items()
                            if estrut and k not in _prim)
            # ⚠️ e o lado A MAIS, que ate hoje so era medido quando o `node`
            #    conseguia ler o exemplo. Na `forca` o conteudo dizia
            #    `palavra`/`pista` e a peca le `p`/`ac`/`d`: nomes totalmente
            #    diferentes, a peca lia `undefined.length` e a crianca ficava
            #    presa em 93% da atividade. Com a leitura no texto cru isto
            #    passa a ser medido nas 79 mecanicas, nao em 72.
            _sobra = sorted(k for k in _prim
                            if k not in _campos and k not in ("img", "voz"))
            if _sobra and len(_sobra) >= len(_prim) / 2.0:
                ruins.append(u"fase %d (%s), mecanica '%s': os campos %s nao "
                             u"existem no exemplo da peca (ela le: %s). Com nome "
                             u"trocado a peca nao acha nada e a fase trava."
                             % (i + 1, f.get("id"), mec,
                                ", ".join("'%s'" % x for x in _sobra),
                                ", ".join(sorted(_campos))))
            if _falta:
                ruins.append(u"fase %d (%s), mecanica '%s': falta(m) o(s) campo(s) "
                             u"%s, que a peca PERCORRE. Sem eles a fase abre vazia "
                             u"e a crianca fica sem saida (veja o exemplo em "
                             u"pecas.json)."
                             % (i + 1, f.get("id"), mec,
                                ", ".join("'%s'" % x for x in _falta)))

        exemplo = literal(info.get("exemplo"))
        if exemplo is None:
            continue
        conhecidas = chaves_uteis(exemplo)
        if not conhecidas:
            continue
        usadas = chaves_uteis(f["dados"])
        # ⚠️ LICAO PAGA (ago/2026, no RIGHT NOW): a memoria mostra a ARTE DE IA
        #    pelo campo `img` (o `imgEl` do motor); o `fig` do exemplo e so o
        #    desenho EMBUTIDO da peca. Como o exemplo usa `fig`, este check
        #    marcava `img` como "campo que a peca NAO le" e a fase saia sem foto
        #    (as cartas mostravam "undefined"). Mas `img`/`imgsen`/`voz`/`vozsen`
        #    sao universais: QUALQUER peca os le pelo motor, estejam ou nao no
        #    exemplo dela. O check gemeo de `dados` (linha ~385) ja isentava
        #    "img"/"voz"; este aqui nao — agora isenta os quatro.
        OPCIONAIS = {"img", "imgsen", "voz", "vozsen"}
        estranhas = sorted(usadas - conhecidas - OPCIONAIS)
        if estranhas:
            ruins.append(u"fase %d (%s), mecanica '%s': campo(s) que a peca NAO "
                         u"le: %s. Ela conhece: %s. (o conteudo seria ignorado e "
                         u"a fase sairia vazia, sem erro nenhum)"
                         % (i + 1, f.get("id"), mec, ", ".join(estranhas),
                            ", ".join(sorted(conhecidas))))
        # dadosExtra pode apontar para uma GAVETA (TITULO, FECHO...) OU para uma
        # TECNICA da peca (marcada com /*TECNICA*/, ex.: LETRAS do digitar, SOIMG
        # do escolher). As duas sao injetaveis pela ponte; so as duas sao validas.
        _extra_ok = list(info.get("gavetas") or []) + list(info.get("tecnicas") or [])
        for chave, val in (f.get("dadosExtra") or {}).items():
            if chave not in _extra_ok:
                ruins.append(u"fase %d: 'dadosExtra' fala de '%s', que nao e "
                             u"gaveta nem tecnica de '%s' (validas: %s)"
                             % (i + 1, chave, mec, ", ".join(_extra_ok)))
                continue
            crua = (info.get("exemplos") or {}).get(chave)
            mod = literal(crua)
            if mod is None:
                continue
            sabe = chaves_uteis(mod)
            estranhas = sorted(chaves_uteis(val) - sabe)
            if sabe and estranhas:
                ruins.append(u"fase %d, gaveta '%s' de '%s': campo(s) que a peca "
                             u"NAO le: %s. Ela conhece: %s"
                             % (i + 1, chave, mec, ", ".join(estranhas),
                                ", ".join(sorted(sabe))))
    return ruins, avisos


# ------------------------------------------------------------------ as vozes
_NOME_LETRA_PTBR = {
    u"A": u"Á",  u"B": u"Bê",  u"C": u"Cê",  u"D": u"Dê",  u"E": u"É",
    u"F": u"Éfe", u"G": u"Gê",  u"H": u"Agá", u"I": u"Í",   u"J": u"Jóta",
    u"K": u"Cá",  u"L": u"Éle", u"M": u"Ême", u"N": u"Ene", u"O": u"Ó",
    u"P": u"Pê",  u"Q": u"Quê", u"R": u"Érre", u"S": u"Ésse", u"T": u"Tê",
    u"U": u"Ú",   u"V": u"Vê",  u"W": u"Dáblio", u"X": u"Xis",
    u"Y": u"Ípsilon", u"Z": u"Zê",
}
def _nome_fonetico_letra(t):
    s = (t or "").strip()
    if len(s) == 1:
        return _NOME_LETRA_PTBR.get(s.upper())
    return None
def _fala_natural(t):
    s = (t or "").strip()
    if not s or " " in s or chr(10) in s:
        return None
    letras = [ch for ch in s if ch.isalpha()]
    if len(letras) >= 4 and s == s.upper() and any(
            ch.lower() in u"aeiouáéíóúâêôãõà" for ch in letras):
        return s.lower()
    return None


# ⚠️ LICAO PAGA (Marcos ouviu, ago/2026): *"na atividade onde fala face está
#    dizendo feice"*. A voz pt-BR do Edge le "face"/"faces" com sotaque ingles
#    ("feice"), porque e palavra que tambem existe em ingles. O conserto NAO
#    pode mudar a tela (a professora quer ler "face"/"faces" escrito certo) nem
#    a CHAVE da voz (o `id`/hash sai do texto da tela — e o que casa o MP3 com
#    o que a crianca ve). Por isso a troca vale SO para o TEXTO que vai ao TTS,
#    aplicada DEPOIS que o id ja foi calculado: o arquivo continua com o nome do
#    texto original, mas o AUDIO dele sai com a pronuncia certa ("fásse").
#    Palavra nova que a voz erra e so por AQUI (uma fonte de verdade), sempre em
#    minusculas foneticas — caixa alta empurra a voz a soletrar.
_FONETICA_VOZ = [
    (re.compile(r"\bfaces\b", re.I), u"fásses"),
    (re.compile(r"\bface\b",  re.I), u"fásse"),
]
_LACUNA = re.compile(r"_+")
def _fonetica_voz(t):
    u"""Reescreve foneticamente as palavras que a voz erra. Vale SO para o texto
    que vai ao TTS — nunca para a tela nem para a chave da voz."""
    for rx, sub in _FONETICA_VOZ:
        t = rx.sub(sub, t)
    # ⚠️ LICAO PAGA (Marcos ouviu, ago/2026): nas fases de COMPLETAR a lacuna e um
    #    "___" na frase ("Ana achou a pista. ___ sorriu."), e a voz pt-BR lia isso
    #    em voz alta como "underline"/"anderline" — repetido em toda rodada, feio.
    #    A lacuna e VISUAL (fica na TELA), mas no AUDIO ela vira so uma pausa. Como
    #    a chave/hash sai do texto da tela (com o "___"), o mp3 continua casando; so
    #    o que a voz DIZ muda. Uma pausa curta (reticencias) no lugar do traco.
    t = _LACUNA.sub(u"…", t)
    # ⚠️ NAO tirar a pontuacao depois da lacuna: a TELA mantem "___." (com ponto),
    #    entao a VOZ tambem tem de manter ("….") — senao o portao 0n ve a tela com
    #    ponto e a voz sem, e reprova uma fase certa (Detetive, ago/2026). So limpa
    #    espaco duplo. O `_` e o "…" saem da conta nos dois lados, no proprio portao.
    t = re.sub(r"\s+…", u" …", t)
    return t


def falas_de(c):
    u"""O falas.json sai do TEXTO DA TELA. É isto que torna impossível a voz
    dizer uma coisa e a tela outra."""
    pre = c["prefixo"].rstrip("_")
    out, vistos = [], set()

    def poe(ident, txt):
        t = texto_limpo(txt)
        if not t or ident in vistos:
            return
        vistos.add(ident)
        _tl = _nome_fonetico_letra(t)
        if _tl is None:
            _tl = _fala_natural(t)
        _base = _tl if _tl is not None else t
        reg = {"id": ident, "texto": _fonetica_voz(_base)}
        if _tl is None and _idioma(t) == "en":
            reg["lang"] = "en"     # a voz do workflow troca para ingles
        out.append(reg)

    poe(pre + "_abertura", c.get("abertura") or c.get("titulo"))
    for f in c["fases"]:
        i = f["id"]
        poe("%s_%s_intro" % (pre, i), f.get("enunciado"))
        if f.get("dica"):
            poe("%s_%s_dica" % (pre, i), f["dica"])
        if f.get("revela"):
            poe("%s_%s_revela" % (pre, i), f["revela"])
        # ⚠️ VOZ POR RODADA: se o enunciado muda dentro da fase, cada item tem a
        #    SUA voz. Sem isto, a crianca que nao le fica sem instrucao do 2o
        #    item em diante — foi o defeito achado no Jardim do Broto.
        for it in (f.get("itens") or []):
            if isinstance(it, dict) and it.get("pergunta"):
                poe("%s_%s_%s" % (pre, i, simples(it.get("k") or it.get("n") or "")),
                    it["pergunta"])
        # alto-falante de cada resposta tocavel
        for it in (f.get("itens") or []) + (f.get("opcoes") or []):
            nome = it.get("n") if isinstance(it, dict) else it
            if nome:
                poe("op_" + chave_voz(texto_limpo(nome)), nome)
        # ...e de TUDO o que a mecanica mostra a partir do `dados` dela
        if f.get("dados") is not None:
            falas_dos_dados(f["dados"], poe)
        # ⭐ COMPARAR: o painel fala a QUANTIDADE por extenso (ver `data-voz` em
        #    `fazPainel`). Os valores `a`/`b` sao INTEIROS, entao o
        #    `falas_dos_dados` (que so grava STRING) nunca os via, e o painel
        #    ficava mudo — foi este o ultimo bloqueio da Lojinha. Aqui mandamos
        #    gravar a palavra de cada valor, com a MESMA lista da peca.
        if f.get("mec") == "comparar":
            for it in (f.get("dados") or []):
                if not isinstance(it, dict):
                    continue
                for v in (it.get("a"), it.get("b")):
                    pal = _num_extenso(v)
                    if pal:
                        poe("op_" + chave_voz(pal), pal)
        # ⚠️ ...e do `dadosExtra` TAMBEM. Faltava, e nao era detalhe: o balao da
        #    mecanica `ordenar` mora em `dadosExtra.ORDTXT.balao`, entao as tres
        #    fases de por o alfabeto em ordem ficavam MUDAS — justo as do
        #    objetivo que a professora pediu primeiro.
        if f.get("dadosExtra") is not None:
            falas_dos_dados(f["dadosExtra"], poe)
    # ...e o BALAO QUE A PROPRIA PECA ESCREVE (ver `balaoes_das_pecas`)
    balaoes_das_pecas(c, poe)
    poe(pre + "_fim", c.get("fim") or u"Você conseguiu!")
    return out


# rende o HTML de um literal do jeito que o NAVEGADOR renderiza, porque e o
# `textContent` que o motor le para procurar a gravacao.
def como_na_tela(h):
    t = re.sub(r"<[^>]+>", "", h or "")
    try:
        from html import unescape
    except ImportError:                                    # python 2
        from HTMLParser import HTMLParser
        unescape = HTMLParser().unescape
    t = unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def balaoes_das_pecas(c, poe):
    u"""⭐ O BALAO DA PECA TAMBEM E VOZ — foi ele que faltou.

    ⚠️ LICAO PAGA (ago/2026). O Marcos: *"não teve fala automática, visto que
    os pequinos precisam"*. Medi e as fases 2 e 3 estavam MUDAS. Nao era bug de
    audio: era o montador nunca ter mandado gravar aquilo.

    Como o motor narra a fase: ele LE o texto do balao que esta na tela e
    procura a gravacao DAQUELE texto (`temVoz`). Se nao acha, fica calado de
    proposito — porque falar outra coisa foi o defeito que o Marcos cobrou tres
    vezes. Acontece que 10 das 11 mecanicas escrevem o proprio balao DENTRO do
    codigo da peca (`el("div","balao","Junte os pedacos e forme a palavra...")`),
    e nao no `conteudo.json`. O `falas_dos_dados` desce o `dados` da fase e
    nunca via esses textos. Resultado: gravacao nenhuma, e o motor calado — por
    decisao correta, a partir de um dado que faltava.

    Aqui o montador abre a PECA de cada mecanica usada e manda gravar o balao
    dela, renderizado como o navegador renderiza (tags fora, entidades
    decodificadas, espacos colapsados) — que e exatamente o que o `textContent`
    devolve e o que a conta do `chaveVoz` recebe.

    So entram balões COMPLETOS (terminam em . ! ou ? e tem 3+ palavras). Os
    pedacos de concatenacao ("Voce juntou <b>" + n + " palavras") sao a
    comemoracao do fim da fase: montam-se em tempo de execucao e nao ha texto
    fixo para gravar. Esses seguem com o som de festa, sem voz.
    """
    d = os.path.join(RAIZ, "_padrao", "pecas")
    for mec in sorted(set(f.get("mec") for f in c["fases"] if f.get("mec"))):
        cam = os.path.join(d, mec + ".html")
        if not os.path.exists(cam):
            continue
        src = io.open(cam, encoding="utf-8").read()
        lits = re.findall(r'"balao[^"]*"\s*,\s*"([^"]{6,160})"', src)
        lits += re.findall(r'balao[^\n]{0,40}?innerHTML\s*=\s*"([^"]{6,160})"', src)
        for bruto in lits:
            txt = como_na_tela(bruto)
            if len(txt.split()) < 3 or txt[-1:] not in u".!?":
                continue                      # pedaco de concatenacao, nao frase
            # mesma convencao das respostas tocaveis: `op_<chave>` -> op_<chave>.mp3
            poe("op_" + chave_voz(txt), txt)
        balao_por_item(src, c, mec, poe)


# `el("div","balao", "Pinte " + des.nome + " do jeito que voce quiser.")`
_CONCAT = (r'("(?:[^"\\]|\\.)*"(?:\s*\+\s*[A-Za-z_$][\w$]*\.[\w$]+\s*\+\s*'
           r'"(?:[^"\\]|\\.)*")+)')
# ⚠️ A DICA TAMBEM E MONTADA NO ATO — e ela e a que MENOS aparece jogando
#    (ago/2026). O andaime da `memoria` so fala no 3o erro do MESMO par:
#    `mostraDica("Vou abrir este par: <b>"+alvo.pal+"</b> &mdash; "+alvo.sen+".")`.
#    O colhedor joga ao acaso, entao cada partida descobre UMA dessas frases —
#    fechar a colheita assim levaria uma rodada por par, e "as vezes pega" nao
#    serve para a crianca que depende da voz. Como o texto sai do MESMO `dados`
#    da fase, da para gerar todos aqui, em tempo de montagem, sem adivinhar.
MOLDES = [
    re.compile(r'el\(\s*"div"\s*,\s*"balao[^"]*"\s*,\s*' + _CONCAT + r'\s*\)'),
    re.compile(r'mostraDica\(\s*' + _CONCAT + r'\s*\)'),
]
MOLDE_ITEM = MOLDES[0]


def balao_por_item(src, c, mec, poe):
    u"""⭐ O BALAO QUE MUDA A CADA ITEM tambem precisa de voz.

    ⚠️ LICAO PAGA (ago/2026). Depois de gravar os balões fixos, 31 das 32 fases
    narravam — e sobrou UMA muda: a de pintar. O balao dela nao e um texto
    fixo, e montado no ato:

        el("div","balao","Pinte "+des.nome+" do jeito que <b>voce</b> quiser.")

    O `des.nome` sai do `dados` da fase ("a placa", "o bolo"), entao o texto
    final so existe em tempo de jogo. O colhedor deveria pega-lo jogando, mas
    ele nao chega a essa tela em toda partida — e "as vezes pega" nao serve
    para a crianca do 1o ano que depende da voz.

    Aqui o montador faz o que da para fazer em tempo de montagem: le o molde da
    peca, ve qual CAMPO do item entra no meio ("nome"), e gera a frase pronta
    para CADA item do `dados` daquela fase. Nada de adivinhar: o texto sai do
    mesmo lugar de onde a peca vai tira-lo.
    """
    moldes = [m for mol in MOLDES for m in mol.finditer(src)]
    if not moldes:
        return
    for m in moldes:
        partes = re.split(r'\s*\+\s*', m.group(1))
        campos = [p.split(".", 1)[1] for p in partes if not p.startswith('"')]
        if not campos:
            continue
        for f in c["fases"]:
            if f.get("mec") != mec:
                continue
            itens = f.get("dados")
            if not isinstance(itens, list):
                continue
            for it in itens:
                if not isinstance(it, dict):
                    continue
                montado, i_campo = u"", 0
                for p in partes:
                    if p.startswith('"'):
                        montado += p[1:-1]
                    else:
                        v = it.get(campos[i_campo])
                        i_campo += 1
                        # campo que nao existe neste `dados`: a frase nao e desta
                        # peca/fase. Some em silencio — melhor nao gravar do que
                        # gravar "undefined".
                        if v is None:
                            montado = u""
                            break
                        montado += u"%s" % v
                txt = como_na_tela(montado)
                if len(txt.split()) >= 3:
                    poe("op_" + chave_voz(txt), txt)


# chaves cujo valor NAO e texto para a crianca (sao codigo: identificador,
# imagem, cor, coordenada). Sem esta lista, o montador mandaria gravar "p0".
#
# ⚠️ LICAO PAGA (ago/2026, na bater-silabas): a lista tinha `img` mas nao os
#    OUTROS nomes que a casa usa para apontar figura — `fig`, `foto`, `imagem`,
#    `cena`, `verso`. O proprio montador ja conhecia essa familia inteira 120
#    linhas abaixo (na hora de LISTAR as artes a gerar) e aqui so lembrava de
#    um. Resultado medido no `_padaria/falas.json`: o nome do arquivo `pd_bolo`
#    virou fala e foi para a fila de gravacao — um MP3 dizendo "pê-dê bolo".
#    Nao explodia nada, e por isso ninguem via: so gastava voz e engordava a
#    entrega. Uma lista que existe em dois lugares vira duas listas diferentes;
#    agora as duas saem da MESMA constante (ver CHAVES_DE_FIGURA).
#    ⚠️ E ELA CRESCEU DE NOVO (ago/2026), pelo mesmo motivo: a `raios-x` chama
#    as duas camadas de `cima` e `baixo`, e nenhuma das duas estava aqui. O
#    `rn_blur1` do 9o ano nunca entrou na lista de compras — o montador disse
#    "0 figura(s) a gerar" e a crianca abriu a fase com um quadradinho vazio.
#    Nome de campo que aponta figura tem que ENTRAR nesta lista no mesmo commit
#    em que a peca nasce; e o portao `_qa/imagens.js` e a rede embaixo.
CHAVES_DE_FIGURA = ("img", "fig", "foto", "imagem", "cena", "verso",
                    "cenaA", "cenaB", "cima", "baixo")
# ⚠️⚠️ LICAO PAGA (ago/2026) — A CHAVE DIZ SE E FALA; A PALAVRA NAO DIZ.
#    A banca achou alto-falantes MUDOS na fase 8 do 6o ano, em cima de
#    "contar", "bata" e "assine" — respostas que a crianca toca. O filtro
#    `eh_fala` barrava "palavra curta, minuscula e sem espaco" achando que era
#    identificador (`p0`, `gav1`). So que "bata" e "assine" sao a RESPOSTA, e
#    "raiz" — o coracao do Jardim do Broto — cai na mesma regra.
#    Palavra de gente e identificador de codigo tem a MESMA cara; o que os
#    separa e o LUGAR onde moram. Entao quem decide passa a ser a chave: se ela
#    esta nesta lista, o valor e referencia e nao se grava; se nao esta, e
#    texto que alguem vai ler — e entao alguem tem que ouvir.
#    `alvo` entrou aqui: e a chave da gaveta em "separe nas gavetas".
CHAVES_MUDAS = set("""k id ic cor classe cls tipo mec r c x y w h lin col
    pLin pCol lado dir face src href fundo forma icone alvo chave grupo
    ref destino origem estado modo
    acao sp val esc
    fora MODO CORP LETRAS ALFA FORCA_FIG FORMAS LADO""".split()) \
    | set(CHAVES_DE_FIGURA)
# ⚠️ LICAO PAGA (Lojinha, ago/2026): o SETE-ERROS descreve as diferencas em
#    MUDA=[{sp,acao,val}] — `acao`("sumir"/"img"/"esc") e `val` sao CODIGO de
#    controle, nao fala. Sem estas chaves aqui o montador mandava gravar a voz
#    "sumir", "img", "esc". Campo de controle e mudo.


def eh_fala(txt):
    u"""isto e frase para a crianca ouvir, ou e codigo?"""
    t = (txt or "").strip()
    # ⭐⭐ A LETRA SOLTA E VOZ — e na alfabetizacao e A voz mais importante.
    #
    # ⚠️ LICAO PAGA (ago/2026). O Marcos: *"tem que falar o que está escrito"*.
    # Medi os alto-falantes da Padaria: 23 na atividade, e OITO deles em cima de
    # uma letra sozinha (M, B, P, D, C, G, Q, O) nao tocavam nada. A crianca do
    # 1o ano tocava o alto-falante da letra — o gesto exato que a atividade
    # ensina — e ouvia SILENCIO.
    #
    # A causa era esta funcao: ela exigia 3 caracteres e 2 letras para
    # considerar que um texto e fala. A regra nasceu certa (impedir que
    # identificadores como "p0" ou "gav1" virassem mp3), mas numa atividade de
    # ALFABETO ela barrava justamente o conteudo.
    #
    # Uma letra em CAIXA ALTA nunca e identificador de codigo — identificador e
    # minusculo. Entao "M" passa, "p0" continua barrado.
    if len(t) == 1:
        return t.isalpha() and t == t.upper()
    if len(t) < 3:
        # duas letras em caixa e SILABA ("PA", "TO") — o coracao da alfabetizacao.
        # ⚠️ LICAO PAGA (ago/2026, ingles 9o ano): "Is"/"Am" sao PALAVRAS que a
        #    crianca toca (o verbo be), mas nao sao caixa-alta -> ficavam mudas.
        #    Palavra de 2 letras com vogal e fala; token de codigo ("fn","px")
        #    nao tem vogal ou vem com numero (ja barrado pelo isalpha).
        return t.isalpha() and (t == t.upper()
                                or bool(re.search(r"[aeiou]", t.lower())))
    baixo = t.lower()
    for ruim in ("<svg", "xmlns", "data:", "url(", "http", "#fff", "rgba(",
                 "translate", "polygon", "viewbox"):
        if ruim in baixo:
            return False
    if t.startswith("#") or t.startswith("."):
        return False
    # ⚠️ LICAO PAGA (ago/2026, remontando a Padaria): CHAVE DE IMAGEM EM `opcoes`.
    #    Mecanica com CATALOGO (arrastar-lugar/classificar) guarda em `opcoes` as
    #    CHAVES do catalogo ("pd_pao", "pd_bolo"), nao o texto — o texto mora no
    #    catalogo. `opcoes` nao esta (e nao pode estar) em CHAVES_MUDAS, senao
    #    calaria as opcoes-frase da `escolher`. Entao a chave "pd_pao" chegava
    #    aqui e passava: tem vogal, e minuscula, parece palavra -> virava um MP3
    #    dizendo "pe-de pao". O `_qa/falas.py` ja rejeita esse formato
    #    `prefixo_nome` (linha 79); a origem do defeito e ESTE filtro nao conhecer
    #    a mesma regra. Palavra de gente nunca tem "_": e sempre referencia.
    if re.match(r"^[a-z]{2,4}_[a-z0-9_]+$", t):
        return False
    letras = sum(1 for ch in t if ch.isalpha())
    if letras < 2:
        return False
    # ⚠️ AQUI FICAVA a regra "sem espaco, minuscula e ate 6 letras = codigo".
    #    Ela barrava "bata", "assine", "contar" e "raiz" — respostas que a
    #    crianca TOCA e precisa ouvir. Quem separa referencia de fala e a CHAVE
    #    (ver `CHAVES_MUDAS`), nao o formato da palavra. O que sobra aqui e so
    #    o que nao pode ser fala em nenhum lugar: token sem vogal ou com
    #    numero colado ("p0", "gav1", "f03").
    if " " not in t and t == baixo:
        if re.search(r"\d", t):
            return False
        if not re.search(r"[aeiouáéíóúâêôãõà]", t):
            return False
    return True


def falas_dos_dados(dados, poe):
    u"""⭐ O ALTO-FALANTE DE TUDO O QUE A PECA MOSTRA.

    O motor ja tem um observador que, a cada mudanca na tela, poe o botaozinho
    de voz em toda resposta cujo TEXTO esteja no `VOZOK` (a conta e o sha do
    proprio texto). So que o `VOZOK` nascia VAZIO nas atividades montadas: as
    respostas moram dentro do `dados` da fase, e ninguem tinha mandado gravar.

    Resultado medido pela banca: *"a atividade tem respostas para a crianca
    TOCAR, mas o VOZOK esta VAZIO — quem ainda nao le escolhe pelo desenho, e a
    atividade vira loteria"*. E o Marcos ja tinha cobrado isso com todas as
    letras: *"o alto-falante nas respostas tambem, para ajudar os alunos que
    nao sabem ler"*.

    Aqui o montador desce o `dados` inteiro e manda gravar CADA frase que a
    crianca ve — pergunta de rodada, resposta, dica, pista. Nada por mecanica:
    vale para as 74 de uma vez, hoje e nas que vierem."""
    if isinstance(dados, dict):
        for chave, val in dados.items():
            if chave in CHAVES_MUDAS:
                # ⚠️ LICAO PAGA (ago/2026, ingles 9o ano): `c` e COLUNA (int) na
                #    cruzadinha/coord — muda de proposito. MAS na `escolher` `c` e
                #    a RESPOSTA CERTA (str), a unica opcao que a crianca toca e
                #    ficava SEM alto-falante (as erradas, em `e`, tinham voz; a
                #    certa nao). Quando `c` (ou `r`) vem como frase, e fala.
                if chave in ("c", "r") and isinstance(val, str) \
                        and eh_fala(texto_limpo(val)):
                    poe("op_" + chave_voz(texto_limpo(val)), val)
                continue
            falas_dos_dados(val, poe)
    elif isinstance(dados, list):
        for x in dados:
            falas_dos_dados(x, poe)
    elif isinstance(dados, str):
        t = texto_limpo(dados)
        if eh_fala(t):
            poe("op_" + chave_voz(t), t)


# ⭐⭐ VOZ BILINGUE (ago/2026, atividade de INGLES do 9o ano). Ordem do Marcos:
#    *"voz inglesa no ingles"*. As frases em ingles ("She is cooking", "Are they
#    playing?") tem que SOAR em ingles; as instrucoes seguem em portugues. O
#    workflow de voz troca para uma voz inglesa quando a fala vem marcada
#    `lang:"en"`. Aqui esta o detector: conservador de proposito — na duvida, PT
#    (a instrucao em portugues com sotaque nao atrapalha; o ingles com sotaque
#    forte, sim). Uma atividade so em portugues nunca marca nada -> nada muda.
_PT_DIACR = u"ãõáéíóúâêôàçÃÕÁÉÍÓÚÂÊÔÀÇ"
_PT_PALAVRAS = set(u"""o a os as um uma que nao não de da do das dos e ou com sem
    para por no na nos nas ao aos toque ache escolha monte leia preencha ligue
    descubra ouca ouça arraste voce você rapido rápido pergunta resposta palavra
    frase foto pedaco pedaço certa certo certo dica pista aqui agora quem sua seu
    voz mascote conte cada tem esta está sao são muito bem parabens parabéns
    complete termine falta legenda cruzadinha quadro grade""".split())
_EN_PALAVRAS = set(u"""the is are am was were be being he she it they we you i
    his her its their your my this that these those what who where when how why
    doing playing cooking reading running writing dancing singing swimming
    watching listening carrying washing riding sitting eating painting a an of
    to in on at and or not yes no do does question answer word photo now right
    football guitar music tv newspaper bike kitchen field""".split())

def _idioma(s):
    t = re.sub(r"<[^>]+>", " ", s or "")
    if any(ch in t for ch in _PT_DIACR):
        return "pt"
    palavras = re.findall(r"[A-Za-z']+", t.lower())
    if not palavras:
        return "pt"
    # ⚠️ "a"/"no"/"do" existem nos DOIS idiomas — nao servem de sinal. Fora eles,
    #    conta sinal ingles vs portugues; ingles ganha quando DOMINA (>=2x), o que
    #    deixa passar um "a" solto de "riding a bike" sem virar portugues.
    ambiguas = {"a", "no", "do", "i"}
    en = sum(1 for p in palavras if p in _EN_PALAVRAS and p not in ambiguas)
    pt = sum(1 for p in palavras if p in _PT_PALAVRAS and p not in ambiguas)
    if en >= 1 and en >= 2 * pt:
        return "en"
    return "pt"


# ⭐ QUANTIDADE POR EXTENSO — a MESMA lista do `UNM` na peca `comparar.html`.
#    Duplicada aqui de proposito (o motor e JS, o montador e Python), com o
#    aviso cruzado nos dois arquivos: nomes de numero sao fato estavel, nao
#    conteudo que muda. Se um dia crescer, cresce nos DOIS — senao a chave da
#    voz nao bate e o alto-falante do painel volta a ficar mudo.
_NUM_EXTENSO = [u"zero", u"um", u"dois", u"três", u"quatro", u"cinco", u"seis",
                u"sete", u"oito", u"nove", u"dez", u"onze", u"doze", u"treze",
                u"catorze", u"quinze", u"dezesseis", u"dezessete", u"dezoito",
                u"dezenove", u"vinte"]


def _num_extenso(n):
    u"""devolve a palavra do numero (0..20) ou None se nao for inteiro no range —
    a peca escreve o numero cru fora do range, que nao se grava."""
    if isinstance(n, bool) or not isinstance(n, int):
        return None
    if 0 <= n < len(_NUM_EXTENSO):
        return _NUM_EXTENSO[n]
    return None


def chave_voz(s):
    u"""a mesma conta do `chaveVoz` das atividades (djb2 em base 36) — assim a
    mesma frase sempre dá o mesmo arquivo, aqui e lá."""
    s = re.sub(r"\s+", " ", s or "").strip().lower()
    h = 5381
    for ch in s:
        h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
    if h == 0:
        return "0"
    dig, out = "0123456789abcdefghijklmnopqrstuvwxyz", ""
    while h:
        out = dig[h % 36] + out
        h //= 36
    return out


# ------------------------------------------------------------------ a arte
def arte_de(c, pasta="."):
    u"""O que a atividade precisa desenhar — e o que o BANCO já resolve.
    É o passo que economiza dinheiro: o que já existe não se gera."""
    pedidos = []

    # ⭐⭐ A ARTE DA IDENTIDADE — a que o MOTOR pede em TODA atividade, e que
    #    este arquivo esquecia. Defeito medido (ago/2026) montando a atividade
    #    de teste: o `arte.json` voltou com "0 figura(s) a gerar" e mesmo assim
    #    a banca achou DEZ imagens que nao carregam — as tres camadas do
    #    mascote, os seis crachas e a medalha. Ninguem tinha mandado desenhar,
    #    porque ninguem tinha PEDIDO. Quem fosse montar de manha geraria a arte
    #    das fases, publicaria, e a crianca abriria a atividade com o mascote
    #    e as figurinhas em quadradinho vazio.
    #    ⚠️ Os nomes vem do motor, nao da minha memoria: ver `motor.html`
    #    (`ID.pre+"_"+ID.mascote+"_feliz"`, `ID.pre+"_cr"+n`, `"med_"+ID.pre`).
    pre = c.get("prefixo") or ""
    masc = c.get("mascote") or "mascote"
    for camada in ("feliz", "fala", "pisca"):
        pedidos.append("%s_%s_%s" % (pre, masc, camada))
    for n in range(1, int(c.get("crachas") or 6) + 1):
        pedidos.append("%s_cr%d" % (pre, n))
    pedidos.append("med_%s" % pre)
    if c.get("fundo"):
        pedidos.append(re.sub(r"\.(png|jpg|jpeg|webp)$", "", c["fundo"]))

    # ⚠️ E AS FIGURAS DAS FASES moram no `dados`/`dadosExtra` (e o que a peca
    #    le), nao em `itens`/`opcoes` — que era o formato ANTIGO, de antes do
    #    esqueleto. Sem descer ali, atividade nenhuma pedia a arte das fases.
    def desce(v):
        if isinstance(v, dict):
            for k in v:
                # a MESMA lista que o `CHAVES_MUDAS` usa para nao mandar gravar
                # o nome do arquivo. Duas listas separadas ja divergiram uma vez.
                if k in CHAVES_DE_FIGURA \
                        and isinstance(v[k], str) and v[k] and "<" not in v[k]:
                    pedidos.append(re.sub(r"\.(png|jpg|jpeg|webp)$", "", v[k]))
                else:
                    desce(v[k])
        elif isinstance(v, list):
            for x in v:
                desce(x)

    for f in c["fases"]:
        for it in (f.get("itens") or []) + (f.get("opcoes") or []):
            if isinstance(it, dict) and it.get("img"):
                pedidos.append(it["img"])
        if f.get("img"):
            pedidos.append(f["img"])
        desce(f.get("dados"))
        desce(f.get("dadosExtra"))
    pedidos = sorted(set(p for p in pedidos if p))

    banco = {}
    cam = os.path.join(RAIZ, "_banco", "index.json")
    if os.path.exists(cam):
        banco = json.load(io.open(cam, encoding="utf-8"))["objetos"]
    chaves = dict((simples(n), n) for n in banco)

    # ⚠️⚠️ O BANCO ESTAVA SENDO IGNORADO POR UM DETALHE DE NOME (achado pelo
    #    Marcos, ago/2026: *"você chegou a consultar o banco de imagens?"*).
    #    O montador procurava pelo nome COMPLETO — `pd_pao` — e o banco guarda
    #    pela palavra — `pao`. Nunca casava. Ele anunciava "0 ja no banco" com
    #    245 objetos guardados la, e mandava PAGAR por arte que ja existia.
    #    Nesta atividade custou 1 figura; na proxima de ciencias custaria arvore,
    #    agua, alface, abobora — tudo o que ja esta desenhado.
    #
    #    ⚠️ E POR QUE NAO CASAR POR PEDACO DE PALAVRA: eu testei. "mel" casa com
    #    "bal-vermelho" e "sal" casa com "mesa_l" — ou seja, a figura ERRADA na
    #    frente da crianca, que e muito pior do que gastar centavos. O casamento
    #    e pela RAIZ EXATA (tirando so o prefixo da atividade), nunca por
    #    substring.
    def do_banco(nome):
        k = chaves.get(simples(nome))
        if k:
            return k
        # tira o prefixo da atividade (`pd_pao` -> `pao`) e tenta de novo, EXATO
        if "_" in nome:
            raiz = nome.split("_", 1)[1]
            k = chaves.get(simples(raiz))
            if k:
                return k
        return None

    # ⚠️ LICAO PAGA (ago/2026) — "A GERAR" PARA ARTE QUE JA ESTAVA NA PASTA.
    #    A arte de IDENTIDADE (mascote, cracha, medalha, fundo) nunca vem do
    #    banco, e por isso caia sempre em "a gerar" — mesmo depois de instalada
    #    em `<pasta>/img/`. O montador anunciava "11 figura(s) a gerar" com as
    #    onze ali, prontas, e eu quase disparei o lote de novo. Relatorio que
    #    conta o que NAO aconteceu e da mesma familia do commit que dizia
    #    "(gemini)" sem o Gemini ter sido chamado: parece resposta e e chute.
    #    Agora sao TRES baldes, e o terceiro e o que estava faltando.
    dentro = os.path.join(pasta, "img")
    ja = []

    tem, falta = [], []
    for p in pedidos:
        if os.path.exists(os.path.join(dentro, p + ".png")):
            ja.append(p)
            continue
        # a arte da IDENTIDADE nunca vem do banco: mascote, cracha, medalha e
        # fundo sao desta atividade e de mais nenhuma (regra do Marcos:
        # "nunca copiar avatares, sempre novo e tematico")
        raiz = p.split("_", 1)[1] if "_" in p else p
        if p.startswith("med_") or re.match(r"^cr\d+$", raiz) or \
           raiz in ("fundo", "cena") or raiz.startswith(("feliz", "fala", "pisca")) or \
           re.search(r"_(feliz|fala|pisca)$", p):
            falta.append(p)
            continue
        k = do_banco(p)
        (tem if k else falta).append(k or p)
    return {"pedidos": pedidos, "no_banco": tem, "gerar": falta, "na_pasta": ja}


# ------------------------------------------------------------------ o HTML

def politica_de_voz(ano):
    u"""⭐ QUANTO A ATIVIDADE FALA SOZINHA, por faixa etária.

    Ordem do Marcos (ago/2026): *"o botão com o áudio em tudo para ajudar quem
    não sabe ler é interessante, o aluno clica e escuta, mas a fala automática,
    acredito que os maiores não gostem disso a todo momento"*.

    O que sustenta: o princípio da SEGMENTAÇÃO de Mayer — *"melhores resultados
    quando a informação é segmentada e os alunos têm controle sobre o ritmo"*
    (`_pesquisa/web/narracao-automatica-por-faixa-etaria.md`). E o padrão de
    acessibilidade é não tocar áudio sozinho; a mesma fonte reconhece que
    obrigar a apertar Play em toda tela *"levaria a uma experiência ruim"*.

    ⚠️ HONESTIDADE, para não virar lenda daqui a um mês: **não achei estudo com
    corte por idade**. A linha abaixo vem do princípio (o controle do aprendiz
    cresce com a idade) e da prática da escola — não de um número medido. Está
    combinado com ele reavaliar.

    O BOTÃO de alto-falante continua em TUDO, em toda idade: é ele que ajuda
    quem não lê sem expor ninguém — o oposto do estigma."""
    n = re.search(r"(\d+)", str(ano or ""))
    n = int(n.group(1)) if n else 0
    if not n or n <= 2:
        return "tudo"          # pré, 1º e 2º: sem voz não há atividade
    if n <= 5:
        return "instrucao"     # 3º ao 5º: a instrução da fase, uma vez
    return "manual"            # 6º ao 9º: nada sozinho


def escreve_index(pasta, c, falas):
    u"""motor + SÓ as mecânicas usadas + o conteúdo = a atividade.

    ⚠️ SÓ AS USADAS, e isto não é economia de disco: é o PC da escola. As 74
    peças juntas dão 913 KB de JS. Uma atividade usa 16 — leva ~1/5 disso. Pôr
    tudo faria o AMD FX-4300 com 3,5 GB engasgar na abertura, e a criança
    olharia uma tela branca achando que quebrou."""
    motor = io.open(os.path.join(AQUI, "motor.html"), encoding="utf-8").read()
    usadas = []
    for f in c["fases"]:
        if f.get("mec") and f["mec"] not in usadas:
            usadas.append(f["mec"])

    js_pecas = recorta(os.path.join(AQUI, "pecas.js"), usadas)
    css_pecas = recorta(os.path.join(AQUI, "pecas.css"), usadas)

    pre = c["prefixo"].rstrip("_")
    dados = [u"\n/* ====== O CONTEUDO DESTA ATIVIDADE (escrito pelo montador) ====== */"]

    # ⭐ A IDENTIDADE — o que antes era "resto de clone" e agora é DADO.
    #    O motor não sabe o nome de nenhum mascote, não tem prefixo de figura,
    #    não tem chave de localStorage própria. Tudo vem daqui.
    mascote = c.get("mascote", "mascote")
    id_desta = json.dumps({
        "pre": pre,
        "mascote": mascote,
        "mascoteNome": c.get("mascoteNome") or mascote.capitalize(),
        "titulo": c.get("titulo", "Atividade"),
        "sub": c.get("sub", ""),
        "fundo": c.get("fundo", ""),
        # ⭐ fundo de FOTO detalhada (museu, cena) fica lindo na CAPA mas "engole"
        #    as fichas de vidro no JOGO. Com fundoSuave=true, o motor desfoca+escurece
        #    o #bg SO nas telas de jogo (a capa continua nítida). Opt-in: atividade
        #    que nao pede continua igual.
        "fundoSuave": bool(c.get("fundoSuave")),
        "crachas": int(c.get("crachas", 6)),
        # o convite do crachá é da HISTÓRIA desta atividade ("Quem vai pilotar
        # o foguete hoje?"), não um texto de sistema
        "convite": c.get("convite") or u"<b>Quem vai jogar</b> hoje?",
        # ⭐ a VOZ QUE FALA SOZINHA sai da IDADE, nao do gosto de quem monta
        "narrar": politica_de_voz(c.get("ano", "")),
    }, ensure_ascii=False)
    dados.append(u"ROTULOS = %s;" % json.dumps(c.get("conceitos") or {},
                                               ensure_ascii=False))
    # a pré-carga: o mascote em 3 camadas, os crachás, a medalha e a arte das
    # fases — nunca a lista da atividade de origem
    # ⚠️ LICAO PAGA (ago/2026): esta lista pedia CINCO poses do mascote, mas a
    # regra da casa so exige TRES (parada, fala, pisca — as outras duas teriam
    # de ser EDICAO da parada, e nem sempre existem). Resultado: `_pensa` e
    # `_festa` entravam na pre-carga, davam 404 e a crianca via o pedido de uma
    # figura que nunca foi desenhada. Agora: as tres obrigatorias sempre; as
    # duas opcionais so se o arquivo ESTIVER na pasta.
    # E a licao maior: "pensar" e "comemorar" nao precisam de desenho novo —
    # sao MOVIMENTO da pose parada (ver `.mascote.pensando`/`.festejando` no
    # tema). Desenho novo do mascote sai fora do personagem com facilidade
    # assustadora; movimento nao tem como sair.
    imgs = ["%s_%s_%s" % (pre, mascote, x) for x in ("feliz", "fala", "pisca")]
    for extra in ("pensa", "festa"):
        nome_extra = "%s_%s_%s" % (pre, mascote, extra)
        if os.path.exists(os.path.join(pasta, "img", nome_extra + ".png")):
            imgs.append(nome_extra)
    imgs += ["%s_cr%d" % (pre, i + 1) for i in range(int(c.get("crachas", 6)))]
    imgs.append("med_" + pre)
    for f in c["fases"]:
        for it in (f.get("itens") or []) + (f.get("opcoes") or []):
            if isinstance(it, dict) and it.get("img"):
                imgs.append(it["img"])
        if f.get("img"):
            imgs.append(f["img"])
    vistas, limpa = set(), []
    for x in imgs:
        if x not in vistas:
            vistas.add(x)
            limpa.append(x)
    dados.append(u"IMGS = %s;" % json.dumps(limpa, ensure_ascii=False))

    # ⭐ A VITRINE QUE ENCHE: uma figura por fase, tirada da PROPRIA fase — o
    #    doce que a crianca acabou de ver e o que entra atras do vidro. Fase sem
    #    figura (traçar, ligar pontos) pega emprestada a figura de outra fase,
    #    girando a lista: a vitrine tem que ter uma vaga por fase, senao ela
    #    para de contar a historia certa.
    #    ⚠️ so entra figura de PRODUTO: mascote, crachá e medalha ficam de fora
    #    (vitrine de padaria com a cara do padeiro dentro nao e vitrine).
    fora = set(["med_" + pre] + ["%s_%s_%s" % (pre, mascote, x)
                                 for x in ("feliz", "fala", "pisca", "pensa", "festa")]
               + ["%s_cr%d" % (pre, i + 1) for i in range(int(c.get("crachas", 6)))])
    # ⚠️ a figura NAO mora num campo fixo: cada mecanica guarda a dela do seu
    #    jeito, dentro da gaveta `dados` (a `ouvir-achar` poe o nome cru em
    #    `alvo`/`opcoes`, outras usam `img`, outras aninham mais fundo). Um
    #    `f.get("itens")` so acha as que ja conheco — e foi assim que a vitrine
    #    nasceu vazia na primeira tentativa. Entao: varrer a fase INTEIRA atras
    #    de nome de figura que EXISTA na pasta. O disco e a verdade.
    def figura_da_fase(no, achado):
        if achado[0]:
            return
        if isinstance(no, dict):
            for v in no.values():
                figura_da_fase(v, achado)
        elif isinstance(no, list):
            for v in no:
                figura_da_fase(v, achado)
        elif isinstance(no, basestring if str is bytes else str):
            if (no.startswith(pre + "_") and no not in fora
                    and os.path.exists(os.path.join(pasta, "img", no + ".png"))):
                achado[0] = no

    por_fase, sobra = [], []
    for f in c["fases"]:
        achado = [None]
        figura_da_fase(f, achado)
        achou = achado[0]
        por_fase.append(achou)
        if achou and achou not in sobra:
            sobra.append(achou)
    # ⚠️⚠️ LICAO PAGA (ago/2026) — VITRINE DE UMA FIGURA SO. A Central de
    #    Entregas nao tem "produto": tem TEXTO. A varredura achou uma unica
    #    figura elegivel (uma folha borrada, que era pista de outra fase) e a
    #    vitrine encheu as TRINTA E NOVE vagas com ela — a mesma miniatura de
    #    53x32 repetida 13 vezes por tela, que o portao do encaixe acusou como
    #    "PEQUENA DEMAIS" dezenas de vezes. Pior: a vitrine existe para contar
    #    "olha tudo o que voce ja juntou", e uma prateleira com o mesmo item
    #    repetido conta o contrario — que nada muda por mais que a crianca ande.
    #    O montador ja IMPRIMIA "1 figura(s) diferentes" e eu passei o olho.
    #    Aviso que so informa nao segura nada: virou decisao.
    # ⭐ A BARRA PREMIUM (poeVitrine: trilho + cometa + "X / N") usa so a
    #    QUANTIDADE de fases (VITRINE.length) — NAO as figuras. Entao ela tem que
    #    aparecer em TODA atividade, inclusive nas de PALAVRA (Teatro, 5o ano),
    #    que nao tem figura de produto.
    #    ⚠️ LICAO PAGA (Teatro, ago/2026): a VITRINE saia VAZIA quando faltavam
    #    figuras e a barra premium sumia — o 1o ano (Lojinha, com dinheiro) ficava
    #    com a barra bonita e o 5o ano com a barra simples. O Marcos pegou no olho.
    #    As MINIATURAS entram quando existem (>=3 distintas, p/ nao repetir a mesma
    #    figura e contar a historia errada), mas a barra premium nao depende delas:
    #    VITRINE sempre sai com uma vaga por fase.
    MINIMO_VITRINE = 3
    if 0 < len(sobra) < MINIMO_VITRINE:
        print(u"   vitrine: so %d figura(s) diferente(s) (min %d) — barra premium "
              u"mesmo assim, sem miniaturas (nao repete a mesma figura)."
              % (len(sobra), MINIMO_VITRINE))
        sobra = []
    if sobra:
        giro = 0
        for i, x in enumerate(por_fase):
            if not x:
                por_fase[i] = sobra[giro % len(sobra)]; giro += 1
        print(u"   vitrine: %d vaga(s), %d figura(s) diferentes"
              % (len(por_fase), len(sobra)))
    else:
        por_fase = [u"" for _ in por_fase]   # barra premium sem miniatura (atividade de texto)
        print(u"   vitrine: %d vaga(s) (barra premium sem miniatura — atividade de texto)"
              % len(por_fase))
    dados.append(u"VITRINE = %s;" % json.dumps(por_fase, ensure_ascii=False))

    # ⚠️⚠️ RESTO DE CLONE NA TELA FINAL (ago/2026) — e o pior lugar possivel,
    #    porque e a ultima coisa que a crianca le. O motor trazia CRAVADO do
    #    Jardim do Broto: *"Jardineiro Mestre!"* e *"voce cuidou da planta do
    #    comeco ao fim"*. Na Padaria das Letras a crianca terminava a aula
    #    sendo chamada de jardineira. O texto de fim JA existia no
    #    conteudo.json (com o gancho de curiosidade e tudo) e era simplesmente
    #    ignorado. Agora o fim tambem e DADO.
    fim_txt = c.get("fim") or u"Você conseguiu!"
    fim_tit = c.get("fimTitulo") or ((c.get("titulo") or u"Campeão") + u"!")
    fim_cra = c.get("fimCracha") or fim_tit.rstrip(u"!")
    dados.append(u"FIM = {titulo:%s, texto:%s, cracha:%s};"
                 % (jstr(fim_tit), jstr(fim_txt), jstr(fim_cra)))

    dados.append(u"ABERTURA = {texto:%s, voz:%s};"
                 % (jstr(c.get("abertura") or ""), jstr(pre + "_abertura")))
    fases = []
    for f in c["fases"]:
        d = dict(f)
        d["vozIntro"] = "%s_%s_intro" % (pre, f["id"])
        if f.get("dica"):
            d["dicaVoz"] = "%s_%s_dica" % (pre, f["id"])
        fases.append(d)
    dados.append(u"FASES = " + json.dumps(fases, ensure_ascii=False) + u";")
    # ⭐ o AR da atividade (borboletas do jardim nao voam na padaria) — ver o
    #    bloco "AMBIENTE VIVO" do motor. Sem declarar, e a poeirinha neutra.
    dados.append(u'AMBI = %s;' % json.dumps(c.get("ambiente", "poeira"), ensure_ascii=False))
    dados.append(u"VOZOK = " + json.dumps(
        dict((x["id"][3:], 1) for x in falas if x["id"].startswith("op_")),
        ensure_ascii=False) + u";")
    # ⚠️ BNCC do RELATORIO do professor. Antes o motor trazia PLANTAS hardcoded
    #    (EF02CI05/06, "agua e luz", "partes da planta") — resto de clone do
    #    Jardim que aparecia no parecer de TODA atividade (o Marcos pegou, ago/2026).
    #    Agora sai da propria atividade: campo `bncc` se existir; senao os codigos
    #    EF que estiverem escritos na `mesa`/`curriculo`/`conceitos`.
    _bncc = c.get("bncc")
    if not _bncc:
        _txt = (json.dumps(c.get("curriculo") or {}, ensure_ascii=False) + u" "
                + str(c.get("mesa", "")) + u" "
                + json.dumps(c.get("conceitos") or {}, ensure_ascii=False))
        _codes = []
        for _m in re.findall(r"EF\d{2}[A-Z]{2}\d{2}", _txt):
            if _m not in _codes:
                _codes.append(_m)
        _bncc = u", ".join(_codes)
    dados.append(u"RELBNCC = %s;" % json.dumps(_bncc or u"", ensure_ascii=False))

    saida = motor
    # ⚠️⚠️ LICAO PAGA, da familia da ORDEM DE BOOT: o `ID` era escrito no FIM,
    #    junto com as fases. So que o corpo do motor USA `ID.pre` durante a
    #    leitura do arquivo — `var perfil={nome:"",fig:ID.pre+"_cr1"}` roda ali
    #    mesmo. Com o `ID` chegando depois, o crachá da criança nascia
    #    `skel_cr1` (o valor de fábrica), uma figura que não existe em nenhuma
    #    atividade: quadradinho vazio na tela do "Quem vai jogar?". Por isso o
    #    `ID` desta atividade SUBSTITUI o de fábrica, lá em cima, e não é uma
    #    atribuição no fim.
    novo_id = u"var ID = %s;" % id_desta
    saida, quantos = re.subn(r"var ID = \{[^;]*\};", lambda m: novo_id, saida, count=1)
    if not quantos:
        print(u"   AVISO: nao achei o `var ID` de fabrica no motor — "
              u"rode extrair_motor.py de novo")
    # ⭐ MASCOTE_NOME literal — o motor traz `var MASCOTE_NOME="";` de fabrica, e o
    #    portao 3e (`_qa/voz_do_mascote.py`) le esse literal para saber de quem e a
    #    voz (o artigo "o Coru"/"a Lina" x a voz de voz.txt). Vazio = "rodou cego"
    #    e a banca reprova. Preenche com o nome desta atividade.
    _mnome = (c.get("mascoteNome") or mascote.capitalize())
    saida, _qm = re.subn(r'var MASCOTE_NOME\s*=\s*"[^"]*";',
                         u'var MASCOTE_NOME="%s";' % _mnome, saida, count=1)
    if not _qm:
        print(u"   AVISO: nao achei `var MASCOTE_NOME` no motor para preencher.")
    # ⭐ MARCADOR DE ATIVIDADE CRIATIVA no HTML — para os portoes da banca
    #    (padrao/pedagogo/cobertura) saberem que e um livro de colorir (mono-
    #    mecanica de PRODUCAO) e nao cobrarem variedade/aquecimento/cobertura,
    #    do mesmo jeito que o validador do montador ja faz. So aparece quando o
    #    conteudo DECLARA `tipo:"criativa"` — ninguem escapa por acidente.
    if str(c.get("tipo", "")).strip().lower() in ("criativa", "livre", "colorir"):
        saida, _qt = re.subn(r'(var MASCOTE_NOME\s*=)',
                             u'var TIPO_ATIVIDADE="criativa"; \\1', saida, count=1)
        if not _qt:
            saida = saida.replace("<script>", '<script>var TIPO_ATIVIDADE="criativa";', 1)
    # ⭐ AVALIAÇÃO (Marcos, ago/2026: "avaliação trimestral"): é um instrumento de
    #    NOTA, mais curto que uma aula de 55 min e SEM aquecimento (não há revisão
    #    espaçada numa prova). Marca `TIPO_ATIVIDADE="avaliacao"` para o piso de
    #    duração (que só cobra "jogo") não reprovar — mas MANTÉM variedade e
    #    cobertura por objetivo (uma avaliação boa é variada e cobre o trimestre).
    elif str(c.get("tipo", "")).strip().lower() in ("avaliacao", "avaliação", "prova"):
        saida, _qt = re.subn(r'(var MASCOTE_NOME\s*=)',
                             u'var TIPO_ATIVIDADE="avaliacao"; \\1', saida, count=1)
        if not _qt:
            saida = saida.replace("<script>", '<script>var TIPO_ATIVIDADE="avaliacao";', 1)
    # ⭐ O TEMA DA ATIVIDADE — `<pasta>/tema.css`, se existir.
    #    Entra por ULTIMO de proposito: e a camada que da IDENTIDADE (a lousa da
    #    padaria, a bandeja de metal, o toldo listrado) e por isso tem que
    #    ganhar do motor e das peças no empate de especificidade.
    #    ⚠️ POR QUE NAO NO MOTOR: o acabamento e da ATIVIDADE, nao do esqueleto.
    #    Pintar a madeira da padaria no `.btn` do motor pintaria TODA atividade
    #    futura de padaria — inclusive a de ciencias do 6o ano. O motor fica
    #    neutro; quem tem cara e a atividade.
    tema = os.path.join(pasta, "tema.css")
    css_tema = u""
    if os.path.exists(tema):
        css_tema = (u"\n/* ==== TEMA DA ATIVIDADE (%s/tema.css) ==== */\n"
                    % os.path.basename(pasta.rstrip("/"))) + \
                   io.open(tema, encoding="utf-8").read()
        print(u"   tema proprio: tema.css (%d KB)" % (len(css_tema) // 1024))
    saida = saida.replace(u"</style>", css_pecas + css_tema + u"\n</style>", 1)
    saida = saida.replace(u"</script>\n</body>",
                          js_pecas + u"\n" + u"\n".join(dados) + u"\n</script>\n</body>", 1)
    saida = saida.replace(u"<title>MOTOR — esqueleto</title>",
                          u"<title>%s</title>" % c.get("titulo", "Atividade"), 1)
    io.open(os.path.join(pasta, "index.html"), "w", encoding="utf-8").write(saida)
    escreve_sw(pasta, c, saida)


def escreve_sw(pasta, c, html):
    u"""⚠️ LIÇÃO PAGA (Lojinha, ago/2026 — Marcos: 'ao clicar no Próximo dá página
    sem conexão'). O motor SEMPRE registra `navigator.serviceWorker.register("sw.js")`,
    mas o montador NUNCA escrevia o sw.js: o arquivo dava 404 e, com a internet
    instável da escola, a navegação caía na 'página sem conexão'. Agora o montador
    gera um sw.js REDE-PRIMEIRO no HTML (online = sempre a tela fresca; offline/rede
    caindo = volta para o index.html do cache, nunca a tela de erro) e CACHE-PRIMEIRO
    em imagem/áudio. `skipWaiting`+`clients.claim` derrubam qualquer SW velho preso.
    O nome do cache leva um HASH do index → cada build novo limpa o cache anterior
    (senão voz regravada continuaria saindo a antiga). O prefixo isola dos outros
    apps no mesmo vidalprof.github.io."""
    import hashlib
    ver = hashlib.md5(html.encode("utf-8")).hexdigest()[:10]
    pre = re.sub(r"[^a-z0-9]+", "", (c.get("prefixo", "app") or "app").lower()) or "app"
    # ⚠️ so pre-cacheia manifest.json se ELE existir (o clone.py acusava a atividade
    #    sem PWA pedindo o manifest da origem). Sem manifest, cacheia so a casca.
    _ativos = u'["./","./index.html"'
    if os.path.exists(os.path.join(pasta, "manifest.json")):
        _ativos += u',"./manifest.json"'
    _ativos += u']'
    sw = (
        u'/* GERADO por montar.py — NAO editar a mao.\n'
        u'   REDE PRIMEIRO no HTML (nunca prende versao velha; se a rede cair, volta\n'
        u'   ao index.html do cache em vez da "pagina sem conexao"); CACHE PRIMEIRO\n'
        u'   em imagem/audio. O HASH no nome do cache troca a cada build. */\n'
        u'var PREFIXO="%s-";\n'
        u'var CACHE=PREFIXO+"%s";\n'
        u'var ATIVOS=%s;\n'
        u'self.addEventListener("install",function(e){self.skipWaiting();e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(ATIVOS).catch(function(){});}));});\n'
        u'self.addEventListener("activate",function(e){e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.map(function(k){if(k!==CACHE&&k.indexOf(PREFIXO)===0)return caches.delete(k);}));}));self.clients.claim();});\n'
        u'function guardar(req,resp){try{if(resp&&resp.status===200&&resp.type==="basic"){var cp=resp.clone();caches.open(CACHE).then(function(c){c.put(req,cp);});}}catch(x){}return resp;}\n'
        u'self.addEventListener("fetch",function(e){\n'
        u'  if(e.request.method!=="GET")return;\n'
        u'  var req=e.request,aceita=req.headers.get("accept")||"";\n'
        u'  var ehPagina=(req.mode==="navigate")||aceita.indexOf("text/html")>=0;\n'
        u'  if(ehPagina){e.respondWith(fetch(req).then(function(r){return guardar(req,r);}).catch(function(){return caches.match(req).then(function(c){return c||caches.match("./index.html");});}));}\n'
        u'  else{e.respondWith(caches.match(req).then(function(c){var rede=fetch(req).then(function(r){return guardar(req,r);}).catch(function(){return c;});return c||rede;}));}\n'
        u'});\n'
    ) % (pre, ver, _ativos)
    io.open(os.path.join(pasta, "sw.js"), "w", encoding="utf-8").write(sw)
    print(u"   sw.js gerado (rede-primeiro, cache %s-%s)" % (pre, ver))


def jstr(s):
    return json.dumps(s, ensure_ascii=False)


def recorta(caminho, nomes):
    u"""tira do arquivo gerado só os pedaços das mecânicas usadas.

    ⚠️ LIÇÃO PAGA: a marca de peça tem que ser uma marca que NENHUMA peça
    escreva por acaso. A primeira era `/* ---------- nome ---------- */` e as
    próprias peças usam esse traço nos comentários delas — 163 marcas para 74
    peças. O recorte partia a peça no primeiro comentário interno e a atividade
    saía com meia mecânica: JS quebrado na mão da criança."""
    if not os.path.exists(caminho) or not nomes:
        return u""
    txt = io.open(caminho, encoding="utf-8").read()
    partes = re.split(r"(?=/\* ==== PECA: )", txt)
    # ⚠️ o que vem ANTES da 1a peça são as FERRAMENTAS que todas usam (`nota`,
    #    `ac`). Recortar só as peças deixava esse cabeçalho para trás e a
    #    atividade morria no primeiro som — "nota is not defined".
    fora = [partes[0]] if partes and not partes[0].startswith("/* ==== PECA:") else []
    for bloco in partes:
        m = re.match(r"/\* ==== PECA: ([\w-]+) ==== \*/", bloco)
        if m and m.group(1) in nomes:
            fora.append(bloco)
    achadas = set(m.group(1) for m in
                  (re.match(r"/\* ==== PECA: ([\w-]+) ==== \*/", b) for b in fora)
                  if m)
    for n in nomes:
        if n not in achadas:
            print(u"   AVISO: a mecanica '%s' nao esta em %s — rode "
                  u"integrar.py --escrever" % (n, os.path.basename(caminho)))
    return u"".join(fora)


# ------------------------------------------------------------------ principal
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    pasta = sys.argv[1].rstrip("/")
    so_ver = "--so-ver" in sys.argv
    cam = os.path.join(pasta, "conteudo.json")
    if not os.path.exists(cam):
        print(u"nao achei %s" % cam)
        return 2
    c = json.load(io.open(cam, encoding="utf-8"))

    problemas, avisos = confere(c, mecanicas())
    p2, a2 = confere_dados(c, mecanicas())
    problemas.extend(p2)
    avisos.extend(a2)
    print(u"MONTADOR — %s (%s, %d fase(s))"
          % (c.get("titulo", "?"), c.get("ano", "?"), len(c.get("fases", []))))
    for a in avisos:
        print(u"   aviso: %s" % a)
    if problemas:
        print(u"   %d PROBLEMA(S) — nada foi gerado:" % len(problemas))
        for p in problemas:
            print(u"    - %s" % p)
        return 1

    falas = falas_de(c)
    # ⭐ FALAS EXTRA (deterministicas) — CONTRATO, licao paga no Museu (ago/2026):
    #    as frases de AUTO-AJUDA que a PECA monta em tempo de jogo (memoria
    #    "Vou abrir este par: X — Y" / "Abri uma para voce: X. Ache o par dela.",
    #    caca "Achou as N palavras!") o colher so pegava JOGANDO, e apenas as que
    #    o ACASO disparava naquela rodada. O portao 0f2 reprovava uma frase
    #    DIFERENTE a cada banca (flakiness pura). Agora a atividade LISTA essas
    #    frases em conteudo["falasExtra"] e TODAS entram de uma vez, sempre — a
    #    chave e o MESMO chaveVoz(texto_limpo) do runtime, entao o mp3 casa.
    _ids = set(f["id"] for f in falas)
    for _t in (c.get("falasExtra") or []):
        _t = (_t or "").strip()
        if not _t:
            continue
        _id = "op_" + chave_voz(texto_limpo(_t))
        if _id not in _ids:
            # id/hash no texto original; AUDIO com pronuncia corrigida (ver _fonetica_voz)
            falas.append({"id": _id, "texto": _fonetica_voz(texto_limpo(_t))})
            _ids.add(_id)
    # ⚠️ A COLHEITA NAO PODE SER APAGADA. O `colher.py` joga a atividade e anota
    #    as frases que so existem em tempo de jogo ("Achou as 4 palavras da
    #    horta!") — coisas que o conteudo.json nao tem como saber. Se o montador
    #    reescrevesse o falas.json do zero, o ciclo
    #        montar -> colher -> montar
    #    apagaria na terceira etapa o que ganhou na segunda, e as telas de fecho
    #    de rodada voltariam a ficar mudas sem ninguem perceber.
    # ⚠️ LICAO PAGA (Museu, ago/2026): quando o TEXTO de uma voz muda (ex.: o
    #    artigo, "O baleia" -> "A baleia"), a versao nova entra com chave nova e a
    #    VELHA ficava presa aqui como "colhida" (id diferente, texto fora do set).
    #    A crianca ouvia a certa (o motor usa a chave do texto atual), mas o
    #    falas.json carregava a errada pendurada — e o Revisor a via. Agora, antes
    #    de guardar, normalizo (tiro artigo/caixa/HTML): se a versao ATUAL ja
    #    cobre aquele texto, a velha e stale e NAO se guarda.
    def _norm_voz(t):
        t = re.sub(r"<[^>]+>", "", t or "").strip().lower()
        t = re.sub(r"^(o|a|os|as|um|uma)\s+", "", t)
        return re.sub(r"\s+", " ", t)
    guardadas = []
    antigo = os.path.join(pasta, "falas.json")
    if os.path.exists(antigo):
        try:
            ids = set(f["id"] for f in falas)
            atuais_norm = set(_norm_voz(f.get("texto", "")) for f in falas)
            for f in json.load(io.open(antigo, encoding="utf-8")):
                if f.get("id") in ids:
                    continue
                if _norm_voz(f.get("texto", "")) in atuais_norm:
                    continue                    # versao stale (mudou artigo/caixa)
                guardadas.append(f)
        except Exception:
            pass
    falas.extend(guardadas)
    if guardadas:
        print(u"   %d fala(s) colhida(s) em jogo preservada(s)" % len(guardadas))
    # ⭐ VARREDURA FONETICA FINAL: garante que NENHUM texto que vai ao TTS carregue
    #    palavra que a voz erra (face->fásse), inclusive as colhidas antigas
    #    preservadas acima (que nasceram antes do conserto). Só mexe no `texto`;
    #    o `id`/hash continua o do texto da tela, então o mp3 casa igual.
    for _f in falas:
        if _f.get("texto"):
            _f["texto"] = _fonetica_voz(_f["texto"])
    arte = arte_de(c, pasta)
    print(u"   escada ok | %d fala(s) a gravar | %d figura(s): %d ja na pasta, "
          u"%d ja no banco, %d a gerar"
          % (len(falas), len(arte["pedidos"]), len(arte.get("na_pasta") or []),
             len(arte["no_banco"]), len(arte["gerar"])))
    if arte["gerar"]:
        print(u"   a gerar (EM CARTELA — `python3 _padrao/cartela.py plano`): %s"
              % ", ".join(arte["gerar"][:12]))
    if so_ver:
        print(u"   (--so-ver: nada foi escrito)")
        return 0

    escreve_index(pasta, c, falas)
    io.open(os.path.join(pasta, "falas.json"), "w", encoding="utf-8").write(
        json.dumps(falas, ensure_ascii=False, indent=1))
    # o workflow de voz le daqui qual voz usar nesta atividade
    VOZES = {"masculina": "pt-BR-AntonioNeural", "feminina": "pt-BR-FranciscaNeural"}
    io.open(os.path.join(pasta, "voz.txt"), "w", encoding="utf-8").write(
        VOZES.get(str(c.get("voz", "")).strip().lower(), "pt-BR-AntonioNeural") + "\n")

    io.open(os.path.join(pasta, "arte.json"), "w", encoding="utf-8").write(
        json.dumps(arte, ensure_ascii=False, indent=1))
    print(u"   escrito: %s/index.html, falas.json e arte.json" % pasta)
    # ⭐ NARRACAO CONFERIDA NA HORA (ago/2026): antes, palavra que a voz erra
    #    ("complita") ou chave de imagem virando "pe-de pao" so apareciam na
    #    banca de 20 min. Agora o montador chama o MESMO `_qa/falas.py` (funcao
    #    `checa`, fonte unica) sobre o que acabou de gerar e AVISA aqui —
    #    "ja sair perfeito na hora de montar" (RECEITA.md). So aviso: o index ja
    #    esta escrito, e a lista `guardadas` (falas colhidas em jogo) tambem
    #    entra na conferencia.
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "..", "..", "_qa"))
        import falas as _falas
        maus = _falas.checa(falas)
        if maus:
            print(u"   AVISO: %d fala(s) que a voz erra (rode `python3 _qa/falas.py "
                  u"%s/falas.json` p/ detalhe):" % (len(maus), pasta))
            for _id, palavra, erro, troca, _t in maus[:10]:
                print(u'      "%s" -> %s | troque por: %s' % (palavra, erro, troca))
    except Exception as e:                                     # noqa: BLE001
        print(u"   aviso: nao consegui conferir a narracao (%s)" % str(e)[:80])


    # ⚠️ OS PROMPTS SAEM JUNTO (pedido do Marcos, ago/2026: *"gere os prompts
    #    que eu preciso, que eu gero aqui"*). Dizer QUAIS figuras faltam sem
    #    dizer COMO pedi-las era deixar o passo mais demorado por conta da mao —
    #    e prompt escrito na hora sai diferente a cada vez, entao figura irma
    #    virava figura estranha. Agora a esteira entrega os dois: o `_lote.json`
    #    para o workflow e o `PROMPTS-IMAGENS.md` para gerar na mao.
    #    Falhar aqui NAO derruba a montagem: o index.html ja esta escrito.
    try:
        import prompts as _prompts
        _prompts.escreve(pasta)
    except Exception as e:                                     # noqa: BLE001
        print(u"   aviso: nao consegui escrever os prompts das figuras (%s)"
              % str(e)[:120])
    return 0


if __name__ == "__main__":
    sys.exit(main())
