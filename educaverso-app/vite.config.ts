import { defineConfig } from 'vite'

// base relativa: funciona quando publicado num subcaminho do GitHub Pages
// (ex.: https://vidalprof.github.io/educaverso-app/)
export default defineConfig({
  base: './',
  build: {
    target: 'es2017'   // compatível com navegadores antigos (Win7 + Chrome/Firefox atualizados)
  }
})
