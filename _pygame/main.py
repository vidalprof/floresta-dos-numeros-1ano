# A Vila que Acorda — TESTE em PyGame (empacotado pra web com pygbag).
# Objetivo: o Marcos julgar, no PC da escola e no celular, o PESO/CARREGAMENTO
# e a sensacao do PyGame rodando dentro do navegador (WebAssembly).
# Mesma arte pintada (Gemini) do app Phaser, pra comparar maca com maca.
import asyncio, math, array
import pygame

W, H = 480, 800


async def main():
    pygame.init()
    try:
        pygame.mixer.init()
    except Exception:
        pass
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("A Vila que Acorda - PyGame")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    small = pygame.font.Font(None, 26)

    bg = pygame.image.load("bg_horta.jpg").convert()
    bg = pygame.transform.smoothscale(bg, (W, W))            # 480x480
    byte = pygame.image.load("byte.png").convert_alpha()
    bh = 220
    bw = int(byte.get_width() * bh / byte.get_height())
    byte = pygame.transform.smoothscale(byte, (bw, bh))
    maca = pygame.image.load("maca.png").convert_alpha()
    mh = 56
    mw = int(maca.get_width() * mh / maca.get_height())
    maca = pygame.transform.smoothscale(maca, (mw, mh))

    # beep curtinho gerado (sem arquivo)
    snd = None
    try:
        sr = 22050
        buf = array.array("h")
        for i in range(int(sr * 0.12)):
            buf.append(int(8000 * math.sin(2 * math.pi * 880 * i / sr) * math.exp(-i / 1400)))
        snd = pygame.mixer.Sound(buffer=buf.tobytes())
    except Exception:
        snd = None

    apples = []     # [x, y, vy]
    total = 0
    t = 0
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                apples.append([W // 2 + ((t * 37) % 140) - 70, 70, 2.0])
                total += 1
                if snd:
                    try:
                        snd.play()
                    except Exception:
                        pass
        t += 1

        screen.fill((150, 205, 130))
        pygame.draw.rect(screen, (198, 230, 245), (0, 0, W, 150))
        screen.blit(bg, (0, 150))

        # Byte respirando (vidinha por codigo)
        s = 1.0 + 0.03 * math.sin(t * 0.06)
        b2 = pygame.transform.smoothscale(byte, (max(1, int(bw * s)), max(1, int(bh * s))))
        screen.blit(b2, (W // 2 - b2.get_width() // 2, 500 - b2.get_height()))

        # macas caindo com quicada
        chao = 700
        for ap in apples:
            ap[2] += 0.45
            ap[1] += ap[2]
            if ap[1] > chao:
                ap[1] = chao
                ap[2] = -ap[2] * 0.35
                if abs(ap[2]) < 1.2:
                    ap[2] = 0
            screen.blit(maca, (int(ap[0] - mw // 2), int(ap[1] - mh // 2)))

        screen.blit(font.render("A Vila que Acorda", True, (31, 91, 138)), (26, 34))
        screen.blit(small.render("PyGame na web (teste) - toque na tela", True, (40, 70, 90)), (26, 78))
        screen.blit(font.render("Macas: %d" % total, True, (255, 255, 255)), (18, 112))

        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)


asyncio.run(main())
