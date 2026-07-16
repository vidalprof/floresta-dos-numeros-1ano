# -*- coding: utf-8 -*-
# EducaVerso — MONTADOR GENERICO (Fase 0): dados + biblioteca + motor -> HTML autossuficiente.
# Uso: python3 eduverse/builders/montar.py <slug>   (default: floresta)
# A ATIVIDADE eh DADO (eduverse/mundos/<slug>/dados.json). O motor (kit) eh reutilizavel.
import base64, os, json, re, sys
HERE=os.path.dirname(os.path.abspath(__file__))
REPO=os.path.abspath(os.path.join(HERE,"..",".."))
ENGINE=os.path.join(REPO,"eduverse","motor","kit-floresta.py")   # motor reutilizavel
PROC=os.path.join(REPO,"eduverse","biblioteca","proc")           # biblioteca LEGO
AUDIO=os.path.join(REPO,"_audio")                                # vozes geradas
def b64(p):
    with open(p,"rb") as f: return base64.b64encode(f.read()).decode()

slug=sys.argv[1] if len(sys.argv)>1 else "floresta"
dados=json.load(open(os.path.join(REPO,"eduverse","mundos",slug,"dados.json"),encoding="utf-8"))
tema=dados["tema"]; mundo=dados["mundo"]; assets=dict(dados["assets"])
if not tema.get("borboletas",True): assets.pop("borboleta",None)

# ---- MOTOR: extrai o template do kit e troca o conteudo FIXO por leitura de MUNDO (data-driven) ----
src=open(ENGINE,encoding="utf-8").read()
tpl=re.search(r'HTML=r"""(.*?)"""',src,re.S).group(1)
tpl=tpl.replace('var SRC=__SRC_JSON__, FALAS=__FALAS_JSON__, TEMA=__THEME_JS__;',
                'var SRC=__SRC_JSON__, FALAS=__FALAS_JSON__, TEMA=__THEME_JS__, MUNDO=__MUNDO_JS__;')
tpl=tpl.replace('var WW=1500,WH=1050;','var WW=MUNDO.WW,WH=MUNDO.WH;')
tpl=tpl.replace('var byte={x:250,y:860,dir:1,resp:0,passo:0,mov:false,r:18};',
                'var byte={x:MUNDO.start[0],y:MUNDO.start[1],dir:1,resp:0,passo:0,mov:false,r:18};')
tpl=tpl.replace('var chave={x:560,y:470,got:false,bob:0};','var chave={x:MUNDO.chave[0],y:MUNDO.chave[1],got:false,bob:0};')
tpl=tpl.replace('var arco={x:1150,y:340};','var arco={x:MUNDO.arco[0],y:MUNDO.arco[1]};')
tpl=tpl.replace('var PATH=[[250,860],[380,740],[300,600],[510,510],[690,560],[840,470],[1010,450],[1150,400]];','var PATH=MUNDO.path;')
tpl=re.sub(r'var TREES=\[\[120,520\].*?\[400,640\]\];','var TREES=MUNDO.trees;',tpl,flags=re.S)
tpl=tpl.replace('var TR=16; // raio tronco','var TR=MUNDO.tr;')
tpl=tpl.replace('var FLORES=[[420,800],[300,690],[560,560],[700,470],[860,520],[1000,430],[1120,330],[240,820],[640,640],[900,700]];','var FLORES=MUNDO.flores;')

# ---- ASSETS (so os ids da atividade) ----
SRCJS={}
for key,idn in assets.items():
    p=os.path.join(PROC,idn+".png")
    if os.path.exists(p): SRCJS[key]="data:image/png;base64,"+b64(p)
    else: print("!! falta asset:",idn)
# ---- FALAS (voz gerada) ----
FAL={}
for idn in dados.get("falas",[]):
    p=os.path.join(AUDIO,idn+".mp3")
    if os.path.exists(p): FAL[idn]="data:audio/mpeg;base64,"+b64(p)
    else: print("(sem audio)",idn)

THEMEJS=json.dumps({"part":tema["part"],"ceu0":tema["ceu0"],"ceu1":tema["ceu1"],
                    "passaros":tema["passaros"],"borboletas":tema["borboletas"]})
html=tpl.replace("__SRC_JSON__",json.dumps(SRCJS)).replace("__FALAS_JSON__",json.dumps(FAL))
html=html.replace("__THEME_JS__",THEMEJS).replace("__MUNDO_JS__",json.dumps(mundo))
html=html.replace("__TITULO__",tema["titulo"]).replace("__EMOJI__",tema["emoji"])

outdir=os.path.join(REPO,"eduverse","dist",slug); os.makedirs(outdir,exist_ok=True)
out=os.path.join(outdir,"index.html"); open(out,"w",encoding="utf-8").write(html)
if "__" in html.split("<script>")[1][:400]:  # sanidade: sobrou placeholder?
    print("!! ATENCAO: placeholder nao substituido")
print("OK ->",out,"(",round(len(html)/1024),"KB ) assets:",sorted(SRCJS.keys()),"falas:",sorted(FAL.keys()))
