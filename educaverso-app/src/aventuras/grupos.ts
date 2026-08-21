// ============================================================================
// AVENTURA "O POMAR DOS GRUPOS" — a 1ª dinâmica CRIATIVA (tabuada 3º ano).
// A ideia-mãe da multiplicação = GRUPOS IGUAIS. A criança CRIA a arrumação:
// pega cestas na pilha, decide QUANTAS usa e reparte as 12 maçãs. NÃO há
// gabarito: 2×6, 3×4, 4×3 e 6×2 TODAS vencem — a LEI só exige grupos iguais.
// Desigual = a cesta diferente TOMBA (consequência mostra ONDE) e o mentor
// PERGUNTA. O nome (3×4=12) é revelado POR ÚLTIMO, a partir da arrumação DELA.
// Gramática da casa: problema exposto (a PEDRONA fecha o caminho da feira) ->
// resolve no mundo -> o MUNDO MUDA (a pedra sai) -> atravessa -> festa.
// (Exemplo da FILOSOFIA: canteiros/grupos — aqui com os sprites que JÁ temos.)
// ============================================================================
import type { TAventuraIn } from '../motor/aventura'

const BYTE = { quem: 'Byte', cor: '#2a9fb3' }
const CASTOR = { quem: 'Mestre Castor', cor: '#8a5a2b' }

export const AVENTURA_GRUPOS: TAventuraIn = {
  id: 'pomar_grupos_v1',
  titulo: 'O Pomar dos Grupos',
  tema: 'pomar',
  objetivo: 'Multiplicação como GRUPOS IGUAIS (EF03MA07): a criança constrói o arranjo',
  conceito_final: 'MULTIPLICAR',
  heroi: 'byte',
  zona_inicial: 'pomar',
  inicio: { x: 420, y: 760 },
  zonas: [
    // ------------------------------------------------------------- O POMAR
    {
      id: 'pomar',
      nome: 'O Pomar',
      chao_textura: 'grama',
      largura: 1800, altura: 1200, chao_min_y: 260,
      bloqueios: [
        { id: 'saida', x: 1560, y: 640, w: 240, h: 460 }   // a PEDRONA fecha a trilha da feira
      ],
      paradas: [
        {
          id: 'pomar_area', nome: 'O Pomar', x: 900, y: 700, cor: '#57e08a', marcador: false,
          objetos: [
            // as macieiras e a mata (colisão: a criança anda ENTRE elas)
            { asset: 'arvore_a', x: 260, y: 400, alt: 300, vida: 'balanca', colide: true },
            { asset: 'arvore_b', x: 640, y: 330, alt: 315, vida: 'balanca', colide: true },
            { asset: 'arvore_a', x: 1040, y: 410, alt: 300, vida: 'balanca', colide: true, flip: true },
            { asset: 'arvore_b', x: 1420, y: 350, alt: 310, vida: 'balanca', colide: true },
            { asset: 'pinheiro', x: 150, y: 720, alt: 270, vida: 'balanca', colide: true },
            { asset: 'pinheiro', x: 1680, y: 420, alt: 280, vida: 'balanca', colide: true, flip: true },
            { asset: 'arvore_a', x: 180, y: 1120, alt: 290, vida: 'balanca', colide: true, flip: true },
            { asset: 'arbusto', x: 460, y: 480, alt: 92 },
            { asset: 'arbusto', x: 1220, y: 560, alt: 96, flip: true },
            { asset: 'arbusto', x: 540, y: 1140, alt: 90 },
            { asset: 'flores', x: 760, y: 470, alt: 56 },
            { asset: 'flores', x: 340, y: 940, alt: 52, flip: true },
            { asset: 'flores', x: 1140, y: 760, alt: 56 },
            { asset: 'flores', x: 880, y: 1150, alt: 54 },
            { asset: 'pedra', x: 1500, y: 1150, alt: 80, colide: true },
            // A PEDRONA — o problema EXPOSTO no mundo (sai quando a carga fecha)
            { id: 'pedrona', asset: 'rocha', x: 1660, y: 900, alt: 185, profundidade: 905 }
          ],
          personagens: [
            {
              nome: 'castor', x: 1380, y: 840, alt: 104,
              fala_ao_chegar: ['f_feira', 'f_carga', 'f_como']
            }
          ],
          falas: []
        }
      ],
      // A MISSÃO CRIATIVA: 12 maçãs, até 6 cestas — a arrumação é DELA
      missao: {
        tipo: 'agrupar', asset: 'maca', alt: 46, kc: 'grupos-iguais',
        itens: [
          { x: 300, y: 640 }, { x: 430, y: 540 }, { x: 570, y: 700 }, { x: 380, y: 870 },
          { x: 650, y: 590 }, { x: 760, y: 810 }, { x: 520, y: 1010 }, { x: 300, y: 1080 },
          { x: 830, y: 540 }, { x: 950, y: 640 }, { x: 700, y: 1110 }, { x: 980, y: 890 }
        ],
        caixa: 'cesta', caixa_alt: 104,
        pilha: { x: 1330, y: 1010 },
        vagas: [
          { x: 700, y: 1000 }, { x: 800, y: 1000 }, { x: 900, y: 1000 },
          { x: 1000, y: 1000 }, { x: 1100, y: 1000 }, { x: 1200, y: 1000 }
        ],
        npc: 'castor', voz_prefixo: 'kn',
        ao_sobrar: ['f_sobra'],
        ao_uma_caixa: ['f_uma'],
        ao_desigual: ['f_tomba', 'f_pensa'],
        ao_completar: ['f_igual', 'f_pedra'],
        conceito_prefixo: 'c_',
        fala_revisita: ['f_rev'],
        some_objeto: 'pedrona',
        remove_bloqueio: 'saida'
      },
      portais: [
        { x: 1730, y: 880, raio: 70, para: 'feira', spawn: { x: 220, y: 640 }, rotulo: 'Feira' }
      ],
      efeitos: { sol: { x: 1500, y: 170 }, polen: true },
      musica: 'mus_carefree',
      chegada: ['f_pomar'],
      falas: [
        { id: 'f_pomar', ...BYTE, texto: 'Chegamos ao pomar! Olha quanta maçã madura pelo chão…' },
        { id: 'f_feira', ...CASTOR, texto: 'Que bom que você chegou! A feira é hoje, ali atrás — mas a pedrona rolou e fechou a passagem.' },
        { id: 'f_carga', ...CASTOR, texto: 'Com a carroça carregada eu tiro a pedrona do caminho! Mas carroça só viaja firme se TODAS as cestas levarem o MESMO tanto de maçãs.' },
        { id: 'f_como', ...BYTE, texto: 'Pega as cestas na pilha e reparte as maçãs. Hmm… como será que fica igualzinho em todas?' },
        { id: 'f_sobra', ...CASTOR, texto: 'Ainda tem maçã solta no pomar! Nenhuma pode ficar pra trás.' },
        { id: 'f_uma', ...CASTOR, texto: 'Tudo numa cesta só? Ficou pesada demais, nem consigo levantar! Será que dá pra repartir em mais cestas?' },
        { id: 'f_tomba', ...CASTOR, texto: 'Opa! Na hora de carregar, uma cesta tombou… Por que será que ELA tombou e as outras não?' },
        { id: 'f_pensa', ...BYTE, texto: 'Olha bem as cestas. Tem alguma com MAIS maçãs? Alguma com MENOS?' },
        { id: 'f_igual', ...CASTOR, texto: 'Agora sim! Todas as cestas com o MESMO tanto — a carroça vai firme. Você repartiu certinho!' },
        { id: 'f_pedra', ...CASTOR, texto: 'Carroça carregada… e lá vai! Olha só: a pedrona saiu do caminho. A passagem está livre!' },
        { id: 'c_2x6', ...BYTE, texto: 'Você fez 2 grupos de 6 maçãs! Sabia que isso tem nome? Os matemáticos escrevem 2×6=12.' },
        { id: 'c_3x4', ...BYTE, texto: 'Você fez 3 grupos de 4 maçãs! Sabia que isso tem nome? Os matemáticos escrevem 3×4=12.' },
        { id: 'c_4x3', ...BYTE, texto: 'Você fez 4 grupos de 3 maçãs! Sabia que isso tem nome? Os matemáticos escrevem 4×3=12.' },
        { id: 'c_6x2', ...BYTE, texto: 'Você fez 6 grupos de 2 maçãs! Sabia que isso tem nome? Os matemáticos escrevem 6×2=12.' },
        { id: 'f_rev', ...CASTOR, texto: 'As maçãs já estão na feira! Obrigado, parceiro — a passagem segue livre.' }
      ]
    },
    // ------------------------------------------------------------- A FEIRA
    {
      id: 'feira',
      nome: 'A Feira',
      chao_textura: 'grama',
      largura: 1440, altura: 1080, chao_min_y: 240,
      festa_na_chegada: true,
      paradas: [
        {
          id: 'bancas', nome: 'As Bancas', x: 720, y: 540, cor: '#ffd25a', marcador: false,
          objetos: [
            { asset: 'casa', x: 420, y: 420, alt: 300, colide: true },
            { asset: 'casa', x: 1050, y: 440, alt: 290, colide: true, flip: true },
            { asset: 'bau_fechado', x: 760, y: 500, alt: 84 },
            { asset: 'cesta', x: 640, y: 700, alt: 100 },
            { asset: 'cesta', x: 860, y: 690, alt: 100, flip: true },
            { asset: 'flores', x: 540, y: 820, alt: 56 },
            { asset: 'flores', x: 930, y: 830, alt: 56, flip: true },
            { asset: 'arvore_a', x: 220, y: 900, alt: 290, vida: 'balanca', colide: true },
            { asset: 'arvore_b', x: 1240, y: 920, alt: 300, vida: 'balanca', colide: true, flip: true },
            { asset: 'tocha', x: 600, y: 520, alt: 96, vida: 'tremula' },
            { asset: 'tocha', x: 900, y: 520, alt: 96, vida: 'tremula' }
          ],
          personagens: [], falas: []
        }
      ],
      portais: [
        { x: 110, y: 640, raio: 70, para: 'pomar', spawn: { x: 1600, y: 900 }, rotulo: 'Pomar' }
      ],
      efeitos: { sol: { x: 1150, y: 160 }, polen: true },
      musica: 'mus_wallpaper',
      chegada: ['f_chegou', 'f_final'],
      falas: [
        { id: 'f_chegou', ...BYTE, texto: 'Você passou! A feira está uma festa — e as maçãs chegaram firmes, do jeitinho que você arrumou.' },
        { id: 'f_final', ...BYTE, texto: 'Repartir em grupos iguais… guarda esse truque! Ele vai aparecer de novo em muitos lugares.' }
      ]
    }
  ]
}
