#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO DO GAME-FEEL — o som e o movimento ajudam ou cansam?

De onde veio: `_pesquisa/REGRAS-NEUROCIENCIA.md`, tabela "O QUE DÁ PARA MEDIR
SOZINHO" (itens 1, 2, 3, 5, 6, 7, 9 e 14). Pedido do Marcos (set/2026): *"faça
tudo que pedi para deixar tudo mais rápido, moderno, ágil, por isso você fez as
pesquisas"*. Pesquisa que não vira portão não muda atividade nenhuma.

O que ele REPROVA (código 1):
  R1  som de acerto/erro NÃO é Web Audio (só `new Audio()` de MP3 — atrasa, falha
      no PC sem alto-falante ligado e não deixa variar);
  R2  oscilador SEM envelope anti-clique (`gain.value=` seco em vez de
      `exponentialRampToValueAtTime`): o "tic" que estala no fone da criança;
  R3  o ERRO não é gentil: nota de erro mais longa que 0,25 s, ou mais alta que
      a de acerto — som de erro que castiga ensina a criança a não tentar;
  R6  não existe `prefers-reduced-motion` na folha — quem pediu menos movimento
      no sistema recebe confete, shake e brilho do mesmo jeito.

O que ele AVISA (sai no relatório, não segura a entrega):
  R5  `@keyframes` que anima `width/height/top/left/box-shadow/margin/...`
      (só `transform`/`opacity` são baratos no PC fraco da escola);
  R7  som de erro sem gêmeo visual perto (no mudo a criança não sabe que errou);
  R9  o áudio não destrava num gesto (`resume()` fora de pointerdown/click);
  R14 o som de acerto é sempre IDÊNTICO (nenhuma variação — o cérebro se
      habitua e a recompensa deixa de recompensar).

Códigos: 0 passou · 1 REPROVOU · 2 não mediu (sem JS).
Uso: python3 _qa/gamefeel.py <index.html | _padrao/pecas/x.html>
"""
import io
import re
import sys


def _js_css(html):
    js = u"\n".join(re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S))
    css = u"\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
    return js, css


def _corpo(js, nome):
    u"""corpo da `function nome(...){...}` — chaves casadas."""
    m = re.search(r"function\s+" + re.escape(nome) + r"\s*\([^)]*\)\s*\{", js)
    if not m:
        return None
    i = m.end()
    prof = 1
    while i < len(js) and prof:
        ch = js[i]
        if ch == "{":
            prof += 1
        elif ch == "}":
            prof -= 1
        i += 1
    return js[m.end():i - 1]


_NUM = r"([0-9.]+)"


def _notas(corpo):
    u"""lista de (duracao, volume, atraso) dos `tom(f,d,tp,v,w)` e
    `nota(f,dur,vol,tipo,atraso)` de um corpo de funcao."""
    out = []
    for m in re.finditer(r"\btom\(\s*[^,]+,\s*" + _NUM + r"\s*,\s*\"[a-z]+\"\s*,\s*" + _NUM
                         + r"(?:\s*,\s*" + _NUM + r")?", corpo):
        out.append((float(m.group(1)), float(m.group(2)), float(m.group(3) or 0)))
    for m in re.finditer(r"\bnota\(\s*[^,]+,\s*" + _NUM + r"\s*,\s*" + _NUM
                         + r"\s*,\s*\"[a-z]+\"\s*,\s*" + _NUM, corpo):
        out.append((float(m.group(1)), float(m.group(2)), float(m.group(3))))
    return out


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/gamefeel.py <arquivo.html>")
        return 2
    alvo = sys.argv[1]
    html = io.open(alvo, encoding="utf-8", errors="replace").read()
    js, css = _js_css(html)
    if not js.strip():
        print(u"%s -> NAO MEDI: nenhum <script> no arquivo" % alvo)
        return 2

    ruins, avisos = [], []

    # ---- R1: acerto/erro por Web Audio ------------------------------------
    cCerto = _corpo(js, "sCerto")
    cErro = _corpo(js, "sErro")
    if cCerto is None and cErro is None:
        avisos.append(u"nao achei sCerto()/sErro(): o portao nao reconhece o som desta pagina "
                      u"(motor da casa usa esses nomes)")
    for nome, c in (("sCerto", cCerto), ("sErro", cErro)):
        if c is None:
            continue
        usaOsc = bool(re.search(r"\b(tom|nota)\s*\(", c)) or "createOscillator" in c
        if not usaOsc and re.search(r"new\s+Audio\s*\(|\.play\s*\(", c):
            ruins.append(u"R1 %s() toca MP3 (`new Audio`) em vez de Web Audio: atrasa, falha "
                         u"no PC sem som liberado e nao varia. Use o oscilador (`tom`/`nota`)." % nome)

    # ---- R2: envelope anti-clique nos geradores de nota --------------------
    for ger in ("tom", "nota"):
        c = _corpo(js, ger)
        if c is None or "createOscillator" not in c:
            continue
        temRampa = "exponentialRampToValueAtTime" in c or "linearRampToValueAtTime" in c
        seco = re.search(r"gain\.value\s*=\s*[0-9.]*[1-9]", c)
        if not temRampa or seco:
            ruins.append(u"R2 %s(): oscilador sem envelope (falta a rampa 0,010–0,020 s no "
                         u"`gain`) — e o estalo que a crianca ouve no fone a cada toque." % ger)

    # ---- R3: o erro e gentil ----------------------------------------------
    if cErro is not None and cCerto is not None:
        nE, nC = _notas(cErro), _notas(cCerto)
        if nE and nC:
            durE = max(d for d, v, a in nE)
            fimE = max(d + a for d, v, a in nE)
            volE = max(v for d, v, a in nE)
            volC = max(v for d, v, a in nC)
            if durE > 0.25 + 1e-9:
                ruins.append(u"R3 sErro(): nota de erro dura %.2f s (limite 0,25 s). Erro longo e "
                             u"castigo, nao informacao." % durE)
            elif fimE > 0.40 + 1e-9:
                ruins.append(u"R3 sErro(): o som de erro inteiro leva %.2f s (limite 0,40 s)." % fimE)
            if volE > volC + 1e-9:
                ruins.append(u"R3 sErro() e mais ALTO (%.2f) que sCerto() (%.2f): o erro nao pode "
                             u"gritar mais que o acerto." % (volE, volC))

    # ---- R6: prefers-reduced-motion ----------------------------------------
    #    Na PECA avulsa e aviso: quem fornece a regra geral e o motor (ela e
    #    integrada e perde a folha propria). Na atividade montada, reprova.
    ePeca = "/pecas/" in alvo.replace("\\", "/")
    if "prefers-reduced-motion" not in css and "prefers-reduced-motion" not in js:
        if re.search(r"@(?:-webkit-)?keyframes", css):
            msg = (u"R6 a folha anima (@keyframes) mas nao tem `@media (prefers-reduced-motion: "
                   u"reduce)`: quem pediu menos movimento no sistema recebe tudo igual.")
            (avisos if ePeca else ruins).append(msg + (u" (na peca avulsa: o motor cobre ao integrar)" if ePeca else u""))

    # ---- R5 (aviso): so transform/opacity ----------------------------------
    caros = []
    for m in re.finditer(r"@(?:-webkit-)?keyframes\s+([\w-]+)\s*\{((?:[^{}]*\{[^{}]*\})*)\s*\}", css):
        props = set(re.findall(r"(?<![-\w])(width|height|top|left|right|bottom|box-shadow|"
                               r"margin[-\w]*|padding[-\w]*|font-size)\s*:", m.group(2)))
        if props:
            caros.append(u"%s(%s)" % (m.group(1), u",".join(sorted(props))))
    caros = sorted(set(caros))
    if caros:
        avisos.append(u"R5 %d @keyframes animam propriedade de LEIAUTE (repinta a tela inteira no "
                      u"PC fraco): %s — preferir transform/opacity" % (len(caros), u", ".join(caros[:8])))

    # ---- R7 (aviso): erro com gemeo visual ---------------------------------
    if cErro is not None:
        semGemeo = 0
        for m in re.finditer(r"(?<![\w.])sErro\s*\(\s*\)", js):
            ini = max(0, m.start() - 500)
            jan = js[ini:m.end() + 500]
            if re.search(r"className|classList|\.style\.|innerHTML|textContent|appendChild|"
                         r"mostraDica|ajuda\s*\(|dica\s*\(|acende|pisca|treme|shake|erra\w*\(|"
                         r"marca\w*\(|fala\w*\(|diz\s*\(|balao", jan):
                continue
            semGemeo += 1
        if semGemeo:
            avisos.append(u"R7 %d chamada(s) de sErro() sem mudanca visual por perto — no mudo a "
                          u"crianca nao sabe que errou" % semGemeo)

    # ---- R9 (aviso): audio destrava no gesto -------------------------------
    if "AudioContext" in js:
        destrava = re.search(r"\.resume\s*\(", js)
        # o MOLDE resume dentro de `ac()`, que toda nota chama — e toda nota nasce
        # de um toque (sTap no onclick). Basta haver resume + algum handler de gesto.
        gesto = re.search(r"onclick|addEventListener\s*\(\s*[\"'](pointerdown|touchstart|mousedown|click)", js)
        if not destrava:
            avisos.append(u"R9 ha AudioContext mas nenhum `resume()`: no Chrome novo o som fica "
                          u"mudo ate alguem destravar no gesto")
        elif not gesto:
            avisos.append(u"R9 `resume()` existe mas nao ha handler de gesto (onclick/pointerdown) "
                          u"nesta pagina — o som pode nunca destravar")

    # ---- R14 (aviso): acerto sempre identico -------------------------------
    if cCerto is not None and _notas(cCerto):
        if not re.search(r"Math\.random|\[\s*Math\.floor|\bk\b\s*=|var\s+\w+\s*=\s*_k", cCerto):
            avisos.append(u"R14 sCerto() toca SEMPRE a mesma frase: sem variacao, a recompensa "
                          u"vira ruido de fundo (habituacao). Uma leve troca de tom ja basta.")

    print(u"%s -> game-feel: %d regra(s) reprovada(s), %d aviso(s)" % (alvo, len(ruins), len(avisos)))
    for a in avisos:
        print(u"   aviso: %s" % a)
    if ruins:
        for r in ruins:
            print(u"   - %s" % r)
        return 1
    print(u"   som e movimento ok: oscilador com envelope, erro gentil, reduced-motion respeitado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
