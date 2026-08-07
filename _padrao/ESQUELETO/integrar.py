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


def regras(css):
    u"""quebra a folha em regras (seletor, corpo) — inclusive dentro de @media."""
    fora, media = [], ""
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
    para o escolhido poder ser conferido, em vez de acreditado."""
    achados = []
    for m in re.finditer(r"^var\s+([A-Za-z_$][\w$]*)\s*=\s*([\[{])", js, re.M):
        if m.group(1) in NAO_E_CONTEUDO:
            continue
        i = m.end() - 1
        achados.append((m.group(1), i, _ate_o_fim(js, i), m.group(2)))
    # ⚠️ so MAIUSCULA e conteudo. A convencao da casa em todas as pecas: dado
    #    que a crianca ve nasce em CAIXA ALTA (`PARES`, `CENA_A`, `RODADAS`), e
    #    o estado do jogo em minuscula (`cels`, `vagas`, `sombras`). Sem este
    #    corte, o autor do conteudo receberia uma lista com o estado interno da
    #    peca no meio — e mexer nele nao e trocar conteudo, e quebrar a peca.
    todas = [a[0] for a in achados if a[0].upper() == a[0]]
    # o exemplo de CADA gaveta, nao so o da principal: e o que permite conferir
    # o formato do `dadosExtra` (foi por falta disso que um `MUDA` no formato
    # errado passou e a fase saiu com ZERO diferencas, dando-se por concluida)
    exemplos = dict((n, js[i:f]) for n, i, f, _t in achados if n.upper() == n)
    if not achados:
        return None, "", "nenhuma", [], {}

    marca = re.search(r"troque APENAS|CONTE[UÚ]DO [EÉ] S[OÓ] EXEMPLO", js, re.I)
    if marca:
        for nome, i, f, _t in achados:
            if i > marca.start():
                return nome, js[i:f], "marca na peca", todas, exemplos
    for nome, i, f, t in achados:
        if t == "[":
            return nome, js[i:f], "primeiro vetor", todas, exemplos
    nome, i, f, _t = achados[0]
    return nome, js[i:f], "primeiro objeto", todas, exemplos


def prefixa_css(css, nome):
    u"""`.opt{...}` vira `.mec-escolher .opt{...}` — duas peças não brigam."""
    fora = []
    for bloco in re.split(r"(@media[^{]*\{)", css):
        fora.append(bloco)
    saida, dentro_media = [], 0
    for pedaco in re.finditer(r"([^{}]+)(\{[^{}]*\})|(@media[^{]*\{)|(\})", css, re.S):
        sel, corpo, media, fecha = pedaco.groups()
        if media:
            saida.append(media); dentro_media += 1
        elif fecha:
            saida.append("}"); dentro_media = max(0, dentro_media - 1)
        elif sel is not None:
            s = sel.strip()
            if not s or s.startswith("@") or s.startswith("/*"):
                saida.append(sel + (corpo or ""))
                continue
            novo = ", ".join(
                (".mec-%s %s" % (nome, x.strip())) if not x.strip().startswith("@") else x
                for x in s.split(","))
            saida.append("\n" + novo + (corpo or ""))
    return "".join(saida)


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
      if(typeof window.mostraBanner === "function"){
        window.mostraBanner(msg || "Muito bem!", _seguir); return;
      }
      setTimeout(_seguir, 420);
    }
    limpa();
%(corpo)s
  })();
};
'''


CSS_PONTE = u'''
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
.centro .pecabox .opt,.centro .pecabox .pc,.centro .pecabox .ficha,.centro .pecabox .cx{
  background:rgba(255,253,246,.96);border:2px solid #e6dcc6;border-bottom-width:5px;
  border-radius:18px;color:#3a3020;font-weight:600;
  -webkit-box-shadow:0 5px 12px rgba(30,50,20,.16);box-shadow:0 5px 12px rgba(30,50,20,.16)}
.centro .pecabox .opt.ok,.centro .pecabox .pc.ok{border-color:#5bbf3a;background:#eafce0}
.centro .pecabox .opt.no{border-color:#ff7a6b;background:#fff0ee}
.centro .pecabox .balao{background:rgba(255,253,246,.95);border:0;border-radius:22px;
  padding:13px 18px;font-size:17px;font-weight:600;line-height:1.35;
  -webkit-box-shadow:0 6px 18px rgba(30,50,20,.22);box-shadow:0 6px 18px rgba(30,50,20,.22)}
.centro .pecabox .selo{background:#7d3fe0;color:#fff;font-size:13px;font-weight:700;
  padding:5px 12px;border-radius:999px}
.centro .pecabox .zap{width:30px;height:30px;border-radius:50%;background:rgba(58,48,32,.09);
  border:0;opacity:.62;padding:0}
.centro .pecabox .hint{color:#fffdf6;background:rgba(58,48,32,.55);border-radius:999px;
  padding:6px 14px;display:inline-block;font-size:14px}

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
(function(){
  if(!window.speechSynthesis) return;
  var vazio = function(){};
  try{
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak = vazio;
    window.speechSynthesis.cancel = vazio;
  }catch(e){}
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
    if(k && typeof falaDaTela === "function") falaDaTela(k);
  }
  if(window.MutationObserver){
    var alvo = document.getElementById("app");
    if(alvo) new MutationObserver(function(){ setTimeout(olha, 70); })
      .observe(alvo, {childList:true, subtree:true, characterData:true});
  }
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
    zap fone tocando""".split())
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
    gavetas = {}
    _do_motor = classes_do_motor()
    _siglas = set()
    renomeadas = {}
    js_out, css_out = [], []

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
        gav, exemplo, regra, todas, exemplos = gaveta(js)
        # ⭐ AQUI a atividade deixa de ser código: a última linha da peça (a
        #    chamada dela mesma) vira "troque o conteúdo de exemplo pelo desta
        #    fase, DEPOIS comece". A peça não sabe de nada; nada nela mudou.
        abre = "    " + porta + "();"
        if gav:
            linhas = ["    if(f && f.dados) %s = f.dados;" % gav]
            outras = [v for v in todas if v != gav]
            if outras:
                # ⚠️ as OUTRAS gavetas desta peca: o `sete-erros` guarda a cena
                #    em CENA_A e os erros em MUDA. Sem isto, a fase saia com a
                #    cena da atividade e os erros do exemplo — sem erro nenhum.
                linhas.append("    if(f && f.dadosExtra){ var _d = f.dadosExtra;")
                for v in outras:
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
        css_out.append((MARCA % nome) + u"\n" + prefixa_css(propria, nome))
        prontas.append(nome)

    faltando, colidindo = confere_contra_motor(js_out)
    vazam = classes_que_vazam(css_out)

    print(u"INTEGRACAO DAS PECAS")
    if renomeadas:
        _n = sum(len(v[1]) for v in renomeadas.values())
        print(u"  🔒 %d classe(s) renomeada(s) em %d peca(s) — a porta da colisao "
              u"com o motor esta FECHADA" % (_n, len(renomeadas)))
    print(u"  %d peca(s) com porta de entrada -> viram MEC[...]" % len(prontas))
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
