#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""EXTRAI O MOTOR DO JARDIM DO BROTO — o esqueleto nasce dele, não de mim.

Ordem do Marcos (ago/2026): *"o nosso modelo de atividade é a atividade do Broto
por enquanto"* — e ele mesmo disse: *"achei que a atividade do Broto está
perfeita"*.

Então o motor do esqueleto **não se escreve do zero**: extrai-se do Broto. É
código que já passou por ele, pela banca e pelas crianças. Escrever de novo seria
jogar fora essa prova e reintroduzir defeitos já pagos.

O QUE FICA (a espinha, 65 funções):
  telaCapa · telaQuem (o crachá) · telaFim (boletim + medalha) ·
  segredoRelatorio (o relatório do professor que abre segurando a medalha) ·
  telaMestre (a senha 1275@) · telaPainel · resumoAnimado · treinarFracos ·
  fracos · parecerDe · reg (a medição) · ajudaJd (o andaime que cresce) ·
  falar/falaDaTela/depoisDaFala/montaBarra · o alto-falante das respostas
  (VOZOK/chaveVoz/poeZap) · o mascote com lip-sync · salvaEstado · os sons.

O QUE SAI (o conteúdo do Broto, 23 telas):
  telaPlantar, telaComemos, telaPrato, telaQualParte, telaRotular... — tudo o que
  fala de planta. No lugar delas entra o CONDUTOR: as fases viram DADOS, e cada
  mecânica é uma entrada em `MEC[...]`, vinda das peças de `_padrao/pecas/`.

⚠️ Este arquivo é a FERRAMENTA, não o motor. Rodá-lo gera
   `_padrao/ESQUELETO/motor.html`. Se o Broto mudar, roda-se de novo.

Uso:  python3 _padrao/ESQUELETO/extrair_motor.py
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORIGEM = os.path.join(RAIZ, "_jardim", "index.html")
DESTINO = os.path.join(RAIZ, "_padrao", "ESQUELETO", "motor.html")

# as telas que são CONTEÚDO do Broto (falam de planta) — saem
CONTEUDO = set("""
telaAbertura telaP1prever telaPlantar telaExperimento telaOrdenar telaCiclo
telaAquecimento telaPrecisa telaPartesBase telaPartes telaFuncoes telaRotular
telaServe telaMontaPalavra telaComemos telaPrato telaQualParte telaMemoria
telaCacaBase telaCacaJd telaCacaPartes telaEnsinar telaRelampagoJd
""".split())

# os dados que são conteúdo do Broto — saem junto
DADOS = ["COMER", "PARTES6", "MONTAJD", "MEMJD", "RELAJD", "CACAJD", "CACAPARTES",
         "QUALP", "ORDEMJD", "CICLOJD", "PRECISAJD", "SERVEJD", "ROTJD"]


def blocos_de_funcao(js):
    u"""onde cada função começa e termina, contando chaves."""
    out = {}
    for m in re.finditer(r"^function\s+([\w$]+)\s*\(", js, re.M):
        n = m.group(1)
        j = js.find("{", m.end())
        k, p = j, 0
        while k < len(js):
            if js[k] == "{":
                p += 1
            elif js[k] == "}":
                p -= 1
                if p == 0:
                    break
            k += 1
        out[n] = (m.start(), k + 1)
    return out


def bloco_de_var(js, nome):
    u"""onde uma `var NOME = [...]` começa e termina (conta colchetes/chaves)."""
    m = re.search(r"^var\s+%s\s*=" % re.escape(nome), js, re.M)
    if not m:
        return None
    k = m.end()
    p = 0
    aberto = False
    while k < len(js):
        c = js[k]
        if c in "[{":
            p += 1
            aberto = True
        elif c in "]}":
            p -= 1
        elif c == ";" and (not aberto or p == 0):
            return (m.start(), k + 1)
        if aberto and p == 0 and c in "]}":
            # segue até o ; final
            while k < len(js) and js[k] != ";":
                k += 1
            return (m.start(), k + 1)
        k += 1
    return None


CONDUTOR = u'''
/* ============================================================
   O CONDUTOR — as 32 fases viram DADOS, não código.

   Aqui estava o conteudo do Jardim do Broto (23 telas que falam de planta).
   No lugar delas entra isto: o motor le a lista `FASES` (que o montador escreve
   a partir do `conteudo.json`) e chama a mecanica de cada uma, registrada em
   `MEC`. Cada mecanica vem de uma peca ja aprovada em `_padrao/pecas/`.

   O que o motor entrega PRONTO antes de chamar a mecanica (ver CONTRATO.md):
   a tela limpa, a barra na posicao certa, o selo, o enunciado FALADO, o `cen`
   onde desenhar, a barra de dica com a voz dela, o andaime `ajuda(n)` e a
   medicao `reg(...)`. A mecanica so desenha e chama `fim()`.
   ============================================================ */
/* ⚠️ a ABERTURA era conteudo do Broto ("Oi! Eu sou o Broto, o meu jardim esta
   vazio..."). No esqueleto ela e DADO: o montador escreve `ABERTURA` a partir do
   `conteudo.json`, e o motor so a apresenta. Sem esta funcao a capa chamava uma
   tela que nao existia mais — a crianca tocava em COMECAR e nada acontecia. */
var ABERTURA = {texto:"", voz:null};
function telaAbertura(){
  limpa(); var t=el("div","tela"); setProg(t,3);
  var c=el("div","centro");
  if(typeof brotoEl==="function") c.appendChild(brotoEl("feliz"));
  c.appendChild(el("div","balao", ABERTURA.texto||""));
  var b=el("button","btn amarelo","Vamos!");
  b.onclick=function(){ arma(); sTap(); abreFase(0); };
  c.appendChild(b);
  t.appendChild(c); app.appendChild(t);
  montaBarra(null,null);
  if(ABERTURA.voz) falar(ABERTURA.voz);
}

var MEC = {};                 /* nome da mecanica -> function(f, cen, fim) */
var FASES = [];               /* escrito pelo montador */
var IFASE = 0;

/* ⚠️ a barra tem que subir na ORDEM REAL de jogo — e ela e calculada da lista,
   nunca escrita a mao. Foi numero escrito a mao que fez a barra do 3o ano andar
   PARA TRAS em duas passagens. */
function progDaFase(i){ return Math.round(4 + 96 * (i / Math.max(1, FASES.length))); }

function abreFase(i){
  IFASE = i;
  if(i >= FASES.length){ telaFim(); return; }
  var f = FASES[i];
  limpa();
  var t = el("div","tela"); setProg(t, progDaFase(i));
  var cen = el("div","centro");
  if(f.selo) cen.appendChild(el("div","selo", f.selo));
  if(f.enunciado) cen.appendChild(el("div","balao", f.enunciado));
  t.appendChild(cen); app.appendChild(t);

  /* o andaime que cresce — o mesmo do Broto (ajudaJd), com a dica desta fase */
  var err = 0;
  window.ajuda = function(n, ops){
    ops = ops || {};
    if(n === 1){ if(f.dica) mostraDica(f.dica); else if(ops.dica) mostraDica(ops.dica); }
    else if(n === 2){ consolo(); if(ops.concreto) ops.concreto(); }
    else if(n >= 3){ if(ops.revelar) ops.revelar();
      /* ⚠️ LICAO PAGA: revela PRIMEIRO, escreve a dica DEPOIS — senao a fase se
         conserta sozinha e a crianca nao sabe por que (achado em 5 de 6 pecas). */
      if(ops.porque) setTimeout(function(){ mostraDica(ops.porque); }, 60); }
  };
  window.regFase = function(ok, tent){ if(f.conceito) reg(f.conceito, ok, tent); };

  montaBarra(f.dicaVoz || null, f.dica || null);
  if(f.vozIntro) falar(f.vozIntro);

  var m = MEC[f.mec];
  if(!m){ /* mecanica que nao existe nao pode virar tela branca na mao da crianca */
    cen.appendChild(el("div","hint","(mecanica '"+f.mec+"' nao registrada)"));
    return; }
  m(f, cen, function(){ salvaEstado(); abreFase(i + 1); });
}
'''


def main():
    html = io.open(ORIGEM, encoding="utf-8").read()
    js_blocos = re.findall(r"<script>(.*?)</script>", html, re.S)
    js = "".join(js_blocos)
    fun = blocos_de_funcao(js)

    fora = []
    for n in CONTEUDO:
        if n in fun:
            fora.append(fun[n])
    for d in DADOS:
        b = bloco_de_var(js, d)
        if b:
            fora.append(b)

    fora.sort(reverse=True)
    novo = js
    for a, b in fora:
        novo = novo[:a] + novo[b:]
    novo += "\n" + CONDUTOR

    print(u"EXTRACAO DO MOTOR")
    print(u"  origem: _jardim/index.html (%d funcoes)" % len(fun))
    print(u"  saiu:   %d bloco(s) de conteudo (%d KB)"
          % (len(fora), (len(js) - len(novo) + len(CONDUTOR)) // 1024))
    print(u"  motor:  %d KB de JS" % (len(novo) // 1024))
    if "--so-ver" in sys.argv:
        print(u"  (--so-ver: nada escrito)")
        return 0

    css = "".join(re.findall(r"<style>(.*?)</style>", html, re.S))
    corpo = re.search(r"<body>(.*?)<script>", html, re.S)
    cab = (u"<!DOCTYPE html>\n<html lang=\"pt-BR\"><head>\n<meta charset=\"utf-8\">\n"
           u"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,"
           u"maximum-scale=1,user-scalable=no\">\n<title>MOTOR — esqueleto</title>\n"
           u"<!-- ⚠️ GERADO por _padrao/ESQUELETO/extrair_motor.py a partir do\n"
           u"     _jardim/index.html. NAO editar a mao: editar o Broto ou o\n"
           u"     extrator e gerar de novo. -->\n<style>\n")
    saida = (cab + css + u"\n</style></head>\n<body>\n"
             + (corpo.group(1) if corpo else u"<div id=\"app\"></div>\n")
             + u"<script>\n" + novo + u"\n</script>\n</body></html>\n")
    io.open(DESTINO, "w", encoding="utf-8").write(saida)
    print(u"  escrito: _padrao/ESQUELETO/motor.html (%d KB)" % (len(saida) // 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
