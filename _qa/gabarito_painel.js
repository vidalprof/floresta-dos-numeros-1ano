/* ============================================================
   PORTÃO — "o painel do professor mede a MESMA prova que a criança fez?"

   ⚠️ DE ONDE ELE NASCE. O painel de uma prova guarda, num bloco `/*DADOS-INI*​/`,
      o GABARITO (a alternativa certa de cada questão) e os EIXOS (o assunto de
      cada uma). É com isso que ele monta o "Onde a turma tropeçou". Só que a
      alternativa certa TAMBÉM está escrita na prova, no campo `correta` de cada
      questão — e essa é a família de defeitos que este projeto passa o tempo a
      fechar: o mesmo número em dois lugares sempre acaba divergindo.

      Aqui o estrago é pior do que o normal e é silencioso: a NOTA do aluno sai
      da prova e continua certa, então nada parece quebrado. O que fica errado é
      o diagnóstico — o painel diz que a turma errou a questão 8, o professor
      reensina a questão 8, e o buraco estava na 11. Um erro que faz o professor
      gastar aula com a coisa errada não dá tela vermelha nenhuma.

   O QUE ELE FAZ: abre a prova, roda o JS dela de verdade (não regex), lê
   `QUESTOES` e `DISCNOME`, e compara com o que o painel declara. Diferença de
   gabarito, de assunto, de quantidade de questões ou de turmas REPROVA.

   COM `--escrever`: em vez de conferir, ESCREVE o bloco de dados do painel a
   partir da prova e do `curriculo.json`. É assim que o painel nasce — ninguém
   copia gabarito à mão.

   uso:  node _qa/gabarito_painel.js <pastaProva> <pastaPainel> [--escrever]
   saída: 0 passou · 1 REPROVADO · 2 NÃO MEDI (que não é "passou")
   ============================================================ */
const fs = require("fs");
const path = require("path");
const vm = require("vm");

function leProva(pasta) {
  const arq = path.join(pasta, "index.html");
  if (!fs.existsSync(arq)) return { erro: "não achei " + arq };
  const html = fs.readFileSync(arq, "utf8");
  const js = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)]
    .map((m) => m[1]).join("\n");
  /* o boot desenha na tela; sem DOM ele estoura. Tira-se só a última chamada. */
  const corpo = js.replace(/\nboot\(\);\s*$/, "\n");
  const caixa = {
    window: {}, console,
    document: { addEventListener() {}, getElementById() { return null; } },
    localStorage: { getItem() { return null; }, setItem() {} },
  };
  vm.createContext(caixa);
  try { vm.runInContext(corpo, caixa); } catch (e) { return { erro: "o JS da prova estourou: " + e.message }; }
  if (!Array.isArray(caixa.QUESTOES)) return { erro: "a prova não expõe `var QUESTOES`" };
  return { q: caixa.QUESTOES, nomes: caixa.DISCNOME || {}, slug: caixa.SLUG || "" };
}

function dadosDoPainel(pasta) {
  const arq = path.join(pasta, "index.html");
  if (!fs.existsSync(arq)) return { erro: "não achei " + arq };
  const html = fs.readFileSync(arq, "utf8");
  const m = html.match(/\/\*DADOS-INI\*\/([\s\S]*?)\/\*DADOS-FIM\*\//);
  if (!m) return { erro: "o painel não tem o bloco /*DADOS-INI*/.../*DADOS-FIM*/" };
  const caixa = { console };
  vm.createContext(caixa);
  try { vm.runInContext(m[1], caixa); } catch (e) { return { erro: "o bloco de dados do painel estourou: " + e.message }; }
  return caixa;
}

function eixosDaProva(p) {
  return p.q.map((q) => p.nomes[q.disc] || q.disc || "—");
}

function escreve(pastaProva, pastaPainel, p) {
  const cj = path.join(pastaProva, "curriculo.json");
  const curric = fs.existsSync(cj) ? JSON.parse(fs.readFileSync(cj, "utf8")) : null;
  const arq = path.join(pastaPainel, "index.html");
  const html = fs.readFileSync(arq, "utf8");
  const velho = dadosDoPainel(pastaPainel);
  const titulo = velho.TITULO, turmas = velho.TURMAS, csv = velho.ARQCSV;
  if (!titulo || !turmas || !csv) {
    console.log("NAO MEDI: para escrever, o painel precisa já ter TITULO, TURMAS e ARQCSV no bloco de dados.");
    return 2;
  }
  const bloco =
    "/*DADOS-INI*/\n" +
    "/* ⚠️ ESTE BLOCO É GERADO, NÃO EDITADO À MÃO:\n" +
    "     node _qa/gabarito_painel.js " + pastaProva + " " + pastaPainel + " --escrever\n" +
    "   O GABARITO e os EIXOS saem da PRÓPRIA prova (campos `correta` e `disc`),\n" +
    "   e o mesmo comando, sem `--escrever`, é o portão que reprova se um dia os\n" +
    "   dois discordarem. Mexeu na prova, rode de novo. */\n" +
    "var TITULO=" + JSON.stringify(titulo) + ";\n" +
    "var TURMAS=" + JSON.stringify(turmas) + ";\n" +
    "var GABARITO=" + JSON.stringify(p.q.map((q) => q.correta)) + ";\n" +
    "var EIXOS=" + JSON.stringify(eixosDaProva(p)) + ";\n" +
    "var ARQCSV=" + JSON.stringify(csv) + ";\n" +
    "var CURRICULO=" + (curric ? JSON.stringify(curric) : "null") + ";\n" +
    "/*DADOS-FIM*/";
  fs.writeFileSync(arq, html.replace(/\/\*DADOS-INI\*\/[\s\S]*?\/\*DADOS-FIM\*\//, bloco));
  console.log("bloco de dados do painel ESCRITO a partir de " + pastaProva +
    ": " + p.q.length + " questões, " + new Set(eixosDaProva(p)).size + " assuntos" +
    (curric ? ", currículo junto" : ", SEM currículo (não há curriculo.json)"));
  return 0;
}

function main() {
  const arg = process.argv.slice(2);
  const escrever = arg.indexOf("--escrever") >= 0;
  const alvos = arg.filter((a) => a.charAt(0) !== "-");
  if (alvos.length < 2) {
    console.log("uso: node _qa/gabarito_painel.js <pastaProva> <pastaPainel> [--escrever]");
    return 2;
  }
  const [pastaProva, pastaPainel] = alvos;
  const p = leProva(pastaProva);
  if (p.erro) { console.log(pastaProva + " -> NAO MEDI: " + p.erro + ' (isso nao e "passou").'); return 2; }
  if (escrever) return escreve(pastaProva, pastaPainel, p);

  const d = dadosDoPainel(pastaPainel);
  if (d.erro) { console.log(pastaPainel + " -> NAO MEDI: " + d.erro + ' (isso nao e "passou").'); return 2; }

  const gabProva = p.q.map((q) => q.correta);
  const eixProva = eixosDaProva(p);
  const erros = [];

  if (!Array.isArray(d.GABARITO)) erros.push("o painel não declara GABARITO.");
  else if (d.GABARITO.length !== gabProva.length) {
    erros.push("a prova tem " + gabProva.length + " questões e o painel mede " +
      d.GABARITO.length + ". O 'onde a turma tropeçou' fica deslocado.");
  } else {
    gabProva.forEach((c, i) => {
      if (d.GABARITO[i] !== c) {
        erros.push("questão " + (i + 1) + ": a prova diz que a certa é a letra " +
          "ABCD".charAt(c) + " e o painel corrige como " + "ABCD".charAt(d.GABARITO[i]) + ".");
      }
    });
  }
  if (Array.isArray(d.EIXOS)) {
    if (d.EIXOS.length !== eixProva.length) {
      erros.push("a prova tem " + eixProva.length + " assuntos e o painel lista " + d.EIXOS.length + ".");
    } else {
      eixProva.forEach((e, i) => {
        if (d.EIXOS[i] !== e) {
          erros.push("questão " + (i + 1) + ": na prova o assunto é \"" + e +
            "\" e no painel \"" + d.EIXOS[i] + "\".");
        }
      });
    }
  }
  /* o currículo aponta questões por número: número fora da prova é conta errada */
  if (d.CURRICULO && Array.isArray(d.CURRICULO.objetivos)) {
    const vistas = {};
    d.CURRICULO.objetivos.forEach((o) => (o.questoes || []).forEach((n) => {
      if (n < 1 || n > gabProva.length) {
        erros.push("o currículo do painel aponta a questão " + n + ", que não existe (a prova tem " + gabProva.length + ").");
      }
      vistas[n] = (vistas[n] || 0) + 1;
    }));
    for (let n = 1; n <= gabProva.length; n++) {
      if (!vistas[n]) erros.push("a questão " + n + " não é medida por objetivo nenhum do currículo.");
      else if (vistas[n] > 1) erros.push("a questão " + n + " aparece em " + vistas[n] + " objetivos do currículo.");
    }
  }

  if (erros.length) {
    console.log(pastaPainel + " -> REPROVADO: o painel nao mede a prova que a crianca faz");
    erros.forEach((e) => console.log("   - " + e));
    console.log("   conserto: node _qa/gabarito_painel.js " + pastaProva + " " + pastaPainel + " --escrever");
    return 1;
  }
  console.log(pastaPainel + " -> gabarito do painel ok: " + gabProva.length +
    " questoes conferidas contra " + pastaProva + " (resposta certa, assunto e as questoes que o curriculo aponta)");
  return 0;
}

process.exit(main());
