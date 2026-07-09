#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# O TESTADOR (auto-playthrough) — injeta um "robo" que JOGA a atividade sozinho:
# preenche nome, clica em Comecar, entra nas paradas, responde, avanca... e um
# capturador registra QUALQUER erro de JS em QUALQUER tela (nao so na primeira).
# No fim le o rastro de telas + os erros via --dump-dom. Tira print do estado final.
#
# Escopo honesto: ele PASSEIA e pega crashes em qualquer ponto (objetivo anti-erro).
# Nao "acerta" as respostas de proposito — clica o que faz avancar/responder.
#
# Roda AQUI (nunca no PC da escola). Uso:
#   python3 _circo/testar-jogando.py <index.html> [<index.html> ...]
import sys, os, glob, subprocess, tempfile, re, json

def achar_chrome():
    for p in sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"), reverse=True):
        return p
    for p in ("/usr/bin/chromium","/usr/bin/chromium-browser","/usr/bin/google-chrome"):
        if os.path.exists(p): return p
    return None

# Robo injetado: dirige a UI e acumula erros+rastro num <div id="__drvout"> (JSON).
DRIVER = r'''<script>(function(){
var errs=[], trace=[], steps=0, MAX=80, seen={};
function push(a,v){for(var i=0;i<a.length;i++){if(a[i]===v)return;}a.push(v);}
window.addEventListener("error",function(e){push(errs,"[ERR] "+((e&&e.message)||"erro")+" @"+((e&&e.filename)||"")+":"+((e&&e.lineno)||""));});
window.addEventListener("unhandledrejection",function(e){push(errs,"[ERR] promessa: "+((e&&e.reason)||""));});
function vista(){var el=document.getElementById("app")||document.getElementById("wrap")||document.body;var t=(el&&(el.innerText||el.textContent)||"").replace(/\s+/g," ").replace(/^\s+/,"");return t.substring(0,60);}
function preencher(){var ins=document.querySelectorAll("input");for(var i=0;i<ins.length;i++){var tp=(ins[i].type||"text").toLowerCase();if((tp==="text"||tp==="")&&!ins[i].value){ins[i].value="Teste";}}}
function visivel(b){var r=b.getBoundingClientRect();return r.width>0&&r.height>0;}
// AVANCAR/entrar/responder = bom;  VOLTAR/menu = evitar (so quando travado).
var FRENTE=/come[cç]|começ|jog|avan|pr[oó]xim|contin|iniciar|start|decolar|responder|desafio|pintar|abrirParada|abrirFase|comecarFase|renderDesafio|seguir|refor|extra/i;
var TRAS=/voltar|in[ií]cio|telaInicio|telaMapa|\bmapa\b|medalha|relat[oó]rio|imprimir/i;
var cliques={};
function chave(b){return (b.getAttribute&&b.getAttribute("onclick"))||b.className||(b.textContent||"").substring(0,20);}
function escolher(){
  var cands=[].slice.call(document.querySelectorAll("button,.btn,[onclick]")).filter(visivel);
  if(!cands.length)return null;
  var melhor=null, melhorNota=-999;
  for(var i=0;i<cands.length;i++){var b=cands[i];
    var txt=(b.textContent||"")+" "+((b.getAttribute&&b.getAttribute("onclick"))||"");
    var k=chave(b); var visto=cliques[k]?1:0;
    var nota;
    if(FRENTE.test(txt)) nota=3;        // avancar/entrar/responder
    else if(TRAS.test(txt)) nota=0;     // voltar/menu: so quando nao ha mais nada novo
    else nota=2;                        // opcao de resposta / outro clicavel
    nota -= visto*3;                    // penaliza repetir o mesmo clique
    nota -= i*0.001;                    // desempate: ordem do DOM
    if(nota>melhorNota){melhorNota=nota; melhor=b;}
  }
  if(melhor){cliques[chave(melhor)]=1;}
  return melhor;
}
function passo(){
  steps++;
  preencher();
  var v=vista(); push(trace, v);
  var el=escolher();
  if(el){try{el.click();}catch(e){push(errs,"[ERR] click: "+((e&&e.message)||""));}}
  if(steps<MAX){setTimeout(passo,120);} else {forcarNivel();setTimeout(fim,4000);} /* forca subir de nivel, espera popups auto-fecharem, dai checa */
}
function forcarNivel(){
  /* dispara o popup de subida de nivel (pra o check de overlay valer): chama as funcoes de ponto que existirem */
  var fns=["addPontos","ganharPontos","darPontos","somarPontos","levelUp","subirNivel"];
  for(var i=0;i<fns.length;i++){try{if(typeof window[fns[i]]==="function"){window[fns[i]](9999);}}catch(e){}}
}
function overlayPreso(){
  /* popup/overlay que ficou VISIVEL e NAO-VAZIO no fim (ex.: pop de nivel preso na tela) */
  if(!document.querySelectorAll||!window.getComputedStyle)return null;
  var els=document.querySelectorAll("[id*=pop],[class*=pop],[id*=overlay],[class*=overlay],[class*=modal],[class*=popup],[class*=toast]");
  for(var i=0;i<els.length;i++){var el=els[i];
    var st=getComputedStyle(el); if(!st)continue;
    if(st.display==="none"||st.visibility==="hidden"||parseFloat(st.opacity)===0)continue;
    var r=el.getBoundingClientRect(); if(r.width<40||r.height<20)continue;
    var txt=(el.textContent||"").replace(/\s+/g," ").replace(/^\s+|\s+$/g,"");
    if(txt.length>=2){return (((el.id||el.className)+"").substring(0,24))+" | "+txt.substring(0,40);}
  }
  return null;
}
function fim(){
  var out=document.createElement("div");out.id="__drvout";
  out.appendChild(document.createTextNode(JSON.stringify({erros:errs, overlay:overlayPreso(), telas:trace, passos:steps})));
  (document.documentElement||document).appendChild(out);
}
setTimeout(passo,300);
})();</script>'''

OUT = re.compile(r'<div id="__drvout">(.*?)</div>', re.S)

# Rejeicoes que sao ARTEFATO do headless (nao bug da atividade): tela cheia sem
# gesto, autoplay de audio/voz bloqueado, vibrar, etc. No PC real com o clique da
# crianca isso funciona. Filtramos para nao dar alarme falso.
BENIGNO = re.compile(
    r'Permissions check failed|fullscreen|NotAllowedError|not allowed by the user'
    r'|user gesture|permissions policy|play\(\) request|AbortError|vibrate'
    r'|speechSynthesis|The play\(\) request', re.I)

def _filtrar_benignos(erros):
    return [e for e in erros if not BENIGNO.search(str(e))]

def nome_curto(path):
    d = os.path.basename(os.path.dirname(path))
    return d if d and d not in (".","_novo","_lote") else os.path.basename(path)

def _injetar(html):
    m = re.search(r'<head[^>]*>', html, re.I)
    if m: pos = m.end()
    else:
        m = re.search(r'<html[^>]*>', html, re.I); pos = m.end() if m else 0
    return html[:pos] + DRIVER + html[pos:]

def jogar(chrome, path, shotdir):
    nome = nome_curto(path)
    shot = os.path.join(shotdir, nome + ".png")
    html = open(path, encoding="utf-8", errors="replace").read()
    tmp = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8")
    tmp.write(_injetar(html)); tmp.close()
    # budget alto: os setTimeout(120ms)*80 passos rodam rapido em tempo virtual
    cmd = [chrome,"--headless","--no-sandbox","--disable-gpu","--hide-scrollbars",
           "--virtual-time-budget=20000","--dump-dom","--screenshot="+shot,
           "--window-size=1000,750","file://"+tmp.name]
    dom = ""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        dom = r.stdout or ""
    except subprocess.TimeoutExpired:
        os.unlink(tmp.name)
        return nome, {"erros":["TIMEOUT (>120s)"],"telas":[],"passos":0}, shot
    os.unlink(tmp.name)
    m = OUT.search(dom)
    if not m:
        return nome, {"erros":["(robo nao concluiu — sem __drvout)"],"telas":[],"passos":0}, shot
    try:
        data = json.loads(m.group(1))
    except Exception as e:
        data = {"erros":["(falha ao ler saida do robo: "+str(e)+")"],"telas":[],"passos":0}
    data["erros"] = _filtrar_benignos(data.get("erros", []))
    ov = data.get("overlay")
    if ov:  # popup/overlay que ficou preso na tela = bug visual
        data["erros"].append("[OVERLAY PRESO] " + str(ov)[:120])
    return nome, data, shot

def main(args):
    if not args:
        print("uso: python3 _circo/testar-jogando.py <index.html> [...]"); return 2
    chrome = achar_chrome()
    if not chrome:
        print("!! Chromium nao encontrado."); return 3
    shotdir = tempfile.mkdtemp(prefix="testador-")
    print("Chromium:", chrome); print("Prints em:", shotdir); print()
    rc = 0
    for p in args:
        if not os.path.isfile(p):
            print("!! nao achei: " + p); continue
        nome, data, shot = jogar(chrome, p, shotdir)
        erros = data.get("erros", []); telas = data.get("telas", []); passos = data.get("passos", 0)
        if erros:
            rc = 1
            print("[ERRO] %-26s  passos=%d  telas=%d" % (nome, passos, len(telas)))
            for e in erros[:6]: print("        - " + str(e)[:180])
        else:
            print("[ OK ] %-26s  passos=%d  telas=%d  (0 erro jogando)" % (nome, passos, len(telas)))
    print("\nResultado:", "REPROVADO (erro ao jogar)" if rc else "APROVADO (0 erro jogando)")
    return rc

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
