# -*- coding: utf-8 -*-
u"""
A Oficina do Material Dourado — gera o dicionário FALAS a partir do bloco ITENS do
index.html, grava-o entre /*FALAS-INI*/ e /*FALAS-FIM*/, escreve o falas.json e o
mapa VOZOK. Mesmo padrão do UNO, da Folha Viva e dos Dedinhos (app à mão).

Por que o gerador lê o ITENS: as folhas SORTEIAM os itens de um pool. Se as frases
fossem escritas à mão, um item sorteado sairia mudo. Aqui todas as combinações
possíveis do pool viram fala — não existe frase sem mp3.

Uso: python3 _dourado5/gerar_falas.py
"""
import io, json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.join(AQUI, "index.html")

U = [u"zero", u"um", u"dois", u"três", u"quatro", u"cinco", u"seis", u"sete", u"oito", u"nove",
     u"dez", u"onze", u"doze", u"treze", u"catorze", u"quinze", u"dezesseis", u"dezessete",
     u"dezoito", u"dezenove"]
DZ = [u"", u"", u"vinte", u"trinta", u"quarenta", u"cinquenta", u"sessenta", u"setenta", u"oitenta", u"noventa"]
CT = [u"", u"cento", u"duzentos", u"trezentos", u"quatrocentos", u"quinhentos", u"seiscentos",
      u"setecentos", u"oitocentos", u"novecentos"]


def ext(n):
    u"""número por extenso, 0..1000 (é o que o caderno usa)."""
    n = int(n)
    if n == 1000:
        return u"mil"
    if n < 20:
        return U[n]
    if n < 100:
        d, r = divmod(n, 10)
        return DZ[d] + (u" e " + U[r] if r else u"")
    c, r = divmod(n, 100)
    if c == 1 and r == 0:
        return u"cem"
    return CT[c] + (u" e " + ext(r) if r else u"")


def pecas_txt(c, d, u_):
    p = []
    if c:
        p.append(u"%s placa" % ext(c) if c == 1 else u"%s placas" % ext(c))
    if d:
        p.append(u"%s barra" % ext(d) if d == 1 else u"%s barras" % ext(d))
    if u_:
        p.append(u"%s cubinho" % ext(u_) if u_ == 1 else u"%s cubinhos" % ext(u_))
    if not p:
        return u"nenhuma peça"
    if len(p) == 1:
        return p[0]
    return u", ".join(p[:-1]) + u" e " + p[-1]


html = io.open(IDX, encoding="utf-8").read()
m = re.search(r"/\*ITENS-INI\*/\s*var ITENS\s*=\s*(\{.*?\});\s*/\*ITENS-FIM\*/", html, re.S)
if not m:
    raise SystemExit("index.html sem o bloco /*ITENS-INI*/ var ITENS = {...}; /*ITENS-FIM*/")
IT = json.loads(m.group(1))

F = {}

# ---- fixas ----------------------------------------------------------------
F.update({
    "capa": u"A Oficina do Material Dourado. Divisão, quinto ano, dez folhas. "
            u"Escreva o seu nome ali embaixo e toque em Começar.",
    "nomeOk": u"Pronto! Agora toque em Começar.",
    "vozOn": u"Narração ligada!",
    "p1enun": u"Cada peça do material dourado vale um tanto. Toque na peça e depois no valor dela, ou puxe uma linha.",
    "p2enun": u"Conte as peças e escreva que número elas formam. Lembre: cada placa vale cem, cada barra vale dez e cada cubinho vale um.",
    "p3enun": u"Agora monte o número com as peças de verdade. Toque na peça de baixo para pôr na mesa; toque numa peça da mesa para tirar.",
    "casaCheia": u"Cada casa vai só até nove. Se juntar dez, é hora de trocar por uma peça maior.",
    "rascLimpo": u"Rascunho limpo. Pode armar a conta de novo.",
    "passou": u"Passou do número! Toque numa peça da mesa para tirar.",
    "p4enun": u"As peças foram repartidas igualmente entre os grupos. Olhe um grupo e escreva quanto ficou em cada um.",
    "p5enun": u"Sobrou uma barra e ela não dá para repartir inteira. Troque a barra por dez cubinhos e termine a conta. É isso que a conta armada chama de abaixar o número.",
    "p6enun": u"Nem tudo dá para repartir igual: o que não fecha um grupo é o resto. Escreva o resultado e o resto.",
    "p7enun": u"Agora só com os números: preencha a chave da conta armada, com o resultado e o resto.",
    "p8enun": u"Toque na conta e depois no resultado dela, ou puxe uma linha até ele.",
    "p9enun": u"Leia o problema, descubra que divisão ele pede e escreva a resposta.",
    "p10enun": u"Para conferir uma divisão a gente faz a prova real: o resultado vezes o divisor, mais o resto, tem que dar o número de novo.",
    "quase": u"Quase! Confira a conta e tente de novo.",
    "essaNao": u"Essa não. Faça a conta de novo e procure o resultado certo.",
    "digite": u"Toque numa caixa e digite a resposta.",
    "ligue": u"Primeiro toque na peça da esquerda, depois no valor.",
    "folhaPronta": u"Folha pronta! Vamos para a próxima.",
    "faltam": u"Ainda falta responder nesta folha. Olhe as caixas tracejadas.",
    "fim": u"Você terminou o caderno inteiro da Oficina do Material Dourado! Parabéns!",
    "fimRel": u"Relatório do professor aberto.",
    "retomar": u"Você estava no meio do caderno. Quer continuar de onde parou?",
    "novoCaderno": u"Caderno novo! As contas mudaram. Vamos lá?",
    # folha 1 — as peças
    "peca_u": u"O cubinho.", "peca_d": u"A barra.", "peca_c": u"A placa.", "peca_m": u"O cubão.",
    "vale_u": u"Isso! O cubinho é uma unidade: vale um.",
    "vale_d": u"Isso! A barra tem dez cubinhos: vale dez.",
    "vale_c": u"Isso! A placa tem dez barras: vale cem.",
    "vale_m": u"Isso! O cubão tem dez placas: vale mil.",
    "dica_u": u"O cubinho é a menor peça de todas. Ele é a unidade.",
    "dica_d": u"Conte os riscos da barra: são dez cubinhos grudados.",
    "dica_c": u"A placa é um quadrado de dez por dez: dez barras, cem cubinhos.",
    "dica_m": u"O cubão é um cubo grande: dez placas empilhadas.",
})
for n in (1, 10, 100, 1000):
    F["n%d" % n] = ext(n)

# ---- folha 2: qual é o número --------------------------------------------
for it in IT["p2"]:
    c, d, u_ = it["c"], it["d"], it["u"]
    n = c * 100 + d * 10 + u_
    F["qual2_%d" % n] = u"Aqui estão %s. Que número elas formam?" % pecas_txt(c, d, u_)
    F["certo2_%d" % n] = u"Isso! %s formam %s." % (pecas_txt(c, d, u_).capitalize(), ext(n))
    F["dica2_%d" % n] = u"Conte por partes: %s são %s; %s são %s; e %s. Junte tudo." % (
        (u"%s placas" % ext(c)) if c != 1 else u"uma placa", ext(c * 100),
        (u"%s barras" % ext(d)) if d != 1 else u"uma barra", ext(d * 10),
        (u"%s cubinhos" % ext(u_)) if u_ != 1 else u"um cubinho")

# ---- folha 3: monte o número ---------------------------------------------
for n in IT["p3"]:
    c, d, u_ = n // 100, (n // 10) % 10, n % 10
    F["monte_%d" % n] = u"Monte o número %s na mesa: quantas placas, quantas barras e quantos cubinhos?" % ext(n)
    F["certo3_%d" % n] = u"Isso! %s são %s." % (ext(n).capitalize(), pecas_txt(c, d, u_))
    F["dica3_%d" % n] = u"Olhe cada algarismo do número %s: o primeiro diz as placas, o do meio diz as barras e o último diz os cubinhos." % ext(n)

# ---- folha 4 e 5: repartir e a troca -------------------------------------
for it in IT["p4"] + IT["p5"]:
    n, d = it["n"], it["d"]
    q = n // d
    k = "%d_%d" % (n, d)
    F["quanto4_" + k] = u"%s dividido por %s. Quanto fica em cada grupo?" % (ext(n), ext(d))
    F["certo4_" + k] = u"Isso! %s dividido por %s dá %s." % (ext(n).capitalize(), ext(d), ext(q))
    F["dica4_" + k] = u"Olhe UM grupo e conte as peças dele: some as barras e os cubinhos daquele grupo."
for it in IT["p5"]:
    n, d = it["n"], it["d"]
    dz, un = (n // 10) % 10, n % 10
    porgrupo = dz // d
    sobra = dz - porgrupo * d
    unidades = sobra * 10 + un
    k = "%d_%d" % (n, d)
    F["troca_" + k] = u"Comece pelas barras: são %s barras para %s grupos. Quantas barras vão para cada grupo?" % (ext(dz), ext(d))
    F["certo5a_" + k] = u"Isso! %s barras para cada grupo." % ext(porgrupo) if porgrupo != 1 else u"Isso! Uma barra para cada grupo."
    F["dica5a_" + k] = u"Reparta só as barras, uma de cada vez, até não dar mais uma para cada grupo."
    F["trocaB_" + k] = u"A barra que sobrou virou dez cubinhos. Com os cubinhos que já tinha, quantos cubinhos há agora?"
    F["certo5b_" + k] = u"Isso! Ficaram %s cubinhos para repartir." % ext(unidades)
    F["dica5b_" + k] = u"Dez cubinhos da barra trocada mais os %s cubinhos que já estavam ali." % ext(un)

# ---- folha 6, 7 e 10: resto, conta armada, prova real ---------------------
for it in IT["p6"] + IT["p7"] + IT["p10"]:
    n, d = it["n"], it["d"]
    q, r = n // d, n % d
    k = "%d_%d" % (n, d)
    F["resto_" + k] = u"%s dividido por %s. Qual é o resultado e qual é o resto?" % (ext(n), ext(d))
    F["certo6_" + k] = u"Isso! %s dividido por %s dá %s e sobram %s." % (ext(n).capitalize(), ext(d), ext(q), ext(r))
    F["dica6_" + k] = u"Reparta o quanto der em grupos iguais. O que não fecha mais um grupo é o resto — e o resto é sempre menor que %s." % ext(d)
    F["armada_" + k] = u"Na chave: %s dividido por %s. Escreva o resultado." % (ext(n), ext(d))
    F["armadaR_" + k] = u"E quanto sobrou nesta conta? Escreva o resto."
    F["certo7_" + k] = u"Isso! %s dividido por %s dá %s%s." % (
        ext(n).capitalize(), ext(d), ext(q), (u", com resto %s" % ext(r)) if r else u", certinho, sem resto")
    F["dica7_" + k] = u"Vá por partes, como no material: primeiro as centenas, depois as dezenas, depois as unidades."
    F["prova_" + k] = u"A prova real: %s vezes %s dá quanto?" % (ext(q), ext(d))
    F["certo10a_" + k] = u"Isso! %s vezes %s dá %s." % (ext(q).capitalize(), ext(d), ext(q * d))
    F["provaB_" + k] = u"Agora some o resto: %s mais %s." % (ext(q * d), ext(r))
    F["certo10b_" + k] = u"Isso! Voltou para %s: a divisão está certa." % ext(n)
    F["dica10_" + k] = u"A prova real é o caminho de volta: resultado vezes divisor, e depois soma o resto."

# ---- folha 8: ligar a conta ao resultado ---------------------------------
for it in IT["p8"]:
    n, d = it["n"], it["d"]
    q = n // d
    k = "%d_%d" % (n, d)
    F["conta_" + k] = u"%s dividido por %s." % (ext(n), ext(d))
    F["certo8_" + k] = u"Isso! %s dividido por %s dá %s." % (ext(n).capitalize(), ext(d), ext(q))
    F["dica8_" + k] = u"Pense na tabuada do %s: quantas vezes o %s cabe em %s?" % (ext(d), ext(d), ext(n))
    F["n%d" % q] = ext(q)

# ---- folha 9: problemas ---------------------------------------------------
for it in IT["p9"]:
    n, d = it["n"], it["d"]
    q = n // d
    k = "%d_%d" % (n, d)
    F["prob_" + k] = it["hist"] + u" " + it["q"]
    F["certo9_" + k] = u"Isso! %s dividido por %s dá %s." % (ext(n).capitalize(), ext(d), ext(q))
    F["dica9_" + k] = u"O problema manda repartir %s em %s partes iguais. Isso é uma divisão: %s dividido por %s." % (
        ext(n), ext(d), ext(n), ext(d))


def chave(s):
    s = re.sub(r"\s+", " ", s or "").strip().lower()
    hh = 5381
    for ch in s:
        hh = (hh * 33 + ord(ch)) & 0xFFFFFFFF
    if hh == 0:
        return "0"
    dd = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    while hh:
        out = dd[hh % 36] + out
        hh //= 36
    return out


bloco = "/*FALAS-INI*/\nvar FALAS = " + json.dumps(F, ensure_ascii=False, indent=1, sort_keys=True) + ";\n/*FALAS-FIM*/"
novo, n1 = re.subn(r"/\*FALAS-INI\*/.*?/\*FALAS-FIM\*/", lambda m2: bloco, html, flags=re.S)
if n1 != 1:
    raise SystemExit("index.html sem as marcas /*FALAS-INI*/ ... /*FALAS-FIM*/")

falas, vistos = [], set()
for k in sorted(F):
    t = re.sub(r"\s+", " ", F[k]).strip()
    c = chave(t)
    if c in vistos:
        continue
    vistos.add(c)
    falas.append({"id": "od_" + c, "texto": t})
io.open(os.path.join(AQUI, "falas.json"), "w", encoding="utf-8").write(
    json.dumps(falas, ensure_ascii=False, indent=1) + "\n")
if not os.path.exists(os.path.join(AQUI, "voz.txt")):
    io.open(os.path.join(AQUI, "voz.txt"), "w", encoding="utf-8").write("pt-BR-AntonioNeural\n")

mapa = "var VOZOK = " + json.dumps({f["id"][3:]: 1 for f in falas}, separators=(",", ":")) + ";"
novo, n2 = re.subn(r"/\*VOZOK-INI\*/.*?/\*VOZOK-FIM\*/", "/*VOZOK-INI*/" + mapa + "/*VOZOK-FIM*/", novo, flags=re.S)
if n2 != 1:
    raise SystemExit("index.html sem as marcas /*VOZOK-INI*/ ... /*VOZOK-FIM*/")
io.open(IDX, "w", encoding="utf-8").write(novo)
print("FALAS: %d chaves; falas.json: %d fala(s); VOZOK gravado" % (len(F), len(falas)))
