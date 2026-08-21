// ============================================================================
// AVENTURA "O POMAR DO BYTE" — o 1º mundo produzido pela FÁBRICA DE MUNDOS.
// 4 zonas exploráveis (pomar → colina → cabana/interior → lago) em pranchas
// pintadas por IA, com MISSÃO DENTRO DO MUNDO (o coelhinho está com fome —
// SEM enunciado numérico; a contagem é narrada pela voz enquanto a criança age;
// o conceito "contar" é nomeado POR ÚLTIMO). O mundo LEMBRA da criança.
// Objetivo (invisível): contagem 1 a 5 — BNCC EF01MA01/EF01MA02.
// ============================================================================
import type { TAventuraIn } from '../motor/aventura'

const BYTE = { quem: 'Byte', cor: '#2a9fb3' }

export const AVENTURA_POMAR: TAventuraIn = {
  id: 'pomar_v1',
  titulo: 'O Pomar do Byte',
  tema: 'pomar',
  objetivo: 'Contagem de 1 a 5 (BNCC EF01MA01, EF01MA02) — invisível ao aluno',
  conceito_final: 'CONTAR',
  heroi: 'byte',
  zona_inicial: 'pomar',
  inicio: { x: 620, y: 950 },
  zonas: [
    // ------------------------------------------------ ZONA 1: O POMAR
    {
      id: 'pomar',
      nome: 'O Pomar',
      prancha: 'z_pomar.jpg',
      largura: 1440, altura: 1440, chao_min_y: 700,
      paradas: [
        {
          id: 'coelho', nome: 'O Coelhinho', x: 1000, y: 1000, cor: '#ffd25a', marcador: false,
          objetos: [],
          personagens: [{ nome: 'coelho', x: 1000, y: 1000, alt: 92, npc: true, fala_ao_chegar: ['w_coelho'] }],
          falas: []
        }
      ],
      missao: {
        tipo: 'colher', asset: 'maca', alt: 52,
        itens: [{ x: 420, y: 880 }, { x: 610, y: 960 }, { x: 780, y: 860 }, { x: 540, y: 1120 }, { x: 880, y: 1210 }],
        cesta: { x: 1010, y: 1130 },
        voz_prefixo: 'kn', npc: 'coelho',
        ao_completar: ['w_feito', 'w_desc', 'w_reflex'],
        fala_revisita: ['w_volta']
      },
      portais: [
        { x: 1360, y: 940, raio: 70, para: 'colina', spawn: { x: 190, y: 950 }, rotulo: 'Colina' }
      ],
      efeitos: { sol: { x: 1180, y: 190 }, polen: true },
      musica: 'mus_carefree',
      chegada: ['w_ola', 'w_anda'],
      falas: [
        { id: 'w_ola', ...BYTE, texto: 'Que lugar bonito! Este é o Pomar. Vamos explorar?' },
        { id: 'w_anda', ...BYTE, texto: 'Toque no chão para andar.' },
        { id: 'w_coelho', ...BYTE, texto: 'O coelhinho está com fome! Vamos colher maçãs para ele?' },
        { id: 'w_feito', ...BYTE, texto: 'Olha só a cestinha cheia! O coelhinho está feliz da vida!' },
        { id: 'w_desc', ...BYTE, texto: 'Você viu? Contando uma a uma, a gente descobre quantas maçãs colhemos. Isso tem nome: contar!' },
        { id: 'w_reflex', ...BYTE, texto: 'O que você mais gostou de explorar hoje?' },
        { id: 'w_volta', ...BYTE, texto: 'Você voltou! O pomar lembrou de você.' }
      ]
    },
    // ------------------------------------------------ ZONA 2: A COLINA
    {
      id: 'colina',
      nome: 'A Colina',
      prancha: 'z_colina.jpg',
      largura: 1440, altura: 1440, chao_min_y: 720,
      paradas: [
        {
          id: 'casa', nome: 'A Cabana', x: 950, y: 740, cor: '#e0a866', marcador: false,
          objetos: [{ asset: 'casa', x: 950, y: 700, alt: 240, vida: 'nada', colide: false, flip: false, terreno: 'terra' }],
          personagens: [], falas: []
        }
      ],
      portais: [
        { x: 90, y: 950, raio: 70, para: 'pomar', spawn: { x: 1280, y: 940 }, rotulo: 'Pomar' },
        { x: 950, y: 745, raio: 58, para: 'cabana', spawn: { x: 720, y: 1180 }, rotulo: 'Cabana' },
        { x: 1360, y: 1050, raio: 70, para: 'lago', spawn: { x: 190, y: 1010 }, rotulo: 'Lago' }
      ],
      efeitos: { sol: { x: 1120, y: 180 }, polen: true },
      musica: 'mus_carefree',
      chegada: ['w_colina', 'w_casa'],
      falas: [
        { id: 'w_colina', ...BYTE, texto: 'Lá do alto da colina dá para ver bem longe!' },
        { id: 'w_casa', ...BYTE, texto: 'Uma cabana! Vamos entrar e ver como é lá dentro?' }
      ]
    },
    // ------------------------------------------------ ZONA 3: DENTRO DA CABANA
    {
      id: 'cabana',
      nome: 'Dentro da Cabana',
      prancha: 'z_cabana.jpg',
      largura: 1440, altura: 1440, chao_min_y: 1050,
      paradas: [],
      portais: [
        { x: 720, y: 1380, raio: 84, para: 'colina', spawn: { x: 950, y: 860 }, rotulo: 'Sair' }
      ],
      efeitos: { lareira: { x: 235, y: 850 }, polen: false },
      musica: 'mus_wallpaper',
      chegada: ['w_dentro'],
      falas: [
        { id: 'w_dentro', ...BYTE, texto: 'Que aconchegante! A lareira está acesa.' }
      ]
    },
    // ------------------------------------------------ ZONA 4: O LAGO
    {
      id: 'lago',
      nome: 'O Lago',
      prancha: 'z_lago.jpg',
      largura: 1440, altura: 1440, chao_min_y: 880,
      paradas: [
        {
          id: 'barco', nome: 'O Barquinho', x: 1050, y: 900, cor: '#8fd4ff', marcador: false,
          objetos: [{ asset: 'barco', x: 960, y: 820, alt: 130, vida: 'flutua_suave', colide: false, flip: false, terreno: 'agua' }],
          personagens: [], falas: []
        }
      ],
      portais: [
        { x: 90, y: 1050, raio: 70, para: 'colina', spawn: { x: 1280, y: 1050 }, rotulo: 'Colina' }
      ],
      efeitos: { sol: { x: 1150, y: 190 }, polen: true },
      musica: 'mus_carefree',
      chegada: ['w_lago'],
      falas: [
        { id: 'w_lago', ...BYTE, texto: 'Um lago! Olha o barquinho balançando na água.' }
      ]
    }
  ]
}
