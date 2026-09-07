# -*- coding: utf-8 -*-
u"""
UNO dos Números — gera o `falas.json` (TODA frase que o jogo fala) e grava o mapa
`VOZOK` no index.html. Pedido do Marcos (2026-09-07): *"o UNO deveria ser com as vozes
no mesmo padrão das atividades, vozes geradas do Antônio, sem voz do navegador"*.

Como funciona: o jogo monta as frases em tempo real (regra da rodada, cor escolhida,
prefixo do que aconteceu). Aqui enumeramos TODAS as combinações possíveis, limpamos os
emojis do mesmo jeito que o `limparTexto` do jogo e calculamos a MESMA chave (`chaveVoz`
do motor: djb2 em base 36 do texto normalizado). O `entregar.yml` grava
`audio/un_<chave>.mp3` para cada uma (voz do `voz.txt`, Antônio); no jogo, `falar()`
calcula a chave da frase e toca o mp3 — a voz do navegador fica só de reserva.

Uso: python3 _uno345/gerar_falas.py      (depois: commit com [entregar _uno345:uno-dos-numeros-345])
"""
import io, json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.join(AQUI, "index.html")

EMOJI = re.compile(u"[\U0001F000-\U0001FAFF☀-➿⬀-⯿️←-⇿]")


def limpar(t):
    return re.sub(r"\s+", " ", EMOJI.sub("", t)).strip()


def chave(s):
    s = re.sub(r"\s+", " ", s or "").strip().lower()
    hh = 5381
    for ch in s:
        hh = (hh * 33 + ord(ch)) & 0xFFFFFFFF
    # base 36 (igual ao toString(36) do JS)
    if hh == 0:
        return "0"
    d = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    while hh:
        out = d[hh % 36] + out
        hh //= 36
    return out


def fala_de(t):
    u"""o que a voz DIZ: igual ao texto limpo, so com os sinais que o TTS le errado trocados."""
    return limpar(t).replace("+4", "mais 4").replace("+2", "mais 2")


CORES = ["vermelho", "azul", "verde", "amarelo"]
REGRAS = [
    u"só vale carta PAR", u"só vale carta ÍMPAR", u"só vale carta MAIOR que a da mesa",
    u"a sua carta + a da mesa = 10", u"só vale MÚLTIPLO DE 3", u"só vale MÚLTIPLO DE 5",
    u"só vale o DOBRO da carta da mesa", u"só vale a METADE da carta da mesa",
    u"a soma das duas é MÚLTIPLO DE 3",
]
PREFIXOS = ["", u"O robô pegou uma carta.", u"Você pegou 2 cartas.", u"O robô jogou +4! Você pegou 4 cartas."]
CURTO = {3: u"par e ímpar, maior e menor, e somar 10",
         4: u"múltiplos de 3 e de 5, dobro e metade",
         5: u"múltiplos de 3, dobro, e a soma das duas cartas"}
CAPA = (u"Eu sou o Robô Esperto, e eu penso antes de jogar. Combine a carta pela COR "
        u"ou pelo NÚMERO — e fique de olho na tarja amarela: às vezes a rodada pede "
        u"uma regra a mais, de %s. Quem ficar sem cartas primeiro vence!")
SLIDES = [
    (u"Oi! Eu sou o Robô Esperto!", u"Bem-vindo ao UNO dos Números! Eu não jogo qualquer carta: eu penso antes. Guardo os coringas, ataco quando você está quase ganhando. Vai precisar de estratégia para me vencer!"),
    (u"Nosso objetivo", u"Você e eu começamos com 7 cartas cada um. Vá jogando suas cartas na mesa até a sua mão ficar vazia!"),
    (u"A regra das cores e números", u"Você só pode jogar uma carta da MESMA COR ou do MESMO NÚMERO da carta que está na mesa. Igualzinho!"),
    (u"As cartas que brilham", u"As cartas que você PODE jogar ficam brilhando e crescem quando você passa o dedo. As apagadas, não dá!"),
    (u"Minhas cartas especiais", u"Pular: eu perco a vez. Mais 2: eu pego 2 cartas. Girar: você joga de novo. Cuidado, eu também posso usá-las em você!"),
    (u"As cartas coringa", u"Arco-íris: você escolhe a cor que quiser! Mais 4: você escolhe a cor E eu pego 4 cartas!"),
    (u"A REGRA DA RODADA", u"De vez em quando aparece uma tarja amarela em cima da mesa com uma regra a mais, só para você. Enquanto ela estiver ali, o número da sua carta também precisa obedecer a ela. Vale por uma rodada só — e as cartas especiais nunca ficam bloqueadas."),
    (u"A regra muda conforme o seu ano", u""),
    (u"Como ganhar de mim", u"Se não puder jogar, toque em \"Pegar 1\" para comprar uma carta. Ficou sem cartas? VOCÊ GANHOU! 🎉"),
]

textos = []
fixas = [
    u"Narração ligada!",
    u"Essa não dá! Escolha uma que brilha. 😊",
    u"Você pulou o robô! Jogue de novo. 🚫",
    u"Você pulou o robô! Não tem carta pra jogar, toque em \"Pegar 1\". 🃏",
    u"Você girou o jogo! Jogue de novo. 🔄",
    u"Você girou o jogo! Não tem carta pra jogar, toque em \"Pegar 1\". 🃏",
    u"O robô pegou 2 cartas! 😄",
    u"Boa! Agora é a vez do robô. 🤖",
    u"Você pegou uma carta que dá pra jogar! Toque nela. ✨",
    u"Essa não deu pra jogar. Agora é a vez do robô. 🤖",
    u"O robô te pulou! Ele joga de novo. 🚫",
    u"O robô girou o jogo! Ele joga de novo. 🔄",
    u"🎉 VOCÊ GANHOU! Parabéns! 🎉",
    u"🤖 O robô ganhou! Tente de novo, você consegue! 💪",
]
textos += fixas
for c in CORES:
    textos.append(u"Você escolheu %s e o robô pegou 4 cartas! 🌈➕" % c)
    textos.append(u"Você escolheu %s! 🎨" % c)
    textos.append(u"O robô escolheu %s! 🎨" % c)
for r in REGRAS:
    textos.append(u"Essa serve na cor, mas hoje %s. Olhe as que brilham! 🔎" % r)
for p in PREFIXOS:
    for r in [None] + REGRAS:
        ini = (p + " ") if p else ""
        if r:
            ini += u"Atenção, regra desta rodada: %s! " % r
        textos.append(ini + u"Sua vez! Toque numa carta que brilha. ✨")
        textos.append(ini + u"Você não tem carta para jogar. Toque em \"Pegar 1\" para comprar uma carta! 🃏")
for ano in (3, 4, 5):
    textos.append(u"UNO dos Números, %dº ano. " % ano + CAPA % CURTO[ano])
for tit, txt in SLIDES:
    textos.append(tit + ". " + txt)

falas, vistos = [], set()
for t in textos:
    limpo = limpar(t)
    k = chave(limpo)
    if k in vistos or not limpo:
        continue
    vistos.add(k)
    falas.append({"id": "un_" + k, "texto": fala_de(t)})

io.open(os.path.join(AQUI, "falas.json"), "w", encoding="utf-8").write(
    json.dumps(falas, ensure_ascii=False, indent=1) + "\n")
if not os.path.exists(os.path.join(AQUI, "voz.txt")):
    io.open(os.path.join(AQUI, "voz.txt"), "w", encoding="utf-8").write("pt-BR-AntonioNeural\n")

# o mapa VOZOK dentro do index.html, entre marcas
html = io.open(IDX, encoding="utf-8").read()
mapa = "var VOZOK = " + json.dumps({f["id"][3:]: 1 for f in falas}, separators=(",", ":")) + ";"
novo, n = re.subn(r"/\*VOZOK-INI\*/.*?/\*VOZOK-FIM\*/", "/*VOZOK-INI*/" + mapa + "/*VOZOK-FIM*/", html, flags=re.S)
if n != 1:
    raise SystemExit("index.html sem as marcas /*VOZOK-INI*/ ... /*VOZOK-FIM*/")
io.open(IDX, "w", encoding="utf-8").write(novo)
print("falas.json: %d fala(s); VOZOK gravado no index.html" % len(falas))
