# -*- coding: utf-8 -*-
u"""
============================================================
PORTÃO — "a VOZ é da mesma pessoa que o MASCOTE?"

⚠️ LIÇÃO PAGA (ago/2026), e foi o Marcos quem OUVIU, pela segunda vez:
   *"Veja, você botou mascote feminina e voz do Antônio, mude o mascote para
   masculino"*.

A regra já existia — está escrita dentro do `entregar.yml`, com as palavras dele
de uma cobrança ANTERIOR: *"quando for feminino tem que pegar voz feminina"*. E o
conserto daquela vez foi bom: cada atividade passou a escrever a voz dela em
`<pasta>/voz.txt`, e o montador do esqueleto se recusa a gerar sem o campo `voz`
no `conteudo.json`.

**Só que a Oficina da Lina foi escrita À MÃO.** Não passou pelo montador, não tem
`conteudo.json`, e por isso nasceu **sem `voz.txt`** — caindo no padrão do
workflow, que é masculino. A mascote é uma menina pintora, chamada Lina, e a
atividade inteira falava com a voz do Antônio.

Nenhum portão pegava, e o motivo é da pior família: **não havia defeito nenhum a
achar**. O mp3 existe, o texto bate com a tela, a chave da voz confere, o
alto-falante toca. O que não batia era a PESSOA — e isso nenhum portão de texto
ou de pixel enxerga.

O QUE ESTE PORTÃO FAZ: descobre o GÊNERO do mascote pelo jeito como a atividade
fala dele (o artigo antes do nome: "a Lina", "o Broto") e compara com a voz
declarada em `voz.txt`. Se discordarem, reprova. E se a atividade não declarar
voz nenhuma, também reprova — porque "não declarou" quer dizer "vai sair
masculino sem ninguém decidir", que foi exatamente o que aconteceu aqui.

Uso:  python3 _qa/voz_do_mascote.py _lina
Sai 0 se a voz combina, 1 se não combina, 2 se não deu para medir.
============================================================
"""
import io
import json
import os
import re
import sys

# as vozes da casa (as mesmas do montar.py — nunca uma lista paralela)
FEMININAS = (u"francisca", u"thalita", u"brenda", u"leila", u"yara", u"giovanna")
MASCULINAS = (u"antonio", u"donato", u"fabio", u"humberto", u"julio", u"nicolau",
              u"valerio")


def genero_da_voz(v):
    v = (v or u"").lower()
    for f in FEMININAS:
        if f in v:
            return u"feminina"
    for m in MASCULINAS:
        if m in v:
            return u"masculina"
    return None


def nome_do_mascote(html):
    m = re.search(r'var\s+MASCOTE_NOME\s*=\s*"([^"]+)"', html)
    return m.group(1) if m else None


def genero_do_mascote(html, nome):
    u"""
    Descobre o genero pelo ARTIGO que a atividade usa antes do nome.

    ⚠️ Nao se adivinha por terminacao ("Lina" acaba em A, "Nico" em O): tem
    mascote chamado Teo, Orbi, Byte, Zeze. O que nao mente e como a propria
    atividade FALA dele — "a Lina guarda os moldes", "o Broto precisa de agua".
    """
    if not nome:
        return None, []
    provas = []
    fem = len(re.findall(r'\b[Aa]\s+' + re.escape(nome) + r'\b', html))
    masc = len(re.findall(r'\b[Oo]\s+' + re.escape(nome) + r'\b', html))
    # "da Lina" / "do Broto" contam junto
    fem += len(re.findall(r'\b[Dd]a\s+' + re.escape(nome) + r'\b', html))
    masc += len(re.findall(r'\b[Dd]o\s+' + re.escape(nome) + r'\b', html))
    for m in re.finditer(r'.{0,28}\b([AaOo]|[Dd][ao])\s+' + re.escape(nome)
                         + r'\b.{0,20}', html):
        provas.append(re.sub(r"\s+", u" ", m.group(0)).strip())
    if fem > masc:
        return u"feminina", provas[:3]
    if masc > fem:
        return u"masculina", provas[:3]
    return None, provas[:3]


def confere(pasta):
    pasta = pasta.rstrip(u"/")
    cam = os.path.join(pasta, u"index.html")
    if not os.path.exists(cam):
        print(u"%s -> sem index.html. NAO MEDI." % pasta)
        return 2
    html = io.open(cam, encoding=u"utf-8").read()

    nome = nome_do_mascote(html)
    if not nome:
        print(u"%s -> nao achei `MASCOTE_NOME`. NAO MEDI de quem e a voz." % pasta)
        return 2

    camv = os.path.join(pasta, u"voz.txt")
    voz = io.open(camv, encoding=u"utf-8").read().strip() if os.path.exists(camv) else u""

    gm, provas = genero_do_mascote(html, nome)
    gv = genero_da_voz(voz)

    print(u"%s -> mascote '%s'%s | voz declarada: %s"
          % (pasta, nome,
             u" (%s)" % gm if gm else u" (genero nao dito no texto)",
             voz or u"NENHUMA"))
    for p in provas:
        print(u"     texto: ...%s..." % p)

    # ⚠️ NAO DECLARAR NAO E NEUTRO: e sair na voz padrao, que e masculina.
    #    A atividade escrita a mao cai aqui, e foi assim que a Lina falou com a
    #    voz do Antonio a atividade inteira.
    if not voz:
        print(u"   !! A ATIVIDADE NAO DIZ QUAL E A VOZ DELA.")
        print(u"   sem `%s/voz.txt` o gravador usa o padrao MASCULINO, e ninguem" % pasta)
        print(u"   decidiu isso. conserto: escrever uma linha em %s/voz.txt" % pasta)
        print(u"   (`pt-BR-FranciscaNeural` para mascote feminino,")
        print(u"    `pt-BR-AntonioNeural` para masculino) e regravar.")
        return 1

    if gm and gv and gm != gv:
        print(u"   !! A VOZ NAO E DA MESMA PESSOA QUE O MASCOTE.")
        print(u"   o mascote e %s e a voz e %s. A crianca ouve uma pessoa e ve" % (gm, gv))
        print(u"   outra a atividade inteira — e nenhum outro portao pega isso,")
        print(u"   porque o mp3 existe e o texto bate. O que nao bate e QUEM fala.")
        print(u"   conserto: trocar a linha de %s/voz.txt e regravar" % pasta)
        print(u"   (`entregar.yml` com `so_voz=sim`; o carimbo ja inclui a voz).")
        return 1

    if not gm:
        print(u"   voz declarada, mas o texto nunca diz 'a %s' nem 'o %s':" % (nome, nome))
        print(u"   NAO MEDI se combina. (isto nao e 'passou'.)")
        return 2

    print(u"   voz ok: o mascote e %s e quem fala tambem" % gm)
    return 0


if __name__ == u"__main__":
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/voz_do_mascote.py <pasta-da-atividade>")
        sys.exit(2)
    sys.exit(confere(sys.argv[1]))
