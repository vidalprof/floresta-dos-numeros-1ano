# -*- coding: utf-8 -*-
# EducaVerso — PORTAO DE ARTE (FASE D, gates POR-DADOS deterministicos + area de jogo).
# arte_proporcao      : h declarado no dados.json vs alvo_altura_px do registro (+-25%).
# arte_fruta_ancorada : o MOTOR desenha haste + sombra pendurada p/ fruta pendurada.
# arte_area_jogo      : em viewport 500x900 o canvas ocupa >=45% da altura util.
import os, re, json, subprocess, tempfile
HERE=os.path.dirname(os.path.abspath(__file__))
REPO=os.path.abspath(os.path.join(HERE,"..",".."))
CH="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
MOTOR=os.path.join(REPO,"eduverse","motor","kit-floresta.py")
TOL=0.25  # +-25%

def _registro():
    return json.load(open(os.path.join(REPO,"eduverse","biblioteca","registro.json"),encoding="utf-8"))

def arte_proporcao(slug):
    dados=json.load(open(os.path.join(REPO,"eduverse","mundos",slug,"dados.json"),encoding="utf-8"))
    reg=_registro(); problemas=[]; vistos=0
    for prop in (dados.get("mundo",{}) or {}).get("props",[]) or []:
        tipo=prop.get("tipo"); ent=reg.get(tipo)
        if not ent or "alvo_altura_px" not in ent: continue   # sem metadado = sem cobranca
        vistos+=1
        alvo=ent["alvo_altura_px"]; h=prop.get("h")
        if h is None:
            problemas.append("%s sem h declarado"%tipo); continue
        if tipo=="cabana" and h<3*64:
            problemas.append("cabana h=%d < 3xByte (192px): desproporcional"%h); continue
        if abs(h-alvo)>TOL*alvo:
            problemas.append("%s h=%d fora de +-25%% do alvo %dpx"%(tipo,h,alvo))
    return {"gate":"arte_proporcao","ok":not problemas,
            "detalhes":"; ".join(problemas) if problemas else "%d props conferidos vs registro"%vistos}

def arte_fruta_ancorada(slug):
    src=open(MOTOR,encoding="utf-8").read()
    m=re.search(r"function desFruta\(.*?\n(?:.*\n)*?function ",src)
    corpo=""
    if m: corpo=m.group(0)
    else:
        i=src.find("function desFruta")
        corpo=src[i:i+4000] if i>=0 else ""
    tem_haste=("haste" in corpo)
    tem_sombra=("sombra pendurada" in corpo)
    faltas=[]
    if not tem_haste: faltas.append("motor sem haste ligando fruta pendurada a copa")
    if not tem_sombra: faltas.append("motor sem sombra pendurada sob a fruta")
    return {"gate":"arte_fruta_ancorada","ok":not faltas,
            "detalhes":"; ".join(faltas) if faltas else "desFruta desenha haste + sombra pendurada"}

def arte_area_jogo(slug):
    dist=os.path.join(REPO,"eduverse","dist",slug,"index.html")
    if not os.path.exists(dist):
        return {"gate":"arte_area_jogo","ok":False,"detalhes":"dist nao existe"}
    html=open(dist,encoding="utf-8").read()
    drv=('<script>window.addEventListener("load",function(){setTimeout(function(){'
         'var c=document.getElementsByTagName("canvas")[0];'
         'if(!c){document.title="AREA|semcanvas";return;}'
         'var r=c.getBoundingClientRect();'
         'document.title="AREA|"+Math.round(r.height)+"|"+window.innerHeight;},600);});</script>')
    harn=os.path.join(tempfile.gettempdir(),"_area_%s.html"%slug)
    open(harn,"w",encoding="utf-8").write(html.replace("</body>",drv+"</body>"))
    out=subprocess.run([CH,"--headless","--no-sandbox","--disable-gpu","--hide-scrollbars",
                        "--window-size=500,900","--virtual-time-budget=2500","--dump-dom",
                        "file://"+harn],capture_output=True,text=True)
    m=re.search(r"<title>AREA\|(\d+)\|(\d+)</title>",out.stdout or "")
    if not m:
        t=re.search(r"<title>([^<]*)</title>",out.stdout or "")
        return {"gate":"arte_area_jogo","ok":False,
                "detalhes":"nao mediu canvas (titulo=%s)"%(t.group(1) if t else "?")}
    ch,ih=int(m.group(1)),int(m.group(2))
    frac=ch/float(ih) if ih else 0
    return {"gate":"arte_area_jogo","ok":frac>=0.45,
            "detalhes":"canvas %dpx / viewport %dpx = %d%% da altura util"%(ch,ih,round(frac*100))}

def checar(slug):
    return [arte_proporcao(slug), arte_fruta_ancorada(slug), arte_area_jogo(slug)]

if __name__=="__main__":
    import sys
    for r in checar(sys.argv[1] if len(sys.argv)>1 else "pomar"): print(r)
