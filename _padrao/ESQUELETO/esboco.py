#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""O ESBOÇO — o `conteudo.json` já nasce no formato certo, com 32 fases.

Cobrança do Marcos (ago/2026): *"otimize tudo, o processo precisa ser bem mais
ágil e rápido e SEM ERROS"* — e a pergunta que veio junto: *"mas por que está
saindo erro se a fábrica de interatividades entrega tudo pronto?"*.

**A fábrica de peças não está errando** — as 74 passam a bancada. Os erros
apareceram na JUNTA entre o conteúdo e a peça, e todos do mesmo tipo:

  · campo com o nome trocado (`{i, como}` onde a peça lê `{sp, acao}`)
    → a fase abriu, anunciou "0 diferenças" e se deu por concluída sozinha;
  · gaveta meia-cheia (as gavetas preenchidas e as fichas no exemplo)
    → as chaves deixaram de casar, nenhuma ficha podia ser posta, criança presa;
  · palavra de 17 letras numa grade de 8 → 857 erros de JS.

Os portões pegam os três. Mas portão avisa **depois** que se errou — e o certo é
**não conseguir errar**. É o que este arquivo faz: escreve o `conteudo.json`
inteiro com a estrutura de cada mecânica **copiada do exemplo da própria peça**,
com todas as gavetas presentes e os textos marcados com `«...»` para trocar.

    esboço (segundos)  →  eu troco só as PALAVRAS  →  montar  →  colher  →  banca

Não há campo para errar o nome, nem gaveta para esquecer: elas já vêm.
E o tempo do trabalho passa a ser o que ele deveria ser — pensar o conteúdo.

Uso:
  python3 _padrao/ESQUELETO/esboco.py <pasta> --ano "3º ano" --prefixo abc \\
        --titulo "O Nome da Atividade" --mascote nino
  (sem --mecs, ele escolhe um leque que já passa nas regras do montador)
"""
import io
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))

# ⚠️ o leque padrão: gestos BEM diferentes entre si, na ordem em que costumam
#    encaixar numa aula (do reconhecer ao produzir). Quem escreve troca à
#    vontade — mas partindo daqui já se cumpre o teto de 40% e a variedade.
LEQUE = ["escolher", "completar", "memoria", "caca-palavras", "ordenar",
         "ligar", "classificar", "arrastar-lugar", "cruzadinha", "forca",
         "digitar", "sombra", "labirinto", "pintar-desenho", "relogio",
         "sete-erros"]

SELOS = {"escolher": "ESCOLHA", "completar": "COMPLETE", "memoria": "MEMORIA",
         "caca-palavras": "CACA-PALAVRAS", "ordenar": "COLOQUE EM ORDEM",
         "ligar": "LIGUE", "classificar": "SEPARE", "arrastar-lugar": "ARRASTE",
         "cruzadinha": "CRUZADINHA", "forca": "FORCA", "digitar": "ESCREVA",
         "sombra": "A SOMBRA", "labirinto": "O CAMINHO",
         "pintar-desenho": "PINTE", "relogio": "QUE HORAS SAO",
         "sete-erros": "ACHE O QUE MUDOU"}


def literal(crua):
    u"""lê um literal JS (o exemplo da peça) e devolve o valor."""
    if not crua:
        return None
    try:
        r = subprocess.run(["node", "-e",
                            "console.log(JSON.stringify((%s)))" % crua],
                           capture_output=True, text=True, timeout=15)
        return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None
    except Exception:
        return None


def marca(v, prof=0):
    u"""troca os TEXTOS por `«trocar»`, mantendo a ESTRUTURA e as CHAVES.

    ⚠️ o que NÃO se marca: as chaves de ligação (`k`, `alvo`, `sp`) e os
    números. Marcar `k:"raiz"` e deixar `alvo:"raiz"` foi exatamente o que
    deixou a fase de classificar sem saída no teste — as duas pontas têm que
    continuar casando."""
    if isinstance(v, dict):
        return dict((k, v[k] if k in LIGACAO else marca(v[k], prof + 1))
                    for k in v)
    if isinstance(v, list):
        return [marca(x, prof + 1) for x in v]
    if isinstance(v, str):
        letras = sum(1 for c in v if c.isalpha())
        if letras < 2 or "<svg" in v or v.startswith("#"):
            return v
        return u"«%s»" % v
    return v


# chaves que LIGAM uma gaveta à outra: mexer nelas quebra o par
LIGACAO = set("k alvo sp i id ref para de".split())


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    pasta = sys.argv[1].rstrip("/")

    def op(nome, padrao=""):
        return (sys.argv[sys.argv.index(nome) + 1]
                if nome in sys.argv and len(sys.argv) > sys.argv.index(nome) + 1
                else padrao)

    ano = op("--ano", u"3º ano")
    pre = op("--prefixo", "abc")
    titulo = op("--titulo", u"«Título da atividade»")
    mascote = op("--mascote", "mascote")
    mecs = op("--mecs", "").split(",") if op("--mecs") else LEQUE
    quantas = int(op("--fases", "32"))

    g = json.load(io.open(os.path.join(AQUI, "pecas.json"),
                          encoding="utf-8"))["gavetas"]
    faltam = [m for m in mecs if m not in g]
    if faltam:
        print(u"mecanica(s) que nao existem na oficina: %s" % ", ".join(faltam))
        return 2

    # ⚠️ o numero de fases MANDA, nao o tamanho do leque. Antes eram sempre duas
    #    voltas do leque: com 12 mecanicas saiam 24 fases, e o combinado sao 32.
    #    Agora o leque gira ate completar — e girando ele nunca repete colado.
    ordem = [mecs[i % len(mecs)] for i in range(quantas)]
    fases, avisos = [], []
    if True:
        for i, m in enumerate(ordem):
            k = i % len(mecs)
            info = g[m]
            ident = "f%02d" % (i + 1)
            selo = SELOS.get(m, m.upper())
            if i == quantas // 2 - 1:         # o AQUECIMENTO cai no MEIO
                ident, selo = "aquecimento", "AQUECIMENTO"
            f = {"id": ident, "mec": m, "selo": selo,
                 "enunciado": u"«o que a criança tem que fazer aqui»",
                 "dica": u"«o 1º degrau do andaime: onde olhar»",
                 "conceito": u"objetivo%d" % (k + 1)}
            # ⭐ TODAS as gavetas desta mecânica, já com a estrutura certa
            principal = info.get("var")
            ex = literal(info.get("exemplo"))
            if ex is not None:
                f["dados"] = marca(ex)
            outras = [v for v in (info.get("gavetas") or []) if v != principal]
            if outras:
                extra = {}
                for v in outras:
                    val = literal((info.get("exemplos") or {}).get(v))
                    if val is not None:
                        extra[v] = marca(val)
                if extra:
                    f["dadosExtra"] = extra
            if not info.get("var"):
                avisos.append(u"%s: a peca '%s' nao tem gaveta — a fase vai rodar "
                              u"com o conteudo de exemplo dela" % (ident, m))
            fases.append(f)

    c = {"titulo": titulo,
         "sub": u"«Disciplina · %s · «o assunto»»" % ano,
         "ano": ano, "prefixo": pre, "mascote": mascote,
         "mascoteNome": mascote.capitalize(), "crachas": 6,
         "fundo": "%s_fundo.jpg" % pre,
         "convite": u"<b>«Quem vai ...»</b> hoje?",
         "abertura": u"«o problema que faz a criança QUERER saber — o conceito "
                     u"vem por último (EDUVERSE-FILOSOFIA.md)»",
         "fim": u"«o que o mascote diz na medalha, com um gancho de curiosidade»",
         # ⭐ O CURRICULO ENTRA NO ARQUIVO, NAO NA MINHA MEMORIA (ordem do
         #    Marcos, ago/2026: "é preciso averiguar o currículo de Blumenau e
         #    passar pelo crivo do pedagogo especialista"). Estava escrito nos
         #    manuais e o esqueleto nao cobrava — e regra escrita nao e regra
         #    cumprida. Agora cada objetivo carrega A HABILIDADE que ele serve,
         #    copiada do `_curriculo/blumenau.txt`, e o montador RECUSA-SE a
         #    gerar enquanto estiver por preencher.
         "mesa": u"«quem sentou na mesa: até o 5º ano manda o PEDAGOGO; do 6º ao "
                 u"9º, o ESPECIALISTA DA DISCIPLINA (ver _padrao/RECEITA.md)»",
         "conceitos": dict((u"objetivo%d" % (k + 1),
                            u"«nome em linguagem de criança»")
                           for k in range(len(mecs))),
         "curriculo": dict((u"objetivo%d" % (k + 1),
                            u"«a habilidade do currículo de Blumenau/BNCC que "
                            u"este objetivo serve — copiada, não resumida»")
                           for k in range(len(mecs))),
         "fases": fases}

    if not os.path.isdir(pasta):
        os.makedirs(pasta)
    cam = os.path.join(pasta, "conteudo.json")
    if os.path.exists(cam):
        print(u"ja existe %s — nao sobrescrevo trabalho feito" % cam)
        return 1
    io.open(cam, "w", encoding="utf-8").write(
        json.dumps(c, ensure_ascii=False, indent=1))
    for a in avisos:
        print(u"   aviso: %s" % a)
    print(u"ESBOCO — %s" % cam)
    print(u"   %d fases | %d mecanicas | todas as gavetas ja no formato certo"
          % (len(fases), len(mecs)))
    print(u"   agora e trocar so o que esta entre «» — a estrutura ja esta certa")
    print(u"   ⚠️ ANTES DAS FASES: preencha `mesa` e `curriculo` (o montador cobra).")
    print(u"      o currículo de Blumenau esta em _curriculo/blumenau.txt (2,1 MB)")
    print(u"   depois: montar.py -> colher.py -> montar.py -> auditar.sh")
    return 0


if __name__ == "__main__":
    sys.exit(main())
