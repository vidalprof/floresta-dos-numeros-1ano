/* A MESMA regra da casa (no-undef, case que vaza, chave dupla...) para os APPS À MÃO
   escritos em JavaScript moderno (const/let/arrow/template) — o UNO dos Números, por
   exemplo. As atividades do motor continuam em ES5 (`eslint.config.mjs`); o
   `_qa/estatico.sh` só cai aqui quando o arquivo não é do motor (sem conteudo.json)
   e o parser ES5 tropeça em sintaxe nova. Nasceu em 2026-09-07: o entregar.yml
   reprovou o UNO com "The keyword 'const' is reserved" e a voz da casa não subiu. */
import base from "./eslint.config.mjs";

export default base.map(c => ({
  ...c,
  languageOptions: { ...c.languageOptions, ecmaVersion: 2020 }
}));
