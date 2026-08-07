#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""O MONTADOR — conteúdo entra, atividade sai.

Meta do Marcos (ago/2026): *"precisamos otimizar o processo a ponto de conseguir
deixar uma atividade inteira com o esqueleto em minutos e não em horas — e claro
que fique profissional e fantástica"*.

O que fazia levar horas era eu **escrever o motor de novo** em cada atividade: o
caça-palavras, a memória, o arrastar, o teclado. É aí que iam as horas, e é de lá
que saíam os defeitos que chegavam nele.

Aqui a atividade deixa de ser código e passa a ser **conteúdo**:

    conteudo.json  ──▶  montar.py  ──▶  index.html   (a atividade)
                                        falas.json   (as vozes)
                                        arte.json    (o que falta desenhar)

⭐ O GANHO QUE NÃO É TEMPO: **o `falas.json` é gerado do próprio enunciado.**
   Fica impossível a voz dizer coisa diferente da tela — o defeito que ele cobrou
   três vezes num só dia deixa de existir por construção, não por eu lembrar de
   conferir.

⭐ E NÃO HÁ DE ONDE CLONAR. O motor é o mesmo para todas; o conteúdo é novo. A
   família inteira de "resto de clone" (a pré-carga da origem, o alto-falante da
   origem, os conceitos da origem) desaparece.

O MODELO É O JARDIM DO BROTO (ordem dele): capa → crachá → fases → boletim com
medalha → relatório do professor escondido. Ver `CONTRATO.md`.

Uso:
  python3 _padrao/ESQUELETO/montar.py <pasta>          # monta a atividade
  python3 _padrao/ESQUELETO/montar.py <pasta> --so-ver # só confere, não escreve
"""
import io
import json
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))

# as mecânicas que existem na oficina (a fonte da verdade é a pasta de peças)
def mecanicas():
    d = os.path.join(RAIZ, "_padrao", "pecas")
    if not os.path.isdir(d):
        return set()
    return set(f[:-5] for f in os.listdir(d)
               if f.endswith(".html") and f != "MOLDE.html")


def simples(s):
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def texto_limpo(h):
    u"""o que a criança OUVE é o que ela LÊ — sem marcação, sem entidade."""
    s = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), h or "")
    s = s.replace("&amp;", "&").replace("&nbsp;", " ")
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()


# ------------------------------------------------------------------ conferência
def confere(c, mecs):
    u"""O montador é o primeiro portão: erro de conteúdo não vira HTML."""
    p, avisos = [], []
    for campo in ("titulo", "ano", "mascote", "prefixo", "fases"):
        if not c.get(campo):
            p.append(u"falta o campo obrigatorio '%s'" % campo)
    if p:
        return p, avisos

    fases = c["fases"]
    n = len(fases)
    if n < 8:
        p.append(u"so %d fase(s): o combinado sao 32 (ou perto disso)" % n)

    ano = str(c.get("ano", "")).lower()
    pequeno = any(x in ano for x in ("pre", "pré", "1", "2"))
    minimo = 10 if pequeno else 16

    vistos, ordem = {}, []
    for i, f in enumerate(fases):
        onde = u"fase %d (%s)" % (i + 1, f.get("id") or "sem id")
        for campo in ("id", "mec", "selo", "enunciado"):
            if not f.get(campo):
                p.append(u"%s: falta '%s'" % (onde, campo))
        m = f.get("mec")
        if m and mecs and m not in mecs:
            p.append(u"%s: a mecanica '%s' nao existe na oficina "
                     u"(_padrao/pecas/). Escreva a peca dela antes." % (onde, m))
        if m:
            vistos[m] = vistos.get(m, 0) + 1
            ordem.append(m)
        if not f.get("dica"):
            avisos.append(u"%s: sem dica — o 1o degrau do andaime fica vazio" % onde)
        if not f.get("conceito"):
            avisos.append(u"%s: sem conceito — esta fase nao entra no parecer "
                          u"do professor" % onde)

    # ⚠️ a regra que o Marcos pediu: variedade contada por GESTO
    if len(vistos) < minimo:
        p.append(u"so %d mecanica(s) diferente(s); o combinado para este ano sao "
                 u"%d (ver CONTRATO.md)" % (len(vistos), minimo))
    for m, q in sorted(vistos.items()):
        if n and q / float(n) > 0.40:
            p.append(u"a mecanica '%s' ocupa %d%% das fases (teto: 40%%)"
                     % (m, round(100.0 * q / n)))
    # ⚠️ vizinhança: duas fases seguidas com o mesmo gesto e "a mesma tela pela
    #    terceira vez", mesmo que o conteudo mude
    for i in range(1, len(ordem)):
        if ordem[i] == ordem[i - 1]:
            p.append(u"as fases %d e %d usam a MESMA mecanica ('%s') coladas — "
                     u"a segunda vez tem que vir depois, e um degrau acima"
                     % (i, i + 1, ordem[i]))
    # aquecimento no meio
    aq = next((i for i, f in enumerate(fases)
               if "quec" in (f.get("id", "") + f.get("mec", "")).lower()
               or "quec" in texto_limpo(f.get("selo", "")).lower()), None)
    if aq is None:
        avisos.append(u"nao ha AQUECIMENTO (a revisao no meio da aula) — e ela "
                      u"que faz o aprendido ficar")
    else:
        pos = (aq + 1) / float(n)
        if pos < 0.25 or pos > 0.65:
            p.append(u"o AQUECIMENTO esta em %d%% do caminho; ele vai no MEIO "
                     u"(entre 25%% e 65%%)" % round(pos * 100))
    return p, avisos


# ------------------------------------------------------------------ as vozes
def falas_de(c):
    u"""O falas.json sai do TEXTO DA TELA. É isto que torna impossível a voz
    dizer uma coisa e a tela outra."""
    pre = c["prefixo"].rstrip("_")
    out, vistos = [], set()

    def poe(ident, txt):
        t = texto_limpo(txt)
        if not t or ident in vistos:
            return
        vistos.add(ident)
        out.append({"id": ident, "texto": t})

    poe(pre + "_abertura", c.get("abertura") or c.get("titulo"))
    for f in c["fases"]:
        i = f["id"]
        poe("%s_%s_intro" % (pre, i), f.get("enunciado"))
        if f.get("dica"):
            poe("%s_%s_dica" % (pre, i), f["dica"])
        if f.get("revela"):
            poe("%s_%s_revela" % (pre, i), f["revela"])
        # ⚠️ VOZ POR RODADA: se o enunciado muda dentro da fase, cada item tem a
        #    SUA voz. Sem isto, a crianca que nao le fica sem instrucao do 2o
        #    item em diante — foi o defeito achado no Jardim do Broto.
        for it in (f.get("itens") or []):
            if isinstance(it, dict) and it.get("pergunta"):
                poe("%s_%s_%s" % (pre, i, simples(it.get("k") or it.get("n") or "")),
                    it["pergunta"])
        # alto-falante de cada resposta tocavel
        for it in (f.get("itens") or []) + (f.get("opcoes") or []):
            nome = it.get("n") if isinstance(it, dict) else it
            if nome:
                poe("op_" + chave_voz(texto_limpo(nome)), nome)
    poe(pre + "_fim", c.get("fim") or u"Você conseguiu!")
    return out


def chave_voz(s):
    u"""a mesma conta do `chaveVoz` das atividades (djb2 em base 36) — assim a
    mesma frase sempre dá o mesmo arquivo, aqui e lá."""
    s = re.sub(r"\s+", " ", s or "").strip().lower()
    h = 5381
    for ch in s:
        h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
    if h == 0:
        return "0"
    dig, out = "0123456789abcdefghijklmnopqrstuvwxyz", ""
    while h:
        out = dig[h % 36] + out
        h //= 36
    return out


# ------------------------------------------------------------------ a arte
def arte_de(c):
    u"""O que a atividade precisa desenhar — e o que o BANCO já resolve.
    É o passo que economiza dinheiro: o que já existe não se gera."""
    pedidos = []
    for f in c["fases"]:
        for it in (f.get("itens") or []) + (f.get("opcoes") or []):
            if isinstance(it, dict) and it.get("img"):
                pedidos.append(it["img"])
        if f.get("img"):
            pedidos.append(f["img"])
    pedidos = sorted(set(pedidos))

    banco = {}
    cam = os.path.join(RAIZ, "_banco", "index.json")
    if os.path.exists(cam):
        banco = json.load(io.open(cam, encoding="utf-8"))["objetos"]
    chaves = dict((simples(n), n) for n in banco)

    tem, falta = [], []
    for p in pedidos:
        k = chaves.get(simples(p))
        (tem if k else falta).append(k or p)
    return {"pedidos": pedidos, "no_banco": tem, "gerar": falta}


# ------------------------------------------------------------------ o HTML
def escreve_index(pasta, c, falas):
    u"""motor + SÓ as mecânicas usadas + o conteúdo = a atividade.

    ⚠️ SÓ AS USADAS, e isto não é economia de disco: é o PC da escola. As 74
    peças juntas dão 913 KB de JS. Uma atividade usa 16 — leva ~1/5 disso. Pôr
    tudo faria o AMD FX-4300 com 3,5 GB engasgar na abertura, e a criança
    olharia uma tela branca achando que quebrou."""
    motor = io.open(os.path.join(AQUI, "motor.html"), encoding="utf-8").read()
    usadas = []
    for f in c["fases"]:
        if f.get("mec") and f["mec"] not in usadas:
            usadas.append(f["mec"])

    js_pecas = recorta(os.path.join(AQUI, "pecas.js"), usadas)
    css_pecas = recorta(os.path.join(AQUI, "pecas.css"), usadas)

    pre = c["prefixo"].rstrip("_")
    dados = [u"\n/* ====== O CONTEUDO DESTA ATIVIDADE (escrito pelo montador) ====== */"]
    dados.append(u"ABERTURA = {texto:%s, voz:%s};"
                 % (jstr(c.get("abertura") or ""), jstr(pre + "_abertura")))
    fases = []
    for f in c["fases"]:
        d = dict(f)
        d["vozIntro"] = "%s_%s_intro" % (pre, f["id"])
        if f.get("dica"):
            d["dicaVoz"] = "%s_%s_dica" % (pre, f["id"])
        fases.append(d)
    dados.append(u"FASES = " + json.dumps(fases, ensure_ascii=False) + u";")
    dados.append(u"VOZOK = " + json.dumps(
        dict((x["id"][3:], 1) for x in falas if x["id"].startswith("op_")),
        ensure_ascii=False) + u";")

    saida = motor
    saida = saida.replace(u"</style>", css_pecas + u"\n</style>", 1)
    saida = saida.replace(u"</script>\n</body>",
                          js_pecas + u"\n" + u"\n".join(dados) + u"\n</script>\n</body>", 1)
    saida = saida.replace(u"<title>MOTOR — esqueleto</title>",
                          u"<title>%s</title>" % c.get("titulo", "Atividade"), 1)
    io.open(os.path.join(pasta, "index.html"), "w", encoding="utf-8").write(saida)


def jstr(s):
    return json.dumps(s, ensure_ascii=False)


def recorta(caminho, nomes):
    u"""tira do arquivo gerado só os pedaços das mecânicas usadas.

    ⚠️ LIÇÃO PAGA: a marca de peça tem que ser uma marca que NENHUMA peça
    escreva por acaso. A primeira era `/* ---------- nome ---------- */` e as
    próprias peças usam esse traço nos comentários delas — 163 marcas para 74
    peças. O recorte partia a peça no primeiro comentário interno e a atividade
    saía com meia mecânica: JS quebrado na mão da criança."""
    if not os.path.exists(caminho) or not nomes:
        return u""
    txt = io.open(caminho, encoding="utf-8").read()
    fora = []
    for bloco in re.split(r"(?=/\* ==== PECA: )", txt):
        m = re.match(r"/\* ==== PECA: ([\w-]+) ==== \*/", bloco)
        if m and m.group(1) in nomes:
            fora.append(bloco)
    achadas = set(re.match(r"/\* ==== PECA: ([\w-]+) ==== \*/", b).group(1)
                  for b in fora)
    for n in nomes:
        if n not in achadas:
            print(u"   AVISO: a mecanica '%s' nao esta em %s — rode "
                  u"integrar.py --escrever" % (n, os.path.basename(caminho)))
    return u"".join(fora)


# ------------------------------------------------------------------ principal
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    pasta = sys.argv[1].rstrip("/")
    so_ver = "--so-ver" in sys.argv
    cam = os.path.join(pasta, "conteudo.json")
    if not os.path.exists(cam):
        print(u"nao achei %s" % cam)
        return 2
    c = json.load(io.open(cam, encoding="utf-8"))

    problemas, avisos = confere(c, mecanicas())
    print(u"MONTADOR — %s (%s, %d fase(s))"
          % (c.get("titulo", "?"), c.get("ano", "?"), len(c.get("fases", []))))
    for a in avisos:
        print(u"   aviso: %s" % a)
    if problemas:
        print(u"   %d PROBLEMA(S) — nada foi gerado:" % len(problemas))
        for p in problemas:
            print(u"    - %s" % p)
        return 1

    falas = falas_de(c)
    arte = arte_de(c)
    print(u"   escada ok | %d fala(s) a gravar | %d figura(s): %d ja no banco, "
          u"%d a gerar" % (len(falas), len(arte["pedidos"]),
                           len(arte["no_banco"]), len(arte["gerar"])))
    if arte["gerar"]:
        print(u"   a gerar (EM CARTELA — `python3 _padrao/cartela.py plano`): %s"
              % ", ".join(arte["gerar"][:12]))
    if so_ver:
        print(u"   (--so-ver: nada foi escrito)")
        return 0

    escreve_index(pasta, c, falas)
    io.open(os.path.join(pasta, "falas.json"), "w", encoding="utf-8").write(
        json.dumps(falas, ensure_ascii=False, indent=1))
    io.open(os.path.join(pasta, "arte.json"), "w", encoding="utf-8").write(
        json.dumps(arte, ensure_ascii=False, indent=1))
    print(u"   escrito: %s/index.html, falas.json e arte.json" % pasta)
    return 0


if __name__ == "__main__":
    sys.exit(main())
