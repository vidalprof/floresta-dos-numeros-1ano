# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — CÓDIGO GÊMEO COM DEFEITO JÁ MEDIDO  (1x)

 ⭐ O DEFEITO QUE ELE PAGA (15/set/2026, o diagrama da moradia).
    Em 14/set eu MEDI no navegador que o caça-palavras do `_ort5b` era um beco
    sem saída: nem o toque-toque nem o arrastar fechavam a folha. Consertei ali,
    escrevi o comentário — e o comentário dizia, com todas as letras, que *"o
    mesmo código está em outros cadernos da casa (a folha de procurar do `_casa1`
    e do `_jogo1`, já no ar)"*. Deixei como aviso ao Marcos, esperando decisão.

    No dia seguinte ele voltou da escola: *"a atividade do diagrama, a número 9
    não funciona na das moradias"*. A criança ficou tentando.

    ⚠️ O ERRO NÃO FOI TÉCNICO, FOI DE MÉTODO. Eu já sabia. Estava escrito. E
       mesmo assim o defeito continuou no ar por um dia numa atividade que a
       turma estava usando. "Avisei" não é conserto: defeito medido num lugar é
       defeito medido em TODOS os lugares que têm o mesmo código, e o conserto
       sai na MESMA rodada, nos três.

    ⚠️ (E o aviso ainda estava errado num detalhe: o `_jogo1` não tem grade
       nenhuma. Chutei "deve estar lá também" em vez de procurar. REGRA ZERO.)

 O QUE ELE MEDE: para cada defeito da tabela abaixo, ele procura no repositório
 todo arquivo que tenha a ASSINATURA daquele código (o pedaço que identifica a
 peça) e reprova o que NÃO tiver a MARCA do conserto. Não adivinha nada: cada
 linha da tabela nasce de um defeito que chegou até a criança, e a data e a
 história estão na própria linha.

 ⚠️ O QUE ELE NÃO MEDE: se o conserto está CERTO — só se ele está PRESENTE.
    Quem mede se a folha fecha é o jogador (`_qa/joga_folha.js`); este aqui
    garante que ninguém fique de fora da rodada do conserto.

 Linha nova = todo defeito que, ao ser consertado, tiver código gêmeo noutra
 pasta. Escrever a linha é parte do conserto, não trabalho extra.

 Uso:  python3 _qa/gemeo.py            (varre o repositório inteiro)
       python3 _qa/gemeo.py <pasta>    (só uma pasta)
 Código 0 = ok · 1 = REPROVADO · 2 = não deu para medir
============================================================
"""
from __future__ import print_function

import io
import os
import re
import sys

# ---------------------------------------------------------------------------
# A TABELA. Cada linha: (apelido, o que procurar para reconhecer a peça,
#                        a marca que prova que o conserto está lá, a história)
# "assinatura" é uma LISTA: o arquivo só é cobrado se tiver TODOS os pedaços.
# ---------------------------------------------------------------------------
DEFEITOS = [
    {
        u"apelido": u"caca-palavras: beco sem saida",
        u"assinatura": [u"dcel", u"var indo = null", u"function caminho("],
        u"marca": u"puloClique",
        u"quando": u"14-15/set/2026",
        u"historia": (u"o `pointerdown` zerava o comeco do traco em TODA letra "
                      u"tocada: o toque-toque nunca fechava (o 2o toque virava "
                      u"novo comeco) e o arrastar tambem nao (quem fechava era o "
                      u"`onclick`, que num arrasto nao cai na ultima letra). A "
                      u"folha inteira era um beco sem saida, SEM erro na tela."),
        u"conserto": (u"o toque so COMECA se nao houver comeco (`if(indo !== null "
                      u"&& indo !== c._i) return;`) e o arrasto FECHA no "
                      u"`pointerup`, na letra em que o dedo parou (`celDoPonto`). "
                      u"Clonar do `_ort5b/folhas.js`."),
    },
    {
        u"apelido": u"caca-palavras: o jogador nao alcanca a folha",
        u"assinatura": [u"dcel", u"var indo = null", u"function caminho("],
        u"marca": u'"cp-" + id + "-a"',
        u"quando": u"15/set/2026",
        u"historia": (u"sem as duas pontas declaradas o `_qa/joga_folha.js` diz "
                      u"\"nao sei jogar esta peca\" e a folha sai como DIVIDA — "
                      u"foi assim que o beco sem saida do `_casa1` passou por "
                      u"toda a banca e so apareceu com a crianca na frente."),
        u"conserto": (u"na primeira e na ultima letra de cada palavra posta, "
                      u"`data-qa=\"cp-<id>-a\"` e `cp-<id>-z`, so quando a celula "
                      u"ainda nao tiver dono."),
    },
    {
        u"apelido": u"teclado tapando a atividade",
        # ⚠️ `getElementById("teclado")` — o I é MAIÚSCULO. A primeira versão
        #    desta linha procurava `id("teclado")` em minúscula, não casava com
        #    arquivo nenhum, e o portão dizia "ok" tendo medido DUAS das três
        #    regras. Portão que não acha a peça não aprova: ele fica cego. Por
        #    isso a saída agora imprime quantos arquivos CADA regra alcançou.
        # ⚠️ E A ASSINATURA PRECISA DE DUAS PEÇAS, não de uma — terceira lição
        #    desta mesma hora. Só com `getElementById("teclado")` o portão
        #    acusou `_dedos`, `_dourado5` e `_folha`, que TAMBÉM têm teclado na
        #    tela. MEDIDO no navegador, a 360x640: o teclado deles tem DOZE
        #    teclas e ocupa 213-219 px (34%); o de letras tem QUARENTA E UMA e
        #    ocupa 336 px (52%). São peças diferentes e só a segunda tapa a
        #    atividade — acusar a primeira seria portão acusando inocente.
        #    Por isso o alfabeto entra na assinatura: é ele que faz o teclado
        #    alto. (Se um dia o teclado de números crescer, ele ganha linha
        #    própria aqui, com a sua própria medida.)
        u"assinatura": [u'getElementById("teclado").className = "aberto"',
                        u"ABCDEFGHIJKLMNOPQRSTUVWXYZ"],
        u"marca": u"rolaParaCruz",
        u"quando": u"15/set/2026",
        u"historia": (u"com 39 teclas o teclado ocupava 368 px de 640 e a grade "
                      u"da cruzadinha ficava INTEIRA por baixo dele: a crianca "
                      u"escrevia as cegas. Medido no navegador."),
        u"conserto": (u"`rolaParaCruz()` sobe a palavra (ou a casa que esta sendo "
                      u"escrita) para a faixa livre, chamada ao abrir o teclado e "
                      u"a cada letra, mais `body.comtec` reservando a rolagem."),
    },
    {
        u"apelido": u"nao avisa o controle da sala que terminou",
        u"assinatura": [u"function fim(){", u"idsDaPagina("],
        u"marca": u'postMessage({eduverse: "terminou"}',
        u"quando": u"15/set/2026",
        u"historia": (u"a tela do aluno do laboratorio reconhece o fim de dois "
                      u"jeitos — espiando a MEDALHA pela classe `.medal` dentro "
                      u"do quadro, e ouvindo `postMessage({eduverse:\"terminou\"})`. "
                      u"A folha viva escapava dos DOIS (a medalha dela e `#medalha`, "
                      u"por id, e ela nao mandava aviso nenhum), entao a maquina "
                      u"da crianca que terminava nunca aparecia na lista do "
                      u"professor e ele nao sabia para quem mandar a proxima."),
        u"conserto": (u"no `fim()`, antes do `calar()`, mandar o postMessage ao "
                      u"pai (protegido por try, porque fora do laboratorio nao ha "
                      u"pai nenhum); e dar a classe `medal` ao `#medalha` no HTML, "
                      u"para a espiada tambem alcancar. Os dois, como no motor."),
    },
]

PULA = (u"node_modules", u".git", u"_qa", u"_lote", u"_recuperado", u"_pesquisa")
EXTS = (u".js", u".html")

# ⚠️⚠️ ELE TEM DE LER O CÓDIGO, NÃO A PROSA — e isto é uma lição paga na
#    primeira hora de vida deste portão (15/set/2026). A assinatura da regra do
#    teclado era `function abreCruz(`, e o COMENTÁRIO que eu tinha acabado de
#    escrever dentro dos dezoito cadernos citava, com crase e tudo, o texto
#    "function abreCruz(". Resultado: o portão dizia "18 arquivos conferidos"
#    quando só TRÊS tinham a peça de verdade. Ele estava medindo a minha própria
#    explicação. Portão que casa com comentário não mede nada: ele confirma o
#    que eu escrevi, que é o contrário de medir.
_COM_BLOCO = re.compile(r"/\*.*?\*/", re.S)
_COM_LINHA = re.compile(r"(?m)^\s*//.*$")
_COM_HTML = re.compile(r"<!--.*?-->", re.S)


def so_codigo(txt):
    u"""Tira comentário de bloco, de linha e de HTML antes de procurar."""
    txt = _COM_BLOCO.sub(u" ", txt)
    txt = _COM_HTML.sub(u" ", txt)
    return _COM_LINHA.sub(u" ", txt)


def arquivos(raiz):
    for pasta, subs, nomes in os.walk(raiz):
        subs[:] = [s for s in subs if s not in PULA and not s.startswith(u".")]
        for n in nomes:
            if n.endswith(EXTS):
                yield os.path.join(pasta, n)


def main():
    raiz = sys.argv[1] if len(sys.argv) > 1 else u"."
    if not os.path.isdir(raiz):
        print(u"%s -> NAO SE APLICA: nao e pasta." % raiz)
        return 2

    achados, vistos = [], 0
    quantos = dict((D[u"apelido"], 0) for D in DEFEITOS)
    for cam in arquivos(raiz):
        try:
            txt = so_codigo(io.open(cam, encoding=u"utf-8", errors=u"replace").read())
        except IOError:
            continue
        for D in DEFEITOS:
            if not all(a in txt for a in D[u"assinatura"]):
                continue
            vistos += 1
            quantos[D[u"apelido"]] += 1
            if D[u"marca"] not in txt:
                achados.append((cam, D))

    print(u"%s -> gemeos: %d peca(s) conhecida(s) conferida(s), %d defeito(s) na tabela"
          % (raiz.rstrip(u"/") or u".", vistos, len(DEFEITOS)))
    # ⚠️ REGRA DA CASA: portão que imprime NADA não é "passou", é "rodou cego".
    #    Por isso cada linha diz quantos arquivos ela ALCANÇOU — uma regra em
    #    zero é uma assinatura errada, não um repositório limpo.
    for D in DEFEITOS:
        n = quantos[D[u"apelido"]]
        print(u"   %s %-44s %d arquivo(s)"
              % (u"·" if n else u"!", D[u"apelido"], n))
        if not n:
            print(u"     ^ ESTA REGRA NAO ACHOU A PECA — assinatura errada ou a")
            print(u"       peca saiu do repositorio. Conferir antes de confiar.")
    if not vistos:
        print(u"   NAO SE APLICA: nenhuma das pecas da tabela existe aqui.")
        return 2
    if not achados:
        print(u"   ok: todo codigo gemeo carrega o conserto que ja foi pago.")
        return 0

    print(u"   REPROVADO — codigo com defeito JA MEDIDO, sem o conserto:")
    for cam, D in achados:
        print(u"    x %s" % cam)
        print(u"      defeito: %s (%s)" % (D[u"apelido"], D[u"quando"]))
        print(u"      o que faz com a crianca: %s" % D[u"historia"])
        print(u"      conserto: %s" % D[u"conserto"])
    print(u"   (defeito medido num lugar e defeito em TODOS os que tem o mesmo")
    print(u"    codigo — o conserto sai na MESMA rodada, nao como aviso.)")
    return 1


if __name__ == u"__main__":
    sys.exit(main())
