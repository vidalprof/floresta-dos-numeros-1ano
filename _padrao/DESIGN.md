# DESIGN.md — o sistema de design da casa (tokens) e como ele é medido

> Ordem do Marcos (2026-09-07): *"quero que nossa produção seja como os grandes sites e
> empresas: apps bonitos, leves, funcionais, completos, modernos e sem erros"*. O que
> separa um app de estúdio grande de um app "montado" é que **tudo obedece a um sistema
> só**: as mesmas cores, os mesmos raios de canto, a mesma escala de letra, as mesmas
> sombras e a mesma duração de movimento, em todas as telas. Este arquivo É esse sistema.
> O portão `_qa/design.py` mede quanto cada peça foge dele (deriva) e **reprova quando a
> deriva CRESCE** em relação ao que já está registrado (catraca: nunca piora; lapidar
> uma peça abaixa a marca dela para sempre).

## 1. Cor — só pelos tokens do motor (`:root` do `motor.html`)

| Token | Valor | Uso |
|---|---|---|
| `--verde` / `--verde-d` | `#5bbf3a` / `#3f9a26` | acerto, progresso, botão principal (base e sombra dura) |
| `--sol` / `--sol-d` | `#ffd43b` / `#eab000` | destaque, botão secundário, selo do que está piscando |
| `--coral` | `#ff7a6b` | "tente de novo" gentil (nunca vermelho puro, nunca "errou") |
| `--rosa` | `#ff8ac2` | festa, medalha |
| `--roxo` | `#7d3fe0` | selo da fase |
| `--terra` | `#a6703c` | madeira, moldura, chão |
| `--texto` | `#3a3020` | TODO texto que cai no fundo da atividade (segue o tema) |
| `--card` / `--linha` | `#fffdf6` / `#e6dcc6` | cartão, ficha, carta; a linha fina delas |

Neutros permitidos além dos tokens: `#fff`, `#f4efe6` (creme sobre mesa escura),
`#221a12` (tinta sobre cartão claro), `rgba(...)` (véus e sombras).

**Regras:**
- Texto que cai no fundo da atividade: `color:var(--texto)`. Nunca hex cravado
  (portão 4c `cor_fixa.py`; e o tema claro do `tema_claro.js` mede o resultado).
- Cor própria só **com a mesa própria** (fundo pintado junto), como `.fcab/.ftxt` do
  investigar-fonte.
- Quatro marrons quase iguais (`#221a12 #4a3608 #33280a #3a2c07`) hoje convivem nas
  peças: é deriva. Ao lapidar, usar `#221a12` sobre claro e `#f4efe6` sobre escuro.

## 2. Tipo — uma família, uma escala

- Família: **Fredoka** (já no motor), com `ui-rounded, "Segoe UI", system-ui` de reserva.
- Escala (px): **12 · 13.5 · 15 · 17 · 19 · 22 · 26 · 32**. Pesos: 600 (texto), 700
  (rótulo), 800 (título/ficha). Fora da escala é deriva.
- Piso de leitura: 15 px para frase que a criança lê; 12 px só para rótulo curto
  (contador, "3 de 32").
- `line-height` 1.2 em título, 1.35 em texto corrido.

## 3. Espaço e raio

- Espaço em múltiplos de **4 px** (4 · 8 · 12 · 16 · 24 · 32). Folga mínima entre
  enunciado e o que vem depois: 13 px (regra do motor, `.balao + *`).
- Raio de canto: **8 · 12 · 16 · 22 · 999 (pílula) · 50 % (círculo)**. Cartão/ficha 16,
  balão 22, botão pílula, alvo pequeno 12, chip 8. Fora disto é deriva.
- Alvo de toque: ≥ 44 px até o 2º ano, ≥ 40 px depois (leiaute.js).

## 4. Sombra e relevo (o "toque de app")

- Botão principal: sombra dura de 6 px na cor `-d` + sombra macia
  (`0 6px 0 var(--verde-d), 0 12px 18px rgba(0,0,0,.25)`); ao pressionar, afunda 3 px.
- Cartão: `0 6px 18px rgba(30,50,20,.22)`. Ficha: `inset 0 2px 0 rgba(255,255,255,.95),
  0 4px 0 #c9bda6, 0 8px 13px rgba(0,0,0,.24)`.
- Nunca borda de 1 px cinza como único relevo (parece formulário, não app).

## 5. Movimento

- Durações: **.16 s** (resposta ao toque) · **.36 s** (entrada de elemento) · **.6 s**
  (troca de tela, pulo do mascote) · **1.15 s** (transição de casca).
- Curva padrão `cubic-bezier(.2,.9,.3,1)`; com "sobra" para chegada
  `cubic-bezier(.3,1.4,.5,1)`.
- Só `transform` e `opacity` (gamefeel R5). Nada em laço infinito sem função (leiaute
  regra 12). Tudo desligado em `prefers-reduced-motion`.
- Entrada em cascata: 30 ms entre irmãos, teto 8 (`_mtEntra`).

## 6. As cascas (`MODELOS-DE-APP.md`)

Casca muda a CENA e o GESTO, não os tokens: Conversa, Trilha, Cartas, Livro, Show e
Bancada usam a mesma paleta, a mesma escala e as mesmas sombras. É isso que faz a
criança sentir "outro app" sem perder a identidade da casa.

## 8. Orçamento de desempenho — `_qa/peso.py <pasta>` (0b8 no pré-voo)

Leve é número, não opinião. Medido em 2026-09-07 nas seis atividades no ar: index
comprimido 134–226 KB (o montador só embute as mecânicas usadas), imagens 2–12 MB,
maior imagem 177–756 KB, áudio 9–14 MB (carregado por demanda, não pesa na abertura).

| Medida | Alvo (aviso acima) | Reprova acima |
|---|---|---|
| index comprimido (gzip) | 220 KB | 300 KB |
| uma imagem | 400 KB | 900 KB |
| imagens somadas | 6 MB | 15 MB |

O portão diz **o que otimizar primeiro** (as 5 maiores, com dimensão): figura de peça em
~512 px no lado maior, fundo/cena em ~1024 px, e recompressão (PNG com paleta ou WebP)
quando a dimensão já está certa. Fila de hoje: Museu (11,8 MB em 69 imagens), Sólidos
(medalha de 756 KB, quebra-cabeça de 672 KB), Central (5 imagens acima de 400 KB).

## 7. Como se mede — `_qa/design.py`

```
python3 _qa/design.py                 # deriva por peça + total; reprova se CRESCEU
python3 _qa/design.py --gravar        # registra a marca de agora (depois de lapidar)
python3 _qa/design.py --peca ordenar  # detalhe de uma peça (o que exatamente foge)
```

Conta, no `<style>` de cada peça: cor hex fora dos tokens/neutros, `border-radius` fora
da escala, `font-size` fora da escala. A marca fica em `_qa/_design_base.json`. Peça
que **piora** reprova (código 1); peça nova nasce com deriva 0 exigida. Lapidar =
trocar pelos tokens e rodar `--gravar`.
