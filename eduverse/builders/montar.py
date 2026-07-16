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
# chave/arco OPCIONAIS: mundo sem a mecanica da chave nao pode quebrar (guarda no JS gerado)
tpl=tpl.replace('var chave={x:560,y:470,got:false,bob:0};','var _chv=(MUNDO.chave||[0,0]);var chave={x:_chv[0],y:_chv[1],got:false,bob:0};')
tpl=tpl.replace('var arco={x:1150,y:340};','var _arc=(MUNDO.arco||[0,0]);var arco={x:_arc[0],y:_arc[1]};')
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
# ---- CARTELA DE POSES DO BYTE (personagem vivo): auto-incluida em TODO mundo que usa o byte.
#      Segue o id do byte do mundo (ex.: byte_pirata_costas), com chave estavel byte_<pose>. ----
if "byte" in assets:
    for pose in ["costas","lado","senta","deita","fala","feliz","frente_anda","costas_anda","frente_anda2","costas_anda2"]:
        pp=os.path.join(PROC,assets["byte"]+"_"+pose+".png")
        if os.path.exists(pp): SRCJS["byte_"+pose]="data:image/png;base64,"+b64(pp)
        else: print("(sem pose)",assets["byte"]+"_"+pose)
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
# ---- SUBTITULOS (historia mora em dados["mundo"]["historia"]; fallback = textos da floresta) ----
hist=mundo.get("historia",{}) if isinstance(mundo.get("historia",{}),dict) else {}
SUB_PC_PADRAO="use as SETAS do teclado p/ o Byte andar &#183; pegue a chave dourada &#128273; &#183; leve-a at&#233; o labirinto"
SUB_TOUCH_PADRAO="use o D-pad p/ o Byte andar &#183; pegue a chave dourada &#128273; &#183; leve-a at&#233; o labirinto"
html=html.replace("__SUB_PC__",hist.get("sub_pc",SUB_PC_PADRAO))
html=html.replace("__SUB_TOUCH__",hist.get("sub_touch",SUB_TOUCH_PADRAO))

# ---- SANIDADE FORTE: nenhum placeholder pode sobrar em lugar NENHUM do HTML ----
_sobras=re.findall(r'__[A-Z_]+__',html)
if _sobras:
    sys.exit("ERRO: placeholder nao substituido: "+", ".join(sorted(set(_sobras))))
outdir=os.path.join(REPO,"eduverse","dist",slug); os.makedirs(outdir,exist_ok=True)
out=os.path.join(outdir,"index.html"); open(out,"w",encoding="utf-8").write(html)
print("OK ->",out,"(",round(len(html)/1024),"KB ) assets:",sorted(SRCJS.keys()),"falas:",sorted(FAL.keys()))
