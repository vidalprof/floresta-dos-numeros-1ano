// ============================================================================
// ESQUEMA DE DADOS DA AVENTURA (validado por Zod)
// É o "contrato" que o ROTEIRO preenche e o MONTADOR (motor) lê pra armar o
// mundo vivo. Dado torto NÃO compila: o Zod valida antes de montar.
//
// v2 (fábrica de mundos): uma aventura = um GRAFO DE ZONAS. Cada zona é um
// pedaço explorável (prancha pintada por IA maior que a tela, câmera segue),
// ligado às vizinhas por PORTAIS (porta da cabana, saída da clareira...).
// A MISSÃO acontece DENTRO do mundo (a criança age nos objetos da cena),
// nunca numa "telinha de exercício". Trocar de aventura = trocar os DADOS.
// ============================================================================
import { z } from 'zod'

// vida procedural que o motor dá a um objeto parado (sem gerar quadro)
export const Vida = z.enum(['nada', 'balanca', 'brilha', 'tremula', 'gira', 'flutua_suave'])

// um objeto colocado no mundo (arte de IA do kit)
export const Objeto = z.object({
  asset: z.string(),                 // chave do kit (ex.: 'casa', 'barco')
  x: z.number(), y: z.number(),
  alt: z.number().default(120),      // altura em px (dimensiona pela ALTURA)
  vida: Vida.default('nada'),
  colide: z.boolean().default(false),
  flip: z.boolean().default(false),
  profundidade: z.number().optional(),
  terreno: z.enum(['terra', 'agua', 'qualquer']).default('terra')
})

// um personagem no mundo (usa a cartela de poses -> animado)
export const PersonagemRef = z.object({
  nome: z.string(),                  // pasta do atlas (ex.: 'byte', 'coelho')
  x: z.number(), y: z.number(),
  alt: z.number().default(90),
  npc: z.boolean().default(true),
  fala_ao_chegar: z.array(z.string()).default([])
})

// uma fala (o áudio MP3 da voz por API é 'audio/<id>.mp3')
export const Fala = z.object({
  id: z.string(),
  quem: z.string(),
  texto: z.string(),
  cor: z.string().default('#2e9c5b')
})

// uma parada do mundo (ponto de história; mecânica de painel é opcional/legado)
export const Parada = z.object({
  id: z.string(),
  nome: z.string(),
  x: z.number(), y: z.number(),
  cor: z.string().default('#ffd25a'),
  marcador: z.boolean().default(true),          // brilho que chama a criança
  objetos: z.array(Objeto).default([]),
  personagens: z.array(PersonagemRef).default([]),
  mecanica: z.object({ id: z.string(), params: z.record(z.any()).default({}) }).optional(),
  falas: z.array(Fala).default([])
})

// PORTAL: liga uma zona à outra (porta, trilha, tapete de saída...)
export const Portal = z.object({
  x: z.number(), y: z.number(),
  raio: z.number().default(64),
  para: z.string(),                              // id da zona destino
  spawn: z.object({ x: z.number(), y: z.number() }),  // onde nasce lá
  rotulo: z.string().default('')                 // nome curtinho (ex.: 'Colina')
})

// MISSÃO NO MUNDO: "colher" — a criança anda até cada item e o mundo reage.
// SEM enunciado numérico ("traga 5" é proibido): o pedido é do MUNDO (o
// coelhinho está com fome); a contagem é NARRADA (voz) conforme ela age, e o
// conceito é nomeado POR ÚLTIMO nas falas de conclusão. (Lei do Portão 0.)
export const MissaoColher = z.object({
  tipo: z.literal('colher'),
  asset: z.string(),                             // ex.: 'maca'
  alt: z.number().default(52),
  itens: z.array(z.object({ x: z.number(), y: z.number() })).min(1),
  cesta: z.object({ x: z.number(), y: z.number() }),
  voz_prefixo: z.string().default('kn'),         // kn1, kn2... (contagem falada)
  npc: z.string().optional(),                    // quem comemora (ex.: 'coelho')
  ao_completar: z.array(z.string()).default([]), // falas: consequência -> descoberta -> conceito -> reflexão
  fala_revisita: z.array(z.string()).default([]) // ao voltar com a missão feita (o mundo LEMBRA)
})

// efeitos de vida ambiente da zona (tudo leve; orçamento do PC fraco)
export const Efeitos = z.object({
  sol: z.object({ x: z.number(), y: z.number() }).optional(),  // brilho que respira
  polen: z.boolean().default(false),                            // partículas de luz
  lareira: z.object({ x: z.number(), y: z.number() }).optional()// brilho quente tremulando
})

// uma ZONA explorável (prancha pintada + paradas + portais + missão)
export const Zona = z.object({
  id: z.string(),
  nome: z.string(),
  prancha: z.string(),               // arquivo em img/ (ex.: 'z_pomar.jpg')
  largura: z.number().default(1440), // tamanho do MUNDO (maior que a tela!)
  altura: z.number().default(1440),
  chao_min_y: z.number().default(700),   // faixa andável começa aqui (horizonte)
  paradas: z.array(Parada).default([]),
  portais: z.array(Portal).default([]),
  missao: MissaoColher.optional(),
  efeitos: Efeitos.default({ polen: false }),
  musica: z.string().default(''),        // arquivo em audio/ (ex.: 'mus_carefree')
  chegada: z.array(z.string()).default([]),  // falas na 1ª visita
  falas: z.array(Fala).default([])
})

// a AVENTURA completa (o mundo = grafo de zonas)
export const Aventura = z.object({
  id: z.string(),
  titulo: z.string(),
  tema: z.string(),
  objetivo: z.string(),              // objetivo de currículo (invisível ao aluno)
  conceito_final: z.string(),        // a palavra nomeada SÓ no fim
  heroi: z.string().default('byte'),
  zona_inicial: z.string(),
  inicio: z.object({ x: z.number(), y: z.number() }),
  zonas: z.array(Zona).min(1)
})

export type TAventura = z.infer<typeof Aventura>
export type TZona = z.infer<typeof Zona>
export type TParada = z.infer<typeof Parada>
export type TObjeto = z.infer<typeof Objeto>
export type TPortal = z.infer<typeof Portal>
export type TPersonagemRef = z.infer<typeof PersonagemRef>
export type TFala = z.infer<typeof Fala>

// valida (dado torto não monta) e devolve a aventura tipada
export function validarAventura (dados: unknown): TAventura {
  const av = Aventura.parse(dados)
  // portais têm que apontar para zonas que existem (grafo fechado)
  const ids = new Set(av.zonas.map(z2 => z2.id))
  for (const zo of av.zonas) for (const p of zo.portais) {
    if (!ids.has(p.para)) throw new Error('portal de "' + zo.id + '" aponta para zona inexistente "' + p.para + '"')
  }
  if (!ids.has(av.zona_inicial)) throw new Error('zona_inicial inexistente: ' + av.zona_inicial)
  return av
}
