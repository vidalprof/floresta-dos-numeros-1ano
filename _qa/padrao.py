# -*- coding: utf-8 -*-
# ============================================================
#  AUDITOR DO PADRÃO DA CASA — "didática, ilustrada, sonora e variada?"
#
#  Nasceu de uma frase do Marcos (ago/2026), dita quando já estávamos na
#  sétima atividade: *"ela tem que ser bem didática progressiva didaticamente,
#  bem ilustrada, sonora lembra? isso deve ser guardado para todas as
#  atividades a serem produzidas"*. Estava no costume, não estava escrito em
#  lugar nenhum — e o que não está escrito, um dia sai errado.
#
#  Ele já tinha cobrado o quarto pilar antes, na Legenda: *"tem muita dinâmica
#  parecida... temos um leque bem grande de interatividade"*. Lá a medição
#  mostrou 8 das 19 fases com o MESMO gesto. Por isso este auditor conta
#  GESTO, não conteúdo: duas fases podem ensinar coisas diferentes e mesmo
#  assim ser, para a criança, a mesma tela pela terceira vez.
#
#  Reprova quando:
#    1. um único gesto passa de 40% das fases (atividade repetitiva);
#    2. alguma fase é MUDA (nenhuma narração) — o padrão é toda tela falada;
#    3. sobram menos de 4 gestos diferentes na atividade inteira.
#  Avisa (sem reprovar) sobre fases sem ilustração — há fases que são texto
#  por natureza (caça-palavras, cruzadinha).
#
#  Uso: python3 _qa/padrao.py _historia/index.html
# ============================================================
import os, re, sys

alvo = sys.argv[1] if len(sys.argv) > 1 else ""
if not alvo:
    print("uso: python3 _qa/padrao.py <arquivo.html>")
    sys.exit(2)
html = open(alvo, encoding="utf-8").read()
js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))

# ⚠️ COMENTÁRIO NÃO É CÓDIGO. Este portão acha as fases procurando funções que
#    chamam `limpa()` — e passou a acusar a função `falar()` como "fase muda"
#    porque o comentário DELA explica a regra escrevendo `limpa()` no meio do
#    texto. Um portão que lê comentário reprova quem documenta bem, que é
#    exatamente o contrário do que a casa quer. Fora os comentários, então —
#    preservando as quebras de linha, que o resto da análise usa.
def _sem_comentario(t):
    t = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), t, flags=re.S)
    return re.sub(r"(?m)^(\s*)//.*$", r"\1", t)

js = _sem_comentario(js)

# ---- as telas: mesma regra do _qa/fluxo.py (funcao que chama limpa())
def corpo_de(nome, texto, pos):
    j = texto.find("{", pos)
    k, d = j, 0
    while k < len(texto):
        if texto[k] == "{":
            d += 1
        elif texto[k] == "}":
            d -= 1
            if d == 0:
                break
        k += 1
    return texto[j:k]

telas = []
for m in re.finditer(r"^function\s+([A-Za-z_$][\w$]*)\s*\(", js, re.M):
    c = corpo_de(m.group(1), js, m.end())
    if re.search(r"\blimpa\(\)", c):
        telas.append((m.group(1), c))

# telas de serviço não contam como fase de conteúdo
SERVICO = ("telaCapa", "telaQuem", "telaMestre", "telaPainel", "telaFim")
def so_narrativa(c):
    """tela de historia: fala, mostra, e tem SO o botao de seguir.
       ⚠️ contar `.onclick=` nao basta: uma fase que monta 8 botoes dentro de um
       `for` tem UMA ocorrencia de onclick no texto e parecia narrativa. A marca
       de verdade da tela narrativa e ter o botao grande de seguir e mais nada:
       nada de campo de escrever, nada de deslizar, nada de alvo em laco."""
    if re.search(r'type\s*=\s*"text"|el\("textarea"|oninput|onchange|type="range"', c):
        return False
    if not re.search(r'el\("button","btn', c):
        return False
    return len(re.findall(r"\.onclick\s*=", c)) <= 1

fases = [(n, c) for n, c in telas
         if not any(n.lower().startswith(s.lower()) for s in SERVICO)
         and not n.lower().endswith("fim")]
narrativas = [n for n, c in fases if so_narrativa(c)]
fases = [(n, c) for n, c in fases if not so_narrativa(c)]

# ---- que GESTO cada fase pede da criança
GESTOS = [
    ("digitar",    r'type\s*=\s*"text"|el\("input"|"campo"'),
    ("ordenar",    r'\bprox\b.*?ordem|ordem.*?\bprox\b'),
    ("deslizar",   r'type\s*=\s*"range"|"termo"'),
    ("arrastar",   r'addEventListener\("touchmove"'),
    ("pintar",     r'"pal pint|pint "|marcaTexto|"paragrafo"|"tinta mira|"tcor '),
    # ⚠️ montar vem ANTES de achar: a fase que monta a planta da sala tem os
    #    dois sinais (peca + alvo na cena) e o gesto dela e MONTAR.
    ("montar",     r'data-vaga'),
    ("achar",      r'"achado mira"|"achado"|"mira vazio'),
    ("orientar",   r'"bussola"|"vento "'),
    ("coordenada", r'"quadric"|"qcel"'),
    ("memoria",    r'"mcarta"'),
    ("forca",      r'"forca"|"letrasfc"|"boneco"|forcaErros'),
    ("simulador",  r'"simul"|"medidor"|regula\(|"linhatempo"'),
    ("grade",      r'el\("div","cel"|"cquad"|"pchip"'),
    ("ligar",      r'el\("div","lig"'),
    ("classificar", r'el\("div","cx"|el\("div","bin"|"gav"'),
    ("montar",     r'el\("div","vaga|"tvaga"|"slot"|el\("div","tec"|"fichaP"'),
    ("virar",      r'el\("div","carta|"vira"'),
    ("explorar",   r'"filtro"|style\.filter|"maquina"|"moldura"|"lupafoto"|"lupacx"'),
    ("escolher",   r'el\("div","opt"|el\("div","tecl"|el\("div","pc |"alim"|"rpos"|"gfoto"'),
]

# ⭐ ATIVIDADE MONTADA PELO ESQUELETO: o gesto de cada fase nao se adivinha do
#    codigo — esta ESCRITO na lista `FASES`, no campo `mec`. E a narracao
#    tambem (`vozIntro`). Lendo com a regua antiga, o portao dizia "82% outro"
#    e "16 fases MUDAS" numa atividade com 16 gestos declarados e todas as
#    fases narradas. Aviso falso ensina a ignorar o portao.
_fs = re.findall(r"FASES\s*=\s*(\[.*?\]);", js, re.S)
ESQUELETO = [m for m in
             (re.findall(r'\{"id":\s*"([^"]+)".*?"mec":\s*"([\w-]+)"',
                         max(_fs, key=len)) if _fs else [])]
if ESQUELETO:
    conta, porfase, mudas, semimg = {}, [], [], []
    _lista = max(_fs, key=len)
    for ident, mec in ESQUELETO:
        conta[mec] = conta.get(mec, 0) + 1
        porfase.append((ident, mec))
    _sem_voz = [i for i, _ in ESQUELETO
                if ('"id": "%s"' % i) in _lista
                and ('"vozIntro": "' not in _lista)]
    mudas = _sem_voz
    fases = [(i, "") for i, _ in ESQUELETO]
    print("   esqueleto: gesto e voz lidos da lista FASES (%d fase(s))"
          % len(ESQUELETO))

conta2, porfase2, mudas2, semimg2 = {}, [], [], []
for n, c in ([] if ESQUELETO else fases):
    g = None
    for nome, pad in GESTOS:
        if re.search(pad, c):
            g = nome
            break
    g = g or "outro"
    conta2[g] = conta2.get(g, 0) + 1
    porfase2.append((n, g))
    # ⚠️ `falaDaTela()` e `introEPergunta()` TAMBEM narram (o motor cresceu e o
    #    portao nao sabia). Sem eles na lista, 11 fases faladas eram acusadas de
    #    mudas — e portao que acusa quem esta certo ensina a ignorar portao.
    if not re.search(r"falar\(|depoisDaFala\(|falaDaTela\(|introEPergunta\(", c):
        mudas2.append(n)
    # ⚠️ cenaImg() e a funcao que poe as CENAS grandes (o motor novo usa ela em
    #    quase tudo). Sem ela na lista, o portao avisava "12 fases sem
    #    ilustracao" numa atividade inteira ilustrada — aviso falso ensina a
    #    ignorar o portao, que e o pior que pode acontecer com um portao.
    if not re.search(r"imgEl\(|fotoEl\(|cenaEl\(|cenaImg\(|<img", c):
        semimg2.append(n)
if not ESQUELETO:
    conta, porfase, mudas, semimg = conta2, porfase2, mudas2, semimg2


# ---- 3c) ALTO-FALANTE NAS RESPOSTAS (o terceiro pilar, medido)
#   Regra do Marcos (ago/2026): *"o alto-falante nas respostas também, para
#   ajudar os alunos que não sabem ler"*. O motor faz isso sozinho: o `VOZOK`
#   lista as chaves que TEM mp3 e o observador pendura o botãozinho em cada
#   resposta. Só que o clone traz `var VOZOK={}` VAZIO — e aí o motor não
#   pendura nada, nenhum portão reclama, e a atividade nasce MUDA nas
#   respostas. Foi assim na Terra dos Papagaios: 21 fases prontas, banca
#   aprovada, e nem uma resposta falava. O portão de clone só pega o contrário
#   (voz prometida sem mp3), então o buraco ficava exatamente aqui.
#   ⚠️ Vale só para quem TEM resposta tocável: fase de digitar ou de arrastar
#   sem rótulo não precisa de alto-falante.
RESPOSTA = r'el\("div","opt|el\("div","cx|el\("div","lig|el\("div","gav|' \
           r'el\("div","relcard|el\("div","bin|el\("div","tlin'
semzap = None
if re.search(RESPOSTA, js) and re.search(r"VOZOK", js):
    # ⚠️ o motor DECLARA `var VOZOK={}` vazio e o montador ATRIBUI a lista de
    #    verdade mais adiante. Lendo so a declaracao, o portao acusava de MUDA
    #    uma atividade com 18 alto-falantes gravados. Vale a MAIOR das duas.
    _todas = re.findall(r"VOZOK\s*=\s*\{(.*?)\}\s*;", js, re.S)
    chaves = (type("m", (), {"group": staticmethod(
        lambda i, _v=max(_todas, key=len): _v)}) if _todas else None)
    quantas = len(re.findall(r'"[^"]+"\s*:', chaves.group(1))) if chaves else 0
    if quantas == 0:
        semzap = ("a atividade tem respostas para a crianca TOCAR, mas o `VOZOK` esta "
                  "VAZIO: nenhuma resposta tem alto-falante. Quem ainda nao le escolhe "
                  "pelo desenho, e a atividade vira loteria")
    else:
        print("   alto-falante: %d resposta(s) com voz propria (op_<chave>.mp3)" % quantas)

# ---- 3d) ALTO-FALANTE NA PERGUNTA (o outro metade do pilar 3)
#   O item 3c acima mede o alto-falante das RESPOSTAS. Falta a PERGUNTA — que é
#   o primeiro pedido do Marcos: *"acrescentar um botão de som onde são as
#   perguntas, para ajudar quem não sabe ler"*. O motor pendura esse botão
#   sozinho, com `poeVozPergunta()` chamada pelo observador; sem ela, TODA fase
#   fica sem o botão e nada acusa.
#   Foi o que aconteceu com a Terra dos Papagaios: ela nasceu depois do conserto
#   feito no 3º ano e ficou com **21 fases e zero botão no enunciado**. A banca
#   inteira passou. Só apareceu quando o Marcos perguntou "os botões de ajuda do
#   som funcionam?" e eu fui CLICAR em todos, fase por fase.
sempergunta = None
if re.search(r'el\("div","balao"', js):
    tem_fn = "function poeVozPergunta" in js
    chamada = re.search(r"poeVozPergunta\(\)\s*;", js.replace("function poeVozPergunta()", ""))
    if not tem_fn or not chamada:
        sempergunta = ("nenhuma pergunta tem alto-falante: falta %s. Quem ainda nao le "
                       "depende desse botao para saber o que a tela esta pedindo"
                       % ("a funcao `poeVozPergunta()`" if not tem_fn
                          else "CHAMAR `poeVozPergunta()` no observador (a funcao existe e nunca roda)"))
    else:
        print("   alto-falante: a PERGUNTA tambem tem botao de voz (poeVozPergunta)")

# ---- 4) TECLADO VIRTUAL sem o teclado DE VERDADE
#   Regra permanente do Marcos (ago/2026): *"essa dinâmica de aceitar também o
#   teclado seria interessante registrar para todas as próximas atividades"*.
#   No PC da escola a criança tem teclado na frente e é natural que ela digite;
#   no celular, não tem. As duas portas ficam abertas e levam ao mesmo lugar —
#   nunca só uma. Vale para cruzadinha, forca, monte a palavra e qualquer fase
#   que desenhe letras para tocar.
TECVIRT = r'el\("div","(?:tec|teclafc|letra|tecla)'
semtecla = []
for n, c in fases:
    if re.search(TECVIRT, c) and not re.search(r"onkeydown|addEventListener\(\s*[\"']keydown", c):
        semtecla.append(n)
if not semtecla and re.search(TECVIRT, js):
    print("   teclado: as fases de digitar aceitam a tela E o teclado de verdade")

print("%s -> padrao da casa: %d fase(s) com gesto (+%d tela(s) so de narrativa)"
      % (alvo, len(fases), len(narrativas)))
if not fases:
    print("   (nenhuma fase encontrada)")
    sys.exit(0)

for g in sorted(conta, key=lambda k: -conta[k]):
    pct = 100.0 * conta[g] / len(fases)
    print("   %-12s %2d fase(s)  %4.1f%%" % (g, conta[g], pct))

problemas = []
# ⚠️ este aviso nasce la em cima (lista `semtecla`) mas so pode ser guardado
#    AQUI, depois que `problemas` existe. Na estreia ele estourou um NameError
#    na primeira atividade que tinha teclado na tela sem teclado de verdade —
#    ou seja, o portao morria justo na hora em que tinha algo a dizer.
if semzap:
    problemas.append(semzap)
if sempergunta:
    problemas.append(sempergunta)
if semtecla:
    problemas.append("%d fase(s) com teclado NA TELA que nao aceitam o teclado DE VERDADE "
                     "(no PC da escola a crianca vai digitar): %s"
                     % (len(semtecla), ", ".join(semtecla)))
nomeados = dict((k, v) for k, v in conta.items() if k != "outro")
maior = max(nomeados, key=lambda k: nomeados[k]) if nomeados else "outro"
pct = 100.0 * conta.get(maior, 0) / len(fases)
if conta.get("outro", 0) > len(fases) * 0.3:
    print("   aviso: %d fase(s) que eu nao consegui classificar — o auditor precisa "
          "aprender esses gestos" % conta["outro"])
# ⚠️⚠️ EXCECAO DECLARADA: JOGO DE MECANICA UNICA (ago/2026, ordem do Marcos).
#    Palavras dele, corrigindo a minha primeira entrega do tangram: *"nao e pra
#    ser atividade, e pra ser o jogo do tangran so que didatico"*, *"nao e para
#    ter as diversas interatividades"*.
#    O leque de 4+ gestos e a lei PARA ATIVIDADE, onde a variedade e o que
#    impede o cansaco. Num JOGO a mecanica unica E o jogo — o que segura a
#    crianca e a dificuldade subindo, nao o gesto mudando. Sem esta porta, o
#    portao obrigaria a DESFAZER uma ordem dele, que e o pior que um portao faz.
#    A porta so abre com a declaracao ESCRITA no arquivo (`var TIPO_ATIVIDADE=
#    "jogo"`), e o portao diz em voz alta que ela foi usada — ninguem escapa
#    por acidente.
E_JOGO = re.search(r'var\s+TIPO_ATIVIDADE\s*=\s*"(jogo|criativa|colorir|livre)"', html) is not None
if E_JOGO:
    print("   ⚠️ EXCECAO DECLARADA no arquivo: `TIPO_ATIVIDADE` (jogo/criativa) —")
    print("      mecanica unica autorizada (jogo ou atividade criativa/colorir).")
    print("      O leque de gestos vira AVISO aqui.")
if nomeados and pct > 40.0 and not E_JOGO:
    quais = [n for n, g in porfase if g == maior]
    problemas.append("o gesto \"%s\" e %.0f%% da atividade (%d de %d fases) — para a crianca "
                     "e a mesma tela de novo. Limite: 40%%. Fases: %s"
                     % (maior, pct, conta[maior], len(fases), ", ".join(quais)))
if len(conta) < 4 and not E_JOGO:
    problemas.append("so %d gesto(s) diferentes na atividade inteira (minimo 4) — o leque de "
                     "interatividade da casa e bem maior que isso" % len(conta))
elif len(conta) < 4:
    print("   aviso (jogo): %d gesto(s) — e o esperado num jogo de mecanica unica."
          % len(conta))
# ⚠️⚠️ O PORTAO NAO PODE OBRIGAR A PIORAR (ago/2026). O Marcos decidiu que a
#    voz que fala SOZINHA muda com a idade: do 6o ao 9o ano nada e narrado
#    automaticamente, so o botao de alto-falante — porque "os maiores nao
#    gostam disso a todo momento". Sem esta ressalva, este portao passaria a
#    reprovar toda atividade dos maiores por "fase muda", e o jeito de passar
#    seria desfazer a decisao dele. Portao que briga com a didatica em vez de
#    defende-la e pior que portao nenhum.
#    ⚠️ o alto-falante em TODA resposta continua obrigatorio em TODA idade —
#    isso e outra regra, medida mais abaixo, e nao afrouxa aqui.
_narrar = re.search(r'narrar\s*:\s*"(\w+)"', js)
_narrar = _narrar.group(1) if _narrar else "tudo"
if mudas and _narrar == "manual":
    print("   (atividade de %s: narrar=manual — a voz e por BOTAO, entao fase sem "
          "narracao automatica nao e defeito. %d fase(s) assim.)"
          % ("6o ao 9o ano", len(mudas)))
elif mudas:
    problemas.append("%d fase(s) MUDA(S), sem nenhuma narracao (o padrao e toda tela falada): %s"
                     % (len(mudas), ", ".join(mudas)))
if semimg:
    print("   aviso: %d fase(s) sem ilustracao (confira se e texto por natureza): %s"
          % (len(semimg), ", ".join(semimg)))

if not problemas:
    print("   padrao ok: variada, falada e ilustrada")
    sys.exit(0)
print("   %d PROBLEMA(S) DE PADRAO:" % len(problemas))
for p in problemas:
    print("    - %s" % p)
sys.exit(1)
