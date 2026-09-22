/* ============================================================
   AS FALAS DESTA PROVA SAEM DO PRÓPRIO APP — nunca de uma lista à mão

   ⚠️ POR QUE ISTO EXISTE. O `falas.json` desta prova nasceu escrito à mão e
      ficou órfão: mexer numa alternativa, num título de ficha ou na fala do
      Léo deixava o texto da tela e o texto gravado em desacordo — e o defeito
      NÃO APARECE em lugar nenhum. O alto-falante simplesmente não toca: sem
      erro no console, sem 404 visível num print, sem portão vermelho. É o
      "silêncio", o único defeito desta casa que não deixa marca.

   O QUE ELE FAZ: lê o `index.html`, roda o JS de dados do próprio app (com o
   navegador simulado no mínimo), e monta o `falas.json` chamando as MESMAS
   funções que a tela chama — `paraVoz` (o "tângram"), `semTag` (o negrito que
   é da tela e não da voz) e `_chaveVoz` (o hash que dá nome ao mp3).
   Não há um segundo lugar onde a regra esteja escrita.

   Uso:  node _efjogos/gerar_falas.js
   ============================================================ */
"use strict";
var fs = require("fs");
var path = require("path");
var vm = require("vm");

var AQUI = __dirname;
var html = fs.readFileSync(path.join(AQUI, "index.html"), "utf8");

var i0 = html.indexOf("<script>");
var i1 = html.lastIndexOf("</script>");
if (i0 < 0 || i1 < 0) { console.error("nao achei o <script> do app"); process.exit(2); }
var js = html.slice(i0 + "<script>".length, i1);

/* O app chama `boot()` no fim, que desenha a capa. Aqui não há tela: um
   documento de mentira basta para o arquivo rodar até o fim sem estourar. */
function noh() {
  return { style: {}, innerHTML: "", value: "", className: "", title: "", scrollTop: 0,
           focus: function () {}, appendChild: function () {},
           getContext: function () { return null; } };
}
var falso = {
  getElementById: function () { return noh(); },
  getElementsByClassName: function () { return []; },
  createElement: function () { return noh(); },
  addEventListener: function () {},
  body: { appendChild: function () {} }
};
var caixa = {
  document: falso,
  window: { addEventListener: function () {}, innerWidth: 900, innerHeight: 700 },
  localStorage: { getItem: function () { return null; }, setItem: function () {} },
  Audio: function () { return { play: function () {} }; },
  XMLHttpRequest: function () { return { open: function () {}, setRequestHeader: function () {}, send: function () {} }; },
  requestAnimationFrame: function () {},
  console: console,
  Math: Math, Date: Date, JSON: JSON, String: String, Number: Number
};
caixa.self = caixa;
vm.createContext(caixa);
try { vm.runInContext(js, caixa, { filename: "_efjogos/index.html" }); }
catch (e) { console.error("o JS do app nao rodou: " + e.message); process.exit(2); }

var falas = [];
var vistos = {};
function poe(texto, deonde) {
  var limpo = caixa.semTag(texto);
  var chave = caixa._chaveVoz(caixa.paraVoz(limpo));
  if (vistos[chave]) { return; }          /* texto repetido = um mp3 só */
  vistos[chave] = true;
  falas.push({ id: chave, texto: caixa.paraVoz(limpo), _de: deonde });
}

/* 1. a apresentação do Léo, na capa */
poe(caixa.HISTORIA, "capa");

/* 2. os avisos da capa (o que ele diz quando falta preencher algo) */
["Escreva o seu nome para começar.", "Escolha o seu ano.",
 "Escolha a sua turma.", "Escolha o seu personagem."].forEach(function (t) { poe(t, "capa/aviso"); });

/* 3. OS DOIS TEXTOS.
   ⚠️ São QUATRO coisas faladas em cada texto, e esquecer uma deixa um botão
      mudo sem dar erro nenhum:
        · a abertura que o Léo diz ao abrir o texto (`PARTES[n].abre`);
        · o SUBTÍTULO sozinho — é o que a leitura corrida (`lerTextoTodo`) diz
          ao entrar em cada assunto, e ele não aparece em nenhum outro lugar;
        · o bloco inteiro (título + frases), que é o que o botão "ver no texto"
          da prova toca;
        · cada frase sozinha, que é o alto-falante ao lado dela. */
caixa.PARTES.forEach(function (P, n) { poe(P.abre, "texto" + (n + 1) + "/abertura"); });
caixa.ESTUDO.forEach(function (f, i) {
  poe(f.titulo + ".", "bloco" + (i + 1) + "/subtitulo");
  poe(caixa.falaDaFicha(i), "bloco" + (i + 1));
  f.linhas.forEach(function (l, k) { poe(l, "bloco" + (i + 1) + "/frase" + (k + 1)); });
});

/* 4. AS QUESTÕES: a pergunta com as quatro letras + cada alternativa sozinha */
caixa.QUESTOES.forEach(function (q, i) {
  poe(caixa.falaDaQuestao(i), "q" + (i + 1));
  q.opcoes.forEach(function (o, k) { poe(o, "q" + (i + 1) + "/op" + (k + 1)); });
});

/* 5. o que ele diz entre uma pergunta e outra, e no fim */
["Próxima pergunta!", "Vamos continuar!", "Muito bem, siga em frente!", "Continue!",
 "Prontinho! Você terminou a prova. O Léo adorou jogar com você. Parabéns!"
].forEach(function (t) { poe(t, "passagem"); });

/* o campo `_de` é só para quem lê o arquivo; o gravador usa id + texto */
fs.writeFileSync(path.join(AQUI, "falas.json"),
  JSON.stringify(falas.map(function (f) { return { id: f.id, texto: f.texto }; }), null, 1) + "\n",
  "utf8");

console.log(falas.length + " falas em _efjogos/falas.json");
console.log("   " + caixa.PARTES.length + " textos (" + caixa.ESTUDO.length + " blocos), " + caixa.QUESTOES.length + " questoes");
