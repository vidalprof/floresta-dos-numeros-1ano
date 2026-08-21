#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TESTE HEADLESS AUTOMATICO — carrega a atividade num Chromium de verdade e
# pega ERRO DE JS EM EXECUCAO (o que a auditoria estatica nao ve: erro que so
# aparece quando o codigo RODA). Tira um print de cada tela inicial.
#
# Roda AQUI (nao no PC da escola). Uso:
#   python3 _circo/testar-headless.py <index.html> [<index.html> ...]
#
# Saida por atividade: OK (0 erros) ou ERRO (com as linhas do erro de JS).
import sys, os, glob, subprocess, tempfile, re

def achar_chrome():
    for p in sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"), reverse=True):
        return p
    for p in ("/usr/bin/chromium","/usr/bin/chromium-browser","/usr/bin/google-chrome"):
        if os.path.exists(p): return p
    return None

# Capturador de erro injetado na pagina: window 'error' e promessas rejeitadas
# gravam a mensagem num <div id="__errbox"> que sai no --dump-dom. Registrado ANTES
# de tudo, entao pega os erros dos scripts da atividade quando eles RODAM.
CATCHER = ('<script>(function(){function box(){var d=document.getElementById("__errbox");'
           'if(!d){d=document.createElement("div");d.id="__errbox";'
           '(document.documentElement||document).appendChild(d);}return d;}'
           'window.addEventListener("error",function(e){box().appendChild(document.createTextNode('
           '" [ERR] "+((e&&e.message)||(e&&e.error)||"erro")+" @"+((e&&e.filename)||"")+":"+((e&&e.lineno)||"")));});'
           'window.addEventListener("unhandledrejection",function(e){box().appendChild(document.createTextNode('
           '" [ERR] promessa rejeitada: "+((e&&e.reason)||"")));});})();</script>')

ERRBOX = re.compile(r'<div id="__errbox">(.*?)</div>', re.S)
MARK = re.compile(r'\[ERR\][^\[<]*')

def nome_curto(path):
    d = os.path.basename(os.path.dirname(path))
    return d if d and d not in (".","_novo","_lote") else os.path.basename(path)

def _injetar_catcher(html):
    # injeta o mais cedo possivel: apos <head>, senao apos <html>, senao no inicio.
    m = re.search(r'<head[^>]*>', html, re.I)
    if m: pos = m.end()
    else:
        m = re.search(r'<html[^>]*>', html, re.I)
        pos = m.end() if m else 0
    return html[:pos] + CATCHER + html[pos:]

def testar_um(chrome, path, shotdir):
    nome = nome_curto(path)
    shot = os.path.join(shotdir, nome + ".png")
    # copia com o capturador injetado (nao altera o arquivo original)
    html = open(path, encoding="utf-8", errors="replace").read()
    tmp = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8")
    tmp.write(_injetar_catcher(html)); tmp.close()
    cmd = [chrome, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
           "--virtual-time-budget=5000", "--dump-dom", "--screenshot=" + shot,
           "--window-size=1000,750", "file://" + tmp.name]
    dom = ""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        dom = r.stdout or ""
    except subprocess.TimeoutExpired:
        os.unlink(tmp.name)
        return nome, ["TIMEOUT ao carregar (>90s)"], shot
    os.unlink(tmp.name)
    # le SO o conteudo da caixinha de erro (nao o DOM todo — o proprio script
    # capturador contem o texto "[ERR]" no fonte e daria falso positivo).
    mb = ERRBOX.search(dom)
    conteudo = mb.group(1) if mb else ""
    erros = [m.group(0).strip() for m in MARK.finditer(conteudo)]
    # dedup mantendo ordem
    vistos, unicos = set(), []
    for e in erros:
        if e not in vistos:
            vistos.add(e); unicos.append(e[:180])
    return nome, unicos, shot

def main(args):
    if not args:
        print("uso: python3 _circo/testar-headless.py <index.html> [...]"); return 2
    chrome = achar_chrome()
    if not chrome:
        print("!! Chromium nao encontrado (esperado em /opt/pw-browsers)."); return 3
    shotdir = tempfile.mkdtemp(prefix="teste-headless-")
    print("Chromium:", chrome)
    print("Prints em:", shotdir); print()
    rc = 0
    for p in args:
        if not os.path.isfile(p):
            print("!! nao achei: " + p); continue
        nome, erros, shot = testar_um(chrome, p, shotdir)
        existe = os.path.exists(shot) and os.path.getsize(shot) > 0
        if erros:
            rc = 1
            print("[ERRO] %-26s  render=%s" % (nome, "sim" if existe else "NAO"))
            for e in erros[:6]:
                print("        - " + e)
        else:
            print("[ OK ] %-26s  render=%s  (0 erro de JS)" % (nome, "sim" if existe else "NAO"))
    print("\nResultado:", "REPROVADO (erros de JS)" if rc else "APROVADO (0 erro em todas)")
    return rc

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
