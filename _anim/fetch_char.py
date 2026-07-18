#!/usr/bin/env python3
# ============================================================================
# PERSONAGEM LPC universal (13 col, 832x1344) — baixa CORPO + ROUPA + CABELO e
# COMPOE o heroi (assets/hero.png). Roda no GitHub Actions (internet liberada).
# Regra do Marcos: nada "no olho" — o CABELO é DESCOBERTO pela API do GitHub
# (acha o caminho real do arquivo), nunca chutado. Se o cabelo falhar, o heroi
# sai sem cabelo (nao quebra), e o log diz exatamente o que aconteceu.
# ============================================================================
import os, sys, json, urllib.request
from PIL import Image

RAIZ = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(RAIZ, 'assets', 'images')
os.makedirs(IMG, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
# Kit CLASSICO estavel (jrconway3): TODAS as camadas na MESMA versao (21 linhas,
# 832x1344) -> alinham perfeito -> rosto no lugar. (Misturar versoes = rosto sumido.)
REPO = 'jrconway3/Universal-LPC-spritesheet'
RAW = 'https://raw.githubusercontent.com/%s/master/' % REPO
API = 'https://api.github.com/repos/%s/contents/' % REPO
ALVO = (832, 1344)  # so compoe camadas deste tamanho (mesma versao)

def http(u, t=120):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t).read()

def baixa(nome, urls):
    for u in urls:
        try:
            d = http(u)
            if len(d) > 500:
                open(os.path.join(IMG, nome + '.png'), 'wb').write(d)
                print('OK %s <- %s (%d bytes)' % (nome, u.split('/spritesheets/')[-1], len(d))); return True
        except Exception as e:
            print('  falhou', u.split('/spritesheets/')[-1], str(e)[:80])
    return False

def api(path):
    return json.loads(http(API + path))

def descobre_png(path, prefere=('black', 'brown', 'male'), prof=0):
    """DFS na API ate achar um .png; prefere caminhos com 'male'/cor. Sem chute."""
    if prof > 5:
        return None
    try:
        itens = api(path)
    except Exception as e:
        print('  API falhou em', path, str(e)[:60]); return None
    pngs = [i for i in itens if i.get('type') == 'file' and i['name'].endswith('.png')]
    if pngs:
        for k in prefere:
            for p in pngs:
                if k in p['path'].lower():
                    return p['download_url']
        return pngs[0]['download_url']
    dirs = [i for i in itens if i.get('type') == 'dir']
    dirs.sort(key=lambda d: 0 if any(k in d['name'].lower() for k in ('plain', 'male', 'adult', 'black')) else 1)
    for d in dirs:
        u = descobre_png(d['path'], prefere, prof + 1)
        if u:
            return u
    return None

def acha(nome, base, prefere):
    """descobre 1 camada pela API (nada chutado) e baixa; tudo do MESMO repo/versao."""
    print('== descobrindo %s em %s ==' % (nome, base))
    url = descobre_png(base, prefere)
    if url:
        print('  achado:', url.split('/master/')[-1])
        baixa(nome, [url])
    else:
        print('  ! nao achei', nome)

def main():
    # TODAS as camadas do MESMO repo (jrconway3) = mesma versao = alinham.
    acha('lpc_body', 'body', ('male', 'light'))
    acha('lpc_legs', 'legs', ('male', 'pants', 'white'))
    acha('lpc_torso', 'torso', ('male', 'longsleeve', 'shirt', 'white'))
    acha('lpc_hair', 'hair', ('male', 'plain', 'brown'))

    # COMPOE o heroi — SO camadas do tamanho ALVO (mesma versao); descarta o resto.
    def carrega(n):
        p = os.path.join(IMG, n + '.png')
        return Image.open(p).convert('RGBA') if os.path.exists(p) else None
    corpo = carrega('lpc_body')
    if not corpo:
        print('::error:: corpo ausente'); sys.exit(1)
    alvo = corpo.size  # o CORPO define o tamanho; so compoe camadas iguais
    print('== corpo %s (esperado 832x1344 = classico) ==' % (alvo,))
    heroi = corpo.copy()
    for camada in ['lpc_legs', 'lpc_torso', 'lpc_hair']:
        c = carrega(camada)
        if c and c.size == alvo:
            heroi.alpha_composite(c, (0, 0)); print('  + camada %s' % camada)
        elif c:
            print('  ! %s tem %s != %s, DESCARTEI (versao diferente)' % (camada, c.size, alvo))
    saida = os.path.join(RAIZ, 'assets', 'hero.png')
    heroi.save(saida)
    print('== hero.png composto:', heroi.size, '==')

if __name__ == '__main__':
    main()
