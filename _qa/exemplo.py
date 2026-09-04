# -*- coding: utf-8 -*-
u"""
PORTÃO DO TEXTO DE EXEMPLO — "a criança está lendo sobre a PLANTA numa atividade
de DIVISÃO?"

NASCEU MONTANDO A GINCANA (set/2026). O montador avisou:

    aviso: fase 13, mecanica 'escolher': voce preencheu 'QZ' mas deixou
    'TITULO' e 'FECHO' com o conteudo de EXEMPLO.

Fui ver o que era esse conteúdo de exemplo e achei, dentro de uma atividade de
divisão do 4º ano, a frase que fecha a fase:

    var FECHO="Você já conhece as partes da planta!";

A criança do 4º ano reparte bolas entre equipes, acerta tudo, e o jogo responde
que ela conhece as partes da planta. **E o mesmo estava na Expedição da Divisão
do 5º ano, que já está no ar** — junto de mais alguns.

⚠️ O QUE FAZ ESTE PORTÃO DIFÍCIL, e por que ele não é um `grep`: nem todo texto
de exemplo é defeito. A maioria é a VOZ GENÉRICA da mecânica e está certa em
qualquer atividade:

    "Cada ficha vai numa gaveta. Toque na ficha e depois na gaveta."   ← certo
    "Digite quanto dá."                                               ← certo
    "Você já conhece as partes da planta!"                            ← DEFEITO

A diferença não é o texto ser de exemplo: é ele falar de um ASSUNTO que esta
atividade não tem. Um `grep` cego reprovaria as três e ensinaria a ignorar o
portão — que é o pior que pode acontecer com um portão.

A REGRA, então, em duas perguntas — e as DUAS têm de dar sim:

  1. a frase cita uma palavra do ASSUNTO DO PRÓPRIO EXEMPLO? (o assunto está
     escrito ali do lado: é o vetor de DADOS de exemplo daquela mecânica — no
     `escolher` é o quiz da planta, com raiz, folha, terra);
  2. essa palavra está AUSENTE do `conteudo.json` desta atividade?

Só aí é resto de exemplo. "PARTES DA PLANTA" cita `planta`, que está no quiz de
exemplo e não está na Gincana: reprova. "Você calculou todas as contas!" não
cita nada do assunto do exemplo — é a voz genérica da mecânica: passa.

⚠️ A PRIMEIRA VERSÃO DESTE PORTÃO ERRAVA AQUI, e vale registrar: eu comparava
TODA palavra de conteúdo da frase com o vocabulário da atividade, e ele acusou
"calculou", "ligou", "conhece" e até "numa" — verbos e palavrinhas que nenhuma
atividade escreve no `conteudo.json`. Cinco acusações, duas verdadeiras. Portão
que acusa inocente ensina a ignorar portão.

Uso:  python3 _qa/exemplo.py <pasta>          (ex.: _gincana)
Sai 0 se limpo, 1 se há texto de exemplo fora de assunto, 2 se não deu para medir.
"""
import json, os, re, sys, unicodedata

PECAS = "_padrao/ESQUELETO/pecas.json"   # a documentacao: o ASSUNTO do exemplo
MOTOR = "_padrao/ESQUELETO/pecas.js"     # o motor: o PADRAO que a crianca recebe

# gavetas que são TABELA DE VOCABULÁRIO (nomes de números, de operadores).
# Não são texto que a criança lê como conteúdo — ficam de fora da medição.
TABELAS = {"UN", "DZ", "UNM", "NOMEDIG", "OPNOME", "PEDACOS", "MAXN"}

# palavras da INTERFACE: aparecem em qualquer atividade e não denunciam assunto
INTERFACE = set(u"""
toque toca clique arraste arrasta leia ler diga fala falar conte contar ache
achar veja olhe escolha escolher digite digitar monte montar ponha por
ficha fichas gaveta gavetas peca pecas carta cartas caixa caixas botao
palavra palavras frase frases letra letras numero numeros conta contas
resposta respostas certa certo errada errado depois antes inteira inteiro
cada todos todas todo toda mesmo mesma outra outro para pela pelo com sem
uma dois duas tres quatro cinco seis sete oito nove dez
voce agora aqui ali isso essa esse este esta muito bem parabens
falta faltando lugar dela dele seu sua qual quais quando onde
devagar rapido primeiro segundo ultima ultimo
desenho desenhos figura figuras imagem som sons cena tela
leve leva empurre empurra puxe solte junte separe risque marque
""".split())


def sem_acento(s):
    return u"".join(c for c in unicodedata.normalize("NFD", s)
                    if unicodedata.category(c) != "Mn")


def palavras(txt):
    t = sem_acento(re.sub(r"<[^>]+>", " ", txt)).lower()
    t = re.sub(r"&[a-z]+;|&#\d+;", " ", t)
    return set(w for w in re.findall(r"[a-z]{4,}", t) if w not in INTERFACE)


def frases_de_exemplo():
    u"""(mecanica.gaveta -> (frase PADRAO de hoje, assunto do exemplo))

    ⚠️ DE ONDE VEM O PADRÃO — o terceiro erro deste portão, e o mais sorrateiro:
    eu lia a frase do `pecas.json`, que é a DOCUMENTAÇÃO (o exemplo do quiz da
    planta, que deve continuar lá para ensinar o formato). Só que o valor que a
    criança recebe quando a fase não preenche a gaveta está no `pecas.js` — é o
    `var FECHO="...";` de dentro do bloco daquela peça. Depois de eu NEUTRALIZAR
    o padrão no motor, o portão continuava reprovando cinco atividades já
    consertadas, porque estava lendo o arquivo errado. Agora ele lê o padrão de
    verdade, no motor; o assunto do exemplo continua vindo do `pecas.json`."""
    d = json.load(open(PECAS, encoding="utf-8"))["gavetas"]
    js = open(MOTOR, encoding="utf-8", errors="replace").read()
    # o motor em blocos, uma peça por bloco
    blocos = {}
    partes = re.split(r"/\* ==== PECA: ([\w-]+) ==== \*/", js)
    for i in range(1, len(partes) - 1, 2):
        blocos[partes[i]] = partes[i + 1]

    out = {}
    for mec, g in d.items():
        ex = g.get("exemplos") or {}
        assunto = set()
        for k, v in ex.items():
            if k in TABELAS or not isinstance(v, str):
                continue
            if v.strip().startswith("[") or v.strip().startswith("{"):
                assunto |= palavras(v)          # vetor de DADOS = o assunto
        bloco = blocos.get(mec)
        if not bloco or not assunto:
            continue
        for k in ex:
            if k in TABELAS:
                continue
            m = re.search(r'var\s+%s\s*=\s*"((?:[^"\\]|\\.)*)"\s*;' % re.escape(k), bloco)
            if not m:
                continue                        # gaveta nao e string com padrao
            s = m.group(1)
            if len(s) < 12 or " " not in s:
                if not (s.isupper() and len(s) >= 8):
                    continue
            out[mec + "." + k] = (s, assunto)
    return out


def confere(pasta):
    pasta = pasta.rstrip("/")
    html = os.path.join(pasta, "index.html")
    cont = os.path.join(pasta, "conteudo.json")
    if not os.path.exists(html) or not os.path.exists(cont):
        print(u"NAO MEDI: %s precisa de index.html e conteudo.json" % pasta)
        return 2
    if not (os.path.exists(PECAS) and os.path.exists(MOTOR)):
        print(u"NAO MEDI: nao achei %s / %s" % (PECAS, MOTOR))
        return 2

    bruto = open(cont, encoding="utf-8", errors="replace").read()
    meu = palavras(bruto)          # o vocabulário DESTA atividade
    dados = json.loads(bruto)

    # ⚠️⚠️ A LIÇÃO QUE MUDOU ESTE PORTÃO INTEIRO: "estar no arquivo" NÃO é "chegar
    #    à criança". A primeira versão procurava a frase no `index.html` e
    #    acusou a Central de Entregas por `PERGUNTA = "Por que a feira mudou de
    #    lugar?"`. Fui conferir e o `conteudo.json` dela estava CERTO ("Por que a
    #    ponte foi fechada?"): a frase da feira é só o valor PADRÃO declarado no
    #    motor, trocado em tempo de execução pelo que a fase manda. Acusação de
    #    inocente, e das piores — a correção estava feita e o portão insistia.
    #    Então a pergunta certa não é "a frase está no arquivo?", e sim: **esta
    #    FASE preencheu essa gaveta?** Se preencheu, o padrão nunca aparece. Se
    #    não preencheu, o padrão é o que a criança lê — e aí sim vale medir.
    frases = frases_de_exemplo()
    ruins, ok, medidas = [], 0, 0
    for f in dados.get("fases", []):
        mec = f.get("mec")
        dou = set((f.get("dadosExtra") or {}).keys())
        for onde, (frase, assunto) in frases.items():
            m, gav = onde.split(".", 1)
            if m != mec or gav in dou:
                continue           # outra mecânica, ou a fase preencheu
            medidas += 1
            fora = (palavras(frase) & assunto) - meu
            if fora:
                ruins.append((frase, u"fase %s · %s" % (f.get("id"), onde), sorted(fora)))
            else:
                ok += 1
    # um mesmo padrão em várias fases é UM defeito, não vários
    vistos, unicos = set(), []
    for frase, onde, fora in ruins:
        if frase in vistos:
            continue
        vistos.add(frase)
        unicos.append((frase, onde, fora))
    ruins = unicos

    if not medidas:
        print(u"%s -> exemplo ok: nenhuma fase deixou gaveta de texto no padrao." % pasta)
        return 0

    if ruins:
        print(u"%s -> %d texto(s) de EXEMPLO chegando a crianca com assunto que "
              u"esta atividade nao tem (de %d gaveta(s) no padrao):"
              % (pasta, len(ruins), medidas))
        for frase, onde, fora in ruins[:10]:
            print(u'    ✗ %s diz "%s"' % (onde, frase[:78]))
            print(u"       assunto que nao existe aqui: %s" % u", ".join(fora[:6]))
        print(u"   Cura: preencher essa gaveta no `dadosExtra` da fase, no")
        print(u"   conteudo.json. Sem isso a crianca le o assunto do EXEMPLO.")
        return 1

    print(u"%s -> exemplo ok: %d gaveta(s) de texto ficaram no padrao do motor, "
          u"todas com a voz GENERICA da mecanica (nenhuma entrega assunto de "
          u"outra atividade)." % (pasta, ok))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/exemplo.py <pasta>")
        sys.exit(2)
    sys.exit(confere(sys.argv[1]))
