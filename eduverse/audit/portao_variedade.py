# -*- coding: utf-8 -*-
# EducaVerso — PORTAO DE VARIEDADE (FASE D). NPC nunca repete a mesma linha:
# variedade_npc      : NPC com "fala" string unica (sem falas[]) = FALHA; falas[]<2 = FALHA.
# variedade_contagem : mecanica contar precisa de n1..nMax nos dados E dos audios no dist.
import os, json
HERE=os.path.dirname(os.path.abspath(__file__))
REPO=os.path.abspath(os.path.join(HERE,"..",".."))

def _dados(slug):
    return json.load(open(os.path.join(REPO,"eduverse","mundos",slug,"dados.json"),encoding="utf-8"))

def variedade_npc(slug):
    dados=_dados(slug); problemas=[]
    for npc in (dados.get("mundo",{}) or {}).get("npcs",[]) or []:
        nome=npc.get("nome") or npc.get("sprite") or "?"
        falas=npc.get("falas")
        tem_fala_str=isinstance(npc.get("fala"),str)
        if falas is None and not tem_fala_str:
            continue   # NPC decorativo (sem fala) e permitido
        if tem_fala_str and not isinstance(falas,list):
            problemas.append("NPC %s tem 'fala' string unica (repetitivo): exige falas[]"%nome); continue
        if not isinstance(falas,list) or len(falas)<2:
            problemas.append("NPC %s tem falas[] com <2 itens"%nome)
    return {"gate":"variedade_npc","ok":not problemas,
            "detalhes":"; ".join(problemas) if problemas else "todo NPC falante tem falas[] variado"}

def variedade_contagem(slug):
    dados=_dados(slug)
    aula=(dados.get("mundo",{}) or {}).get("aula",{}) or {}
    rounds=aula.get("rounds",[]) or []
    conta=[r for r in rounds if r.get("tipo")=="contar"]
    if not conta:
        return {"gate":"variedade_contagem","ok":True,"detalhes":"sem mecanica contar (nao se aplica)"}
    maior=max((r.get("n",0) for r in rounds), default=0)
    falas=set(str(f) for f in dados.get("falas",[]) or [])
    faltam=[("n%d"%i) for i in range(1,maior+1) if ("n%d"%i) not in falas]
    if faltam:
        return {"gate":"variedade_contagem","ok":False,
                "detalhes":"faltam falas de contagem nos dados: "+", ".join(faltam[:8])}
    dist=os.path.join(REPO,"eduverse","dist",slug,"index.html")
    if not os.path.exists(dist):
        return {"gate":"variedade_contagem","ok":False,"detalhes":"dist nao existe"}
    html=open(dist,encoding="utf-8").read()
    n_audio=html.count("data:audio/mpeg")
    n_falas=len(dados.get("falas",[]) or [])
    ok=n_audio>=n_falas
    return {"gate":"variedade_contagem","ok":ok,
            "detalhes":"dist embute %d audios p/ %d falas do dado (cobertura %s)"%(n_audio,n_falas,"OK" if ok else "INCOMPLETA")}

def checar(slug):
    return [variedade_npc(slug), variedade_contagem(slug)]

if __name__=="__main__":
    import sys
    for r in checar(sys.argv[1] if len(sys.argv)>1 else "pomar"): print(r)
