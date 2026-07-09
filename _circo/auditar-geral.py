#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# AUDITOR GENERICO — roda em QUALQUER atividade (nao so no Circo).
# Faz DUAS coisas:
#   (A) CHECAGENS DE COMPATIBILIDADE/QUALIDADE (barram: valem p/ navegador antigo)
#   (B) CHECKLIST DE RECURSOS (o que a atividade TEM/FALTA — base p/ a "base-mae")
#
# Uso:
#   python3 _circo/auditar-geral.py <index.html> [<index.html> ...]
#   python3 _circo/auditar-geral.py --matriz <index.html> [...]   (tabela resumo)
#
# Este script roda AQUI (Python), nunca no PC da escola. Ele PROTEGE o PC antigo:
# barra tudo que quebraria navegador velho. Nao envia nada pra criancas.
import sys, re, subprocess, tempfile, os

# ---------- (A) CHECAGENS DE COMPATIBILIDADE / QUALIDADE (genericas) ----------
def checar_compat(html):
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
    js = "\n".join(scripts)
    falhas, avisos = [], []

    # 1) tokens de imagem nao resolvidos ({{FOO}})
    toks = set(re.findall(r'\{\{[A-Z_]+\}\}', html))
    if toks: falhas.append("Tokens nao resolvidos: " + ", ".join(sorted(toks)))

    # 2) node --check (sintaxe do maior bloco de script)
    maior = max(scripts, key=len) if scripts else ""
    if maior.strip():
        tf = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8")
        tf.write(maior); tf.close()
        r = subprocess.run(["node","--check",tf.name], capture_output=True, text=True)
        os.unlink(tf.name)
        if r.returncode != 0:
            falhas.append("JS invalido (node --check): " + r.stderr.strip()[:160])

    # 3) JS moderno proibido (quebra navegador antigo).
    #    IMPORTANTE: remover o CONTEUDO das strings antes de procurar, senao reticencias
    #    em texto ("Pensando...") viram falso "spread ..." e setas em texto viram "arrow =>".
    js_sem_uri = re.sub(r'data:[^"\')\s]+', '', js)
    js_sem_str = re.sub(r'"(?:\\.|[^"\\])*"', '""', js_sem_uri)      # tira "..."
    js_sem_str = re.sub(r"'(?:\\.|[^'\\])*'", "''", js_sem_str)      # tira '...'
    js_sem_str = re.sub(r'/\*.*?\*/', ' ', js_sem_str, flags=re.S)   # tira /* comentario */
    js_sem_str = re.sub(r'//[^\n]*', ' ', js_sem_str)               # tira // comentario
    for pat,nome in [(r'=>',"arrow =>"),(r'\blet\b',"let"),(r'\bconst\b',"const"),
                     (r'`',"template literal"),(r'\?\.',"optional chaining ?."),
                     (r'\?\?',"nullish ??"),(r'\basync\b',"async"),(r'\bawait\b',"await"),
                     (r'\.\.\.[A-Za-z_$\[\{(]',"spread ...")]:
        if re.search(pat, js_sem_str): falhas.append("JS moderno proibido: " + nome)

    # 4) funcoes duplicadas
    fns = re.findall(r'function ([a-zA-Z_][a-zA-Z0-9_]*)\(', js)
    dup = sorted(set([f for f in fns if fns.count(f) > 1]))
    if dup: avisos.append("Funcoes duplicadas: " + ", ".join(dup))

    # 5) variavel com acento no nome
    if re.search(r'\bvar +[a-zA-Z_]*[a-ÿ]', js) and re.search(r'\bvar +[a-zA-Z_]*[áàâãéêíóôõúüç]', js):
        falhas.append("Variavel com acento no nome")

    # 6) CSS moderno (aviso: alguns quebram em navegador MUITO antigo)
    for pat,nome in [(r'display\s*:\s*grid',"display:grid"),(r'\bgap\s*:',"gap:"),
                     (r'clamp\(',"clamp()"),(r'\bvar\(--',"var(--)")]:
        if re.search(pat, html): avisos.append("CSS moderno (checar em PC antigo): " + nome)

    # 7) keyframes pareados (-webkit-)
    kf = len(re.findall(r'@keyframes', html)); wkf = len(re.findall(r'@-webkit-keyframes', html))
    if kf != wkf: avisos.append("Keyframes nao pareados: @keyframes=%d @-webkit-keyframes=%d" % (kf, wkf))

    # 8) onclick sem funcao definida
    ocs = set(re.findall(r'onclick="([a-zA-Z_][a-zA-Z0-9_]*)\(', html))
    faltando = sorted([o for o in ocs if o not in set(fns)])
    if faltando: falhas.append("onclick sem funcao definida: " + ", ".join(faltando[:8]))

    # 9) EMOJI MODERNO (> Unicode 6.0 quebra em navegador antigo) — literais e entidades
    sem_img = re.sub(r'data:[^;]+;base64,[A-Za-z0-9+/=]+', '', html)
    def quebra(o):   # vira QUADRADINHO em navegador antigo (Unicode 7.0+ e tons de pele)
        return (0x1F3FB <= o <= 0x1F3FF) or o >= 0x1F900
    def cosmet(o):   # so cosmetico (o desenho-base ainda aparece): VS16 e ZWJ
        return o == 0xFE0F or o == 0x200D
    quebram, cosmeticos = {}, {}
    ords = [ord(c) for c in sem_img]
    ords += [int(m) for m in re.findall(r'&#(\d+);', sem_img)]
    ords += [int(m,16) for m in re.findall(r'&#x([0-9A-Fa-f]+);', sem_img)]
    for o in ords:
        if quebra(o): quebram[o] = True
        elif cosmet(o): cosmeticos[o] = True
    if quebram:
        falhas.append("Emoji moderno QUEBRA (vira quadradinho, use <= Unicode 6.0): " +
                      ", ".join("U+%04X"%o for o in sorted(quebram)))
    if cosmeticos:
        avisos.append("Emoji com modificador (VS16/ZWJ) — so cosmetico em navegador antigo: " +
                      ", ".join("U+%04X"%o for o in sorted(cosmeticos)))

    return falhas, avisos

# ---------- (B) CHECKLIST DE RECURSOS (o que a atividade tem) ----------
# Cada recurso: nome -> lista de padroes (regex). Presente se QUALQUER padrao casar.
RECURSOS = [
    ("reset55",    [r'__aulaInicio', r'_DUR_AULA', r'progVenceu', r'ESTADO\.inicio']),
    ("adap_extra", [r'iniciarExtra', r'ofereceExtra', r'Desafio Extra']),
    ("adap_reforco",[r'iniciarReforco', r'ofereceRef', r'Refor[cç]ar']),
    ("relatorio",  [r'telaRelatorio', r'\bimprimir\s*\(', r'relat[oó]rio do professor', r'window\.print']),
    ("narracao",   [r'speechSynthesis']),
    ("som",        [r'AudioContext', r'webkitAudioContext']),
    ("niveis",     [r'\bNIVEIS\b', r'nivelIdx', r'emblema']),
    ("medalhas",   [r'medal', r'medalha']),
    ("conquistas", [r'CONQUISTAS', r'conquista', r'\bselo']),
    ("streak",     [r'streak', r'Streak']),
]

def checar_recursos(html):
    feats = {}
    for nome, pats in RECURSOS:
        feats[nome] = any(re.search(p, html, re.I) for p in pats)
    return feats

def auditar(path):
    html = open(path, encoding="utf-8", errors="replace").read()
    falhas, avisos = checar_compat(html)
    feats = checar_recursos(html)
    return falhas, avisos, feats

def nome_curto(path):
    d = os.path.basename(os.path.dirname(path))
    return d if d and d not in (".","_novo","_lote") else os.path.basename(path)

def main(args):
    matriz = False
    if args and args[0] == "--matriz":
        matriz = True; args = args[1:]
    if not args:
        print("uso: python3 _circo/auditar-geral.py [--matriz] <index.html> [...]"); return 2

    resultados = []
    for p in args:
        if not os.path.isfile(p):
            print("!! nao achei: " + p); continue
        f, a, feats = auditar(p)
        resultados.append((nome_curto(p), f, a, feats))

    if matriz:
        cols = [r[0] for r in RECURSOS]
        cab = "%-26s | %-8s | " % ("ATIVIDADE", "COMPAT") + " ".join("%-3s"%c[:3] for c in [x[0] for x in RECURSOS])
        print(cab); print("-"*len(cab))
        for nome, f, a, feats in resultados:
            compat = "FALHA" if f else ("aviso" if a else "OK")
            cells = " ".join(("[x]" if feats[k] else " . ") for k,_ in RECURSOS)
            print("%-26s | %-8s | %s" % (nome[:26], compat, cells))
        print("\nlegenda recursos:", ", ".join(k for k,_ in RECURSOS))
        print("[x]=tem   . =nao tem   COMPAT: OK/aviso/FALHA (FALHA=quebra navegador antigo)")
        return 0

    rc = 0
    for nome, f, a, feats in resultados:
        print("=== " + nome + " ===")
        for x in f: print("  [FALHA] " + x)
        for x in a: print("  [aviso] " + x)
        faltando = [k for k,_ in RECURSOS if not feats[k]]
        print("  recursos que FALTAM: " + (", ".join(faltando) if faltando else "nenhum"))
        print("  -> " + ("REPROVADO" if f else "APROVADO" + (" (com avisos)" if a else "")))
        if f: rc = 1
    return rc

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
