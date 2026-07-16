#!/usr/bin/env python3
# Build da Confeitaria: otimiza recortes -> base64, inlina app.js, gera index.html final.
import base64, io, os, re
from PIL import Image

REC="_novo/rec"
def datauri(path, kind, alt):
    im=Image.open(path)
    if kind=="jpg":
        im=im.convert("RGB")
        w,h=im.size; nw=int(w*alt/h)
        im=im.resize((nw,alt), Image.LANCZOS)
        b=io.BytesIO(); im.save(b,"JPEG",quality=82,optimize=True)
        return "data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode()
    im=im.convert("RGBA")
    w,h=im.size; nw=int(w*alt/h)
    im=im.resize((nw,alt), Image.LANCZOS)
    # quantiza p/ leveza mantendo alpha
    a=im.split()[3]
    q=im.convert("RGB").quantize(colors=64, method=Image.MEDIANCUT, dither=Image.NONE).convert("RGBA")
    q.putalpha(a)
    b=io.BytesIO(); q.save(b,"PNG",optimize=True)
    return "data:image/png;base64,"+base64.b64encode(b.getvalue()).decode()

TOK={}
TOK["capa"]=("_novo/capa.png","jpg",460)
for i in range(6): TOK["chef%d"%i]=("%s/chef-confeito_%d.png"%(REC,i),"png",240)
for i in range(8): TOK["obj%d"%i]=("%s/objetos_%d.png"%(REC,i),"png",130)
TOK["ilha0"]=("%s/ilhas_0.png"%REC,"png",200); TOK["ilha1"]=("%s/ilhas_1.png"%REC,"png",200)
TOK["ilhabolo"]=("%s/ilha_bolo.png"%REC,"png",200)
for i in (4,5,6,7,8): TOK["ilha%d"%i]=("%s/ilhas_%d.png"%(REC,i),"png",200)
for i in range(8): TOK["med%d"%i]=("%s/medalhas_%d.png"%(REC,i),"png",170)
for i in range(5): TOK["emb%d"%i]=("%s/emblemas_%d.png"%(REC,i),"png",132)
for i in range(6): TOK["selo%d"%i]=("%s/selos_%d.png"%(REC,i),"png",130)
for i in range(4): TOK["extra%d"%i]=("%s/extras_%d.png"%(REC,i),"png",210)
for i in (1,2,3): TOK["bolo%d"%i]=("%s/bolo_p%d.png"%(REC,i),"png",180)

html=open("_novo/confeitaria-app.html",encoding="utf-8").read()
js=open("_novo/app.js",encoding="utf-8").read()
# inlina app.js
html=html.replace('<script src="app.js"></script>', "<script>\n"+js+"\n</script>")

# audio (se existir _novo/audio_map.json embute; senao AUDIO_TXT={})
import json
amap="_novo/audio_map.json"
if os.path.exists(amap):
    m=json.load(open(amap))
    html=html.replace("var AUDIO_TXT={};","var AUDIO_TXT="+json.dumps(m)+";")

miss=[]
for tok,(path,kind,alt) in TOK.items():
    if not os.path.exists(path): miss.append((tok,path)); continue
    uri=datauri(path,kind,alt)
    html=html.replace("@@%s@@"%tok, uri)

# tokens nao resolvidos?
left=re.findall(r"@@[a-z0-9]+@@", html)
out="_novo/confeitaria-index.html"
open(out,"w",encoding="utf-8").write(html)
print("gerado:", out, "%.0f KB"%(len(html)/1024))
if miss: print("FALTAM arquivos:", miss)
if left: print("TOKENS nao resolvidos:", set(left))
if not miss and not left: print("OK - todos os assets embutidos")
