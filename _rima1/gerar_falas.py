# -*- coding: utf-8 -*-
u"""GERA AS FALAS DO BANDO DAS RIMAS — e é ELE que manda no texto.

⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada;
   texto mudou = voz regravada. É isso que acaba com "a tela diz uma coisa e a
   voz diz outra".

⚠️ A RIMA É COISA DE OUVIDO. Numa atividade de rima, o alto-falante não é apoio:
   é o próprio conteúdo. Toda palavra que aparece na tela tem `pal_<w>`, e é por
   isso que este arquivo gera uma fala por palavra do pote inteiro.

Uso: python3 _rima1/gerar_falas.py
"""
from __future__ import print_function

import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"ri_"
VOZ = u"pt-BR-AntonioNeural"

html = io.open(CAM, encoding=u"utf-8").read()
IT = json.loads(re.search(r"/\*ITENS-INI\*/\s*var ITENS = (\{.*?\});\s*/\*ITENS-FIM\*/",
                          html, re.S).group(1))

# ⚠️ COMO A VOZ DIZ CADA PALAVRA. O Edge TTS lê bem o português, mas há palavras
#    em que ele tropeça — e no 1º ano uma palavra mal dita ENSINA ERRADO. Estas
#    foram conferidas uma a uma.
DIZ = {
    u"aviao": u"avião", u"balao": u"balão", u"mamao": u"mamão", u"mao": u"mão",
    u"cafe": u"café", u"picole": u"picolé", u"coracao": u"coração",
    u"sorvete_taca": u"sorvete", u"sorvete_casquinha": u"sorvete",
}


def falado(w):
    return DIZ.get(w, w)


F = {}

# ---- a casa: capa, fim, teclado ----------------------------------------------
F[u"capa"] = (u"O Bando das Rimas. Dez folhas para brincar com as palavras que "
              u"terminam igual. Escreva o seu nome ali embaixo e toque em Começar.")
F[u"fim"] = (u"Você chegou ao fim do Bando das Rimas! Agora você sabe ouvir o "
             u"final das palavras. Olhe o seu mural de rimas ali embaixo.")
F[u"escreva"] = u"Escreva a palavra que rima."
F[u"vozOn"] = u"Narração ligada!"

# ---- os enunciados de cada folha ---------------------------------------------
F[u"p1enun"] = u"Ouça as duas palavras. Elas terminam com o mesmo som?"
F[u"p2enun"] = u"Toque na figura que rima com a de cima."
F[u"p3enun"] = u"Pinte a palavra que rima com a figura."
F[u"p4enun"] = (u"Cuidado! Uma delas começa parecido, mas não rima. "
                u"Ache a que rima de verdade.")
F[u"p5enun"] = u"Circule as duas figuras que rimam."
F[u"p6enun"] = u"Puxe até a figura de cima a que rima com ela. Tocar também vale."
F[u"p7enun"] = u"Ligue cada figura à que rima com ela."
F[u"p8enun"] = u"Ouça a parlenda e escolha a palavra que fecha a rima."
F[u"p9enun"] = u"Escreva a palavra que rima com a figura."
F[u"p10enun"] = (u"Toque nos pares que você mais gostou. "
                 u"Eles vão para o seu mural de rimas.")

# ---- TODA palavra que aparece na tela ganha alto-falante ---------------------
usadas = set()


def usa(w):
    if w:
        usadas.add(w)


for it in IT[u"p1"]:
    usa(it[u"a"]); usa(it[u"b"])
for chave_folha in (u"p2", u"p3", u"p4", u"p6"):
    for it in IT[chave_folha]:
        usa(it[u"f"])
        for w in it[u"op"]:
            usa(w)
for it in IT[u"p5"]:
    for w in it[u"g"]:
        usa(w)
for g in IT[u"p7"]:
    for par in g:
        usa(par[u"e"]); usa(par[u"d"])
for it in IT[u"p8"]:
    for w in it[u"op"]:
        usa(w)
for it in IT[u"p9"]:
    usa(it[u"f"]); usa(it[u"c"].lower())
for it in IT[u"p10"]:
    usa(it[u"f"]); usa(it[u"par"])

for w in sorted(usadas):
    F[u"pal_%s" % w] = falado(w) + u"."

# ---- folha 1: rima ou não rima ------------------------------------------------
# ⚠️ O RETORNO DIZ O PORQUÊ, não só "isso!". É o feedback específico do Hattie:
#    a criança tem que sair sabendo ONDE olhar da próxima vez.
for it in IT[u"p1"]:
    a, b = falado(it[u"a"]), falado(it[u"b"])
    if it[u"r"]:
        F[u"certo1_%s_%s" % (it[u"a"], it[u"b"])] = (
            u"Isso! %s e %s terminam com o mesmo som." % (a.capitalize(), b))
        F[u"dica1_%s_%s" % (it[u"a"], it[u"b"])] = (
            u"Fale devagar: %s... %s. Escute só o FINAL das duas." % (a, b))
    else:
        F[u"certo1_%s_%s" % (it[u"a"], it[u"b"])] = (
            u"Isso mesmo! %s e %s terminam diferente." % (a.capitalize(), b))
        F[u"dica1_%s_%s" % (it[u"a"], it[u"b"])] = (
            u"Escute o final: %s... %s. Terminam igual ou diferente?" % (a, b))

# ---- folhas 2, 3, 4 e 6: a figura-chave e as três opções ----------------------
FIM_DE = {
    u"gato": u"ato", u"pato": u"ato", u"rato": u"ato",
    u"bola": u"ola", u"mola": u"ola",
    u"vela": u"ela", u"panela": u"ela", u"janela": u"ela", u"estrela": u"ela",
    u"boca": u"oca", u"foca": u"oca", u"pipoca": u"oca",
    u"balao": u"ão", u"mamao": u"ão", u"mao": u"ão", u"aviao": u"ão",
    u"foguete": u"ete", u"sorvete": u"ete",
    u"tomate": u"ate", u"abacate": u"ate",
    u"sereia": u"eia", u"baleia": u"eia",
    u"cabrito": u"ito", u"apito": u"ito",
    u"passarinho": u"inho", u"ninho": u"inho", u"ursinho": u"inho",
    u"picole": u"é", u"cafe": u"é",
}


def porque(f, c):
    u"""diz o pedaço que as duas partilham — é isso que a criança leva embora"""
    p = FIM_DE.get(c) or FIM_DE.get(f)
    if p:
        return u" As duas terminam com %s." % p
    return u""


for chave_folha, n in ((u"p2", 2), (u"p3", 3), (u"p4", 4), (u"p6", 6)):
    for it in IT[chave_folha]:
        f, c = it[u"f"], it[u"c"]
        F[u"certo%d_%s" % (n, f)] = (
            u"Muito bem! %s rima com %s.%s"
            % (falado(f).capitalize(), falado(c), porque(f, c)))
        F[u"dica%d_%s" % (n, f)] = (
            u"Fale o nome da figura: %s. Agora escute o final de cada palavra "
            u"e ache a que termina igual." % falado(f))

# ---- folha 4: a dica da PEGADINHA é PRÓPRIA ----------------------------------
# ⭐ Aqui está o coração desta folha. A criança que erra a pegadinha errou por um
#    motivo específico — ela ouviu o COMEÇO — e a dica tem que dizer isso, senão
#    ela erra de novo pelo mesmo caminho.
for it in IT[u"p4"]:
    F[u"dicapeg_%s" % it[u"f"]] = (
        u"Cuidado com a pegadinha! %s começa parecido, mas rima é o FINAL da "
        u"palavra, não o começo. Escute de novo só o finalzinho."
        % falado(it[u"peg"]).capitalize())

# ---- folha 5: circule as duas ------------------------------------------------
for it in IT[u"p5"]:
    a, b = it[u"c"][0], it[u"c"][1]
    F[u"certo5_%s" % a] = (u"Isso! %s e %s rimam.%s"
                           % (falado(a).capitalize(), falado(b), porque(a, b)))
    F[u"dica5_%s" % a] = (u"Fale o nome de cada figura em voz alta e escute o "
                          u"final. Duas delas terminam igual.")

# ---- folha 7: ligar ----------------------------------------------------------
for g in IT[u"p7"]:
    for par in g:
        e, dd = par[u"e"], par[u"d"]
        F[u"certo7_%s" % e] = (u"Isso! %s e %s rimam.%s"
                               % (falado(e).capitalize(), falado(dd), porque(e, dd)))
        F[u"dica7_%s" % e] = (u"Escute o final de %s e procure do outro lado a "
                              u"que termina igual." % falado(e))

# ---- folha 8: as parlendas ---------------------------------------------------
for i, it in enumerate(IT[u"p8"]):
    texto = it[u"t"].replace(u"###", it[u"c"])
    F[u"parl_%d" % i] = texto
    F[u"certo8_%d" % i] = u"Isso! %s" % texto
    F[u"dica8_%d" % i] = (u"Fale a parlenda até o fim e escute: qual palavra "
                          u"combina com o som do final?")

# ---- folha 9: escrever -------------------------------------------------------
for it in IT[u"p9"]:
    F[u"certo9_%s" % it[u"f"]] = (
        u"Muito bem! %s rima com %s.%s"
        % (falado(it[u"f"]).capitalize(), falado(it[u"c"].lower()),
           porque(it[u"f"], it[u"c"].lower())))
    F[u"dica9_%s" % it[u"f"]] = (
        u"A palavra tem que terminar igual a %s. Toque no alto-falante e escute "
        u"de novo." % falado(it[u"f"]))

# ---- folha 10: o mural -------------------------------------------------------
for it in IT[u"p10"]:
    F[u"certo10_%s" % it[u"f"]] = (
        u"%s e %s foram para o seu mural!"
        % (falado(it[u"f"]).capitalize(), falado(it[u"par"])))


# ---- a chave da casa (a MESMA do JS: djb2 em base 36) ------------------------
def chave(s):
    s = re.sub(r"\s+", u" ", s or u"").strip().lower()
    hh = 5381
    for ch in s:
        hh = ((hh * 33) ^ ord(ch)) & 0xFFFFFFFF
    d, out = hh, u""
    if d == 0:
        return u"0"
    while d:
        out = u"0123456789abcdefghijklmnopqrstuvwxyz"[d % 36] + out
        d //= 36
    return out


falas, vistos = [], {}
for k in sorted(F.keys()):
    t = F[k]
    if not t:
        continue
    c = chave(t)
    if c in vistos:
        continue
    vistos[c] = 1
    falas.append({u"id": PREFIXO + c, u"texto": t, u"voz": VOZ})

io.open(os.path.join(AQUI, u"falas.json"), u"w", encoding=u"utf-8").write(
    json.dumps(falas, ensure_ascii=False, indent=1))
io.open(os.path.join(AQUI, u"voz.txt"), u"w", encoding=u"utf-8").write(VOZ + u"\n")

blocoF = (u"/*FALAS-INI*/\nvar FALAS = "
          + json.dumps(F, ensure_ascii=False, indent=1, sort_keys=True) + u";\n/*FALAS-FIM*/")
blocoV = (u"/*VOZOK-INI*/var VOZOK = "
          + json.dumps(dict((c, 1) for c in vistos), ensure_ascii=False) + u";/*VOZOK-FIM*/")
novo = re.sub(r"/\*FALAS-INI\*/.*?/\*FALAS-FIM\*/", lambda m: blocoF, html, flags=re.S)
novo = re.sub(r"/\*VOZOK-INI\*/.*?/\*VOZOK-FIM\*/", lambda m: blocoV, novo, flags=re.S)
# ⚠️ esta atividade NÃO recorta sílaba de dentro da palavra (isso é da Fábrica de
#    Palavras). O bloco SILMAP some, e com ele o `silabas.json`.
novo = re.sub(r"/\*SILMAP-INI\*/.*?/\*SILMAP-FIM\*/",
              lambda m: u"/*SILMAP-INI*/var SILMAP = {};/*SILMAP-FIM*/", novo, flags=re.S)
io.open(CAM, u"w", encoding=u"utf-8").write(novo)

print(u"FALAS: %d chaves; falas.json: %d fala(s); VOZOK gravado" % (len(F), len(falas)))
