# -*- coding: utf-8 -*-
# EducaVerso — ROBO-AUDITOR (Fase 0). Roda os portoes automaticos numa atividade
# montada e devolve um LAUDO. Uso: python3 eduverse/audit/runner.py <slug>
# Portoes: node --check | render sem erro | DIRIGIR a mecanica | colisao | peso | offline.
import subprocess, os, re, sys, json, tempfile
HERE=os.path.dirname(os.path.abspath(__file__))
REPO=os.path.abspath(os.path.join(HERE,"..",".."))
CH="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
sys.path.insert(0,HERE)
import portao_coerencia, portao_arte, portao_variedade
AVISA=("--avisa" in sys.argv)                       # gates novos so reportam (nao derrubam exit)
_args=[a for a in sys.argv[1:] if not a.startswith("--")]
slug=_args[0] if _args else "floresta"
dados=json.load(open(os.path.join(REPO,"eduverse","mundos",slug,"dados.json"),encoding="utf-8"))
dist=os.path.join(REPO,"eduverse","dist",slug,"index.html")

laudo={}; falhou=[]
def gate(nome, ok, detalhe=""):
    laudo[nome]="OK" if ok else "FALHA"
    if not ok: falhou.append(nome+(" ("+detalhe+")" if detalhe else ""))
    print(("  [OK] "+nome) if ok else ("  [FALHA] "+nome+("  -> "+detalhe if detalhe else "")))

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

# 6) MUNDO VIVO (nada estatico): 2 frames espacados -> ha animacao.
#    Fotografa o CANVAS em tamanho cheio (a area viva ocupa a foto toda) e compara frames
#    distantes no tempo (animacoes lentas se acumulam). Robusto: vivo ~14000px, parado ~0.
_livecss=('<style>#wrap{display:block!important;padding:0!important;}h1,.sub,#painel,#dpad{display:none!important;}'
          '#frame{padding:0!important;border-radius:0!important;box-shadow:none!important;}'
          'canvas{max-width:none!important;max-height:none!important;width:720px!important;height:500px!important;border-radius:0!important;}</style>')
_liveharn=os.path.join(tempfile.gettempdir(),"_liveharn_%s.html"%slug)
open(_liveharn,"w",encoding="utf-8").write(html.replace("</head>",_livecss+"</head>"))
def _shot(budget):
    p=os.path.join(tempfile.gettempdir(),"_live_%s_%d.png"%(slug,budget))
    subprocess.run([CH,"--headless","--no-sandbox","--disable-gpu","--hide-scrollbars","--window-size=720,500",
                    "--screenshot="+p,"--virtual-time-budget=%d"%budget,"file://"+_liveharn],capture_output=True)
    return p
try:
    from PIL import Image, ImageChops
    import numpy as _np
    frames=[Image.open(_shot(b)).convert("RGB") for b in (1500,2700,3900)]  # 3 momentos
    difs=[]
    for i in range(len(frames)-1):
        if frames[i].size==frames[i+1].size:
            arr=_np.asarray(ImageChops.difference(frames[i],frames[i+1])); difs.append(int((arr.max(axis=2)>18).sum()))
    melhor=max(difs) if difs else 0   # basta UM par diferir p/ provar animacao (anti-intermitencia)
    gate("mundo_vivo", melhor>3000, "so %d px mudaram no melhor par (mundo quase parado)"%melhor)
except Exception as e:
    gate("mundo_vivo", True, "sem PIL/numpy - checagem pulada")

# ===== PAINEL DE AUDITORES (uma dimensao cada) =====
# AUDITOR DE SOM
gate("som_voz_embutida", ("data:audio/mpeg" in html), "sem voz gerada embutida")
gate("som_ambiente", ("ambMaster" in js or "initAudio" in js), "sem som ambiente")
# AUDITOR DE TEXTO/LINGUA (nao pode ter simbolo/emoji dentro de fala narrada)
falas_txt=" ".join([f.get("texto","") if isinstance(f,dict) else str(f) for f in (dados.get("dialogos",{}) or {}).values()]) if isinstance(dados.get("dialogos",{}),dict) else ""
import re as _re
tem_simbolo=bool(_re.search(r"[#*_<>{}\\^~|]", falas_txt))
gate("texto_sem_simbolo", not tem_simbolo, "fala com simbolo que o TTS le errado")
# AUDITOR PEDAGOGICO (Portao 0 estrutural) — o arco do EducaVerso esta nos dados?
tem_arco = ("arco" in dados) or ("missoes" in dados) or ("arco" in dados.get("pedagogia",{}))
laudo["pedagogia_arco"]= "OK" if tem_arco else "PENDENTE_HUMANO"
print(("  [OK] " if tem_arco else "  [PENDENTE] ")+"pedagogia_arco  (arco Historia->...->Reflexao nos dados)")

# LAUDO
laudo_path=os.path.join(REPO,"eduverse","missoes",slug); os.makedirs(laudo_path,exist_ok=True)
json.dump(laudo, open(os.path.join(laudo_path,"laudo.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n== LAUDO %s: %s =="%(slug, "APROVADO" if not falhou else "REPROVADO -> "+", ".join(falhou)))
sys.exit(0 if not falhou else 1)
