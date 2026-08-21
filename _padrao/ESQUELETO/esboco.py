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
        # ⚠️⚠️ LICAO PAGA (ago/2026): DESENHO NAO E TEXTO. As linhas do
        #    labirinto sao um MAPA em letras — "S..#." e uma fileira de cinco
        #    casas: saida, chao, chao, parede, chao. Marcando como texto, a
        #    linha virava «.#X.F»: SETE casas em vez de cinco, a grade
        #    desalinhava, o caminho ate a estrela deixava de existir e a fase
        #    ficava sem saida — sem erro de JS, sem aviso nenhum. O jogador
        #    automatico ficou PRESO ali, e so o descobrimos porque ele passou a
        #    jogar a atividade inteira.
        #    Regra: string feita SO de simbolos de mapa (e curta) e estrutura,
        #    nao redacao. Quem troca um labirinto troca o mapa inteiro.
        if len(v) <= 16 and set(v) <= set(u"SFX#.oO*+-|_ "):
            return v
        return u"«%s»" % v
    return v


# chaves que LIGAM uma gaveta à outra: mexer nelas quebra o par
LIGACAO = set("k alvo sp i id ref para de".split())

# ⚠️ gaveta que só vale quando OUTRA gaveta tem um certo valor. Tem que ser a
#    MESMA regra do `montar.py` (`DEPENDE`), senão o esboço volta a nascer
#    reprovado por ele. Se um dia crescer, o certo é as duas lerem de um lugar
#    só — por ora são duas linhas, e o comentário aqui e lá aponta uma para a outra.
DEPENDE = {("caca-palavras", "PALDEF"): ("MODO", "definicoes")}


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

    # ⚠️⚠️ LICAO PAGA (ago/2026) — O ESBOCO NASCIA REPROVADO PELA PROPRIA BANCA.
    #    O objetivo saia do INDICE DA MECANICA (`k = i % len(mecs)`): com 16
    #    mecanicas e 32 fases, cada objetivo ficava com exatamente DUAS fases —
    #    e as duas da MESMA mecanica, porque o leque gira no mesmo passo. Ou
    #    seja, o pior arranjo possivel: 2 fases (o minimo da casa e 3) e UM
    #    gesto so ("quem nao entende por esse caminho nao tem outro").
    #    Medido: 32 problemas de cobertura numa atividade recem-esbocada, sem
    #    ninguem ter escrito uma linha. O professor perderia a manha
    #    consertando uma estrutura que nao foi ele que montou.
    #    O conserto: objetivo por BLOCO de fases consecutivas. Como o leque
    #    gira, um bloco de 4 traz 4 mecanicas DIFERENTES — 4 fases e 4 gestos
    #    por objetivo, com folga sobre o minimo.
    POR_OBJETIVO = 4
    nobj = max(1, (quantas + POR_OBJETIVO - 1) // POR_OBJETIVO)
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
                 "conceito": u"objetivo%d" % (min(i // POR_OBJETIVO, nobj - 1) + 1)}
            # ⭐ TODAS as gavetas desta mecânica, já com a estrutura certa
            principal = info.get("var")
            ex = literal(info.get("exemplo"))
            if ex is not None:
                f["dados"] = marca(ex)
            outras = [v for v in (info.get("gavetas") or []) if v != principal]
            if outras:
                exs = info.get("exemplos") or {}
                tecnicas = info.get("tecnicas") or []
                extra = {}
                for v in outras:
                    # ⚠️ LICAO PAGA (ago/2026, bussola travando o jogador): as
                    #    TECNICAS (marcadas /*TECNICA*/) sao CONFIG com default
                    #    legitimo — direcoes cardeais, setas, tipos de rodada. O
                    #    esboco NAO pode emiti-las como «placeholder»: `["«NORTE»"]`
                    #    injetado quebra o casamento `rumo===alvoDir` (nunca casa)
                    #    e `tipo:"«achalugar»"` manda a rodada para o galho errado.
                    #    Tecnica fica no default; o autor liga so se quiser, com
                    #    valor REAL.
                    if v in tecnicas:
                        continue
                    # ⚠️⚠️ LICAO PAGA (ago/2026): O ESBOCO NASCIA REPROVADO PELO
                    #    PROPRIO MONTADOR. O exemplo do caca-palavras traz a
                    #    gaveta `PALDEF` (as definicoes) JUNTO com `MODO="lista"`
                    #    — e a peca so olha `PALDEF` quando `MODO="definicoes"`.
                    #    O montador tem um guarda (`DEPENDE`) que reprova essa
                    #    combinacao; copiando o exemplo cru, o esboco caia nele
                    #    (f04 e f20 da prova da esteira). Agora o esboco conhece
                    #    a MESMA regra e nao emite a gaveta dependente quando a
                    #    condicao dela nao bate — o esboco sai montavel de nascenca.
                    dep = DEPENDE.get((m, v))
                    if dep:
                        dep_gav, dep_val = dep
                        atual = literal(exs.get(dep_gav))
                        if atual != dep_val:
                            continue
                    val = literal(exs.get(v))
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
         # ⚠️ `.png` e nao `.jpg`: o gerador de imagem salva PNG, e o motor
         #    monta `url(img/<fundo>)` LITERAL. Com a extensao errada o fundo
         #    da atividade inteira simplesmente nao carrega — sem erro, sem
         #    aviso, so a tela lisa. Duas atividades foram ao ar assim.
         "fundo": "%s_fundo.png" % pre,
         # ⭐ AS DUAS LINHAS QUE FAZEM O PROMPT DA FIGURA FICAR BOM.
         #    O `prompts.py` monta o pedido de cada desenho a partir daqui; sem
         #    elas ele cai no titulo, que serve mas sai generico ("a friendly
         #    scene"). Escrever estas duas linhas leva um minuto e e o que
         #    separa a figura irma das outras da figura estranha.
         "arte": {
             "cenario": u"«o lugar onde a atividade acontece, em uma linha: "
                        u"'a small sign painter workshop in a german-style "
                        u"street in Blumenau'»",
             "mascote": u"«quem e o mascote, em uma linha: 'a cheerful young "
                        u"woman sign painter with denim overalls, a blue cap "
                        u"and a paintbrush in her hand'»",
         },
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
                           for k in range(nobj)),
         "curriculo": dict((u"objetivo%d" % (k + 1),
                            u"«a habilidade do currículo de Blumenau/BNCC que "
                            u"este objetivo serve — copiada, não resumida»")
                           for k in range(nobj)),
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
