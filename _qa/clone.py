# -*- coding: utf-8 -*-
# ============================================================
#  AUDITOR DE RESTO DE CLONE — "sobrou coisa da atividade de origem?"
#
#  Nasceu da Fábrica de Brinquedos do Bento (ago/2026). Clonar o MOTOR de uma
#  atividade pronta é a regra da casa e economiza dias de trabalho — mas traz de
#  carona pedaços que são CONTEÚDO, não motor, e que passam despercebidos porque
#  o app abre bonito e não dá erro nenhum:
#
#   1. `var IMGS=[...]` (pré-carga) apontando para as imagens da atividade de
#      ORIGEM: 16 requisições 404 e nenhuma imagem própria pré-carregada. Nos PCs
#      da escola isso faz cada imagem aparecer com atraso na primeira vez.
#      (Estava assim na Fábrica E na Doceria, sem ninguém ver.)
#   2. `var VOZOK={...}` da origem: o alto-falante aparece ao lado de respostas
#      cuja voz não existe nesta pasta. Botão que não faz nada é PIOR que botão
#      nenhum — a criança toca, não acontece nada, e ela desiste de usar.
#   3. `var DOM={...}` com os conceitos da origem: o boletim do fim mostrava
#      "grupos, soma, vezes" numa atividade de 4º ano.
#   4. fala usada sem o MP3 correspondente: o mascote fica mudo naquela tela.
#
#  Uso: python3 _qa/clone.py _fabrica/index.html
# ============================================================
import os, re, sys

alvo = sys.argv[1] if len(sys.argv) > 1 else ""
if not alvo:
    print("uso: python3 _qa/clone.py <arquivo.html|pasta>")
    sys.exit(2)
pasta = alvo if os.path.isdir(alvo) else os.path.dirname(os.path.abspath(alvo))
pasta = os.path.relpath(pasta)
arq = alvo if os.path.isfile(alvo) else os.path.join(pasta, "index.html")
if not os.path.isfile(arq):
    print("%s -> sem index.html" % pasta)
    sys.exit(0)

html = open(arq, encoding="utf-8").read()
js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))
img = os.path.join(pasta, "img")
audio = os.path.join(pasta, "audio")
problemas = []

# ---- 1) pré-carga apontando para imagem que não existe aqui
m = re.search(r"var IMGS=\[(.*?)\];", js, re.S)
if m and os.path.isdir(img):
    nomes = re.findall(r'"([^"]+)"', m.group(1))
    faltam = [n for n in nomes if not os.path.exists(os.path.join(img, n + ".png"))]
    if faltam:
        problemas.append("pre-carga (var IMGS) aponta para %d imagem(ns) que NAO existem aqui: %s%s"
                         % (len(faltam), ", ".join(faltam[:5]), " ..." if len(faltam) > 5 else ""))
    elif nomes:
        print("   pre-carga: %d imagens, todas existem" % len(nomes))

# ---- 2) alto-falante prometendo voz que não existe
m = re.search(r"var VOZOK=\{(.*?)\};", js, re.S)
if m and os.path.isdir(audio):
    ks = re.findall(r'"([0-9a-z]+)"\s*:', m.group(1))
    faltam = [k for k in ks if not os.path.exists(os.path.join(audio, "op_%s.mp3" % k))]
    if faltam:
        problemas.append("alto-falante (VOZOK) promete %d voz(es) sem MP3 aqui: %s%s"
                         % (len(faltam), ", ".join(faltam[:5]), " ..." if len(faltam) > 5 else ""))
    elif ks:
        print("   alto-falante: %d vozes, todas com MP3" % len(ks))

# ---- 3) fala usada sem MP3
if os.path.isdir(audio):
    ids = set(re.findall(r'falar\("([a-z0-9_]+)"', js))
    ids |= set(re.findall(r'depoisDaFala\("([a-z0-9_]+)"', js))
    ids |= set(re.findall(r'montaBarra\("([a-z0-9_]+)"', js))
    faltam = sorted(i for i in ids if not os.path.exists(os.path.join(audio, i + ".mp3")))
    if faltam:
        problemas.append("%d fala(s) usada(s) sem MP3 (o mascote fica mudo ali): %s%s"
                         % (len(faltam), ", ".join(faltam[:5]), " ..." if len(faltam) > 5 else ""))
    elif ids:
        print("   narracao: %d falas usadas, todas com MP3" % len(ids))

# ---- 4) conceitos medidos x conceitos registrados x rotulos do boletim
m = re.search(r"var DOM=\{(.*?)\}", js, re.S)
if m:
    dom = set(re.findall(r"([a-z_]+)\s*:", m.group(1)))
    regs = set(re.findall(r'reg\("([a-z_]+)"', js))
    orfaos = sorted(regs - dom)
    mudos = sorted(dom - regs)
    if orfaos:
        problemas.append("reg() usa conceito que NAO esta no DOM (nao entra no boletim nem no relatorio): %s"
                         % ", ".join(orfaos))
    if mudos:
        problemas.append("DOM tem conceito que NENHUMA fase registra (aparece sempre zerado): %s"
                         % ", ".join(mudos))
    mr = re.search(r"var ROTCRI=\{(.*?)\};", js, re.S)
    if mr:
        rot = set(re.findall(r"([a-z_]+)\s*:", mr.group(1)))
        semrot = sorted(dom - rot)
        if semrot:
            problemas.append("conceito sem rotulo em ROTCRI (o boletim mostra o nome tecnico): %s"
                             % ", ".join(semrot))
    if not orfaos and not mudos:
        print("   medicao: %d conceitos, todos registrados por alguma fase" % len(dom))

# ---- 5) fase de arrastar sem o guarda do evento fantasma do celular
# so conta como ARRASTO se houver touchmove + fantasma/clone; o touchstart
# sozinho costuma ser o gesto secreto da medalha (segurar 2s), que nao arrasta.
temArrasto = bool(re.search(r'addEventListener\("touchmove"', js)) and \
             bool(re.search(r"cloneNode|fantasma", js))
if temArrasto:
    if not re.search(r"ultimoToque", js):
        problemas.append("tem fase de ARRASTAR sem guarda de evento fantasma do celular "
                         "(o mouse de compatibilidade desmarca a peca e o TOQUE simples nao funciona)")
    else:
        print("   arrasto: guarda de evento fantasma presente")

print("%s -> resto de clone conferido" % pasta)
if not problemas:
    print("   clone ok: nada da atividade de origem sobrou")
    sys.exit(0)
print("   %d RESTO(S) DA ATIVIDADE DE ORIGEM:" % len(problemas))
for p in problemas:
    print("    - %s" % p)
sys.exit(1)
