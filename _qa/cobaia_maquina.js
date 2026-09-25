/* Cobaia da MÁQUINA DE VIDRO: joga a aula 1 inteira e prova que ela termina.
   ⚠️ Prova o que print não prova: que o robô CHEGA, que o relatório aparece
      e que voltar do painel não deixa a tela morta. */
/* ⚠️ Mesmo caminho dos outros portões: o playwright e o Chromium moram fora do
   repo, e `require("playwright")` puro nao os acha. */
let chromium;
try { chromium = require("/opt/node22/lib/node_modules/playwright/index.js").chromium; }
catch(e) { chromium = require("playwright").chromium; }
const CROMO = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const path = require("path");
const ARQ = "file://" + path.resolve("_comp3/index.html");
const SOL = {
  1:["ANDAR","ANDAR"],
  2:["ANDAR","ANDAR","VIRAR À ESQUERDA","ANDAR","ANDAR"],
  4:["ANDAR","ANDAR","ANDAR"],
  5:["ANDAR","ANDAR","VIRAR À DIREITA","ANDAR","ANDAR"],
  6:["ANDAR","ANDAR","ANDAR","ANDAR","VIRAR À DIREITA","ANDAR","ANDAR","ANDAR"]
};
(async () => {
  const b = await chromium.launch({ executablePath:CROMO, args:["--no-sandbox","--disable-gpu"] });
  const p = await b.newPage({ viewport:{width:390,height:780} });
  const erros = [];
  p.on("pageerror", e => erros.push("ERRO JS: " + e.message));
  /* ⚠️ MP3 QUE FALTA NAO E DEFEITO — e informacao. A voz e gravada depois, pelo
     entregar.yml, a partir do falas.json (regra do pre-voo). Contar isso como
     defeito faria a regua reprovar todo caderno recem-nascido, e regua que grita
     no caso normal ensina a ignorar a regua. Entao: separo os dois. */
  let vozFalta = 0;
  p.on("requestfailed", r => { if (/audio\/cp3_.*\.mp3$/.test(r.url())) vozFalta++; });
  p.on("console", m => {
    if (m.type() !== "error") return;
    if (/ERR_FILE_NOT_FOUND|ERR_NAME_NOT_RESOLVED/.test(m.text())) return;  /* o mp3 */
    erros.push("CONSOLE: " + m.text());
  });
  await p.goto(ARQ);

  // abertura: o problema
  await p.click("#pedir"); await p.waitForTimeout(150);
  await p.click("#vai");   await p.waitForTimeout(250);

  for (let n = 1; n <= 6; n++) {
    const passo = await p.textContent(".passo");
    if (!passo.includes("Desafio " + n)) throw new Error("esperava desafio "+n+", achei: "+passo);
    // limpa o que vier pré-montado quando eu vou montar do zero
    if (SOL[n]) {
      await p.click("#limpar"); await p.waitForTimeout(80);
      for (const r of SOL[n]) {
        await p.click(`.blo:text-is("${r}")`); await p.waitForTimeout(50);
      }
    }
    if (n === 3) { await p.click('.opb:text-is("Na casa da caixa")'); await p.waitForTimeout(120); }
    await p.click("#rodar");
    await p.waitForSelector("#prox", { timeout: 15000 });
    const av = await p.textContent(".aviso.bom");
    if (!av.includes("chegou")) throw new Error("desafio "+n+" nao confirmou a chegada");
    console.log("  desafio " + n + ": o robo chegou");
    await p.click("#prox"); await p.waitForTimeout(250);
  }

  // a folha das peças
  await p.click("#vp");
  const fic = await p.$$(".fic");
  console.log("  fichas de hardware/software: " + fic.length);
  for (const f of fic) { await f.click(); await p.waitForTimeout(60); }
  await p.waitForSelector("#fim", { timeout: 5000 });
  await p.click("#fim"); await p.waitForTimeout(200);

  const fim = await p.textContent(".cart");
  if (!fim.includes("ALGORITMO")) throw new Error("o fecho nao trouxe a palavra");
  console.log("  fecho: a palavra ALGORITMO chega por ultimo");

  // o painel da máquina real, e a volta
  await p.click("#btmaq"); await p.waitForTimeout(200);
  const pr = await p.textContent(".cart");
  if (!pr.includes("Este computador")) throw new Error("painel da maquina real nao abriu");
  const nucleos = await p.textContent("table");
  console.log("  painel real: leu a maquina (" + (nucleos.match(/(\d+) n[úu]cleos/)||["?","?"])[1] + " nucleos)");
  await p.click("#fechar"); await p.waitForTimeout(250);
  await p.waitForSelector("#rel", { timeout: 5000 });   // a tela NAO morreu

  // relatório descritivo
  await p.click("#rel"); await p.waitForTimeout(250);
  const rel = await p.textContent(".cart");
  for (const t of ["Relatório descritivo","hardware","Dominou","Tema da aula"])
    if (!rel.includes(t)) throw new Error("o relatorio nao traz: " + t);
  console.log("  relatorio descritivo: ok (parecer em palavras, sem nota)");
  await p.screenshot({ path: "/tmp/claude-0/c3-relatorio.png", fullPage: true });

  await b.close();
  if (erros.length) { console.log("\nDEFEITOS:\n" + erros.join("\n")); process.exit(1); }
  console.log("  voz: " + vozFalta + " fala(s) ainda sem mp3 (informacao, nao defeito)");
  console.log("\nCOBAIA: a aula 1 joga do comeco ao fim, sem erro de JS.");
})().catch(e => { console.error("REPROVOU: " + e.message); process.exit(1); });
