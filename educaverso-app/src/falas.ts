// ============================================================================
// FALAS DO MUNDO — Ilha do Tesouro (Etapa 3)
// REGRA DE OURO: toda fala tem MP3 gerado por API (edge-tts) — Antonio para o
// narrador, Donato para o Louro. NUNCA a voz do navegador.
// Os MP3 vivem em public/audio/<id>.mp3 (gerados pelo gerar-audio.yml).
// O QA confere cobertura: todo id usado aqui precisa ter o seu MP3.
// Filosofia: o Louro PERGUNTA, nunca responde; o conceito é nomeado por
// ÚLTIMO, pelo narrador (n_conceito).
// ============================================================================

export interface Fala {
  quem: string      // nome mostrado na plaquinha do balão
  texto: string     // texto exibido letra a letra (typewriter)
  cor: string       // cor da plaquinha de nome
}

export const FALAS: { [id: string]: Fala } = {
  // ---- narrador (voz Antonio) ----
  n_bemvindo: {
    quem: 'Narrador', cor: '#3a6ea5',
    texto: 'Bem-vindo à Ilha do Tesouro! Use as setas do teclado, ou toque na areia, para explorar. Fale com quem você encontrar pelo caminho!'
  },
  n_conceito: {
    quem: 'Narrador', cor: '#3a6ea5',
    texto: 'Você criou uma sequência de passos, na ordem certa, para resolver um problema. Isso tem um nome: ALGORITMO! Você acabou de criar um algoritmo!'
  },

  // ---- Louro, o papagaio (voz Donato) ----
  l_ola: {
    quem: 'Louro', cor: '#2e9c5b',
    texto: 'Crá! Oi, amiguinho! Que bom que você apareceu! Eu estou com um problemão... quer ouvir?'
  },
  l_problema: {
    quem: 'Louro', cor: '#2e9c5b',
    texto: 'A maré subiu e o baú do tesouro ficou preso lá nas pedras! O caranguejo Chico até vai buscar... mas ele só anda se receber as instruções certinhas, uma por uma. E agora, o que a gente faz?'
  },
  l_como: {
    quem: 'Louro', cor: '#2e9c5b',
    texto: 'Boa ideia! Monte os passos para o Chico: toque nas setas, na ordem que ele deve andar. Quando estiver pronto, mande ele ir!'
  },
  l_agua: {
    quem: 'Louro', cor: '#2e9c5b',
    texto: 'Ih! O Chico caiu na água! Crá! O que será que aconteceu? Qual passo a gente pode mudar?'
  },
  l_quase: {
    quem: 'Louro', cor: '#2e9c5b',
    texto: 'Hmm, o Chico parou no meio do caminho... será que faltou algum passo?'
  },
  l_vitoria: {
    quem: 'Louro', cor: '#2e9c5b',
    texto: 'Crá crá! O Chico chegou no baú! Você conseguiu! Me conta: como você fez isso?'
  }
}

// lista usada no preload (e no gate de cobertura de voz do QA)
export const IDS_FALAS = Object.keys(FALAS)
