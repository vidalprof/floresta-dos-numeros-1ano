# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO — "a prova tem o número de questões que ela PROMETE?"

 ⚠️ LIÇÃO PAGA (20/set/2026, Mesa de Jogos do Léo). A narração da capa dizia,
    com a voz do mascote:

        "São VINTE perguntas: quinze sobre as regras oficiais do UNO (...)
         e cinco sobre a origem do Tangram."

    e a prova tinha VINTE E UMA. Eu escrevi a fala quando o roteiro previa 20,
    acrescentei uma questão depois e não voltei na fala. A criança ouviria
    "são vinte perguntas", responderia vinte, veria "Pergunta 21 de 21" e
    pensaria que errou alguma coisa — ou que o computador quebrou.

    O que assusta é o que NÃO pegou isso: sintaxe, clone, revisor de texto,
    contraste, leiaute, sobreposto, currículo verbatim, o jogador que joga a
    prova inteira em cinco tamanhos e até o portão do gabarito do painel. TODOS
    passaram, porque cada um olhava uma coisa certa e nenhum comparava a
    PROMESSA com o FATO. Quem pegou foi o Marcos pedindo outra coisa ("faça com
    20 questões"), por acaso.

 O QUE ELE FAZ: roda o JS da prova de verdade (não regex), lê `QUESTOES` e a
 narração da capa (`HISTORIA`), acha o número que ela promete — por extenso ou
 em algarismo — e reprova se não for o número de questões que existem.

 ⚠️ O QUE ELE **NÃO** FAZ, dito antes de alguém confiar demais: ele confere o
    TOTAL, que é inequívoco ("N perguntas"). Os outros números da frase (os
    subtotais por assunto, "quinze sobre o UNO e cinco sobre o Tangram") ele
    IMPRIME para o olho humano conferir, mas não reprova — a frase pode
    legitimamente citar números que não são contagem de questão ("a partir de
    7 anos", "500 pontos"), e portão que acusa inocente é portão que se aprende
    a ignorar. Quando os subtotais somam o total, ele diz isso em uma linha.

 uso:  python3 _qa/prova_promete.py <pasta-da-prova>
 saída: 0 passou · 1 REPROVADO · 2 NÃO MEDI (que não é "passou")
============================================================
"""
import io
import json
import os
import re
import subprocess
import sys

EXTENSO = {
    u"uma": 1, u"um": 1, u"dois": 2, u"duas": 2, u"três": 3, u"tres": 3,
    u"quatro": 4, u"cinco": 5, u"seis": 6, u"sete": 7, u"oito": 8, u"nove": 9,
    u"dez": 10, u"onze": 11, u"doze": 12, u"treze": 13, u"quatorze": 14,
    u"catorze": 14, u"quinze": 15, u"dezesseis": 16, u"dezessete": 17,
    u"dezoito": 18, u"dezenove": 19, u"vinte": 20, u"trinta": 30,
    u"vinte e uma": 21, u"vinte e um": 21, u"vinte e duas": 22,
    u"vinte e cinco": 25, u"vinte e quatro": 24, u"vinte e três": 23,
}
# "N perguntas", "N questões", "N perguntinhas"... — o que conta o instrumento
COISA = u"(?:perguntas?|quest[õo]es|quest[ãa]o)"


def le_prova(pasta):
    u"""roda o JS da prova num Node e devolve QUESTOES e HISTORIA."""
    arq = os.path.join(pasta, "index.html")
    if not os.path.exists(arq):
        return None, u"não achei %s" % arq
    script = u"""
const fs=require("fs"),vm=require("vm");
const h=fs.readFileSync(process.argv[1],"utf8");
const js=[...h.matchAll(/<script(?![^>]*src)[^>]*>([\\s\\S]*?)<\\/script>/g)].map(m=>m[1]).join("\\n");
const c={window:{},console:{log(){},error(){},warn(){}},
  document:{addEventListener(){},getElementById(){return null}},
  localStorage:{getItem(){return null},setItem(){}}};
vm.createContext(c);
try{ vm.runInContext(js.replace(/\\nboot\\(\\);\\s*$/,"\\n"),c); }
catch(e){ console.log(JSON.stringify({erro:String(e.message)})); process.exit(0); }
console.log(JSON.stringify({n:(c.QUESTOES||[]).length, hist:c.HISTORIA||""}));
"""
    r = subprocess.run(["node", "-e", script, arq], capture_output=True, text=True)
    if r.returncode != 0:
        return None, u"o Node falhou: %s" % (r.stderr or "")[:160]
    try:
        d = json.loads(r.stdout.strip().split("\n")[-1])
    except Exception:
        return None, u"não entendi a saída do Node"
    if d.get("erro"):
        return None, u"o JS da prova estourou: %s" % d["erro"]
    return d, None


def numeros(texto):
    u"""todo número da frase, por extenso ou em algarismo, com o que vem depois."""
    achados = []
    for m in re.finditer(r"\d+", texto):
        achados.append((int(m.group(0)), m.start(), m.end()))
    chaves = sorted(EXTENSO, key=len, reverse=True)   # "vinte e uma" antes de "vinte"
    for k in chaves:
        for m in re.finditer(r"(?<![a-zà-ú])" + re.escape(k) + r"(?![a-zà-ú])", texto, re.I):
            if any(a <= m.start() < b for _, a, b in achados):
                continue
            achados.append((EXTENSO[k], m.start(), m.end()))
    return sorted(achados, key=lambda x: x[1])


def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/prova_promete.py <pasta-da-prova>")
        return 2
    pasta = sys.argv[1].rstrip("/")
    d, erro = le_prova(pasta)
    if erro:
        print(u'%s -> NAO MEDI: %s (isso nao e "passou").' % (pasta, erro))
        return 2
    n, hist = d["n"], d["hist"]
    if not n:
        print(u'%s -> NAO MEDI: a prova nao expoe `var QUESTOES` (isso nao e "passou").' % pasta)
        return 2
    if not hist.strip():
        print(u'%s -> NAO MEDI: a prova nao tem narracao de capa (`var HISTORIA`).' % pasta)
        return 2

    achados = numeros(hist)
    # o TOTAL é o número seguido (em até ~18 letras) de "perguntas"/"questões"
    prometido, trecho = None, u""
    for valor, ini, fim in achados:
        depois = hist[fim:fim + 22]
        if re.match(r"^\s*(?:\w+\s+){0,2}" + COISA, depois, re.I):
            prometido = valor
            trecho = hist[max(0, ini - 24):fim + 22].strip()
            break

    if prometido is None:
        print(u"%s -> NAO SE APLICA: a narracao da capa nao promete um numero de "
              u"perguntas. Nada a conferir (a prova tem %d)." % (pasta, n))
        return 2

    outros = [v for v, _, _ in achados if v != prometido]
    if prometido != n:
        print(u"%s -> REPROVADO: a capa PROMETE %d e a prova tem %d" % (pasta, prometido, n))
        print(u'   a narracao diz: "...%s..."' % trecho)
        print(u"   a crianca ouve o numero errado, responde e ve 'Pergunta %d de %d'." % (n, n))
        print(u"   conserto: acertar `var HISTORIA` (e regerar o falas.json a partir dela).")
        return 1

    print(u"%s -> a capa promete %d pergunta(s) e a prova tem %d: bate" % (pasta, prometido, n))
    if outros:
        soma = sum(outros)
        print(u"   outros numeros na mesma frase (NAO medidos, confira com o olho): %s"
              % u", ".join(str(x) for x in outros))
        if soma == n:
            print(u"   -> e eles somam %d, exatamente o total. Bom sinal." % soma)
        else:
            print(u"   -> eles somam %d, que NAO e o total (%d). Pode ser certo (a frase "
                  u"talvez cite idade, pontos...), mas OLHE." % (soma, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
