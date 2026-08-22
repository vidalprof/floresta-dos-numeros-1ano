#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO DAS DINÂMICAS — cada mecânica conferida pelas armadilhas DELA.

Cobrança do Marcos (ago/2026): *"veja, nós temos um leque de interatividades
muito grande, precisam ser TREINADAS, para quando for posta em prática não dar
todos esses erros"*.

Ele está certo sobre a causa. Toda vez que eu monto um caça-palavras, um jogo da
memória ou uma fase de arrastar, eu **escrevo aquilo do zero** — e repito um
defeito que já foi pago numa atividade anterior. São catorze mecânicas, cada uma
com as suas armadilhas; memória de humano (ou de máquina sem memória) não dá
conta. "Treinar" só vale se for MEDIDO, como os outros portões.

Aqui cada regra é uma linha nascida de um defeito que chegou até ele:

  CAÇA-PALAVRAS
    · célula em PORCENTAGEM, não px fixo — com px cabem 10 numa grade de 9 e a
      palavra quebra a linha ("TROCA e o A em outra linha", cobrado por ele);
    · se há palavra na diagonal, o enunciado TEM que avisar;
    · a grade publica `data-qa` — sem isso o auditor-jogador nunca fecha a fase.
  MEMÓRIA
    · verso de ARTE, não retângulo liso; virada 3D; carta grande (o piso de
      130×88 quem mede é o `_qa/leiaute.js`).
  ARRASTAR
    · nunca `preventDefault` no `touchstart` (mata o toque no celular);
    · guarda contra o evento de mouse FANTASMA que vem depois do toque;
    · caminho de TOQUE simples além do arrasto. Defeito pego DUAS vezes.
  TECLADO NA TELA (cruzadinha, forca, monte a palavra)
    · tem que aceitar TAMBÉM o teclado de verdade (`document.onkeydown`) — no PC
      da escola tem teclado e a criança vai digitar.
  FORCA
    · letra usada sai do alcance (senão a criança — e o auditor — toca nela para
      sempre);
    · a palavra a adivinhar vai SEM acento (o teclado não tem tecla de acento) e
      a da faixa vai COM.
  ESCOLHER / QUIZ
    · opções EMBARALHADAS: na Fábrica de Estrelas a certa era sempre a 1ª e a
      criança aprendia a posição, não o conteúdo.
  ACHAR NA CENA
    · a zona é a FIGURA recortada (grade de bits), não um pontinho com raio.

⚠️ Este portão AVISA onde não dá para ter certeza e REPROVA só o que é medível
sem ambiguidade. Portão que grita à toa é portão que ninguém lê.

Uso:  python3 _qa/dinamicas.py _naveg/index.html
Sai com 1 se alguma armadilha conhecida estiver aberta.
"""
import io
import re
import sys


def sem_comentarios(t):
    u"""tira comentario de HTML, de CSS/JS de bloco e de linha.

    Existe porque gatilho de portao tem que casar com o que a atividade FAZ, e
    nao com o que alguem escreveu explicando o que ela faz."""
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"/\*.*?\*/", " ", t, flags=re.S)
    t = re.sub(r"(?m)^\s*//.*$", " ", t)
    return t


def js_de(html):
    js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    return re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), js, flags=re.S)


def css_de(html):
    u"""⚠️⚠️ LICAO PAGA (ago/2026) — A TERCEIRA VEZ NA MESMA FAMILIA, e desta vez
    o comentario do proprio codigo mentia: dizia que *"o `js_de` e o `css_de` ja
    tiram comentario"*. O `js_de` tirava; o `css_de` NAO.

    O preco: eu escrevi, num comentario CSS da peca `escolher`, que aquele
    defeito *"e o mesmo que a `ouvir-achar` ja tinha pago"* — e o gatilho de
    "ouvir e achar" casou com a minha PROSA. A peca `escolher`, que nao toca
    som nenhum, passou a ser acusada de depender do som e a bancada reprovou.

    A regra, agora escrita nos dois lugares: **portao que le prosa mede prosa**.
    Gatilho casa com o que a peca FAZ, nunca com o que alguem escreveu
    explicando o que ela faz.

    ⚠️ A marca `/* ==== PECA: nome ==== */` fica: e comentario, mas e ESTRUTURA
    — e ela que separa os blocos de cada mecanica na atividade montada (lição
    ja paga logo abaixo, no `main`)."""
    css = "".join(re.findall(r"<style>(.*?)</style>", html, re.S))
    return re.sub(r"/\*(?!\s*====\s*PECA:).*?\*/",
                  lambda m: "\n" * m.group(0).count("\n"), css, flags=re.S)


def analisa(js, css, baixo, html=None):
    u"""⭐ AS ARMADILHAS SAO DA MECANICA, NAO DO ARQUIVO.

    Cada regra aqui pergunta uma coisa do tipo *"esta peca de CRIACAO tem som de
    tropeco?"*. Enquanto uma atividade tinha uma mecanica de cada, olhar o
    arquivo inteiro dava no mesmo. Numa atividade MONTADA sao DEZESSEIS mecanicas
    no mesmo arquivo — e ai a pergunta se perde: o `sErro()` legitimo de uma fase
    de quiz virava acusacao contra a fase de PINTAR, que nem chama `sErro`.
    Medido na primeira atividade montada: 2 armadilhas "abertas", nenhuma das
    duas existia. Portao que acusa o inocente ensina a ignorar portao.

    Por isso a analise virou funcao: o `main` roda uma vez por PECA quando o
    arquivo e montado, e cada regra volta a olhar so o codigo da mecanica dela.
    """
    usa, ruins, avisos = [], [], []

    # ---------------------------------------------------- CACA-PALAVRAS
    # ⚠️ TERCEIRO CONSERTO DO PROPRIO PORTAO, na mesma tarde (ago/2026). O gatilho
    #    era `.grade` + `data-qa` + a palavra "caca" EM QUALQUER LUGAR do arquivo,
    #    comentario inclusive — e uma CRUZADINHA que citava "mesma regra do
    #    caca-palavras" numa nota de CSS passou a ser cobrada pelas regras da
    #    mecanica errada (levou aviso de diagonal, que cruzadinha nao tem).
    #    O gatilho honesto e o que SO um caca-palavras publica: o `data-qa` da
    #    grade com o JSON das posicoes ({"PALAVRA":{"r":..,"c":..,"n":..}}).
    if re.search(r'\.grade\b', css) and re.search(
            r'setAttribute\("data-qa"\s*,\s*JSON\.stringify|"r"\s*:.{0,40}"c"\s*:.{0,40}"n"\s*:', js):
        usa.append("caca-palavras")
        # 1) celula em porcentagem
        cel = re.search(r'\.qcel\{([^}]*)\}|\.cel\{([^}]*)\}', css)
        largura_js = re.search(r'\.style\.width\s*=\s*\(?100\s*/\s*\w+', js)
        if not largura_js:
            regra = (cel.group(1) or cel.group(2)) if cel else ""
            if re.search(r'width\s*:\s*\d+px', regra):
                ruins.append(u"caca-palavras: a celula tem LARGURA FIXA em px. Numa grade de 9 "
                             u"cabem 10 e a palavra quebra a linha (defeito 'TROCA e o A em "
                             u"outra linha'). Use (100/N)%% + box-sizing:border-box.")
            else:
                avisos.append(u"caca-palavras: nao achei a largura da celula em porcentagem — "
                              u"confira que a grade fecha certo em 320px.")
        # 2) diagonal avisada
        tem_diag = re.search(r'\[1,\s*1\]|\[1,\s*-1\]|dl\s*:\s*|diagonal', js)
        if tem_diag and "diagonal" not in baixo:
            ruins.append(u"caca-palavras: ha palavra na DIAGONAL e o enunciado nao avisa. "
                         u"A crianca varre so linha e coluna e desiste.")
        # 3) data-qa para o auditor
        if not re.search(r'\.setAttribute\("data-qa"', js):
            avisos.append(u"caca-palavras: a grade nao publica data-qa — o auditor-jogador nao "
                          u"consegue fechar a fase e vai dar 'PRESO' num lugar que funciona.")
        # 4) ⭐ MODO DEFINICOES (ago/2026, copiado do EdiLIM). No lugar da lista de
        #    palavras vao as PISTAS: a crianca pensa na palavra e SO DEPOIS procura.
        #    Modo novo nasce com o portao que o mede — senao e caminho que ninguem
        #    confere, que foi como nasceram os defeitos que chegaram ao professor.
        if re.search(r'PALDEF', js):
            if not re.search(r'"zap"', js) or not re.search(r'\.zap\{', css):
                ruins.append(u"caca-palavras (definicoes): a pista e TEXTO e nao tem "
                             u"alto-falante. Quem ainda le devagar fica de fora justo na "
                             u"parte que virou o conteudo da fase.")
            if len(re.findall(r'setAttribute\("data-qa"', js)) < 2:
                avisos.append(u"caca-palavras (definicoes): o chip mostra a PISTA, entao o "
                              u"auditor-jogador nao sabe de que palavra ele e. Publique a "
                              u"palavra em data-qa no chip, senao sai 'PRESO' numa fase boa.")
            bloco = re.search(r'PALDEF\s*=\s*\{(.*?)\n\};', js, re.S)
            if bloco:
                for mm in re.finditer(r'"([A-ZÀ-Ü]{3,})"\s*:\s*"([^"]{5,})"', bloco.group(1)):
                    if mm.group(1).lower() in mm.group(2).lower():
                        ruins.append(u"caca-palavras (definicoes): a pista de %s CONTEM a "
                                     u"propria palavra. Ai a crianca copia as letras em vez "
                                     u"de pensar — o modo perde a razao de existir."
                                     % mm.group(1))

    # ---------------------------------------------------- MEMORIA
    if re.search(r'\.mcarta|\.mcard', css):
        usa.append("memoria")
        if "rotateY" not in css and "rotatey" not in css.lower():
            avisos.append(u"memoria: nao achei a virada 3D (rotateY). Carta que troca de face "
                          u"sem girar perde metade da graca.")
        verso = re.search(r'VERSO\s*=\s*([^;]{0,200})', js)
        if verso and "img" not in verso.group(1) and "imgEl" not in verso.group(1):
            ruins.append(u"memoria: o VERSO da carta nao usa imagem — retangulo liso nao e "
                         u"ilustracao. Regra da casa: verso de arte de IA.")

    # ---------------------------------------------------- RIMA (achar o par que rima)
    # Mecanica nova (ago/2026, da pesquisa fonologica): o par e por SOM do fim,
    # num tabuleiro de cartas viradas para cima. Regra da casa: mecanica nova =
    # linha no _padrao/DINAMICAS.md E regra AQUI, no mesmo commit. Gatilho honesto:
    # so esta peca tem a carta `.rmc` E casa por `rimam(`.
    if re.search(r'\.rmc\b', css) and re.search(r'\brimam\s*\(', js):
        usa.append("rima")
        # ⭐ A ARMADILHA NUMERO UM: tabuleiro NAO embaralhado. Se as cartas ficam na
        #    ordem em que foram escritas, a crianca decora a POSICAO do par em vez
        #    de escutar o fim da palavra — a fase perde a razao de existir.
        #    ⚠️ `baguncar` vem DECLARADO no motorzinho de toda peca: declarar nao e
        #    usar (a mesma pedra de colorir/ligar-pontos/letras-escondidas). So
        #    conta CHAMADA de verdade.
        _mist = [m for m in re.finditer(r'\b(?:baguncar|embaralhar?|shuffle)\s*\(', js)
                 if not js[max(0, m.start() - 9):m.start()].rstrip().endswith("function")]
        if not _mist:
            ruins.append(u"rima: o tabuleiro nao e EMBARALHADO. A crianca decora a posicao do "
                         u"par em vez de escutar o som do fim — a rima e do ouvido, nao do lugar.")
        # a rima e do OUVIDO: cada carta tem que poder falar. Na atividade o motor
        # poe o alto-falante pela classe `.ptxt`; sem ela, quem ainda soletra
        # escolhe pelo desenho e a fase vira loteria.
        if not re.search(r'\bptxt\b', css + js) and not re.search(r'data-voz', js):
            ruins.append(u"rima: as cartas nao tem alto-falante (classe .ptxt / data-voz). A "
                         u"rima e do ouvido — quem ainda le devagar fica de fora justo no "
                         u"conteudo da fase.")
        # erro NAO pune: o andaime tem que crescer (dica -> ver o par -> revela)
        if not re.search(r'function\s+revela\b', js):
            avisos.append(u"rima: nao achei o 3o degrau do andaime (revela). Sem ele, quem erra "
                          u"tres vezes fica sem o par aceso e pode travar.")

    # ------------------------------------------- BATER AS SILABAS (contar)
    # Gatilho honesto: so esta mecanica publica um TAMBOR (`.bsBater`) junto com
    # marcas que NASCEM do dedo (`.bsBatida`). E mecanica de CONTAGEM POR GESTO —
    # a resposta nao e escolher, e bater o numero certo de vezes.
    if re.search(r'\.bsBater\b', css) and re.search(r'\.bsBatida\b', css):
        usa.append("bater silabas")
        # ⭐ A ARMADILHA NUMERO UM desta familia: desenhar os lugares prontos.
        #    Se a tela ja mostra 3 casinhas, a crianca conta as CASINHAS e nao os
        #    pedacos da palavra — a resposta esta dada e a fase nao mede nada.
        #    ⚠️ a 1a versao desta regra tambem escapou no teste do mutante: ela
        #    perdoava o arquivo inteiro se a palavra "revela" aparecesse em
        #    qualquer lugar (o 3o degrau do andaime, que PODE desenhar). Agora
        #    olha o LUGAR certo: a linha que cria a linha das batidas. Ela tem
        #    que nascer VAZIA — o que vier depois e outro assunto.
        _bx = re.search(r'["\']bsBatidas["\']', js)
        if _bx and re.search(r'bsBatida["\']', js[_bx.end():_bx.end() + 400]):
            ruins.append(u"bater silabas: as batidas ja nascem desenhadas na tela. A crianca "
                         u"conta as marcas em vez de contar os pedacos da palavra — a "
                         u"resposta esta dada.")
        # contar errado no meio nao pode prender: tem que dar para APAGAR
        # ⚠️ esta regra ja escapou uma vez no teste do mutante: ela aceitava a
        #    PALAVRA "apagar" — e o rotulo do botao continuava escrito mesmo
        #    depois de eu arrancar o botao. Palavra na tela nao e botao que
        #    funciona. Agora cobra o par: a classe estilizada no CSS **e** usada
        #    no JS. Regra que so le texto nao mede nada.
        if not (re.search(r'\.bsLimpa\b', css) and re.search(r'bsLimpa', js)):
            ruins.append(u"bater silabas: nao achei o APAGAR. Quem se perdeu no meio da "
                         u"contagem fica preso com um numero que sabe que esta errado.")
        # ⭐ AS DUAS PORTAS (regra do Marcos, ago/2026): no PC da escola tem
        #    teclado de verdade, e a crianca vai usar.
        if not re.search(r'onkeydown|keydown', js):
            ruins.append(u"bater silabas: so da para bater com o dedo. No PC da escola tem "
                         u"teclado — a barra de espaco tambem tem que bater (as duas portas).")
        # o andaime do 2o degrau desta mecanica e pelo OUVIDO, nao escrito
        if not re.search(r'ecoDoRitmo|ritmo\s*\(', js):
            avisos.append(u"bater silabas: nao achei o eco do RITMO (a peca batendo junto). "
                          u"Sem ele o 2o degrau do andaime vira texto, e quem nao le "
                          u"nao tem por onde subir.")

    # ---------------------------------------------------- ARRASTAR
    if re.search(r'touchstart', js):
        usa.append("arrastar/toque")
        # ⚠️ LICAO PAGA (ago/2026): isto lia uma JANELA FIXA de 300 caracteres
        #    depois do `touchstart`, e a janela invadia o handler seguinte. Uma
        #    peca com `preventDefault` no TOUCHMOVE — onde ele e necessario, para
        #    a pagina nao rolar durante o arrasto — levava a acusacao de matar o
        #    toque. Agora conta as chaves e le o corpo DE VERDADE do handler.
        for m in re.finditer(r'touchstart["\']?\s*,\s*function\s*\([^)]*\)\s*\{', js):
            k, prof = m.end() - 1, 0
            while k < len(js):
                if js[k] == "{":
                    prof += 1
                elif js[k] == "}":
                    prof -= 1
                    if prof == 0:
                        break
                k += 1
            corpo_ts = js[m.end():k]
            if "preventDefault" in corpo_ts:
                ruins.append(u"arrastar: ha preventDefault dentro do touchstart. Isso MATA o "
                             u"toque no celular — a peca nao pega.")
                break
        if not re.search(r'ultimoToque|ultToque|__toque|toqueAgora', js):
            avisos.append(u"arrastar: nao achei o guarda contra o evento de mouse FANTASMA que o "
                          u"celular dispara depois do toque (ele desmarca a peca). "
                          u"Defeito ja pego DUAS vezes.")

    # ---------------------------------------------------- TECLADO NA TELA
    tecla_tela = re.search(r'\.tec\b|\.tecl\b|teclafc|tecladofc', css) or re.search(r'"tec"|"tecl"', js)
    if tecla_tela:
        usa.append("teclado na tela")
        if "document.onkeydown" not in js and "addEventListener(\"keydown\"" not in js:
            ruins.append(u"teclado na tela: a fase NAO aceita o teclado de verdade "
                         u"(document.onkeydown). No PC da escola tem teclado e a crianca vai "
                         u"digitar. Regra das DUAS PORTAS.")

    # ---------------------------------------------------- FORCA
    if re.search(r'FORCA|forca', js):
        usa.append("forca")
        if not re.search(r'usada', js):
            avisos.append(u"forca: nao achei a marca 'usada' na letra ja tocada. Letra que "
                          u"continua clicavel prende a crianca (e o auditor) para sempre.")
        # ⭐ MODO NOVO (ago/2026, do EdiLIM): a figura como PREMIO — ela fica
        #    tapada e so aparece quando a palavra e descoberta. Regra da casa:
        #    modo novo nasce com o portao que o mede, senao vira caminho que
        #    ninguem confere. O que se cobra aqui e a promessa da casa: ERRO NAO
        #    PUNE. Se a figura so se revela em `fecha()`, quem gastou os seis
        #    baloes fica sem ver o bicho — a recompensa vira castigo, que e
        #    exatamente o contrario do que a peca existe para fazer.
        if re.search(r'FORCA_FIG', js):
            if not re.search(r'function\s+revelaFig', js):
                avisos.append(u"forca (figura-premio): nao achei a funcao que revela a figura. "
                              u"Sem ela o modo 'premio' esconde e nunca mostra.")
            else:
                corpo_entrega = re.search(r'function\s+entrega\s*\(\s*\)\s*\{(.*?)\n  \}', js, re.S)
                if corpo_entrega and "revelaFig" not in corpo_entrega.group(1):
                    ruins.append(u"forca (figura-premio): a figura NAO e revelada quando os "
                                 u"baloes acabam. Quem nao descobriu a palavra fica sem ver a "
                                 u"figura — recompensa que vira castigo. Erro nao pune.")

    # ------------------------------------- QUEBRA-CABECA: o FUNDO como andaime
    # ⭐ MODO NOVO (ago/2026, copiado do EdiLIM, que deixa o autor regular a
    #    opacidade do desenho por baixo do tabuleiro). Aqui ele nao depende de
    #    ninguem escolher: comeca escondido e CHEGA NO ERRO (2o fraco, 3o forte).
    #    Duas coisas se medem, e as duas ja custaram caro noutras pecas:
    #    (a) fundo que comeca invisivel e nunca acende = andaime morto;
    #    (b) ajuda que existe SO na imagem — a dica tem que DIZER que o desenho
    #        apareceu, senao quem nao enxerga bem (ou olhava para o banco) nao
    #        percebe que a peca acabou de ajudar.
    if re.search(r'\.qcfundo', css):
        usa.append("quebra-cabeca (fundo-andaime)")
        comeca_escondido = re.search(r'\.qcfundo\{[^}]*opacity\s*:\s*0[^.\d]', css)
        if comeca_escondido:
            if "poeFundo" not in js:
                ruins.append(u"quebra-cabeca: o fundo apagado comeca invisivel e NADA o acende. "
                             u"Andaime morto: a crianca erra e a ajuda nunca chega.")
            elif not re.search(r'apagadinho|desenho', js):
                avisos.append(u"quebra-cabeca: o fundo aparece mas a dica nao DIZ isso. Ajuda "
                              u"so na imagem passa batido para quem estava olhando o banco.")

    # ---------------------------------------------------- ESCOLHER / QUIZ
    if re.search(r'el\("div","opt"|"opt"', js):
        usa.append("escolher")
        # ⚠️ TERCEIRA VEZ QUE ESTE DEFEITO APARECE (ago/2026) — por isso virou
        #    REGRA MEDIDA, nao licao escrita. Com 2 distratores a crianca elimina
        #    tudo antes do 3o erro: o degrau REVELAR nunca acontece (codigo morto)
        #    e sobra uma tela com uma opcao so, onde o auditor fica PRESO.
        for mm in re.finditer(r'alts?\s*=\s*\[(.{0,600}?)\]\s*;', js, re.S):
            corpo = mm.group(1)
            erradas = len(re.findall(r'false', corpo))
            if 0 < erradas < 3 and corpo.count("[") >= 2:
                avisos.append(u"escolher: uma rodada tem so %d opcao(oes) ERRADA(S). "
                              u"Com menos de 3, a crianca elimina tudo antes do 3o "
                              u"erro e o degrau 'revelar' vira codigo morto." % erradas)
                break
        if not re.search(r'baguncar\(|embaralh|shuffle', js):
            ruins.append(u"escolher: as opcoes nao sao EMBARALHADAS. Na Fabrica de Estrelas a "
                         u"certa era sempre a 1a e a crianca aprendeu a posicao, nao o conteudo.")

    # ---------------------------------------------------- OUVIR E ACHAR
    # ⚠️ ACUSOU O INOCENTE (ago/2026, na varredura das 74 pecas): o gatilho era
    #    `speechSynthesis` + opcoes na tela. So que `speechSynthesis` e a voz de
    #    reserva do navegador, usada por VARIAS pecas para ler a resposta em voz
    #    alta — nao e a marca desta mecanica. Cinco pecas casavam, e so UMA era
    #    de ouvir e achar; as outras quatro levavam a cobranca de "a palavra tem
    #    que estar escrita junto", que nem se aplica a elas. Duas reprovaram a
    #    bancada por isso (ensinar-mascote e medir).
    #    A marca de verdade e a peca TOCAR O ALVO para a crianca procurar: uma
    #    funcao que toca o que se quer achar (`tocaAlvo`), ou o nome dela.
    if re.search(r'ouvir.?e.?achar|ouvir-achar|tocaAlvo|pecaOuvir', css + js, re.I) and \
       re.search(r'"opt"|\.fig\b', css + js):
        usa.append("ouvir e achar")
        # ⚠️ PC de escola sem caixa de som existe: a peca NAO pode depender do som
        if not re.search(r'palavra|texto|escrit', js, re.I):
            ruins.append(u"ouvir e achar: nao achei a palavra ESCRITA junto. A peca "
                         u"nao pode depender so do som — PC de escola sem caixa de "
                         u"som existe, e a crianca surda tambem.")

    # ---------------------------------------------------- PASSO A PASSO (a receita)
    if re.search(r'receita|passo.?a.?passo|\.fita\b', css + js, re.I) and \
       re.search(r'executa|roda|encena', js, re.I):
        usa.append("passo a passo")
        if not re.search(r'[Aa]rrumar|[Cc]onsertar|[Dd]epura', js):
            avisos.append(u"passo a passo: falta o ARRUMAR que preserva a ordem "
                          u"montada. Recomecar do zero apaga o raciocinio dela; "
                          u"depurar e a metade que ensina.")

    # ---------------------------------------------------- RELOGIO DE PONTEIROS
    if re.search(r'ponteir|\.mostrador\b|\.horas\b', css + js, re.I):
        usa.append("relogio")
        if not re.search(r'5|cinco', js):
            avisos.append(u"relogio: nao achei o encaixe de 5 em 5 minutos. Dedo de "
                          u"crianca nao tem precisao de minuto.")
        if not re.search(r'peq|pequeno|hora.*prop|prop.*hora', js, re.I):
            avisos.append(u"relogio: o ponteiro PEQUENO tem que andar junto, "
                          u"proporcional — e isso que ensina que as 3h30 ele fica "
                          u"ENTRE o 3 e o 4.")

    # ---------------------------------------------------- PECA COM MODOS (licao do EdiLIM)
    # ⭐ ago/2026: as pecas comecaram a ganhar MODOS (`var MODO=`), que e como o
    #    EdiLIM tira "mais de 50 atividades" de ~40 paginas. Modo novo e caminho
    #    NOVO — e a regra da casa e que caminho sem portao e caminho que ninguem
    #    confere, que e exatamente como nasceram os defeitos que chegaram ao
    #    Marcos. Este bloco cobra as armadilhas de cada modo que a casa conhece.
    #    ⚠️ o gatilho e ESTREITO de proposito: so dispara quando o arquivo
    #    declara `var MODO=` E usa um dos modos conhecidos pelo nome. Sem isso
    #    ele acusaria qualquer arquivo com uma variavel chamada MODO (a
    #    `_aventura` tem uma, e nao e disto que ela fala).
    tem_modo = re.search(r'\bvar\s+MODO\s*=', js)
    modos_vistos = [m for m in (u"hover", u"escrever", u"mostrar")
                    if ('"%s"' % m) in js]
    if tem_modo and modos_vistos:
        usa.append(u"modos (" + u", ".join(modos_vistos) + u")")
        if u"hover" in modos_vistos:
            # ⚠️ NO CELULAR NAO EXISTE PASSAR O MOUSE. Modo de hover sem caminho
            #    de toque deixa a fase INACESSIVEL no telefone — e metade da
            #    escola joga no telefone.
            # ⚠️ LICAO PAGA NA HORA DE ESCREVER ESTE PORTAO: a primeira versao
            #    perguntava se a palavra "onclick" existia EM ALGUM LUGAR do
            #    arquivo. Existe sempre (o botao de recomecar, o banner...), e o
            #    portao nunca reprovaria — eu quebrei a peca de proposito e ele
            #    aprovou. A pergunta certa e sobre O MESMO ELEMENTO: quem recebe
            #    `onmouseover` tem que receber `onclick` tambem.
            for alvo in set(re.findall(r'(\w+)\.onmouseover\s*=', js)):
                if not re.search(r'\b' + re.escape(alvo) + r'\.onclick\s*=', js):
                    ruins.append(u"modo hover: `%s.onmouseover` sem `%s.onclick`. No "
                                 u"celular nao existe passar o mouse: sem o caminho do "
                                 u"TOQUE no MESMO elemento a fase fica inacessivel no "
                                 u"telefone." % (alvo, alvo))
            # ⚠️ o celular dispara mouseover/mousedown FANTASMA depois do dedo
            if not re.search(r'ultimoToque|souDedo|ehFantasma', js):
                ruins.append(u"modo hover: falta o guarda do evento de rato FANTASMA "
                             u"(`ultimoToque`/`souDedo`). Depois do toque o celular "
                             u"dispara `mouseover` sozinho e o mesmo ponto e lido duas "
                             u"vezes. Defeito ja pego DUAS vezes nesta casa.")
        if u"escrever" in modos_vistos:
            # a regra das DUAS PORTAS, cobrada com todas as letras pelo Marcos.
            # ⚠️ pergunta pelo HANDLER, nao pelo nome: `document.onkeydown=null`
            #    (que toda tela faz para nao prender o teclado na fase anterior)
            #    contem o nome e faria o portao aprovar uma peca que nao escuta
            #    tecla nenhuma. Medido: quebrei a peca de proposito e a primeira
            #    versao deste portao deixou passar.
            liga = re.search(r'document\.onkeydown\s*=\s*(?!null\b)\S', js)
            if not liga and u'addEventListener("keydown"' not in js:
                ruins.append(u"modo escrever: nao achei o `document.onkeydown`. Quem "
                             u"digita na tela tem que poder digitar no teclado de "
                             u"verdade — no PC da escola tem teclado e a crianca vai "
                             u"usar. Regra das DUAS PORTAS.")
        if u"mostrar" in modos_vistos and not re.search(r'sTap|sCerto|fala\(|diz\(', js):
            avisos.append(u"modo mostrar: nao ha resposta certa nele, entao o que nao "
                          u"pode existir e SILENCIO. Tocar num ponto ja visto tem que "
                          u"responder (som ou voz), senao a crianca acha que travou.")

    # ---------------------------------------------------- DOMINO
    if re.search(r'\bdomino\b|\.pdom\b|\.corrente\b', css + js, re.I):
        usa.append("domino")
        avisos.append(u"domino: a corrente tem que ser montada de antemao, com semente "
                      u"no meio — senao sobra peca que nao encaixa em lugar nenhum e a "
                      u"crianca fica presa sem culpa.")

    # ---------------------------------------------------- BINGO
    if re.search(r'\bbingo\b|\.cartela\b|\.pedra\b', css + js, re.I):
        usa.append("bingo")
        ruins_bingo = not re.search(r'nao tenho|n&#227;o tenho|naoTenho', html, re.I)
        if ruins_bingo:
            avisos.append(u"bingo: falta o botao 'nao esta na minha cartela'. Sem ele a "
                          u"crianca so pode acertar tocando, e o jogo vira loteria.")

    # ---------------------------------------------------- TRILHA COM DADO
    if re.search(r'\btrilha\b|\.peao\b|\.dado\b|\.casa\b', css + js, re.I):
        usa.append("trilha")
        if re.search(r'setTimeout\([^)]*rola|rolaAuto|autoRola', js):
            ruins.append(u"trilha: o dado rola SOZINHO. Rolar e o gesto da crianca — "
                         u"e a espera dela que faz a graca.")

    # ---------------------------------------------------- MEDIR COM A REGUA
    if re.search(r'\bregua\b|\.regua', css + js, re.I):
        usa.append("medir")
        if not re.search(r'zero|\bcm\b', js, re.I):
            avisos.append(u"medir: nao achei o ZERO. O erro que esta mecanica existe "
                          u"para ensinar e comecar a medir do 1 — o zero tem que ser "
                          u"visivel e ter encaixe com tolerancia.")

    # ---------------------------------------------------- CALENDARIO
    # o gatilho pelo NOME do arquivo falha: a peca se chama calendario mas nao usa
    # a palavra por dentro. As marcas de verdade sao a semana e os pulos.
    if re.search(r'"semana"|\.semana\b', css + js) and re.search(r'"pulos"|\.dia\b|\.diac\b', css + js):
        usa.append("calendario")
        if not re.search(r'pulo|salto|conta', js, re.I):
            avisos.append(u"calendario: contar de um dia a outro tem que ser um PULO "
                          u"visivel, casa por casa. Sem o pulo vira conta de cabeca.")

    # ---------------------------------------------------- COMPARAR (maior/menor)
    if re.search(r'&gt;|&lt;|maior que|menor que', html) and re.search(r'compara', css + js, re.I):
        usa.append("comparar")
        if not re.search(r'fileira|coluna|barra|monte|torre', js, re.I):
            ruins.append(u"comparar: o sinal aparece sem as duas quantidades LADO A "
                         u"LADO. A crianca tem que VER quem tem mais antes de escolher "
                         u"o simbolo — senao decora o bico do sinal.")

    # ---------------------------------------------------- LABIRINTO
    # ⚠️ o gatilho `.seta` acusava o 3o ano (a rota do Nico usa setas) de ser um
    #    labirinto com vida e derrota. Gatilho tem que ser EXPLICITO.
    if re.search(r'\blabirint', css + js, re.I):
        usa.append("labirinto")
        if "onkeydown" not in js and 'addEventListener("keydown"' not in js:
            ruins.append(u"labirinto: so ha botao na tela. AS DUAS PORTAS — no PC da "
                         u"escola a crianca vai usar as SETAS DO TECLADO.")
        # ⚠️ ACUSOU O INOCENTE (ago/2026): `vida` sem fronteira de palavra casa
        #    dentro de "atiVIDAde" — e a palavra "atividade" esta em toda parte.
        #    O labirinto dizia, no proprio comentario, "sem vida perdida, sem fim
        #    de jogo", e mesmo assim levava a acusacao.
        if re.search(r'\bvidas?\b|game ?over|morreu|perdeu', js, re.I):
            ruins.append(u"labirinto: ha vida/derrota. Encostar no inimigo NAO e "
                         u"castigo — volta ao comeco do trecho e segue.")
        if not re.search(r'setAttribute\("data-qa"', js):
            avisos.append(u"labirinto: nao publica o proximo passo em data-qa — o "
                          u"auditor-jogador nao consegue atravessar e dara 'PRESO'.")

    # ---------------------------------------------------- PINTAR / LIVRO DE COLORIR
    # ⚠️ QUASE ACUSEI O INOCENTE (ago/2026, na mesma noite em que consertei tres
    #    portoes por isso). A regra era `.tcor|.tinta|paleta` — e o "PINTE O MAPA"
    #    do 3o ano tem paleta, mas e PINTURA COM GABARITO (azul e a agua, verde e a
    #    mata): ali existe certo e errado, e o som de tropeco e legitimo. O que
    #    distingue o LIVRO DE COLORIR e o BALDE: so a pintura livre tem balde de
    #    tinta, porque so nela a crianca escolhe a cor sem resposta certa.
    if re.search(r'\.balde\b', css):
        usa.append("colorir")
        if not re.search(r'[Rr]ecome|[Ll]impar|[Aa]pagar', js):
            avisos.append(u"colorir: nao achei o RECOMECAR. Criança que se arrepende "
                          u"precisa poder voltar sem perder a vontade.")
        # ⚠️ `sErro` vem DECLARADO no motorzinho do molde em toda peca. So conta
        #    se for CHAMADO — declarar nao e usar.
        # a DECLARACAO e `function sErro(){...}`: olhar o que vem ANTES do nome.
        usos = [m for m in re.finditer(r'\bsErro\s*\(\s*\)', js)
                if not js[max(0, m.start()-9):m.start()].rstrip().endswith("function")]
        if usos:
            ruins.append(u"colorir: ha som de tropeco numa peca de CRIACAO. Aqui nao "
                         u"existe certo e errado — e desenho dela.")

    # ---------------------------------------------------- LIGAR PONTOS
    # ⚠️ `.pt` sozinho e generico demais: o ARRASTAR-LUGAR tambem tem uma classe
    #    `.pt`, e levava as regras de ligar-pontos. Agora o gatilho pede tambem a
    #    palavra "ponto" no codigo — quem liga pontos fala em pontos.
    if (re.search(r'ligar.?pontos', css)
            or (re.search(r'\.pt\b', css) and re.search(r'\bpontos?\b', js, re.I))) \
            and re.search(r'proximo|ordem', js, re.I):
        usa.append("ligar pontos")
        # ⚠️ MESMO DESCUIDO DUAS VEZES NA MESMA NOITE: `sErro` vem DECLARADO no
        #    motorzinho de toda peca. Eu tinha consertado isso em "colorir" e
        #    repeti aqui. Declarar nao e usar — e o portao acusou o inocente.
        usos = [m for m in re.finditer(r'\bsErro\s*\(\s*\)', js)
                if not js[max(0, m.start()-9):m.start()].rstrip().endswith("function")]
        if usos:
            avisos.append(u"ligar pontos: tocar no ponto errado nao deve punir — so "
                          u"nao liga.")

    # ---------------------------------------------------- PINTAR / MARCA-TEXTO
    # ⚠️ BURACO ACHADO PELO PROPRIO PROFISSIONAL QUE MONTOU A PECA (ago/2026):
    #    `pintar.html` passou na bancada com "0 dinamica reconhecida" — ou seja,
    #    passou SEM SER MEDIDO nesta parte. Portao que nao conhece a mecanica da
    #    uma aprovacao vazia, que e pior que reprovar.
    # ⚠️ FALSO POSITIVO PAGO NA MESMA TARDE: a regra era `\.pal\b` em css+js, e
    #    uma peca de DIGITAR que tinha uma propriedade de dados chamada `r.pal`
    #    passou a ser reconhecida como marca-texto e levou avisos que nao eram
    #    dela. Portao que acusa o inocente vale menos que portao nenhum: agora a
    #    classe `.pal` so conta se estiver no CSS (onde classe mora de verdade).
    if re.search(r'\.pal\b|pintada|marcatexto', css) or re.search(r'marca-texto', css + js):
        usa.append("pintar/marca-texto")
        if not re.search(r'background-size|tracocorre|transition[^;]*background', css):
            avisos.append(u"pintar: nao achei o TRACO CORRENDO (transicao de "
                          u"background-size). Marca que aparece de uma vez nao tem "
                          u"a sensacao de riscar.")
        if not re.search(r'[Ff]alta|restam|de \d+|contador|barra', js):
            avisos.append(u"pintar: nao achei quantas FALTAM. Sem o contador a "
                          u"crianca nao sabe quando parou de faltar.")
        # a marca nao pode ser SO cor
        if not re.search(r'font-weight|text-decoration|border-bottom|content\s*:', css):
            ruins.append(u"pintar: a palavra pintada parece marcada SO PELA COR. "
                         u"Quem nao distingue a cor nao ve o que ja marcou — "
                         u"precisa de negrito, traco ou sinal junto.")

    # ---------------------------------------------------- ACHAR NA CENA
    if re.search(r'naZona\(|pzona\(|ZONAS\b', js):
        usa.append("achar na cena")
        if re.search(r'Math\.sqrt\(.{0,40}raio|dist\s*<\s*\d+', js) and not re.search(r'naZona\(', js):
            ruins.append(u"achar na cena: o alvo e um PONTO com raio, nao a figura recortada. "
                         u"A crianca toca na coisa certa e o app diz que errou.")

    # ==================================================================
    # ⭐ AS DEZ MECANICAS QUE O PORTAO NAO ENXERGAVA (medido em ago/2026)
    #
    # Contei quantas das 77 pecas do catalogo este portao reconhecia: 67. As
    # outras DEZ saiam com "0 dinamica reconhecida" — o aviso existe e e honesto,
    # mas aviso nao pega defeito. A regra da casa (CLAUDE.md) e clara: *"Mecanica
    # nova = linha nova no arquivo E regra nova no portao, no mesmo commit"*; ela
    # nao foi cumprida para estas dez.
    #
    # Cada regra abaixo cobra o que a PROPRIA peca aprovada ja faz — o gatilho e
    # uma marca que so aquela mecanica publica, e a cobranca sai da lista "AS
    # ARMADILHAS QUE ESTA PECA FECHA" que esta escrita no cabecalho dela. Assim a
    # regra nao inventa exigencia nova: ela impede que a COPIA perca o que a
    # original ja tinha certo — que e de onde vem quase todo defeito nosso.
    # ==================================================================

    # ---------------------------------------------------- BALANCA DA IGUALDADE
    if re.search(r'\.viga\b', css) and re.search(r'\.prato\b', css):
        usa.append("balanca")
        # O MOVIMENTO E O ARGUMENTO: a viga tem que GIRAR, com transicao. Balanca
        # que so troca de figura (nivelada/torta) nao ensina — e a descida do
        # prato mais pesado que faz a crianca dizer "esse lado tem mais".
        viga = re.search(r'\.viga\{([^}]*)\}', css)
        if not (viga and re.search(r'transition', viga.group(1))):
            ruins.append(u"balanca: a viga nao tem TRANSICAO — ela vai pular de uma posicao "
                         u"para a outra. O que ensina aqui e o movimento: o prato mais pesado "
                         u"DESCENDO devagar. Sem isso vira so duas figuras.")
        # ⚠️ e a minha propria regra ja nasceu ACUSANDO INOCENTE: procurei
        #    `rotate` so no CSS, e a balanca aprovada gira pelo JS
        #    (`style.webkitTransform="rotate("+g+"deg)"`). Onde a peca faz a
        #    coisa certa e onde a regra olha tem que ser o MESMO lugar.
        if not re.search(r'rotate', js + css):
            ruins.append(u"balanca: a viga nao gira (`rotate`). Balanca que nao inclina nao e "
                         u"balanca: e desenho.")
        # nada essencial so na cor: o estado tem que estar ESCRITO tambem
        if not re.search(r'leve|pesad|igual', baixo):
            ruins.append(u"balanca: o estado dos pratos nao esta escrito em lugar nenhum "
                         u"(leve / pesado / igual). Quem nao distingue a inclinacao fica sem nada.")

    # ---------------------------------------------------- BUSSOLA (orientar-se)
    if re.search(r'\.rosa\b', css) and re.search(r'\.vento\b|\.ventos\b', css):
        usa.append("bussola")
        # a resposta sai da POSICAO no mapinha, calculada — nunca escrita a mao
        if not re.search(r'dirDe\s*\(|function\s+dirDe', js):
            ruins.append(u"bussola: a direcao certa nao e CALCULADA da posicao no mapinha. "
                         u"Escrita a mao, um dia o desenho muda e a resposta fica mentindo.")
        # a rosa dos ventos e a REGUA: fica na tela o tempo todo, nao e dica
        if re.search(r'\.rosa[^{]*\{[^}]*display\s*:\s*none', css):
            ruins.append(u"bussola: a rosa dos ventos comeca escondida. Ela nao e dica, e a "
                         u"regua da fase — sem ela 'leste' nao quer dizer nada para a crianca.")

    # ---------------------------------------------------- CONTADORES (produzir)
    if re.search(r'\.canteiro\b', css) and re.search(r'\.sem\b|\.semente\b', css):
        usa.append("contadores")
        # o total NUNCA e digitado: ele nasce de contar o que a crianca montou
        if re.search(r'type\s*=\s*["\']text["\']', js + css):
            ruins.append(u"contadores: apareceu campo de texto. O total desta mecanica tem que "
                         u"NASCER DA CONTAGEM item a item — digitar devolve o chute que a peca "
                         u"existe para tirar.")
        # passo de UM: o pulo esconde justamente a contagem
        if re.search(r'[+\-]=\s*[2-9]\b', js):
            ruins.append(u"contadores: ha botao que anda mais de UM por vez. O pulo esconde a "
                         u"contagem um-a-um, que e o conteudo da fase.")

    # ---------------------------------------------------- ESCREVER (producao)
    if re.search(r'\.apoios\b', css) and re.search(r'\.campo\b', css):
        usa.append("escrever")
        # risco vermelho e o X disfarcado
        if not re.search(r'spellcheck\s*=\s*["\']?false', js + (html or "")):
            ruins.append(u"escrever: falta `spellcheck=false`. O risco vermelho do navegador e "
                         u"um X disfarcado embaixo da palavra — e aqui NAO se corrige ortografia.")
        # o texto dela tem que voltar para ela
        if not re.search(r'suatxt|placa', css):
            avisos.append(u"escrever: nao achei onde o texto DELA aparece no fim. Devolver o "
                          u"texto e o que faz a crianca querer escrever de novo.")

    # ---------------------------------------------------- TESTE JUSTO (variavel)
    if re.search(r'\.colv\b', css) and re.search(r'\.dif\b', css):
        usa.append("teste justo")
        # o aviso e PERGUNTA, nunca bronca
        if re.search(r'errou|voce errou|esta errado', baixo):
            ruins.append(u"teste justo: ha 'errou' escrito. Aqui o mascote PERGUNTA ('se mudei "
                         u"duas coisas, como vou saber quem fez a planta crescer?') — a trava ja "
                         u"e o conceito, bronca so estraga.")
        # comparar so quando e justo: tem que haver a trava
        # ⚠️ segundo alarme falso da mesma leva: a trava desta peca e a CLASSE
        #    `btn trava` (`el("button","btn trava")`), e eu procurava `\.trava`
        #    com ponto, que so casa em seletor de CSS.
        if not re.search(r'disabled|trava|podeComparar', js + css):
            ruins.append(u"teste justo: nao achei a TRAVA do comparar. Sem ela a crianca conclui "
                         u"de um teste com duas mudancas — que e exatamente o contrario do que a "
                         u"fase ensina.")

    # ---------------------------------------------------- PENEIRA / FILTRO
    if re.search(r'\.peneira\b', css) and re.search(r'\.furos\b', css):
        usa.append("filtro")
        # os DOIS lados contam: o que passou e o que ficou
        if not (re.search(r'\.cesta\b', css) and re.search(r'\.vpas\b|passou', css + baixo)):
            ruins.append(u"filtro: so um lado do resultado aparece. A criterio da peneira so fica "
                         u"claro vendo O QUE PASSOU e O QUE FICOU, lado a lado.")

    # ---------------------------------------------------- SIMETRIA (espelhar)
    if re.search(r'\.gradesim\b', css) or (re.search(r'\.eixov\b', css) and re.search(r'\.eixoh\b', css)):
        usa.append("simetria")
        # o eixo e a regra da fase: tem que estar desenhado
        if not re.search(r'\.eixov[^{]*\{[^}]*(background|border)', css):
            ruins.append(u"simetria: o EIXO nao esta desenhado. Sem a linha do espelho a crianca "
                         u"nao tem como saber de onde para onde e o reflexo.")
        # o espelho tem que ser CALCULADO
        if not re.search(r'espelh|refle|\blar\s*-\s*1\s*-\s*c\b|\bn\s*-\s*1\s*-\s*', js):
            avisos.append(u"simetria: nao achei o calculo do espelho — se as celulas certas "
                          u"estiverem escritas a mao, um dia a grade muda e a resposta mente.")

    # ---------------------------------------------------- SOMBRA (casar figura)
    if re.search(r'\.sesq\b', css) and re.search(r'\.sdir\b', css):
        usa.append("sombra")
        # sombra e figura preta: nada pode depender de COR
        if not re.search(r'\.fnome\b|\.snome\b|alt\s*=', css + js):
            ruins.append(u"sombra: as figuras nao tem NOME junto. Sombra e forma pura — quem "
                         u"nao reconhece a silhueta fica sem nenhuma outra pista.")
        # as duas portas: casar por toque tambem, nao so arrastando
        if re.search(r'touchmove', js) and not re.search(r'onclick|addEventListener\("click"', js):
            ruins.append(u"sombra: so da para ARRASTAR. No PC da escola a crianca clica; tem que "
                         u"casar tocando tambem (as duas portas de entrada).")

    # ---------------------------------------------------- TABELA DE DUAS ENTRADAS
    if re.search(r'\.lintab\b', css) and re.search(r'\.cabl\b|\.cabc\b', css):
        usa.append("tabela")
        # tabela sem cabecalho nos DOIS lados nao e tabela de duas entradas
        if not (re.search(r'\.cabl\b', css) and re.search(r'\.cabc\b', css)):
            ruins.append(u"tabela: falta cabecalho de linha OU de coluna. A leitura cruzada "
                         u"depende dos dois — com um so, a crianca adivinha.")
        # alvo pequeno: celula de tabela e o alvo mais apertado que existe
        cel = re.search(r'\.cel\{([^}]*)\}', css)
        if cel and re.search(r'(width|height)\s*:\s*(1\d|2\d|3\d)px', cel.group(1)):
            ruins.append(u"tabela: a celula esta abaixo de 40px. Numa grade o dedo ja erra; "
                         u"abaixo disso a crianca acha que foi ela quem errou.")

    # ---------------------------------------------------- TERMOMETRO (medir)
    if re.search(r'\.merc\b', css) and re.search(r'\.tubo\b', css):
        usa.append("termometro")
        # medida sem numero na escala nao se le
        if not re.search(r'\.escala\b|\.grau\b', css):
            ruins.append(u"termometro: nao ha ESCALA com numeros. Coluna que sobe sem regua nao "
                         u"e medida, e animacao.")
        # o valor tambem por escrito: altura de coluna e informacao so visual
        if not re.search(r'&deg;|graus|\bC\b', baixo):
            avisos.append(u"termometro: confira se o valor tambem aparece ESCRITO — a altura da "
                          u"coluna sozinha e informacao so visual.")

    # ------------------------------------------- LETRAS ESCONDIDAS (a letra que falta)
    # Mecanica nova (ago/2026), vinda da pesquisa do EdiLIM (paginas *Ortografia*
    # e *Letras*): a palavra vem com buraco (`CA_PO`) e a crianca leva a letra
    # certa ate ele, com letras A MAIS na bandeja para apertar. Regra da casa:
    # mecanica nova = linha no `_padrao/DINAMICAS.md` E regra AQUI, no mesmo
    # commit — senao o defeito dela nao tem quem pegue na proxima atividade.
    # Gatilho honesto: so esta mecanica publica o BURACO e o LADRILHO de letra.
    if re.search(r'\.leBuraco\b', css) and re.search(r'\.leLetra\b', css):
        usa.append("letras escondidas")
        # ⭐ A ARMADILHA NUMERO UM: a letra que falta escrita A PARTE. Ela tem que
        #    sair da PALAVRA, na posicao do `_` do molde — resposta guardada num
        #    campo proprio e resposta que um dia mente, porque o conteudo muda e
        #    ela fica onde estava.
        # ⚠️ e o teste do mutante mostrou que a MINHA primeira regra era frouxa:
        #    eu procurava so `charAt`, e a peca tem `esc.charAt` na outra metade
        #    da mesma funcao — o mutante que trocava a letra por um campo escrito
        #    a mao passava limpo. O que se cobra e o alinhamento com a PALAVRA.
        if not re.search(r'pal\s*\.\s*charAt', js):
            ruins.append(u"letras escondidas: a letra que falta nao e tirada da PALAVRA na "
                         u"posicao do `_` (molde `esc` + `pal`). Resposta escrita a parte um "
                         u"dia deixa de bater com a palavra — e ninguem vai perceber.")
        # AS DUAS PORTAS: aqui o que falta e uma LETRA, entao digitar e o gesto
        # natural — e no PC da escola tem teclado.
        # ⚠️ nao basta a palavra `document.onkeydown` aparecer: toda peca a escreve
        #    para DESLIGAR o teclado da tela anterior (`document.onkeydown=null`).
        #    O mutante que arrancou o unico teclado da peca passou por causa disso.
        #    Cobra-se o teclado que FUNCIONA: alguem virando funcao.
        if not (re.search(r'onkeydown\s*=\s*function', js)
                or re.search(r'addEventListener\(\s*["\']keydown["\']', js)):
            ruins.append(u"letras escondidas: a fase nao aceita o teclado de verdade "
                         u"(document.onkeydown). O que falta e uma LETRA: digitar e o gesto "
                         u"natural, e no PC da escola a crianca vai digitar.")
        # bandeja embaralhada, senao a crianca aprende a POSICAO da letra
        # ⚠️ `baguncar` vem DECLARADO no motorzinho de toda peca — declarar nao e
        #    usar. E a mesma pedra em que as regras de `colorir` e `ligar pontos`
        #    ja tropecaram, e eu tropecei nela de novo: o mutante sem embaralho
        #    passou porque a DECLARACAO casava.
        # ⚠️ e a folga `embaralh|shuffle` que eu tinha copiado daqui de cima leu
        #    PROSA: o mutante sem embaralho trazia um comentario de linha
        #    ("// sem embaralhar") e o portao se deu por satisfeito. Portao que le
        #    prosa mede prosa — a lição ja esta no topo deste arquivo, e eu a
        #    repeti. Agora so conta CHAMADA de verdade.
        _mist = [m for m in re.finditer(r'\b(?:baguncar|embaralhar?|shuffle)\s*\(', js)
                 if not js[max(0, m.start() - 9):m.start()].rstrip().endswith("function")]
        if not _mist:
            ruins.append(u"letras escondidas: a bandeja nao e EMBARALHADA. A crianca decora a "
                         u"posicao da letra em vez de escutar a palavra.")
        # letra usada sai da bandeja (e sai de verdade: display:none)
        if not re.search(r'_usada|\busada\b', js):
            avisos.append(u"letras escondidas: nao achei a marca de letra JA USADA. Letra que "
                          u"continua clicavel depois de posta prende a crianca (e o auditor).")
        # ⭐ E A ARMADILHA QUE ESTA PECA PAGOU NA BANCADA: se o 2o degrau do
        #    andaime tira TODAS as letras erradas, sobra so a certa — a resposta
        #    fica dada e o 3o degrau nunca acontece (codigo morto). Por isso cada
        #    palavra precisa de pelo menos DUAS letras a mais. E a mesma conta que
        #    a mecanica `escolher` ja faz com os distratores.
        for mm in re.finditer(r'extra\s*:\s*\[(.*?)\]', js, re.S):
            if len(re.findall(r'["\'][^"\']+["\']', mm.group(1))) < 2:
                avisos.append(u"letras escondidas: ha palavra com menos de DUAS letras a mais. "
                              u"O 2o degrau do andaime limpa a bandeja inteira, a resposta fica "
                              u"dada e o 3o degrau vira codigo morto.")
                break

    # ---------------------------------------------------- A REVELACAO QUE SOME
    # ⚠️ DEFEITO DE FAMILIA, achado duas vezes pelo `_qa/errador.js` (ago/2026):
    #    na `linha-do-tempo` e na `ordenar`, o 3o degrau do andaime escreve a
    #    explicacao ("Era este! Eu coloco e voce segue") E poe a peca no lugar.
    #    So que POR a peca passa pelo caminho do acerto, que chama `apagaDica()`
    #    — a frase aparecia e sumia no mesmo pisco. A crianca que mais precisava
    #    da explicacao era a unica que nao conseguia ler a dela.
    #    Aqui e AVISO, nao reprovacao: so o navegador sabe se o revelar TAMBEM
    #    avanca a fase nesta peca. Quem mede de verdade e o errador; isto aqui e
    #    para o autor da proxima peca nao repetir sem perceber.
    if re.search(r'\brevela\s*\(', js) and re.search(r'\bapagaDica\s*\(', js) \
            and not re.search(r'seguraDica', js):
        avisos.append(u"a revelacao (3o degrau do andaime) escreve a explicacao e, se ela "
                      u"tambem AVANCAR a fase, o `apagaDica()` do acerto apaga a frase no "
                      u"mesmo instante. Se for o caso, segure a dica alguns segundos "
                      u"(`seguraDica`, como na linha-do-tempo e na ordenar).")

    return usa, ruins, avisos


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    alvo = sys.argv[1]
    html = io.open(alvo, encoding="utf-8").read()
    js = js_de(html)
    css = css_de(html)
    # ⚠️⚠️ LICAO PAGA (ago/2026), e pela SEGUNDA vez na mesma familia: o gatilho
    #    de "comparar" (`maior que|menor que|&gt;|&lt;`) le o HTML CRU — e o HTML
    #    cru inclui os COMENTARIOS. Eu escrevi num comentario da peca "o teto e
    #    MAIOR QUE o conteudo" e a peca `ouvir-achar`, que nao compara nada,
    #    passou a ser acusada de ser uma dinamica de maior/menor com armadilha
    #    aberta. Portao que le prosa mede prosa.
    #    O `js_de` e o `css_de` ja tiram comentario; o `html` nao tinha quem o
    #    limpasse. Agora tem — e os gatilhos passam a ler so o que a crianca ve
    #    ou o que o codigo faz.
    # ⚠️ SEGUNDA LICAO, no mesmo dia e por minha causa: eu tirei os comentarios
    #    do `html` para os gatilhos pararem de ler prosa — e junto foram embora
    #    as marcas `/* ==== PECA: nome ==== */`, que sao COMENTARIO e sao o que
    #    separa os blocos de cada mecanica na atividade montada. Resultado: o
    #    portao voltou a medir o arquivo inteiro de uma vez e acusou a peca de
    #    PINTAR de tocar som de erro — som que esta noutro bloco, a mil linhas
    #    dali. Limpeza tem escopo: os gatilhos leem o texto limpo; quem corta os
    #    blocos le o texto CRU. Guardo os dois.
    html_cru = html
    html = sem_comentarios(html)
    baixo = html.lower()

    # ⚠️⚠️ LICAO PAGA (ago/2026, Cidade dos Solidos 2o ano): a peca `simulador`
    #    do motor ESQUELETO **nao e generica** — ela e a CHUVA/RIO/PONTE da
    #    atividade de historia onde nasceu ("O RIO E A CHUVA", "Mexa a chuva",
    #    a agua que sobe ate a ponte, MAXC/NIVEL_PONTE fixos). Ela NAO le o
    #    conteudo da fase: por mais que eu escreva `enunciado="Solte os solidos
    #    na rampa"`, a crianca ve o jogo da chuva. Eu montei DUAS fases de
    #    solidos com `mec="simulador"` e o print ficou lindo — o defeito so
    #    aparecia JOGANDO (a banca pegou pelos numeros 3/4/5/7 mudos e pela
    #    balao "Mexa a chuva"). E resto de clone puro: a cena de OUTRA atividade
    #    dentro desta. Enquanto o motor nao tiver um simulador TEMATIZAVEL, o
    #    `mec="simulador"` so pode ser usado quando a fase for mesmo de agua.
    #    Regra que pega sozinho: fase `mec="simulador"` cujo texto (selo +
    #    enunciado) nao fala de agua = a cena da chuva aparecendo fora do lugar.
    m = re.search(r"\nFASES = (\[.*?\]);", html_cru, re.S)
    if m:
        try:
            import json as _json
            _fases = _json.loads(m.group(1))
        except Exception:
            _fases = []
        _agua = re.compile(
            r"chuva|rio|ponte|\bagua\b|\bágua\b|barco|enchente|"
            r"n[ií]vel|molha|inunda|mar\b|onda|represa|barrag", re.I)
        _simul_fora = []
        for f in _fases:
            if (f.get("mec") or "") != "simulador":
                continue
            texto = u"%s %s" % (f.get("selo") or "", f.get("enunciado") or "")
            if not _agua.search(texto):
                _simul_fora.append(f.get("id") or "?")
        if _simul_fora:
            print(u"%s -> %d fase(s) usam o SIMULADOR fora de tema de agua"
                  % (alvo, len(_simul_fora)))
            print(u"   %d ARMADILHA(S) ABERTA(S):" % len(_simul_fora))
            for fid in _simul_fora:
                print(u"    - [simulador] fase %s: a peca simulador do motor e a "
                      u"CHUVA/RIO/PONTE fixa (resto de clone). Fora de tema de "
                      u"agua ela mostra a cena de OUTRA atividade. Troque a "
                      u"mecanica desta fase ou tematize o simulador no motor." % fid)
            return 1

    # ⭐ atividade MONTADA: cada mecanica se mede no bloco DELA
    # ⚠️ a marca de peca e um COMENTARIO, e o `js_de` tira comentarios (de
    #    proposito: e assim que o portao para de acusar o que esta escrito em
    #    nota). Entao a divisao por peca se faz no script CRU, e so depois cada
    #    pedaco passa pelo mesmo limpador.
    cru = "".join(re.findall(r"<script>(.*?)</script>", html_cru, re.S))
    # ⚠️ e a ULTIMA peca nao pode engolir o que vem depois dela (o conteudo que
    #    o montador escreve: FASES, VOZOK, ID). Sem este corte, a peca da SOMBRA
    #    levou acusacao de forca, de labirinto e de ligar pontos — porque a lista
    #    de fases, logo abaixo dela, cita todas as mecanicas da atividade.
    blocos = []
    for n, c in re.findall(
            r"/\* ==== PECA: ([\w-]+) ==== \*/(.*?)(?=/\* ==== PECA: |\Z)",
            cru, re.S):
        corte = c.find("/* ====== O CONTEUDO DESTA ATIVIDADE")
        if corte >= 0:
            c = c[:corte]
        blocos.append((n, re.sub(r"/\*.*?\*/", " ", c, flags=re.S)))
    if blocos:
        cssb = dict(re.findall(
            r"/\* ==== PECA: ([\w-]+) ==== \*/(.*?)(?=/\* ==== PECA: |$)", css, re.S))
        usa, ruins, avisos = [], [], []
        for nome, corpo in blocos:
            u2, r2, a2 = analisa(corpo, cssb.get(nome, ""), corpo.lower(),
                                 corpo + cssb.get(nome, ""))
            for x in u2:
                if x not in usa:
                    usa.append(x)
            ruins.extend(u"[%s] %s" % (nome, x) for x in r2)
            avisos.extend(u"[%s] %s" % (nome, x) for x in a2)
    else:
        usa, ruins, avisos = analisa(js, css, baixo, html)

    print(u"%s -> %d dinamica(s) reconhecida(s): %s"
          % (alvo, len(usa), ", ".join(usa) if usa else "nenhuma"))
    # ⚠️ A CURA GERAL DO "PASSOU SEM SER MEDIDO" (ago/2026). Duas vezes hoje uma
    #    peca saiu com "0 dinamica reconhecida" e foi lida como aprovacao — mas
    #    zero reconhecida quer dizer que ESTE portao nao olhou nada. Aprovacao
    #    vazia da confianca falsa, que e pior do que reprovar. Agora ele avisa,
    #    alto, que a mecanica e nova para ele e precisa de regra.
    if not usa:
        avisos.append(u"NENHUMA mecanica reconhecida — este portao NAO mediu nada "
                      u"neste arquivo. Se ha mecanica aqui, ela e nova para mim: "
                      u"escreva a regra dela (e a linha no _padrao/DINAMICAS.md) "
                      u"no MESMO commit, senao o defeito dela nao tem quem pegue.")
    for a in avisos:
        print(u"   aviso: %s" % a)
    if ruins:
        print(u"   %d ARMADILHA(S) ABERTA(S):" % len(ruins))
        for r in ruins:
            print(u"    - %s" % r)
        return 1
    if usa:
        print(u"   dinamicas ok: as armadilhas conhecidas de cada mecanica estao fechadas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
