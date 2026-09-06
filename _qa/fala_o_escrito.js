/* ============================================================
   PORTÃO — "a voz diz o que está ESCRITO?"

   ⚠️ LIÇÃO PAGA (ago/2026), e quem pegou foi o Marcos, não portão nenhum:
   *"os erros que achei nessa atividade foram (...) a questão dos botões não
   falar o que está escrito, e não teve fala automática, visto que os pequinos
   precisam"* — e, quando eu mostrei a medição: *"tem que falar o que está
   escrito"*.

   Medido na Padaria das Letras, ANTES do conserto:
     · 32 fases, **1** narrava sozinha — 31 mudas;
     · 23 alto-falantes, **8** deles em cima de uma letra sozinha (M, B, P, D,
       C, G, Q, O) não tocavam NADA. A criança do 1º ano tocava o alto-falante
       da letra — o gesto exato que a atividade ensina — e ouvia silêncio;
     · 2 fases tinham resposta tocável e nenhum alto-falante.

   Nenhum dos portões existentes via isso. Eles mediam se a voz EXISTE
   (`_qa/falas.py` mede a pronúncia; o montador conta quantas gravar), nunca se
   o que está NA TELA tem a gravação DAQUELE texto. É a mesma família do
   "existir não é medir".

   O que este portão faz, fase por fase, na atividade montada:
     1. lê o BALÃO da fase e confere que há gravação para aquele texto
        (senão o motor fica calado de propósito — é a "fala automática" que
        some);
     2. acha todo ALTO-FALANTE (`.zap`) e confere que a gravação dele é
        exatamente o texto escrito ao lado;
     3. avisa quando a fase tem resposta tocável e nenhum alto-falante — no 1º
        ano, quem ainda soletra escolhe pelo desenho e a atividade vira loteria.

   ⚠️ Ele NÃO mede se o mp3 já foi gravado (isso é do `entregar.yml`): mede se o
   texto da tela ESTÁ NA LISTA de gravação. Um sem o outro não resolve.

   Uso: node _qa/fala_o_escrito.js <pasta-da-atividade>
   ============================================================ */
/* ⚠️⚠️ LICAO PAGA (set/2026, na 3a tentativa de publicar o mesmo conserto): o
   `require` do Playwright fica no TOPO, fora de qualquer try. Num lugar sem
   Playwright — o runner do GitHub, por exemplo — ele estoura na hora e o Node
   sai com codigo **1**, que a esteira le como REPROVOU. Mas o portao nao
   reprovou nada: ele nem conseguiu comecar. Isso e codigo **2** (NAO MEDI), e a
   diferenca decide se a entrega para ou segue. */
let chromium;
try { chromium = require('/opt/node22/lib/node_modules/playwright/index.js').chromium; }
catch (e) {
  console.log('NAO MEDI: Playwright nao esta instalado aqui (' + e.code + '). ' +
              'Este portao roda na bancada local, onde ha Chromium.');
  process.exit(2);
}
const fs = require('fs');
const path = require('path');

(async () => {
  const pasta = (process.argv[2] || '').replace(/\/$/, '');
  if (!pasta) { console.log('uso: node _qa/fala_o_escrito.js <pasta>'); process.exit(2); }
  const html = path.resolve(pasta, 'index.html');
  const jf = path.resolve(pasta, 'falas.json');
  if (!fs.existsSync(html) || !fs.existsSync(jf)) {
    console.log(pasta + ' -> falta index.html ou falas.json. NAO MEDI NADA.');
    process.exit(2);
  }
  const porId = {};
  /* ⚠️ SEGUNDA LICAO PAGA (ago/2026, no Jardim do Broto): este portao acusou 24
     fases de MUDAS que falam perfeitamente. Sao DOIS jeitos de gravar a mesma
     frase, e o portao so conhecia um:
       · atividade MONTADA pelo esqueleto -> a chave e a CONTA do texto
         (`op_<chaveVoz(balao)>.mp3`), porque o balao e gerado;
       · atividade ESCRITA A MAO -> a mesma frase e gravada com NOME PROPRIO
         (`jd_abertura`), e a tela chama `falar("jd_abertura")`.
     Procurar so pela conta reprovava toda atividade premium feita a mao. A
     pergunta honesta nao e "o id bate?", e "a crianca OUVE o que esta escrito
     no balao?" — entao o indice abaixo tambem guarda o TEXTO de cada fala. */
  const porTexto = {};
  const achata = s => (s || '').replace(/&[a-z]+;|&#\d+;/gi, ' ')
    .normalize('NFD').replace(/[̀-ͯ]/g, '')
    .toLowerCase().replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim();
  JSON.parse(fs.readFileSync(jf, 'utf8')).forEach(f => {
    porId[f.id] = f.texto;
    if (f.texto) porTexto[achata(f.texto)] = f.id;
  });

  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--disable-gpu', '--autoplay-policy=no-user-gesture-required']});
  const p = await b.newPage({viewport: {width: 1366, height: 640}});
  await p.goto('file://' + html);
  await p.waitForTimeout(900);

  /* Atividade MONTADA anda pelo `FASES`. Atividade ESCRITA A MAO (o Jardim do
     Broto, o Circo do Teo) tem uma funcao por tela — entao as telas sao
     descobertas pelo nome, como o resto da banca ja faz. Sem isto o portao
     dizia "nao achei as FASES" justo nas atividades premium feitas a mao. */
  const montada = await p.evaluate(() => typeof FASES !== 'undefined' && typeof montaFase === 'function');
  const telas = montada ? [] : await p.evaluate(() => {
    /* telas do PROFESSOR (painel, menu de fases da senha 1275@) e as de entrada
       nao sao fase de crianca: nao tem narracao gravada por natureza. */
    const fora = {telaPainel: 1, telaCapa: 1, telaQuem: 1, telaP: 1, telaMestre: 1};
    return Object.keys(window).filter(k => /^tela[A-Z]/.test(k) &&
      typeof window[k] === 'function' && !fora[k]).sort();
  });
  const n = montada ? await p.evaluate(() => FASES.length) : telas.length;
  if (!n) {
    console.log(pasta + ' -> nao achei nem FASES nem telas. NAO MEDI NADA (isso nao e "passou").');
    process.exit(2);
  }
  console.log(pasta + ' -> ' + (montada ? 'atividade montada' : 'atividade escrita a mao') +
              ', ' + n + ' tela(s) a medir');

  /* ⚠️ CAIXA NAO CONTA (licao ago/2026). A chave da voz baixa a caixa de
     proposito: "EATING" e "eating" dividem UM mp3, e e assim que a casa
     economiza gravacao. Numa atividade de ingles a mesma palavra aparece em
     CAIXA ALTA como etiqueta ("EATING") e em minuscula dentro da frase
     ("He is eating a sandwich") — as duas certas, e a voz identica nas duas.
     Comparar com a caixa fazia o portao acusar uma diferenca que NAO EXISTE
     para a crianca, que ouve. O que ele tem que medir e o que se OUVE. */
  /* ⚠️ a LACUNA do completar ("___" na tela) vira PAUSA no audio ("…"): e um GAP
     nos dois lados, entao sai da conta (senao "___" != "…" reprova uma fase certa).
     Detetive, ago/2026. */
  const norm = s => (s || '').replace(/[_…]+/g, ' ').replace(/\s+/g, ' ').trim().toLowerCase();
  /* ⭐ LICAO PAGA (ago/2026, Trem do Alfabeto). O `montar.py` (eh_fala) grava,
     DE PROPOSITO, uma letra sozinha pelo NOME dela: o vagao "D" fala "Dê", o "I"
     fala "Í". E o certo — a crianca do 1o ano aprende a NOMEAR a letra, e a voz
     crua do "I" saia em ingles ("ai"). Este portao comparava o glifo escrito
     ("D") com a gravacao ("Dê") e inventava 18 defeitos: a mesma tabela que o
     montar usa vive AQUI, e "D" == "Dê" e ACERTO, nao erro. Uma letra dita por
     nome ERRADO (ex.: "D" gravado "Efe") continua reprovando. */
  const NOMES = {A:'Á',B:'Bê',C:'Cê',D:'Dê',E:'É',F:'Éfe',G:'Gê',H:'Agá',I:'Í',
    J:'Jóta',K:'Cá',L:'Éle',M:'Ême',N:'Ene',O:'Ó',P:'Pê',Q:'Quê',R:'Érre',
    S:'Ésse',T:'Tê',U:'Ú',V:'Vê',W:'Dáblio',X:'Xis',Y:'Ípsilon',Z:'Zê'};
  const letraLidaPeloNome = (escrito, gravado) => {
    const t = (escrito || '').trim();
    return /^[A-Za-z]$/.test(t) && norm(gravado) === norm(NOMES[t.toUpperCase()]);
  };
  const mudas = [], semVoz = [], semZap = [];
  let zaps = 0, batem = 0;

  for (let i = 0; i < n; i++) {
    const nome = montada ? ('fase ' + (i + 1)) : telas[i];
    try {
      if (montada) {
        await p.evaluate(k => {
          try { perfil = {nome: 'ANA', fig: ID.pre + '_cr1'}; } catch (e) {}
          montaFase(k, function () {});
        }, i);
      } else {
        await p.evaluate(t => {
          try { if (typeof ALUNO !== 'undefined') ALUNO = 'ANA'; } catch (e) {}
          window[t]();
        }, telas[i]);
      }
    } catch (e) { continue; }
    await p.waitForTimeout(330);

    const r = await p.evaluate(() => {
      const cx = (document.getElementsByClassName('pecabox')[0] || document.querySelector('.tela') || document.body);
      const bs = cx ? cx.getElementsByClassName('balao') : null;
      const balao = (bs && bs.length) ? (bs[0].textContent || '') : '';
      /* ⚠️ LICAO PAGA (ago/2026): este portao acusou 32 alto-falantes INOCENTES.
         Existem DOIS mecanismos de voz, e eles nao usam o mesmo arquivo:
           `.zap`  (resposta tocavel) -> tocaVoz(chaveVoz(texto)) -> op_<conta>.mp3
           `.zapb` (o enunciado)      -> falar(vozDaTela())       -> <id>.mp3
         Medir os dois pela conta do texto reprovava todo enunciado, que e
         gravado com nome proprio (`pd_f01_intro`). Portao que mede pelo
         mecanismo errado nao esta rigoroso: esta cego para o certo e barulhento
         para o errado. Aqui cada um e perguntado do SEU jeito. */
      const lista = [];
      document.querySelectorAll('.zap').forEach(z => {
        /* ⚠️ TERCEIRA LICAO DA MESMA FAMILIA (ago/2026): o portao lia a TELA para
           descobrir o que o botao diz, e o MOTOR le o `data-voz` quando existe
           (motor.html: `elm.getAttribute("data-voz") ? ... : textoVisivel(elm)`).
           Onde a peca declara a voz — e ela declara justamente onde a leitura da
           tela erraria — o portao acusava 25 alto-falantes INOCENTES: a carta da
           memoria tem o rotulo colado no valor, e ele pedia a gravacao de
           "PALAVRAMALA". Portao tem que perguntar do mesmo jeito que o motor
           responde; medir por outro caminho e inventar um defeito. */
        const dv = z.getAttribute && z.getAttribute('data-voz');
        const t = dv || (z.parentNode.textContent || '').replace(/\s+/g, ' ').trim();
        lista.push({txt: t, arq: (typeof chaveVoz === 'function' ? 'op_' + chaveVoz(t) : ''), tipo: 'resposta'});
      });
      document.querySelectorAll('.zapb').forEach(z => {
        const t = (z.parentNode.textContent || '').replace(/\s+/g, ' ').trim();
        lista.push({txt: t, arq: (typeof vozDaTela === 'function' ? vozDaTela() : ''), tipo: 'enunciado'});
      });
      return {
        balao: balao,
        balaoK: (balao && typeof chaveVoz === 'function') ? chaveVoz(balao.replace(/\s+/g, ' ').trim()) : null,
        zaps: lista,
        resp: document.querySelectorAll('.opt, .oaf, .carta, .escolha').length
      };
    });

    /* narrado = existe gravacao pela CONTA do texto (atividade montada) OU uma
       fala com esse MESMO TEXTO gravada com nome proprio (escrita a mao). */
    if (r.balao && !porId['op_' + r.balaoK] && !porTexto[achata(r.balao)]) {
      mudas.push(nome + ': "' + norm(r.balao).slice(0, 52) + '"');
    }
    zaps += r.zaps.length;
    r.zaps.forEach(z => {
      if (!z.arq) {
        semVoz.push(nome + ' [' + z.tipo + ']: o alto-falante de "' + z.txt.slice(0, 32) + '" nao toca nada');
        return;
      }
      const grav = porId[z.arq];
      /* o enunciado e gravado com nome proprio (pd_f01_intro): o texto dele
         mora no falas.json sob esse id, e nao sob a conta do texto. Se o id
         existe na lista de gravacao, o botao TOCA o enunciado desta fase — que
         e exatamente o que esta escrito. */
      if (grav === undefined) {
        /* ⚠️ (set/2026) o TEXTO vai junto: sem ele eu nao tinha como saber que voz
           faltava (fiquei calculando chaves no escuro na Expedicao da Divisao). */
        semVoz.push(nome + ' [' + z.tipo + ']: toca ' + z.arq + ', que nao esta na lista de gravacao — o botao diz "' + String(z.txt).slice(0, 48) + '"');
      } else if (z.tipo === 'resposta' && norm(grav) !== norm(z.txt)
                 && !letraLidaPeloNome(z.txt, grav)) {
        semVoz.push(nome + ': escrito "' + z.txt.slice(0, 28) +
                    '" mas gravado "' + norm(grav).slice(0, 28) + '"');
      } else batem++;
    });
    if (!r.zaps.length && r.resp > 1) {
      semZap.push(nome + ': ' + r.resp + ' resposta(s) tocavel(is), 0 alto-falante');
    }
  }
  await b.close();

  console.log('   ' + n + ' tela(s) medida(s) | ' + zaps + ' alto-falante(s)');
  console.log('   balao COM gravacao (a fala automatica): ' + (n - mudas.length) + ' de ' + n);
  console.log('   alto-falante que diz o que esta escrito: ' + batem + ' de ' + zaps);

  const erros = mudas.length + semVoz.length;
  if (mudas.length) {
    console.log('   ' + mudas.length + ' FASE(S) MUDA(S) — o motor le o balao e nao acha gravacao:');
    mudas.slice(0, 8).forEach(m => console.log('    - ' + m));
  }
  if (semVoz.length) {
    console.log('   ' + semVoz.length + ' ALTO-FALANTE(S) QUE NAO DIZEM O ESCRITO:');
    semVoz.slice(0, 8).forEach(m => console.log('    - ' + m));
  }
  if (semZap.length) {
    console.log('   aviso: ' + semZap.length + ' fase(s) com resposta tocavel e sem alto-falante:');
    semZap.slice(0, 6).forEach(m => console.log('    . ' + m));
  }
  if (!erros) console.log('   voz ok: toda tela narra e todo alto-falante diz o que esta escrito');
  process.exit(erros ? 1 : 0);
})();
