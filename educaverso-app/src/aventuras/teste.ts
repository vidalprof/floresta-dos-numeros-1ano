// Aventura de TESTE — prova que o MONTADOR lê dados e arma o mundo (v2: zonas).
// Usa assets que já existem no app (kit antigo). Abre com ?teste.
import type { TAventura } from '../motor/aventura'

export const AVENTURA_TESTE: TAventura = {
  id: 'teste_montador',
  titulo: 'Teste do Montador',
  tema: 'ilha',
  objetivo: 'validar o montador (dados -> mundo)',
  conceito_final: 'ALGORITMO',
  heroi: 'heroi',
  zona_inicial: 'ilha',
  inicio: { x: 500, y: 800 },
  zonas: [
    {
      id: 'ilha',
      nome: 'Ilha de Teste',
      prancha: 'chao.jpg',
      largura: 2048, altura: 1440, chao_min_y: 200,
      paradas: [
        {
          id: 'p1', nome: 'Palmeiras', x: 400, y: 500, cor: '#ffd25a', marcador: true,
          objetos: [
            { asset: 'palmeira', x: 300, y: 520, alt: 300, vida: 'balanca', colide: true, flip: false, terreno: 'terra' },
            { asset: 'tocha', x: 560, y: 560, alt: 120, vida: 'tremula', colide: false, flip: false, terreno: 'terra' },
            { asset: 'rocha', x: 700, y: 700, alt: 70, vida: 'nada', colide: true, flip: false, terreno: 'terra' }
          ],
          mecanica: { id: 'contar', params: { quantidade: 5, item: 'tocha', max: 30 } },
          personagens: [], falas: []
        },
        {
          id: 'p2', nome: 'A Poça', x: 1500, y: 900, cor: '#8fd4ff', marcador: true,
          objetos: [
            { asset: 'pocao', x: 1500, y: 950, alt: 240, vida: 'nada', colide: true, flip: false, terreno: 'qualquer' },
            { asset: 'bau_fechado', x: 1600, y: 820, alt: 70, vida: 'brilha', colide: false, flip: false, terreno: 'terra' },
            { asset: 'palmeira', x: 1850, y: 700, alt: 260, vida: 'balanca', colide: true, flip: true, terreno: 'terra' }
          ],
          personagens: [], falas: []
        }
      ],
      portais: [],
      efeitos: { polen: true },
      musica: '',
      chegada: [],
      falas: []
    }
  ]
}
