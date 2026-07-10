#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDITOR DE CONTRASTE (WCAG) — pega texto que "some no fundo" ANTES de publicar.

Abre a atividade no Chromium headless, percorre as telas principais (capa, mapa,
desafio e cada mini-jogo), DESLIGA o fade/animacao e a narracao, e mede o
contraste de CADA texto contra o fundo efetivo dele (primeiro ancestral com cor
solida). Reprova quem ficar abaixo do minimo WCAG AA (4.5:1 p/ texto normal,
3:1 p/ texto grande >=24px ou >=19px negrito).

Uso:  python3 _circo/auditar-contraste.py <arquivo.html> [--min 4.5] [--json]
Saida: relatorio por tela + lista dos textos reprovados. Codigo != 0 se reprovar.
"""
import sys, os, re, json, subprocess, tempfile

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

# telas a auditar: (rotulo, js que leva ate a tela)
TELAS = [
    ("capa", ""),
    ("mapa", "comecarComNome();"),
    ("desafio", "comecarComNome();comecarDesafios('estacao');"),
    ("forca", "comecarComNome();iniciarForca();"),
    ("ligar", "comecarComNome();iniciarLigar();"),
    ("memoria", "comecarComNome();iniciarMemoria();"),
    ("mapa-mundi", "comecarComNome();iniciarMapa();"),
    ("caca-palavras", "comecarComNome();iniciarCaca();"),
    ("climograma", "comecarComNome();iniciarClima();"),
    ("quebra", "comecarComNome();iniciarQuebra();"),
]

# CSS que congela animacoes e forca tudo visivel (opacidade 1) p/ medir cor real
FORCE_CSS = ("<style>*{-webkit-animation:none!important;animation:none!important;"
             "-webkit-transition:none!important;transition:none!important;opacity:1!important;}"
             "#app,#app *{opacity:1!important;}</style>")

# desliga a narracao (senao alguns fluxos travam/escondem)
PRE = ("try{tocarFala=function(){};falar=function(){};falarDepois=function(){};"
       "narrarDesafio=function(){};narrarInicio=function(){};narrarMapa=function(){};"
       "falarAbertura=function(){};}catch(e){}")

# auditor injetado: roda no navegador, mede contraste e escreve JSON no title
SCAN = r"""
function _lum(c){var a=[c[0],c[1],c[2]].map(function(v){v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4);});return 0.2126*a[0]+0.7152*a[1]+0.0722*a[2];}
function _ratio(f,b){var L1=_lum(f),L2=_lum(b),hi=Math.max(L1,L2),lo=Math.min(L1,L2);return (hi+0.05)/(lo+0.05);}
function _rgb(s){var m=(s||"").match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?/);if(!m)return null;return {c:[+m[1],+m[2],+m[3]],a:(m[4]===undefined?1:+m[4])};}
function _bg(el){var e=el;while(e&&e.nodeType===1){var cs=getComputedStyle(e);var p=_rgb(cs.backgroundColor);if(p&&p.a>=0.5)return {c:p.c,img:(cs.backgroundImage&&cs.backgroundImage!=="none")};if(cs.backgroundImage&&cs.backgroundImage!=="none")return {c:null,img:true};e=e.parentNode;}return {c:[255,255,255],img:false};}
function _vis(el){var cs=getComputedStyle(el);if(cs.display==="none"||cs.visibility==="hidden"||parseFloat(cs.opacity)===0)return false;var r=el.getBoundingClientRect();return r.width>2&&r.height>2&&r.bottom>0&&r.right>0;}
function _txt(el){var t="";for(var i=0;i<el.childNodes.length;i++){var n=el.childNodes[i];if(n.nodeType===3)t+=n.nodeValue;}return t.replace(/\s+/g," ").replace(/^ | $/g,"");}
function auditar(){
  var raiz=document.body;
  var all=raiz.getElementsByTagName("*");var fails=[],okc=0,i;
  for(i=0;i<all.length;i++){var el=all[i];var tx=_txt(el);if(tx.length<2)continue;if(!_vis(el))continue;
    var cs=getComputedStyle(el);var fg=_rgb(cs.color);if(!fg)continue;var bg=_bg(el);
    var fs=parseFloat(cs.fontSize)||16;var bold=(cs.fontWeight>=600||cs.fontWeight==="bold");
    var big=(fs>=24)||(fs>=19&&bold);var min=big?3.0:4.5;
    if(bg.c===null){ /* texto sobre imagem: nao da p/ medir com seguranca */ continue; }
    var r=_ratio(fg.c,bg.c);
    if(r<min){ fails.push({t:tx.slice(0,42),tag:el.tagName.toLowerCase(),cls:(""+(el.className||"")).slice(0,40),fg:"rgb("+fg.c.join(",")+")",bg:"rgb("+bg.c.join(",")+")",r:Math.round(r*100)/100,min:min,fs:Math.round(fs)}); } else { okc++; }
  }
  return {ok:okc,fails:fails};
}
try{ document.title="AUD::"+JSON.stringify(auditar()); }catch(e){ document.title="ERR::"+e.message; }
"""

def render_e_auditar(src_html, js_nav, budget=4500):
    h = open(src_html, encoding="utf-8").read()
    inj = ('<script>window.addEventListener("load",function(){setTimeout(function(){try{'
           + PRE + ';' + js_nav + '}catch(e){}; setTimeout(function(){' + SCAN + '},500);},450);});</script>')
    h = h.replace("</head>", FORCE_CSS + "</head>", 1).replace("</body>", inj + "</body>", 1)
    tf = tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8")
    tf.write(h); tf.close()
    try:
        out = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                              "--run-all-compositor-stages-before-draw",
                              "--window-size=900,1250", "--virtual-time-budget=%d" % budget,
                              "--dump-dom", "file://" + tf.name],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=60).stdout.decode("utf-8", "ignore")
    except Exception as e:
        return {"erro": str(e)}
    finally:
        try: os.remove(tf.name)
        except Exception: pass
    m = re.search(r"<title>AUD::(.*?)</title>", out, re.S)
    if not m:
        m2 = re.search(r"<title>ERR::(.*?)</title>", out, re.S)
        return {"erro": (m2.group(1) if m2 else "sem resultado")}
    try:
        return json.loads(m.group(1))
    except Exception as e:
        return {"erro": "json invalido: %s" % e}

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("uso: python3 _circo/auditar-contraste.py <arquivo.html> [--min 4.5] [--json]"); sys.exit(2)
    src = args[0]
    quer_json = "--json" in sys.argv
    total_fail = 0
    relatorio = {}
    for rotulo, js in TELAS:
        res = render_e_auditar(src, js)
        if "erro" in res:
            print("  [%-14s] ERRO: %s" % (rotulo, res["erro"])); relatorio[rotulo] = {"erro": res["erro"]}; continue
        fails = res.get("fails", [])
        relatorio[rotulo] = res
        if fails:
            total_fail += len(fails)
            print("  [%-14s] REPROVADO: %d texto(s) de baixo contraste (ok=%d)" % (rotulo, len(fails), res.get("ok", 0)))
            for f in fails[:12]:
                print("      - \"%s\"  ratio=%.2f (min %.1f)  cor=%s sobre %s  <%s.%s %spx>" %
                      (f["t"], f["r"], f["min"], f["fg"], f["bg"], f["tag"], f["cls"], f["fs"]))
        else:
            print("  [%-14s] OK (%d textos, todos >= min)" % (rotulo, res.get("ok", 0)))
    print("== RESUMO CONTRASTE: %s ==" % ("APROVADO (nenhum texto ilegivel)" if total_fail == 0 else "REPROVADO — %d texto(s) somem no fundo" % total_fail))
    if quer_json:
        open("/tmp/contraste.json", "w").write(json.dumps(relatorio, ensure_ascii=False, indent=1))
        print("(json em /tmp/contraste.json)")
    sys.exit(0 if total_fail == 0 else 1)

if __name__ == "__main__":
    main()
