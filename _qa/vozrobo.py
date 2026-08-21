# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — "toda voz é GRAVADA?" (nada de voz-robô do navegador)

 ⚠️ LIÇÃO PAGA (ago/2026), e foi o Marcos quem ouviu, com a atividade na mão:
 *"onde tenho que ouvir a palavra não funciona, tem o enunciado que funciona,
 o som da palavra que não funciona. os sons nas opções de respostas
 funcionam"*.

 Um único botão mudo, no meio de tudo funcionando — e o botão mais importante
 daquela fase, porque a fase inteira é OUVIR a palavra e achar a figura.

 A CAUSA VERDADEIRA — e a minha primeira explicação estava errada, o que vale
 registrar: eu escrevi que "no PC da escola não há voz pt-BR instalada". Não é
 isso. Fomos NÓS que desligamos a voz do navegador, de propósito, e está escrito
 no integrador: o Marcos tinha pegado antes *"tem voz do navegador junto com a
 voz do Antonio e às vezes os dois falam ao mesmo tempo"*, e a ponte passou a
 neutralizar o `speechSynthesis` em três camadas.

 O guarda estava certo. Só que a peça `ouvir-achar` usava exatamente essa voz
 para dizer A PALAVRA — o coração daquela fase. Consertamos as duas vozes
 falando juntas e, sem perceber, emudecemos o botão mais importante dela.

 É o defeito mais traiçoeiro que existe: nasceu de um conserto.

 O enunciado e os alto-falantes das respostas funcionavam porque passam pelo
 motor, que toca MP3 gravado com a voz da casa (Edge TTS).

 A REGRA DA CASA, agora medida: **toda voz que a criança ouve é gravada.** A
 ponte do integrador já reaponta o `diz` das peças para a voz do motor; este
 portão existe para que ninguém possa desfazer isso sem que a banca perceba.

 O QUE ESTE PORTÃO FAZ: procura `speechSynthesis` na atividade montada e exige
 que ele só apareça como ÚLTIMO RECURSO — depois de a ponte ter tentado a voz
 gravada (`temVoz`). Se uma peça chamar a voz-robô direto, reprova.

 Uso: python3 _qa/vozrobo.py <arquivo.html>
============================================================
"""
import io
import re
import sys


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/vozrobo.py <arquivo.html>")
        return 2
    arq = sys.argv[1]
    html = io.open(arq, encoding="utf-8").read()
    js = u"\n".join(re.findall(r"<script(?![^>]*src)[^>]*>(.*?)</script>",
                               html, re.S))
    if u"speechSynthesis" not in js:
        print(u"%s -> nenhuma voz-robo no arquivo" % arq)
        print(u"   voz ok: tudo o que a crianca ouve e gravado")
        return 0

    # ⚠️ SEGUNDA VERSÃO (no mesmo dia): a primeira acusou 36 usos e TODOS eram
    #    código morto. A ponte do integrador reaponta o `diz` da peça
    #    (`var diz = function(...)` com `temVoz` dentro) ANTES do corpo dela;
    #    a `function diz(){...speechSynthesis...}` que a peça declara é içada
    #    pelo JavaScript e logo em seguida SUBSTITUÍDA pela da ponte. Ela
    #    continua escrita no arquivo e nunca roda.
    #    Medido no navegador, para não ficar no "eu acho": apertando OUVIR na
    #    Padaria, o que toca é `op_377imf.mp3` — MP3 gravado — e a voz-robô é
    #    chamada ZERO vezes.
    #    Então a conta é por BLOCO: peça com a ponte religada está fechada;
    #    o que sobra é o que a criança pode mesmo ouvir (ou não ouvir).
    def blocos(t):
        u"""[(inicio, fim, religado)] de cada MEC[...] + o resto do arquivo."""
        saida, i = [], 0
        for m in re.finditer(r'MEC\["[a-z0-9\-]+"\]\s*=\s*function', t):
            j = t.find("{", m.end())
            if j < 0:
                continue
            prof, k = 0, j
            while k < len(t):
                if t[k] == "{":
                    prof += 1
                elif t[k] == "}":
                    prof -= 1
                    if prof == 0:
                        break
                k += 1
            corpo = t[j:k + 1]
            religado = bool(re.search(r"var\s+diz\s*=\s*function", corpo)
                            and re.search(r"\btemVoz\s*\(", corpo))
            saida.append((j, k + 1, religado))
            i = k + 1
        return saida

    fechados = [(a, b) for a, b, r in blocos(js) if r]

    def dentro_de_fechado(pos):
        return any(a <= pos < b for a, b in fechados)

    ruins, ok = [], 0
    for m in re.finditer(r"speechSynthesis", js):
        if dentro_de_fechado(m.start()):
            ok += 1
            continue
        # o GUARDA que desliga a voz-robô também contém a palavra
        # `speechSynthesis` — e ele é o contrário de um defeito. Reconhece-se
        # pelo objeto inerte e pelo `defineProperty` ao redor.
        # ⚠️ e o COMENTARIO do guarda tambem cita a palavra — inclusive no meio
        #    de um bloco /* */, onde a linha nem comeca com `*`. Comentario nao
        #    chama voz nenhuma: acusar texto explicativo e ruido puro, e ruido e
        #    o que faz portao virar coisa que se ignora.
        abre = js.rfind("/*", 0, m.start())
        fecha = js.rfind("*/", 0, m.start())
        if abre > fecha:                      # esta dentro de um /* ... */
            ok += 1
            continue
        linha_txt = js[js.rfind("\n", 0, m.start()) + 1:js.find("\n", m.start())]
        if linha_txt.lstrip().startswith("//"):
            ok += 1
            continue
        volta = js[max(0, m.start() - 400):m.start() + 200]
        if "inerte" in volta or "defineProperty" in volta or "vazio" in volta:
            ok += 1
            continue
        antes = js[max(0, m.start() - 700):m.start()]
        if re.search(r"\btemVoz\s*\(", antes) or re.search(r"\btocaVoz\s*\(", antes):
            ok += 1
        else:
            linha = js[:m.start()].count("\n") + 1
            ruins.append(linha)

    print(u"%s -> %d uso(s) de voz-robo conferido(s)" % (arq, ok + len(ruins)))
    if not ruins:
        print(u"   voz ok: a voz-robo so entra depois de a gravada faltar")
        return 0

    print(u"   %d VOZ(ES)-ROBO SEM A GRAVADA ANTES — no PC da escola isso e "
          u"SILENCIO, e falha calada:" % len(ruins))
    for l in ruins[:8]:
        print(u"    - linha %d do JS: chama speechSynthesis sem tentar `temVoz` antes" % l)
    print(u"   conserto: a ponte do integrador reaponta o `diz` da peca para a "
          u"voz do motor (ver integrar.py). Toda voz que a crianca ouve e gravada.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
