import { defineConfig } from 'vite'

// base relativa: funciona quando publicado num subcaminho do GitHub Pages
// (ex.: https://vidalprof.github.io/educaverso-app/)
export default defineConfig({
  base: './',
  build: {
    // Alvo = Chrome 109 (o último do Win7, de 2023): moderno o bastante p/ usar
    // recursos atuais SEM gambiarra, e ainda rodar no PC da escola. Firefox
    // atualizado tb entra nesse patamar.
    target: ['chrome109', 'firefox115']
  }
})
