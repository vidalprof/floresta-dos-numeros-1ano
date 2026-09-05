# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — "a figura combina com a palavra?"

 ⚠️ LIÇÃO PAGA (ago/2026), e foi o Marcos quem viu, olhando a tela:
 *"tem figuras que é por exemplo um abacate, está escrito ovo e o som está
 ovo, tudo tem que corresponder"*.

 Ele estava certo, e o defeito estava escrito com todas as letras no conteúdo:

     "pd_ovo": {"nome": "OVO", "voz": "ovo", "img": "pd_mamao"}

 A palavra dizia OVO, a voz dizia "ovo", e o desenho era um MAMÃO — porque a
 figura do ovo nunca tinha sido gerada e alguém apontou para a que existia.

 Por que NENHUM portão pegou: o `imagens.js` confere se a figura CARREGA (e o
 mamão carrega lindamente); o `arte_propria.py` confere se ela foi copiada de
 outra atividade (não foi); o `encaixe.js` confere se ela cabe na caixa (cabe).
 Nenhum deles pergunta se ela é a figura DAQUELA palavra — e essa é justamente
 a pergunta da criança que ainda não lê: ela escolhe pelo desenho.

 O QUE ESTE PORTÃO FAZ: em todo lugar do conteúdo onde uma palavra e uma figura
 andam juntas (`nome`/`img`, `t`/`img`, `pal`/`img`), confere se o nome do
 arquivo tem alguma coisa a ver com a palavra. `OVO` -> `pd_ovo` passa;
 `OVO` -> `pd_mamao` reprova.

 ⚠️ Ele NÃO olha o desenho: se a arte do `pd_ovo.png` sair um abacate, quem
 pega é o olho do professor. Este portão pega o descuido de APONTAR para a
 figura errada, que é o que aconteceu — e é o mais comum, porque acontece
 quando a figura certa ainda não existe.

 Uso: python3 _qa/figura_certa.py <pasta-da-atividade>
============================================================
"""
import io
import json
import os
import re
import sys
import unicodedata


def achata(s):
    u"""tira acento, caixa e o que não é letra: "PÃO" -> "pao"."""
    s = unicodedata.normalize("NFD", s or u"")
    s = u"".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "", s.lower())


# palavras que nao dizem NADA sobre o desenho: artigo, preposicao, ligacao.
# Sem tirar isto, "THE BOY" e "BOY EATING" nao teriam palavra em comum.
VAZIAS = set(u"""a o as os um uma the of in on at to and e de da do das dos
                 um uma no na nos nas com por para this that these those""".split())


def palavras(s):
    u"""as palavras que CARREGAM sentido, achatadas: "THE BOY" -> {"boy"}."""
    bruto = re.split(r"[^A-Za-z0-9\u00c0-\u017f]+", s or u"")
    return set(x for x in (achata(p) for p in bruto) if x and x not in VAZIAS)


def numeros(s):
    u"""os NUMEROS inteiros da string, como inteiros (nao pedaco de texto):
    "2 REAIS" -> {2}, "nota20" -> {20}. \u26a0\ufe0f LICAO PAGA (Lojinha, ago/2026): a
    figura do dinheiro e "lb_nota2"/"lb_moeda1", e a palavra e "2 REAIS"/"1
    REAL". A comparacao por LETRA nunca casa (nota2 x 2reais), mas o VALOR e o
    mesmo \u2014 e e o valor que a crianca le na cedula. Quando a palavra e a figura
    dividem o mesmo numero, a figura E daquela palavra. So faz PASSAR mais (nunca
    reprova ninguem novo), e o "20" vira 20 (inteiro), entao "nota2" e "nota20"
    nao se confundem."""
    return set(int(n) for n in re.findall(r"\d+", s or u""))


# uma resposta que e LUGAR comeca por preposicao de lugar: o desenho mostra a
# cena, e o nome do arquivo fala da acao que acontece nela.
LUGAR = (u"at ", u"in ", u"on ", u"under ", u"behind ", u"near ", u"next ",
         u"no ", u"na ", u"em ", u"sob ", u"atras ", u"perto ")


def so_lugar(s):
    t = (s or u"").strip().lower()
    return any(t.startswith(p) for p in LUGAR)


# as duplas (palavra, figura) que o conteúdo usa. A chave da palavra vem
# primeiro; a da figura, depois.
DUPLAS = [("nome", "img"), ("t", "img"), ("pal", "img"), ("n", "img"),
          ("txt", "img"), ("rot", "img")]


def pares(o, achados):
    if isinstance(o, dict):
        # ⚠️ LICAO PAGA (Museu, 3o ano, ago/2026): GAVETA DE CATEGORIA COM EXEMPLAR.
        #    Quando `rot` e verdadeiro (classificar em grupos), o `n` e o NOME DE UM
        #    GRUPO ("MAMIFERO", "VERTEBRADO") e a `img` e um EXEMPLAR dele
        #    (mv_cachorro) — de proposito: o cachorro REPRESENTA a categoria, nao e
        #    a legenda da palavra. Nao e o defeito "ovo escrito, mamao desenhado".
        #    A crianca le/ouve o grupo e a figura fraca so ilustra. Entao a dupla
        #    n->img nao entra na regra do nome (senao reprova conteudo correto).
        pula_n = bool(o.get("rot"))
        for kp, ki in DUPLAS:
            if kp == "n" and pula_n:
                continue
            palavra = o.get(kp)
            figura = o.get(ki)
            if isinstance(palavra, str) and isinstance(figura, str) and figura:
                achados.append((palavra, figura))
        for v in o.values():
            pares(v, achados)
    elif isinstance(o, list):
        for v in o:
            pares(v, achados)


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/figura_certa.py <pasta-da-atividade>")
        return 2
    pasta = sys.argv[1].rstrip("/")
    cam = os.path.join(pasta, "conteudo.json")
    if not os.path.exists(cam):
        print(u"%s -> sem conteudo.json (atividade escrita a mao?): "
              u"NAO MEDI se a figura combina com a palavra." % pasta)
        return 2

    d = json.load(io.open(cam, encoding="utf-8"))
    achados = []
    pares(d, achados)
    if not achados:
        print(u"%s -> NAO SE APLICA: nenhuma dupla palavra+figura no conteudo. Nada a conferir." % pasta)
        return 2

    prefixo = (d.get("prefixo") or u"") + u"_"
    ruins, ok, sem_como_medir = [], 0, []
    for palavra, figura in achados:
        # a figura vem como "pd_ovo": tira o prefixo da atividade
        nome_arq = figura[len(prefixo):] if figura.startswith(prefixo) else figura
        a, b = achata(palavra), achata(nome_arq)
        if not a or not b:
            continue
        # ⚠️ LICAO PAGA (ago/2026, no 9o ano): a regra era "um contem o outro",
        #    e ela so serve para palavra de UMA palavra. "THE BOY" x
        #    "rn_boy_eating" e a figura CERTA — o menino comendo — e mesmo
        #    assim reprovava, porque "theboy" nao esta dentro de "boyeating".
        #    Onze acusacoes, todas em conteudo correto. Comparar por PALAVRA
        #    mantem o dente onde importa: "ovo" x "mamao" continua reprovando,
        #    porque nao ha palavra em comum.
        # ⚠️ LICAO PAGA (Lojinha, ago/2026): a gaveta de CATEGORIA "MOEDA" /
        #    "NOTA" tem por figura um exemplar (`lb_moeda1`, `lb_nota5`) — a
        #    moeda de 1 real REPRESENTA a categoria "moeda". O digito final do
        #    nome do arquivo (moeda1, nota5) impedia o casamento por palavra
        #    ("moeda" != "moeda1"). Comparo tambem com o digito final removido:
        #    "moeda1"->"moeda", "nota5"->"nota". So faz PASSAR mais (nunca
        #    reprova ninguem novo): "ovo" x "mamao" continua sem palavra comum.
        raiz_arq = set(re.sub(r"\d+$", u"", t) for t in palavras(nome_arq))
        if (a in b or b in a or (palavras(palavra) & palavras(nome_arq))
                or (palavras(palavra) & raiz_arq)
                or (numeros(palavra) & numeros(nome_arq))):
            ok += 1
        elif so_lugar(palavra):
            # ⚠️ E O QUE ELE NAO TEM COMO MEDIR: quando a resposta e um LUGAR
            #    ("AT THE BENCH"), a figura mostra a cena inteira e o nome dela
            #    fala da acao ("read_news"), nao do banco. Nao da para decidir
            #    pelo nome do arquivo — e "nao medi" nunca pode virar "reprovado"
            #    (regra da casa). Vai para a lista do olho do professor.
            sem_como_medir.append((palavra, figura))
        else:
            ruins.append((palavra, figura))

    print(u"%s -> %d dupla(s) palavra+figura conferida(s)"
          % (pasta, ok + len(ruins) + len(sem_como_medir)))
    if sem_como_medir:
        print(u"   %d dupla(s) que ESTE portao nao sabe medir (a resposta e um "
              u"lugar; o nome do arquivo fala da acao) — olho do professor:"
              % len(sem_como_medir))
        for palavra, figura in sem_como_medir[:8]:
            print(u'    . "%s" aponta para "%s"' % (palavra, figura))
    if not ruins:
        print(u"   figura ok: o desenho de cada palavra tem o nome dela")
        return 0

    print(u"   %d FIGURA(S) QUE NAO COMBINAM COM A PALAVRA — a crianca que "
          u"ainda nao le escolhe pelo desenho:" % len(ruins))
    vistos = set()
    for palavra, figura in ruins:
        if (palavra, figura) in vistos:
            continue
        vistos.add((palavra, figura))
        print(u'    - a palavra e "%s" e o desenho e "%s"' % (palavra, figura))
    print(u"   conserto: gerar a figura DAQUELA palavra (gerar-imagens.yml) e "
          u"apontar o `img` para ela. Apontar para a figura que ja existe e "
          u"como legendar a foto errada.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
