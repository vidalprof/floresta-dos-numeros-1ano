# -*- coding: utf-8 -*-
# EducaVerso — PORTAO DE COERENCIA (FASE D). Quando o mundo NAO e o da chave
# (historia.objetivo != "chave"), nenhum termo de OUTRO mundo pode aparecer no
# texto VISIVEL do produto. No <script>, tolera apenas fallbacks (linhas com
# "||" ou comentario) — a historia mora nos DADOS, o motor so tem o texto padrao.
import os, re, json
HERE=os.path.dirname(os.path.abspath(__file__))
REPO=os.path.abspath(os.path.join(HERE,"..",".."))
PROIBIDOS=["labirinto","chave dourada","nimbo","jaula","pedra-seta"]

def checar(slug):
    dados=json.load(open(os.path.join(REPO,"eduverse","mundos",slug,"dados.json"),encoding="utf-8"))
    dist=os.path.join(REPO,"eduverse","dist",slug,"index.html")
    if not os.path.exists(dist):
        return {"gate":"coerencia_tema","ok":False,"detalhes":"dist nao existe (rode montar.py)"}
    html=open(dist,encoding="utf-8").read()
    hist=(dados.get("mundo",{}) or {}).get("historia",{}) or {}
    objetivo=hist.get("objetivo","chave")   # sem historia declarada => mundo legado da chave
    if objetivo=="chave":
        return {"gate":"coerencia_tema","ok":True,"detalhes":"objetivo=chave (lexico da chave e nativo)"}
    # data URIs (base64) nao sao TEXTO: fora da varredura (evita falso positivo tipo "nimbo" no meio do base64)
    html=re.sub(r"data:[a-z/+.-]+;base64,[A-Za-z0-9+/=]+","data:B64",html)
    # separa VISIVEL x SCRIPT
    scripts=re.findall(r"<script>.*?</script>",html,re.S)
    visivel=re.sub(r"<script>.*?</script>","",html,flags=re.S)
    problemas=[]
    low=visivel.lower()
    for termo in PROIBIDOS:
        pos=low.find(termo)
        if pos>=0:
            trecho=visivel[max(0,pos-40):pos+len(termo)+40].replace("\n"," ")
            problemas.append("VISIVEL contem '%s': ...%s..."%(termo,trecho.strip()))
    for sc in scripts:
        for ln in sc.split("\n"):
            l=ln.lower()
            for termo in PROIBIDOS:
                if termo in l:
                    # fallback tolerado: literal apos "||" ou linha comentada
                    if "||" in ln or "/*" in ln or ln.strip().startswith("//"):
                        continue
                    problemas.append("SCRIPT (fora de fallback) contem '%s': %s"%(termo,ln.strip()[:120]))
    return {"gate":"coerencia_tema","ok":not problemas,
            "detalhes":"; ".join(problemas[:4]) if problemas else "sem termo de outro mundo"}

if __name__=="__main__":
    import sys; print(checar(sys.argv[1] if len(sys.argv)>1 else "pomar"))
