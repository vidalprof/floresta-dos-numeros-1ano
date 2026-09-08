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

E nenhum portão via, porque nenhum portão contava o **tamanho** do trabalho: a
bancada media se funciona, se ilustra, se fala — nunca se DÁ AULA.

COMO ESTE PORTÃO MEDE (é uma ESTIMATIVA, e ele diz isso em voz alta):
  · a voz gravada: `falas.json` inteiro, a 2,6 palavras por segundo (a Francisca
    e o Antônio falam nesse passo com a pontuação da casa);
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
Sai 0 se enche a aula, 1 se ficou curta, 2 se não deu para medir.
============================================================
"""
import io
import json
import os
import re
import sys

PAL_POR_S = 2.6      # passo da voz da casa
S_POR_ITEM = 9.0     # ler, pensar e tocar (4o/5o ano)
S_POR_TELA = 12.0    # capa, cracha, banner, elogio

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
    seg_voz = 0.0
    camf = os.path.join(pasta, u"falas.json")
    if os.path.exists(camf):
        try:
            falas = json.loads(io.open(camf, encoding=u"utf-8").read())
            for f in falas:
                seg_voz += len((f.get(u"texto") or u"").split()) / PAL_POR_S
        except ValueError:
            print(u"%s -> falas.json ilegivel. NAO MEDI o tempo de voz." % pasta)
            return 2
    else:
        print(u"%s -> sem falas.json: NAO MEDI (MP3 nao se le)." % pasta)
        return 2

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
                if u"montador(" in corpo:
                    custo, gesto = 45.0, u"manipular"
                elif u"montaLigar(" in corpo:
                    custo, gesto = 14.0, u"ligar"
                else:
                    caixas = len(re.findall(r'\bcaixa\(', corpo)) or 1
                    custo, gesto = 25.0 * caixas, (u"digitar x%d" % caixas)
                if isinstance(lista[0], dict) and lista[0].get(u"hist"):
                    custo += 45.0            # ler e entender o problema
                    gesto = u"problema"
                itens += n
                seg_itens += n * custo
                detalhe.append((chave, n, gesto))

    # 3) quantas telas
    telas = len(re.findall(r'^function\s+tela\w+\(', html, re.M))

    seg = seg_voz + seg_itens + telas * S_POR_TELA
    mins = seg / 60.0

    print(u"%s -> ESTIMATIVA de duracao: %.0f min" % (pasta, mins))
    print(u"   voz gravada: %.0f min | %d itens para resolver | %d telas"
          % (seg_voz / 60.0, itens, telas))
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

    if mins < piso_min:
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
    print(u"   duracao ok: da para ocupar a aula (%.0f min, piso %d)"
          % (mins, piso_min))
    return 0


if __name__ == u"__main__":
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/duracao.py <pasta-da-atividade> [piso_em_minutos]")
        sys.exit(2)
    piso = float(sys.argv[2]) if len(sys.argv) > 2 else 40.0
    sys.exit(confere(sys.argv[1], piso))
