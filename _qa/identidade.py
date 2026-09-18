# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO 0b11 — "IDENTIDADE PRÓPRIA": cada caderno de folha viva tem a SUA cor,
 a SUA capa e a SUA animação — nenhum é a cópia visual de outro.

 ⚠️ POR QUE EXISTE — ordem do Marcos, 18/set/2026, com a turma na frente:
    *"cada caderno precisa ter capa diferente, cor diferente animações etc,
    pois são muito parecidos e os estudantes acham que é a mesma atividade,
    mesmo o título sendo diferente"*.

    Medido no dia: os SEIS cadernos nascidos do esqueleto (`_sil2`, `_troca2`,
    `_nasal2`, `_ponto2`, `_casa1`, `_ing8`) tinham a MESMA cor (`--cor:#b0562a`,
    a telha da casa) e a MESMA capa (a rua de casas, com sol e nuvens — que é o
    tema de `_casa1` e de nenhum outro); os CINCO do 1º ano (`_rima1`, `_som1`,
    `_roda1`, `_abc1`, `_jogo1`) tinham todos o roxo `#6d5ae6`. A criança de sete
    anos não lê o título antes de decidir "isso eu já fiz": ela olha a cor e o
    desenho da capa. Título diferente com capa igual É a mesma atividade para ela.

 O QUE ELE MEDE (e reprova, código 1):
   1. COR — o `--cor` do `:root` (ou, nos cadernos antigos, a cor da borda do
      `#topo`) igual ao de outro caderno de folha viva.
   2. CAPA — o bloco de CSS da capa (do marcador `A CAPA` até o `#fim`), sem
      comentário e sem espaço, idêntico ao de outro caderno ou ao do ESQUELETO
      (`_padrao/FOLHA-VIVA`). Capa igual ao esqueleto = ninguém desenhou a capa.
   3. ANIMAÇÃO — o conjunto de `@keyframes` que a capa usa idêntico ao de outro
      caderno E a estrutura do HTML da capa (o `f0` do `folhas.js`, com o título
      tirado) também idêntica. Uma das duas pode coincidir; as duas juntas é a
      mesma capa com outra cor.
 O QUE ELE NÃO MEDE: se a capa é BONITA ou se tem a ver com o assunto. Isso é
 do Marcos (portão do professor). Ele mede só que não é a cópia de outra.

 Código 2 (NÃO MEDI) quando a pasta não tem `.capa` no CSS ou não tem `f0`.

 Uso: python3 _qa/identidade.py <pasta>          (a banca e o pré-voo)
      python3 _qa/identidade.py --todos          (a tabela de todos, informativa)
============================================================
"""
from __future__ import print_function
import io
import os
import re
import sys
import unicodedata

ESQUELETO = "_padrao/FOLHA-VIVA"


def le(cam):
    try:
        return io.open(cam, encoding="utf-8").read()
    except IOError:
        return u""


def cadernos():
    u"""Toda pasta com `folhas.js` + `index.html` é um caderno de folha viva."""
    out = []
    for d in sorted(os.listdir(".")):
        if not d.startswith("_") or d in ("_novo", "_padrao", "_recuperado"):
            continue
        if os.path.isfile(os.path.join(d, "folhas.js")) and os.path.isfile(os.path.join(d, "index.html")):
            out.append(d)
    return out


def sem_comentario(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def cor_de(html):
    m = re.search(r"--cor\s*:\s*(#[0-9a-fA-F]{3,8})", html)
    if m:
        return m.group(1).lower()
    m = re.search(r"#topo\{[^}]*border-bottom\s*:\s*\d+px\s+solid\s+(#[0-9a-fA-F]{3,8})", html)
    if m:
        return m.group(1).lower()
    return None


def bloco_capa(html):
    css = sem_comentario(html)
    i = css.find(".capa{")
    if i < 0:
        return None
    j = css.find("#fim,#retomar{", i)
    if j < 0:
        j = css.find("</style>", i)
    return re.sub(r"\s+", "", css[i:j])


def keyframes_da_capa(html):
    css = sem_comentario(html)
    i = css.find(".capa{")
    if i < 0:
        return None
    j = css.find("#fim,#retomar{", i)
    trecho = css[i:j if j > 0 else len(css)]
    nomes = set(re.findall(r"animation\s*:\s*([A-Za-z_][\w-]*)", trecho))
    nomes |= set(re.findall(r"@keyframes\s+([A-Za-z_][\w-]*)", trecho))
    nomes.discard("none")
    return frozenset(nomes)


def estrutura_f0(js):
    m = re.search(r"function f0\(d\)\{(.*?)\n\}", js, re.S)
    if not m:
        return None
    corpo = m.group(1)
    corpo = re.sub(r'nome\s*=\s*"[^"]*"', 'nome=""', corpo)   # o título sai
    corpo = re.sub(r"<div class=\"sub\">.*?</div>", "<div class=\"sub\"></div>", corpo, flags=re.S)
    return re.sub(r"\s+", "", corpo)


def classes_da_capa(js, html):
    u"""As classes que o `f0` usa DENTRO da capa, e as que têm regra fora dela.

    ⚠️ LIÇÃO PAGA — 18/set/2026, `_verbo4`: a figura da capa nasceu com
    `class="cf"`, e `.cf` é o CONFETE do motor (`position:absolute` +
    `animation:cai`, que acaba em `opacity:0` e 105vh abaixo). As cinco figuras
    estavam no DOM, com o tamanho certo e `visibility:visible` — e INVISÍVEIS na
    tela. O `leiaute_mao` não olha a capa; o `css_atregra` mede animação órfã, não
    animação ALHEIA. Quem viu foi a foto. Agora é medido.
    """
    m = re.search(r"function f0\(d\)\{(.*?)\n\}", js, re.S)
    if not m:
        return []
    usadas = set(re.findall(r'class=\\?"([^"\\]+)', m.group(1)))
    nomes = set()
    for u in usadas:
        for c in u.split():
            if c and c != "capa":
                nomes.add(c)
    css = sem_comentario(html)
    i = css.find(".capa{")
    j = css.find("#fim,#retomar{", i) if i >= 0 else -1
    fora = css[:i] + css[j:] if i >= 0 and j > 0 else css
    # ⚠️ NEM TODA COLISAO ESCONDE. `.capa .lt` (0,2,0) ganha de `.lt` (0,1,0) nas
    #    propriedades que a capa declara. O que MACHUCA e' a propriedade que a capa
    #    NAO declara e o motor declara: `position`, `animation`, `opacity`,
    #    `display`, `transform`, `visibility` — foi assim que `.cf` (confete) pos
    #    `position:absolute` + `animation:cai` na figura da capa e ela sumiu.
    PERIGO = ("position", "animation", "opacity", "display", "transform", "visibility")
    chocam = []
    for c in sorted(nomes):
        for m2 in re.finditer(r"(^|[\s,}])\.%s\s*\{([^}]*)\}" % re.escape(c), fora, re.M):
            corpo = m2.group(2)
            props = [p for p in PERIGO
                     if re.search(r"(^|;)\s*(-webkit-)?%s\s*:" % p, corpo)]
            if props:
                chocam.append("%s (o motor lhe da %s)" % (c, ", ".join(props)))
                break
    return chocam


def nome_da_capa(js):
    m = re.search(r'function f0\(d\)\{.*?nome = "([^"]*)"', js, re.S)
    return m.group(1) if m else None


def titulo(html):
    m = re.search(r"<title>([^<]*)</title>", html)
    return m.group(1) if m else None


def _chave(t):
    u"""só as letras, sem acento e sem caixa — para comparar nome e título"""
    if not t:
        return u""
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z]", "", t.lower())


def ficha(pasta):
    html = le(os.path.join(pasta, "index.html"))
    js = le(os.path.join(pasta, "folhas.js"))
    return {
        "pasta": pasta,
        "cor": cor_de(html),
        "capa": bloco_capa(html),
        "anim": keyframes_da_capa(html),
        "f0": estrutura_f0(js),
        "choque": classes_da_capa(js, html),
        "nome": nome_da_capa(js),
        "titulo": titulo(html),
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    todos = [ficha(p) for p in cadernos()]
    if sys.argv[1] == "--todos":
        print("%-10s %-9s %s" % ("pasta", "cor", "animacoes da capa"))
        for f in todos:
            print("%-10s %-9s %s" % (f["pasta"], f["cor"], ",".join(sorted(f["anim"] or []))))
        # e quem colide com quem
        print("\nCOLISOES (mesma cor):")
        vistos = {}
        for f in todos:
            vistos.setdefault(f["cor"], []).append(f["pasta"])
        for c, ps in vistos.items():
            if len(ps) > 1:
                print("   %s -> %s" % (c, ", ".join(ps)))
        return 0

    pasta = sys.argv[1].rstrip("/")
    eu = ficha(pasta)
    if eu["capa"] is None or eu["f0"] is None:
        print("%s -> NAO MEDI: nao achei `.capa{` no CSS ou `function f0` no folhas.js" % pasta)
        return 2
    esq = ficha(ESQUELETO) if os.path.isdir(ESQUELETO) else None
    erros = []
    # ⚠️ O NOME NA CAPA TEM DE SER O DESTE CADERNO (18/set/2026). Dois cadernos no
    #    ar mostravam o título de OUTRO — `_roda1` abria escrito "A FAMÍLIA DAS
    #    PALAVRAS" e `_mult2` abria "O ARMAZÉM DO MESMO TANTO". Resto de clone que
    #    nenhum portão via, e que é justamente o que faz a criança dizer
    #    "isso eu já fiz".
    if eu["nome"] and eu["titulo"]:
        # o <title> costuma ser "<Nome> — <ano>": basta que um seja PREFIXO do outro
        alvo, meu = _chave(eu["titulo"]), _chave(eu["nome"])
        if alvo and meu and not (alvo.startswith(meu) or meu.startswith(alvo)):
            erros.append(u"a CAPA diz `%s` e o <title> diz `%s`: o nome na capa e de OUTRO caderno."
                         % (eu["nome"], eu["titulo"]))
    for c in eu["choque"]:
        erros.append(u"a capa usa a classe `%s`, que TAMBEM tem regra fora da capa "
                     u"(classe do motor): o estilo do motor ganha e a peca da capa pode "
                     u"sumir — foi assim que `.cf` (o confete) apagou as figuras da capa." % c)
    for o in todos:
        if o["pasta"] == pasta:
            continue
        if eu["cor"] and o["cor"] == eu["cor"]:
            erros.append("COR igual a `%s` (%s): a crianca decide pela cor antes de ler o titulo." % (o["pasta"], eu["cor"]))
        if o["capa"] == eu["capa"]:
            erros.append("CAPA identica a `%s` (o mesmo CSS, byte a byte)." % o["pasta"])
        elif o["anim"] == eu["anim"] and o["f0"] == eu["f0"]:
            erros.append("mesma ANIMACAO e mesma estrutura de capa que `%s` (%s): e a mesma capa com outra cor."
                         % (o["pasta"], ",".join(sorted(eu["anim"] or [])) or "sem animacao"))
    if esq and esq["capa"] == eu["capa"]:
        erros.append("CAPA identica ao ESQUELETO `%s`: ninguem desenhou a capa deste caderno." % ESQUELETO)
    if esq and esq["cor"] and eu["cor"] == esq["cor"]:
        erros.append("COR igual a do ESQUELETO (%s): a cor do caderno tem que ser escolhida pelo assunto dele." % eu["cor"])

    print("%s -> cor %s · animacoes da capa: %s · %d caderno(s) comparados"
          % (pasta, eu["cor"], ",".join(sorted(eu["anim"] or [])) or "nenhuma", len(todos) - 1))
    if erros:
        print("   REPROVOU (identidade propria — Marcos, 18/set/2026: \"os estudantes acham que e a mesma atividade\"):")
        for e in sorted(set(erros)):
            print("    - " + e)
        print("   Conserto: trocar `--cor/--cor2/--corclara` no :root e redesenhar o bloco `A CAPA`")
        print("   (fundo, cena e @keyframes com nome proprio) + o `f0` do folhas.js, a partir do ASSUNTO do caderno.")
        return 1
    print("   ok: nenhum outro caderno tem esta cor, esta capa ou esta animacao.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
