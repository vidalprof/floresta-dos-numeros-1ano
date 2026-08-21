# -*- coding: utf-8 -*-
# ============================================================
#  AUDITOR DO MASCOTE — "ele treme quando fala ou pisca?"
#
#  Nasceu de um defeito que o Marcos pegou no olho (ago/2026), na Fábrica de
#  Brinquedos do Bento: *"ao falar ou piscar o mascote se treme todo"*.
#
#  Por que acontece: o mascote são TRÊS imagens empilhadas (parado / falando /
#  piscando) e o motor faz o cruzamento delas 60 vezes por segundo para o
#  lip-sync. Se as três forem DESENHOS DIFERENTES — e é o que a IA devolve
#  quando a gente pede as três do zero, mesmo escrevendo "exatamente igual" —
#  o cruzamento morfa o corpo inteiro e a criança vê o mascote vibrando.
#
#  A conta que denuncia: quantos por cento dos pixels do CORPO mudam entre a
#  pose parada e cada uma das outras. Medido nas atividades que estavam boas:
#     Legenda 1-2% · Jardim 2-8% · Doceria 5-6% · Órbi 8-11%
#  A Fábrica, feita errado, dava 77%.
#
#  ⭐ A CURA (e a regra da casa a partir de agora): as poses "falando" e
#  "piscando" NUNCA se geram do zero. Elas se geram EDITANDO a pose parada
#  (`gerar-imagens.yml` com o input `base`), que mantém o personagem e muda só
#  o que o prompt pedir.
#
#  Uso: python3 _qa/mascote.py _fabrica
# ============================================================
import os, re, sys

LIMITE = 15.0   # % do corpo que pode mudar entre as camadas
PISO = 0.15     # % MINIMO: abaixo disso a camada e copia da parada (nao move nada)

try:
    from PIL import Image
    import numpy as np
except Exception:
    print("  (sem Pillow/numpy — auditor do mascote pulado)")
    sys.exit(0)

alvo = sys.argv[1] if len(sys.argv) > 1 else ""
if not alvo:
    print("uso: python3 _qa/mascote.py <pasta-da-atividade|arquivo.html>")
    sys.exit(2)
pasta = alvo if os.path.isdir(alvo) else os.path.dirname(os.path.abspath(alvo))
pasta = os.path.relpath(pasta)
img = os.path.join(pasta, "img")
if not os.path.isdir(img):
    print("%s -> sem pasta img/, nada a conferir" % pasta)
    sys.exit(0)

arquivos = [f[:-4] for f in sorted(os.listdir(img)) if f.endswith(".png")]

def acha(*chaves):
    for n in arquivos:
        if all(k in n for k in chaves):
            return n
    return None

# a pose parada pode se chamar "_base" ou "_feliz" conforme a atividade
parado = acha("base") or acha("feliz")
falando = acha("fala")
piscando = acha("pisca")

if not parado or (not falando and not piscando):
    print("%s -> sem as camadas do mascote (base/fala/pisca), nada a conferir" % pasta)
    sys.exit(0)

def le(n):
    return np.asarray(Image.open(os.path.join(img, n + ".png")).convert("RGBA")).astype(np.int16)

b = le(parado)
ruins = []
print("%s -> mascote em camadas: %s (parado)" % (pasta, parado))
for nome in (falando, piscando):
    if not nome:
        continue
    o = le(nome)
    if o.shape != b.shape:
        print("   %-16s TAMANHO DIFERENTE do parado (%s x %s) -> a imagem PULA ao trocar"
              % (nome, o.shape[:2], b.shape[:2]))
        ruins.append((nome, "TREME"))
        continue
    dif = np.abs(b[:, :, :3] - o[:, :, :3]).max(axis=2)
    corpo = (b[:, :, 3] > 120) | (o[:, :, 3] > 120)
    pc = 100.0 * ((dif > 28) & corpo).sum() / max(1, corpo.sum())
    # ⚠️ LICAO PAGA (ago/2026, e foi o MARCOS quem viu, jogando): *"o mascote nao
    #    movimenta a boca ao falar e sim o bone"*. As tres camadas da Lina eram o
    #    MESMO arquivo, byte a byte — e este portao imprimia "muda 0.0% do corpo
    #    ok", que e o elogio maximo dele. Zero nao e camada perfeita: e camada que
    #    NAO EXISTE. Trocar uma imagem por ela mesma nao move boca nenhuma, e o
    #    unico movimento que sobra e o balanco do corpo — que na Lina, de bone,
    #    e o bone que balanca. Chao junto com o teto: abaixo de 0,15% tambem
    #    reprova.
    if pc < PISO:
        marca = "COPIA"
    elif pc > LIMITE:
        marca = "TREME"
    else:
        marca = "ok"
    print("   %-16s muda %5.1f%% do corpo   %s" % (nome, pc, marca))
    if pc > LIMITE or pc < PISO:
        ruins.append((nome, marca))

if not ruins:
    print("   mascote ok: as camadas sao o MESMO desenho, so a boca/os olhos mudam")
    sys.exit(0)

copias = [n for (n, m) in ruins if m == "COPIA"]
tremem = [n for (n, m) in ruins if m == "TREME"]
if copias:
    print("   %d CAMADA(S) SAO COPIA DA POSE PARADA — nao movem nada:" % len(copias))
    for n in copias:
        print("    %s" % n)
    print("   a crianca ve o mascote FALAR de boca fechada. O unico movimento que")
    print("   sobra e o balanco do corpo, e ela le isso como 'mexe o chapeu'.")
    print("   conserto: EDITAR a pose parada (gemini + base=), ou — sem credito —")
    print("   abrir a boca/fechar os olhos na propria arte, so na regiao do rosto.")
if tremem:
    print("   %d CAMADA(S) SAO OUTRO DESENHO (o mascote vai tremer ao falar/piscar):" % len(tremem))
    for n in tremem:
        print("    %s" % n)
    print("   conserto: gerar essa camada EDITANDO a pose parada —")
    print("   gerar-imagens.yml com modelo=gemini e base=_novo/%s.png," % parado)
    print("   pedindo para mudar SO a boca (ou so os olhos) e mais nada.")
sys.exit(1)
