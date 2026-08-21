#!/usr/bin/env python3
# ============================================================================
# FAZENDA (Stardew-like) — LOGISTICA DE ASSETS (roda no GitHub Actions).
# Baixa pacotes PIXEL ART CC0 do Kenney (top-down RPG/fazenda) — arte CONSISTENTE
# (evita o bug de coerencia). Abre a pagina do pacote, acha o .zip real, baixa,
# extrai os PNGs pra _fazenda/assets/images/ e escreve o manifest com os nomes reais.
# ============================================================================
import os, re, sys, io, zipfile, urllib.request

RAIZ = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(RAIZ, 'assets', 'images')
os.makedirs(IMG, exist_ok=True)
os.makedirs(os.path.join(RAIZ, 'assets', 'audio'), exist_ok=True)

# pacotes top-down pixel art (chao, arvores, agua, personagens, casas, plantacoes)
PAGINAS = [
    'https://kenney.nl/assets/roguelike-characters',  # PERSONAGENS top-down (frames de caminhada)
    'https://kenney.nl/assets/roguelike-rpg-pack',    # tilesheet RPG + itens
    'https://kenney.nl/assets/tiny-town',             # casinhas/fazenda pixel top-down
]
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}

def http(url, timeout=120):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()

def acha_zips(pagina):
    html = http(pagina).decode('utf-8', 'ignore')
    zips = re.findall(r'href="([^"]+?\.zip)"', html) + re.findall(r"href='([^']+?\.zip)'", html)
    norm = []
    for z in zips:
        if z.startswith('//'): z = 'https:' + z
        elif z.startswith('/'): z = 'https://kenney.nl' + z
        elif not z.startswith('http'): z = 'https://kenney.nl/' + z.lstrip('./')
        if z not in norm: norm.append(z)
    return norm

def extrai(zip_bytes, prefixo):
    zf = zipfile.ZipFile(io.BytesIO(zip_bytes)); n = 0
    for name in zf.namelist():
        low = name.lower()
        if not low.endswith('.png') or name.endswith('/'):
            continue
        if '/vector' in low:
            continue
        with zf.open(name) as f:
            # guarda o CAMINHO (pra saber o que e tilesheet vs tile solto)
            safe = prefixo + '__' + name.replace('/', '_')
            open(os.path.join(IMG, safe), 'wb').write(f.read()); n += 1
    return n

def main():
    total = 0
    for pg in PAGINAS:
        nome = pg.rstrip('/').split('/')[-1]
        print('== pacote:', nome, '==')
        try:
            zips = acha_zips(pg)
            print('  zips na pagina:', zips[:5] if zips else 'NENHUM')
            if not zips: continue
            data = http(zips[0], 180)
            print('  baixado: %.1f MB' % (len(data) / 1048576))
            n = extrai(data, nome); print('  extraidos %d PNG' % n); total += n
        except Exception as e:
            print('  ERRO:', str(e)[:220])
    arquivos = sorted(os.listdir(IMG))
    with open(os.path.join(RAIZ, 'assets', 'manifest.txt'), 'w') as m:
        m.write('total_png=%d\n' % len(arquivos)); m.write('\n'.join(arquivos))
    print('== TOTAL %d PNG | manifest com %d arquivos ==' % (total, len(arquivos)))
    if total == 0:
        print('::error::nenhum asset baixado'); sys.exit(1)

if __name__ == '__main__':
    main()
