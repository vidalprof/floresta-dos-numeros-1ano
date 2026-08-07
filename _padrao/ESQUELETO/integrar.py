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


def gaveta(js):
    u"""A GAVETA DE CONTEÚDO da peça — o que faz a atividade virar dado.

    Toda peça abre com um bloco assim, e o comentário acima dele diz sempre a
    mesma frase: *"O CONTEÚDO É SÓ EXEMPLO... troque APENAS este bloco"*:

        var QZ = [ {p:"...", c:"...", e:[...], d:[...]}, ... ];

    Essa `var` é a **primeira lista/objeto declarada no topo da peça**. Achando
    o nome dela, o montador consegue trocar o conteúdo de exemplo pelo conteúdo
    de verdade (`f.dados`) **sem tocar na peça** — que é o ponto: a peça já foi
    testada, e reescrevê-la é reintroduzir os defeitos que ela custou.

    Devolve `(nome, exemplo)` — o exemplo é o valor de exemplo escrito na peça,
    que vai para o `pecas.json` e é o que responde, sem abrir 74 arquivos, à
    única pergunta que importa na hora de escrever o conteúdo: *"o que eu ponho
    em `dados` desta mecânica?"*. Devolve `(None, "")` se a peça não tiver
    gaveta (aí a fase roda com o exemplo dela e o montador avisa)."""
    m = re.search(r"^var\s+([A-Za-z_$][\w$]*)\s*=\s*[\[{]", js, re.M)
    if not m:
        return None, ""
    # até o `;` que fecha, contando colchetes — o exemplo pode ter vários níveis
    k = m.end() - 1
    p, fim = 0, len(js)
    while k < len(js):
        if js[k] in "[{":
            p += 1
        elif js[k] in "]}":
            p -= 1
            if p == 0:
                fim = k + 1
                break
        k += 1
    return m.group(1), js[m.end() - 1:fim]


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
    function mostraBanner(msg, cb){ if(typeof festa === "function") festa();
      /* ⚠️ o banner do motor e quem leva a fase seguinte: a peca so avisa que
         acabou. Se ela passar um `cb` (a tela de fim dela), ele e IGNORADO —
         no esqueleto quem manda no caminho e o motor.                        */
      setTimeout(_seguir, 420); }
    limpa();
%(corpo)s
  })();
};
'''


CSS_PONTE = u'''
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
'''


FERRAMENTAS = u'''
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
    if(typeof temVoz !== "function") return;
    var k = temVoz(txt);
    /* sem voz gravada nao inventa nada: ficar calado e melhor que falar
       outra coisa (foi esse o defeito que o Marcos cobrou tres vezes). */
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
        gav, exemplo = gaveta(js)
        # ⭐ AQUI a atividade deixa de ser código: a última linha da peça (a
        #    chamada dela mesma) vira "troque o conteúdo de exemplo pelo desta
        #    fase, DEPOIS comece". A peça não sabe de nada; nada nela mudou.
        abre = "    " + porta + "();"
        if gav:
            abre = ("    if(f && f.dados) %s = f.dados;\n" % gav) + abre
        else:
            sem_gaveta.append(nome)
        corpo = re.sub(r"^\s*%s\s*\(\s*\)\s*;\s*$" % re.escape(porta),
                       abre, js, flags=re.M)
        gavetas[nome] = {"var": gav,
                         # o exemplo cru da peça: é o molde do que vai em `dados`
                         "exemplo": (exemplo or "")[:900]}
        js_out.append(PONTE % {"nome": nome, "corpo": corpo})
        # o CSS leva a MESMA marca: o montador recorta peça inteira, nunca
        # regra a regra (um `@media{` que perdesse as regras de dentro deixaria
        # um `}` solto e derrubaria a folha inteira da atividade)
        propria = css_da_peca(html)
        if len(propria.strip()) < 40:
            # peca que nao acrescenta estilo nenhum e suspeita: quase toda
            # mecanica tem pelo menos a classe da peca dela
            sem_css.append(nome)
        css_out.append((MARCA % nome) + u"\n" + prefixa_css(propria, nome))
        prontas.append(nome)

    faltando, colidindo = confere_contra_motor(js_out)

    print(u"INTEGRACAO DAS PECAS")
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
