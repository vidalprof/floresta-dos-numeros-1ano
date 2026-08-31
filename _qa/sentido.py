# -*- coding: utf-8 -*-
u"""PORTÃO DE SENTIDO — a SEGUNDA LEITURA (o QC de significado da linha de montagem).

Nasceu da investigação (set/2026): os ~60 portões medem se a atividade EXISTE e é
CONSISTENTE (roda, a figura carrega, o alvo tem 44px, a voz tem mp3). NENHUM lê o
SIGNIFICADO do conteúdo. Por isso a classe que mais chega ao Marcos — resposta
declarada errada, dica que não descreve a resposta, voz que não bate com o texto,
enunciado ambíguo, fonte fora do ano — atravessa a banca inteira, e o ÚNICO leitor
de sentido vira o professor. Isto aqui dá esse olho à máquina.

COMO FUNCIONA (cirúrgico e otimizado — UM payload por atividade, UMA leitura):
  1. Este script MONTA o payload: lê o `conteudo.json` e emite, por fase, só o que
     importa para a 2ª leitura — enunciado, dica, resposta marcada como CERTA, as
     erradas, e a VOZ de cada uma. Um bloco de texto compacto por atividade.
  2. A LEITURA de sentido é feita por um segundo modelo (o revisor), que responde,
     por fase, três perguntas objetivas:
        · a resposta marcada como CERTA está de fato correta?
        · a DICA descreve/ajuda a chegar nessa resposta (e não em outra)?
        · a VOZ de cada opção diz o mesmo que o TEXTO que aparece na tela?
     — e, quando dá, dois extras: o enunciado é claro (sem ambiguidade) e o
        conteúdo cabe no ano/disciplina.
  3. No CI (`entregar.yml`, que tem internet) tenta rodar essa leitura por LLM se
     houver chave que responda; sem chave/quota, EMITE o payload e marca a revisão
     como PENDENTE (o revisor humano/Claude lê o payload e aprova) — nunca finge
     que passou.

Uso:
  python3 _qa/sentido.py <pasta>                 # emite o payload (stdout)
  python3 _qa/sentido.py <pasta> --json          # payload estruturado (p/ LLM)
  python3 _qa/sentido.py <pasta> --out FILE       # grava o payload num arquivo
Sai 0 sempre que CONSEGUIU montar o payload (o veredito de sentido é do revisor);
2 se não achou conteudo.json.
"""
import io
import json
import os
import re
import sys

# chaves que costumam marcar a RESPOSTA CERTA nas várias mecânicas
_CERTAS = ("c", "cer", "certa", "resp", "alvo", "correta", "ok")
# chaves das ERRADAS / distratores
_ERRADAS = ("e", "out", "erradas", "distratores")
# chaves de DICA
_DICAS = ("d", "dic", "dica", "dicas", "d1", "d2", "d3")
# chaves de VOZ (o que o alto-falante fala)
_VOZ = ("voz", "vozsen", "cvoz")


def _txt(v):
    u"""tira HTML/entidades para o revisor ler o que a criança VÊ."""
    if isinstance(v, dict):
        # opção {t:"5", voz:"cinco"} etc.
        base = v.get("t", v.get("n", v.get("nome", "")))
        voz = v.get("voz", "")
        s = _limpa(str(base))
        if voz and _limpa(str(voz)) != s:
            s += u"  [voz: %s]" % _limpa(str(voz))
        return s
    return _limpa(str(v))


def _limpa(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = (s.replace("&mdash;", "—").replace("&eacute;", "é").replace("&aacute;", "á")
          .replace("&ccedil;", "ç").replace("&atilde;", "ã").replace("&otilde;", "õ")
          .replace("&iacute;", "í").replace("&oacute;", "ó").replace("&#225;", "á")
          .replace("&#234;", "ê").replace("&#233;", "é").replace("&#227;", "ã")
          .replace("&nbsp;", " ").replace("&minus;", "−"))
    s = re.sub(r"&#?\w+;", "", s)
    return re.sub(r"\s+", " ", s).strip()


def _campo(d, chaves):
    for k in chaves:
        if isinstance(d, dict) and k in d and d[k] not in (None, "", [], {}):
            return d[k]
    return None


def _rodada_txt(r):
    u"""uma rodada/opção de `dados`: mostra CERTA, ERRADAS, DICA, VOZ que houver."""
    if not isinstance(r, dict):
        return u"  · " + _txt(r)
    linhas = []
    cer = _campo(r, _CERTAS)
    if cer is not None:
        if isinstance(cer, list):
            linhas.append(u"  CERTA: " + " | ".join(_txt(x) for x in cer))
        else:
            linhas.append(u"  CERTA: " + _txt(cer))
    err = _campo(r, _ERRADAS)
    if err is not None:
        err = err if isinstance(err, list) else [err]
        linhas.append(u"  ERRADAS: " + " | ".join(_txt(x) for x in err))
    dic = _campo(r, _DICAS)
    if dic is not None:
        dic = dic if isinstance(dic, list) else [dic]
        linhas.append(u"  DICA: " + " / ".join(_txt(x) for x in dic))
    # enunciado interno da rodada (p/quiz que muda a pergunta por rodada)
    for k in ("p", "enun", "pergunta", "ante", "bal", "fala"):
        if isinstance(r, dict) and r.get(k):
            linhas.append(u"  PERGUNTA: " + _txt(r[k]))
            break
    # INTRUSO: os itens comparados, o que fica de fora, e as RAZÕES (explicação).
    if isinstance(r.get("itens"), list):
        linhas.append(u"  ITENS: " + " | ".join(_txt(x) for x in r["itens"]))
    if r.get("fora") is not None or r.get("nomeFora"):
        linhas.append(u"  INTRUSO (o que NÃO combina): " + _txt(r.get("nomeFora") or r.get("fora")))
    if isinstance(r.get("razoes"), list):
        rz = []
        for x in r["razoes"]:
            t = _txt(x)
            if isinstance(x, dict) and x.get("ok"):
                t += u"  ← marcada como razão CERTA"
            rz.append(t)
        linhas.append(u"  RAZÕES (por quê): " + " | ".join(rz))
    if r.get("enunPorque"):
        linhas.append(u"  PERGUNTA-PORQUÊ: " + _txt(r["enunPorque"]))
    # QUEM-SOU-EU: as pistas e os outros; a resposta
    if isinstance(r.get("pistas"), list):
        linhas.append(u"  PISTAS: " + " / ".join(_txt(x) for x in r["pistas"]))
    if isinstance(r.get("outros"), list):
        linhas.append(u"  OUTROS (erradas): " + " | ".join(_txt(x) for x in r["outros"]))
    # digitar-numero / conta: mostra a operação e o resultado declarado
    if r.get("op") and (r.get("a") is not None) and (r.get("b") is not None):
        linhas.append(u"  CONTA: %s %s %s = %s" % (r.get("a"), r.get("op"), r.get("b"), r.get("resp")))
    if not linhas:
        # dump enxuto do resto (sem img/técnicos) p/ o revisor ver algo
        vis = {k: r[k] for k in r
               if k not in ("img", "imgsen", "imgA", "imgB", "seed", "cls", "modo",
                            "selo", "k", "tol", "traco", "min", "max", "num")
               and not isinstance(r[k], (dict, list))}
        if vis:
            linhas.append(u"  " + "; ".join(u"%s=%s" % (k, _limpa(str(v))) for k, v in vis.items()))
    return "\n".join(linhas)


def payload(pasta):
    cam = os.path.join(pasta, "conteudo.json")
    if not os.path.exists(cam):
        return None
    d = json.load(io.open(cam, encoding="utf-8"))
    fases = d.get("fases", []) if isinstance(d, dict) else []
    out = []
    out.append(u"ATIVIDADE: %s" % _limpa(str(d.get("titulo", pasta))))
    out.append(u"ANO/DISCIPLINA: %s" % _limpa(str(d.get("sub", d.get("ano", "")))))
    obj = d.get("conceitos", {})
    if obj:
        out.append(u"OBJETIVOS: " + " | ".join(_limpa(str(v)) for v in obj.values()))
    out.append(u"=" * 60)
    for i, f in enumerate(fases):
        if not isinstance(f, dict):
            continue
        out.append(u"FASE %d [%s] — %s" % (i + 1, f.get("mec", "?"), _limpa(str(f.get("selo", "")))))
        if f.get("enunciado"):
            out.append(u"  ENUNCIADO: " + _txt(f["enunciado"]))
        if f.get("dica"):
            out.append(u"  DICA GERAL: " + _txt(f["dica"]))
        dados = f.get("dados")
        if isinstance(dados, list):
            for j, r in enumerate(dados):
                bloco = _rodada_txt(r)
                if bloco.strip():
                    out.append(u"  — rodada %d —" % (j + 1))
                    out.append(bloco)
        out.append(u"-" * 40)
    return "\n".join(out)


def payload_json(pasta):
    cam = os.path.join(pasta, "conteudo.json")
    if not os.path.exists(cam):
        return None
    d = json.load(io.open(cam, encoding="utf-8"))
    fases = []
    for i, f in enumerate(d.get("fases", []) if isinstance(d, dict) else []):
        if not isinstance(f, dict):
            continue
        rod = []
        for r in (f.get("dados") or []):
            if not isinstance(r, dict):
                rod.append({"item": _txt(r)})
                continue
            item = {}
            cer = _campo(r, _CERTAS)
            if cer is not None:
                item["certa"] = [_txt(x) for x in cer] if isinstance(cer, list) else _txt(cer)
            err = _campo(r, _ERRADAS)
            if err is not None:
                item["erradas"] = [_txt(x) for x in (err if isinstance(err, list) else [err])]
            dic = _campo(r, _DICAS)
            if dic is not None:
                item["dica"] = [_txt(x) for x in (dic if isinstance(dic, list) else [dic])]
            for k in ("p", "enun", "pergunta", "ante", "bal", "fala"):
                if r.get(k):
                    item["pergunta"] = _txt(r[k])
                    break
            if item:
                rod.append(item)
        fases.append({"n": i + 1, "mec": f.get("mec"), "selo": _limpa(str(f.get("selo", ""))),
                      "enunciado": _txt(f.get("enunciado", "")), "dica": _txt(f.get("dica", "")),
                      "rodadas": rod})
    return {"titulo": _limpa(str(d.get("titulo", ""))),
            "ano": _limpa(str(d.get("sub", d.get("ano", "")))),
            "fases": fases}


def main():
    if len(sys.argv) < 2:
        print(u"uso: sentido.py <pasta> [--json] [--out FILE]")
        return 2
    pasta = sys.argv[1].rstrip("/")
    if "--json" in sys.argv:
        p = payload_json(pasta)
        if p is None:
            print(u"%s -> sem conteudo.json (nada a ler de sentido)." % pasta)
            return 2
        texto = json.dumps(p, ensure_ascii=False, indent=1)
    else:
        texto = payload(pasta)
        if texto is None:
            print(u"%s -> sem conteudo.json (nada a ler de sentido)." % pasta)
            return 2
    if "--out" in sys.argv:
        fn = sys.argv[sys.argv.index("--out") + 1]
        io.open(fn, "w", encoding="utf-8").write(texto)
        print(u"payload de sentido escrito em %s (%d fase(s))." % (fn, texto.count("FASE ")))
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
