# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO DO CATÁLOGO — "esta atividade existe no painel do Marcos?"

 ⭐ PEDIDO DO MARCOS (set/2026), logo depois que o painel ficou pronto:
 *"um lembrete, cada atividade nova vai para esse painel certo? certifique-se
 disso, que cada seção saiba disso"*.

 "Cada seção saiba" não pode ser uma PROMESSA minha — eu começo cada sessão sem
 memória, e promessa é justamente o que se perde. Por isso a regra virou PORTÃO:
 o `entregar.yml` chama este arquivo antes de publicar, e uma atividade que não
 está no catálogo **não sobe**. Assim a próxima sessão não precisa lembrar de
 nada: ela é obrigada pelo portão.

 A CORRENTE, e por que ela fecha sozinha:
   `ATIVIDADES.md` (fonte única da verdade)
        -> `python3 _painel/montar_painel.py` (gera o painel do catálogo)
        -> `_painel/index.html`  -> publicado em painel-atividades
 Uma linha nova no catálogo vira um cartão novo no painel. Nenhum passo é
 manual, então nenhum passo pode ser esquecido.

 O que ele cobra, para a pasta que está sendo publicada:
   1. **ESTÁ NO CATÁLOGO** — existe uma linha no `ATIVIDADES.md` cuja coluna
      "Pasta" é esta pasta. Sem isso, a atividade some do painel e o Marcos
      volta a me pedir o link no chat — o atrito que o painel existe para matar.
   2. **O LINK É O DE VERDADE** — quando o destino é informado (é o que o
      `entregar.yml` faz), a linha tem que trazer
      `https://vidalprof.github.io/<destino>/`. Uma linha com link errado é pior
      que linha nenhuma: ele copia, cola na sala e abre a atividade errada.
   3. **O PAINEL ESTÁ EM DIA** — o `_painel/index.html` commitado tem que bater
      com o que o `ATIVIDADES.md` gera AGORA. Se alguém editou o catálogo e não
      rodou o montador, o painel no ar é uma cópia velha.

 ⚠️ O QUE ELE NÃO MEDE: se o texto do "o que trabalha" está bom, se a turma está
 certa, se o link está no ar (isso é do `noar` do próprio `entregar.yml`).

 Uso:  python3 _qa/catalogo.py <pasta> [destino]
       ex.: python3 _qa/catalogo.py _pinta pinta-e-monta
       Sem argumento: confere a corrente inteira (item 3 + linhas sem link).
 Sai 0 se está no painel, 1 se ficou de fora, 2 se não deu para medir.
============================================================
"""
import io
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CATALOGO = os.path.join(RAIZ, "ATIVIDADES.md")
PAINEL = os.path.join(RAIZ, "_painel", "index.html")
MONTADOR = os.path.join(RAIZ, "_painel", "montar_painel.py")


def _itens():
    u"""lê o catálogo com o MESMO código do montador — se o portão lesse de um
    jeito e o painel de outro, o portão aprovaria o que o painel não mostra."""
    if not os.path.exists(MONTADOR):
        return None, u"nao achei o montador do painel (%s)" % MONTADOR
    sys.path.insert(0, os.path.dirname(MONTADOR))
    try:
        import montar_painel
    except Exception as e:                       # noqa: BLE001
        return None, u"nao consegui carregar o montador: %s" % e
    itens = montar_painel.le_catalogo()
    if itens is None:
        return None, u"nao achei o %s" % CATALOGO
    return itens, None


def _dados_do_painel():
    u"""o JSON que está DENTRO do `_painel/index.html` publicado"""
    if not os.path.exists(PAINEL):
        return None, u"o painel ainda nao foi gerado (%s)" % PAINEL
    html = io.open(PAINEL, encoding="utf-8").read()
    m = re.search(r"var DADOS = ", html)
    if not m:
        return None, u"o painel nao tem a marca `var DADOS =`"
    try:
        dados, _ = json.JSONDecoder().raw_decode(html, m.end())
    except ValueError as e:
        return None, u"o JSON do painel nao le: %s" % e
    return dados, None


def _chave(a):
    return (a.get("turma", ""), a.get("nome", ""), a.get("pasta", ""),
            a.get("trabalha", ""), a.get("link", ""), a.get("painel", ""))


def confere(pasta=None, destino=None):
    itens, erro = _itens()
    if itens is None:
        print(u"NAO MEDI: %s" % erro)
        return 2

    problemas = []

    # 1 e 2 — a atividade que está subindo agora
    if pasta:
        p = pasta.strip().rstrip("/")
        linha = [a for a in itens if a["pasta"] == p]
        if not linha:
            problemas.append(
                u"A pasta `%s` NAO esta no ATIVIDADES.md. Toda atividade nova "
                u"entra no catalogo — uma linha na tabela do ANO (o titulo `## "
                u"<ano>`), com Nome | O que trabalha | Pasta | Link — e so assim "
                u"aparece no painel de links do Marcos. Adicione a linha e rode "
                u"`python3 _painel/montar_painel.py`." % p)
        elif destino:
            alvo = u"https://vidalprof.github.io/%s/" % destino.strip().strip("/")
            temlink = [a for a in linha if a["link"].rstrip("/") + u"/" == alvo]
            if not temlink:
                tem = u" · ".join(a["link"] or u"(sem link)" for a in linha)
                problemas.append(
                    u"A linha de `%s` no ATIVIDADES.md nao aponta para o site "
                    u"que esta sendo publicado. Esperado: %s. Achei: %s."
                    % (p, alvo, tem))

    # 3 — o painel bate com o catálogo?
    dados, erro = _dados_do_painel()
    if dados is None:
        print(u"%s -> NAO MEDI o painel: %s" % (pasta or u"catalogo", erro))
        if problemas:
            print(u"   REPROVOU:")
            for x in problemas:
                print(u"    - %s" % x)
            return 1
        return 2
    agora = sorted(_chave(a) for a in itens)
    nele = sorted(_chave(a) for a in dados)
    emdia = (agora == nele)
    if not emdia:
        falta = [k for k in agora if k not in nele]
        sobra = [k for k in nele if k not in agora]
        det = u""
        if falta:
            det += u" Falta(m) no painel: %s." % u", ".join(k[1] for k in falta[:6])
        if sobra:
            det += u" So no painel (linha mudou/saiu): %s." % \
                   u", ".join(k[1] for k in sobra[:6])
        problemas.append(
            u"O `_painel/index.html` esta ATRASADO em relacao ao ATIVIDADES.md."
            u"%s Rode `python3 _painel/montar_painel.py` e commite." % det)

    sem = [a["nome"] for a in itens if not a["link"]]
    print(u"%s -> catalogo com %d atividade(s); painel %s"
          % (pasta or u"catalogo", len(itens),
             u"em dia com o catalogo" if emdia else u"ATRASADO"))
    if sem:
        print(u"   aviso: %d sem link no catalogo (%s)"
              % (len(sem), u", ".join(sem[:5])))

    if problemas:
        print(u"   REPROVOU:")
        for x in problemas:
            print(u"    - %s" % x)
        return 1
    if pasta:
        print(u"   `%s` esta no catalogo e no painel, com o link certo." % pasta)
    return 0


if __name__ == "__main__":
    _p = sys.argv[1] if len(sys.argv) > 1 else None
    _d = sys.argv[2] if len(sys.argv) > 2 else None
    sys.exit(confere(_p, _d))
