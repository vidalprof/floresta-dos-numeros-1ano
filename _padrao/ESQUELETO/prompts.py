# -*- coding: utf-8 -*-
u"""
============================================================
OS PROMPTS DAS FIGURAS — o passo que faltava na esteira

⚠️ POR QUE ISTO EXISTE (pedido do Marcos, ago/2026):
   *"Gere os prompts que eu preciso, que eu gero aqui / As imagens pode me
   passar os prompts que eu gero"*.

   Ate agora o esqueleto dizia QUAIS figuras faltam (`arte.json`) e parava ai.
   Quem escrevia o prompt de cada uma era eu, na mao, uma por uma — e e
   justamente nisso que se perde a 1h30 de montar uma atividade. Pior: prompt
   escrito na hora sai diferente a cada vez, e figura irma vira figura estranha.

   Este passo fecha a esteira:

     conteudo.json ─▶ montar.py ─▶ index.html + falas.json + arte.json
                                        │
                                        └▶ prompts.py ─▶ _lote.json          (o workflow gera)
                                                      └▶ PROMPTS-IMAGENS.md  (o Marcos gera na mao)

O QUE ELE SABE FAZER, por TIPO de figura:
  · mascote parado      -> personagem inteiro, de corpo, no tema da atividade
  · mascote fala/pisca  -> NAO gera do zero: escreve o pedido de EDICAO da pose
                           parada (senao o boneco TREME — ver _qa/mascote.py)
  · crachas (cr1..crN)  -> seis criancas DIFERENTES entre si, do peito para cima
  · fundo               -> cena larga do cenario, sem personagem e sem texto
  · medalha             -> medalha com o simbolo do tema, na fita
  · figura de conteudo  -> o ASSUNTO sai do proprio conteudo.json (o rotulo que
                           acompanha a imagem naquela fase), nao de adivinhacao

⚠️ TRES REGRAS QUE JA CUSTARAM CARO E ESTAO EMBUTIDAS AQUI:
  1. `no text, no letters` em TODA figura. A IA sempre escreve letra torta, e
     em atividade de lingua a letra E o conteudo.
  2. As tres camadas do mascote saem da MESMA pose (edicao), nunca de tres
     geracoes — medido pelo `_qa/mascote.py`, que reprova acima de 15%.
  3. Peca recortavel vai em CARTELA quando for paga (ver `_qa/cartela.py`);
     por isso o `_lote.json` sai marcado `modelo: pollinations`, que e o
     caminho de R$ 0,00.

USO
    python3 _padrao/ESQUELETO/prompts.py <pasta>
    python3 _padrao/ESQUELETO/prompts.py <pasta> --so-faltando
============================================================
"""
import io
import json
import os
import re
import sys

# ------------------------------------------------------------------
# O MOLDE DA CASA — o acabamento que faz as figuras parecerem IRMAS.
# ⚠️ Mexer aqui muda TODAS as atividades novas: e a identidade visual.
# ------------------------------------------------------------------
ACABAMENTO = (
    u"Soft matte CLAY 3D illustration, handmade plasticine model photographed "
    u"in a studio, rounded chunky friendly shapes, rich saturated colours, "
    u"soft gentle shadows, smooth matte surface, children's storybook look. "
    u"Not a photograph, not flat vector. No text, no letters, no numbers, "
    u"no logo, no watermark."
)
RECORTE = (
    u"ONE single object, centered, filling the frame, isolated on a plain pure "
    u"white background, no scenery, no floor, no horizon, no other objects."
)

# tons de pele/cabelo variados: e escola publica, a crianca tem que se achar ali
CRIANCAS = [
    u"a girl with warm brown skin and dark curly hair in two puffs",
    u"a boy with deep brown skin and short black hair",
    u"a girl with light olive skin and straight black hair in a ponytail",
    u"a boy with tan skin and wavy brown hair",
    u"a girl with pale skin, freckles and red hair in a bob",
    u"a boy with medium brown skin, glasses and short curly hair",
]


def _limpa(t):
    u"""tira marcacao, entidade e as aspas-guia do esboco («assim»)."""
    t = re.sub(r"<[^>]+>", u" ", t or u"")
    t = re.sub(r"&#\d+;|&\w+;", u" ", t)
    t = t.replace(u"«", u" ").replace(u"»", u" ")
    return re.sub(r"\s+", u" ", t).strip()


def _e_exemplo(t):
    u"""o esboco nasce com texto-guia; prompt em cima dele sai sem sentido."""
    t = (t or u"").lower()
    return (not t) or (u"«" in t) or (u"o assunto" in t) or (u"exemplo" in t)


def assunto_das_figuras(c):
    u"""
    Descobre o QUE cada figura de conteudo mostra, lendo o proprio conteudo.

    ⚠️ LICAO: adivinhar pelo NOME do arquivo (`lt_campo` -> "campo") funciona
    ate a primeira palavra ambigua ("manga" e fruta ou roupa?). O rotulo que a
    crianca ve ao lado da figura ja diz, sem adivinhacao — entao e ele que
    manda, e o nome do arquivo fica so como reserva.
    """
    from montar import CHAVES_DE_FIGURA  # a MESMA constante, nunca uma copia

    achados = {}

    def anota(no):
        if not isinstance(no, dict):
            return
        nome = None
        for k in CHAVES_DE_FIGURA:
            v = no.get(k)
            if isinstance(v, str) and v:
                nome = re.sub(r"\.(png|jpg|jpeg|webp)$", u"", v)
                break
        if nome:
            for k in (u"txt", u"texto", u"rotulo", u"nome", u"lab", u"palavra",
                      u"alt", u"titulo", u"resposta"):
                r = no.get(k)
                if isinstance(r, str) and _limpa(r):
                    achados.setdefault(nome, _limpa(r))
                    break
            achados.setdefault(nome, u"")

    def anda(no):
        if isinstance(no, dict):
            anota(no)
            for v in no.values():
                anda(v)
        elif isinstance(no, list):
            for v in no:
                anda(v)

    anda(c.get(u"fases", []))
    return achados


def cenario_de(c):
    u"""
    O cenario da atividade em uma linha, para o fundo e para o tema das figuras.

    Vem do bloco `arte` do conteudo.json quando o autor escreveu; senao sai do
    titulo — que e sempre tematico ("A Oficina de Letreiros da Lina").
    """
    arte = c.get(u"arte") or {}
    cen = _limpa(arte.get(u"cenario") or u"")
    if cen and not _e_exemplo(cen):
        return cen
    tit = _limpa(c.get(u"titulo") or u"")
    return tit or u"a friendly classroom scene"


def prompts_de(c, arte):
    u"""Monta a lista [(nome, prompt, tipo)] de tudo o que falta desenhar."""
    pre = c.get(u"prefixo") or u"at"
    masc = c.get(u"mascote") or u"mascote"
    nome_masc = c.get(u"mascoteNome") or masc.capitalize()
    bloco = c.get(u"arte") or {}
    desc_masc = _limpa(bloco.get(u"mascote") or u"")
    cen = cenario_de(c)
    # ⭐ SIMBOLO DA MEDALHA (set/2026, montando a Gincana): sem isto o prompt da
    #    medalha herdava a CENA INTEIRA — "uma medalha com o simbolo de uma quadra
    #    de escola com bandeirinhas, cones, arcos, arquibancada e as montanhas do
    #    vale gravado no meio". Pedido impossivel: medalha tem um simbolo, nao uma
    #    paisagem. Agora `arte.simbolo` diz, em poucas palavras, o QUE gravar; sem
    #    ele nada muda e continua caindo na cena, como antes.
    sim = _limpa((c.get(u"arte") or {}).get(u"simbolo") or u"") or cen
    assuntos = assunto_das_figuras(c)

    if _e_exemplo(desc_masc):
        desc_masc = (u"a friendly cartoon character named %s, the guide of "
                     u"this activity about %s" % (nome_masc, cen))

    out = []
    for nome in arte.get(u"gerar", []):
        base = nome[len(pre) + 1:] if nome.startswith(pre + u"_") else nome

        # ---- as tres camadas do mascote ----
        if base == u"%s_feliz" % masc:
            out.append((nome, (
                u"%s, standing, full body, facing the viewer, smiling warmly, "
                u"mouth closed, eyes open. %s %s"
                % (desc_masc, ACABAMENTO, RECORTE)), u"mascote"))
            continue
        if base in (u"%s_fala" % masc, u"%s_pisca" % masc):
            o_que = (u"open the mouth into a rounded \"ah\" shape as if speaking"
                     if base.endswith(u"_fala")
                     else u"close the eyes into two happy curved lines, as if blinking")
            out.append((nome, (
                u"[EDICAO da pose parada — subir %s_%s_feliz.png como base]\n"
                u"Keep this exact same character, exact same pose, exact same "
                u"colours, exact same position and size in the frame. "
                u"Change ONLY the %s: %s. Do not move anything else. "
                u"Do not redraw the character."
                % (pre, masc,
                   u"mouth" if base.endswith(u"_fala") else u"eyes", o_que)),
                u"edicao"))
            continue

        # ---- os crachas ----
        m = re.match(r"cr(\d+)$", base)
        if m:
            i = (int(m.group(1)) - 1) % len(CRIANCAS)
            out.append((nome, (
                u"A friendly portrait of %s, seen from the chest up, facing the "
                u"viewer, smiling, dressed for %s. %s %s"
                % (CRIANCAS[i], cen, ACABAMENTO, RECORTE)), u"cracha"))
            continue

        # ---- o fundo (cena larga, e a unica que NAO e recortada) ----
        if base == u"fundo":
            out.append((nome, (
                u"A wide establishing shot of %s, empty, with no people and no "
                u"animals in it, seen from eye level, with plenty of calm space "
                u"in the middle for text to sit on top. %s"
                % (cen, ACABAMENTO)), u"fundo"))
            continue

        # ---- a medalha do fim ----
        if nome.startswith(u"med_"):
            out.append((nome, (
                u"A golden award medal hanging from a wide blue ribbon, with a "
                u"simple symbol of %s embossed in the middle of the medal. %s %s"
                % (sim, ACABAMENTO, RECORTE)), u"medalha"))
            continue

        # ---- figura de conteudo: o assunto vem do proprio conteudo.json ----
        assunto = assuntos.get(nome) or base.replace(u"_", u" ")
        out.append((nome, (
            u"%s, a single clear object, easy for a child to recognise at a "
            u"glance. %s %s" % (assunto, ACABAMENTO, RECORTE)), u"peca"))
    return out


def escreve(pasta, so_faltando=False):
    c = json.load(io.open(os.path.join(pasta, u"conteudo.json"), encoding=u"utf-8"))
    cam_arte = os.path.join(pasta, u"arte.json")
    if not os.path.exists(cam_arte):
        print(u"%s -> sem arte.json. Rode antes: python3 _padrao/ESQUELETO/montar.py %s"
              % (pasta, pasta))
        return 2
    arte = json.load(io.open(cam_arte, encoding=u"utf-8"))

    lista = prompts_de(c, arte)
    if so_faltando:
        img = os.path.join(pasta, u"img")
        lista = [t for t in lista
                 if not os.path.exists(os.path.join(img, t[0] + u".png"))]
    if not lista:
        print(u"%s -> nenhuma figura a pedir (todas ja estao na pasta)." % pasta)
        return 0

    # ---- 1) o lote do workflow (so o que se gera do ZERO; edicao fica de fora)
    #
    # ⚠️ LICAO PAGA DUAS VEZES, e a segunda foi o MARCOS quem viu (ago/2026):
    #    *"Não seria melhor você gerar em cartelas?"*. Este gerador nasceu
    #    pedindo UMA IMAGEM POR VEZ — a regra da cartela estava escrita no
    #    CLAUDE.md, tinha ferramenta pronta (`_padrao/cartela.py`) e portao que
    #    mede (`_qa/cartela.py`), e mesmo assim o arquivo novo saiu ignorando as
    #    tres coisas. Regra que o codigo novo nao herda nao e regra: e sorte.
    #
    #    E o custo maior nem e dinheiro. Peca gerada UMA A UMA sai com a luz e a
    #    escala daquela geracao; ao lado das outras, ela DESTOA. Foi exatamente
    #    o que aconteceu na Oficina da Lina: as tres figuras refeitas em lotes
    #    separados ficaram estranhas ao lado das primeiras. Geradas na MESMA
    #    folha, saem irmas.
    # ⚠️ O "grupo" e o TIPO, nao um rotulo unico. O agrupador do
    #    `_padrao/cartela.py` monta UMA FOLHA POR FAMILIA justamente porque a
    #    folha promete "mesma escala, mesma luz": juntar a medalha, seis
    #    retratos de crianca e o mascote numa folha so faz a IA obedecer o
    #    "mesma escala" e devolver a medalha do tamanho da crianca. Marcando
    #    tudo como "peca" eu estava pedindo esse defeito de volta.
    lote = [{u"nome": n, u"grupo": (u"cena" if t == u"fundo" else t),
             u"prompt": p, u"modelo": u"pollinations"}
            for (n, p, t) in lista if t != u"edicao"]
    cam_lote = os.path.join(pasta, u"_lote.json")
    io.open(cam_lote, u"w", encoding=u"utf-8").write(
        json.dumps(lote, ensure_ascii=False, indent=1))

    # ---- 1b) e as pecas recortaveis tambem saem AGRUPADAS EM CARTELA ----
    #      (o fundo nao entra: cena larga nao se recorta, e vai de graca)
    cartelas = []
    recortaveis = [d for d in lote if d[u"grupo"] != u"cena"]
    if len(recortaveis) >= 3:
        try:
            sys.path.insert(0, os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))))
            import cartela as _cartela                   # _padrao/cartela.py
            _cartela.plano(cam_lote)                     # escreve _lote_cartelas.json
            if os.path.exists(u"_lote_cartelas.json"):
                cartelas = json.load(io.open(u"_lote_cartelas.json",
                                             encoding=u"utf-8"))
                cam_cart = os.path.join(pasta, u"_lote_cartelas.json")
                io.open(cam_cart, u"w", encoding=u"utf-8").write(
                    json.dumps(cartelas, ensure_ascii=False, indent=1))
                os.remove(u"_lote_cartelas.json")
        except Exception as e:                                 # noqa: BLE001
            print(u"   aviso: nao consegui agrupar em cartela (%s)" % str(e)[:100])

    # ---- 2) a folha para o Marcos gerar na mao ----
    tit = _limpa(c.get(u"titulo") or pasta)
    L = []
    L.append(u"# PROMPTS DAS IMAGENS — %s" % tit)
    L.append(u"")
    L.append(u"Gerado por `_padrao/ESQUELETO/prompts.py`. Copie o bloco de cada")
    L.append(u"figura e cole no gerador. Os prompts estao em **ingles de")
    L.append(u"proposito**: os geradores entendem melhor e erram menos.")
    L.append(u"")
    L.append(u"## Como salvar")
    L.append(u"")
    L.append(u"1. **O nome do arquivo tem que ser exatamente o que esta escrito**")
    L.append(u"   (ex.: `%s.png`). Nome trocado = figura que nao aparece." % lista[0][0])
    L.append(u"2. Fundo branco liso; **PNG com fundo transparente** e melhor ainda.")
    L.append(u"3. Salvar tudo em `%s/img/`." % pasta)
    L.append(u"")
    L.append(u"> Atalho: em vez de gerar na mao, da para acionar o workflow")
    L.append(u"> `gerar-imagens.yml` com `lote=%s` e `dest=%s/img`" % (cam_lote, pasta))
    L.append(u"> — ele desenha, recorta o fundo e commita sozinho, por R$ 0,00.")
    L.append(u"")
    if cartelas:
        L.append(u"---")
        L.append(u"")
        L.append(u"# ⭐ AS PECAS VAO EM CARTELA — varias numa folha so")
        L.append(u"")
        L.append(u"Peca gerada UMA A UMA sai com a luz e a escala daquela")
        L.append(u"geracao, e ao lado das outras ela DESTOA. Na mesma folha,")
        L.append(u"saem irmas — e sao %d chamada(s) no lugar de %d."
                 % (len(cartelas), len(recortaveis)))
        L.append(u"")
        L.append(u"Salve cada folha com o nome dela (`cart_...png`) e me mande:")
        L.append(u"eu recorto cada peca com o nome certo")
        L.append(u"(`python3 _padrao/cartela.py cortar`) e monto a folha de")
        L.append(u"conferencia para o senhor olhar antes de embutir.")
        L.append(u"")
        for c in cartelas:
            L.append(u"## Folha `%s.png`" % c.get(u"nome", u"cartela"))
            L.append(u"")
            L.append(u"Vem nela: **%s**" % u", ".join(c.get(u"pecas", [])))
            L.append(u"")
            L.append(u"```")
            L.append(c.get(u"prompt", u""))
            L.append(u"```")
            L.append(u"")

    ordem = [(u"mascote", u"O MASCOTE (pose parada)"),
             (u"edicao", u"AS DUAS CAMADAS DO MASCOTE — sao EDICAO, nao desenho novo"),
             (u"cracha", u"OS CRACHAS DAS CRIANCAS"),
             (u"fundo", u"O FUNDO (cena larga)"),
             (u"medalha", u"A MEDALHA DO FIM"),
             (u"peca", u"AS FIGURAS DAS FASES (uma a uma — so se a cartela nao servir)")]
    for tipo, titulo in ordem:
        doTipo = [t for t in lista if t[2] == tipo]
        if not doTipo:
            continue
        L.append(u"---")
        L.append(u"")
        L.append(u"# %s" % titulo)
        if tipo == u"edicao":
            L.append(u"")
            L.append(u"⚠️ **Se estas duas forem geradas do zero, o mascote TREME na")
            L.append(u"tela** — o motor cruza as tres camadas umas 60 vezes por")
            L.append(u"segundo para a boca acompanhar a voz, e tres desenhos")
            L.append(u"diferentes viram tremor. No print parado nao aparece; so com")
            L.append(u"a crianca na frente. Suba a pose parada e peca a EDICAO.")
        L.append(u"")
        for (n, p, _t) in doTipo:
            L.append(u"## `%s.png`" % n)
            L.append(u"")
            L.append(u"```")
            L.append(p)
            L.append(u"```")
            L.append(u"")
    cam_md = os.path.join(pasta, u"PROMPTS-IMAGENS.md")
    io.open(cam_md, u"w", encoding=u"utf-8").write(u"\n".join(L))

    print(u"%s -> %d figura(s): %d no lote (workflow) + %d edicao(oes) do mascote"
          % (pasta, len(lista), len(lote), len(lista) - len(lote)))
    print(u"   escrito: %s" % cam_lote)
    print(u"   escrito: %s" % cam_md)
    return 0


if __name__ == u"__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    args = [a for a in sys.argv[1:] if not a.startswith(u"--")]
    if not args:
        print(u"uso: python3 _padrao/ESQUELETO/prompts.py <pasta> [--so-faltando]")
        sys.exit(2)
    sys.exit(escreve(args[0].rstrip(u"/"), u"--so-faltando" in sys.argv))
