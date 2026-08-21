# 🎪 O Grande Circo do Teo — PLANO (Pré)

Atividade nova, do zero, seguindo EXATAMENTE o modelo do `ATIVIDADE-PREMIUM.md`
(mesma tela inicial, mapa vivo, fluxo de fase, comemoração, narração que não
corta, gamificação, relatório). Só mudam tema/mascote/conteúdo/cores/imagens.

## Identidade
- **Tema:** circo. **Mascote:** **Teo**, um ursinho equilibrista (roupinha de circo).
- **História:** vai começar o grande espetáculo, mas uma ventania bagunçou o
  circo; a criança ajuda o Teo a arrumar cada parada do picadeiro pro show começar.
- **Cores:** tom festivo de circo (vermelho/dourado/azul), fundo escuro bonito com
  luzinhas. Definir paleta na montagem.
- **Público:** Pré. **Repo destino (sugestão):** `circo-do-teo` (confirmar nome).

## Paradas (11) + final de pintar
1. **Balões Coloridos** — Cores — classificar por cor (cesto)
2. **Contando no Picadeiro** — Números/contagem — contar e tocar no número (apoio ao erro por contagem acesa)
3. **Formas da Festa** — Formas — classificar forma (círculo/quadrado/triângulo)
4. **Ligar à Sombra** — Observação — arrastar animal do circo → sombra
5. **Caminho das Luzes** — Números em ordem — ligar os pontos 1–10, revela desenho
6. **Vogais do Circo** — Vogais — tocar na vogal inicial (falada foneticamente). A=arara, E=elefante, U=urso; I e O = Claude escolhe as imagens mais claras
7. **Qual é o Diferente?** — Atenção — tocar no diferente
8. **Quebra-Cabeça do Circo (1)** — montar foto 2×2 (fase-jogo, sem extra)
9. **Memória do Circo** — memória, achar pares (fase-jogo)
10. **Caça aos 7 Erros** — Atenção — achar as diferenças
11. **Quebra-Cabeça do Circo (2)** — 2º quebra-cabeça (fase-jogo)
- 🎨 **Final: Pintar o Circo** — recompensa livre (não conta nota)

## Decisões já fechadas com a professora
- **7 erros:** a professora gera 1 cena; **o Claude cria os 7 erros por código**
  (7 mudancinhas controladas: cor/sumir/trocar), clicáveis. Diferenças simples.
- **Pintar:** imagem bonita de contorno (linha preta), **paleta de cores grande**,
  **pincel gordinho** (fácil pra mãozinha do Pré), **musiquinha de circo
  sintetizada** (Web Audio, NÃO MP3 — leve/compatível), e a **voz fala o nome da
  cor** ao escolher. Recompensa livre no fim.
- **Mascote:** ursinho equilibrista "Teo".

## Regras de imagem (do manual)
- Toda imagem = foto real gerada no ChatGPT, **nunca SVG**.
- Cartelas: fundo branco puro #FFFFFF, SEM sombra, **contorno preto grosso e
  fechado** em cada objeto (inclusive claros), cartoon flat infantil cores vivas,
  objetos separados em grade, sem texto/números.
- Cenas (abertura/final/pintar/7-erros): retângulo deitado 3:2 preenchendo tudo
  (podem ter sombra; viram fundo/cena inteira).
- Sobe em `_imagens/`, Claude recorta (PIL) + de-fringe + limpa + otimiza + embute
  base64. **Apaga de `_imagens/` depois de embutir.**
- Capa = **medalhão redondo** na tela inicial (padrão fixo).

## Fluxo de construção (etapas)
1. **Fatia de teste primeiro:** mascote (4 poses) + cena de abertura → montar
   tela inicial "bem bacana" + mapa → mostrar à professora pra aprovar o estilo.
2. Depois, parada a parada: gerar prompts → prof gera/sobe → Claude integra.
3. Validação 3 níveis (dev/QA/pedagogo) + publicar via Fábrica + confirmar link.

## Status
- [x] Plano aprovado (tema, mascote, 11 paradas + pintar, 7-erros por código, pintar completo)
- [ ] Mascote + capa (1ª fatia)
- [ ] Paradas 2..11 (proxima: Contando no Picadeiro)
- [ ] Tela de pintar
- [ ] Validação + publicação
