// Gera o LOTE de falas do Antonio (id = hash da fala, igual ao vozHash do motor) para
// o workflow gerar-audio.yml. Só as falas FIXAS (as dinâmicas seguem em texto por ora).
function vozHash (s) { let h = 5381; for (let i = 0; i < s.length; i++) h = (((h << 5) + h) + s.charCodeAt(i)) >>> 0; return h.toString(36) }
const norm = s => s.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim()
const FALAS = [
  'A notícia se espalhou — a encomenda CRESCEU! Agora são mais potes pra arrumar.',
  'A carroça chegou ao rio: 3 fregueses esperam, cada um com a SUA caixa!',
  'São 3 caixas — uma pra CADA freguês — e ninguém aceita menos que o outro. Como repartir os 12 potes pra ficar justo?',
  'Você DIVIDIU: 12÷3! Bora pro pomar! 🌟',
  'No pomar a colheita rendeu 18 potes — e de novo são 3 cestas iguais!',
  '18 potes, 3 cestas, tudo igual. Quantos vão em CADA cesta?',
  '18÷3=6! Você mandou muito bem! 🌟',
  'No alto da montanha, 4 amigos dividem a ÚLTIMA carga da aventura!',
  'Agora são 4 caixas iguais pra 12 potes. Quantos em cada uma?',
  'AULA COMPLETA! Você multiplicou E dividiu de vários jeitos! 🏆',
  'Opa! Na hora de carregar, uma caixa tombou… Por que será que ELA tombou e as outras não?',
  'Deixa eu conferir! Vamos contar juntos, caixa por caixa…',
  'Ainda tem potes soltos pelo campo! Nenhum pode ficar pra trás.',
  'Tudo numa caixa só? Ficou pesada demais — nem consigo levantar! Será que dá pra repartir em mais caixas?'
]
const lote = FALAS.map(f => ({ id: vozHash(norm(f)), texto: norm(f) }))
console.log(JSON.stringify(lote))
