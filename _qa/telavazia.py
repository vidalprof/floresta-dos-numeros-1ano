#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO DA TELA VAZIA — "sobrou o fundo falando sozinho?"

Defeito que o Marcos pegou (ago/2026): *"na fase de quem esta aqui, quando
conclui, fica so a tela de fundo e falando, fica feio, favor corrigir e
verificar se isso não acontece em outras fases também"*. Ele estava certo, e não
era um caso isolado: **23 fases** das duas atividades terminavam assim.

O MOLDE DO DEFEITO é sempre o mesmo:

    function passo(){
      limpa();                       // apaga TUDO da tela
      if(idx>=LISTA.length){         // acabou a fase
        depoisDaFala("x_revela",13000,function(){ mostraBanner(...); });
        return;                      // ... e nao desenha NADA
      }
      ...

Entre o `limpa()` e o `mostraBanner` passam-se até **13 segundos** de narração
com a tela em branco: a criança fica olhando o fundo de madeira ouvindo uma voz
sem dono. No print isso nunca aparece, porque print nenhum pega o meio de uma
narração — só jogando a fase até o fim.

O CONSERTO é o `fechaFase()` do motor: o fecho vira uma TELA de verdade (o
mascote, o selo da fase e o que ele está dizendo, escrito). Este portão garante
que ninguém volte ao molde antigo.

REGRA: se uma função chama `limpa()` e, sem desenhar nada (`app.appendChild`),
chega a um `depoisDaFala(...)` seguido de `return`, é tela vazia falando.

Uso:  python3 _qa/telavazia.py _naveg/index.html
Sai com 1 se achar.
"""
import io
import re
import sys


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    alvo = sys.argv[1]
    html = io.open(alvo, encoding="utf-8").read()
    js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    # comentário não é código (a lição do _qa/padrao.py)
    js = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), js, flags=re.S)

    achados = []
    for m in re.finditer(r"\blimpa\(\);", js):
        trecho = js[m.end():m.end() + 700]
        # até onde vai este caminho: para no primeiro `return;`
        r = trecho.find("return;")
        if r < 0:
            continue
        cam = trecho[:r]
        if "depoisDaFala(" not in cam:
            continue
        if "app.appendChild" in cam or "fechaFase(" in cam:
            continue
        d = re.search(r'depoisDaFala\("([a-z0-9_]+)"', cam)
        achados.append(d.group(1) if d else "?")

    print(u"%s -> fechos de fase conferidos" % alvo)
    if achados:
        print(u"   %d TELA(S) VAZIA(S) FALANDO SOZINHA(S) (a crianca olha o fundo "
              u"enquanto a voz conta o final):" % len(achados))
        for a in achados[:10]:
            print(u"    - depois de %s a tela fica em branco" % a)
        print(u"   conserto: use `fechaFase(selo,texto,idFala,ms,proxima,prog)` "
              u"— ele desenha o mascote e o texto enquanto a voz fala.")
        return 1
    print(u"   fecho ok: nenhuma fase termina com a tela vazia")
    return 0


if __name__ == "__main__":
    sys.exit(main())
