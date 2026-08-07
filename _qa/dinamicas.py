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


def js_de(html):
    js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    return re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), js, flags=re.S)


def css_de(html):
    return "".join(re.findall(r"<style>(.*?)</style>", html, re.S))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    alvo = sys.argv[1]
    html = io.open(alvo, encoding="utf-8").read()
    js = js_de(html)
    css = css_de(html)
    baixo = html.lower()

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

    # ---------------------------------------------------- ARRASTAR
    if re.search(r'touchstart', js):
        usa.append("arrastar/toque")
        # preventDefault dentro do touchstart mata o toque
        for m in re.finditer(r'touchstart["\']?\s*,\s*function\s*\([^)]*\)\s*\{(.{0,300})', js, re.S):
            if "preventDefault" in m.group(1):
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
        if re.search(r'vida|game ?over|morreu|perdeu', js, re.I):
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
    if re.search(r'ligar.?pontos|\.pt\b', css) and re.search(r'proximo|ordem', js, re.I):
        usa.append("ligar pontos")
        if re.search(r'sErro\(', js):
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
