# -*- coding: utf-8 -*-
u"""
PORTÃO DA FIGURA MORDIDA — "o recorte comeu um pedaço do desenho?"

NASCEU DO OLHO DO MARCOS (set/2026): *"observei que as imagens bola e elefante
aparecem faltando partes, corrija e verifique se tem mais imagens assim"*.

E ele estava certo nas duas:
  · pw_bola.png — a base da bola sumiu. Sobrou um fragmento azul solto no vão, e
    a bola não fecha embaixo.
  · pw_elefante.png — uma mordida entre as duas patas, comendo a barriga, mais
    um pedacinho solto no meio do vão.

A causa é o recorte automático de fundo (rembg). Ele decide, pixel a pixel, o
que é figura e o que é fundo — e erra justamente onde o desenho tem cor parecida
com o fundo ou uma sombra colada. O resultado passa por TODOS os nossos portões:
a imagem existe, carrega, tem o tamanho certo, o `_qa/imagens.js` confirma que
não é um quadradinho quebrado. Ela só está ERRADA, e isso só o olho vê.

O QUE ELE MEDE — três marcas do recorte que comeu demais:
  1. BURACO: transparência CERCADA pela figura (a água que entra pelas bordas
     não alcança). Um desenho pode ter buraco de verdade — a alça de uma xícara,
     o meio de uma rosquinha — por isso só reprova quando é grande.
  2. FRAGMENTO SOLTO: um pedaço opaco separado do corpo principal. Quase sempre
     é lixo que o recorte deixou (a sombra virando ilha), ou um pedaço da figura
     que se desprendeu.
  3. MORDIDA: uma reentrância funda vinda da borda para dentro da silhueta —
     foi assim que a bola perdeu a base e o elefante perdeu a barriga. Medida
     comparando a figura com o seu "casco" (o contorno preenchido linha a
     linha): se falta muito lá dentro, o recorte mordeu.

⚠️⚠️ LIÇÃO DA CALIBRAÇÃO, e ela muda o que este portão promete. Tentei separar
"recorte comeu" de "vão legítimo" por número — buraco, fragmento, mordida no
casco, serrilhado do contorno. Nenhuma medida sozinha resolve, e os números
provam: a zebra (mordida de verdade) dá contorno 10,1 de serrilhado, mas a flor
(pétalas e folhas separadas, perfeita) dá 4,5 e o rato (a cauda fina) dá 6,2 —
enquanto a bola, que perdeu a base inteira, dá 2,0. Calibrar para pegar a bola
acusaria metade das figuras boas, e portão que acusa inocente ensina a ignorar
portão.

Então este portão faz DUAS coisas, e é honesto sobre cada uma:
  · REPROVA só o que é certeza matemática — buraco cercado pela figura e
    fragmento solto grande. Aqui não há dúvida: o desenho não tem furo.
  · MONTA UM CONTATO-FOLHA (todas as figuras da atividade numa página, sobre
    fundo xadrez, com o nome de cada uma) e diz para OLHAR. Dez segundos de olho
    humano decidem o que nenhuma conta decidiu — foi assim que o Marcos pegou a
    bola e o elefante, e assim que confirmei a zebra.

Isso não é desistir da medição: é medir o que dá para medir e parar de fingir
que o resto também está medido.

Uso:  python3 _qa/figura_mordida.py <pasta>        (ex.: _por4)
      python3 _qa/figura_mordida.py <pasta> --tudo  (mostra também as limpas)
Sai 0 se limpo, 1 se achou figura mordida, 2 se não deu para medir.
"""
import glob, os, sys
from collections import deque

try:
    from PIL import Image
except ImportError:
    print(u"NAO MEDI: falta a Pillow (pip install pillow)")
    sys.exit(2)

OPACO = 120          # acima disso é figura
IGNORA = ("fundo", "_fundo", "ceu", "capa", "bg", "medalha", "med_")


def analisa(caminho):
    im = Image.open(caminho).convert("RGBA")
    w, h = im.size
    a = im.split()[-1].load()

    # --- 1) o que é fundo de verdade: a água que entra pelas 4 bordas ---
    fora = [[False] * h for _ in range(w)]
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if a[x, y] <= OPACO and not fora[x][y]:
                fora[x][y] = True; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if a[x, y] <= OPACO and not fora[x][y]:
                fora[x][y] = True; q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not fora[nx][ny] and a[nx, ny] <= OPACO:
                fora[nx][ny] = True; q.append((nx, ny))

    figura = buraco = 0
    for x in range(w):
        for y in range(h):
            if a[x, y] > OPACO: figura += 1
            elif not fora[x][y]: buraco += 1
    if not figura:
        return None

    # --- 2) pedaços soltos: componentes opacos separados ---
    visto = [[False] * h for _ in range(w)]
    pedacos = []
    for sx in range(w):
        for sy in range(h):
            if a[sx, sy] > OPACO and not visto[sx][sy]:
                n = 0; q = deque([(sx, sy)]); visto[sx][sy] = True
                while q:
                    x, y = q.popleft(); n += 1
                    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and not visto[nx][ny] and a[nx, ny] > OPACO:
                            visto[nx][ny] = True; q.append((nx, ny))
                pedacos.append(n)
    pedacos.sort(reverse=True)
    corpo = pedacos[0]
    soltos = [p for p in pedacos[1:] if p > figura * 0.002]   # lixo minúsculo não conta

    # --- 3) mordida: o "casco" (contorno preenchido por linha e por coluna) ---
    #     Onde o casco tem figura e a imagem não tem, o recorte comeu.
    casco = 0
    for y in range(h):
        xs = [x for x in range(w) if a[x, y] > OPACO]
        if xs: casco += xs[-1] - xs[0] + 1
    cascoV = 0
    for x in range(w):
        ys = [y for y in range(h) if a[x, y] > OPACO]
        if ys: cascoV += ys[-1] - ys[0] + 1
    # a mordida conta só o que falta nas DUAS varreduras (senão a perna de um
    # boneco, que é um vão legítimo, seria acusada)
    falta_h = max(0, casco - figura)
    falta_v = max(0, cascoV - figura)
    mordida = min(falta_h, falta_v)

    return {
        "w": w, "h": h, "figura": figura,
        "buraco_pc": buraco * 100.0 / figura,
        "soltos": len(soltos),
        "solto_pc": (sum(soltos) * 100.0 / figura) if soltos else 0.0,
        "mordida_pc": mordida * 100.0 / figura,
    }


def contato(arqs, pasta):
    u"""Monta a folha de contato: todas as figuras numa página só, sobre xadrez.
    É o que o olho humano precisa para decidir em dez segundos o que as contas
    não decidem."""
    try:
        from PIL import ImageDraw
    except ImportError:
        return None
    vis = [p for p in arqs
           if not any(k in os.path.basename(p).lower() for k in IGNORA)]
    if not vis:
        return None
    CEL, COLS = 190, 5
    linhas = (len(vis) + COLS - 1) // COLS
    W, H = COLS * CEL, linhas * (CEL + 22)
    folha = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    px = folha.load()
    for x in range(W):                       # xadrez: sem ele a falta some no branco
        for y in range(H):
            if ((x // 12) + (y // 12)) % 2:
                px[x, y] = (206, 206, 220, 255)
    d = ImageDraw.Draw(folha)
    for i, p in enumerate(vis):
        try:
            im = Image.open(p).convert("RGBA")
        except Exception:
            continue
        im.thumbnail((CEL - 16, CEL - 16))
        cx = (i % COLS) * CEL + (CEL - im.width) // 2
        cy = (i // COLS) * (CEL + 22) + (CEL - im.height) // 2
        folha.alpha_composite(im, (cx, cy))
        d.text(((i % COLS) * CEL + 6, (i // COLS) * (CEL + 22) + CEL + 4),
               os.path.basename(p)[:-4], fill=(20, 20, 30, 255))
    saida = os.path.join("_qa", "_dossie", "contato-%s.png" % os.path.basename(pasta).lstrip("_"))
    try:
        os.makedirs(os.path.dirname(saida), exist_ok=True)
        folha.save(saida)
        return saida
    except Exception:
        return None


def confere(pasta, tudo=False):
    if os.path.isdir(pasta):
        arqs = sorted(glob.glob(os.path.join(pasta, "img", "*.png")))
        if not arqs:
            arqs = sorted(glob.glob(os.path.join(pasta, "*.png")))
    else:
        arqs = [pasta]
    if not arqs:
        print(u"NAO MEDI: nenhum .png em %s" % pasta)
        return 2

    ruins, olhar, medidas = [], [], 0
    for p in arqs:
        nome = os.path.basename(p)
        if any(k in nome.lower() for k in IGNORA):
            continue
        try:
            r = analisa(p)
        except Exception as e:
            print(u"   (nao consegui ler %s: %s)" % (nome, e))
            continue
        if not r:
            continue
        medidas += 1
        marcas = []
        if r["buraco_pc"] > 0.6:
            marcas.append(u"BURACO no meio (%.1f%% da figura)" % r["buraco_pc"])
        # ⚠️ o TAMANHO do pedaço solto é o que separa lixo de arte: o resto que o
        #    recorte deixou é PEQUENO (o pontinho no vão do elefante); o que é
        #    grande quase sempre é parte legítima do desenho — as folhas da flor
        #    (33,9%!), as antenas da abelha, a cauda solta. Acima de 8% vira
        #    "olhe", não reprovação.
        if r["soltos"] and 0.15 < r["solto_pc"] <= 8:
            marcas.append(u"%d pedaco(s) SOLTO(s) e pequeno(s) fora do corpo (%.1f%%) — cheira a lixo do recorte"
                          % (r["soltos"], r["solto_pc"]))
        elif r["soltos"] and r["solto_pc"] > 8:
            olhar.append(u"%s (%d pedaco(s) solto(s), %.0f%% — pode ser folha/antena/cauda)"
                         % (nome, r["soltos"], r["solto_pc"]))
        # ⚠️ a "mordida por casco" NÃO reprova: ela acusa a flor (folhas soltas)
        #    e o rato (cauda fina) tanto quanto a zebra (mordida real). Fica como
        #    dica de ONDE olhar primeiro no contato-folha.
        if r["mordida_pc"] > 20:
            olhar.append(u"%s (silhueta %.0f%% vazia — confira no contato-folha)"
                         % (nome, r["mordida_pc"]))
        if marcas:
            ruins.append((nome, r, marcas))
        elif tudo:
            print(u"   ok  %-24s %dx%d" % (nome, r["w"], r["h"]))

    if not medidas:
        print(u"NAO MEDI: nenhuma figura com transparencia em %s" % pasta)
        return 2

    if olhar:
        print(u"   olhe primeiro estas (pode ser vão do desenho, pode ser recorte):")
        for m in olhar[:8]:
            print(u"      · %s" % m)

    folha = contato(arqs, pasta)
    if folha:
        print(u"   👁  contato-folha para OLHAR: %s" % folha)
        print(u"      (as contas não separam 'recorte comeu' de 'vão do desenho' —")
        print(u"       veja o cabeçalho deste arquivo. Dez segundos de olho resolvem.)")

    if ruins:
        print(u"%s -> %d figura(s) MORDIDAS pelo recorte (de %d conferidas):"
              % (pasta, len(ruins), medidas))
        for nome, r, marcas in ruins:
            print(u"    ✗ %-24s %dx%d" % (nome, r["w"], r["h"]))
            for m in marcas:
                print(u"         · %s" % m)
        print(u"   Conserto: a figura precisa ser gerada de novo (o recorte comeu")
        print(u"   parte do desenho). O Claude nao gera arte — passe o prompt ao")
        print(u"   Marcos, e ao receber confira aqui de novo antes de publicar.")
        return 1

    print(u"%s -> figuras ok: %d conferidas, nenhuma mordida pelo recorte." % (pasta, medidas))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/figura_mordida.py <pasta> [--tudo]")
        sys.exit(2)
    sys.exit(confere(sys.argv[1].rstrip("/"), "--tudo" in sys.argv))
