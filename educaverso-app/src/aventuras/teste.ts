// Aventura de TESTE — só pra provar que o MONTADOR lê dados e arma o mundo.
// Usa assets que já existem no app (kit antigo) + o atlas do herói limpo.
// (o kit bonito da Fazendinha entra depois; aqui é o "esqueleto" da máquina.)
import type { TAventura } from '../motor/aventura'

export const AVENTURA_TESTE: TAventura = {
  id: 'teste_montador',
  titulo: 'Teste do Montador',
  tema: 'ilha',
  objetivo: 'validar o montador (dados -> mundo)',
  conceito_final: 'ALGORITMO',
  estilo: 'limpo',
  heroi: 'heroi',
  inicio: { x: 500, y: 800 },
  mundo: { largura: 2400, altura: 1600, chao: 'chao', hora: 'noite', ambiente_sons: ['mar'] },
  paradas: [
    {
      id: 'p1', nome: 'Palmeiras', x: 400, y: 500, cor: '#ffd25a',
      objetos: [
        { asset: 'palmeira', x: 300, y: 520, alt: 300, vida: 'balanca', colide: true, flip: false },
        { asset: 'tocha', x: 560, y: 560, alt: 120, vida: 'tremula', colide: false, flip: false },
        { asset: 'rocha', x: 700, y: 700, alt: 70, vida: 'nada', colide: true, flip: false }
      ],
      personagens: [], falas: []
    },
    {
      id: 'p2', nome: 'A Poça', x: 1500, y: 900, cor: '#8fd4ff',
      objetos: [
        { asset: 'pocao', x: 1500, y: 950, alt: 240, vida: 'nada', colide: true, flip: false },
        { asset: 'bau_fechado', x: 1600, y: 820, alt: 70, vida: 'brilha', colide: false, flip: false },
        { asset: 'palmeira', x: 1850, y: 700, alt: 260, vida: 'balanca', colide: true, flip: true }
      ],
      personagens: [], falas: []
    },
    {
      id: 'p3', nome: 'A Trilha', x: 900, y: 1300, cor: '#57e08a',
      objetos: [
        { asset: 'rocha', x: 800, y: 1300, alt: 66, vida: 'nada', colide: true, flip: false },
        { asset: 'rocha', x: 1050, y: 1350, alt: 60, vida: 'nada', colide: true, flip: true },
        { asset: 'tocha', x: 950, y: 1250, alt: 120, vida: 'tremula', colide: false, flip: false }
      ],
      personagens: [], falas: []
    }
  ]
}
