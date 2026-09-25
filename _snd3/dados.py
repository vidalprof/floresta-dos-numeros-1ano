# -*- coding: utf-8 -*-
u"""Gera os DADOS do _snd3 com as contas FEITAS, nunca digitadas.

⚠️ POR QUE GERAR EM VEZ DE ESCREVER. São 35 folhas de sistema decimal: cada
número tem a sua decomposição, o seu antecessor, o seu sucessor, o valor de
cada algarismo e a posição dele na reta. Digitar isso à mão é convidar o erro
de conta — e erro de conta numa folha de Matemática é a pior coisa que este
caderno pode ter, porque a criança confia nele. Aqui o número é a ÚNICA coisa
escolhida à mão; tudo o que dele decorre é calculado.
"""
from __future__ import print_function
import io, json

def ordens(n):
    return {"m": n // 1000, "c": (n // 100) % 10, "d": (n // 10) % 10, "u": n % 10}

def partes(n):
    u"""300 + 50 + 6 — e SEM as parcelas que valem zero, que é como se escreve."""
    o = ordens(n)
    p = []
    if o["m"]: p.append(o["m"] * 1000)
    if o["c"]: p.append(o["c"] * 100)
    if o["d"]: p.append(o["d"] * 10)
    if o["u"]: p.append(o["u"])
    return p

UN = [u"zero", u"um", u"dois", u"três", u"quatro", u"cinco", u"seis", u"sete",
      u"oito", u"nove", u"dez", u"onze", u"doze", u"treze", u"catorze", u"quinze",
      u"dezesseis", u"dezessete", u"dezoito", u"dezenove"]
DEZ = [u"", u"", u"vinte", u"trinta", u"quarenta", u"cinquenta", u"sessenta",
       u"setenta", u"oitenta", u"noventa"]
CEM = [u"", u"cento", u"duzentos", u"trezentos", u"quatrocentos", u"quinhentos",
       u"seiscentos", u"setecentos", u"oitocentos", u"novecentos"]

def extenso(n):
    u"""Por extenso, até 1.000. Serve à cruzadinha e ao texto falado."""
    if n == 1000: return u"mil"
    if n == 100: return u"cem"
    o = ordens(n)
    fim = []
    if o["c"]: fim.append(CEM[o["c"]])
    resto = n % 100
    if resto:
        if resto < 20: fim.append(UN[resto])
        elif o["u"] == 0: fim.append(DEZ[o["d"]])
        else: fim.append(DEZ[o["d"]] + u" e " + UN[o["u"]])
    return u" e ".join(fim) if fim else UN[0]

# ------------------------------------------------------------------
# OS NÚMEROS ESCOLHIDOS À MÃO — e cada escolha tem motivo escrito.
# ------------------------------------------------------------------
D = {}

# f04/f05 — ler as peças e escrever o número (três ordens, sem zero)
D["p4"] = [234, 152, 316, 425, 143, 261]
# f05 sobe o degrau: passa a haver o zero em alguma ordem
D["p5"] = [304, 420, 250, 506, 130, 640]
# f06/f07 — montar com as peças
D["p6"] = [213, 142, 325, 231]
D["p7"] = [205, 430, 307, 260]          # o zero numa das ordens
# f09/f10 — o quadro C D U
D["p9"] = [376, 248, 591, 137, 462, 825]
D["p10"] = [508, 640, 903, 270]
# f11/f12 — o valor do algarismo
D["p11"] = [253, 471, 168, 342, 795, 526]
D["p12"] = [253, 523, 355, 535]         # o MESMO algarismo em lugares diferentes
# f13/f14 — o zero guarda-lugar
D["p13"] = [(205, 25), (307, 37), (409, 49)]
D["p14"] = [305, 350, 35]
# f15/f16 — montar a soma (decompor)
D["p15"] = [356, 274, 683, 519, 428, 147]
D["p16"] = [508, 470, 603, 290]
# f17/f18 — compor
D["p17"] = [452, 736, 218, 965, 384, 127]
D["p18"] = [452, 736, 218, 965]         # as parcelas vêm fora de ordem
# f20/f21 — equivalências
D["p20"] = [(1, "centena", 10, "dezenas"), (1, "centena", 100, "unidades"),
            (1, "dezena", 10, "unidades"), (1, "milhar", 10, "centenas")]
D["p21"] = [340, 520, 810, 260]         # quantas dezenas cabem em…
# f22/f23 — antecessor e sucessor
D["p22"] = [347, 512, 268, 431, 795, 183]
D["p23"] = [199, 299, 999, 409]         # a passagem que muda de ordem
# f24 — a fila dos vizinhos (ordenar)
D["p24"] = [[248, 249, 250, 251, 252]]
# f25 — verdadeiro ou falso
D["p25"] = [
  (u"O sucessor de 199 é 200.", True),
  (u"O antecessor de 999 é 1.000.", False),   # o item falso de propósito (crivo §5)
  (u"Em 407 há 4 centenas, 0 dezenas e 7 unidades.", True),
  (u"O número 250 é maior que 205.", True),
  (u"Em 63 o algarismo 6 vale seis.", False),
]
# f26/f27 — o ditado numérico
D["p26"] = [175, 483, 296, 351, 628]
D["p27"] = [406, 250, 703, 890]
# f28/f29 — a reta numérica
D["p28"] = [(120, 130, 125), (240, 250, 245), (370, 380, 373), (560, 570, 566)]
D["p29"] = [(100, 200, 10, 150), (300, 400, 10, 370), (200, 700, 100, 500),
            (400, 900, 100, 600)]
# f30 — comparar
D["p30"] = [(205, 250), (318, 381), (470, 470), (692, 629), (150, 105), (843, 834)]
# f31 — ordenar do menor ao maior
D["p31"] = [[420, 204, 240, 402]]
# f32 — o caça-números: marcar todos os que têm 5 dezenas
D["p32"] = [[352, 458, 253, 519, 651, 405, 750, 236]]
# f33 — a cruzadinha dos números por extenso
D["p33"] = [[13, 40, 15, 60, 100, 12]]
# f34 — o cartaz final (sobre 407)
D["p34"] = [[407]]
D["p35"] = [[562]]

def main():
    saida = {}
    for k, v in D.items():
        saida[k] = v
    # as contas derivadas, para o JS não ter de refazê-las nem errá-las
    deriv = {}
    # ⚠️ achatar TUDO antes de derivar: há listas, tuplas e listas de listas
    #    misturadas, e a primeira versão quebrou somando tupla com lista.
    def achata(x, saco):
        if isinstance(x, (list, tuple)):
            for y in x: achata(y, saco)
        elif isinstance(x, int) and 0 <= x <= 1000:
            saco.add(x)
    saco = set()
    for k in D:
        achata(D[k], saco)
    for n in sorted(saco):
        deriv[str(n)] = {
            "o": ordens(n), "p": partes(n), "e": extenso(n),
            "ant": n - 1, "suc": n + 1,
        }
    for n in D["p33"][0]:
        deriv[str(n)] = {"o": ordens(n), "p": partes(n), "e": extenso(n),
                         "ant": n - 1, "suc": n + 1}
    saida["_n"] = deriv
    io.open("/tmp/claude-0/v/snd3_dados.json", "w", encoding="utf-8").write(
        json.dumps(saida, ensure_ascii=False, indent=1) + u"\n")
    print(u"%d números derivados" % len(deriv))
    for n in (356, 508, 205, 999, 340, 13, 100):
        d = deriv.get(str(n))
        if d: print(u"  %4d  %-28s  ant %-5d suc %-5d  %s" %
                    (n, " + ".join(str(x) for x in d["p"]), d["ant"], d["suc"], d["e"]))

if __name__ == "__main__":
    main()
