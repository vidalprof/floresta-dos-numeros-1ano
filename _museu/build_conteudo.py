# -*- coding: utf-8 -*-
import json, io, os
RAIZ="/home/user/floresta-dos-numeros-1ano"

# grupo -> (vert?, animais [(nome, img, caracteristica curta)])
G = {
 "mamiferos": (True, [("cachorro","mv_cachorro","tem pelos e mama quando bebê"),
                      ("gato","mv_gato","tem pelos e faz miau"),
                      ("morcego","mv_morcego","mamífero que voa, tem pelos"),
                      ("baleia","mv_baleia","vive no mar mas respira ar"),
                      ("onça","mv_onca","tem pelos com pintas"),
                      ("macaco","mv_macaco","tem pelos e sobe nas árvores")]),
 "aves": (True, [("tucano","mv_tucano","tem penas e um bico grande"),
                 ("arara","mv_arara","tem penas coloridas"),
                 ("coruja","mv_coruja","tem penas e voa de noite"),
                 ("pinguim","mv_pinguim","tem penas mas não voa"),
                 ("beija-flor","mv_beija_flor","tem penas e bate as asas rápido"),
                 ("galinha","mv_galinha","tem penas e bota ovos")]),
 "repteis": (True, [("jacaré","mv_jacare","tem escamas duras"),
                    ("jiboia","mv_jiboia","tem escamas duras e rasteja"),
                    ("tartaruga","mv_tartaruga","tem casco e escamas"),
                    ("lagarto","mv_lagarto","tem escamas e quatro patas"),
                    ("camaleão","mv_camaleao","tem escamas e muda de cor")]),
 "anfibios": (True, [("sapo","mv_sapo","pele úmida, vive na água e na terra"),
                     ("perereca","mv_perereca","pele lisa e pula alto"),
                     ("rã","mv_ra","pele úmida e nada bem"),
                     ("salamandra","mv_salamandra","pele lisa e rabo comprido")]),
 "peixes": (True, [("dourado","mv_dourado","tem escamas e nadadeiras"),
                   ("tubarão","mv_tubarao","peixe grande com nadadeiras"),
                   ("cavalo-marinho","mv_cavalo_marinho","peixe pequeno que fica em pé"),
                   ("peixe-palhaço","mv_peixe_palhaco","peixe laranja e branco"),
                   ("arraia","mv_arraia","peixe chato e largo")]),
 "invertebrados": (False, [("borboleta","mv_borboleta","asas coloridas, seis patas"),
                   ("joaninha","mv_joaninha","besouro vermelho com pintas"),
                   ("abelha","mv_abelha","faz mel, tem seis patas"),
                   ("aranha","mv_aranha","tece teia, oito patas"),
                   ("caracol","mv_caracol","corpo mole com concha"),
                   ("minhoca","mv_minhoca","corpo mole, vive na terra"),
                   ("caranguejo","mv_caranguejo","tem casca dura e pinças"),
                   ("polvo","mv_polvo","corpo mole com oito braços")]),
}
GNOME = {"mamiferos":"MAMÍFERO","aves":"AVE","repteis":"RÉPTIL","anfibios":"ANFÍBIO",
         "peixes":"PEIXE","invertebrados":"INVERTEBRADO"}
VERT = [a for g,(v,l) in G.items() if v for a in l]        # 26
INV  = [a for a in G["invertebrados"][1]]                    # 8
INV_IMGS = set(a[1] for a in INV)   # imgs dos invertebrados (casar por FIGURA)
TODOS = [(g,)+a for g,(v,l) in G.items() for a in l]

fases=[]
def add(**k): fases.append(k)

# ---- RAIO-X: tem esqueleto? vertebrado x invertebrado (4) ----
rx_sets=[ [("cachorro","mv_cachorro",True),("borboleta","mv_borboleta",False)],
          [("peixe-palhaço","mv_peixe_palhaco",True),("caracol","mv_caracol",False)],
          [("tucano","mv_tucano",True),("aranha","mv_aranha",False)],
          [("jacaré","mv_jacare",True),("polvo","mv_polvo",False)] ]
for i,par in enumerate(rx_sets):
    itens=[]
    for nome,img,vert in par:
        # VERTEBRADO: baixo = a chapa de esqueleto ALINHADA (mv_<bicho>_xray),
        #   e cima = o bicho tambem alinhado (mv_<bicho>_rx) para o esqueleto
        #   CASAR de tamanho e posicao quando a janelinha revela.
        # INVERTEBRADO: NAO tem esqueleto -> a janelinha nao pode revelar osso
        #   nenhum (ordem do Marcos, ago/2026: "se o animal nao tiver esqueleto
        #   nao mostre esqueleto, nao mostre nada"). baixo = chapa VAZIA
        #   transparente -> a crianca passa o raio-X e ve o vazio: e isso que
        #   ensina "nao tem osso por dentro".
        # OS DOIS usam a chapa _rx (bicho normalizado em 800x592 com margem 14%)
        # para NAO cortar na moldura arredondada (defeito que o Marcos pegou,
        # ago/2026: os invertebrados usavam a imagem-base de outra proporcao e o
        # `cover` recortava o bicho). Margem grande = extremidades longe da borda.
        cima = img+"_rx"
        baixo = (img+"_xray") if vert else "mv_vazio"
        itens.append({"k":img,"cima":cima,"baixo":baixo,"borrado":False,
            "p":"Passe o raio-X: <b>%s</b> tem osso por dentro?"%nome.upper(),
            "c":"TEM COLUNA (vertebrado)" if vert else "NÃO TEM OSSO (invertebrado)",
            "e":["NÃO TEM OSSO (invertebrado)"] if vert else ["TEM COLUNA (vertebrado)"],
            "d":["Leve a janelinha bem devagar pelo meio do bicho.",
                 ("Procure uma linha de ossos no meio das costas (a coluna)." if vert
                  else "Passe a janelinha pelo corpo todo: não aparece nenhum osso."),
                 ("Tem coluna: é VERTEBRADO." if vert else "Não tem osso por dentro: é INVERTEBRADO.")]})
    add(id="f%02d"%(len(fases)+1),mec="raios-x",selo="RAIO-X",
        enunciado="Descubra se o bicho tem <b>esqueleto por dentro</b>.",
        dica="Vertebrado tem coluna; invertebrado não tem osso.",conceito="objetivo1",dados=itens)

# ---- CLASSIFICAR vertebrado x invertebrado (2) ----
def fichas_vi(lst): return [{"img":a[1],"alvo":("vert" if (a in VERT) else "inv"),"t":a[0].upper()} for a in lst]
import random
grp2=[("vert","VERTEBRADO<br>(tem coluna)"),("inv","INVERTEBRADO<br>(não tem osso)")]
lote1=[("cachorro","mv_cachorro"),("borboleta","mv_borboleta"),("tucano","mv_tucano"),("aranha","mv_aranha"),("jacaré","mv_jacare"),("caracol","mv_caracol")]
lote2=[("baleia","mv_baleia"),("abelha","mv_abelha"),("sapo","mv_sapo"),("polvo","mv_polvo"),("dourado","mv_dourado"),("minhoca","mv_minhoca")]
lote3=[("gato","mv_gato"),("joaninha","mv_joaninha"),("coruja","mv_coruja"),("caranguejo","mv_caranguejo"),("lagarto","mv_lagarto"),("polvo","mv_polvo")]
for i,lote in enumerate([lote1,lote2,lote3]):
    # ⚠️ LIÇÃO PAGA (o Marcos: "não deixa a abelha/minhoca ir na gaveta dos
    #    invertebrados"). O destino era `("inv" if (nm,im) in INV ...)` — mas INV
    #    guarda tuplas de 3 (nome,img,caract) e `(nm,im)` tem 2 -> NUNCA batia ->
    #    TODO bicho virava "vert" e o invertebrado não entrava na gaveta certa.
    #    Casa por FIGURA (INV_IMGS), que não depende do tamanho da tupla.
    fich=[{"img":im,"alvo":("inv" if im in INV_IMGS else "vert"),"t":nm.upper()} for nm,im in lote]
    add(id="f%02d"%(len(fases)+1),mec="classificar",selo="SEPARE",
        enunciado="É <b>vertebrado</b> ou <b>invertebrado</b>? Guarde na gaveta.",
        dica="Vertebrado tem coluna (osso). Invertebrado não tem.",conceito="objetivo1",
        dados=[{"k":"vert","n":"VERTEBRADO<br>(tem coluna)","img":"mv_cachorro","voz":"vertebrado","rot":True},
               {"k":"inv","n":"INVERTEBRADO<br>(não tem osso)","img":"mv_borboleta","voz":"invertebrado","rot":True}],
        dadosExtra={"FICHAS":fich,
          "DICAS":["Pense: dá para sentir uma coluna de ossos nas costas dele?",
                   "Vertebrado tem esqueleto por dentro; invertebrado é molinho ou tem casca por fora.",
                   "Olhe a gaveta que acendeu: é ali que esta ficha mora."]})

# ---- CLASSIFICAR em grupos (4) ----
# ⚠️ A peca classificar foi desenhada para 2-3 gavetas (o comentario dela diz isso).
#    Com 5 gavetas a figura encolhia para 45px e o .bandeja estourava no celular
#    estreito (portoes encaixe+leiaute, ago/2026). Cada fase mostra 3 GRUPOS e as
#    fichas so daqueles grupos; girando os grupos, todos os grupos aparecem varias
#    vezes e a carga cognitiva por tela cai (Sweller: uma ideia de cada vez).
GNM={"mamiferos":"MAMÍFERO","aves":"AVE","repteis":"RÉPTIL","anfibios":"ANFÍBIO","peixes":"PEIXE"}
GIMG={"mamiferos":"mv_cachorro","aves":"mv_tucano","repteis":"mv_jacare","anfibios":"mv_sapo","peixes":"mv_dourado"}
# (grupos da fase, fichas: nome, img, grupo) — 3 gavetas, 4-6 fichas por fase
lotesG=[
  (["mamiferos","aves","repteis"],
   [("cachorro","mv_cachorro","mamiferos"),("tucano","mv_tucano","aves"),("jacaré","mv_jacare","repteis"),
    ("onça","mv_onca","mamiferos"),("arara","mv_arara","aves"),("jiboia","mv_jiboia","repteis")]),
  (["repteis","anfibios","peixes"],
   [("tartaruga","mv_tartaruga","repteis"),("sapo","mv_sapo","anfibios"),("dourado","mv_dourado","peixes"),
    ("camaleão","mv_camaleao","repteis"),("rã","mv_ra","anfibios"),("tubarão","mv_tubarao","peixes")]),
  (["mamiferos","aves","peixes"],
   [("morcego","mv_morcego","mamiferos"),("coruja","mv_coruja","aves"),("arraia","mv_arraia","peixes"),
    ("macaco","mv_macaco","mamiferos"),("pinguim","mv_pinguim","aves"),("cavalo-marinho","mv_cavalo_marinho","peixes")]),
  (["mamiferos","anfibios","repteis"],
   [("onça","mv_onca","mamiferos"),("perereca","mv_perereca","anfibios"),("jacaré","mv_jacare","repteis"),
    ("cachorro","mv_cachorro","mamiferos"),("salamandra","mv_salamandra","anfibios"),("jiboia","mv_jiboia","repteis")]),
]
for grps,lote in lotesG:
    fich=[{"img":im,"alvo":g,"t":nm.upper()} for nm,im,g in lote]
    add(id="f%02d"%(len(fases)+1),mec="classificar",selo="GRUPOS",
        enunciado="Cada bicho no seu <b>grupo</b>. Toque no bicho e na gaveta certa.",
        dica="Pelos→mamífero, penas→ave, escamas secas→réptil, pele úmida→anfíbio, escamas na água→peixe.",
        conceito="objetivo2",
        dados=[{"k":g,"n":GNM[g],"img":GIMG[g],"voz":GNM[g].lower(),"rot":True} for g in grps],
        dadosExtra={"FICHAS":fich,
          "DICAS":["Olhe a pele do bicho: tem pelo, pena, escama ou é úmida?",
                   "Pelos=mamífero; penas=ave; escamas secas=réptil; pele úmida=anfíbio; vive só na água com nadadeira=peixe.",
                   "A gaveta certa acendeu — toque nela."]})

# ---- DIGITAR o nome do animal (2) ----
dig1=[("mv_cachorro","CACHORRO","Mamífero que late e abana o rabo."),
      ("mv_tucano","TUCANO","Ave de bico grande e colorido."),
      ("mv_sapo","SAPO","Anfíbio de pele úmida que pula.")]
dig2=[("mv_arara","ARARA","Ave azul que fala e voa."),
      ("mv_jacare","JACARE","Réptil de escamas que vive no rio."),
      ("mv_abelha","ABELHA","Invertebrado que faz mel.")]
dig3=[("mv_tartaruga","TARTARUGA","Réptil de casco duro."),
      ("mv_coruja","CORUJA","Ave que voa de noite."),
      ("mv_gato","GATO","Mamífero que faz miau.")]
for lote in [dig1,dig2,dig3]:
    add(id="f%02d"%(len(fases)+1),mec="digitar",selo="ESCREVA",
        enunciado="Que bicho é este? <b>Escreva o nome</b>.",
        dica="Diga o nome devagar e escreva letra por letra.",conceito="objetivo3",
        dados=[{"img":im,"palavra":pal,"pista":pi,"dic":"Comece pelo primeiro som de <b>%s</b>."%pal} for im,pal,pi in lote])

# ---- LIGAR grupo x caracteristica (6) ----
lig_base=[("p0","MAMÍFERO","Tem pelos e mama quando bebê"),
          ("p1","AVE","Tem penas e bico"),
          ("p2","RÉPTIL","Tem escamas secas e rasteja"),
          ("p3","ANFÍBIO","Tem pele úmida (água e terra)"),
          ("p4","PEIXE","Vive na água, tem nadadeiras")]
lig_ex=[("p0","PELOS","Do mamífero"),("p1","PENAS","Da ave"),("p2","ESCAMAS SECAS","Do réptil"),
        ("p3","PELE ÚMIDA","Do anfíbio"),("p4","NADADEIRAS","Do peixe")]
lig_verinv=[("p0","VERTEBRADO","Tem coluna (osso por dentro)"),("p1","INVERTEBRADO","Não tem osso; é mole ou tem casca")]
# cada conjunto carrega o objetivo que ELE ensina (cobertura equilibrada):
lig_sets=[(lig_base,"objetivo2"), (lig_ex,"objetivo2"),
  ([("p0","CACHORRO","Mamífero"),("p1","TUCANO","Ave"),("p2","COBRA","Réptil"),("p3","RÃ","Anfíbio"),("p4","DOURADO","Peixe")],"objetivo3"),
  ([("p0","ABELHA","Faz mel (invertebrado)"),("p1","ARANHA","Tece teia (invertebrado)"),("p2","CARACOL","Tem concha (invertebrado)"),("p3","POLVO","Oito braços (invertebrado)")],"objetivo1"),
  ([("p0","BALEIA","Mamífero do mar"),("p1","PINGUIM","Ave que não voa"),("p2","TARTARUGA","Réptil de casco"),("p3","SALAMANDRA","Anfíbio de rabo")],"objetivo2"),
  (lig_verinv,"objetivo1")]
for s,conc in lig_sets:
    add(id="f%02d"%(len(fases)+1),mec="ligar",selo="LIGUE",
        enunciado="Ligue cada bicho/grupo à sua <b>característica</b>.",
        dica="Pense no que aquele grupo tem no corpo.",conceito=conc,
        dados=[{"k":k,"t":t,"s":s2} for k,t,s2 in s])

# ---- QUEM SOU EU? (6) ----
qse=[("MAMÍFERO",["Eu tenho <b>pelos</b> no corpo.","Quando bebê, eu <b>mamo</b> o leite da mãe.","Cachorro, gato e onça são do meu grupo."],["AVE","RÉPTIL","PEIXE"]),
     ("AVE",["Eu tenho <b>penas</b> e um <b>bico</b>.","A maioria de nós <b>voa</b>.","Eu boto <b>ovos</b> no ninho."],["MAMÍFERO","ANFÍBIO","INVERTEBRADO"]),
     ("RÉPTIL",["Eu tenho <b>escamas secas</b>.","Eu gosto de me esquentar no <b>sol</b>.","Jacaré, cobra e tartaruga são do meu grupo."],["ANFÍBIO","AVE","PEIXE"]),
     ("ANFÍBIO",["Minha pele é <b>úmida e lisa</b>.","Eu vivo na <b>água E na terra</b>.","Quando filhote (girino) eu moro na água."],["RÉPTIL","PEIXE","MAMÍFERO"]),
     ("PEIXE",["Eu tenho <b>escamas</b> e <b>nadadeiras</b>.","Eu respiro por <b>guelras</b>, dentro da água.","Eu nunca saio da água."],["ANFÍBIO","RÉPTIL","AVE"]),
     ("INVERTEBRADO",["Eu <b>não tenho osso</b> por dentro.","Alguns de nós têm <b>casca</b> por fora ou são <b>molinhos</b>.","Abelha, aranha e caracol são do meu grupo."],["MAMÍFERO","AVE","PEIXE"])]
for resp,pistas,outros in qse:
    # o enunciado tem que ser IGUAL ao balao que a peca quem-sou-eu mostra/fala
    add(id="f%02d"%(len(fases)+1),mec="quem-sou-eu",selo="QUEM SOU EU?",
        enunciado="Descubra <b>quem está falando</b>. Cada pista nova conta mais.",
        dica="Cada pista fala de uma característica do corpo.",conceito="objetivo4",
        dados=[{"resp":resp,"pistas":pistas,"outros":outros}])

# ---- INTRUSO (4) ----
intr=[("mamiferos","MAMÍFEROS",[("cachorro","mv_cachorro"),("gato","mv_gato"),("onça","mv_onca"),("tucano","mv_tucano")],"mv_tucano","TUCANO"),
      ("aves","AVES",[("arara","mv_arara"),("coruja","mv_coruja"),("galinha","mv_galinha"),("jacaré","mv_jacare")],"mv_jacare","JACARÉ"),
      ("repteis","RÉPTEIS",[("jiboia","mv_jiboia"),("lagarto","mv_lagarto"),("camaleão","mv_camaleao"),("sapo","mv_sapo")],"mv_sapo","SAPO"),
      ("invertebrados","INVERTEBRADOS",[("abelha","mv_abelha"),("aranha","mv_aranha"),("polvo","mv_polvo"),("baleia","mv_baleia")],"mv_baleia","BALEIA")]
intr_razao={"mv_tucano":"As outras três são mamíferos (têm pelos); o tucano é ave (tem penas).",
            "mv_jacare":"As outras três são aves (têm penas); o jacaré é réptil (tem escamas).",
            "mv_sapo":"As outras três são répteis (escamas secas); o sapo é anfíbio (pele úmida).",
            "mv_baleia":"As outras três são invertebrados (sem osso); a baleia é vertebrado."}
for g,selo,itens,foraimg,foranome in intr:
    fora_k=foraimg; certo=intr_razao[foraimg]
    # o enunciado tem que ser IGUAL ao 'enun' que a peca intruso mostra/fala
    add(id="f%02d"%(len(fases)+1),mec="intruso",selo="ACHE O INTRUSO",
        enunciado="Três destes são <b>%s</b>. Qual é o intruso?"%selo,
        dica="Olhe a pele e o corpo: qual é de outro grupo?",conceito="objetivo4",
        dados=[{"selo":selo,"tipo":"figura",
          "enun":"Três destes são <b>%s</b>. Qual é o intruso?"%selo,
          "itens":[{"k":im,"n":nm.upper(),"img":im} for nm,im in itens],
          "fora":fora_k,"nomeFora":foranome,
          "d1":"Pense no grupo: pelos? penas? escamas? pele úmida?",
          "d2":"Três combinam. Um é de outro grupo — procure a pele diferente.",
          "d3":"O intruso é <b>%s</b>."%foranome,
          "razoes":[{"t":certo,"ok":1},
                    {"t":"Porque ele é o maior do grupo.","ok":0},
                    {"t":"Porque ele tem uma cor diferente.","ok":0},
                    {"t":"Porque ele é o mais bonito.","ok":0}],
          "p1":"O que você olhou pode ser verdade. Mas veja as OUTRAS três: o que elas têm em comum?",
          "p2":"Cor e tamanho mudam de um bicho para outro. O que conta é o <b>grupo</b> (a pele e o corpo).",
          "p3":certo,
          "regra":certo}])

# ---- CACA-PALAVRAS (2) ----
add(id="f%02d"%(len(fases)+1),mec="caca-palavras",selo="CAÇA-PALAVRAS",
    enunciado="Ache os <b>grupos</b> dos vertebrados.",dica="Procure de pé e deitado.",conceito="objetivo2",
    dados=["MAMIFERO","AVE","REPTIL","ANFIBIO","PEIXE"])
add(id="f%02d"%(len(fases)+1),mec="caca-palavras",selo="CAÇA-PALAVRAS",
    enunciado="Ache os <b>bichos</b> escondidos.",dica="As palavras não viram de cabeça para baixo.",conceito="objetivo3",
    dados=["ABELHA","ARANHA","CARACOL","POLVO","MINHOCA"])

# ---- MEMORIA (2) ----
# ⚠️ o enunciado tem que ser IGUAL ao balao que a peca memoria mostra
#    ("Ache a palavra e o desenho que combina") — senao a voz colhida diz uma
#    coisa e a tela mostra outra (portoes 0g/0n, ago/2026).
_MEM_ENUN="Ache a <b>palavra</b> e o <b>desenho que combina</b>."
add(id="f%02d"%(len(fases)+1),mec="memoria",selo="MEMÓRIA",
    enunciado=_MEM_ENUN,dica="Vire duas e guarde onde cada uma está.",conceito="objetivo3",
    dados=[{"k":"cao","pal":"CACHORRO","fig":"mv_cachorro","sen":"mamífero","figsen":"mv_cachorro"},
           {"k":"tuc","pal":"TUCANO","fig":"mv_tucano","sen":"ave","figsen":"mv_tucano"},
           {"k":"jac","pal":"JACARÉ","fig":"mv_jacare","sen":"réptil","figsen":"mv_jacare"},
           {"k":"sap","pal":"SAPO","fig":"mv_sapo","sen":"anfíbio","figsen":"mv_sapo"}])
add(id="f%02d"%(len(fases)+1),mec="memoria",selo="MEMÓRIA",
    enunciado=_MEM_ENUN,dica="Vire duas e guarde onde cada uma está.",conceito="objetivo4",
    dados=[{"k":"abe","pal":"ABELHA","fig":"mv_abelha","sen":"invertebrado","figsen":"mv_abelha"},
           {"k":"dou","pal":"DOURADO","fig":"mv_dourado","sen":"peixe","figsen":"mv_dourado"},
           {"k":"ara","pal":"ARARA","fig":"mv_arara","sen":"ave","figsen":"mv_arara"},
           {"k":"onc","pal":"ONÇA","fig":"mv_onca","sen":"mamífero","figsen":"mv_onca"}])

# ---- VITRINE de abertura: PAREDE do museu, 6 bichos por tela (imagem + info) ----
#   todos os 34 bichos aparecem; escrito e falado (alto-falante em cada card).
# ⚠️ o artigo segue o NOME do bicho, nao o grupo: "aves" tem tucano (o tucano)
#    e arara (a arara); "repteis" tem jacaré (o) e jiboia (a). Palavra terminada
#    em -a/-ã e feminina (a arara, a jiboia, a rã); o resto, masculino (o tucano).
def artigo_de(nome):
    n=nome.lower()
    return "A" if (n.endswith("a") or n.endswith("ã")) else "O"
VIT_PANELS=[]
_ordem=["mamiferos","aves","repteis","anfibios","peixes","invertebrados"]
for _g in _ordem:
    _vert,_lst=G[_g]
    for _nome,_img,_carac in _lst:
        _caracM=_carac[0].upper()+_carac[1:]        # 2a frase da voz começa com MAIÚSCULA
        # ⚠️ LIÇÃO PAGA (o Marcos: "ele fala 'uma peixe'"). O artigo do GRUPO era
        #    escolhido por ortografia — "termina em E -> uma" — que acerta AVE
        #    (uma ave) mas ERRA PEIXE (masculino: um peixe). Gênero não se adivinha
        #    pela letra final. Agora é EXPLÍCITO: só "ave" é feminino no museu.
        _fem = {"AVE"}
        _art = "uma" if GNOME[_g] in _fem else "um"
        VIT_PANELS.append({"img":_img,"nome":_nome.upper(),"grupo":GNOME[_g],
            "info":_caracM+".",
            "voz":"%s %s é %s %s. %s."%(artigo_de(_nome), _nome, _art, GNOME[_g].lower(), _caracM)})
_VIT_ANTIGO=[
 {"img":"","nome":"OS ANIMAIS","grupo":"VERTEBRADOS e INVERTEBRADOS",
  "fatos":["Todo animal é de um tipo: VERTEBRADO tem osso por dentro (a coluna).",
           "INVERTEBRADO não tem osso: é molinho ou tem casca por fora.",
           "No museu você vai conhecer os grupos de cada um!"]},
 {"img":"mv_cachorro","nome":"OS MAMÍFEROS","grupo":"VERTEBRADO",
  "fatos":["Onde vivem: em toda parte — terra, água e até no ar.",
           "O que comem: de tudo (plantas, carne, leite quando bebês).",
           "Marca do corpo: têm PELOS e mamam quando bebês."]},
 {"img":"mv_tucano","nome":"AS AVES","grupo":"VERTEBRADO",
  "fatos":["Onde vivem: nas árvores, no chão, perto da água.",
           "O que comem: frutas, sementes, insetos.",
           "Marca do corpo: têm PENAS, bico e botam ovos."]},
 {"img":"mv_jacare","nome":"OS RÉPTEIS","grupo":"VERTEBRADO",
  "fatos":["Onde vivem: em lugares quentes, perto da água.",
           "O que comem: peixes e outros animais.",
           "Marca do corpo: têm ESCAMAS SECAS e gostam do sol."]},
 {"img":"mv_sapo","nome":"OS ANFÍBIOS","grupo":"VERTEBRADO",
  "fatos":["Onde vivem: na ÁGUA e na TERRA.",
           "O que comem: insetos e bichinhos.",
           "Marca do corpo: têm PELE ÚMIDA e lisa."]},
 {"img":"mv_dourado","nome":"OS PEIXES","grupo":"VERTEBRADO",
  "fatos":["Onde vivem: dentro da água (rios e mares).",
           "O que comem: plantas e animais menores.",
           "Marca do corpo: ESCAMAS, nadadeiras e respiram por guelras."]},
 {"img":"mv_abelha","nome":"OS INVERTEBRADOS","grupo":"NÃO TÊM OSSO",
  "fatos":["Onde vivem: em toda parte — jardins, terra, água.",
           "O que comem: plantas, néctar, restos, outros bichinhos.",
           "Marca do corpo: NÃO têm osso; muitos têm patas, antenas ou concha."]},
]
vit_fase={"id":"f00","mec":"vitrine","selo":"VITRINE","enunciado":"Conheça os grupos dos animais no museu.",
          "dica":"Toque em Próximo para ver o próximo grupo.","conceito":"objetivo2","dados":VIT_PANELS}

# ---- preenche os TEXTOS internos das pecas (tira o conteudo de EXEMPLO) ----
# ⚠️ LICAO PAGA (Museu, ago/2026): as pecas classificar/ligar/digitar EXIBEM e
#    NARRAM o `ENUN` (dadosExtra), nao o `enunciado` da fase. Se os dois divergem,
#    a voz diz uma coisa e o DADO (que o portao 0g le como "a tela") diz outra ->
#    reprova "a voz nao diz o que esta escrito". Conserto: ENUN = o proprio
#    enunciado da fase (a crianca ve e ouve a pergunta pedagogica, nao um generico).
for f in fases:
    de=f.setdefault("dadosExtra",{})
    m=f["mec"]
    if m=="classificar": de["ENUN"]=f["enunciado"]
    elif m=="ligar":
        de["ENUN"]=f["enunciado"]
        de.setdefault("FECHO","Você ligou tudo certo!")
        de.setdefault("DICAS",["Pense no que aquele grupo tem no corpo.",
                               "Pelos=mamífero, penas=ave, escamas=réptil, pele úmida=anfíbio, nadadeira=peixe.",
                               "Siga a linha que acendeu e toque na resposta certa."])
    elif m=="raios-x": de.setdefault("RXTXT","Leve a janelinha do raio-X pelo bicho e descubra se ele tem osso por dentro.")
    elif m=="digitar":
        de["ENUN"]=f["enunciado"]
        de.setdefault("FECHO","Você escreveu todos os nomes!")
    elif m=="caca-palavras":
        de.setdefault("TITULO","OS BICHOS ESCONDIDOS")

# ---- INTERCALAR: nenhuma mecanica colada (regra do motor) ----
from collections import defaultdict, deque
buckets=defaultdict(deque)
for f in fases: buckets[f["mec"]].append(f)
ordem_mec=["classificar","raios-x","quem-sou-eu","ligar","digitar","intruso","caca-palavras","memoria"]
inter=[]; ultimo=None
total=len(fases)
while len(inter)<total:
    # escolhe a mecanica com MAIS fases restantes que nao seja a ultima
    cand=[m for m in ordem_mec if buckets[m] and m!=ultimo]
    if not cand: cand=[m for m in ordem_mec if buckets[m]]  # so sobrou a ultima
    m=max(cand,key=lambda x:len(buckets[x]))
    inter.append(buckets[m].popleft()); ultimo=m
fases=[vit_fase]+inter          # a VITRINE abre a atividade (só observar/ler/ouvir)

# ---- AQUECIMENTO (revisao espacada ~40%): retoma vert/invert, o 1o conceito ----
#   pilar do Marcos: a revisao no MEIO da aula e o que faz o aprendido FICAR
#   (Roediger/Bjork). O pedagogo reconhece pelo "aquec" no id; o motor a trata
#   como fase normal. Mistura bicho de cada tipo, so para relembrar.
aquec={"id":"faquec","mec":"classificar","selo":"AQUECIMENTO","aquecimento":True,
  "enunciado":"<b>Aquecimento!</b> Lembra? É vertebrado ou invertebrado?",
  "dica":"Vertebrado tem coluna (osso). Invertebrado não tem.","conceito":"objetivo1",
  "dados":[{"k":"vert","n":"VERTEBRADO<br>(tem coluna)","img":"mv_cachorro","voz":"vertebrado","rot":True},
           {"k":"inv","n":"INVERTEBRADO<br>(não tem osso)","img":"mv_borboleta","voz":"invertebrado","rot":True}],
  "dadosExtra":{"FICHAS":[{"img":"mv_onca","alvo":"vert","t":"ONÇA"},
                          {"img":"mv_joaninha","alvo":"inv","t":"JOANINHA"},
                          {"img":"mv_arara","alvo":"vert","t":"ARARA"},
                          {"img":"mv_caracol","alvo":"inv","t":"CARACOL"}],
    "ENUN":"Toque no bicho e depois na gaveta certa.",
    "DICAS":["Pense: dá para sentir uma coluna de ossos nas costas dele?",
             "Vertebrado tem esqueleto por dentro; invertebrado é molinho ou tem casca.",
             "Olhe a gaveta que acendeu: é ali que esta ficha mora."]}}
# insere ~40%, sem colar com a mecanica dos vizinhos
pos=int(len(fases)*0.4)
while pos<len(fases) and (fases[pos-1]["mec"]=="classificar" or (pos<len(fases) and fases[pos]["mec"]=="classificar")):
    pos+=1
fases.insert(pos,aquec)

for i,f in enumerate(fases):
    f["id"]=("f%02daquec"%(i+1)) if f.get("selo")=="AQUECIMENTO" else "f%02d"%(i+1)

# ---- FALAS EXTRA (deterministicas): auto-ajuda que a PECA monta ao jogar ----
#   O colher so pegava JOGANDO as frases que o acaso disparava, e o portao 0f2
#   reprovava uma diferente a cada rodada. Aqui listamos TODAS de uma vez (a
#   chave e o mesmo chaveVoz do runtime; o montador dedup e grava). Ver CONTRATO.
falasExtra=[]
# memoria: andaime dos 3 degraus, por par (rot=pal, rot2=sen)
for _f in fases:
    if _f["mec"]=="memoria":
        for _p in _f["dados"]:
            _pal,_sen=_p.get("pal",""),_p.get("sen","")
            if _pal:
                falasExtra.append("Ouça: %s. Ache o desenho que combina."%_pal)
                falasExtra.append("Abri uma para você: %s. Ache o par dela."%_pal)
                if _sen: falasExtra.append("Vou abrir este par: %s — %s."%(_pal,_sen))
# caca-palavras: contagem + fecho (N = nº de palavras da fase)
for _f in fases:
    if _f["mec"]=="caca-palavras":
        _n=len(_f["dados"])
        for _k in range(1,_n):
            falasExtra.append("Já achou %d de %d! Faltam as outras."%(_k,_n))
        falasExtra.append("Achou as %d palavras!"%_n)
        for _w in _f["dados"]:
            falasExtra.append("A palavra é %s"%_w)   # degrau2 narra assim
# digitar: os dois degraus de andaime
if any(_f["mec"]=="digitar" for _f in fases):
    falasExtra.append("A letra que vem agora está acesa.")
    falasExtra.append("Era esta! Eu coloco e você segue.")
# classificar: a dica de "toque na ficha primeiro" (quando toca a gaveta sem ficha)
if any(_f["mec"]=="classificar" for _f in fases):
    falasExtra.append("Primeiro toque na ficha lá de cima. Depois toque na gaveta.")
# motor: a tela "Quem vai jogar?" é narrada em toda atividade
falasExtra.append("Quem vai jogar hoje?")
# tira repetidos preservando ordem
_vis=set(); falasExtra=[x for x in falasExtra if not (x in _vis or _vis.add(x))]

conteudo={
 "titulo":"O Museu Vivo dos Bichos",
 "sub":"Ciências · 3º ano · Animais vertebrados e invertebrados",
 "ano":"3º ano","prefixo":"mv","mascote":"tato","mascoteNome":"Professor Tato",
 "crachas":6,"fundo":"mv_fundo.jpg","fundoSuave":True,
 "voz":"masculina",
 "abertura":"Bem-vindo ao Museu Vivo dos Bichos! Eu sou o Professor Tato. Vamos descobrir os grupos dos animais?",
 "fim":"Você virou um cientista dos bichos! O museu ficou completo. Volte sempre!",
 "mesa":"Até o 5º ano quem manda é o PEDAGOGO, com o especialista de Ciências, roteirista, game designer, especialista em interatividade, web designer, diretor de arte, engenheiro e o PhD de testes (ver _padrao/RECEITA.md).",
 "conceitos":{
   "objetivo1":"Vertebrado ou invertebrado (tem osso por dentro?)",
   "objetivo2":"Os grupos dos vertebrados (mamífero, ave, réptil, anfíbio, peixe)",
   "objetivo3":"Reconhecer e nomear o animal",
   "objetivo4":"Dizer a que grupo o animal pertence"},
 "curriculo":{
   "objetivo1":"Características e classificação dos animais (vertebrados e invertebrados) — Currículo de Blumenau, Ciências 3º ano (Vida e evolução).",
   "objetivo2":"Comparar alguns animais e organizar grupos com base em características externas comuns — BNCC/Currículo de Blumenau, Ciências 3º ano.",
   "objetivo3":"Descrever características de plantas e animais (tamanho, forma, cor) — Currículo de Blumenau, Ciências 3º ano.",
   "objetivo4":"Comparar alguns animais e organizar grupos com base em características externas comuns — BNCC/Currículo de Blumenau, Ciências 3º ano."},
 "falasExtra":falasExtra,
 "fases":fases,
}
io.open(os.path.join(RAIZ,"_museu/conteudo.json"),"w",encoding="utf-8").write(json.dumps(conteudo,ensure_ascii=False,indent=1))
from collections import Counter
print("fases:",len(fases),"| gestos:",dict(Counter(f["mec"] for f in fases)))
