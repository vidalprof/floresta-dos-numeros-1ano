#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDITOR DE PROVA — o "profissional" que faltava. Trava justamente a classe de
erros que escapou dos outros auditores numa PROVA/atividade de lateralidade:

  1) CONCORDANCIA escrito x falado: a pergunta (na tela) e a fala (narrador) da
     MESMA pista tem que combinar — mesmo eixo (cima/baixo x direita/esquerda) e
     mesma forma de genero.
  2) GENERO uniforme: direcao sempre no feminino ("direita/esquerda"), igual aos
     botoes. Flagra a forma masculina "direito/esquerdo" como direcao.
  3) GABARITO de lateralidade: recomputa a resposta certa (de costas = alinhado;
     de frente = espelho; par = lado do alvo; seta = sentido; vert = objeto de cima)
     e compara com o 'correta' do codigo.
  4) FINAL/FEEDBACK: numa prova, nao pode revelar certo/errado nem falar em
     "professora"/"registrado" para o aluno.
  5) ASSETS: cada pista 'masc' referencia a pose masc_<vista>_<lado>.png e o
     objeto <obj>.png; cada fala tem audio/<chave>.mp3. Tudo tem que existir.

Uso:  python3 _circo/auditar-prova.py _lote/<atividade>/index.html [--rigoroso]
      (--rigoroso: sai != 0 se houver QUALQUER erro — use antes de publicar)
"""
import sys, os, re


def chave_voz(t):
    s = re.sub(r"\s+", " ", t).strip()
    h = 5381
    for ch in s:
        h = ((h * 33) + ord(ch)) & 0xFFFFFFFF
    if h == 0:
        return "v0"
    digs = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    n = h
    while n > 0:
        out = digs[n % 36] + out
        n //= 36
    return "v" + out


def campos(item):
    d = {}
    for k in ("tipo", "vista", "lado", "aponta", "alvo", "obj", "cima", "baixo",
              "esq", "dir", "pergunta", "fala"):
        m = re.search(r'%s:"([^"]*)"' % k, item)
        if m:
            d[k] = m.group(1)
    m = re.search(r"correta:(\d+)", item)
    if m:
        d["correta"] = int(m.group(1))
    d["opcoes"] = re.findall(r't:"([^"]+)"', item)
    return d


def gabarito_esperado(q):
    t = q.get("tipo")
    if t == "vert":
        return "Em cima"          # o objeto de cima e' o alvo
    if t == "seta":
        return "Direita" if q.get("aponta") == "dir" else "Esquerda"
    if t == "par":
        return "Esquerda" if q.get("alvo") == "esq" else "Direita"
    if t == "masc":
        lado = q.get("lado")
        if q.get("vista") == "costas":
            return "Direita" if lado == "dir" else "Esquerda"
        # de frente = espelho
        return "Direita dele" if lado == "esq" else "Esquerda dele"
    return None


def auditar(src):
    h = open(src, encoding="utf-8").read()
    base = os.path.dirname(src)
    erros, avisos = [], []

    mbloco = re.search(r"var QUESTOES=\[(.*?)\n\];", h, re.S)
    if not mbloco:
        return ["Nao achei o array QUESTOES."], [], 0
    itens = re.split(r"\n\s*(?=\{tipo:)", mbloco.group(1).strip())

    MASC_DIR = re.compile(r"\b(direito|esquerdo)\b")   # forma masculina (direcao)
    FEM_DIR = re.compile(r"\b(direita|esquerda)\b")

    for i, raw in enumerate(itens, 1):
        q = campos(raw)
        perg = q.get("pergunta", "")
        fala = q.get("fala", "")
        tag = "Pista %d" % i

        # (1) concordancia de EIXO: cima/baixo x esquerda/direita
        perg_vert = bool(re.search(r"em cima|embaixo", perg, re.I))
        fala_vert = bool(re.search(r"em cima|embaixo", fala, re.I))
        perg_lr = bool(FEM_DIR.search(perg) or MASC_DIR.search(perg))
        fala_lr = bool(FEM_DIR.search(fala) or MASC_DIR.search(fala))
        if perg_vert != fala_vert or (perg_lr and fala_vert) or (fala_lr and perg_vert):
            erros.append("%s: eixo do escrito x falado nao bate (cima/baixo x direita/esquerda)." % tag)

        # (2) genero: direcao masculina é proibida (padrao = feminino)
        for nome, txt in (("escrito", perg), ("falado", fala)):
            m = MASC_DIR.search(txt)
            if m:
                erros.append("%s: %s usa forma MASCULINA '%s' (padronize p/ 'direita/esquerda')."
                             % (tag, nome, m.group(1)))
        # (2b) concordancia de genero entre escrito e falado
        if (FEM_DIR.search(perg) and MASC_DIR.search(fala)) or (MASC_DIR.search(perg) and FEM_DIR.search(fala)):
            erros.append("%s: genero da direcao diverge entre escrito e falado." % tag)

        # (3) gabarito
        esp = gabarito_esperado(q)
        cor = q.get("correta")
        ops = q.get("opcoes", [])
        if esp is not None and cor is not None and cor < len(ops):
            marcada = ops[cor].strip()
            if marcada != esp:
                erros.append("%s: GABARITO errado -> marca '%s', esperado '%s' (tipo=%s vista=%s lado=%s)."
                             % (tag, marcada, esp, q.get("tipo"), q.get("vista"), q.get("lado")))

        # (5) assets: pose + objeto + audio
        if q.get("tipo") == "masc":
            pose = "masc_%s_%s.png" % ("frente" if q.get("vista") == "frente" else "costas",
                                       "dir" if q.get("lado") == "dir" else "esq")
            if not os.path.exists(os.path.join(base, "img", pose)):
                erros.append("%s: falta a imagem da pose img/%s." % (tag, pose))
            if q.get("obj") and not os.path.exists(os.path.join(base, "img", q["obj"] + ".png")):
                erros.append("%s: falta o objeto img/%s.png." % (tag, q["obj"]))
        if fala:
            k = chave_voz(fala)
            if not os.path.exists(os.path.join(base, "audio", k + ".mp3")):
                erros.append("%s: falta o audio da fala (audio/%s.mp3)." % (tag, k))

    # (4) prova nao revela / nao fala em professora ao aluno
    is_prova = bool(re.search(r"URL_PLANILHA|FIREBASE_DB|enviarResultado", h))
    if is_prova:
        # texto renderizado (fora de comentarios): procura 'professora'/'registrad' em innerHTML
        for m in re.finditer(r'(innerHTML\s*=\s*|s\.innerHTML\s*=\s*)"([^"]*)"', h):
            txt = m.group(2)
            if re.search(r"professora|registrad", txt, re.I):
                erros.append("Final/feedback mostra ao aluno: \"%s\" (prova nao deve falar em professora/registro)." % txt[:60])
        # nao deve existir marcacao de acerto/erro visivel
        if re.search(r"acertou|voce errou|resposta certa|resposta correta", h, re.I):
            avisos.append("Ha texto que pode revelar certo/errado — confira se nao aparece ao aluno.")

    return erros, avisos, len(itens)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    rig = "--rigoroso" in sys.argv
    if not args:
        print("uso: python3 _circo/auditar-prova.py <arquivo.html> [--rigoroso]")
        sys.exit(2)
    src = args[0]
    if not os.path.exists(src):
        print("arquivo nao encontrado:", src)
        sys.exit(2)
    erros, avisos, n = auditar(src)
    print("  📋 AUDITOR DE PROVA — %d pistas verificadas" % n)
    for a in avisos:
        print("    ~ (aviso):", a)
    for e in erros:
        print("    ✗", e)
    ok = not erros
    print("== RESUMO PROVA: %s ==" % (
        "APROVADO (concordancia, genero, gabarito, final e assets OK)" if ok
        else "REPROVADO — %d erro(s) a corrigir antes de publicar" % len(erros)))
    sys.exit(1 if (rig and not ok) else 0)


if __name__ == "__main__":
    main()
