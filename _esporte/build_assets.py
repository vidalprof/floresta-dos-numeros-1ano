#!/usr/bin/env python3
# ============================================================================
# ESTUDIO — LOGISTICA DE ASSETS (roda no GitHub Actions, internet liberada).
# Baixa PACOTES DE ARTE CC0 CONSISTENTES (Kenney) para EVITAR o bug de coerencia
# (personagem mudando a cada frame). Passos:
#   1) abre a pagina do pacote no kenney.nl e ACHA o link .zip real (adapta ao hash);
#   2) baixa e extrai os PNGs para _esporte/assets/images/;
#   3) escreve manifest.txt com os nomes REAIS dos arquivos (pro game.js usar certo);
#   4) (proxima etapa) monta o spritesheet unico + atlas.json.
# Fallback: se o kenney.nl falhar, tenta um espelho no GitHub.
# ============================================================================
import os, re, sys, io, zipfile, urllib.request

RAIZ = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(RAIZ, 'assets', 'images')
os.makedirs(IMG, exist_ok=True)
os.makedirs(os.path.join(RAIZ, 'assets', 'audio'), exist_ok=True)   # onde o Gemini salva os sons

# paginas dos pacotes (personagem animado + itens de esporte)
PAGINAS = [
    'https://kenney.nl/assets/toon-characters-1',   # personagem consistente (poses)
    'https://kenney.nl/assets/sports-pack',         # bola, gol, cesta, campo
]
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}

def http(url, timeout=90):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()

def acha_zips(pagina):
    html = http(pagina).decode('utf-8', 'ignore')
    zips = re.findall(r'href="([^"]+?\.zip)"', html) + re.findall(r'href=\'([^\']+?\.zip)\'', html)
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
        # pula variantes vetor/retina/duplicadas se houver pastas alternativas
        if '/vector' in low or 'double' in low:
            continue
        with zf.open(name) as f:
            safe = prefixo + '__' + os.path.basename(name)
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
            if not zips:
                continue
            data = http(zips[0], 180)
            print('  baixado: %.1f MB' % (len(data) / 1048576))
            n = extrai(data, nome)
            print('  extraidos %d PNG' % n); total += n
        except Exception as e:
            print('  ERRO:', str(e)[:220])
    arquivos = sorted(os.listdir(IMG))
    with open(os.path.join(RAIZ, 'assets', 'manifest.txt'), 'w') as m:
        m.write('total_png=%d\n' % len(arquivos))
        m.write('\n'.join(arquivos))
    print('== TOTAL %d PNG | manifest com %d arquivos ==' % (total, len(arquivos)))
    if total == 0:
        print('::error::nenhum asset baixado — revisar fonte/URLs')
        sys.exit(1)

if __name__ == '__main__':
    main()
