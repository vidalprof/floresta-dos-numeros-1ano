# -*- coding: utf-8 -*-
u"""
PORTÃO DA RESPOSTA ENTREGUE — "a pergunta já dá a resposta de graça?"

NASCEU DO REVISOR FINAL (set/2026), na primeira foto que ele tirou. A fase 2 da
Revista das Palavras mostrava, na tela do celular:

    “Guardei o **bolo** na geladeira.” Qual palavra é um SUBSTANTIVO?
       [ guardei ]   [ bolo ]   [ na ]

O "bolo" da pergunta estava em NEGRITO E LARANJA. A criança não precisava saber
o que é substantivo: bastava procurar a palavra pintada. Eram 16 perguntas
assim, e a fase inteira — que existe para ENSINAR a reconhecer substantivo —
virava um jogo de achar a cor.

POR QUE NENHUM DOS 65 PORTÕES PEGOU: todos leem o CÓDIGO e o código estava
impecável. A resposta declarada batia com a opção certa (`_qa/sentido.py`
aprovou), a dica crescia direito, a voz dizia o escrito, o jogador chegava na
medalha. O defeito não é de código: é de DIDÁTICA, e só aparece quando alguém
OLHA a tela e pensa "espera, isso está entregue".

A regra que fica: **o destaque da pergunta nunca pode cair em cima da
resposta.** Destacar a palavra em foco é bom quando a tarefa é sobre OUTRA
coisa ("na frase X, quem é o dono do cachorro?"); vira entrega quando a tarefa
é justamente ACHAR aquela palavra.

O que ele mede, em cada pergunta de escolha (`c` = certa, `e` = erradas):
  1. a resposta certa aparece marcada (<b>, <strong>, <mark>, <u>, <i>) na
     própria pergunta → REPROVA;
  2. só a certa está marcada e nenhuma errada está → REPROVA (é o mesmo defeito
     escrito de outro jeito: a marca aponta a resposta);
  3. a resposta certa é a única opção que aparece LITERALMENTE no texto da
     pergunta, e a tarefa é de "qual palavra" → AVISA (pode ser legítimo, mas é
     onde o defeito costuma morar).

Uso:  python3 _qa/entrega.py <pasta ou conteudo.json>
Sai 0 se limpo, 1 se reprovou, 2 se não deu para medir.
"""
import json, os, re, sys

MARCAS = re.compile(r"<\s*(b|strong|mark|u|i|em)\s*>(.*?)<\s*/\s*\1\s*>", re.I | re.S)
LIMPA  = re.compile(r"<[^>]*>")

# perguntas em que a tarefa É achar a palavra — aqui o destaque nunca vale
TAREFA_DE_ACHAR = re.compile(
    u"qual palavra|que palavra|marque a palavra|marque as palavras|"
    u"qual delas|qual e o substantivo|qual é o substantivo|qual e o adjetivo|"
    u"qual é o adjetivo|qual e o verbo|qual é o verbo|aponte|encontre|"
    u"identifique|classifique", re.I)


def texto(s):
    return LIMPA.sub(u" ", unicode_(s)).replace(u"&nbsp;", u" ").strip()


def unicode_(s):
    try:
        return s if isinstance(s, str) else str(s)
    except Exception:
        return u""


def marcadas(p):
    u"""o que está destacado dentro da pergunta, em minúsculas e sem tag."""
    return [texto(m.group(2)).lower().strip(u" .,;:!?“”\"'") for m in MARCAS.finditer(p)]


def confere(caminho):
    if os.path.isdir(caminho):
        caminho = os.path.join(caminho, "conteudo.json")
    if not os.path.exists(caminho):
        print(u"NAO MEDI: nao achei %s" % caminho)
        return 2
    try:
        d = json.load(open(caminho, encoding="utf-8"))
    except Exception as e:
        print(u"NAO MEDI: %s nao e JSON valido — %s" % (caminho, e))
        return 2

    fases = d.get("fases", d if isinstance(d, list) else [])
    if not fases:
        print(u"NAO MEDI: nenhuma fase em %s" % caminho)
        return 2

    ruins, avisos, medidas = [], [], 0
    for f in fases:
        fid = f.get("id", "?")
        dados = f.get("dados")
        if not isinstance(dados, list):
            continue
        for q in dados:
            if not isinstance(q, dict):
                continue
            certa = texto(q.get("c", "")).lower().strip(u" .,;:!?“”\"'")
            if not certa:
                continue
            p = unicode_(q.get("p", ""))
            if not p:
                continue
            medidas += 1
            erradas = [texto(x).lower().strip(u" .,;:!?“”\"'")
                       for x in (q.get("e") or []) if texto(x)]
            marcas = marcadas(p)

            # 1) a resposta certa está destacada na pergunta
            if certa in marcas:
                ruins.append(u"[%s] a pergunta DESTACA a resposta: “...%s...” e a certa e “%s”. "
                             u"A crianca acha pela cor, nao pelo conceito." %
                             (fid, u"/".join(marcas)[:60], certa))
                continue

            # 2) alguma marca CONTEM a certa (ex.: <b>o bolo</b> e a certa "bolo")
            for m in marcas:
                if certa and certa in m.split():
                    ruins.append(u"[%s] a pergunta destaca “%s”, que carrega a resposta “%s”." %
                                 (fid, m[:40], certa))
                    break
            else:
                # 3) só as erradas apareceriam se o destaque fosse neutro;
                #    aqui olhamos o caso "a certa e a unica opcao no texto"
                if TAREFA_DE_ACHAR.search(texto(p)):
                    corpo = u" " + texto(p).lower() + u" "
                    tem_certa = re.search(r"\b%s\b" % re.escape(certa), corpo)
                    tem_errada = any(re.search(r"\b%s\b" % re.escape(x), corpo)
                                     for x in erradas if x)
                    if tem_certa and erradas and not tem_errada:
                        avisos.append(u"[%s] so a resposta “%s” aparece no texto da pergunta; "
                                      u"as erradas nao. Da para acertar por eliminacao, sem o "
                                      u"conceito. (Pode ser legitimo — confira.)" % (fid, certa))

    if not medidas:
        print(u"NAO MEDI: nenhuma pergunta com resposta declarada (`c`) em %s" % caminho)
        return 2

    for a in avisos[:8]:
        print(u"   aviso: %s" % a)
    if ruins:
        print(u"%s -> %d pergunta(s) ENTREGAM a resposta (de %d conferidas):"
              % (caminho, len(ruins), medidas))
        for r in ruins[:12]:
            print(u"    ✗ %s" % r)
        if len(ruins) > 12:
            print(u"    ... e mais %d" % (len(ruins) - 12))
        print(u"   Conserto: tire a marcacao de cima da palavra que e a resposta. "
              u"Destaque so o que NAO se pergunta.")
        return 1

    print(u"%s -> entrega ok: %d pergunta(s) conferidas, nenhuma destaca a propria resposta."
          % (caminho, medidas))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/entrega.py <pasta ou conteudo.json>")
        sys.exit(2)
    sys.exit(confere(sys.argv[1].rstrip("/")))
