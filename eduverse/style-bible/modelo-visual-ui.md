# 🎨 MODELO VISUAL DE UI — "fofo arredondado" (design system das atividades)

> Marcos pediu (2026-07): "um modelo visual bem atraente, que todo mundo goste".
> Este é o **design system das telas/UI** das atividades (botões, cartões, cor, tipo,
> movimento, mascote). Complementa o `ambiente-vivo.md` (que é do mundo/cena).
> Demo pronto: `scratchpad/modelo-visual.html` (aberto = botões saltam ao tocar).
> **Uma pesquisa profunda de design (fontes + código) está rodando** — quando chegar,
> refina/confirma este doc. Base atual = consolidado de UX infantil (Duolingo/Toca Boca/
> Khan Kids: "friendly rounded", personagem-forte, pouco texto, feedback imediato).

## POR QUE ESTE ESTILO
Formas redondas + personagem forte + pouco texto = lê como **BRINQUEDO, não escola**
(o que o Marcos quer). É o mais amado por crianças 6–12 **e** o mais leve (forma chapada
arredondada + 1 sombra roda liso em PC fraco). Regra de ouro: **tudo transform/opacity**.

## 1) PALETA (hex)
- **Base clara** `#fff7ec` · **Base escura** `#141a2e` · texto `#20264a` / claro `#eef1ff`.
- **Acentos vivos e harmônicos** (cor por MUNDO/disciplina):
  verde `#3fbf6a` (Geografia) · azul `#3aa0ff` (Matemática) · amarelo-sol `#ffcf3f`
  (Ciências) · coral `#ff7a6b` (Língua) · roxo `#8a6bff` (extra).
- Cada botão/chip = **gradiente leve** (topo mais claro → base mais escura) + a sombra da cor.

## 2) SHAPE LANGUAGE (formas)
- Cartão: `border-radius:22px`. Botão: **pílula** `border-radius:999px`. Chip: `18px`.
  Ícone-quadrado: `12px`. **Nada de canto reto.** Tudo "gordinho".
- Alvo de toque **grande** (≥48px de altura).

## 3) PROFUNDIDADE barata (1 sombra + relevo)
- Cartão: **1 sombra suave** `0 10px 24px rgba(40,60,120,.16)`.
- Botão "apertável" (dá vontade de tocar): sombra dupla = **relevo embaixo** +
  sombra de contato: `box-shadow:0 6px 0 <cor-escura>, 0 12px 18px rgba(..,.3)`.
  Ao `:active` → afunda (`translateY(4px) scale(.98)` + relevo curto). = feedback físico.

## 4) TIPOGRAFIA
- Fonte **redonda e legível** (Fredoka / Baloo 2 / Nunito). Offline → **embutir base64**
  (a legibilidade infantil vale o peso). Fallback: `"Segoe UI Rounded","SF Pro Rounded",system-ui`.
- Título **900** (bem gordo), corpo **700**. **Pouco texto** — a voz faz o resto.

## 5) KIT DE MOVIMENTO (durações/easings padrão — só transform/opacity)
- **Toque**: saltinho `scale .96→1.05→1`, ~180ms, `ease-out-back` (afunda no active).
- **Botão principal**: pulso lento `scale 1→1.04` 1.8s (chama o dedo).
- **Troca de tela**: deslizar + fade, ~300ms.
- **Celebração de acerto**: pop + partículas (estrelas) + tremidinha curta (~340ms) + flash.
- **Idle do mascote**: flutua/respira 3s + pisca. NUNCA fica parado morto.
- Regra: nada de animação longa; feedback é **imediato** (<120ms de resposta ao toque).

## 6) MASCOTE (regra de ouro)
- **Baby schema** (Kindchenschema): cabeça grande, **olhos grandes**, bochechas, sorriso.
- **Silhueta reconhecível** de longe; **cor de identidade fixa** (Fagulha=amarelo estrela; Nara=exploradora).
- 4–5 poses (fala/pensa/comemora/acena) + **respira + pisca** sempre. Lip-sync na fala.
- Consistente entre TODAS as telas. É o rosto da marca.

## 7) UI/UX infantil
- **Feedback imediato** em tudo; **affordance óbvia** (parece tocável).
- **Menos leitura** (texto curto + voz); **onboarding jogando** (sem tutorial chato).
- **Acessível**: contraste WCAG nos 2 temas; não depender só de cor (daltônicos);
  alvo grande; `alt` nas imagens.
- **Evitar**: poluição visual, enfeite que não muda com o modelo (detalhe sedutor), inconsistência.

## ✅ CHECKLIST "tela premium visualmente atraente"
1. [ ] Cantos redondos (22px cartão / pílula botão) — zero canto reto.
2. [ ] 1 sombra suave + botão com relevo "apertável".
3. [ ] Cor do mundo/disciplina aplicada (gradiente + sombra da cor).
4. [ ] Fonte redonda, título gordo, **pouco texto**.
5. [ ] Toque com saltinho + feedback <120ms.
6. [ ] Mascote presente, vivo (respira/pisca) e consistente.
7. [ ] Alvos grandes, contraste WCAG, sem poluição.
8. [ ] Celebração com pop+partículas quando acerta.

## 💡 IDEIAS VISUAIS INOVADORAS (para DESTACAR — virar nossa marca)
1. **Céu reage à HORA REAL** do relógio (manhã/tarde/noite) — "o app sabe". Quase ninguém faz.
2. **Cenas vivas pintadas por IA** com direção de arte consistente + movimento sutil no Canvas
   (parallax/partículas) = **nosso diferencial** (grátis com cara de pago).
3. **Mapa-mundo que floresce** conforme a criança avança (ilha apagada → cheia de vida).
4. **Transições de storybook** (virar página / câmera passeando) em vez de corte seco.
5. **UI diegética** (botão vira placa de madeira / cristal que brilha) — parte do mundo.
6. **"Marca" do mascote**: um gesto/som que ele SEMPRE faz (como a coruja do Duolingo).

## ✅ CONFIRMADO + REFINADO PELA PESQUISA (107 agentes, 2026-07 — fonte: design system Duolingo, WCAG, baby schema)
A pesquisa profunda **validou** este modelo e trouxe refinamentos de fonte primária:
1. **LINGUAGEM DE 3 FORMAS (adotar já):** todo o visual fofo nasce de **3 primitivas** — **retângulo
   arredondado** (a mais usada), **círculo** e **triângulo arredondado** — **toda borda arredondada**
   (forma pontuda = "off-brand"). O interesse vem do **RITMO**: variar formas de pesos diferentes, com o
   **mínimo** de formas. Traduz direto p/ SVG (`rect rx`, `circle`, `path`) e `border-radius` em tudo.
2. **TOKENS DE COR NOMEADOS (adotar já):** usar **variáveis CSS** com nome semântico (Chrome 109 suporta),
   não hex cru espalhado. Ex.: `--marca`, `--acao`, `--superficie-mascote`, `--texto`. **Texto = quase-preto
   `#3a3f52`/`#4B4B4B`, NUNCA preto puro** (suaviza o contraste — jeito Duolingo "Eel").
3. **MASCOTE FOFO POR CIÊNCIA:** exagerar o **baby schema** (cabeça grande, **olhos grandes e fundos**,
   bochechas redondas, corpo arredondado) dispara o "cuidado" inato. **Estudo confirmou que prompt "cute"
   na IA prioriza olhos grandes + corpo redondo** → nossa geração de mascote por workflow está no caminho.
4. **ANIMAÇÃO (regra de ouro p/ PC fraco):** animar **SÓ transform e opacity** (compostos na GPU, sem
   reflow/repaint) + **requestAnimationFrame** (nunca setInterval). Já fazemos — manter como LEI.
5. **ALVOS DE TOQUE:** mínimo **24×24px** (WCAG 2.2), e p/ criança **≥30px** (conteúdo) / **≥44–48px**
   (ícones de borda). Conferir em toda tela.
6. **⚠️ MASCOTE FOFO SIM, ONIPRESENTE NÃO (limite honesto):** a fofura eleva o **prazer**, mas **não há
   ganho de aprendizado provado** — e mascote **intrusivo/chato REDUZ o prazer**. Regra: aparecer nos
   momentos certos (celebração, dúvida, onboarding), **sem interromper/invadir** a tarefa.

> Doc completo da pesquisa: `PESQUISA-DESIGN-VISUAL-2026-07.md`.

> **Próximo passo:** aplicar este modelo (botões-pílula, relevo, saltinho, cores por mundo, tokens de cor,
> texto quase-preto) nas telas reais (capa ✅, mapa, botões) — 1 tela de cada vez, com prévia ao Marcos.
