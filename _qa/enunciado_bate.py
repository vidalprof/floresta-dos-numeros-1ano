# -*- coding: utf-8 -*-
u"""
PORTÃO DO ENUNCIADO — "a fase promete um assunto e cobra outro?"

NASCEU DE UMA FOTO DO MARCOS (set/2026), com a turma do 4º ano jogando a
Oficina das Palavras. Ele escreveu só: *"Nessa atividade a dica não está
correta"*. A tela mostrava:

    selo:      QUE TEMPO SOU EU?
    enunciado: Ouça as pistas e descubra o TEMPO DO VERBO.
    dica:      Pense se a ação já foi feita ou ainda vai ser.

    PISTA 1 — Eu deixo a palavra pequena.
    PISTA 2 — Termino em -inho ou -inha.
    PISTA 3 — Casinha e gatinho foram feitos por mim.
    [ O DIMINUTIVO ]  [ O AUMENTATIVO ]  [ O VERBO ]  [ A SÍLABA ]

A fase tem três rodadas: passado, futuro e DIMINUTIVO. As duas primeiras são
tempo de verbo; a terceira não é — é grau do substantivo. O título, o enunciado
e a dica falavam pelas duas primeiras e mentiam na terceira. A criança lê "pense
se a ação já foi feita", olha pistas sobre -inho/-inha, e não entende o que
querem dela. Pior: quem ESTÁ aprendendo pode concluir que diminutivo é tempo
verbal, que é um erro que o professor vai ter de desfazer depois.

POR QUE NENHUM PORTÃO PEGAVA: o `_qa/sentido.py` confere se a resposta declarada
bate com a opção certa — e batia. As pistas descrevem o diminutivo corretamente,
a resposta certa É "O DIMINUTIVO", o jogador chega na medalha. Cada peça, isolada,
está certa. O que está errado é o CASAMENTO entre a promessa do enunciado e o que
a fase cobra — e isso ninguém media.

O QUE ELE MEDE: quando o selo, o enunciado ou a dica nomeiam uma FAMÍLIA de
conteúdo (tempo verbal, grau, classe de palavra, sílaba, operação), todas as
respostas da fase têm de ser daquela família. Resposta de outra família = a fase
promete uma coisa e cobra outra.

⚠️ Ele só fala quando TEM certeza: precisa reconhecer a família no enunciado E a
família da resposta. Fase cujo enunciado é genérico ("descubra quem está
falando") não é cobrada — genérico é justamente a saída honesta para uma fase
que mistura assuntos de propósito.

Uso:  python3 _qa/enunciado_bate.py <pasta ou conteudo.json>
Sai 0 se limpo, 1 se reprovou, 2 se não deu para medir.
"""
import json, os, re, sys

LIMPA = re.compile(r"<[^>]*>")


def texto(s):
    return LIMPA.sub(u" ", u"%s" % s).replace(u"&nbsp;", u" ").strip()


# As famílias. Cada uma: como ela se anuncia no ENUNCIADO, e o que são as
# RESPOSTAS dela. Só entra família que já apareceu numa atividade da casa.
FAMILIAS = {
    u"tempo verbal": {
        u"enunciado": [u"tempo do verbo", u"tempo verbal", u"que tempo",
                       u"passado ou futuro", u"quando aconteceu"],
        u"respostas": [u"passado", u"presente", u"futuro"],
    },
    u"grau (aumentativo/diminutivo)": {
        u"enunciado": [u"aumentativo", u"diminutivo", u"grau da palavra",
                       u"palavra pequena", u"palavra grande"],
        u"respostas": [u"diminutivo", u"aumentativo"],
    },
    u"classe de palavra": {
        u"enunciado": [u"classe de palavra", u"substantivo", u"adjetivo",
                       u"que classe"],
        u"respostas": [u"substantivo", u"adjetivo", u"verbo", u"artigo",
                       u"pronome", u"numeral", u"advérbio"],
    },
    u"sílaba": {
        u"enunciado": [u"sílaba", u"silaba", u"pedaço da palavra"],
        u"respostas": [u"sílaba", u"silaba"],
    },
    u"operação": {
        u"enunciado": [u"qual operação", u"qual conta", u"soma ou subtração"],
        u"respostas": [u"adição", u"subtração", u"multiplicação", u"divisão",
                       u"soma", u"menos", u"vezes"],
    },
}


def familia_do_enunciado(t):
    u"""qual família o enunciado ANUNCIA (None se for genérico)."""
    t = texto(t).lower()
    for nome, d in FAMILIAS.items():
        for marca in d[u"enunciado"]:
            if marca in t:
                return nome
    return None


def familia_da_resposta(r):
    u"""a que família a RESPOSTA pertence (None se não reconheço)."""
    r = texto(r).lower()
    for nome, d in FAMILIAS.items():
        for marca in d[u"respostas"]:
            if re.search(r"\b%s\b" % re.escape(marca), r):
                return nome
    return None


def respostas_da_fase(f):
    u"""colhe o que a fase declara como resposta certa, em qualquer mecânica."""
    out = []
    dados = f.get("dados")
    if isinstance(dados, list):
        for d in dados:
            if not isinstance(d, dict):
                continue
            for chave in ("resp", "c", "certa", "r"):
                v = d.get(chave)
                if isinstance(v, str) and v.strip():
                    out.append(v)
                elif isinstance(v, dict) and v.get("t"):
                    out.append(v["t"])
    return out


def confere(caminho):
    if os.path.isdir(caminho):
        caminho = os.path.join(caminho, "conteudo.json")
    if not os.path.exists(caminho):
        print(u"NAO MEDI: nao achei %s" % caminho)
        return 2
    try:
        d = json.load(open(caminho, encoding="utf-8"))
    except Exception as e:
        print(u"NAO MEDI: %s nao e JSON — %s" % (caminho, e))
        return 2

    fases = d.get("fases", d if isinstance(d, list) else [])
    ruins, medidas = [], 0

    for f in fases:
        fid = f.get("id", "?")
        # a promessa mora no selo, no enunciado e na dica — as três falam com a criança
        promessa = u" ".join([texto(f.get("selo", "")), texto(f.get("enunciado", "")),
                              texto(f.get("dica", ""))])
        fam = familia_do_enunciado(promessa)
        if not fam:
            continue          # enunciado genérico: nada a cobrar
        respostas = respostas_da_fase(f)
        if not respostas:
            continue
        medidas += 1
        fora = []
        for r in respostas:
            fr = familia_da_resposta(r)
            if fr and fr != fam:
                fora.append((texto(r), fr))
        if fora:
            ruins.append((fid, texto(f.get("selo", "")) or texto(f.get("enunciado", ""))[:40],
                          fam, fora))

    if not medidas:
        print(u"NAO MEDI: nenhuma fase com enunciado de familia reconhecida em %s"
              % caminho)
        return 2

    if ruins:
        print(u"%s -> %d fase(s) PROMETEM um assunto e COBRAM outro (de %d medidas):"
              % (caminho, len(ruins), medidas))
        for fid, selo, fam, fora in ruins[:8]:
            print(u"    ✗ [%s] “%s” anuncia %s, mas cobra:" % (fid, selo, fam))
            for r, fr in fora[:4]:
                print(u"         · “%s” — isso e %s" % (r, fr))
        print(u"   Conserto: ou tire a rodada que nao pertence, ou deixe o selo, o")
        print(u"   enunciado E a dica genericos (ex.: “descubra quem esta falando”),")
        print(u"   que e a saida honesta para uma fase que mistura assuntos de proposito.")
        return 1

    print(u"%s -> enunciado ok: %d fase(s) com assunto anunciado, todas cobram o que prometem."
          % (caminho, medidas))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/enunciado_bate.py <pasta ou conteudo.json>")
        sys.exit(2)
    sys.exit(confere(sys.argv[1].rstrip("/")))
