# -*- coding: utf-8 -*-
u"""
============================================================
PORTÃO — "a atividade enche a aula?"

⚠️ LIÇÃO PAGA (ago/2026, na Oficina da Lina). Palavras do Marcos:
   *"A atividade precisa durar pelo menos 40 minutos"*.

Eu tinha entregado uma atividade que ele mediu em **catorze minutos**. Não
faltava nada nela — as fases funcionavam, a arte estava lá, a voz gravada. O
que faltava era CHÃO: a aula do laboratório dura 55 minutos e a criança
terminava com meia aula sobrando, o que na prática significa a turma inteira
ociosa e o professor sem plano B.

⭐ E O OUTRO LADO — O TETO, QUE AVISA (set/2026). O Marcos primeiro disse *"cada
   aula deve durar 50 minutos"* e logo corrigiu: *"não tem problema se a aula
   durar mais, na verdade tem 55 minutos"*. Ficou assim: a aula tem **55 min**, e
   passar disso **não reprova** — a criança volta de onde parou (o convite do
   `RETOMAR` dura os mesmos 55). O portão só AVISA, porque quem passa muito
   talvez não chegue no fecho (o boletim dela, o parecer, o relatório do
   professor), e quem decide se isso importa naquela atividade é o professor.
   O PISO continua reprovando: catorze minutos com a turma ociosa é defeito.

⚠️⚠️ A VOZ OUVIDA NÃO É O BANCO DE VOZ — e este portão media errado. Ele somava
   o `falas.json` INTEIRO como se a criança ouvisse tudo. Na Fábrica de Palavras
   são 515 falas, e 333 delas são o `certo_` e o `dica_` de CADA item possível do
   pote; a criança resolve 73 itens. O portão dizia 24 min de voz onde há 5 a 15.
   É a MESMA lição que ele já tinha aprendido para os ITENS — *"conta o que a
   folha SORTEIA, não o tamanho do pote"* — e que a voz não tinha recebido.
   Consertado, as duas últimas atividades saíram de "54 min" para "35 a 45".

⚠️ POR QUE UMA FAIXA E NÃO UM NÚMERO. Quantas falas cada item aciona depende da
   criança: a econômica ouve só o retorno; a que usa a atividade como ela foi
   feita toca no alto-falante de cada opção, erra, ouve a dica. São 20 minutos de
   diferença, e as duas crianças são reais. O portão dá a FAIXA e só reprova
   quando ela cai fora INTEIRA.

E nenhum portão via, porque nenhum portão contava o **tamanho** do trabalho: a
bancada media se funciona, se ilustra, se fala — nunca se DÁ AULA.

COMO ESTE PORTÃO MEDE (é uma ESTIMATIVA, e ele diz isso em voz alta):
  · a voz OUVIDA: as falas fixas (capa, enunciado de folha, fim) inteiras, mais
    o banco pelo que a criança de fato aciona, a 2,6 palavras por segundo;
  · o trabalho da criança: cada item das listas de conteúdo, com o preço do
    GESTO daquela fase — escrever no teclado da tela 25 s, achar palavra na
    grade 20 s, virar carta 20 s, arrastar 14 s, tocar numa opção 8 s. (Preço
    único para tudo mente: dizia 30 min numa atividade em que metade das fases
    é DIGITADA, e digitar leva o triplo de tocar.)
  · o custo fixo de cada tela (capa, crachá, banner de fim de fase): 12 s.

Não é cronômetro: é ordem de grandeza. Serve para separar "catorze minutos" de
"a aula inteira", que é a pergunta que o Marcos faz.

Uso:  python3 _qa/duracao.py _lina            (piso padrão: 40 min)
      python3 _qa/duracao.py _lina 25          (piso próprio, p/ atividade curta)
Sai 0 se enche a aula, 1 se ficou CURTA, 2 se não deu para medir. Passar dos
55 min avisa, não reprova.
============================================================
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mp3_dur import por_id as mp3_por_id   # o RELOGIO da voz

PAL_POR_S = 1.8      # MEDIDO: 890 mp3 da casa, 1,66 a 1,90 palavra/s
                     # (antes era 2,6, inventado por mim — ver o bloco da voz)
S_POR_ITEM = 9.0     # ler, pensar e tocar (4o/5o ano)
S_POR_TELA = 12.0    # capa, cracha, banner, elogio
# ⚠️ QUANTAS FALAS DO BANCO CADA ITEM ACIONA — e por que sao DUAS numeros e nao
#    um. A crianca economica ouve so o retorno ("muito bem!"): 1 por item. A que
#    usa a atividade como ela foi feita toca no alto-falante de cada opcao, erra,
#    ouve a dica e o retorno: 4. Entre uma e outra ha 20 minutos de diferenca
#    numa atividade de 1o ano — e as DUAS sao criancas reais. Fingir um numero
#    unico aqui e dar cara de medida a um palpite meu; por isso o portao calcula
#    a FAIXA e so reprova quando a faixa INTEIRA cai fora.
FALAS_ITEM_MIN = 1.0
FALAS_ITEM_MAX = 4.0
# ⭐ A AULA DO LABORATORIO — 55 MINUTOS (Marcos, set/2026, corrigindo o 50 que
#    ele tinha dito na frase anterior: *"nao tem problema se a aula durar mais,
#    na verdade tem 55 minutos"*). E o mesmo 55 do convite do `RETOMAR`: a
#    crianca que nao termina volta de onde parou, dentro da aula.
#    ⚠️ POR ISSO O TETO AVISA E NAO REPROVA. Passar de 55 nao e defeito — e
#    informacao: quem passa muito talvez nao chegue no fecho (o boletim, o
#    parecer, o relatorio). Quem decide se isso importa naquela atividade e o
#    professor, nao o portao. O PISO continua reprovando: catorze minutos
#    deixando a turma ociosa e' defeito, e foi o que deu origem a este portao.
AULA_MIN = 55.0

# custo por GESTO na atividade montada (segundos por item resolvido)
# ⚠️ LICAO PAGA (set/2026, na Grande Expedicao de divisao): a montada precificava
#    TODO gesto nao-listado como 9 s ("tocar"), o default. So que DIGITAR uma
#    divisao (calcular na cabeca + escrever no teclado da tela) e o mesmo gesto
#    que o cabecalho deste portao ja valoriza em 25 s na trilha das LISTAS — e
#    ESTIMAR, EQUILIBRAR a balanca, ACHAR na reta ou TROCAR na base dez sao
#    raciocinio, nao um toque. Precificar tudo a 9 s subestimava uma atividade
#    de matematica inteira (30 min onde a crianca leva 40+). Aqui os gestos que
#    pensam ganham o preco real — mesma filosofia da trilha das listas. Custo
#    maior nunca REPROVA sozinho (nao ha teto): so conta melhor o trabalho real.
CUSTO_MEC = {u"memoria": 20.0, u"ligar": 14.0, u"classificar": 14.0,
             u"arrastar-lugar": 14.0, u"caixa-dinheiro": 12.0,
             u"achar-na-cena": 20.0, u"caca-palavras": 20.0,
             u"digitar-numero": 25.0, u"base-dez": 18.0,
             u"reta-numerica": 15.0, u"estimar": 15.0, u"balanca": 15.0,
             u"repartir": 14.0, u"saltos-na-fita": 12.0, u"padrao": 12.0,
             u"contadores": 10.0, u"arranjo": 16.0, u"resto": 16.0,
             u"quociente-parcial": 22.0}


def _extrai_fases(html):
    u"""⭐ LICAO PAGA (ago/2026): a atividade MONTADA pelo Esqueleto guarda o
    conteudo real em `FASES = [ ... ]` (json.dumps, e SEM `var`), invisivel ao
    regex `var X=[...]` que contava so os EXEMPLOS das pecas. Resultado: TODA
    montada (o novo padrao 6x6) reprovava por '21 min' tendo 36 fases de
    verdade. Aqui achamos o array FASES por casamento de colchetes e o lemos
    como JSON — e o trabalho REAL da crianca passa a contar."""
    for m in re.finditer(r'\bFASES\s*=\s*\[', html):
        i = html.index(u"[", m.start())
        prof = 0
        for k in range(i, len(html)):
            if html[k] == u"[":
                prof += 1
            elif html[k] == u"]":
                prof -= 1
                if prof == 0:
                    try:
                        arr = json.loads(html[i:k + 1])
                        if (isinstance(arr, list) and arr
                                and isinstance(arr[0], dict) and arr[0].get(u"mec")):
                            return arr
                    except ValueError:
                        pass
                    break
    return None


def confere(pasta, piso_min=40.0):
    pasta = pasta.rstrip(u"/")
    cam = os.path.join(pasta, u"index.html")
    if not os.path.exists(cam):
        print(u"%s -> sem index.html. NAO MEDI." % pasta)
        return 2
    html = io.open(cam, encoding=u"utf-8").read()
    # ⚠️ LICAO PAGA (set/2026, na Fabrica de Palavras): a atividade a mao pode partir
    #    o codigo em `<script src="folhas.js">` ao lado. O portao lia so o index, nao
    #    achava as funcoes `fN` das folhas e precificava TUDO como "digitar" (25 s) —
    #    dizia 39 min numa atividade cujos gestos sao quase todos de tocar. Aqui os
    #    irmaos locais entram na leitura, e o gesto de cada folha volta a ser medido.
    for m_src in re.finditer(r'<script[^>]+src="([^":]+\.js)"', html):
        irmao = os.path.join(pasta, m_src.group(1))
        if os.path.exists(irmao):
            html += u"\n" + io.open(irmao, encoding=u"utf-8").read()

    # 1) quanto tempo de voz gravada
    # ⚠️⚠️ AQUI HAVIA UM CHUTE COM CARA DE MEDIDA (12/set/2026 — ordem do Marcos,
    #    em quatro palavras: *"Nunca chute nunca invente"*).
    #
    #    Este bloco calculava o tempo de voz dividindo as PALAVRAS por 2,6 — um
    #    numero que eu inventei, sem cronometro e sem fonte, e que saia impresso
    #    no log como se fosse medida. Os mp3 estao no disco: a duracao exata
    #    esta DENTRO deles, quadro a quadro.
    #
    #    Conferido nos tres cadernos com voz completa (890 arquivos): a voz da
    #    casa fala a 1,66-1,90 palavra por segundo. O meu 2,6 era 37% rapido
    #    demais — ou seja, eu vinha SUBESTIMANDO a voz em quase 40%.
    #
    #    Agora: se o mp3 existe, vale o RELOGIO. So quando ele ainda nao foi
    #    gravado e que se estima — e aí pelo passo MEDIDO, dizendo que estimou.
    seg_voz = 0.0
    voz_medida, voz_estimada = 0, 0
    camf = os.path.join(pasta, u"falas.json")
    if os.path.exists(camf):
        try:
            falas = json.loads(io.open(camf, encoding=u"utf-8").read())
        except ValueError:
            print(u"%s -> falas.json ilegivel. NAO MEDI o tempo de voz." % pasta)
            return 2
        relogio = mp3_por_id(os.path.join(pasta, u"audio"))
        for f in falas:
            real = relogio.get(f.get(u"id") or u"")
            if real:
                seg_voz += real
                voz_medida += 1
            else:
                seg_voz += len((f.get(u"texto") or u"").split()) / PAL_POR_S
                voz_estimada += 1
    else:
        print(u"%s -> sem falas.json: NAO MEDI (MP3 nao se le)." % pasta)
        return 2
    seg_voz_banco = seg_voz
    faixa = None

    # 2) quantos itens a crianca tem que resolver — e QUANTO CUSTA CADA UM.
    #    ⚠️ nao se conta item por item igual: escrever uma palavra no teclado da
    #    tela leva o triplo do tempo de tocar numa opcao.
    corpos = {}
    for m in re.finditer(r'^function\s+(\w+)\s*\(', html, re.M):
        ini = html.find(u"{", m.end())
        prof, k = 0, ini
        while k < len(html):
            if html[k] == u"{":
                prof += 1
            elif html[k] == u"}":
                prof -= 1
                if prof == 0:
                    break
            k += 1
        corpos[m.group(1)] = html[ini:k]

    def custo_da_lista(nome):
        # segundos por item, pelo GESTO da fase que usa a lista
        for corpo in corpos.values():
            if not re.search(r'\b' + re.escape(nome) + r'\b', corpo):
                continue
            # ⚠️ so e ESCREVER quando ha teclado E lacunas: um par de botoes
            #    chamado `letras` e TOCAR, e contava como digitacao (25 s).
            if re.search(r'\.tec\b|slots|<input', corpo):
                return 25.0, u"escrever"
            if u"mcarta" in corpo:
                return 20.0, u"memoria"
            if re.search(r'celula|grade|caca', corpo):
                return 20.0, u"procurar"
            if re.search(r'arrast|drag|gaveta', corpo):
                return 14.0, u"arrastar"
        return S_POR_ITEM, u"tocar"

    itens, seg_itens, detalhe = 0, 0.0, []
    fases_m = _extrai_fases(html)
    for nome, corpo in ([] if fases_m else
                        re.findall(r'var\s+([A-Z][A-Z0-9_]{2,})\s*=\s*\[(.*?)\];',
                                   html, re.S)):
        if nome in (u"IMGS", u"VOZOK", u"FASES_MESTRE", u"MED", u"TREINO"):
            continue
        # ⚠️ contar `{` cru INFLA: uma ficha com objeto dentro virava tres itens
        #    (FICHAS deu 54 onde sao 18). Conta so o que esta no PRIMEIRO nivel.
        # ⚠️ LICAO PAGA (ago/2026, no tangram): contar o item de PRIMEIRO nivel
        #    subestimava o trabalho. A lista tinha 10 figuras, e o portao disse
        #    "7 minutos" — mas cada figura pede 5 a 7 PECAS, uma a uma. Quando o
        #    item tem uma lista dentro (as vagas da figura, as rodadas da fase),
        #    o trabalho da crianca esta LA DENTRO, e e isso que conta.
        n, prof, dentro = 0, 0, 0
        for ch in corpo:
            if ch == u"{":
                if prof == 0:
                    n += 1
                elif prof >= 1:
                    dentro += 1
                prof += 1
            elif ch == u"}":
                prof -= 1
        if dentro > n:
            n = dentro          # o trabalho mora nos sub-itens
        if not n:
            n = len(re.findall(r'"[^"]*"|\[[^\[\]]*\]', corpo))
        if n:
            custo, gesto = custo_da_lista(nome)
            # ⚠️ PORTAL DE LEITURA (formato site/revista — ago/2026): uma lista
            #    cujos itens trazem `texto:` + `fala:` NAO e um toque de 9 s. E uma
            #    SECAO que a crianca LE (paragrafo + fatos + foto) e OUVE narrada.
            #    Ler+ouvir uma secao dessas leva ~1 min no 5o ano. Precificar como
            #    "tocar" media 23 min num portal que na pratica enche a aula.
            if re.search(r'\btexto\s*:', corpo) and re.search(r'\bfala\s*:', corpo):
                custo, gesto = 70.0, u"ler"
            itens += n
            seg_itens += n * custo
            detalhe.append((nome, n, gesto))

    # 2b) MONTADA: conta o trabalho REAL de cada uma das fases (nao os exemplos)
    if fases_m:
        for f in fases_m:
            mec = f.get(u"mec", u"")
            ex = f.get(u"dadosExtra") or {}
            dd = f.get(u"dados")
            if mec == u"caixa-dinheiro":
                n = len(ex.get(u"RODADAS") or [])
            elif mec == u"classificar":
                n = len(ex.get(u"FICHAS") or [])
            else:
                n = len(dd) if isinstance(dd, list) else 1
            n = max(n, 1)
            custo = CUSTO_MEC.get(mec, S_POR_ITEM)
            itens += n
            seg_itens += n * custo
        # resumo por mecanica para a linha "maiores listas"
        from collections import Counter
        cont = Counter()
        for f in fases_m:
            mec = f.get(u"mec", u"")
            ex = f.get(u"dadosExtra") or {}
            dd = f.get(u"dados")
            if mec == u"caixa-dinheiro":
                cont[mec] += len(ex.get(u"RODADAS") or [])
            elif mec == u"classificar":
                cont[mec] += len(ex.get(u"FICHAS") or [])
            else:
                cont[mec] += len(dd) if isinstance(dd, list) else 1
        detalhe = [(m, q, m) for m, q in cont.most_common()]

    # 2c) FOLHA A MAO (livro de folhas interativas — set/2026, na Oficina do
    #     Material Dourado). ⚠️ LICAO PAGA: o app a mao nao tem `FASES` nem
    #     `var LISTA=[...]` de conteudo; o que a crianca resolve mora no bloco
    #     `/*ITENS-INI*/ var ITENS = {...}` (uma lista por FOLHA, chave "pN").
    #     Sem isto o portao lia as listas ERRADAS — pegava NOMES e CORES (os
    #     titulos e as cores das folhas!) e dizia "20 itens, 23 min" numa
    #     atividade de 57 respostas. Contar o titulo da folha como trabalho da
    #     crianca e pior que nao medir: da um numero com cara de medida.
    #     O preco sai do GESTO da folha, lido na funcao `fN` que a desenha:
    #     cada `caixa(` e uma resposta digitada; `montador(` e manipular pecas
    #     (por em cima da mesa uma a uma); `montaLigar(` e ligar; e um item com
    #     `hist` e um PROBLEMA, que antes de resolver precisa ser lido.
    m_it = re.search(r'/\*ITENS-INI\*/\s*var\s+ITENS\s*=\s*(\{.*?\})\s*;\s*/\*ITENS-FIM\*/',
                     html, re.S)
    if m_it and not fases_m:
        try:
            itens_js = json.loads(m_it.group(1))
        except ValueError:
            itens_js = None
        if itens_js:
            itens, seg_itens, detalhe = 0, 0.0, []
            for chave in sorted(itens_js.keys()):
                lista = itens_js[chave]
                if not isinstance(lista, list) or not lista:
                    continue
                # ⚠️ conta o que a folha SORTEIA, nao o tamanho do pote: o pool
                #    tem 6 contas e a folha pede 3. Contar o pote inflava a
                #    estimativa em quase o dobro — numero com cara de medida, de
                #    novo. O `pega(ITENS.pN, Q, ...)` do `novaFolha` diz o Q.
                mq = re.search(r'pega\(\s*ITENS\.' + re.escape(chave) + r'\s*,\s*(\d+)', html)
                n = min(len(lista), int(mq.group(1))) if mq else len(lista)
                mm = re.match(r'^p(\d+)$', chave)
                corpo = corpos.get(u"f%s" % mm.group(1), u"") if mm else u""
                # ⚠️⚠️ ESTE PORTAO ESTAVA INFLANDO A AULA, e quem desconfiou foi o
                #    Marcos (set/2026): *"eu nao acredito que 10 folhas durem uma aula
                #    toda"*. Ele estava certo, e a causa era aqui.
                #
                #    O galho da FOLHA VIVA so sabia reconhecer dois gestos (o montador
                #    e o ligar). Tudo o mais caia no `else` e era precificado a 25 s
                #    por item — que e o preco de DIGITAR uma palavra no teclado da
                #    tela. Uma folha em que a crianca so TOCA numa de tres opcoes
                #    custava o mesmo que escrever a palavra inteira letra por letra.
                #    Nos dez cadernos de alfabetizacao quase toda folha caia nesse
                #    `else`: a estimativa inteira saiu com cara de medida e era um
                #    palpite caro.
                #
                #    ⚠️ E o pior: o portao usava o numero para dizer "duracao ok:
                #       enche a aula". Ele APROVAVA por causa do proprio erro.
                #
                #    O galho da MONTADA ja sabia fazer isto direito (ver
                #    `custo_da_lista` la em cima) — so nunca tinha sido trazido para
                #    ca. Agora o gesto e lido no corpo da propria folha.
                if u"montador(" in corpo:
                    custo, gesto = 45.0, u"manipular"
                elif u"montaLigar(" in corpo:
                    custo, gesto = 14.0, u"ligar"
                elif re.search(r'\bcaixa\(', corpo):
                    caixas = len(re.findall(r'\bcaixa\(', corpo))
                    custo, gesto = 25.0 * caixas, (u"digitar x%d" % caixas)
                elif re.search(r'\bativa\(|\bativaLetras\(|\.tec\b|<input', corpo):
                    custo, gesto = 25.0, u"escrever"      # teclado de verdade
                elif u"mcarta" in corpo:
                    custo, gesto = 20.0, u"memoria"
                elif re.search(r'celula|caca|cruzad', corpo):
                    custo, gesto = 20.0, u"procurar"
                elif re.search(r'gaveta|coluna|puxavel\(|arrast', corpo):
                    custo, gesto = 14.0, u"arrastar"
                elif re.search(r'riscoDeCircular\(|Conferir', corpo):
                    custo, gesto = 12.0, u"marcar varios"
                else:
                    custo, gesto = S_POR_ITEM, u"tocar"
                if isinstance(lista[0], dict) and lista[0].get(u"hist"):
                    custo += 45.0            # ler e entender o problema
                    gesto = u"problema"
                itens += n
                seg_itens += n * custo
                detalhe.append((chave, n, gesto))

    # 2d) ⭐⭐ A VOZ OUVIDA NÃO É O BANCO DE VOZ (set/2026 — o Marcos: *"cada aula
    #     deve durar 55 minutos"*, e ao conferir se as duas últimas cabiam achei
    #     ISTO).
    #
    #     ⚠️ LIÇÃO PAGA, E É A MESMA DE ANTES, NOUTRO LUGAR. Este portão já tinha
    #     aprendido, para os ITENS, que *"conta o que a folha SORTEIA, não o
    #     tamanho do pote"*. A VOZ ficou com o defeito antigo: somava o
    #     `falas.json` INTEIRO como se a criança ouvisse tudo.
    #
    #     Na Fábrica de Palavras isso são 515 falas — e 333 delas são o `certo_`
    #     e o `dica_` de CADA item possível do pote. A criança resolve 73 itens:
    #     ela ouve uns 160 desses arquivos, nunca os 501. O portão dizia 24 min
    #     de voz onde há ~9. Numa atividade que SORTEIA, o `falas.json` é o
    #     BANCO de voz, não o ROTEIRO da aula.
    #
    #     Como se separa: o bloco `/*FALAS-INI*/var FALAS={...}` tem as chaves
    #     com NOME (o `falas.json` só tem o id embaralhado). Chave FIXA (`capa`,
    #     `fim`, `pNenun`) a criança ouve sempre e conta inteira; o resto é banco
    #     e conta pelo que ela de fato aciona: por item resolvido, o retorno mais
    #     o enunciado/alto-falante ocasional e parte das dicas.
    m_fal = re.search(r'/\*FALAS-INI\*/\s*var\s+FALAS\s*=\s*(\{.*?\})\s*;?\s*/\*FALAS-FIM\*/',
                      html, re.S)
    if m_fal and itens:
        try:
            dfal = json.loads(m_fal.group(1))
        except ValueError:
            dfal = None
        if dfal:
            fixa = re.compile(r'^(capa|fim|fimRel|escreva|intro|abertura|medalha|'
                              r'relat|p\d+enu[nm]|p\d+ajuda)')
            s_fix = s_banco = 0.0
            n_banco = 0
            for k, v in dfal.items():
                dur = len((u"%s" % v).split()) / PAL_POR_S
                if fixa.match(k):
                    s_fix += dur
                else:
                    s_banco += dur
                    n_banco += 1
            if n_banco:
                media = s_banco / n_banco
                voz_min = s_fix + media * min(n_banco, itens * FALAS_ITEM_MIN)
                voz_max = s_fix + media * min(n_banco, itens * FALAS_ITEM_MAX)
                seg_voz = (voz_min + voz_max) / 2.0
                faixa = (voz_min, voz_max)

    # 3) quantas telas
    telas = len(re.findall(r'^function\s+tela\w+\(', html, re.M))

    seg = seg_voz + seg_itens + telas * S_POR_TELA
    mins = seg / 60.0

    if faixa:
        base = seg_itens + telas * S_POR_TELA
        lo, hi = (base + faixa[0]) / 60.0, (base + faixa[1]) / 60.0
    else:
        lo = hi = mins

    if faixa:
        print(u"%s -> ESTIMATIVA de duracao: %.0f a %.0f min" % (pasta, lo, hi))
        print(u"   voz ouvida: %.0f a %.0f min (banco gravado: %.0f min) | %d itens "
              u"para resolver | %d telas"
              % (faixa[0] / 60.0, faixa[1] / 60.0, seg_voz_banco / 60.0, itens, telas))
        print(u"   (a faixa e a crianca que so ouve o retorno x a que toca em todo")
        print(u"    alto-falante; as duas existem na turma)")
    else:
        print(u"%s -> ESTIMATIVA de duracao: %.0f min" % (pasta, mins))
        print(u"   voz gravada: %.0f min | %d itens para resolver | %d telas"
              % (seg_voz / 60.0, itens, telas))
    # ⭐ O QUE FOI MEDIDO E O QUE FOI ESTIMADO — dito em voz alta, SEMPRE.
    #    Regra do Marcos (12/set/2026): *"Nunca chute nunca invente"*. Numero de
    #    portao que nao diz de onde veio e chute com cara de medida — foi assim
    #    que este mesmo portao me fez repetir "39 a 65 min" para ele.
    print(u"   MEDIDO no relogio: %d fala(s) lida(s) do proprio mp3%s"
          % (voz_medida,
             u"" if not voz_estimada
             else u"; ESTIMADAS %d ainda sem mp3 (a %.1f palavra/s, o passo MEDIDO"
                  u" em 890 arquivos)" % (voz_estimada, PAL_POR_S)))
    print(u"   PALPITE DECLARADO (nunca cronometrado com crianca): o tempo por "
          u"gesto — escrever 25s, memoria/procurar 20s, ligar/arrastar 14s, "
          u"marcar 12s, tocar 9s.")
    detalhe.sort(key=lambda x: -x[1])
    print(u"   maiores listas: %s"
          % u", ".join(u"%s %d %s" % (n, q, g) for (n, q, g) in detalhe[:8]))

    # ⚠️ EXCECAO DECLARADA: JOGO (ver a mesma porta no `_qa/padrao.py`).
    # O piso de 40 min nasceu de uma ATIVIDADE que terminava em catorze e
    # deixava a turma ociosa. Um JOGO nao tem esse problema: o professor usa
    # quanto tempo quiser dele, e a crianca que acaba as figuras joga de novo.
    # A porta so abre com `var TIPO_ATIVIDADE="jogo"` escrito no arquivo.
    if re.search(r'var\s+TIPO_ATIVIDADE\s*=\s*"jogo"', html) and mins < piso_min:
        print(u"   \u26a0 EXCECAO DECLARADA: `TIPO_ATIVIDADE=\"jogo\"`. %.0f min e o tamanho"
              % mins)
        print(u"      do jogo, nao um defeito — o piso de %d min vale para ATIVIDADE."
              % piso_min)
        return 0

    if hi < piso_min:
        # ⚠️ (set/2026) imprimia "40 min" arredondado e reprovava por 39,6 < 40 —
        #    a tela dizia uma coisa e o veredito outra. Reprova mostra o decimal.
        print(u"   !! A ATIVIDADE NAO ENCHE A AULA (piso: %d min; estimativa exata: %.1f min)."
              % (piso_min, mins))
        print(u"   a aula do laboratorio dura 55 min. Terminando em %.1f, a turma"
              % mins)
        print(u"   fica ociosa e o professor sem plano B — foi essa a cobranca.")
        print(u"   conserto: mais rodadas nas listas que ja existem (sai de graca,")
        print(u"   sem arte nem voz nova) ou uma fase a mais com gesto diferente.")
        return 1

    # ⭐ O OUTRO LADO DA REGUA — e ele AVISA, nao reprova.
    #    O Marcos primeiro disse *"cada aula deve durar 50 minutos"* e logo
    #    corrigiu: *"nao tem problema se a aula durar mais, na verdade tem 55"*.
    #    Entao passar de 55 NAO e defeito: a crianca volta de onde parou (o
    #    convite do RETOMAR dura os mesmos 55 min). O que o portao faz e AVISAR,
    #    porque quem passa muito talvez nao chegue no fecho — o boletim dela, o
    #    parecer, o relatorio do professor — e quem decide se isso importa
    #    naquela atividade e o professor, nao o portao.
    if lo > AULA_MIN:
        print(u"   ⚠ passa da aula: ate a crianca mais rapida leva %.0f min "
              u"(a aula tem %d)." % (lo, AULA_MIN))
    elif hi > AULA_MIN:
        print(u"   ⚠ a crianca que ouve todo alto-falante leva %.0f min "
              u"(a aula tem %d)." % (hi, AULA_MIN))
    if lo > AULA_MIN or hi > AULA_MIN:
        print(u"      Nao e defeito: ela volta de onde parou. Mas quem passa muito")
        print(u"      talvez nao chegue no fecho (boletim, parecer, relatorio). Se")
        print(u"      quiser encurtar: menos itens sorteados por folha, no `pega(...)`")
        print(u"      — nao mexe no pote nem pede voz nova.")
        # ⚠️ na atividade MONTADA a voz ainda entra como o BANCO INTEIRO (nao ha
        #    bloco FALAS nomeado), entao este numero esta ALTO de proposito.
        if not faixa:
            print(u"      ⚠ nesta montada a voz conta o banco inteiro: o numero")
            print(u"         esta ALTO. Confirmar no relogio antes de encurtar.")
    print(u"   duracao ok: enche a aula (%.0f a %.0f min; piso %d, aula %d)"
          % (lo, hi, piso_min, AULA_MIN))
    return 0


if __name__ == u"__main__":
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/duracao.py <pasta-da-atividade> [piso_em_minutos]")
        sys.exit(2)
    piso = float(sys.argv[2]) if len(sys.argv) > 2 else 40.0
    sys.exit(confere(sys.argv[1], piso))
