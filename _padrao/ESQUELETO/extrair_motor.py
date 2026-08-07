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
         "QUALP", "ORDEMJD", "CICLOJD", "PRECISAJD", "SERVEJD", "ROTJD",
         # ⚠️ estes quatro são a CARA do "resto de clone" e escaparam na 1ª
         #    extração: são mapas de CONCEITO do Broto (luz_agua, sequencia...)
         #    e — pior — o TREINO apontava para telas que já não existiam. A
         #    atividade abria bonita, o `node --check` passava, e a criança
         #    chegava ao boletim e a tela morria em `fracos()`. No esqueleto os
         #    quatro NASCEM da lista de fases (ver `preparaIdentidade`).
         "DOM", "ROTCRI", "TREINO", "FASES_MESTRE",
         # achados pela CONFERENCIA abaixo, que varre o motor atras de marca do
         # Broto: dados de conteudo que nao estavam dentro de nenhuma tela
         "PLAQLADO", "RODA", "ZONAS", "PARTES", "FUNCOES"]

# ⚠️ AS TROCAS DE IDENTIDADE — o coração do "nunca mais resto de clone".
#    Cada linha aqui é uma marca do Broto que estava ESCRITA no motor e que, se
#    ficasse, viajaria para toda atividade que o esqueleto gerasse: o prefixo
#    das figuras, a chave do localStorage (e no GitHub Pages TODAS as atividades
#    dividem a MESMA origem — duas com a chave "jardim_med" se apagariam uma à
#    outra), o crachá, o nome do mascote, as vozes de elogio e consolo, o fundo.
#    Viram consultas ao `ID`, que o montador escreve a partir do conteudo.json.
TROCAS = [
    (r'localStorage\.setItem\("jardim_med"', 'localStorage.setItem(ID.pre+"_med"'),
    (r'localStorage\.getItem\("jardim_med"', 'localStorage.getItem(ID.pre+"_med"'),
    (r'perfil\.fig\.indexOf\("jd_cr"\)!==0\) perfil\.fig="jd_cr1"',
     'perfil.fig.indexOf(ID.pre+"_cr")!==0) perfil.fig=ID.pre+"_cr1"'),
    (r'imgEl\("jd_broto_feliz","lay base"\), fala=imgEl\("jd_broto_fala","lay fala"\), '
     r'pisca=imgEl\("jd_broto_pisca","lay pisca"\)',
     'imgEl(ID.pre+"_"+ID.mascote+"_feliz","lay base"), '
     'fala=imgEl(ID.pre+"_"+ID.mascote+"_fala","lay fala"), '
     'pisca=imgEl(ID.pre+"_"+ID.mascote+"_pisca","lay pisca")'),
    (r'var n=\["jd_acerto1","jd_acerto2","jd_acerto3"\]',
     'var n=[ID.pre+"_acerto1",ID.pre+"_acerto2",ID.pre+"_acerto3"]'),
    (r'falar\(Math\.random\(\)<0\.5\?"jd_erro1":"jd_erro2"\)',
     'falar(Math.random()<0.5?ID.pre+"_erro1":ID.pre+"_erro2")'),
    (r'"O Jardim do Broto"', 'ID.titulo'),
    (r'O Jardim do Broto &#8212; parecer', '"+ID.titulo+" &#8212; parecer'),
    (r'"Ci&#234;ncias &#183; 2&#186; ano &#183; As plantas"', 'ID.sub'),
    (r'\{nome:"",fig:"jd_cr1"\}', '{nome:"",fig:ID.pre+"_cr1"}'),
    # o CRACHA: a tela "Quem vai jogar?" trazia as 6 criancas do Jardim. Regra
    # do Marcos: "nunca copiar avatar de outra atividade — sempre novo e
    # tematico". Aqui a lista se MONTA do prefixo, entao nao ha o que copiar.
    (r'var lista=\["jd_cr1","jd_cr2","jd_cr3","jd_cr4","jd_cr5","jd_cr6"\];',
     'var lista=[],_c;for(_c=1;_c<=ID.crachas;_c++) lista.push(ID.pre+"_cr"+_c);'),
    (r'falar\("jd_fim"\)', 'falar(ID.pre+"_fim")'),
    # o fundo estava CRAVADO no CSS (`url(img/jd_fundo.jpg)`) — nenhum portão de
    # JS olha para lá, e ele viajaria calado para todas as atividades
    (r'background-image:url\(img/jd_fundo\.jpg\)', 'background-image:none'),
    (r'var MASCOTE_NOME="Broto";', 'var MASCOTE_NOME="";  /* ID.mascoteNome */'),
    # ⚠️ a PRE-CARGA e a VOZ das respostas do Broto: as duas primeiras da lista
    #    do CLONAR-MOTOR.md. Ficam VAZIAS aqui; o montador escreve as desta
    #    atividade. E a pre-carga deixa de rodar sozinha (IIFE) e vira funcao,
    #    porque agora ela so pode rodar DEPOIS que a lista existir.
    (r'var IMGS=\[[^\]]*\];', 'var IMGS=[];'),
    (r'var IMG=\{\};\(function\(\)\{var i;for\(i=0;i<IMGS\.length;i\+\+\)'
     r'\{var im=new Image\(\);im\.src="img/"\+IMGS\[i\]\+"\.png";'
     r'IMG\[IMGS\[i\]\]=im;\}\}\)\(\);',
     'var IMG={};function precarrega(){var i;for(i=0;i<IMGS.length;i++)'
     '{var im=new Image();im.src="img/"+IMGS[i]+".png";IMG[IMGS[i]]=im;}}'),
    (r'var VOZOK=\{[^}]*\};', 'var VOZOK={};'),
    # ⚠️ o Broto abre a capa na ULTIMA linha do JS dele — que, no esqueleto,
    #    vem ANTES do condutor. A capa abria antes de as fases existirem.
    (r'if\(location\.search\.indexOf\("painel"\)>=0\)\{ telaPainel\(\); \}'
     r' else \{ telaCapa\(\); \}', '/* o boot mudou de lugar: ver inicia() */'),
]

# ⚠️ A PARTIDA VAI PARA O FIM DA FILA, e isto NAO e detalhe: as pecas e o
#    conteudo (FASES, ID, IMGS) sao escritos pelo montador DEPOIS do condutor.
#    Chamando `inicia()` direto, ele rodava com `FASES` ainda vazia — a capa
#    abria bonita, mas o menu do professor (senha 1275@) nascia sem nenhuma
#    fase, o boletim do fim sem nenhum objetivo e a pre-carga sem nenhuma
#    figura. Nada disso da erro, e o auditor-jogador nao ve (ele nunca abre o
#    menu do professor). O `setTimeout(...,0)` espera o arquivo inteiro ser
#    lido — e funciona tanto na atividade montada quanto no motor sozinho.
PARTIDA = u"\nsetTimeout(inicia, 0);\n"

# ⚠️ O `ID` PRECISA EXISTIR ANTES DO BOOT: `carregaEstado()` e `var perfil` rodam
#    no meio do motor, muito antes do CONDUTOR (que e acrescentado no fim). Se o
#    `ID` so nascesse la, a atividade morria na primeira linha com "ID is not
#    defined". Por isso ele e PREPENDIDO.
CABECA = u'''/* ====== A IDENTIDADE DESTA ATIVIDADE ======
   Tudo o que era a marca do Jardim do Broto dentro do motor (o prefixo das
   figuras, a chave do localStorage, o cracha, o nome do mascote, as vozes de
   elogio e consolo, o titulo, o fundo) vira consulta a este objeto. O montador
   o reescreve a partir do conteudo.json.

   ⚠️ A chave do localStorage E CRITICA: no GitHub Pages TODAS as atividades
   moram na MESMA origem (vidalprof.github.io). Duas atividades com a chave
   "jardim_med" apagariam o progresso uma da outra na mesma tarde. */
var ID = {pre:"skel", mascote:"mascote", mascoteNome:"", titulo:"Atividade",
          sub:"", fundo:"", crachas:6};
'''



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

function montaFase(i, aoFim){
  IFASE = i;
  /* ⚠️ LICAO PAGA: quatro portoes da banca (contraste, leiaute, encaixe e
     imagem quebrada) abrem CADA tela chamando a funcao dela — inclusive sem
     argumento. `montaFase()` virava `FASES[undefined]`, e a linha seguinte
     estourava lendo `.selo` de `undefined`. Quatro portoes cegos de uma vez,
     e a atividade "passava" por nao ter sido medida. Fase que nao existe leva
     ao fim, nunca a uma tela morta. */
  if(!(i >= 0) || i >= FASES.length || !FASES[i]){ telaFim(); return; }
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
  m(f, cen, aoFim);
}

function abreFase(i){
  montaFase(i, function(){ salvaEstado(); abreFase(i + 1); });
}
/* a MESMA fase, mas no percurso do "Treinar o que faltou": ao acabar ela volta
   para a fila do treino, nao para a fase seguinte da atividade */
function abreFaseTreino(i){ montaFase(i, function(){ salvaEstado(); proximoTreino(); }); }

/* ============================================================
   OS QUATRO MAPAS QUE ERAM DO BROTO — agora NASCEM da lista de fases.

   `DOM` (o quanto a crianca domina cada objetivo), `ROTCRI` (o nome do objetivo
   em linguagem de crianca, para o boletim), `TREINO` (qual fase refazer quando
   o objetivo ficou fraco) e `FASES_MESTRE` (o menu da senha 1275@).

   ⚠️ LICAO PAGA, e das caras: na primeira extracao os quatro FICARAM com o
   conteudo do Broto (luz_agua, sequencia, partes...) e o `TREINO` apontava para
   telas que ja tinham sido removidas. A atividade abria bonita, o `node --check`
   passava, o print ficava perfeito — e a crianca chegava ao BOLETIM DO FIM e a
   tela morria em `fracos()`. Foi o auditor-jogador que pegou, jogando ate o fim.
   ============================================================ */
var DOM = {}, ROTCRI = {}, TREINO = {}, FASES_MESTRE = [];

function preparaIdentidade(){
  var i, f, c;
  /* ⚠️ a ORDEM importa: primeiro o que a crianca ja tinha feito (a retomada de
     55 min), DEPOIS os objetivos que faltarem. Ao contrario, o `DOM={}` novo
     apagava o progresso salvo — a criança voltava e o boletim estava zerado. */
  carregaEstado();
  for(i = 0; i < FASES.length; i++){
    f = FASES[i];
    /* o menu do professor guarda o NOME de uma funcao global (e assim que o
       telaMestre do Broto o le) — entao cada fase ganha a sua */
    window["_f" + i] = (function(k){ return function(){ abreFase(k); }; })(i);
    FASES_MESTRE.push(["_f" + i, (i + 1) + ". " + semTag(f.selo || f.id)]);
    c = f.conceito;
    if(!c) continue;
    if(!DOM.hasOwnProperty(c)) DOM[c] = 0.3;      /* objetivo novo desta versao */
    if(!ROTCRI[c]) ROTCRI[c] = ROTULOS[c] || c;   /* nome em lingua de crianca */
    if(!TREINO[c]) TREINO[c] =
      (function(k){ return function(){ abreFaseTreino(k); }; })(i);
  }
  /* o fundo saiu do CSS (era `url(img/jd_fundo.jpg)`, cravado) e virou dado:
     assim ele nao viaja calado para a proxima atividade */
  if(ID.fundo){ var bg = document.getElementById("bg");
    if(bg) bg.style.backgroundImage = "url(img/" + ID.fundo + ")"; }
  window["_ffim"] = function(){ telaFim(); };
  FASES_MESTRE.push(["_ffim", (FASES.length + 1) + ". FIM"]);
  precarrega();
}
var ROTULOS = {};   /* conceito -> nome de crianca (o montador escreve) */
function semTag(h){ return String(h || "").replace(/<[^>]+>/g, ""); }

/* o motor so comeca DEPOIS que a identidade e as fases existem — a linha
   original do Broto abria a capa antes disso (ver TROCAS) */
function inicia(){
  preparaIdentidade();
  if(location.search.indexOf("painel") >= 0){ telaPainel(); } else { telaCapa(); }
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

    css = css_orig = "".join(re.findall(r"<style>(.*?)</style>", html, re.S))
    # ⚠️ o CSS TAMBEM carrega marca do Broto (`url(img/jd_fundo.jpg)`) e nenhum
    #    portao de JS olha para la — passaria calado para toda atividade
    for alvo, troco in TROCAS:
        css = re.sub(alvo, troco.replace("\\", "\\\\"), css)

    fora.sort(reverse=True)
    novo = js
    for a, b in fora:
        novo = novo[:a] + novo[b:]
    nao_pegou = []
    for alvo, troco in TROCAS:
        novo, n = re.subn(alvo, troco.replace("\\", "\\\\"), novo)
        if not n and not re.search(alvo, css_orig):
            nao_pegou.append(alvo)
    novo = CABECA + novo + "\n" + CONDUTOR + PARTIDA

    # ⭐ A CONFERENCIA — o extrator NAO escreve um motor que ainda carregue a
    #    marca do Broto. Sem isto, cada marca esquecida aqui viraria "resto de
    #    clone" em TODA atividade que o esqueleto gerasse: uma so falha,
    #    multiplicada por todas. E a versao automatica da ordem do Marcos
    #    ("favor nao poder mais haver resto do clone").
    #    ⚠️ so o CODIGO conta: os comentarios do proprio esqueleto dizem, de
    #    proposito, que ele NASCEU do Jardim do Broto — e isso e memoria, nao
    #    resto. O que nao pode e a marca chegar em algo que a criança vê.
    codigo = re.sub(r"/\*.*?\*/", " ", novo + "\n" + css, flags=re.S)
    codigo = re.sub(r"(?m)^\s*//.*$", " ", codigo)
    sobrou = sorted(set(re.findall(r"jd_[a-z0-9_]+", codigo)
                        + re.findall(r"Broto", codigo)))
    print(u"EXTRACAO DO MOTOR")
    for a in nao_pegou:
        print(u"  ⚠️ TROCA QUE NAO PEGOU (o Broto mudou?): %s" % a[:66])
    print(u"  origem: _jardim/index.html (%d funcoes)" % len(fun))
    print(u"  saiu:   %d bloco(s) de conteudo (%d KB)"
          % (len(fora), (len(js) - len(novo) + len(CONDUTOR)) // 1024))
    print(u"  motor:  %d KB de JS" % (len(novo) // 1024))
    if sobrou:
        print(u"  ✗ MARCA DO BROTO NO MOTOR (%d) — nada foi escrito: %s"
              % (len(sobrou), ", ".join(sobrou[:14])))
        print(u"    ponha na lista DADOS (se for dado) ou em TROCAS (se for "
              u"identidade) e rode de novo.")
        return 1
    print(u"  limpo: nenhuma marca do Broto sobrou no motor")
    if "--so-ver" in sys.argv:
        print(u"  (--so-ver: nada escrito)")
        return 0

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
