# Pesquisa profunda — DESIGN VISUAL de apps educativos (2026-07)

> Encomendada pelo Marcos ("modelo visual bem atraente + ver os códigos + ideias inovadoras").
> Deep-research: 107 agentes, verificado. VEREDITO: nosso modelo "fofo arredondado" está CERTO.
> Destilado e aplicado no `eduverse/style-bible/modelo-visual-ui.md`. Fonte forte: design system
> oficial da Duolingo, WCAG, baby schema (Kindchenschema).

## OS 6 ACHADOS
1. **Linguagem de 3 formas (alta conf.):** todo o visual fofo = retângulo arredondado (mais usado) +
   círculo + triângulo arredondado; TODA borda arredondada (pontudo = off-brand); interesse vem do
   RITMO (variar pesos) com o MÍNIMO de formas. Copiável: SVG (rect rx/circle/path) + border-radius.
2. **Cor tokenizada (alta):** variáveis CSS nomeadas (Chrome 109 suporta), não hex cru. Duolingo:
   âncora Feather Green #58CC02; superfície do mascote Mask Green #89E219; TEXTO quase-preto Eel
   #4B4B4B (nunca preto puro); fundo off-white "Snow".
3. **Mascote por ciência (alta):** exagerar baby schema (cabeça/olhos grandes, bochechas, corpo
   redondo) = gatilho inato de "fofo". Estudo (Midjourney v5.2 + avaliação humana) confirma que
   prompt "cute" prioriza olhos grandes + corpo redondo → dá p/ gerar mascote fofo confiável via IA.
4. **Animação barata (alta):** SÓ transform + opacity (GPU, sem reflow/paint) + requestAnimationFrame
   (não setInterval). Exatamente certo p/ Chrome 109/PC fraco.
5. **Alvos de toque (alta):** WCAG 2.2 mín 24×24px; p/ criança ≥30px (conteúdo), ≥44–48px (ícones de borda).
6. **⚠️ Limite honesto (média):** fofura/mascote eleva PRAZER, mas NÃO há ganho de aprendizado provado;
   mascote intrusivo REDUZ prazer. "Fofo sim, onipresente não" — aparecer nos momentos certos.

## RESSALVAS
- A evidência verificada concentrou-se em Duolingo (forma/cor), baby schema e performance de animação —
  os pilares mais acionáveis e de fonte primária. Vários apps citados (Khan Kids, Prodigy, DragonBox,
  ST Math, Toca Boca, Sago Mini, Osmo, Blooket, Kahoot, Scratch, Minecraft) NÃO geraram claims
  verificados nesta rodada (ausência ≠ irrelevância).
- Páginas da Duolingo deram 403 a fetch direto (anti-bot); confirmação veio de snippets verbatim +
  espelhos independentes (sólido, mas não leitura direta).
- Psicologia do embodiment (Nature 2024) = amostra pequena, adolescente/adulto → extrapolar p/ 6–12 é inferência.

## O QUE JÁ APLICAMOS (bate com a pesquisa)
- Botão-pílula com relevo + saltinho; cartão fosco arredondado (capa de estrelas ✅ e Planeta Vivo ✅);
  animação só transform/opacity; mascote baby-schema gerado por IA.

## O QUE REFINAR (próximos passos)
- Tokens de cor nomeados (variáveis CSS) + texto quase-preto (não preto puro).
- Conferir alvos de toque ≥30/48px em todas as telas.
- Fonte redonda embutida (base64) — o toque que mais falta p/ "fofo".
- Mascote presente só nos momentos certos (não onipresente).
