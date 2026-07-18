#!/usr/bin/env python3
# Busca um PERSONAGEM ANIMADO (andar 4 direcoes) de fontes CC0/livres, via GitHub Actions.
# Tenta varias fontes e RELATA qual funcionou (adaptativo). Salva em _anim/assets/images.
import os, io, sys, zipfile, urllib.request

RAIZ = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(RAIZ, 'assets', 'images')
os.makedirs(IMG, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}

def http(u, t=120):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t).read()

# 1) LPC "universal" body (andar 4 direcoes garantido) — repositorios conhecidos
LPC = [
    'https://raw.githubusercontent.com/sanderfrenken/Universal-LPC-Spritesheet-Character-Generator/master/spritesheets/body/bodies/male/universal.png',
    'https://raw.githubusercontent.com/LiberatedPixelCup/Universal-LPC-Spritesheet-Character-Generator/master/spritesheets/body/bodies/male/universal.png',
    'https://raw.githubusercontent.com/sanderfrenken/Universal-LPC-Spritesheet-Character-Generator/master/spritesheets/body/male/light.png',
    'https://raw.githubusercontent.com/jrconway3/Universal-LPC-spritesheet/master/body/male/light.png',
]
# roupa/cabelo LPC (opcional, deixa o personagem vestido)
LPC_EXTRA = [
    ('lpc_torso', ['https://raw.githubusercontent.com/sanderfrenken/Universal-LPC-Spritesheet-Character-Generator/master/spritesheets/torso/clothes/longsleeve/longsleeve/male/white.png']),
    ('lpc_hair', ['https://raw.githubusercontent.com/sanderfrenken/Universal-LPC-Spritesheet-Character-Generator/master/spritesheets/hair/plain/adult/male/black.png']),
]

def baixa_primeiro(nome, urls):
    for u in urls:
        try:
            d = http(u)
            if len(d) > 500:
                open(os.path.join(IMG, nome + '.png'), 'wb').write(d)
                print('OK %s <- %s (%d bytes)' % (nome, u, len(d))); return True
        except Exception as e:
            print('  falhou', u.split('/master/')[-1] if '/master/' in u else u, str(e)[:90])
    return False

def main():
    ok = 0
    if baixa_primeiro('lpc_body', LPC): ok += 1
    for nome, urls in LPC_EXTRA:
        if baixa_primeiro(nome, urls): ok += 1
    arquivos = sorted(os.listdir(IMG))
    open(os.path.join(RAIZ, 'assets', 'manifest.txt'), 'w').write('\n'.join(arquivos))
    print('== baixados: %d | arquivos: %s ==' % (ok, arquivos))
    if ok == 0:
        print('::error::nenhum personagem baixado'); sys.exit(1)

if __name__ == '__main__':
    main()
