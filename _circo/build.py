#!/usr/bin/env python3
# Injeta as imagens base64 no template -> _circo/index.html
import base64, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img")

reps = {}
def m(token, fname):
    reps["{{" + token + "}}"] = os.path.join(IMG, fname)

m("CAPA", "capa.png")
m("M_FELIZ", "masc-feliz.png")
m("M_EXPLICA", "masc-explicando.png")
m("M_COMEMORA", "masc-comemorando.png")
m("M_PENSA", "masc-pensando.png")
m("TROFEU", "trofeu.png")
# Companheiros do circo
for k in ["leao","elefante","macaco","foca","arara","palhaco","ponei","cachorro"]:
    m("C_" + k, "comp-" + k + ".png")
# Baloes
for k in ["vermelho","azul","verde","amarelo","roxo","laranja"]:
    m("B_" + k, "bal-" + k + ".png")
# Objetos de contagem
for k in ["bola","argola","pipoca","estrela","chapeu","bandeirinha"]:
    m("O_" + k, "obj-" + k + ".png")
# Numeros
for n in range(1, 11):
    m("N_" + str(n), "num-" + str(n) + ".png")
# Formas (parada 3)
for k in ["bola","presente","chapeu","tambor","dado","bandeirinha"]:
    m("F_" + k, "form-" + k + ".png")
# Ilhas (cenario de cada parada)
for k in ["cores","numeros","formas","sombra","luzes","vogais","diferente","quebra1","memoria","erros","quebra2"]:
    m("ILHA_" + k, "ilha-" + k + ".png")
# Silhuetas (fase da sombra)
for k in ["leao","elefante","foca","macaco","arara","ponei"]:
    m("SIL_" + k, "sil-" + k + ".png")
# Figuras do ligar-pontos (Caminho das Luzes)
for k in ["cartola","gravata"]:
    m("LP_" + k, "lp-" + k + ".png")
# Imagens das vogais (Parada 6)
for k in ["ioio","urso","oculos"]:
    m("VOG_" + k, "vog-" + k + ".png")
# Letras-vogais de circo (bolha-imagem)
for L in ["A","E","I","O","U"]:
    m("VOGL_" + L, "vog-letra-" + L + ".png")
# Guloseimas de circo (Parada 7 - Qual e o Diferente)
for k in ["pipoca","algodao","maca","sorvete","pirulito","cachorro"]:
    m("GUL_" + k, "gul-" + k + ".png")
# Pecas do quebra-cabeca (Parada 8)
for k in range(4):
    m("PZ_" + str(k), "pz-" + str(k) + ".png")
# Cena dos 7 erros (Parada 10)
m("ERR_CERTA", "err-certa.png")
m("ERR_ERRADA", "err-errada.png")
# Quebra-cabeca 2 (Parada 11) - 6 pecas 2x3
for k in range(6):
    m("Q2_" + str(k), "q2-" + str(k) + ".png")
# Medalhas por parada (1..11)
for k in range(1, 12):
    m("MED_" + str(k), "med-" + str(k) + ".png")

def datauri(path):
    with open(path, "rb") as f:
        b = base64.b64encode(f.read()).decode("ascii")
    return "data:image/png;base64," + b

with open(os.path.join(BASE, "index-template.html"), "r", encoding="utf-8") as f:
    html = f.read()

faltando = []
for token, path in reps.items():
    if not os.path.exists(path):
        faltando.append((token, path))
if faltando:
    for t, p in faltando:
        print("FALTA:", t, "->", p)
    sys.exit(1)

for token, path in reps.items():
    html = html.replace(token, datauri(path))

# checa tokens nao resolvidos
import re
rest = re.findall(r"\{\{[A-Za-z0-9_]+\}\}", html)
if rest:
    print("TOKENS NAO RESOLVIDOS:", sorted(set(rest)))
    sys.exit(1)

with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)

print("OK -> _circo/index.html  (%.2f MB)" % (len(html) / 1048576.0))
