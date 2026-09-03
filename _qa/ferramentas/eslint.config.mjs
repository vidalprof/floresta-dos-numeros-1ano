/* Regras do ESLint para as atividades da casa.
   O alvo NAO e "codigo bonito": e a familia de defeitos que derruba o app na
   cara da crianca e que o `node --check` nao ve, porque nao e sintaxe.
   O caso que pagou por esta config: `FASES_MESTRE is not defined` (Tangram,
   set/2026) — tela branca, banca inteira aprovando. */
import globals from "globals";

export default [{
  languageOptions: {
    ecmaVersion: 5,          // as atividades sao ES5 (PC velho da escola)
    sourceType: "script",
    globals: {
      ...globals.browser,
      ...globals.es2021,  /* Uint8Array, Promise, Map... que o browser sozinho nao lista */

      /* ⚠️ GLOBAIS IMPLICITOS DA CASA — e isto e DIVIDA, nao virtude.
         Sao nomes criados por atribuicao SEM `var` (`RELBNCC = "..."`,
         `fimDaPeca = _seguir`, `sPing = ...`). Em ES5 nao-strict isso cria um
         global e funciona; o ESLint nao tem como adivinhar e acusa uso nao
         declarado em 15 atividades. Ficam listados aqui para o portao nao virar
         ruido — mas a divida continua: global implicito e o mesmo mecanismo que
         faz um erro de digitacao (`fimDaPeça = ...`) criar uma variavel NOVA em
         silencio, em vez de reclamar. O certo e declarar com `var` no motor.
         Conferido em 03/set/2026: o portao de boot e o dossie jogaram a
         atividade inteira sem nenhum ReferenceError com estes nomes. */
      RELBNCC: "writable", fimDaPeca: "writable", sPing: "writable"
      /* ⚠️ LICAO PAGA NA HORA (set/2026): eu tinha listado aqui os nomes do
         motor (el, limpa, festa, imgEl, arma, ac, setProg, mostraBanner). Mas
         eles NAO vem de fora — sao declarados no PROPRIO arquivo. Declarar um
         global com o mesmo nome fez o `no-redeclare` acusar a atividade
         INTEIRA: 20 erros no Tangram consertado, idênticos aos do quebrado.
         Portao que reprova o certo e o errado do mesmo jeito nao informa nada.
         Regra: aqui so entram nomes que a atividade USA e NUNCA declara. */
    }
  },
  rules: {
    /* ⭐ O QUE IMPORTA: nome usado que nunca foi declarado. E o
       `ReferenceError` da tela branca, pego ANTES de abrir o navegador. */
    "no-undef": "error",
    /* ⚠️ `no-use-before-define` fica DESLIGADO de proposito. Em ES5 o
       `var` sobe (hoisting) e a casa inteira escreve assim: a funcao de cima
       usa a variavel declarada la embaixo, e roda perfeito porque so e LIDA
       depois. Ligado, ele acusou 8 nomes legitimos no Tangram que funciona.
       O defeito que interessa (nome que NUNCA foi declarado) e o `no-undef`. */
    /* `case` que cai no seguinte sem `break` — troca a resposta da crianca */
    "no-fallthrough": "error",
    /* dois `case` iguais / duas chaves iguais no objeto: a segunda apaga a
       primeira em silencio (ja aconteceu com fala repetida) */
    "no-duplicate-case": "error",
    "no-dupe-keys": "error",
    "no-dupe-args": "error",
    /* ⚠️ `no-func-assign` DESLIGADO: a casa troca funcao de proposito. O
       "Treinar o que faltou" guarda o `mostraBanner` original e poe um no
       lugar, para desviar o "proximo" sem mexer em nenhuma fase. Esta escrito
       e comentado no codigo. A regra acusava esse padrao legitimo. */
    /* ⚠️ `no-redeclare` DESLIGADO, e com motivo medido (set/2026). O integrador
       inlina a peca e, dentro do fechamento dela, ficam DUAS `diz`: a
       `function diz(txt)` da peca sozinha (voz-robo do navegador, para a peca
       funcionar na bancada) e a `var diz = function(txt)` da PONTE, que
       reaponta para a voz da casa (o MP3 gravado). Por hoisting a `function`
       nasce primeiro e a `var` a sobrescreve na execucao: a PONTE vence, que e
       exatamente o desejado. Prova de execucao: as atividades narram com voz
       gravada — se a da peca vencesse, seriam MUDAS no PC da escola, que nao
       tem voz pt-BR instalada. Ligada, a regra acusava 15 atividades corretas.
       Vale para `temImg`, `w`, `k`, `nb` pelo mesmo motivo (peca inlinada). */
    /* `if (x = 1)` no lugar de `==`: acerta sempre, o erro nunca aparece */
    "no-cond-assign": "error",
    /* codigo depois de return/throw: nunca roda, e costuma ser a linha que
       consertava alguma coisa */
    "no-unreachable": "error",
    "no-sparse-arrays": "error",
    "use-isnan": "error",
    "valid-typeof": "error",
    "no-obj-calls": "error",
    "no-unsafe-negation": "error"
  }
}];
