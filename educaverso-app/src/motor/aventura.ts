// ============================================================================
// ESQUEMA DE DADOS DA AVENTURA (validado por Zod)
// É o "contrato" que o ROTEIRO preenche e o MONTADOR (motor) lê pra armar o
// mundo vivo. Dado torto NÃO compila: o Zod valida antes de montar.
// Uma aventura = um mundo amplo + várias PARADAS. Trocar de aventura = trocar
// este objeto de dados (a mesma máquina monta qualquer uma).
// ============================================================================
import { z } from 'zod'

// vida procedural que o motor dá a um objeto parado (sem gerar quadro)
export const Vida = z.enum(['nada', 'balanca', 'brilha', 'tremula', 'gira', 'flutua_suave'])

// um objeto colocado no mundo (arte de IA do kit)
export const Objeto = z.object({
  asset: z.string(),                 // chave do kit (ex.: 'palmeira')
  x: z.number(), y: z.number(),
  alt: z.number().default(120),      // altura em px (dimensiona pela ALTURA)
  vida: Vida.default('nada'),
  colide: z.boolean().default(false),
  flip: z.boolean().default(false),
  profundidade: z.number().optional(),
  // COERÊNCIA: onde esta peça PODE ficar (o auditor confere).
  // 'terra' = coqueiro/pedra (NUNCA no mar); 'agua' = poça/barco; 'qualquer' = livre.
  terreno: z.enum(['terra', 'agua', 'qualquer']).default('terra')
})

// um personagem no mundo (usa a cartela de poses -> animado)
export const PersonagemRef = z.object({
  nome: z.string(),                  // pasta do atlas (ex.: 'heroi', 'louro')
  x: z.number(), y: z.number(),
  alt: z.number().default(90),
  npc: z.boolean().default(true),    // false = é o herói (a criança controla)
  fala_ao_chegar: z.array(z.string()).default([])  // ids de fala quando a criança se aproxima
})

// uma fala (o áudio MP3 do Antonio é 'audio/<id>.mp3')
export const Fala = z.object({
  id: z.string(),
  quem: z.string(),
  texto: z.string(),
  cor: z.string().default('#2e9c5b')
})

// uma parada do mundo (ponto de história + degrau da mecânica)
export const Parada = z.object({
  id: z.string(),
  nome: z.string(),
  x: z.number(), y: z.number(),      // onde fica no mapa
  cor: z.string().default('#ffd25a'),
  objetos: z.array(Objeto).default([]),
  personagens: z.array(PersonagemRef).default([]),
  // mecânica desta parada (do catálogo); params são livres por mecânica
  mecanica: z.object({
    id: z.string(),                  // ex.: 'ordenar_comandos', 'contar'
    params: z.record(z.any()).default({})
  }).optional(),
  // interior explorável (cabana/gruta): se existir, a parada tem porta
  interior: z.object({
    chao: z.string(),                // asset do fundo do interior
    objetos: z.array(Objeto).default([]),
    personagens: z.array(PersonagemRef).default([])
  }).optional(),
  falas: z.array(Fala).default([])
})

// o mundo (chão amplo + ambiente)
export const Mundo = z.object({
  largura: z.number().default(2400),
  altura: z.number().default(1600),
  chao: z.string(),                  // asset do chão (grande/tileável)
  hora: z.enum(['dia', 'tarde', 'noite']).default('noite'),
  ambiente_sons: z.array(z.string()).default([]),  // ex.: ['mar','grilos']
  // COERÊNCIA: retângulos de ÁGUA (mar/rio). O auditor usa pra pegar
  // "coqueiro dentro do mar" (peça de terra numa zona de água).
  zonas_agua: z.array(z.object({ x: z.number(), y: z.number(), w: z.number(), h: z.number() })).default([])
})

// a AVENTURA completa
export const Aventura = z.object({
  id: z.string(),
  titulo: z.string(),
  tema: z.string(),
  objetivo: z.string(),              // objetivo de currículo (invisível ao aluno)
  conceito_final: z.string(),        // a palavra nomeada SÓ no fim
  estilo: z.string().default('limpo'),
  heroi: z.string().default('heroi'),// atlas do personagem do aluno
  inicio: z.object({ x: z.number(), y: z.number() }),
  mundo: Mundo,
  paradas: z.array(Parada).min(1)
})

export type TAventura = z.infer<typeof Aventura>
export type TParada = z.infer<typeof Parada>
export type TObjeto = z.infer<typeof Objeto>
export type TPersonagemRef = z.infer<typeof PersonagemRef>
export type TFala = z.infer<typeof Fala>

// valida (dado torto não monta) e devolve a aventura tipada
export function validarAventura (dados: unknown): TAventura {
  return Aventura.parse(dados)
}
