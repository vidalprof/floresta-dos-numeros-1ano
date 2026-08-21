# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — "a peça termina num BECO?"

 ⚠️ LIÇÃO PAGA (ago/2026), e o CONTRATO já chamava esta família de o pior
 defeito que a fábrica teve. A peça `relampago` fechava assim:

     var b = el("button","btn","Jogar de novo");
     b.onclick = telaComecarRelampago;      // <- volta para o COMEÇO DELA

 Na bancada isso é o certo: a peça roda sozinha e o botão a reinicia. **Dentro
 da atividade é um beco.** A criança fecha o aquecimento na fase 13 de 39, cai
 numa tela que diz "PEÇA FECHADA" e o único caminho é refazer o MESMO
 aquecimento. Para sempre. Nada quebra, nada avisa: o app está "funcionando".

 O integrador TEM duas pontes que consertam isso: ele reaponta `fimDaPeca` para
 a continuação do motor, e reaponta `mostraBanner` para "mostre e siga". Quem
 fecha por um desses dois caminhos está salvo.

 ⚠️⚠️ E AQUI ESTÁ A APARADA QUE ESTE PORTÃO PRECISOU, porque a primeira versão
 dele acusou DEZ peças que estavam certas. Ter um botão "jogar de novo" não é o
 defeito — dez peças têm e nenhuma delas prende ninguém, porque a tela onde o
 botão mora só é alcançada por `mostraBanner(...)`, e dentro da atividade essa
 ponte leva embora antes de a tela existir. O defeito é a tela de fim ser
 chamada **DIRETO**, por dentro da peça: aí ela aparece de verdade, com o botão
 que só sabe voltar ao começo. Era o caso do `relampago` (o `proxima()` chamava
 `telaFimRelampago()` na mão) e do `conserte-o-erro`.

 Portão que acusa inocente é portão que se aprende a ignorar — e essa lição já
 custou caro nesta casa. Então a pergunta é exata: **a tela que tem o botão de
 recomeçar é chamada direto em algum lugar?**

 ⚠️ O que ele NÃO mede: se a peça CHEGA ao fim (isso é o `_qa/jogador.js`, que
 joga de verdade). Este aqui é o aviso barato, sem navegador — e teria pego o
 relâmpago em um segundo, em vez de trinta minutos de banca.

 Uso: python3 _qa/beco_peca.py <peca.html>
============================================================
"""
import io
import re
import sys


def limites(js, nome):
    u"""(inicio, fim) do corpo de `function nome(){...}`, ou (None, None)."""
    m = re.search(r"function\s+%s\s*\([^)]*\)\s*\{" % re.escape(nome), js)
    if not m:
        return None, None
    i = m.end() - 1
    prof, k = 0, i
    while k < len(js):
        if js[k] == "{":
            prof += 1
        elif js[k] == "}":
            prof -= 1
            if prof == 0:
                return i, k
        k += 1
    return i, len(js)


def porta(js):
    u"""a PORTA DE ENTRADA: a função que a peça chama na última linha.

    É a mesma que o integrador troca por "monte esta fase e comece"."""
    achados = re.findall(r"^\s*([A-Za-z_$][\w$]*)\s*\(\s*\)\s*;\s*$", js, re.M)
    return achados[-1] if achados else None


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/beco_peca.py <peca.html>")
        return 2
    arq = sys.argv[1]
    html = io.open(arq, encoding="utf-8").read()
    js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    js = re.sub(r"/\*.*?\*/", " ", js, flags=re.S)

    p = porta(js)
    if not p:
        print(u"%s -> nao achei a porta de entrada (a peca nao se chama na "
              u"ultima linha). NAO MEDI." % arq)
        return 2

    # o botão que volta para a porta de entrada
    bot = re.search(r"onclick\s*=\s*%s\s*;" % re.escape(p), js)
    if not bot:
        bot = re.search(r"onclick\s*=\s*function\s*\([^)]*\)\s*\{\s*%s\s*\(\s*\)\s*;"
                        % re.escape(p), js)
    if not bot:
        print(u"%s -> porta: %s()  |  nenhum botao volta para o comeco" % (arq, p))
        print(u"   beco ok: a peca nao tem 'jogar de novo'")
        return 0

    # em que função ele mora? (a tela de fim)
    dono = None
    for fm in re.finditer(r"function\s+([A-Za-z_$][\w$]*)\s*\(", js):
        i, k = limites(js, fm.group(1))
        if i is not None and i <= bot.start() < k:
            dono = fm.group(1)
    if not dono:
        print(u"%s -> porta: %s()  |  o botao de recomecar nao esta dentro de "
              u"funcao nenhuma. NAO MEDI." % (arq, p))
        return 2

    if dono == "fimDaPeca":
        print(u"%s -> porta: %s()  |  tela de fim: fimDaPeca()" % (arq, p))
        print(u"   beco ok: o 'jogar de novo' mora em fimDaPeca(), que o "
              u"integrador troca por 'siga para a proxima fase'")
        return 0

    # ela é chamada DIRETO em algum lugar (fora de ser callback do mostraBanner)?
    diretos = []
    dec = re.search(r"function\s+%s\s*\(" % re.escape(dono), js)
    for cm in re.finditer(r"(?<![\w.])%s\s*\(" % re.escape(dono), js):
        if dec and abs(cm.start() - dec.start()) < 12:
            continue                       # é a própria declaração
        antes = js[max(0, cm.start() - 120):cm.start()]
        if "mostraBanner" in antes and antes.rstrip().endswith(","):
            continue                       # é callback da ponte: está salvo
        diretos.append(cm.start())

    print(u"%s -> porta: %s()  |  tela de fim: %s()  |  %d chamada(s) direta(s)"
          % (arq, p, dono, len(diretos)))
    if not diretos:
        print(u"   beco ok: a tela de fim so aparece por mostraBanner(), e "
              u"dentro da atividade essa ponte leva para a fase seguinte")
        return 0

    print(u"   BECO: %s() e chamada DIRETO, entao a tela de fim APARECE de" % dono)
    print(u"   verdade dentro da atividade — e o unico botao dela volta para o")
    print(u"   comeco da MESMA fase. A crianca nao sai dali.")
    for i in diretos:
        print(u"    - linha %d do <script>: %s"
              % (js.count("\n", 0, i) + 1, " ".join(js[i:i + 70].split())))
    print(u"   conserto: a tela de fim chama `fimDaPeca()` no botao, e o")
    print(u"   'jogar de novo' passa a morar DENTRO de fimDaPeca(), que e a")
    print(u"   unica tela que so a bancada ve.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
