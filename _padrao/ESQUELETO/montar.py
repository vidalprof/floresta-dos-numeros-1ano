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
    minimo = 10 if pequeno else 16

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
    if len(vistos) < minimo:
        p.append(u"so %d mecanica(s) diferente(s); o combinado para este ano sao "
                 u"%d (ver CONTRATO.md)" % (len(vistos), minimo))
    for m, q in sorted(vistos.items()):
        if n and q / float(n) > 0.40:
            p.append(u"a mecanica '%s' ocupa %d%% das fases (teto: 40%%)"
                     % (m, round(100.0 * q / n)))
    # ⚠️ vizinhança: duas fases seguidas com o mesmo gesto e "a mesma tela pela
    #    terceira vez", mesmo que o conteudo mude
    for i in range(1, len(ordem)):
        if ordem[i] == ordem[i - 1]:
            p.append(u"as fases %d e %d usam a MESMA mecanica ('%s') coladas — "
                     u"a segunda vez tem que vir depois, e um degrau acima"
                     % (i, i + 1, ordem[i]))
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
def chaves_de(v, fundo=None):
    u"""todos os nomes de campo que aparecem dentro de uma estrutura."""
    fundo = set() if fundo is None else fundo
    if isinstance(v, dict):
        for k, x in v.items():
            fundo.add(k)
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

        # ⚠️ GAVETA MEIA-CHEIA DEIXA A FASE SEM SAIDA. O "separe nas gavetas" tem
        #    TRES: as gavetas (com as chaves), as fichas (que APONTAM para essas
        #    chaves) e as dicas. Preenchendo so as gavetas, as chaves deixam de
        #    casar e nenhuma ficha pode ser posta — a crianca fica presa, e nao ha
        #    erro de JS nenhum. Foi o auditor-jogador que pegou, travado em 22%.
        # ⚠️ AVISO QUE GRITA A TOA ENSINA A IGNORAR AVISO (ago/2026). Nem toda
        #    gaveta e CONTEUDO: `NUM` e a tabela dos nomes dos numeros, `FEITAS`
        #    e `GALERIA` sao ESTADO (nascem vazias e a peca preenche jogando),
        #    `TINTAS` e a paleta, `DIRS`/`LIN`/`COL`/`ROT`/`NOMEH`/`NOMEM` sao
        #    rotulos fixos do motorzinho. Deixar essas no exemplo e o CERTO — e
        #    mesmo assim eu levava quatro avisos numa montagem so, o que faz a
        #    gente parar de ler os avisos que importam.
        ESTADO = set("NUM FEITAS GALERIA TINTAS DIRS LIN COL ROT NOMEH NOMEM "
                     "CORES PALETA POSFRU POSJAN".split())
        outras = [v for v in (info.get("gavetas") or [])
                  if v != info.get("var") and v not in ESTADO]
        faltando = [v for v in outras if v not in (f.get("dadosExtra") or {})]
        if outras and faltando:
            avisos.append(u"fase %d (%s), mecanica '%s': voce preencheu '%s' mas "
                          u"deixou %s com o conteudo de EXEMPLO. Se uma gaveta "
                          u"aponta para a outra (chave/alvo), a fase fica SEM "
                          u"SAIDA e nada reclama — confira em pecas.json"
                          % (i + 1, f.get("id"), mec, info.get("var"),
                             " e ".join("'%s'" % v for v in faltando)))

        exemplo = literal(info.get("exemplo"))
        if exemplo is None:
            continue
        conhecidas = chaves_uteis(exemplo)
        if not conhecidas:
            continue
        usadas = chaves_uteis(f["dados"])
        estranhas = sorted(usadas - conhecidas)
        if estranhas:
            ruins.append(u"fase %d (%s), mecanica '%s': campo(s) que a peca NAO "
                         u"le: %s. Ela conhece: %s. (o conteudo seria ignorado e "
                         u"a fase sairia vazia, sem erro nenhum)"
                         % (i + 1, f.get("id"), mec, ", ".join(estranhas),
                            ", ".join(sorted(conhecidas))))
        for chave, val in (f.get("dadosExtra") or {}).items():
            if chave not in (info.get("gavetas") or []):
                ruins.append(u"fase %d: 'dadosExtra' fala de '%s', que nao e "
                             u"gaveta de '%s' (as gavetas sao: %s)"
                             % (i + 1, chave, mec,
                                ", ".join(info.get("gavetas") or [])))
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
        out.append({"id": ident, "texto": t})

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
MOLDE_ITEM = re.compile(
    r'el\(\s*"div"\s*,\s*"balao[^"]*"\s*,\s*'
    r'("(?:[^"\\]|\\.)*"(?:\s*\+\s*[A-Za-z_$][\w$]*\.[\w$]+\s*\+\s*"(?:[^"\\]|\\.)*")+)\s*\)')


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
    m = MOLDE_ITEM.search(src)
    if not m:
        return
    partes = re.split(r'\s*\+\s*', m.group(1))
    campos = [p.split(".", 1)[1] for p in partes if not p.startswith('"')]
    if not campos:
        return
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
                    if v is None:
                        montado = u""
                        break
                    montado += u"%s" % v
            txt = como_na_tela(montado)
            if len(txt.split()) >= 3:
                poe("op_" + chave_voz(txt), txt)


# chaves cujo valor NAO e texto para a crianca (sao codigo: identificador,
# imagem, cor, coordenada). Sem esta lista, o montador mandaria gravar "p0".
CHAVES_MUDAS = set("""k id img ic cor classe cls tipo mec r c x y w h lin col
    pLin pCol lado dir face src href fundo forma icone""".split())


def eh_fala(txt):
    u"""isto e frase para a crianca ouvir, ou e codigo?"""
    t = (txt or "").strip()
    if len(t) < 3:
        return False
    baixo = t.lower()
    for ruim in ("<svg", "xmlns", "data:", "url(", "http", "#fff", "rgba(",
                 "translate", "polygon", "viewbox"):
        if ruim in baixo:
            return False
    if t.startswith("#") or t.startswith("."):
        return False
    letras = sum(1 for ch in t if ch.isalpha())
    if letras < 2:
        return False
    # identificador solto ("raiz", "p0", "gav1"): sem espaco, tudo minusculo e
    # curto. Palavra que a crianca le vem em CAIXA ou com espaco.
    if " " not in t and t == baixo and len(t) <= 6:
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
                continue
            falas_dos_dados(val, poe)
    elif isinstance(dados, list):
        for x in dados:
            falas_dos_dados(x, poe)
    elif isinstance(dados, str):
        t = texto_limpo(dados)
        if eh_fala(t):
            poe("op_" + chave_voz(t), t)


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
def arte_de(c):
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
                if k in ("img", "fig", "foto", "imagem", "cena", "verso", "cenaA", "cenaB") \
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

    tem, falta = [], []
    for p in pedidos:
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
    return {"pedidos": pedidos, "no_banco": tem, "gerar": falta}


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
    imgs = ["%s_%s_%s" % (pre, mascote, x) for x in
            ("feliz", "fala", "pisca", "pensa", "festa")]
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
    dados.append(u"VOZOK = " + json.dumps(
        dict((x["id"][3:], 1) for x in falas if x["id"].startswith("op_")),
        ensure_ascii=False) + u";")

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
    saida = saida.replace(u"</style>", css_pecas + u"\n</style>", 1)
    saida = saida.replace(u"</script>\n</body>",
                          js_pecas + u"\n" + u"\n".join(dados) + u"\n</script>\n</body>", 1)
    saida = saida.replace(u"<title>MOTOR — esqueleto</title>",
                          u"<title>%s</title>" % c.get("titulo", "Atividade"), 1)
    io.open(os.path.join(pasta, "index.html"), "w", encoding="utf-8").write(saida)


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
    # ⚠️ A COLHEITA NAO PODE SER APAGADA. O `colher.py` joga a atividade e anota
    #    as frases que so existem em tempo de jogo ("Achou as 4 palavras da
    #    horta!") — coisas que o conteudo.json nao tem como saber. Se o montador
    #    reescrevesse o falas.json do zero, o ciclo
    #        montar -> colher -> montar
    #    apagaria na terceira etapa o que ganhou na segunda, e as telas de fecho
    #    de rodada voltariam a ficar mudas sem ninguem perceber.
    guardadas = []
    antigo = os.path.join(pasta, "falas.json")
    if os.path.exists(antigo):
        try:
            ids = set(f["id"] for f in falas)
            for f in json.load(io.open(antigo, encoding="utf-8")):
                if f.get("id") not in ids:
                    guardadas.append(f)
        except Exception:
            pass
    falas.extend(guardadas)
    if guardadas:
        print(u"   %d fala(s) colhida(s) em jogo preservada(s)" % len(guardadas))
    arte = arte_de(c)
    print(u"   escada ok | %d fala(s) a gravar | %d figura(s): %d ja no banco, "
          u"%d a gerar" % (len(falas), len(arte["pedidos"]),
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
