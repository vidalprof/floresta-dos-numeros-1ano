# -*- coding: utf-8 -*-
u"""
============================================================
 OS MAPAS DA PROVA — desenhados AQUI, em SVG, e não buscados na internet.

 ⚠️ POR QUE NÃO FOTO DE MAPA (decisão, set/2026). O Marcos disse "pode encontrar
    o material e ilustrações na internet". Para as FOTOS de paisagem isso vale, e
    a prova usa as fotos reais que a Expedição Santa Catarina já trouxe. Para os
    MAPAS, não:
      · mapa achado na internet vem com licença desconhecida e, pior, com dado
        que eu não tenho como conferir — e mapa errado numa prova de cartografia
        ensina errado exatamente onde a criança está aprendendo a confiar no mapa;
      · imagem de mapa é texto pequeno: no netbook da escola (1024×600) a legenda
        vira borrão. SVG cresce sem perder nada.

 ⚠️ E ELES SÃO ESQUEMÁTICOS, E A PROVA DIZ ISSO NA LEGENDA. O contorno de Santa
    Catarina aqui é simplificado — o que está correto e é o que a questão cobra
    são as RELAÇÕES: quem faz divisa com quem, de que lado fica o oceano, onde
    fica cada mesorregião em relação às outras, para onde aponta o Norte.
    Chamar de mapa preciso o que é esquema seria a mesma mentira que a foto.

 Uso: python3 _geo5/mapas.py
============================================================
"""
import io
import os

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")

CORES = {
    "oeste":  "#7fb069",
    "norte":  "#e8a33d",
    "vale":   "#4a90d9",
    "serra":  "#9b7cb8",
    "gfloripa": "#e26d5c",
    "sul":    "#e8c547",
    "mar":    "#bfe3f2",
    "vizinho": "#e6e2d8",
    "traco":  "#2b3245",
}

# ⚠️ contorno ESQUEMÁTICO de SC: as relações estão certas (Paraná ao norte, Rio
#    Grande do Sul ao sul, Argentina a oeste, oceano a leste), o desenho é
#    simplificado de propósito, para a legenda caber e ser lida.
MESO = {
    "oeste":    ("Oeste",               "M 60,120 L 235,112 L 243,330 L 66,322 Z"),
    "serra":    ("Serrana",             "M 243,196 L 380,190 L 392,336 L 245,330 Z"),
    "norte":    ("Norte",               "M 235,112 L 452,104 L 455,190 L 243,196 Z"),
    "vale":     ("Vale do Itajaí",      "M 455,190 L 560,186 L 565,252 L 392,258 L 380,190 Z"),
    "gfloripa": ("Grande Florianópolis","M 565,252 L 596,250 L 600,318 L 393,322 L 392,258 Z"),
    "sul":      ("Sul",                 "M 393,322 L 600,318 L 584,392 L 392,336 Z"),
}


def cabeca(w, h, titulo):
    return (u'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            u'role="img" aria-label="%s"><title>%s</title>\n'
            u'<rect width="%d" height="%d" fill="#fdfcf8"/>\n' % (w, h, titulo, titulo, w, h))


def rosa(x, y, r=34):
    u"""a rosa dos ventos — N em cima, e os quatro pontos escritos."""
    return (
        u'<g transform="translate(%d,%d)">'
        u'<circle r="%d" fill="#fff" stroke="%s" stroke-width="2"/>'
        u'<path d="M 0,-%d L 7,0 L 0,8 L -7,0 Z" fill="%s"/>'
        u'<path d="M 0,%d L 7,0 L 0,-8 L -7,0 Z" fill="#fff" stroke="%s" stroke-width="1.5"/>'
        u'<text x="0" y="-%d" text-anchor="middle" font-size="13" font-weight="700" fill="%s">N</text>'
        u'<text x="0" y="%d" text-anchor="middle" font-size="13" font-weight="700" fill="%s">S</text>'
        u'<text x="%d" y="5" text-anchor="middle" font-size="13" font-weight="700" fill="%s">L</text>'
        u'<text x="-%d" y="5" text-anchor="middle" font-size="13" font-weight="700" fill="%s">O</text>'
        u'</g>\n' % (x, y, r, CORES["traco"], r - 6, CORES["traco"], r - 6, CORES["traco"],
                     r + 7, CORES["traco"], r + 17, CORES["traco"],
                     r + 12, CORES["traco"], r + 12, CORES["traco"]))


def escala(x, y, larg, km):
    u"""a barra de escala: metade preta, metade branca, com o número em km."""
    m = larg // 2
    return (
        u'<g transform="translate(%d,%d)">'
        u'<rect width="%d" height="10" fill="%s" stroke="%s" stroke-width="1.5"/>'
        u'<rect x="%d" width="%d" height="10" fill="#fff" stroke="%s" stroke-width="1.5"/>'
        u'<text x="0" y="25" font-size="12" fill="%s">0</text>'
        u'<text x="%d" y="25" text-anchor="end" font-size="12" fill="%s">%d km</text>'
        u'</g>\n' % (x, y, m, CORES["traco"], CORES["traco"], m, m, CORES["traco"],
                     CORES["traco"], larg, CORES["traco"], km))


def mapa_mesorregioes():
    w, h = 900, 560
    s = cabeca(w, h, u"Mapa esquemático de Santa Catarina com as seis mesorregiões")
    s += u'<rect x="600" y="80" width="70" height="330" fill="%s"/>\n' % CORES["mar"]
    s += (u'<text x="636" y="250" text-anchor="middle" font-size="15" fill="#2c6b86" '
          u'font-weight="700" transform="rotate(90 636 250)">OCEANO ATLÂNTICO</text>\n')
    # vizinhos
    s += u'<rect x="40" y="52" width="640" height="56" fill="%s"/>\n' % CORES["vizinho"]
    s += u'<text x="360" y="88" text-anchor="middle" font-size="16" font-weight="700" fill="#5a5548">PARANÁ</text>\n'
    s += u'<rect x="40" y="400" width="620" height="56" fill="%s"/>\n' % CORES["vizinho"]
    s += u'<text x="350" y="436" text-anchor="middle" font-size="16" font-weight="700" fill="#5a5548">RIO GRANDE DO SUL</text>\n'
    s += u'<rect x="8" y="108" width="50" height="296" fill="%s"/>\n' % CORES["vizinho"]
    s += (u'<text x="33" y="256" text-anchor="middle" font-size="14" font-weight="700" fill="#5a5548" '
          u'transform="rotate(-90 33 256)">ARGENTINA</text>\n')
    # as seis
    for k in ("oeste", "serra", "norte", "vale", "gfloripa", "sul"):
        nome, d = MESO[k]
        s += u'<path d="%s" fill="%s" stroke="%s" stroke-width="2.5" opacity=".88"/>\n' % (
            d, CORES[k], CORES["traco"])
    rot = {"oeste": (148, 228), "serra": (312, 268), "norte": (340, 154),
           "vale": (476, 226), "gfloripa": (492, 292), "sul": (490, 356)}
    for k, (x, y) in rot.items():
        s += (u'<text x="%d" y="%d" text-anchor="middle" font-size="14" font-weight="700" '
              u'fill="#1c2130">%s</text>\n' % (x, y, MESO[k][0]))
    # a capital
    s += u'<circle cx="598" cy="286" r="7" fill="#fff" stroke="%s" stroke-width="3"/>\n' % CORES["traco"]
    s += u'<text x="586" y="286" text-anchor="end" font-size="13" font-weight="700" fill="#1c2130">Florianópolis</text>\n'
    s += rosa(776, 140)
    s += escala(700, 470, 160, 200)
    s += (u'<text x="40" y="36" font-size="19" font-weight="800" fill="#1c2130">'
          u'Santa Catarina — as seis mesorregiões</text>\n')
    s += (u'<text x="40" y="518" font-size="12" fill="#6a6a72">Mapa esquemático: o contorno é '
          u'simplificado; as posições de cada região, os vizinhos e o oceano estão corretos.</text>\n')
    s += u"</svg>\n"
    return "geo_mapa_meso.svg", s


def mapa_legenda():
    u"""mapa pequeno com SÍMBOLOS e a legenda ao lado — a questão de ler legenda."""
    w, h = 900, 500
    s = cabeca(w, h, u"Mapa com legenda: cidade, rio, serra e rodovia")
    s += u'<rect x="40" y="60" width="520" height="380" fill="#eef4e6" stroke="%s" stroke-width="2.5"/>\n' % CORES["traco"]
    s += u'<rect x="486" y="60" width="74" height="380" fill="%s"/>\n' % CORES["mar"]
    # rio
    s += (u'<path d="M 70,120 C 180,160 250,110 330,170 C 400,222 430,300 486,330" fill="none" '
          u'stroke="#4a90d9" stroke-width="7" stroke-linecap="round"/>\n')
    # rodovia
    s += (u'<path d="M 70,380 L 250,360 L 400,300 L 486,250" fill="none" stroke="#8a8a93" '
          u'stroke-width="7" stroke-dasharray="16 9" stroke-linecap="round"/>\n')
    # serra
    for cx in (150, 210, 270):
        s += (u'<path d="M %d,250 l 30,-46 l 30,46 Z" fill="#9b7cb8" stroke="%s" stroke-width="2"/>\n'
              % (cx, CORES["traco"]))
    # cidades
    for cx, cy, nome in ((330, 170, u"Blumenau"), (470, 330, u"Itajaí"), (120, 390, u"Chapecó")):
        s += u'<circle cx="%d" cy="%d" r="9" fill="#e26d5c" stroke="%s" stroke-width="2.5"/>\n' % (cx, cy, CORES["traco"])
        s += u'<text x="%d" y="%d" font-size="13" font-weight="700" fill="#1c2130">%s</text>\n' % (cx + 14, cy - 10, nome)
    # a legenda
    s += u'<rect x="600" y="60" width="262" height="250" fill="#fff" stroke="%s" stroke-width="2.5"/>\n' % CORES["traco"]
    s += u'<text x="620" y="90" font-size="16" font-weight="800" fill="#1c2130">LEGENDA</text>\n'
    itens = [
        (u"cidade", u'<circle cx="634" cy="%d" r="9" fill="#e26d5c" stroke="%s" stroke-width="2.5"/>'),
        (u"rio", u'<path d="M 620,%d h 30" stroke="#4a90d9" stroke-width="7" stroke-linecap="round"/>'),
        (u"serra", u'<path d="M 620,%d l 14,-20 l 14,20 Z" fill="#9b7cb8" stroke="%s" stroke-width="2"/>'),
        (u"rodovia", u'<path d="M 620,%d h 30" stroke="#8a8a93" stroke-width="7" stroke-dasharray="10 7"/>'),
        (u"oceano", u'<rect x="620" y="%d" width="30" height="16" fill="' + CORES["mar"] + u'"/>'),
    ]
    y = 122
    for nome, marca in itens:
        m = marca
        if m.count("%d") and m.count("%s"):
            m = m % (y, CORES["traco"])
        elif m.count("%d"):
            m = m % (y - 8 if nome == "oceano" else y)
        s += m + u"\n"
        s += u'<text x="666" y="%d" font-size="14" fill="#1c2130">%s</text>\n' % (y + 5, nome)
        y += 40
    s += rosa(776, 390)
    s += escala(60, 466, 150, 100)
    s += (u'<text x="40" y="36" font-size="19" font-weight="800" fill="#1c2130">'
          u'Um pedaço de Santa Catarina — leia pela legenda</text>\n')
    s += u"</svg>\n"
    return "geo_mapa_legenda.svg", s


def perfil_relevo():
    u"""o corte do relevo: do mar ao planalto. É a questão de relevo em UMA figura."""
    w, h = 900, 420
    s = cabeca(w, h, u"Perfil do relevo de Santa Catarina, do litoral ao planalto")
    s += u'<rect x="40" y="250" width="150" height="90" fill="%s"/>\n' % CORES["mar"]
    s += (u'<path d="M 190,340 L 190,300 L 330,296 L 420,150 L 520,120 L 860,116 L 860,340 Z" '
          u'fill="#cbb994" stroke="%s" stroke-width="2.5"/>\n' % CORES["traco"])
    s += (u'<path d="M 190,300 L 330,296 L 330,340 L 190,340 Z" fill="#a8d18d"/>\n')
    s += (u'<path d="M 420,150 L 520,120 L 860,116 L 860,340 L 520,340 Z" fill="#8fbf7a" opacity=".75"/>\n')
    for x, y, t in ((115, 240, u"OCEANO"), (258, 285, u"PLANÍCIE\nLITORÂNEA"),
                    (392, 210, u"SERRA"), (680, 100, u"PLANALTO")):
        for i, linha in enumerate(t.split("\n")):
            s += (u'<text x="%d" y="%d" text-anchor="middle" font-size="15" font-weight="800" '
                  u'fill="#1c2130">%s</text>\n' % (x, y + i * 18, linha))
    s += u'<line x1="40" y1="360" x2="860" y2="360" stroke="%s" stroke-width="2"/>\n' % CORES["traco"]
    s += u'<text x="40" y="384" font-size="13" fill="#4a4a55">LESTE (mar)</text>\n'
    s += u'<text x="860" y="384" text-anchor="end" font-size="13" fill="#4a4a55">OESTE (interior)</text>\n'
    s += (u'<text x="40" y="36" font-size="19" font-weight="800" fill="#1c2130">'
          u'Do mar para o interior: como o relevo sobe</text>\n')
    s += u"</svg>\n"
    return "geo_perfil.svg", s


def mapa_brasil():
    u"""Brasil esquemático com a Região Sul e SC destacada."""
    w, h = 760, 560
    s = cabeca(w, h, u"Mapa esquemático do Brasil com Santa Catarina destacada")
    s += (u'<path d="M 300,40 L 470,60 L 560,150 L 600,270 L 520,380 L 430,470 L 330,470 '
          u'L 250,400 L 170,300 L 150,170 L 210,70 Z" fill="#e6e2d8" stroke="%s" '
          u'stroke-width="2.5"/>\n' % CORES["traco"])
    # a Regiao Sul
    s += (u'<path d="M 330,470 L 430,470 L 452,392 L 300,392 Z" fill="#cfe3c4" stroke="%s" '
          u'stroke-width="2.5"/>\n' % CORES["traco"])
    s += u'<text x="376" y="500" text-anchor="middle" font-size="15" font-weight="800" fill="#1c2130">Região Sul</text>\n'
    # SC
    s += (u'<path d="M 318,432 L 436,432 L 432,452 L 322,452 Z" fill="#e26d5c" stroke="%s" '
          u'stroke-width="2.5"/>\n' % CORES["traco"])
    s += u'<text x="470" y="446" font-size="15" font-weight="800" fill="#a8412f">Santa Catarina</text>\n'
    s += rosa(660, 120)
    s += (u'<text x="40" y="36" font-size="19" font-weight="800" fill="#1c2130">'
          u'Onde fica Santa Catarina no Brasil</text>\n')
    s += (u'<text x="40" y="536" font-size="12" fill="#6a6a72">Mapa esquemático: o contorno é '
          u'simplificado; a posição da Região Sul e do estado está correta.</text>\n')
    s += u"</svg>\n"
    return "geo_mapa_brasil.svg", s


if __name__ == "__main__":
    for nome, svg in (mapa_mesorregioes(), mapa_legenda(), perfil_relevo(), mapa_brasil()):
        cam = os.path.join(SAIDA, nome)
        io.open(cam, "w", encoding="utf-8").write(svg)
        print(u"   %s  (%d bytes)" % (nome, os.path.getsize(cam)))
