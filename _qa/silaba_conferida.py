# -*- coding: utf-8 -*-
u"""
============================================================
 PORTAO 1y — A VOZ SE CONFERIU SOZINHA? (e o Marcos nao teve de ouvir)

 ⭐ ORDEM DO MARCOS (17/set/2026): *"eu preciso de uma ferramenta ou metodo que
    deixe tudo isso correto SEM EU TER QUE PRECISAR OUVIR"*.

 Ele esta certo, e o que havia antes era indefensavel: quem descobria que a
 silaba saiu errada era ELE, na sala, com a crianca na frente. Isso nao e
 portao — e sorte.

 O METODO, em uma linha (versao de 18/set/2026): **so a PALAVRA INTEIRA grava;
 depois de cortar, cada recorte e medido — DURACAO contra um teto absoluto por
 tamanho, e nucleo de vogal presente.** O que cada medida pega, aferido nos 52
 soletrados guardados e nos 882 bons:

     · teto de duracao (0,40/0,55/0,60 s por 1/2/3 letras) -> 33/52 soletrados, 0 bons
     · zero nucleo de vogal -> o corte perdeu a voz        -> recusa
     · dois+ nucleos -> so AVISO: pega 6/52 e confunde liquida (LU, BRI) com vogal

 ⚠️ A versao anterior deste texto dizia que "dois nucleos = soletrou". A banca
    mediu: 46 dos 52 soletrados tem UM nucleo (a voz diz "ve" longo, nao
    "ve-a"). Quem separa e a duracao. Fica escrito para nao voltar.

 Quem faz isso e o `_padrao/silabas_voz.py` na hora de gravar. O recibo fica em
 `<pasta>/audio/_conferencia.json`.

 ⚠️⚠️ A PRIMEIRA VERSAO DESTE PORTAO DESCREVIA OUTRO METODO, E ELE ESTAVA
    ERRADO — fica escrito porque a armadilha e bonita. Eu contava os pedacos na
    GRAVACAO e exigia que batessem com o numero de silabas. Isso reprova
    justamente a fala CORRIDA, que e a unica fonte segura: numa palavra falada
    de verdade as silabas sao COARTICULADAS, nao ha silencio entre elas, e por
    isso ela e UM BLOCO SO. Nao e defeito, e o portugues — quem separa nao e o
    silencio, e o alinhamento forcado. Resultado medido em 17/set/2026: o
    caminho `es co la` venceu em 205 de 326 palavras, a voz leu cada pedaco
    ISOLADO e SOLETROU (1,22 s onde cabiam 0,32 s), e o portao `_qa/silabas.py`
    reprovou os OITO cadernos e segurou a publicacao. **Contar pedacos na
    gravacao responde a pergunta errada; contar vogais no recorte responde a
    certa.**

 ESTE PORTAO LE O RECIBO. Ele reprova quando:
   1. nao ha recibo (a voz foi gravada antes deste metodo existir);
   2. alguma palavra ficou em `nao_conferidas`;
   3. o recibo esta velho — ha palavra no `silabas.json` que ele nao menciona.

 ⚠️ O QUE ELE NAO FAZ: julgar se a pronuncia esta BONITA. Ele garante que a voz
    disse UMA silaba em cada recorte, nao que o timbre agrade. Para a
    alfabetizacao e o que importa: a crianca precisa ouvir TRES pedacos em
    ES-CO-LA, cada um com som e nenhum soletrado.
    ⚠️ E ele nao substitui o `_qa/silabas.py` (duracao) nem o `_qa/silaba_audio.py`
       (forca e silencio na frente): sao tres reguas diferentes da mesma peca, e
       foi a de duracao que pegou o meu proprio erro de metodo em 17/set.

 ⚠️ E ele depende de o runner ter `librosa` na hora da gravacao. Sem ele o
    `silabas_voz.py` escreve "sem librosa: NAO CONFERI" — e isto reprova aqui,
    de proposito: nao medir nunca e "passou".

 Uso:  python3 _qa/silaba_conferida.py <pasta>
 Codigos: 0 passou · 1 REPROVOU · 2 nao deu para medir
============================================================
"""
from __future__ import print_function

import io
import json
import os
import sys


def confere(pasta):
    sj = os.path.join(pasta, u"silabas.json")
    if not os.path.exists(sj):
        return 2, [u"   sem `silabas.json`: este caderno nao fala silaba. NAO MEDI"]
    try:
        palavras = json.load(io.open(sj, encoding=u"utf-8")).get(u"palavras") or {}
    except ValueError:
        return 2, [u"   `silabas.json` ilegivel: NAO MEDI"]
    if not palavras:
        return 0, [u"   nenhuma palavra registrada: nada a conferir"]

    rec = os.path.join(pasta, u"audio", u"_conferencia.json")
    dir_audio = os.path.join(pasta, u"audio")
    if not os.path.exists(rec):
        if not os.path.isdir(dir_audio):
            return 2, [u"   a voz ainda nao foi gravada (sem pasta `audio/`): "
                       u"NAO MEDI. Ela nasce no `entregar.yml`."]
        # ⚠️ PASTA `audio/` VAZIA NAO E "GRAVOU SEM RECIBO" — e "ainda nao
        #    gravou". O esqueleto (`nova_folha_viva.sh`) ja cria a pasta, entao
        #    todo caderno RECEM-NASCIDO caia na mensagem de baixo, que diz
        #    "esta voz foi gravada ANTES de a gravacao se conferir sozinha" e
        #    manda regravar. Nada tinha sido gravado. Portao que conta historia
        #    errada custa o dia de quem vai atras dela.
        if not [a for a in os.listdir(dir_audio) if a.startswith(u"sb_")
                and a.endswith(u".mp3")]:
            return 2, [u"   a voz ainda nao foi gravada (a pasta `audio/` esta "
                       u"sem recorte de silaba): NAO MEDI. O recibo nasce no "
                       u"`entregar.yml`, junto com o mp3 — conferir DEPOIS de "
                       u"publicar. Isto NAO e 'passou'."]
        return 1, [u"   REPROVADO: nao ha recibo de conferencia "
                   u"(`audio/_conferencia.json`).",
                   u"   Esta voz foi gravada ANTES de a gravacao passar a se "
                   u"conferir sozinha. Regrave: apague `audio/_silabas.json` e "
                   u"rode o `entregar.yml`.",
                   u"   Sem o recibo, a unica garantia de que a silaba sai certa "
                   u"e alguem OUVIR — e e exatamente isso que o Marcos pediu "
                   u"para nao precisar mais fazer."]
    try:
        R = json.load(io.open(rec, encoding=u"utf-8"))
    except ValueError:
        return 1, [u"   REPROVADO: o recibo `audio/_conferencia.json` esta ilegivel"]

    ok = {x.get(u"palavra"): x for x in (R.get(u"conferidas") or [])}
    ruins = R.get(u"nao_conferidas") or []
    faltam = [w for w in sorted(palavras)
              if w not in ok and not any(y.get(u"palavra") == w for y in ruins)]

    L = [u"   recibo: voz `%s`, rate `%s`, metodo `%s`"
         % (R.get(u"voz"), R.get(u"rate"), R.get(u"metodo") or u"(antigo, sem metodo)")]
    # ⭐ CARIMBO x RECIBO (18/set/2026): palavra CARIMBADA (audio/_silabas.json,
    #   quer dizer "gravada e aceita") que nao aparece no recibo e recibo
    #   TRUNCADO — foi o que uma gravacao incremental fazia ate 18/set, ao
    #   sobrescrever o recibo so com a rodada do dia. Reprova, porque "conferida"
    #   nao pode nascer sem a medida escrita.
    carimbo_cam = os.path.join(pasta, u"audio", u"_silabas.json")
    carimbadas = set()
    if os.path.exists(carimbo_cam):
        try:
            carimbadas = set(json.load(io.open(carimbo_cam, encoding=u"utf-8")))
        except ValueError:
            pass
    sem_recibo = sorted(w for w in carimbadas if w in palavras and w not in ok
                        and not any(y.get(u"palavra") == w for y in ruins))
    por_caminho = {}
    for x in ok.values():
        c = x.get(u"caminho")
        por_caminho[c] = por_caminho.get(c, 0) + 1
    if por_caminho:
        L.append(u"   %d palavra(s) conferidas pela propria gravacao (%s)"
                 % (len(ok), u", ".join(u"`%s` x%d" % (k, v)
                                        for k, v in sorted(por_caminho.items()))))
    fc = sum(1 for x in ok.values() for d in (x.get(u"recortes") or []) if d.get(u"forma") == u"citacao")
    fp = sum(1 for x in ok.values() for d in (x.get(u"recortes") or []) if d.get(u"forma") == u"palavra")
    if fc or fp:
        L.append(u"   forma da silaba solta: %d em CITACAO (como a professora separa) · "
                 u"%d como saem na PALAVRA (a apartada soletrou/nao fechou)" % (fc, fp))
        if fp:
            quais = sorted(set(d.get(u"silaba", u"?") for x in ok.values()
                               for d in (x.get(u"recortes") or []) if d.get(u"forma") == u"palavra"))
            L.append(u"      silabas que ficaram na forma da palavra: %s" % u", ".join(quais[:30]))
    ruim = 0
    if sem_recibo:
        ruim = 1
        L.append(u"   REPROVADO: %d palavra(s) CARIMBADA(S) como gravadas que nao "
                 u"estao no recibo — recibo truncado (gravacao incremental "
                 u"sobrescreveu?): %s" % (len(sem_recibo), u", ".join(sem_recibo[:10])))
    if ruins:
        ruim = 1
        L.append(u"   REPROVADO: %d palavra(s) que a gravacao NAO conseguiu "
                 u"conferir:" % len(ruins))
        for x in ruins[:12]:
            L.append(u"      • %-12s %s" % (str(x.get(u"palavra")).upper(),
                                            x.get(u"motivo")))
        L.append(u"   conserto: veja se a divisao esta certa (portao 1w) e "
                 u"regrave. Se a palavra for mesmo dificil para a voz, troque-a "
                 u"no caderno — entregar audio que ninguem conferiu e o que se "
                 u"quer acabar.")
    if faltam:
        ruim = 1
        L.append(u"   REPROVADO: o recibo esta VELHO — %d palavra(s) do "
                 u"`silabas.json` que ele nao menciona: %s"
                 % (len(faltam), u", ".join(w.upper() for w in faltam[:10])))
        L.append(u"   conserto: apague `audio/_silabas.json` e regrave.")
    if not ruim:
        L.append(u"   ✓ todas as %d palavras foram conferidas pela propria "
                 u"gravacao — ninguem precisou ouvir" % len(palavras))
    return ruim, L


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/silaba_conferida.py <pasta>")
        return 2
    pior = 0
    for pasta in sys.argv[1:]:
        cod, L = confere(pasta.rstrip(u"/"))
        print(u"%s -> voz conferida sozinha: %s"
              % (pasta.rstrip(u"/"),
                 {0: u"ok", 1: u"REPROVADO", 2: u"NAO MEDI"}[cod]))
        for lin in L:
            print(lin)
        pior = max(pior, cod) if cod != 2 or pior == 0 else pior
    return pior


if __name__ == "__main__":
    sys.exit(main())
