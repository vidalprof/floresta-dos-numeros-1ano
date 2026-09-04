# -*- coding: utf-8 -*-
u"""PORTÃO DO TOQUE — "arrastar não pega no tablet/celular da escola".

HISTÓRIA (Marcos, ago/2026). A Feirinha usava mecânicas de ARRASTAR e a criança
não conseguia jogar no iPhone/iPad. A 1ª versão deste portão BANIA todo arrasto —
premissa ERRADA. Um teste de toque sintético (Chromium headless, `new TouchEvent`)
provou que os handlers de toque das peças RESPONDEM ao dedo (classificar, ordenar,
ligar) e que o dinheiro (caixa-dinheiro) é na verdade TAP. O que faltava não era o
handler: era a blindagem de CSS **`touch-action:none`** na PEÇA arrastável. Sem ela,
o iOS lê o gesto na peça como ROLAGEM/zoom e o arrasto some sob o dedo — exatamente
o "não funciona" que chegou ao professor.

REGRA NOVA (o portão RECOMPENSA a blindagem, não bane o arrasto):
  · achou mecânica de ARRASTO no HTML  →  exige que a PEÇA dela tenha
    `touch-action:none` no CSS embutido (ex.: `.mec-classificar .pc{...touch-action:none}`);
  · toda arrastável blindada  →  passa (exit 0);
  · arrastável SEM blindagem  →  REPROVA (exit 1) e diz qual falta.

O portão mede o defeito CONHECIDO (falta de `touch-action`), que é necessário, não
suficiente: a palavra final sobre o aparelho real é do professor. Por isso segue
valendo o atalho `<!-- TOQUE-CONFERIDO -->`: quem jogou no tablet/celular REAL e
confirmou libera a atividade inteira com esse marcador.

Uso:  python3 _qa/toque.py <index.html>
"""
import io
import re
import sys

# mecânicas cujo gesto é ARRASTAR (precisam de touch-action:none na peça).
# caixa-dinheiro NÃO entra: o teste provou que é TAP (tocar a nota -> bandeja),
# seguro por natureza no touchscreen.
ARRASTO = {
    u"reta-numerica", u"classificar", u"domino", u"ligar", u"ordenar",
    u"arrastar-lugar", u"arrastar-sombra", u"grafico", u"circuito",
    u"quebra-cabeca", u"tangram", u"mapa-conceitual",
    # ⭐ MECANICA NOVA = REGRA NOVA NO PORTAO, NO MESMO COMMIT (regra da casa).
    #    A `divisao-dourado` (a Oficina da Divisao portada, set/2026) e de
    #    ARRASTO puro — a crianca leva o bloco ate o grupo, e nao vale clicar.
    #    Sem o nome dela aqui o portao dizia "nenhuma mecanica de arrasto" e
    #    NAO conferia o `touch-action` — ou seja, passava cego numa atividade
    #    inteira de arrastar.
    u"divisao-dourado",
}


def mecs_de_arrasto(html):
    u"""mecânicas de arrasto presentes (pelos marcadores de peça `PECA: <nome>`)."""
    nomes = re.findall(r"/\*\s*====\s*PECA:\s*([\w-]+)\s*====\s*\*/", html)
    return sorted(set(n for n in nomes if n in ARRASTO))


def mecs_blindadas(html):
    u"""mecânicas cujo CSS embutido tem uma regra com `touch-action:none`.

    Varre cada regra `SELETOR { ... touch-action:none ... }` e colhe os
    `.mec-<nome>` citados no seletor. Funciona com o CSS minificado do montado."""
    # ⚠️ LICAO DE VELOCIDADE (set/2026, cobranca do Marcos: "tudo isso tem que
    #    ser otimizado e rapido"). Este portao levava 15 SEGUNDOS — sem abrir
    #    navegador nenhum, so lendo texto. O culpado era o regex antigo:
    #        r"([^{}]*)\{[^{}]*touch-action:none"
    #    Num HTML de 500 KB, esse `[^{}]*` no comeco faz o motor de regex tentar
    #    casar a partir de CADA posicao e voltar atras a cada falha — trabalho
    #    que cresce com o QUADRADO do tamanho do arquivo.
    #    O conserto tem duas partes, e as duas importam:
    #      1. procurar primeiro `touch-action:none` (busca simples, rapidissima)
    #         e so entao olhar para TRAS os poucos caracteres do seletor;
    #      2. antes disso, ficar so com o CSS (o <style>), que e uma fracao do
    #         arquivo — nao ha touch-action no meio do JavaScript.
    #    Resultado medido: 15s -> menos de 1s, mesmo resultado.
    css = u"".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S)) or html
    achadas = set()
    for m in re.finditer(r"touch-action\s*:\s*none", css):
        # o seletor desta regra: o texto entre a `}` anterior e a `{` da regra
        ini = css.rfind("}", 0, m.start()) + 1
        chave = css.rfind("{", ini, m.start())
        if chave < 0:
            continue
        for nm in re.findall(r"\.mec-([\w-]+)", css[ini:chave]):
            achadas.add(nm)
    return achadas


def main():
    if len(sys.argv) < 2:
        print(u"uso: toque.py <index.html>")
        return 2
    html = io.open(sys.argv[1], encoding="utf-8").read()
    if u"TOQUE-CONFERIDO" in html:
        print(u"%s -> toque: liberado (marcador TOQUE-CONFERIDO — jogado no aparelho real)." % sys.argv[1])
        return 0
    drag = mecs_de_arrasto(html)
    if not drag:
        print(u"%s -> toque ok: nenhuma mecânica de arrasto." % sys.argv[1])
        return 0
    blind = mecs_blindadas(html)
    faltam = [m for m in drag if m not in blind]
    if not faltam:
        print(u"%s -> toque ok: %d mecânica(s) de arrasto, TODAS com touch-action:none."
              % (sys.argv[1], len(drag)))
        for m in drag:
            print(u"    ✓ %s (blindada)" % m)
        return 0
    print(u"%s -> %d mecânica(s) de arrasto SEM blindagem `touch-action:none` "
          u"(o arrasto some sob o dedo no iPad):" % (sys.argv[1], len(faltam)))
    for m in faltam:
        print(u"    ✗ %s" % m)
    print(u"   Conserto: pôr `touch-action:none` na peça arrastável dela no "
          u"`_padrao/ESQUELETO/pecas.css` (ex.: `.mec-%s .pc{touch-action:none}`)." % faltam[0])
    print(u"   Ou, se ESTA atividade já foi jogada num tablet/celular REAL e o "
          u"arrasto funcionou, libere com <!-- TOQUE-CONFERIDO --> no HTML.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
