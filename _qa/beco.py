# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO DO BECO SEM SAÍDA — "a fase tem como continuar?"

 ⚠️ LIÇÃO PAGA (ago/2026), e o defeito mais grave que esta fábrica já teve.

 Cada peça do catálogo é uma mini-atividade que termina na PRÓPRIA medalha:
 tela "PEÇA FECHADA", a medalha dela, e um botão "Jogar de novo". É a tela de
 BANCADA — existe para quem está testando a peça sozinha.

 Dentro da atividade montada essa tela é um BECO. A criança termina a fase 3 de
 32, cai numa tela que diz "esta é a peça O INTRUSO" e o único caminho é
 recomeçar a MESMA fase. Para sempre. Sem erro de JS, sem aviso: o print fica
 perfeito e o defeito só existe com a criança na frente.

 A ponte do integrador já cuidava do caminho pelo `mostraBanner` — mas TRINTA
 das 78 peças chamam `fimDaPeca()` DIRETO, e essa chamada não passava por lugar
 nenhum. O conserto é o integrador reapontar `fimDaPeca` para a continuação do
 motor (`_seguir`) antes de a peça começar.

 E por que nenhum portão pegou: o jogador automático, que existe justamente para
 achar criança presa, reconhecia o fim por "apareceu uma medalha" — e via a
 medalha DA PEÇA. Ele dava a partida por encerrada na 3ª fase, com código 0.

 O QUE ESTE PORTÃO FAZ: lê a atividade montada e, para cada peça (`MEC[...]`),
 exige que — se ela declara `fimDaPeca` — a ponte tenha reapontado essa função
 (`fimDaPeca = _seguir`). Confere também que nenhuma fala de BANCADA ("PEÇA
 FECHADA", "esta é a peça X") sobrou visível para a criança.

 Uso:  python3 _qa/beco.py <arquivo.html>
 Sai 1 se alguma fase puder virar beco; 2 se não houver o que medir.
============================================================
"""
import io
import re
import sys

# as frases que só existem na bancada da peça: se a criança pode ler isso, a
# tela de teste vazou para dentro da atividade.
FALAS_DE_BANCADA = [
    u"PE&#199;A FECHADA", u"PEÇA FECHADA", u"PECA FECHADA",
    # ⚠️ (set/2026) a `calendario` escreve o C-cedilha como entidade NOMEADA — e
    #    este portao, que so conhecia a numerica, nao a via. Mesma frase, outra
    #    grafia, portao cego. Toda grafia que uma peca usar entra aqui.
    u"PE&Ccedil;A FECHADA", u"PE&ccedil;a fechada",
    u"Esta &#233; a pe&#231;a", u"Esta é a peça", u"Esta e a peca",
]


def blocos_mec(js):
    u"""devolve [(nome, corpo)] de cada `MEC["nome"] = function(...){...}`."""
    saida = []
    for m in re.finditer(r'MEC\["([a-z0-9\-]+)"\]\s*=\s*function', js):
        nome = m.group(1)
        i = js.find("{", m.end())
        if i < 0:
            continue
        prof, k = 0, i
        while k < len(js):
            if js[k] == "{":
                prof += 1
            elif js[k] == "}":
                prof -= 1
                if prof == 0:
                    break
            k += 1
        saida.append((nome, js[i:k + 1]))
    return saida


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/beco.py <arquivo.html>")
        return 2
    arq = sys.argv[1]
    html = io.open(arq, encoding="utf-8").read()
    js = u"\n".join(re.findall(r"<script(?![^>]*src)[^>]*>(.*?)</script>",
                               html, re.S))

    mecs = blocos_mec(js)
    if not mecs:
        # atividade escrita à mão (o Jardim do Broto, o Circo do Teo): não há
        # peça de catálogo aqui, e portanto não há esta armadilha. "Não medi" é
        # a resposta honesta — nunca "passou".
        print(u"%s -> sem pecas de catalogo (atividade escrita a mao?): "
              u"NAO MEDI o beco de fim de fase." % arq)
        return 2

    presos, vazados = [], []
    for nome, corpo in mecs:
        tem = re.search(r"function\s+fimDaPeca\s*\(", corpo)
        religada = re.search(r"fimDaPeca\s*=\s*_seguir", corpo)
        if tem and not religada:
            presos.append(nome)
        # ⚠️ a fala de bancada dentro do `fimDaPeca` de uma peça RELIGADA é
        #    código morto: a função nunca roda, porque a ponte a reapontou para
        #    a continuação do motor. Acusar isso seria gritar com quem já está
        #    consertado — e portão que acusa inocente ensina a ignorar portão.
        #    Só conta a fala que a criança pode mesmo LER: a de peça não
        #    religada, ou a que mora FORA do `fimDaPeca`.
        corpo_vivo = corpo
        if religada and tem:
            i = corpo.find(tem.group(0))
            j = corpo.find("{", i)
            prof, k = 0, j
            while k < len(corpo):
                if corpo[k] == "{":
                    prof += 1
                elif corpo[k] == "}":
                    prof -= 1
                    if prof == 0:
                        break
                k += 1
            corpo_vivo = corpo[:i] + corpo[k + 1:]
        # ⚠️ (set/2026) Tentei aqui uma heuristica "a funcao so e passada como
        #    callback, entao e codigo morto" — e ela perdoou a `contadores`, que
        #    CHAMA a tela de bancada direto quando as rodadas acabam. Heuristica
        #    que perdoa culpado e pior que portao rigido. A regra volta a ser uma
        #    so e clara: fala de bancada so pode morar no `fimDaPeca` de peca
        #    religada. Toda peca passou a fechar por esse nome (set/2026).
        for fala in FALAS_DE_BANCADA:
            if fala in corpo_vivo:
                vazados.append((nome, fala))
                break

    print(u"%s -> %d peca(s) de catalogo conferida(s)" % (arq, len(mecs)))
    if not presos and not vazados:
        print(u"   saida ok: toda fase leva para a seguinte "
              u"(nenhuma tela de bancada solta)")
        return 0

    if presos:
        print(u"   %d FASE(S) QUE PODEM VIRAR BECO — a crianca termina e so "
              u"pode recomecar a MESMA fase:" % len(presos))
        for n in presos[:12]:
            print(u"    - %s: declara `fimDaPeca` e a ponte nao reapontou "
                  u"para `_seguir`" % n)
    if vazados:
        print(u"   %d FALA(S) DE BANCADA visivel(is) para a crianca:" % len(vazados))
        for n, f in vazados[:8]:
            print(u"    - %s: \"%s\"" % (n, f))
    print(u"   conserto: o integrador reaponta `fimDaPeca` para a continuacao "
          u"do motor antes de a peca comecar (ver integrar.py).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
