#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""LIGA AS PEÇAS AO MOTOR — sem reescrever nenhuma das duas.

O problema: a peça é uma **mini-atividade** (monta a própria tela, chama
`limpa()`, `setProg()` e termina em `mostraBanner`). O motor quer uma **fase**
(recebe o `cen` pronto e chama `fim()`). Reescrever 78 peças para virarem fases
seria jogar fora o teste de cada uma — e reintroduzir os 31 defeitos que elas já
custaram.

A ponte: cada peça entra num **fechamento** com ajudantes trocados por versões
que servem à fase. A peça continua achando que está sozinha; o motor continua
mandando. Ninguém reescreve nada.

  limpa()          → limpa só o `cen` da fase (não a tela do motor)
  setProg(t,p)     → não faz nada (quem manda na barra é o motor)
  app              → o `cen` da fase
  mostraBanner(m,c)→ comemora e chama `fim()` (o motor leva à fase seguinte)
  ajuda / regFase  → os do motor (andaime e medição de verdade)

⚠️ O CSS da peça também vem junto, com o nome dela na frente de cada regra, para
   duas peças não brigarem por causa da mesma classe (`.opt`, `.pc`, `.zona`).

Uso:  python3 _padrao/ESQUELETO/integrar.py            → lista o que dá para ligar
      python3 _padrao/ESQUELETO/integrar.py --escrever → escreve pecas.js/pecas.css
"""
import io
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
PECAS = os.path.join(RAIZ, "_padrao", "pecas")

MARCA_CSS = "CSS DESTA"          # onde começa o CSS próprio da peça, no molde
MARCA_JS = "A PE"                # "A PEÇA COMEÇA AQUI"


def css_da_peca(html):
    u"""só o bloco que a peça acrescentou — o CSS do molde já está no motor."""
    st = re.findall(r"<style>(.*?)</style>", html, re.S)
    if not st:
        return ""
    todo = st[0]
    i = todo.find(MARCA_CSS)
    if i < 0:
        return ""
    j = todo.find("*/", i)
    return todo[j + 2:] if j > 0 else todo[i:]


def js_da_peca(html):
    u"""o segundo <script>: o corpo da mecânica."""
    sc = re.findall(r"<script>(.*?)</script>", html, re.S)
    return sc[1] if len(sc) > 1 else ""


def entrada(js):
    u"""a função que a peça chama sozinha no fim do arquivo — é a porta dela."""
    m = None
    for m in re.finditer(r"^\s*([\w$]+)\s*\(\s*\)\s*;\s*$", js, re.M):
        pass
    return m.group(1) if m else None


def gaveta(js):
    u"""A GAVETA DE CONTEÚDO da peça — o que faz a atividade virar dado.

    Toda peça abre com um bloco assim, e o comentário acima dele diz sempre a
    mesma frase: *"O CONTEÚDO É SÓ EXEMPLO... troque APENAS este bloco"*:

        var QZ = [ {p:"...", c:"...", e:[...], d:[...]}, ... ];

    Essa `var` é a **primeira lista/objeto declarada no topo da peça**. Achando
    o nome dela, o montador consegue trocar o conteúdo de exemplo pelo conteúdo
    de verdade (`f.dados`) **sem tocar na peça** — que é o ponto: a peça já foi
    testada, e reescrevê-la é reintroduzir os defeitos que ela custou.

    Devolve o nome da variável, ou None (aí a fase roda com o exemplo dela e o
    montador avisa em alto e bom som)."""
    for m in re.finditer(r"^var\s+([A-Za-z_$][\w$]*)\s*=\s*[\[{]", js, re.M):
        return m.group(1)
    return None


def prefixa_css(css, nome):
    u"""`.opt{...}` vira `.mec-escolher .opt{...}` — duas peças não brigam."""
    fora = []
    for bloco in re.split(r"(@media[^{]*\{)", css):
        fora.append(bloco)
    saida, dentro_media = [], 0
    for pedaco in re.finditer(r"([^{}]+)(\{[^{}]*\})|(@media[^{]*\{)|(\})", css, re.S):
        sel, corpo, media, fecha = pedaco.groups()
        if media:
            saida.append(media); dentro_media += 1
        elif fecha:
            saida.append("}"); dentro_media = max(0, dentro_media - 1)
        elif sel is not None:
            s = sel.strip()
            if not s or s.startswith("@") or s.startswith("/*"):
                saida.append(sel + (corpo or ""))
                continue
            novo = ", ".join(
                (".mec-%s %s" % (nome, x.strip())) if not x.strip().startswith("@") else x
                for x in s.split(","))
            saida.append("\n" + novo + (corpo or ""))
    return "".join(saida)


u"""⚠️ LIÇÃO PAGA (a marca que o montador procura): a primeira marca era
`/* ---------- nome ---------- */`, e as PRÓPRIAS peças usam esse traço nos
comentários delas ("a regra da fase", "as TRÊS portas de entrada"...). Eram 163
marcas para 74 peças. O `recorta()` do montador partia a peça no meio do primeiro
comentário interno e escrevia meia mecânica na atividade — JS quebrado na mão da
criança. A marca agora é `==== PECA: nome ====`, que nenhuma peça escreve."""
MARCA = u"/* ==== PECA: %s ==== */"

PONTE = u'''
/* ==== PECA: %(nome)s ==== */
MEC["%(nome)s"] = function(f, cen, fim){
  cen.className = cen.className + " mec-%(nome)s";
  (function(){
    /* a peca acha que esta sozinha; estes ajudantes fazem o meio de campo */
    var app = cen;
    function limpa(){ var g = cen.getElementsByClassName("pecabox")[0];
      if(g) g.innerHTML = ""; else { g = document.createElement("div");
      g.className = "pecabox"; cen.appendChild(g); } app = g; }
    function setProg(){}
    function mostraBanner(msg, cb){ if(typeof festa === "function") festa();
      /* ⚠️ o banner do motor e quem leva a fase seguinte: a peca so avisa que
         acabou. Se ela passar um `cb` (a tela de fim dela), ele e IGNORADO —
         no esqueleto quem manda no caminho e o motor.                        */
      setTimeout(function(){ fim(); }, 420); }
    limpa();
%(corpo)s
  })();
};
'''


def main():
    escrever = "--escrever" in sys.argv
    prontas, sem_porta, sem_gaveta = [], [], []
    gavetas = {}
    js_out, css_out = [], []

    for arq in sorted(os.listdir(PECAS)):
        if not arq.endswith(".html") or arq == "MOLDE.html":
            continue
        nome = arq[:-5]
        html = io.open(os.path.join(PECAS, arq), encoding="utf-8").read()
        js = js_da_peca(html)
        porta = entrada(js)
        if not porta:
            sem_porta.append(nome)
            continue
        gav = gaveta(js)
        # ⭐ AQUI a atividade deixa de ser código: a última linha da peça (a
        #    chamada dela mesma) vira "troque o conteúdo de exemplo pelo desta
        #    fase, DEPOIS comece". A peça não sabe de nada; nada nela mudou.
        abre = "    " + porta + "();"
        if gav:
            abre = ("    if(f && f.dados) %s = f.dados;\n" % gav) + abre
        else:
            sem_gaveta.append(nome)
        corpo = re.sub(r"^\s*%s\s*\(\s*\)\s*;\s*$" % re.escape(porta),
                       abre, js, flags=re.M)
        gavetas[nome] = gav
        js_out.append(PONTE % {"nome": nome, "corpo": corpo})
        # o CSS leva a MESMA marca: o montador recorta peça inteira, nunca
        # regra a regra (um `@media{` que perdesse as regras de dentro deixaria
        # um `}` solto e derrubaria a folha inteira da atividade)
        css_out.append((MARCA % nome) + u"\n" + prefixa_css(css_da_peca(html), nome))
        prontas.append(nome)

    print(u"INTEGRACAO DAS PECAS")
    print(u"  %d peca(s) com porta de entrada -> viram MEC[...]" % len(prontas))
    print(u"  %d com gaveta de conteudo (aceitam `dados` do conteudo.json)"
          % (len(prontas) - len(sem_gaveta)))
    if sem_porta:
        print(u"  %d sem porta (nao chamam a propria funcao no fim): %s"
              % (len(sem_porta), ", ".join(sem_porta)))
    if sem_gaveta:
        print(u"  %d SEM GAVETA — vao rodar com o conteudo de EXEMPLO delas: %s"
              % (len(sem_gaveta), ", ".join(sem_gaveta)))
    if not escrever:
        print(u"  (--escrever para gerar pecas.js e pecas.css)")
        return 0

    # o mapa das gavetas: é ele que o autor do conteudo.json consulta para saber
    # o formato de `dados` de cada mecânica (sem abrir 74 arquivos)
    io.open(os.path.join(AQUI, "pecas.json"), "w", encoding="utf-8").write(
        json.dumps({"gavetas": gavetas}, ensure_ascii=False, indent=1,
                   sort_keys=True))

    io.open(os.path.join(AQUI, "pecas.js"), "w", encoding="utf-8").write(
        u"/* GERADO por integrar.py — nao editar a mao */\n" + "".join(js_out))
    io.open(os.path.join(AQUI, "pecas.css"), "w", encoding="utf-8").write(
        u"/* GERADO por integrar.py — nao editar a mao */\n" + "\n".join(css_out))
    print(u"  escrito: pecas.js (%d KB) e pecas.css (%d KB)"
          % (sum(len(x) for x in js_out) // 1024,
             sum(len(x) for x in css_out) // 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
