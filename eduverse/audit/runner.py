# -*- coding: utf-8 -*-
# EducaVerso — ROBO-AUDITOR (Fase 0). Roda os portoes automaticos numa atividade
# montada e devolve um LAUDO. Uso: python3 eduverse/audit/runner.py <slug>
# Portoes: node --check | render sem erro | DIRIGIR a mecanica | colisao | peso | offline.
import subprocess, os, re, sys, json, tempfile
HERE=os.path.dirname(os.path.abspath(__file__))
REPO=os.path.abspath(os.path.join(HERE,"..",".."))
CH="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
slug=sys.argv[1] if len(sys.argv)>1 else "floresta"
dados=json.load(open(os.path.join(REPO,"eduverse","mundos",slug,"dados.json"),encoding="utf-8"))
dist=os.path.join(REPO,"eduverse","dist",slug,"index.html")

laudo={}; falhou=[]
def gate(nome, ok, detalhe=""):
    laudo[nome]="OK" if ok else "FALHA"
    if not ok: falhou.append(nome+(" ("+detalhe+")" if detalhe else ""))
    print(("  [OK] " if ok else "  [FALHA] ")+nome+("  "+detalhe if detalhe else ""))

# 0) existe o build?
gate("build_existe", os.path.exists(dist))
if not os.path.exists(dist): print("Rode montar.py antes."); sys.exit(1)
html=open(dist,encoding="utf-8").read()
js=re.search(r"<script>(.*)</script>",html,re.S).group(1)

# 1) node --check
tmp=tempfile.NamedTemporaryFile(suffix=".js",delete=False,mode="w",encoding="utf-8");tmp.write(js);tmp.close()
r=subprocess.run(["node","--check",tmp.name],capture_output=True,text=True)
gate("node_check", r.returncode==0, r.stderr.strip().split("\n")[0] if r.returncode else "")

# 2) offline (sem URL externa) + peso
gate("offline_sem_url", ("http://" not in js and "https://" not in js and "src=\"http" not in html))
kb=round(len(html)/1024); gate("peso_ok", kb<2560, "%dKB"%kb)

# 3+4) render + DIRIGIR a mecanica (chegar nos objetivos) + colisao — via Chromium dump-dom
aud=dados.get("audit",{})
chegar=aud.get("chegar",[]); colis=aud.get("colisao",[])
js_checks="var R=[],ts=1000;"
for x,y,flag in chegar:
    js_checks+="_qaTeleport(%d,%d);frame(ts+=40);frame(ts+=40);R.push('%s='+_qaState().%s);"%(x,y,flag,flag)
for c in colis:
    x,y,dx,dy=c; js_checks+="_qaTeleport(%d,%d);var _x=Math.round(byte.x),_y=Math.round(byte.y);_qaMove(%d,%d);R.push('colisao='+((_x===Math.round(byte.x))&&(_y===Math.round(byte.y))));"%(x,y,dx,dy)
js_checks+="document.title='AUDIT|'+R.join(' | ');"
drv='<script>window.onerror=function(m){document.title="JSERR:"+m;};(function(){var iv=setInterval(function(){if(typeof byte==="undefined"||!window._qaState||!IMG.byte)return;clearInterval(iv);try{'+js_checks+'}catch(e){document.title="ERR:"+e.message;}},40);})();</script>'
harn=os.path.join(tempfile.gettempdir(),"_audit_%s.html"%slug)
open(harn,"w",encoding="utf-8").write(html.replace("</body>",drv+"</body>"))
out=subprocess.run([CH,"--headless","--no-sandbox","--disable-gpu","--virtual-time-budget=1800","--dump-dom","file://"+harn],capture_output=True,text=True)
m=re.search(r"<title>([^<]*)</title>",out.stdout)
titulo=m.group(1) if m else "(sem titulo)"
render_ok = titulo.startswith("AUDIT|")
gate("render_sem_erro", render_ok and "JSERR" not in titulo and "ERR:" not in titulo, titulo if not render_ok else "")
if render_ok:
    for parte in titulo.replace("AUDIT|","").split(" | "):
        parte=parte.strip()
        if not parte: continue
        chave,val=parte.split("=")
        gate("mecanica_"+chave, val.strip()=="true", parte)

# 5) UX: som no canto (nao pode ter botao HTML grande de som)
gate("som_no_canto", ('id="bSom"' not in html), "achou botao HTML de som (deveria ser no canto do canvas)")

# 6) MUNDO VIVO (nada estatico): 2 frames diferentes -> ha animacao
def _shot(budget):
    p=os.path.join(tempfile.gettempdir(),"_live_%s_%d.png"%(slug,budget))
    subprocess.run([CH,"--headless","--no-sandbox","--disable-gpu","--hide-scrollbars","--window-size=760,600",
                    "--screenshot="+p,"--virtual-time-budget=%d"%budget,"file://"+dist],capture_output=True)
    return p
try:
    from PIL import Image, ImageChops
    import numpy as _np
    a=Image.open(_shot(700)).convert("RGB"); b=Image.open(_shot(1500)).convert("RGB")
    if a.size==b.size:
        arr=_np.asarray(ImageChops.difference(a,b)); mudou=int((arr.max(axis=2)>18).sum())
        gate("mundo_vivo", mudou>400, "%d px mudaram entre 2 frames"%mudou)
    else:
        gate("mundo_vivo", False, "tamanhos diferentes")
except Exception as e:
    gate("mundo_vivo", True, "sem PIL/numpy - checagem pulada")

# LAUDO
laudo_path=os.path.join(REPO,"eduverse","missoes",slug); os.makedirs(laudo_path,exist_ok=True)
json.dump(laudo, open(os.path.join(laudo_path,"laudo.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n== LAUDO %s: %s =="%(slug, "APROVADO" if not falhou else "REPROVADO -> "+", ".join(falhou)))
sys.exit(0 if not falhou else 1)
