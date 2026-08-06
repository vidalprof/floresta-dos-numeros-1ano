#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO DA VOZ QUE NÃO EXISTE — "o mp3 dessa fala foi gravado?"

Defeito que o Marcos pegou (ago/2026): *"na cruzadinha do 3º ano os áudios e o
botão 'ouvir de novo' não funcionam"*. Ele estava certo, e a causa era simples e
invisível: o código chamava `falaDaTela("mp_cruz_q"+idx)` e os arquivos
`mp_cruz_q0.mp3`, `q1` e `q2` **nunca foram gerados**. O texto estava escrito no
`falas.json`; a voz é que não veio.

Por que ninguém viu: `narr.src` de um arquivo que não existe dá 404, dispara
`error`, o motor chama `fimFala()` e **segue em frente sem reclamar**. A tela
funciona, a fase anda, o `node --check` passa, o print fica perfeito. O único
sintoma é o silêncio — e silêncio não aparece em print nenhum. Para a criança
que não lê, a fase inteira fica sem instrução.

REGRA: todo id de narração que o código usa E que tem texto no `falas.json`
precisa do `<pasta>/audio/<id>.mp3`.

⚠️ Ids MONTADOS (`"x_q"+idx`) são expandidos de 0 a 9, e por isso muitos não
existem de propósito (a lista da fase tem 3 itens, não 10). Por isso a regra só
cobra o que **tem texto escrito** no `falas.json`: texto escrito é promessa de
voz. Sem esse filtro o portão gritaria em cima de tudo — e portão que grita à
toa é portão que ninguém lê.

Uso:  python3 _qa/vozfalta.py _mapa/index.html
Sai com 1 se faltar mp3.
"""
import io
import json
import os
import re
import sys

USOS = re.compile(r'(?:falar|falaDaTela|depoisDaFala|introEPergunta|montaBarra)\("([a-z0-9_]+)"')
MONTADOS = re.compile(r'(?:falar|falaDaTela)\("([a-z0-9_]+_q)"\s*\+')


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    alvo = sys.argv[1]
    pasta = os.path.dirname(os.path.abspath(alvo))
    html = io.open(alvo, encoding="utf-8").read()
    js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    js = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), js, flags=re.S)

    ids = set(USOS.findall(js))
    for pref in set(MONTADOS.findall(js)):
        for i in range(10):
            ids.add(pref + str(i))

    dir_audio = os.path.join(pasta, "audio")
    if not os.path.isdir(dir_audio):
        print(u"%s -> sem pasta audio/. Nada a conferir." % alvo)
        return 0
    tem = set(f[:-4] for f in os.listdir(dir_audio) if f.endswith(".mp3"))

    cam = os.path.join(pasta, "falas.json")
    texto = {}
    if os.path.exists(cam):
        texto = dict((x["id"], x["texto"]) for x in json.load(io.open(cam, encoding="utf-8")))

    # ⚠️ SEGUNDO BURACO, ago/2026 (Jardim do Broto): a fase que fala uma voz por
    #    rodada monta o id em tempo de execucao — `falaDaTela("jd_come_"+it.img
    #    .replace("jd_",""))`. Nenhuma expressao regular acha isso no codigo, e o
    #    portao dava "voz ok" com 16 alimentos MUDOS. A saida honesta e inverter
    #    a pergunta: o `falas.json` e a VERDADE do que a atividade promete falar,
    #    entao TODA linha dele precisa do mp3 — tenha o id aparecido no codigo ou
    #    nao. Se o texto esta escrito ali, a crianca vai ouvi-lo.
    faltam = sorted(set(i for i in ids if i not in tem and i in texto)
                    | set(i for i in texto if i not in tem))

    print(u"%s -> %d narracao(oes) usada(s) no codigo, %d prometida(s) no falas.json"
          % (alvo, len(ids), len(texto)))
    if faltam:
        print(u"   %d VOZ(ES) COM TEXTO ESCRITO E SEM MP3 (a fase fica MUDA e o "
              u"'ouvir de novo' nao faz nada):" % len(faltam))
        for i in faltam[:10]:
            print(u"    - %s.mp3  (texto: \"%s\")" % (i, texto[i][:58]))
        print(u"   conserto: gerar essas falas com o `gerar-audio.yml` "
              u"(outdir=<pasta>/audio) — o texto ja esta no falas.json.")
        return 1
    print(u"   voz ok: toda fala com texto escrito tem o mp3 gravado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
