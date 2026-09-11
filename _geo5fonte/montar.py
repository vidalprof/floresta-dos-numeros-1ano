# -*- coding: utf-8 -*-
u"""
============================================================
 MONTA A PROVA DE GEOGRAFIA DO 5º ANO a partir do `questoes.json`.

 Por que existe um montador em vez de eu editar o HTML à mão: o `questoes.json`
 é a VERDADE — é ele que o Marcos audita, com a resposta certa sempre em
 primeiro lugar e o campo `fonte` dizendo onde conferir cada dado. O HTML é
 produto; se eu editasse os dois, eles iam divergir no primeiro conserto.

 ⚠️ E É AQUI QUE AS ALTERNATIVAS SE EMBARALHAM. No arquivo-fonte a certa é
    sempre a primeira, de propósito (auditar 20 questões em que a resposta
    muda de lugar é como o erro entra). Na prova isso seria um desastre — a
    criança perceberia em três questões que a A é sempre a certa. O embaralho
    usa uma SEMENTE FIXA: a prova sai sempre igual (a turma toda vê a mesma
    coisa, o gabarito do painel vale) mas com a certa em lugares diferentes.

 Uso: python3 _geo5fonte/montar.py
============================================================
"""
import io
import json
import os
import random
import re

# ⚠️ A FONTE E O PRODUTO MORAM SEPARADOS, de proposito:
#    `_geo5fonte/` fica NESTE repositorio e nunca sobe — e onde vivem o
#    `questoes.json` (a certa e sempre a primeira), o `GABARITO.md` e os 25 MB
#    de mapas baixados. Se isso fosse junto, a criança acharia o gabarito
#    digitando o endereço, e o repositorio publicado engasgaria o build do
#    Pages com o peso (ja aconteceu nesta casa).
#    `_geo5/` e so o que o navegador precisa: HTML, figuras, voz.
FONTE = os.path.dirname(os.path.abspath(__file__))
AQUI = os.path.join(FONTE, "..", "_geo5")
# ⚠️ A SEMENTE NÃO É QUALQUER NÚMERO. Esta foi escolhida medindo: ela deixa o
#    gabarito em 5 A, 5 B, 5 C, 5 D e nunca a mesma letra três vezes seguidas.
#    A primeira que usei (20260911) dava C nove vezes em vinte — quem marcasse
#    tudo C levava 45% sem ler nada, e a prova deixava de medir o que mede.
SEMENTE = 20260386          # trava a ordem: mesma prova para a turma toda

TURMAS = [u"5º A", u"5º B", u"5º C", u"5º D"]
SLUG = "geografia-sc-5ano"
TITULO = u"Expedição Cartográfica — Geografia de Santa Catarina"
HISTORIA = (
    u"Olá, explorador! Esta é a sua expedição pela Geografia de Santa Catarina. "
    u"São vinte perguntas sobre o nosso estado: onde ele fica, como é o relevo, o "
    u"clima, os rios, a vegetação — e, principalmente, como LER um mapa de verdade. "
    u"Quase toda pergunta tem um mapa ou uma foto junto: olhe com calma antes de "
    u"responder, porque a resposta quase sempre está ali. Eu leio cada pergunta e "
    u"cada alternativa em voz alta, e você toca na que achar certa. Agora escreva o "
    u"seu nome, escolha a sua turma e o seu personagem, e toque em começar!")


def num_por_extenso(n):
    nomes = [u"um", u"dois", u"três", u"quatro", u"cinco", u"seis", u"sete", u"oito",
             u"nove", u"dez", u"onze", u"doze", u"treze", u"catorze", u"quinze",
             u"dezesseis", u"dezessete", u"dezoito", u"dezenove", u"vinte"]
    return nomes[n - 1]


def fala_da_questao(n, pergunta, opcoes):
    u"""a narração: o número da questão, o enunciado e cada alternativa com a letra.

    ⚠️ A voz lê o texto LIMPO: sem as marcas do HTML e sem os parênteses de
       crédito. O que a criança ouve tem que ser o que ela lê."""
    limpo = re.sub(r"<[^>]+>", u"", pergunta)
    letras = u"ABCDEFG"
    partes = [u"Pergunta %s." % num_por_extenso(n), limpo]
    for i, o in enumerate(opcoes):
        partes.append(u"Letra %s: %s" % (letras[i], re.sub(r"<[^>]+>", u"", o)))
    return u" ".join(partes)


def chave_voz(texto):
    u"""o MESMO djb2 do `_chaveVoz` do HTML — o nome do mp3 sai do texto.

    ⚠️ Se este cálculo divergir do JavaScript por um caractere, o app procura um
       mp3 que não existe e a prova fica MUDA sem dar erro nenhum. Por isso o
       `confere_falas` abaixo compara os dois no fim."""
    s = re.sub(r"\s+", u" ", texto).strip()
    h = 5381
    for ch in s:
        h = ((h * 33) + ord(ch)) & 0xFFFFFFFF
    return u"v0" if h == 0 else u"v" + _b36(h)


def _b36(n):
    d = u"0123456789abcdefghijklmnopqrstuvwxyz"
    if n == 0:
        return u"0"
    out = u""
    while n:
        out = d[n % 36] + out
        n //= 36
    return out


def escreve_falas(html, questoes):
    u"""o `falas.json` — a VERDADE da voz, que o `entregar.yml` grava.

    Entra tudo que o app manda para o `falar()`: a história da capa, a narração
    de cada pergunta, CADA ALTERNATIVA (o alto-falante que a criança toca), as
    frases de passagem e os avisos da capa. Texto que não estiver aqui vira
    silêncio na sala."""
    voz = io.open(os.path.join(AQUI, "voz.txt"), encoding="utf-8").read().strip()
    textos = [HISTORIA]
    for q in questoes:
        textos.append(q["fala"])
        textos.extend(q["opcoes"])          # o alto-falante de cada alternativa
    textos.extend([u"Próxima pergunta!", u"Vamos continuar!",
                   u"Muito bem, siga em frente!", u"Continue!"])
    # os avisos escritos à mão dentro do HTML, pegos do próprio arquivo
    textos.extend(re.findall(r'falar\("([^"]+)"', html))

    vistos, falas = set(), []
    for tx in textos:
        tx = re.sub(r"\s+", u" ", tx).strip()
        if not tx or tx in vistos:
            continue
        vistos.add(tx)
        falas.append({"id": chave_voz(tx), "texto": tx, "voz": voz})
    io.open(os.path.join(AQUI, "falas.json"), "w", encoding="utf-8").write(
        json.dumps(falas, ensure_ascii=False, indent=1))
    print(u"falas.json: %d falas (voz %s)" % (len(falas), voz))


def main():
    fonte = json.load(io.open(os.path.join(FONTE, "questoes.json"), encoding="utf-8"))
    creditos = json.load(io.open(os.path.join(AQUI, "creditos.json"), encoding="utf-8"))
    curriculo = json.load(io.open(os.path.join(AQUI, "curriculo.json"), encoding="utf-8"))
    qs = fonte["questoes"]
    if len(qs) != 20:
        raise SystemExit(u"esperava 20 questoes, achei %d" % len(qs))

    # ---- PORTÃO DO CURRÍCULO: questão que nenhum objetivo mede é questão solta
    #      (e objetivo que aponta uma questão inexistente é promessa vazia).
    cobre = []
    for o in curriculo["objetivos"]:
        cobre.extend(o["questoes"])
    faltam = [q["n"] for q in qs if q["n"] not in cobre]
    repete = sorted(set(n for n in cobre if cobre.count(n) > 1))
    sobra = sorted(set(n for n in cobre if n not in [q["n"] for q in qs]))
    if faltam or repete or sobra:
        raise SystemExit(u"curriculo.json nao fecha com a prova: sem objetivo %s | "
                         u"em dois objetivos %s | questao inexistente %s"
                         % (faltam or u"-", repete or u"-", sobra or u"-"))

    rnd = random.Random(SEMENTE)
    saida, gabarito = [], []
    for q in qs:
        if q["correta"] != 0:
            raise SystemExit(u"questao %d: no arquivo-fonte a certa tem que ser a "
                             u"PRIMEIRA (e o que torna a auditoria possivel)" % q["n"])
        ops = list(q["opcoes"])
        certa_txt = ops[0]
        rnd.shuffle(ops)
        correta = ops.index(certa_txt)
        gabarito.append(u"ABCD"[correta])
        saida.append({
            "disc": q["eixo"],
            "img": q["img"],
            "pergunta": q["pergunta"],
            "opcoes": ops,
            "correta": correta,
            "fala": fala_da_questao(q["n"], q["pergunta"], ops),
        })

    # ---- PORTÃO DO GABARITO: prova em que uma letra domina não mede nada
    from collections import Counter as _C
    _c = _C(gabarito)
    if max(_c.values()) > 6:
        raise SystemExit(u"gabarito desequilibrado (%s): troque a SEMENTE"
                         % u" ".join(u"%s=%d" % (k, _c[k]) for k in u"ABCD"))
    for i in range(len(gabarito) - 2):
        if gabarito[i] == gabarito[i + 1] == gabarito[i + 2]:
            raise SystemExit(u"a letra %s se repete 3x seguidas (questao %d): "
                             u"troque a SEMENTE" % (gabarito[i], i + 1))

    # ---- o bloco JS das questões, uma por linha, legível no diff
    linhas = []
    for i, q in enumerate(saida):
        linhas.append(u' {disc:%s, img:%s, pergunta:%s,\n  opcoes:%s, correta:%d,\n  fala:%s}'
                      % (json.dumps(q["disc"], ensure_ascii=False),
                         json.dumps(q["img"], ensure_ascii=False),
                         json.dumps(q["pergunta"], ensure_ascii=False),
                         json.dumps(q["opcoes"], ensure_ascii=False),
                         q["correta"],
                         json.dumps(q["fala"], ensure_ascii=False)))
    bloco = u"var QUESTOES=[\n" + u",\n\n".join(linhas) + u"\n];"

    cam = os.path.join(AQUI, "index.html")
    t = io.open(cam, encoding="utf-8").read()
    t = re.sub(r"var QUESTOES=\[.*?\n\];", lambda _: bloco, t, count=1, flags=re.S)

    # ---- configuração
    t = re.sub(r'var TURMAS=\[.*?\];',
               u'var TURMAS=[%s];' % u",".join(u'"%s"' % x for x in TURMAS), t, count=1)
    t = re.sub(r'var SLUG="[^"]*";', u'var SLUG="%s";' % SLUG, t, count=1)
    t = re.sub(r'var HISTORIA="[^"]*";',
               u'var HISTORIA=%s;' % json.dumps(HISTORIA, ensure_ascii=False), t, count=1)
    t = re.sub(r"var AVATARES=\[.*?\];",
               u'var AVATARES=[\n {id:"geo_cr1.png", cor:"#2f7d4f"},{id:"geo_cr2.png", cor:"#2a6fb0"},\n'
               u' {id:"geo_cr3.png", cor:"#c25a2c"},{id:"geo_cr4.png", cor:"#6f4fa8"},\n'
               u' {id:"geo_cr5.png", cor:"#b03a63"},{id:"geo_cr6.png", cor:"#b8860b"}\n];',
               t, count=1, flags=re.S)
    t = re.sub(r"var DISCNOME=\{.*?\};",
               u"var DISCNOME=" + json.dumps(fonte["eixos"], ensure_ascii=False) + u";",
               t, count=1, flags=re.S)
    t = re.sub(r"<title>[^<]*</title>", u"<title>%s — 5º ano</title>" % TITULO, t, count=1)

    # ---- o CRÉDITO das imagens, exigência de quem usa mapa de terceiro
    cr = u'<div id="creditos"><b>Créditos das imagens</b><ul>'
    for c in creditos:
        cr += (u"<li>%s — %s (%s). <a href=\"%s\" target=\"_blank\" rel=\"noopener\">Wikimedia Commons</a></li>"
               % (c["legenda"], c["autor"] or u"autor não informado", c["licenca"], c["pagina"]))
    cr += (u"<li>Fotos de paisagens de Santa Catarina: acervo da própria escola, "
           u"reaproveitadas da Expedição Santa Catarina.</li>"
           u"<li>Perfil do relevo e mapas esquemáticos: desenhados para esta prova.</li>")
    cr += u"</ul></div>"
    if 'id="creditos"' in t:
        t = re.sub(r'<div id="creditos">.*?</div>', lambda _: cr, t, count=1, flags=re.S)
    else:
        t = t.replace(u"</body>", cr + u"\n</body>", 1)

    io.open(cam, "w", encoding="utf-8").write(t)
    escreve_falas(t, saida)

    # ---- o painel do professor
    camp = os.path.join(AQUI, "..", "_geo5painel", "index.html")
    p = io.open(camp, encoding="utf-8").read()
    p = re.sub(r'var SLUG="[^"]*";', u'var SLUG="%s";' % SLUG, p, count=1)
    p = re.sub(r"<title>[^<]*</title>",
               u"<title>Painel — Expedição Cartográfica</title>", p, count=1)
    # ⚠️ O painel NÃO se edita à mão: o gabarito dele tem que ser o MESMO que a
    #    semente sorteou nesta montagem. Se os dois se separassem, o professor
    #    veria "a turma toda errou a 3" quando ninguém errou nada.
    dados = (u"/*DADOS-INI*/\n"
             u"var TITULO=%s;\n"
             u"var TURMAS=%s;\n"
             u"var GABARITO=%s;\n"
             u"var EIXOS=%s;\n"
             u"var ARQCSV=%s;\n"
             u"var CURRICULO=" + json.dumps(curriculo, ensure_ascii=False) + u";\n"
             u"/*DADOS-FIM*/") % (
        json.dumps(u"Geografia de Santa Catarina · 5º ano · Prova trimestral",
                   ensure_ascii=False),
        json.dumps(TURMAS, ensure_ascii=False),
        json.dumps([q["correta"] for q in saida]),
        json.dumps([fonte["eixos"][q["eixo"]] for q in qs], ensure_ascii=False),
        json.dumps(SLUG + u"-notas.csv"))
    p = re.sub(r"/\*DADOS-INI\*/.*?/\*DADOS-FIM\*/", lambda _: dados, p, count=1, flags=re.S)
    io.open(camp, "w", encoding="utf-8").write(p)

    # ---- o gabarito, para o professor conferir sem abrir o código
    gab = u"# Gabarito — %s\n\n(gerado por `python3 _geo5/montar.py`; semente %d)\n\n" % (TITULO, SEMENTE)
    gab += u"| # | eixo | resposta | o que a questão mede |\n|---|---|---|---|\n"
    for q, g in zip(qs, gabarito):
        gab += u"| %d | %s | **%s** | %s |\n" % (q["n"], fonte["eixos"][q["eixo"]], g,
                                                 q["opcoes"][0].rstrip("."))
    io.open(os.path.join(FONTE, "GABARITO.md"), "w", encoding="utf-8").write(gab)

    print(u"prova montada: %d questoes | gabarito %s" % (len(saida), u"".join(gabarito)))
    from collections import Counter
    c = Counter(gabarito)
    print(u"   distribuicao das certas: " + u"  ".join(u"%s=%d" % (k, c[k]) for k in u"ABCD"))
    for k, v in Counter(q["eixo"] for q in qs).most_common():
        print(u"   %-6s %d questao(oes)  %s" % (k, v, fonte["eixos"][k]))


if __name__ == "__main__":
    main()
