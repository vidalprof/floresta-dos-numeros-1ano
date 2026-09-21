# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — "O RECORTE CORTOU O DESENHO?"  (1i7)

 ⭐ DE ONDE ELE NASCEU (19/set/2026). O Marcos abriu o *Jornalista por um Dia* e
    viu, na folha 4: *"na imagem de a irmã deu um presente ao irmão está cortada
    aparecendo parte do irmão. Esse tipo de erro não pode acontecer"*. Ele estava
    certo: a caixa de recorte da figura `choro` terminava em x=484 e o menino ia
    até x=501 — **faltava metade do corpo dele**.

 ⚠️ E NENHUM PORTÃO VIA ISSO, o que é o ponto. O arquivo saía íntegro: o PNG
    abre, não tem halo, não está esticado na tela, o `leiaute_mao` mede a
    proporção e aprova, o jogador automático resolve a folha. **O defeito não
    está no arquivo — está na diferença entre o arquivo e o DESENHO DA FOLHA DE
    PAPEL de onde ele veio.** Só se pega olhando as duas coisas juntas, e é
    exatamente isso que este portão faz.

 COMO MEDE: lê as caixas declaradas no `<pasta>/recortar_das_folhas.py`, abre a
 folha de papel original e olha uma MOLDURA em volta de cada caixa.

 Em cada um dos quatro lados, pergunta se há TINTA DOS DOIS LADOS DA BORDA, na
 mesma altura, num trecho contínuo e largo. Se há, um objeto do desenho está
 sendo partido ao meio ali. Uma moldura impressa ou a pauta da folha também
 atravessa — mas só pela espessura dela, dois ou três pixels; um menino cortado
 atravessa por dezenas. É essa diferença que separa o defeito do inocente.

 ⚠️ PALPITE DECLARADO — e está impresso na saída: a MARGEM de 8 px, a mancha
    mínima de 60 px e a diferença de 16 níveis para a foto são escolhas minhas,
    afinadas nas 10 figuras deste caderno e nas dos outros cadernos de folha
    viva. Não são medida de sala.

 ⚠️ QUANDO O CORTE É DE PROPÓSITO: há caixas que cortam mesmo, e com razão — o
    desenho encosta na moldura impressa, ou a peça é um pedaço escolhido de uma
    cena maior. Declare em `<pasta>/RECORTE-OK.json` — `{"nome": "o motivo"}` —
    como no `HALO-OK.json`. Declarado é IMPRESSO em toda rodada, nunca
    desligado.

 Uso:  python3 _qa/recorte_cortado.py <pasta>
 Código 0 = ok · 1 = REPROVADO · 2 = não deu para medir
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re
import sys

MARGEM = 10         # ⚠️ PALPITE DECLARADO
VAO = 2             # ⚠️ PALPITE DECLARADO — pixels de transicao que nao contam
TRECHO_MIN = 14     # ⚠️ PALPITE DECLARADO — tinta atravessando a borda por
                    #    menos que isto e moldura/pauta, nao desenho
FRACAO_MIN = 0.10   # ⚠️ PALPITE DECLARADO — e por menos de 10%% do lado
PAPEL = 232         # acima disto conta como papel branco


def _folha_real(dir_folhas, nome):
    u"""o arquivo da colheita: ou o nome inteiro, ou o prefixo (`d22`)."""
    if os.path.exists(os.path.join(dir_folhas, nome)):
        return nome
    for a in sorted(os.listdir(dir_folhas)):
        if a.startswith(nome + u"_") or a == nome:
            return a
    return None


def _quatro(no):
    u"""a tupla (x1,y1,x2,y2) de inteiros, ou None."""
    import ast
    if not isinstance(no, (ast.Tuple, ast.List)) or len(no.elts) != 4:
        return None
    fora = []
    for e in no.elts:
        if isinstance(e, ast.Constant) and isinstance(e.value, int):
            fora.append(e.value)
        elif isinstance(e, ast.UnaryOp) and isinstance(e.op, ast.USub) \
                and isinstance(e.operand, ast.Constant) and isinstance(e.operand.value, int):
            fora.append(-e.operand.value)
        else:
            return None
    return tuple(fora)


def _txt(no):
    import ast
    return no.value if isinstance(no, ast.Constant) and isinstance(no.value, str) else None


def le_pecas(pasta, dir_folhas):
    u"""as caixas declaradas no `recortar_das_folhas.py`, em QUALQUER dos formatos
    que a casa usa.

    ⚠⚠ POR QUE POR AST E NAO POR EXPRESSAO REGULAR (19/set/2026). Na primeira
       versao eu li so o formato `PECAS = [(nome, CONST, x1,y1,x2,y2, modo)]`, que
       e o dos quatro cadernos mais novos, e o portao respondeu "NAO SE APLICA"
       em OITO pastas. Isso e exatamente o defeito que eu tinha acabado de
       consertar no `_qa/ligar_rotulo.py`, que ficou meses dizendo "nao medi" por
       causa de uma expressao estreita demais. Portao nasce cego uma vez so.
       Os quatro formatos que existem hoje:
         · `PECAS  = [(nome, CONST, x1,y1,x2,y2 [, modo])]`     (_not2, _narra2…)
         · `CORTES = [(pasta, "d22", {nome: (x1,y1,x2,y2)})]`   (_casa1)
         · `D37 = {"arquivo": "d37_x.jpg", "caixas": [(nome,(x1,y1,x2,y2))]}` (_sinon2…)
         · `CAIXAS_POR_FOLHA = [...]`                            (_reinos)
       O AST entende a SINTAXE, entao ele acha as caixas em todos: procura
       qualquer nome de arquivo de imagem e liga a ele as quadras de inteiros
       que aparecem ao lado, com o nome da peca."""
    import ast
    cam = os.path.join(pasta, u"recortar_das_folhas.py")
    if not os.path.exists(cam):
        return None, u"a pasta nao tem recortar_das_folhas.py"
    txt = io.open(cam, encoding=u"utf-8").read()
    try:
        arv = ast.parse(txt)
    except SyntaxError as e:
        return None, u"o recortar_das_folhas.py nao compila (%s)" % e

    # ⚠️ AS CONSTANTES DE PASTA (5o formato, o do `_corpo5`): nele cada recorte
    #    diz de QUAL COLHEITA vem, porque o caderno colheu em duas pastas
    #    (`folhas_corpo5` e `folhas_corpo5circ`). A linha e
    #    `FOLHAS = os.path.join(BASE, "_sequencias", "folhas_corpo5")`.
    pastas = {}
    for no in ast.walk(arv):
        if isinstance(no, ast.Assign) and len(no.targets) == 1 \
                and isinstance(no.targets[0], ast.Name) \
                and isinstance(no.value, ast.Call):
            partes = [_txt(a) for a in no.value.args]
            seq = [x for x in partes if x]
            if len(seq) >= 2 and seq[-2] == u"_sequencias":
                cam = os.path.join(u"_sequencias", seq[-1])
                if os.path.isdir(cam):
                    pastas[no.targets[0].id] = cam

    # 1) as constantes que guardam nome de folha: D31 = "d31_bb11a2.png"
    const = {}
    for no in ast.walk(arv):
        if isinstance(no, ast.Assign) and len(no.targets) == 1 \
                and isinstance(no.targets[0], ast.Name):
            v = _txt(no.value)
            if v and re.search(r"\.(png|jpe?g)$", v, re.I):
                const[no.targets[0].id] = v

    # ⚠️⚠️ A ORDEM DOS QUATRO NUMEROS NAO SE ADIVINHA — ELA SE LE (19/set/2026).
    #    O `_sinon2` declara as caixas em (y1, x1, y2, x2), e nao em
    #    (x1, y1, x2, y2) como os outros. Lendo na ordem errada, o portao mediu o
    #    CABECALHO da folha no lugar das sopas e acusou DOZE figuras que estavam
    #    inteiras. Portao que mede o lugar errado e pior que portao que nao mede:
    #    o primeiro manda consertar o que esta certo. Quem diz a ordem e o proprio
    #    script, no desempacotamento (`for nome, (y1, x1, y2, x2) in ...`).
    yx = bool(re.search(r"for\s+\w+\s*,\s*\(\s*y1\s*,\s*x1\s*,\s*y2\s*,\s*x2\s*\)", txt))

    achadas = []

    def guarda(folha, nome, cx, modo=u"figura", pasta_folha=None):
        if cx and yx:
            cx = (cx[1], cx[0], cx[3], cx[2])
        if folha and nome and cx and cx[2] > cx[0] and cx[3] > cx[1]:
            achadas.append((nome, os.path.join(pasta_folha, folha) if pasta_folha
                            else folha, cx[0], cx[1], cx[2], cx[3], modo))

    # ⭐ 1b) O CAMINHO CURTO: `<pasta>/img/RECORTE.json` (21/set/2026).
    #    Ate aqui este portao so sabia LER PYTHON: ele analisa a arvore do
    #    `recortar_das_folhas.py` de cada caderno procurando os formatos de
    #    caixa que ja viu. Funciona, e ja aprendeu cinco formatos — mas toda vez
    #    que um caderno escreve as caixas de um jeito novo ele fica CEGO, e a
    #    cegueira dele custou duas figuras partidas ao meio no `_corpo5`.
    #    O `_dinheiro5` escreve as caixas tambem em JSON, ao recortar:
    #        {"dn5_arroz.png": {"folha": "folhas_dinheiro5c/d01_...jpg",
    #                           "caixa": [x0, y0, x1, y1]}}
    #    Isso e o que o script REALMENTE cortou, nao o que eu deduzi do codigo
    #    dele — e vale para qualquer formato de caixa que venha depois, inclusive
    #    o corte CIRCULAR da moeda, que nao e caixa nenhuma e por isso fica de
    #    fora (quem tem "circulo" em vez de "caixa" nao entra aqui).
    cam_rec = os.path.join(pasta, u"img", u"RECORTE.json")
    if os.path.exists(cam_rec):
        try:
            import json as _json
            rec = _json.load(io.open(cam_rec, encoding=u"utf-8"))
        except Exception as e:                                  # noqa: BLE001
            print(u"%s -> NAO MEDI: %s nao e JSON valido (%s)." % (pasta, cam_rec, e))
            return None, u"RECORTE.json ilegivel"
        for nome_png, d in sorted(rec.items()):
            if not isinstance(d, dict):
                continue
            cx = d.get(u"caixa")
            folha = d.get(u"folha")
            if not folha or not isinstance(cx, list) or len(cx) != 4:
                continue
            nome = re.sub(r"\.png$", u"", nome_png)
            achadas.append((nome, os.path.join(u"_sequencias", folha),
                            cx[0], cx[1], cx[2], cx[3], u"figura"))

    # 2) varre toda tupla/lista procurando os tres formatos
    for no in ast.walk(arv):
        if not isinstance(no, (ast.Tuple, ast.List)):
            continue
        el = no.elts
        # (nome, CONST, x1, y1, x2, y2 [, modo])
        if len(el) in (6, 7) and _txt(el[0]) and isinstance(el[1], ast.Name) \
                and el[1].id in const:
            cx = _quatro(ast.Tuple(elts=list(el[2:6]), ctx=ast.Load()))
            guarda(const[el[1].id], _txt(el[0]), cx, _txt(el[6]) if len(el) == 7 else u"figura")
            continue
        # ⚠️ 5o FORMATO — (PASTA, "d29", nome, (x1,y1,x2,y2), u"o que e"), do
        #    `_corpo5`. Sem ele o portao dizia "nao achei caixa nenhuma (formato
        #    novo? avise, para o portao aprender)" — e avisar e isto aqui. E o
        #    silencio dele custou caro nesse caderno: DUAS figuras foram ao
        #    recorte partidas ao meio (o coracao sem a veia cava e sem a ponta,
        #    o menino do respiratorio com meia cabeca) e quem as achou fui eu,
        #    olhando. E exatamente o defeito que este portao existe para pegar.
        if len(el) == 5 and isinstance(el[0], ast.Name) and el[0].id in pastas \
                and _txt(el[1]) and _txt(el[2]) and isinstance(el[3], (ast.Tuple, ast.List)):
            dd = pastas[el[0].id]
            folha = _folha_real(dd, _txt(el[1]))
            guarda(folha, _txt(el[2]), _quatro(el[3]), pasta_folha=dd)
            continue
        # (nome, (x1,y1,x2,y2))  — precisa do "arquivo" do dict que a contem
        # (pasta, "d22", {nome: caixa})
        if len(el) == 3 and _txt(el[1]) and isinstance(el[2], ast.Dict):
            # a pasta da colheita pode vir no 1o campo (_casa1: "folhas_moradia")
            dd = dir_folhas
            p0 = _txt(el[0])
            if p0 and p0.startswith(u"folhas_"):
                alt = os.path.join(u"_sequencias", p0)
                if os.path.isdir(alt):
                    dd = alt
            folha = _folha_real(dd, _txt(el[1]))
            for k, v in zip(el[2].keys, el[2].values):
                guarda(folha, _txt(k), _quatro(v), pasta_folha=dd)

    # 3) dicts com "arquivo" + "caixas"
    for no in ast.walk(arv):
        if not isinstance(no, ast.Dict):
            continue
        ch = dict((_txt(k), v) for k, v in zip(no.keys, no.values) if _txt(k))
        arq = _txt(ch.get(u"arquivo")) if u"arquivo" in ch else None
        cxs = ch.get(u"caixas")
        if not arq or not isinstance(cxs, (ast.List, ast.Tuple)):
            continue
        folha = _folha_real(dir_folhas, arq)
        for it in cxs.elts:
            if isinstance(it, (ast.Tuple, ast.List)) and len(it.elts) >= 2:
                guarda(folha, _txt(it.elts[0]), _quatro(it.elts[1]))

    # 4) o formato de GRADE: {"arquivo", "area", "linhas", "colunas", "nomes"}
    #    (_subst5, _reinos, _ort5, _ing8, _mult3). Aqui as caixas nao estao
    #    escritas: sao CALCULADAS a partir da area e das faixas. O portao faz a
    #    mesma conta, senao ficaria cego em cinco cadernos — e portao cego foi
    #    exatamente o defeito que acabei de consertar no `ligar_rotulo.py`.
    for no in ast.walk(arv):
        if not isinstance(no, ast.Dict):
            continue
        ch = dict((_txt(k), v) for k, v in zip(no.keys, no.values) if _txt(k))
        if not (u"arquivo" in ch and u"area" in ch and u"nomes" in ch):
            continue
        arq = _txt(ch[u"arquivo"])
        area = _quatro(ch[u"area"])
        folha = _folha_real(dir_folhas, arq) if arq else None
        if not folha or not area:
            continue
        def faixas(no2):
            fora = []
            if isinstance(no2, (ast.List, ast.Tuple)):
                for e in no2.elts:
                    if isinstance(e, (ast.Tuple, ast.List)) and len(e.elts) == 2:
                        v = [_txt(x) for x in e.elts]
                        ii = []
                        for x in e.elts:
                            if isinstance(x, ast.Constant) and isinstance(x.value, int):
                                ii.append(x.value)
                        if len(ii) == 2:
                            fora.append(tuple(ii))
            return fora
        lins = faixas(ch.get(u"linhas"))
        cols = faixas(ch.get(u"colunas"))
        nomes = ch.get(u"nomes")
        if not (lins and cols and isinstance(nomes, (ast.List, ast.Tuple))):
            continue
        for i, linha in enumerate(nomes.elts):
            if not isinstance(linha, (ast.List, ast.Tuple)) or i >= len(lins):
                continue
            for j, cel in enumerate(linha.elts):
                nome = _txt(cel)
                if not nome or j >= len(cols):
                    continue
                guarda(folha, nome, (area[0] + cols[j][0], area[1] + lins[i][0],
                                     area[0] + cols[j][1], area[1] + lins[i][1]))

    if not achadas:
        return None, u"nao achei caixa nenhuma (formato novo? avise, para o portao aprender)"
    # tira repetidas
    visto, fora = set(), []
    for p in achadas:
        if p[:6] in visto:
            continue
        visto.add(p[:6]); fora.append(p)
    return fora, None


def olha(folha, x1, y1, x2, y2, modo, recorte):
    u"""devolve (cortou?, por que) para uma caixa.

    ⚠⚠ A MEDIDA É O ATRAVESSAMENTO, e cheguei nela depois de DUAS tentativas
       que acusavam inocente — o que é pior que não medir, porque portao que
       grita em tudo a gente aprende a ignorar (licao ja paga no
       `silaba_fonte.py`, que reprovou 21 recortes legitimos).

       O que NAO funcionou, e por que (fica escrito para ninguem refazer):
         1. juntar a tinta em MANCHAS CONEXAS e ver se alguma sai da caixa:
            acusou 7 das 10 pecas, porque a moldura impressa do quadro de jornal
            e a linha da tabela sao tinta, ficam coladas no desenho e saem;
         2. passar a caixa MAIOR pelo pipeline do recorte e comparar o contorno:
            acusou 8 das 10, pelo mesmo motivo — na caixa ampliada a moldura
            deixa de ser "pequena e encostada na borda" e o `tira_linha_impressa`
            nao a alcanca mais.

       O SINAL EXATO do defeito que o Marcos viu é outro, e é estreito: **um
       objeto do desenho atravessa a borda**. Ou seja, ha tinta dos DOIS lados da
       borda, na mesma altura, num trecho LARGO e CONTINUO. Uma moldura ou uma
       pauta tambem atravessa — mas por 2 ou 3 pixels, que e a espessura dela.
       Um menino cortado ao meio atravessa por dezenas. E essa diferenca que o
       portao mede, e so ela."""
    import numpy as np
    W, H = folha.size
    mx1, my1 = max(0, x1 - MARGEM), max(0, y1 - MARGEM)
    mx2, my2 = min(W, x2 + MARGEM), min(H, y2 + MARGEM)
    encosta = (x1 - MARGEM < 0, y1 - MARGEM < 0, x2 + MARGEM > W, y2 + MARGEM > H)
    ox, oy = x1 - mx1, y1 - my1
    fx, fy = ox + (x2 - x1), oy + (y2 - y1)
    a = np.asarray(folha.crop((mx1, my1, mx2, my2)).convert(u"RGB"))
    tinta = (a.min(axis=2) < PAPEL)
    # ⚠️⚠️ NAO BASTA HAVER TINTA DOS DOIS LADOS: ela tem de ser A MESMA MANCHA.
    #    Terceira licao do mesmo portao (19/set/2026), e a mais util. Em folha
    #    com as figuras em GRADE — as oito do `_sinon2`, as moradias do `_casa1` —
    #    a caixa de uma peca quase encosta na vizinha, e a tinta que aparece do
    #    outro lado da borda e o DESENHO DO VIZINHO, nao a continuacao do meu.
    #    Doze figuras do `_sinon2` foram acusadas assim, e as doze estavam
    #    inteiras (conferi olhando o contato). Quando o desenho e MEU e continua,
    #    a tinta atravessa LIGADA: mesma mancha conexa dos dois lados. Quando e o
    #    vizinho, ha papel entre nos e as manchas sao outras.
    from scipy import ndimage as nd
    rot, _ = nd.label(nd.binary_dilation(tinta, np.ones((3, 3), bool)))
    rot = rot * tinta

    def maior_trecho(v):
        u"""o mais longo pedaco CONTINUO de True."""
        melhor = atual = 0
        for x in v:
            atual = atual + 1 if x else 0
            melhor = max(melhor, atual)
        return melhor

    # ⚠️ O VÃO DE 2 PIXELS, E ELE FOI LIÇÃO DA PRÓPRIA PROVA (19/set/2026): a
    #    foto do cachorro estava CERTA e o portao a acusou, porque a caixa
    #    terminava em y=438 e a foto tinha UMA linha de transicao (quase branca,
    #    mas ainda escura pelo limiar) em y=439. Tinta colada na borda e
    #    antialiasing do escaneamento, nao desenho que continua. Entao a faixa de
    #    fora comeca DEPOIS do vao: o que segue por 3 a 6 pixels e desenho.
    V, E = VAO, VAO + 4
    def ligadas(dentro, fora, eixo):
        u"""por posicao: ha tinta dos dois lados E ela e a MESMA mancha?"""
        saida = np.zeros(dentro.shape[1 - eixo] if dentro.ndim == 2 else 0, bool)
        n = dentro.shape[1] if eixo == 0 else dentro.shape[0]
        saida = np.zeros(n, bool)
        for i in range(n):
            d = dentro[:, i] if eixo == 0 else dentro[i, :]
            f = fora[:, i] if eixo == 0 else fora[i, :]
            dd = set(int(v) for v in d if v)
            if dd and dd & set(int(v) for v in f if v):
                saida[i] = True
        return saida

    lados = []
    if not encosta[0] and ox >= E:
        lados.append((u"a esquerda", ligadas(rot[oy:fy, ox:ox + 2].T,
                                             rot[oy:fy, ox - E:ox - V].T, 0)))
    if not encosta[2] and tinta.shape[1] - fx >= E:
        lados.append((u"a direita", ligadas(rot[oy:fy, fx - 2:fx].T,
                                            rot[oy:fy, fx + V:fx + E].T, 0)))
    if not encosta[1] and oy >= E:
        lados.append((u"em cima", ligadas(rot[oy:oy + 2, ox:fx],
                                          rot[oy - E:oy - V, ox:fx], 0)))
    if not encosta[3] and tinta.shape[0] - fy >= E:
        lados.append((u"embaixo", ligadas(rot[fy - 2:fy, ox:fx],
                                          rot[fy + V:fy + E, ox:fx], 0)))

    pior = None
    for nome, atravessa in lados:
        if atravessa.size == 0:
            continue
        trecho = maior_trecho(atravessa)
        frac = float(atravessa.sum()) / float(len(atravessa))
        if trecho >= TRECHO_MIN and frac >= FRACAO_MIN:
            if pior is None or trecho > pior[1]:
                pior = (nome, trecho, frac)
    if pior:
        return True, (u"o desenho atravessa a borda %s num trecho continuo de %d "
                      u"pixel(s) (%d%% do lado): ha figura dos dois lados do corte"
                      % (pior[0], pior[1], round(pior[2] * 100)))
    return False, None


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/recorte_cortado.py <pasta>")
        return 2
    pasta = sys.argv[1].rstrip(u"/")
    try:
        from PIL import Image
        import numpy  # noqa: F401
        sys.path.insert(0, u"_padrao")
        from recorte_folha import limpa_fundo, tira_halo, tira_linha_impressa
        recorte = {u"limpa_fundo": limpa_fundo, u"tira_halo": tira_halo,
                   u"tira_linha_impressa": tira_linha_impressa}
    except ImportError as e:
        print(u"%s -> NAO MEDI: falta biblioteca (%s)." % (pasta, e))
        return 2
    # de onde saem as folhas de papel
    if not os.path.exists(os.path.join(pasta, u"recortar_das_folhas.py")):
        print(u"%s -> NAO SE APLICA: a pasta nao tem recortar_das_folhas.py." % pasta)
        return 2
    txt = io.open(os.path.join(pasta, u"recortar_das_folhas.py"), encoding=u"utf-8").read()
    m = re.search(r'FOLHAS\s*=\s*os\.path\.join\(RAIZ,\s*u?"([^"]+)",\s*u?"([^"]+)"\)', txt)
    if not m:
        # a pasta pode vir em cada item (_casa1) — o `_sequencias` serve de raiz
        dir_folhas = u"_sequencias"
    else:
        dir_folhas = os.path.join(m.group(1), m.group(2))
    if not os.path.isdir(dir_folhas):
        dir_folhas = u"_sequencias"          # o item diz a pasta dele (_casa1)
    pecas, erro = le_pecas(pasta, dir_folhas)
    if pecas is None:
        print(u"%s -> NAO SE APLICA: %s." % (pasta, erro))
        return 2

    liberados = {}
    cam_ok = os.path.join(pasta, u"RECORTE-OK.json")
    if os.path.exists(cam_ok):
        try:
            liberados = json.load(io.open(cam_ok, encoding=u"utf-8"))
        except Exception as e:
            print(u"%s -> NAO MEDI: %s nao e JSON valido (%s)." % (pasta, cam_ok, e))
            return 2

    abertas, erros, olhados, naomedi, medidos = {}, [], [], [], 0
    for nome, arq, x1, y1, x2, y2, modo in pecas:
        cam = arq if os.path.sep in arq else os.path.join(dir_folhas, arq)
        if not os.path.exists(cam):
            continue
        if arq not in abertas:
            abertas[arq] = Image.open(cam)
        # ⚠️ PORTAO QUE ESTOURA NAO E "REPROVOU": E PORTAO QUEBRADO, e o pior
        #    tipo, porque acusa a atividade de um defeito que e dele. A casa ja
        #    pagou essa licao no `resposta_impressa.py` (int.upper()). Aqui o
        #    estouro veio de uma quadra que o AST leu como caixa sem ser
        #    (x2 < x1): peca que nao da para medir sai da conta e e IMPRESSA.
        if x2 <= x1 or y2 <= y1:
            naomedi.append((nome, u"a caixa lida nao e um retangulo (%d,%d,%d,%d)"
                            % (x1, y1, x2, y2)))
            continue
        medidos += 1
        try:
            cortou, porque = olha(abertas[arq], x1, y1, x2, y2, modo, recorte)
        except Exception as e:
            medidos -= 1
            naomedi.append((nome, u"%s" % e))
            continue
        if not cortou:
            continue
        if nome in liberados:
            olhados.append((nome, porque, liberados[nome]))
        else:
            erros.append((nome, arq, modo, porque))

    print(u"%s -> recorte: %d caixa(s) conferida(s) contra a folha de papel"
          % (pasta, medidos))
    print(u"   PALPITE DECLARADO (nunca medido com crianca): margem %d px, vao de %d px "
          u"que nao conta, trecho minimo de %d px atravessando e %d%% do lado."
          % (MARGEM, VAO, TRECHO_MIN, round(FRACAO_MIN * 100)))
    if naomedi:
        print(u"   %d caixa(s) que NAO DEU PARA MEDIR (isso nao e 'passou'):" % len(naomedi))
        for nome, por in naomedi[:8]:
            print(u"    ? %-12s %s" % (nome, por))
    if olhados:
        print(u"   %d recorte(s) que cortam DE PROPOSITO, declarados em RECORTE-OK.json:"
              % len(olhados))
        for nome, porque, por in olhados:
            print(u"    - %-12s %s  (%s)" % (nome, porque, por))
    if erros:
        print(u"   %d FIGURA(S) CORTADA(S) — a crianca ve metade do desenho:" % len(erros))
        for nome, arq, modo, porque in erros[:12]:
            print(u"    x %-12s (%s, %s): %s" % (nome, arq[:3], modo, porque))
        print(u"   conserto: abrir a folha de papel, medir onde a tinta do desenho")
        print(u"   realmente acaba e alargar a caixa em `recortar_das_folhas.py`.")
        print(u"   Se o corte for de proposito, declare em %s com o motivo." % cam_ok)
        return 1
    print(u"   ok: nenhum desenho continua para fora da sua caixa.")
    return 0


if __name__ == u"__main__":
    sys.exit(main())
