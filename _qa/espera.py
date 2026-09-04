# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO DA ESPERA — "ela acertou. Quanto tempo fica olhando a tela parada?"

 ⚠️ LIÇÃO PAGA VÁRIAS VEZES, e é isso que dói. As palavras do Marcos, set/2026:
 *"já pedi essas correções várias vezes, e sempre acontece a mesma coisa"*. Ele
 está certo, e a culpa é do método, não dele:

   · 1ª vez: *"nas fases de ligar em alguns pcs está travando, não passa, o botão
     de próximo que não aparece"* → consertei o `mostraBanner` (guardas try/catch).
   · 2ª vez: *"sinto nas atividades que às vezes esse botão demora muito a
     aparecer ou não aparece"* → consertei de novo, no mesmo lugar.
   · 3ª vez: *"atividade oficina das palavras travando na fase 13"*, e depois o
     retrato exato: *"o estudante acerta, e fica parado esperando o botão
     continuar"*.

 Três rodadas, o mesmo defeito, porque as duas primeiras consertaram o CÓDIGO e
 não criaram o PORTÃO. Sem portão, cada mecânica nova nasce com o mesmo tempo
 morto e ninguém vê — não dá erro, não quebra nada, o print fica igual. Só a
 criança sente, e ela não reclama: ela desiste.

 O QUE FOI MEDIDO na 3ª rodada, e que ninguém tinha medido antes:

   mecânica            espera depois do acerto
   escolher                 4000 ms   ← a mais usada da casa
   tabela                   1900 ms
   saltos-na-fita           1700 ms
   bater-silabas            1500 ms   (+ 820 ms por sílaba)
   medir                    1500 ms
   balanca / caixas-de-som  1400 ms
   juntar-silabas           1400 ms
   completar                1050 ms

 Nove das ~20 mecânicas. Em bater-sílabas, com NAVIO (3 sílabas), a conta dava
 **4,3 segundos** de tela parada depois de a criança já ter acertado.

 ⭐ A REGRA: depois que a criança acerta, o botão de seguir tem que aparecer em
 até 900 ms. Comemoração é bom-vindo — mas ela acontece COM o botão na tela, não
 no lugar dele. Quem quiser mostrar mais coisa (o ritmo das sílabas, a balança
 equilibrando) mostra ANTES do prazo ou junto, nunca segurando a saída.

 ⚠️ A ÚNICA ESPERA LONGA QUE PASSA é a REDE DE SEGURANÇA declarada — o
 `setTimeout` que só dispara quando a voz não chega (o `escolher` tem um). Ela
 se declara escrevendo `/* rede-de-seguranca */` na mesma linha. Sem essa marca,
 espera longa é espera longa.

 Uso:  python3 _qa/espera.py                    (todas as peças do motor)
       python3 _qa/espera.py _padrao/pecas/x.html
 Sai 0 se ninguém segura a criança, 1 se alguém segura, 2 se não deu para medir.
============================================================
"""
import glob
import io
import os
import re
import sys

TETO_MS = 900

# o que, no corpo do setTimeout, significa "isto leva a criança adiante"
SEGUIR = re.compile(r"_seguir|fimDaPeca|mostraBanner|pecaBater|pecaBalanca|"
                    r"proxima|avanca|_avanca|ri\+\+|idx\+\+")


def sem_comentario(s):
    return re.sub(r"/\*[\s\S]*?\*/", u" ", s)


def confere(arquivos):
    if not arquivos:
        print(u"NAO MEDI: nenhuma peca encontrada em _padrao/pecas/")
        return 2
    ruins, medidas = [], 0
    for f in arquivos:
        bruto = io.open(f, encoding="utf-8", errors="replace").read()
        limpo = sem_comentario(bruto)
        for m in re.finditer(r"setTimeout\(([\s\S]{0,260}?),\s*(\d{3,})\s*\)", limpo):
            ms = int(m.group(2))
            if not SEGUIR.search(m.group(1)):
                continue        # animacao solta, nao segura a saida
            medidas += 1
            if ms <= TETO_MS:
                continue
            # a rede de seguranca declarada passa
            trecho = bruto[max(0, bruto.find(m.group(0)) - 120):]
            if u"rede-de-seguranca" in trecho[:400]:
                continue
            ruins.append((os.path.basename(f), ms))

    if not medidas:
        print(u"NAO MEDI: nenhuma espera antes de seguir encontrada — "
              u"isto nao e \"passou\".")
        return 2

    print(u"espera conferida em %d peca(s), %d ponto(s) de saida"
          % (len(arquivos), medidas))
    if ruins:
        ruins.sort(key=lambda x: -x[1])
        print(u"   %d MECANICA(S) SEGURAM A CRIANCA depois do acerto "
              u"(teto da casa: %d ms):" % (len(ruins), TETO_MS))
        for nome, ms in ruins:
            print(u"    - %-26s %d ms de tela parada" % (nome, ms))
        print(u"   Cura: comemorar COM o botao na tela, nao no lugar dele. Se a")
        print(u"   espera for rede de seguranca (a voz que pode nao chegar),")
        print(u"   escreva /* rede-de-seguranca */ na mesma linha.")
        return 1
    print(u"   espera ok: o botao de seguir aparece em ate %d ms depois do acerto"
          % TETO_MS)
    return 0


if __name__ == "__main__":
    alvos = sys.argv[1:] or sorted(glob.glob("_padrao/pecas/*.html"))
    sys.exit(confere(alvos))
