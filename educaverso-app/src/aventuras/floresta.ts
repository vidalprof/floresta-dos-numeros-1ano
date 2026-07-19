// ============================================================================
// AVENTURA "A FLORESTA DO BYTE" — o estilo que o Marcos pediu: mundo MONTADO
// de peças (chão contínuo + árvores/rio/ponte com colisão), a criança anda
// ENTRE as coisas. Prova da GRAMÁTICA: problema exposto (PONTE QUEBRADA barra o
// caminho) -> resolve (acha as tábuas) -> ganha ITEM (mochila) -> ENTREGA ao
// mestre Castor -> o MUNDO MUDA (ponte consertada, passagem abre) -> prossegue
// (clareira secreta). Aluno protagonista; aprende sem perceber.
// (Mundo-prova da máquina — a atividade curricular nasce depois, no fluxo
//  tema+ano -> Pedagogo -> Roteirista.)
// ============================================================================
import type { TAventuraIn } from '../motor/aventura'

const BYTE = { quem: 'Byte', cor: '#2a9fb3' }
const CASTOR = { quem: 'Mestre Castor', cor: '#8a5a2b' }

export const AVENTURA_FLORESTA: TAventuraIn = {
  id: 'floresta_v1',
  titulo: 'A Floresta do Byte',
  tema: 'floresta',
  objetivo: 'Prova da gramática problema->item->entrega->mundo muda (contagem 1-3 embutida)',
  conceito_final: 'AJUDAR',
  heroi: 'byte',
  zona_inicial: 'floresta',
  inicio: { x: 500, y: 700 },
  zonas: [
    // ------------------------------------------ A FLORESTA (oeste | rio | leste)
    {
      id: 'floresta',
      nome: 'A Floresta',
      chao_textura: 'grama',
      agua_textura: 'rio',
      largura: 2080, altura: 1440, chao_min_y: 240,
      agua: [{ x: 1310, y: 0, w: 150, h: 1440 }],
      bloqueios: [
        { id: 'rio_n', x: 1310, y: 0, w: 150, h: 600 },
        { id: 'rio_ponte', x: 1310, y: 600, w: 150, h: 180 },   // sai quando a ponte é consertada
        { id: 'rio_s', x: 1310, y: 780, w: 150, h: 660 }
      ],
      paradas: [
        {
          id: 'mata', nome: 'A Mata', x: 500, y: 700, cor: '#57e08a', marcador: false,
          objetos: [
            { asset: 'arvore_a', x: 300, y: 420, alt: 300, vida: 'balanca', colide: true },
            { asset: 'arvore_b', x: 620, y: 330, alt: 320, vida: 'balanca', colide: true },
            { asset: 'pinheiro', x: 180, y: 780, alt: 280, vida: 'balanca', colide: true },
            { asset: 'arvore_b', x: 800, y: 600, alt: 300, vida: 'balanca', colide: true, flip: true },
            { asset: 'arvore_a', x: 480, y: 1000, alt: 290, vida: 'balanca', colide: true, flip: true },
            { asset: 'pinheiro', x: 240, y: 1220, alt: 270, vida: 'balanca', colide: true },
            { asset: 'arvore_a', x: 860, y: 1290, alt: 300, vida: 'balanca', colide: true },
            { asset: 'arvore_b', x: 1080, y: 430, alt: 310, vida: 'balanca', colide: true },
            { asset: 'pinheiro', x: 1150, y: 1120, alt: 280, vida: 'balanca', colide: true },
            { asset: 'arvore_a', x: 1680, y: 400, alt: 300, vida: 'balanca', colide: true, flip: true },
            { asset: 'arvore_b', x: 1870, y: 800, alt: 310, vida: 'balanca', colide: true },
            { asset: 'pinheiro', x: 1620, y: 1180, alt: 280, vida: 'balanca', colide: true },
            { asset: 'arbusto', x: 420, y: 560, alt: 90 },
            { asset: 'arbusto', x: 960, y: 860, alt: 96, flip: true },
            { asset: 'arbusto', x: 1750, y: 1000, alt: 90 },
            { asset: 'flores', x: 560, y: 840, alt: 56 },
            { asset: 'flores', x: 350, y: 950, alt: 52 },
            { asset: 'flores', x: 900, y: 480, alt: 56, flip: true },
            { asset: 'flores', x: 1560, y: 700, alt: 56 },
            { asset: 'pedra', x: 700, y: 1180, alt: 84, colide: true },
            { asset: 'pedra', x: 1230, y: 300, alt: 78, colide: true },
            // A PONTE — o problema EXPOSTO no mundo (muda p/ 'ponte' na entrega)
            { id: 'ponte', asset: 'ponte_quebrada', x: 1385, y: 748, alt: 124, profundidade: 600 }
          ],
          personagens: [
            {
              nome: 'castor', x: 1150, y: 820, alt: 104,
              fala_ao_chegar: ['f_ponte', 'f_castor'],
              quer_item: 'tabuas',
              ao_receber: {
                falas: ['f_entrega', 'f_conserta'],
                muda_objeto: { id: 'ponte', asset: 'ponte' },
                remove_bloqueio: 'rio_ponte'
              }
            }
          ],
          falas: []
        }
      ],
      missao: {
        tipo: 'colher', asset: 'tabuas', alt: 64,
        itens: [{ x: 420, y: 770 }, { x: 720, y: 1120 }, { x: 300, y: 1060 }],
        voz_prefixo: 'kn',
        ao_completar: ['f_pegou'],
        fala_revisita: [],
        recompensa_item: { asset: 'tabuas', nome: 'Tábuas' }
      },
      portais: [
        { x: 1985, y: 720, raio: 75, para: 'clareira', spawn: { x: 220, y: 700 }, rotulo: 'Clareira' }
      ],
      efeitos: { sol: { x: 1700, y: 170 }, polen: true },
      musica: 'mus_carefree',
      chegada: ['f_floresta'],
      falas: [
        { id: 'f_floresta', ...BYTE, texto: 'Que floresta linda! Vamos explorar?' },
        { id: 'f_ponte', ...BYTE, texto: 'Oh, não! A ponte está quebrada. Assim a gente não consegue atravessar o rio.' },
        { id: 'f_castor', ...CASTOR, texto: 'Olá! Eu sou o mestre Castor. Eu conserto a ponte num instante — mas preciso de tábuas de madeira. Será que você encontra tábuas pela floresta?' },
        { id: 'f_pegou', ...BYTE, texto: 'Tábuas de madeira! Era disso que o mestre Castor precisava. Vamos levar até ele!' },
        { id: 'f_entrega', ...BYTE, texto: 'Aqui está, mestre Castor!' },
        { id: 'f_conserta', ...CASTOR, texto: 'Toc, toc, toc… Prontinho! A ponte está consertada. Obrigado pela ajuda!' }
      ]
    },
    // ------------------------------------------ A CLAREIRA SECRETA (recompensa)
    {
      id: 'clareira',
      nome: 'A Clareira Secreta',
      chao_textura: 'grama',
      largura: 1440, altura: 1080, chao_min_y: 200,
      festa_na_chegada: true,
      paradas: [
        {
          id: 'jardim', nome: 'O Jardim', x: 720, y: 540, cor: '#ffd25a', marcador: false,
          objetos: [
            { asset: 'arvore_a', x: 320, y: 380, alt: 300, vida: 'balanca', colide: true },
            { asset: 'arvore_b', x: 1120, y: 420, alt: 310, vida: 'balanca', colide: true, flip: true },
            { asset: 'pinheiro', x: 260, y: 900, alt: 270, vida: 'balanca', colide: true },
            { asset: 'arvore_a', x: 1180, y: 920, alt: 290, vida: 'balanca', colide: true, flip: true },
            { asset: 'flores', x: 620, y: 620, alt: 60 },
            { asset: 'flores', x: 820, y: 560, alt: 56, flip: true },
            { asset: 'flores', x: 700, y: 760, alt: 60 },
            { asset: 'flores', x: 560, y: 480, alt: 52 },
            { asset: 'flores', x: 880, y: 700, alt: 56 },
            { asset: 'arbusto', x: 480, y: 860, alt: 92 },
            { asset: 'arbusto', x: 980, y: 840, alt: 92, flip: true }
          ],
          personagens: [], falas: []
        }
      ],
      portais: [
        { x: 110, y: 700, raio: 70, para: 'floresta', spawn: { x: 1880, y: 720 }, rotulo: 'Floresta' }
      ],
      efeitos: { sol: { x: 1150, y: 160 }, polen: true },
      musica: 'mus_wallpaper',
      chegada: ['f_atravessa', 'f_clareira'],
      falas: [
        { id: 'f_atravessa', ...BYTE, texto: 'A ponte está firme! Agora dá para atravessar. Você conseguiu!' },
        { id: 'f_clareira', ...BYTE, texto: 'Uma clareira secreta! Ela só abriu porque você ajudou o mestre Castor.' }
      ]
    }
  ]
}
