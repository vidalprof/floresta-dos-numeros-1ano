import { defineConfig } from 'vite'

// base relativa: funciona quando publicado num subcaminho do GitHub Pages
// (ex.: https://vidalprof.github.io/educaverso-app/)
export default defineConfig({
  base: './',
  build: {
    // Alvo = os navegadores REAIS da escola (confirmados pelo Marcos):
    //   - Chrome 109 (o último do Win7, de 2023)
    //   - Firefox 106 (64 bits) ← é MAIS ANTIGO que o 115; por isso o alvo
    //     tem que ser 106, senao o Vite gera sintaxe que o 106 nao entende.
    // Ambos sao modernos o bastante (ES2022) p/ usar recursos atuais SEM
    // gambiarra e ainda rodar no PC velho.
    target: ['chrome109', 'firefox106']
  }
})
