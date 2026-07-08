#!/usr/bin/env python3
# Auditoria pre-publicacao de uma atividade (index.html). Roda ANTES de todo publish.
# Uso: python3 _circo/auditar.py <caminho/index.html>
import sys, re, subprocess, tempfile, os

def main(path):
    html = open(path, encoding="utf-8").read()
    scripts = re.findall(r'<script>(.*?)</script>', html, re.S)
    js = max(scripts, key=len) if scripts else ""
    falhas = []
    avisos = []

    # 1) tokens de imagem nao resolvidos
    toks = set(re.findall(r'\{\{[A-Z_]+\}\}', html))
    if toks: falhas.append("Tokens de imagem nao resolvidos: " + ", ".join(sorted(toks)))

    # 2) node --check (sintaxe)
    tf = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8")
    tf.write(js); tf.close()
    r = subprocess.run(["node","--check",tf.name], capture_output=True, text=True)
    os.unlink(tf.name)
    if r.returncode != 0: falhas.append("JS invalido (node --check): " + r.stderr.strip()[:200])

    # 3) JS moderno proibido
    for pat,nome in [(r'=>',"arrow =>"),(r'\blet\b',"let"),(r'\bconst\b',"const"),
                     (r'`',"template literal (crase)"),(r'\?\.',"optional chaining ?."),
                     (r'\?\?',"nullish ??"),(r'\basync\b',"async"),(r'\bawait\b',"await"),(r'\.\.\.',"spread ...")]:
        if re.search(pat, js): falhas.append("JS moderno proibido: " + nome)

    # 4) funcoes duplicadas
    fns = re.findall(r'function ([a-zA-Z_][a-zA-Z0-9_]*)\(', js)
    dup = sorted(set([f for f in fns if fns.count(f) > 1]))
    if dup: falhas.append("Funcoes duplicadas: " + ", ".join(dup))

    # 5) variavel com acento no nome
    if re.search(r'\bvar +[a-zA-Z_]*[áàâãéêíóôõúç]', js): falhas.append("Variavel com acento no nome")

    # 6) CONCORDANCIA: digito seguido de substantivo FEMININO dentro de uma fala
    fem = "parada|paradas|medalha|medalhas|bola|bolas|argola|argolas|pipoca|pipocas|estrela|estrelas|bandeirinha|bandeirinhas|cor|cores|volta|voltas|ilha|ilhas"
    for m in re.findall(r'falar\("([^"]*)"', js):
        if re.search(r'"?\b1\s+(' + fem + r')\b', '"'+m):
            avisos.append("Possivel concordancia (1 + feminino) na fala: ..." + m[:70])
        if re.search(r'\+\s*[a-zA-Z_]+\s*\+\s*"?\s+(parada|bola|estrela)', m):
            pass  # heuristica fraca; ignorar
    # varredura direta por '1 <feminino>' hardcoded em qualquer string
    for m in re.findall(r'"([^"]*\b1\s+(?:' + fem + r')\b[^"]*)"', js):
        avisos.append("String com '1 + feminino' (checar se e falada): " + m[:70])

    # 7) CSS moderno proibido (no HTML/CSS)
    css = html
    for pat,nome in [(r'display\s*:\s*grid',"display:grid"),(r'\bgap\s*:',"gap:"),(r'clamp\(',"clamp()"),(r'var\(--',"var(--)")]:
        if re.search(pat, css): avisos.append("CSS moderno (checar): " + nome)

    # 8) keyframes pareados
    kf = len(re.findall(r'@keyframes', css)); wkf = len(re.findall(r'@-webkit-keyframes', css))
    if kf != wkf: avisos.append("Keyframes nao pareados: @keyframes=%d @-webkit-keyframes=%d" % (kf, wkf))

    # 9) onclick sem funcao definida
    ocs = set(re.findall(r'onclick="([a-zA-Z_][a-zA-Z0-9_]*)\(', html))
    defined = set(fns)
    faltando = sorted([o for o in ocs if o not in defined])
    if faltando: falhas.append("onclick sem funcao definida: " + ", ".join(faltando))

    print("=== AUDITORIA:", os.path.basename(path), "===")
    if not falhas and not avisos:
        print("OK — nenhum problema encontrado.")
    for f in falhas: print("  [FALHA] " + f)
    for a in avisos: print("  [aviso] " + a)
    print("Resultado:", "REPROVADO" if falhas else "APROVADO" + (" (com avisos)" if avisos else ""))
    return 1 if falhas else 0

if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "_novo/index.html"
    sys.exit(main(p))
