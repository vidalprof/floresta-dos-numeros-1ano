# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO 1c2 — DUPLICATA IGUAL: dois nomes, a MESMA figura, na mesma atividade.

 Nasceu da auditoria do banco (set/2026, `_banco/AUDITORIA.md`), no mesmo dia em
 que o testador humano achou o kiwi no lugar do hipopotamo. A conta deu 13
 pares assim dentro das atividades:

   · `_padaria`  pd_l_I = pd_l_H       -> a letra I em pao e a figura do H
   · `_clima`    nara_aponta = nara_acena -> duas poses do mascote, o mesmo desenho
   · `_central`  ce_mascote_fala = _pisca = _feliz -> mascote sem camadas
   · `_trem`     tr_coru_fala = tr_coru_feliz     -> a coruja fala de boca fechada

 Nenhum deles da erro: a imagem carrega (o `imagens.js` passa), o nome existe (o
 `clone.py` passa), o `node --check` passa. A crianca e que ve a MESMA figura
 em dois lugares que prometem coisas diferentes. Por isso o portao compara o
 CONTEUDO (sha1), nao o nome.

 O que REPROVA (codigo 1): duas imagens identicas, com nomes diferentes, e as
 DUAS usadas pelo `index.html` — a crianca ve as duas.

 ⭐ 2a MEDIDA (set/2026) — NOME DE PECA DE INTERFACE QUE COLIDE COM PALAVRA DO
    POTE. A estrelinha da medalha chamava-se `xx_estrela.png` e era carregada por
    um caminho LITERAL no codigo. No dia em que a palavra ESTRELA entrou no pote
    de um caderno de alfabetizacao, o `img("estrela")` passou a montar exatamente
    o mesmo caminho — e a crianca via o selo dourado da medalha no lugar do
    desenho da estrela. Nada quebrava: o arquivo existe, a imagem carrega, o
    `node --check` passa. Por isso o portao compara os dois mundos: todo caminho
    `img/<prefixo><nome>` escrito LITERALMENTE no codigo e peca de interface (as
    figuras do pote nascem de `img/<prefixo>' + palavra`), e nenhum desses nomes
    pode ser tambem uma palavra do `var PAL`.
 O que so AVISA: a duplicata existe na pasta mas so um nome (ou nenhum) e usado
 pela atividade. Ainda e sujeira no banco (o `_banco/montar.py` copia a figura
 errada com o nome errado), mas nao chega na crianca hoje.

 COPIAS DECLARADAS (nao reprovam):
   · cracha = avatar (`xx_cr3` = `xx_av3`): a plaquinha "Quem vai jogar?" usa o
     mesmo retrato do avatar, de proposito.
   · o que estiver em `<pasta>/_copias_ok.json`:
       {"copias": [{"nomes": ["bl_mapa", "bl_fundo"], "porque": "..."}]}
     Declarar e decisao; o portao imprime a razao para ela ficar visivel.

 Codigos: 0 passou · 1 REPROVOU · 2 nao consegui medir.
 Uso: python3 _qa/duplicatas.py <arquivo.html|pasta>
============================================================
"""
import hashlib
import io
import json
import os
import re
import sys

alvo = sys.argv[1] if len(sys.argv) > 1 else ""
if not alvo:
    print(u"uso: python3 _qa/duplicatas.py <arquivo.html|pasta>")
    sys.exit(2)
pasta = alvo if os.path.isdir(alvo) else os.path.dirname(os.path.abspath(alvo))
pasta = os.path.relpath(pasta)
arq = alvo if os.path.isfile(alvo) else os.path.join(pasta, "index.html")
img = os.path.join(pasta, "img")
if not os.path.isdir(img):
    print(u"%s -> sem pasta img/ (nada a conferir)" % pasta)
    sys.exit(0)

html = io.open(arq, encoding="utf-8").read() if os.path.isfile(arq) else u""
# tambem vale o que o motor le do conteudo.json (a fita do alfabeto, as pecas)
extra = u""
for nome_json in ("conteudo.json", "arte.json"):
    cam = os.path.join(pasta, nome_json)
    if os.path.isfile(cam):
        try:
            extra += io.open(cam, encoding="utf-8").read()
        except Exception:
            pass


def usada(nome):
    u"""o nome da figura aparece no index.html (ou no conteudo que o gera)?"""
    padrao = re.compile(r'(?<![A-Za-z0-9_])' + re.escape(nome) + r'(?![A-Za-z0-9_])')
    return bool(padrao.search(html)) or bool(padrao.search(extra))


# copias declaradas
declaradas = []
cam_ok = os.path.join(pasta, "_copias_ok.json")
if os.path.isfile(cam_ok):
    try:
        d = json.load(io.open(cam_ok, encoding="utf-8"))
        for c in d.get("copias", []):
            declaradas.append((set(c.get("nomes", [])), c.get("porque", u"")))
    except Exception as e:
        print(u"   aviso: _copias_ok.json ilegivel (%s)" % e)


def declarada(nomes):
    s = set(nomes)
    # cracha = avatar: xx_cr3 e xx_av3 (ou cr3/av3) sao o mesmo retrato de proposito
    if len(s) == 2:
        a, b = sorted(s)
        if re.sub(r"_?cr(\d+)$", r"_av\1", a) == b or re.sub(r"_?cr(\d+)$", r"_av\1", b) == a:
            return u"cracha = avatar (mesmo retrato, de proposito)"
    for conj, porque in declaradas:
        if s <= conj:
            return u"declarada em _copias_ok.json: %s" % (porque or u"(sem razao escrita)")
    return None


grupos = {}
total = 0
for f in sorted(os.listdir(img)):
    if not f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        continue
    total += 1
    cam = os.path.join(img, f)
    try:
        sha = hashlib.sha1(io.open(cam, "rb").read()).hexdigest()
    except Exception:
        continue
    grupos.setdefault(sha, []).append(os.path.splitext(f)[0])

# ---- 2a medida: peca de INTERFACE com nome de palavra do pote -----------------
fontes = html
for extra_js in ("folhas.js", "app.js", "pecas.js"):
    cam_js = os.path.join(pasta, extra_js)
    if os.path.isfile(cam_js):
        try:
            fontes += io.open(cam_js, encoding="utf-8").read()
        except Exception:
            pass

pote = set()
m_pal = re.search(r"var PAL\s*=\s*\{(.*?)\n\};", fontes, re.S)
if m_pal:
    pote = set(re.findall(r'(\w+)\s*:\s*\[', m_pal.group(1)))

colisoes = []
if pote:
    vistos = set()
    for bruto, _off in re.findall(
            r'''["']img/([A-Za-z0-9_]+?)(_off)?(?:\.png|\.jpg|\.jpeg|\.webp|["'])''', fontes):
        if bruto.endswith("_"):          # `img/mo_` + palavra -> figura do pote, nao interface
            continue
        nu = re.sub(r"^[A-Za-z]{1,4}_", "", bruto)
        if nu in pote and nu not in vistos:
            vistos.add(nu)
            colisoes.append((bruto, nu))

for bruto, nu in colisoes:
    print(u"   REPROVA img/%s  — este caminho esta escrito LITERALMENTE no codigo "
          u"(e peca de INTERFACE), mas `%s` tambem e uma palavra do pote: o "
          u"`img(\"%s\")` monta o MESMO arquivo e a crianca ve a peca de interface "
          u"no lugar do desenho. Renomeie a peca de interface (ex.: `selo`)."
          % (bruto, nu, nu))

pares = [g for g in grupos.values() if len(g) > 1]
if not pares:
    if colisoes:
        print(u"%s -> %d imagem(ns); REPROVADO: %d nome(s) de interface colidindo com "
              u"palavra do pote" % (pasta, total, len(colisoes)))
        sys.exit(1)
    print(u"%s -> %d imagem(ns), nenhuma duplicata com nome diferente" % (pasta, total))
    sys.exit(0)

reprovas, avisos, ok = [], [], []
for g in pares:
    razao = declarada(g)
    if razao:
        ok.append((g, razao))
        continue
    em_uso = [n for n in g if usada(n)]
    if len(em_uso) >= 2:
        reprovas.append((g, em_uso))
    else:
        avisos.append((g, em_uso))

print(u"%s -> %d imagem(ns), %d grupo(s) de arquivos IDENTICOS com nomes diferentes"
      % (pasta, total, len(pares)))
for g, razao in ok:
    print(u"   ok     %s  (%s)" % (u" = ".join(g), razao))
for g, em_uso in avisos:
    print(u"   AVISO  %s  — a MESMA figura com dois nomes; %s. Sujeira no banco: "
          u"regerar ou apagar o nome que nao e."
          % (u" = ".join(g), (u"so `%s` e usada pela atividade" % em_uso[0]) if em_uso
             else u"nenhum dos nomes e usado pelo index.html"))
for g, em_uso in reprovas:
    print(u"   REPROVA %s  — a crianca ve a MESMA figura em %d lugares que prometem "
          u"coisas diferentes (%s). Regerar a(s) que falta(m) ou declarar a copia em "
          u"%s/_copias_ok.json com a razao."
          % (u" = ".join(g), len(em_uso), u", ".join(em_uso), pasta))

if reprovas or colisoes:
    print(u"REPROVADO: %d duplicata(s) que a crianca ve + %d colisao(oes) "
          u"interface x pote" % (len(reprovas), len(colisoes)))
    sys.exit(1)
print(u"passou (%d aviso(s) de sujeira no banco)" % len(avisos) if avisos else u"passou")
sys.exit(0)
