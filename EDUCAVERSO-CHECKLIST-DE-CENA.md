# ✅ EducaVerso — CHECKLIST DE CENA (a "definição de pronto")

> **Regra do Marcos:** *"não podemos perder tempo consertando — os profissionais têm que pensar em TUDO."*
> Esta é a lista que **TODA cena/atividade** cumpre ANTES de chegar ao Marcos. O **Portão de Coerência**
> (auditor) reprova se faltar qualquer item. O **roteirista** já entrega o breakdown de cena preenchendo
> tudo isto; o **Diretor de Arte** e o **Engenheiro** realizam; o Portão confere. Nenhum item vira surpresa.

## 1. Coerência com a HISTÓRIA (o roteiro manda)
- [ ] Cada cena tem: **cenário, hora do dia, clima, personagens presentes, efeitos, sons, props** — todos
      vindos do roteiro (não improvisados).
- [ ] Tudo que aparece **faz sentido no contexto** (por que este prop/personagem está aqui?).
- [ ] A ação da criança e o objetivo pedagógico da cena estão claros.

## 2. PROPORÇÃO e ARTE (Diretor de Arte)
- [ ] **Proporção coerente com o Byte** (~64px): objetos do mundo (fruta, ferramenta) são **claramente
      menores** que o Byte; nada do tamanho dele ou maior sem motivo real.
- [ ] Alvo fácil p/ criança pequena **sem** aumentar o objeto: **brilho + área de toque generosa (invisível)**.
- [ ] **TUDO pintado por IA premium** e coerente com o `style-bible` — **nada geométrico code-drawn à mostra**
      (sem círculo/quadrado/losango de placeholder).
- [ ] Objetos colocados com lógica real (ex.: maçãs **penduradas nas árvores** + algumas caídas; não flutuando).
- [ ] Props só entram com contexto (ex.: fogueira = cena de NOITE com aldeões, não solta de dia).

## 3. AMBIENTE VIVO e RICO (Engenheiro + motor)
- [ ] Efeitos da cena ligados: **vento/sons da floresta, clima quando pedido (chuva/neve/tempestade+trovão),
      sombra direcional (sol/lua), nuvens, poeira ao andar, dia/noite**.
- [ ] **Personagens com VIDA e que INTERAGEM** com o Byte: micro-movimentos (respira/pisca/balança),
      NPCs que trabalham (lenhador etc.), **animais vivos** (cachorro corre+late, coelho pula), pássaros.
- [ ] **Rosto vivo** quando couber (olhos piscam, boca mexe ao falar) — por código sobre o sprite.
- [ ] Momentos de mundo: **anoitecer → cabana → dormir → continua** onde fizer sentido (checkpoint/save).

## 4. VOZ e ÁUDIO
- [ ] Narração **SEMPRE gerada por API (edge-tts, tipo Antonio)** e embutida em MP3 — **nunca voz do navegador**.
- [ ] Nada essencial é só-texto: **ícone + voz + cor**. Falas curtíssimas p/ os pequenos.
- [ ] SFX de ambiente/ação por Web Audio; sons de animais reais = CC0 por workflow.

## 5. PEDAGOGIA (Portão 0 — já existe)
- [ ] Não é quiz; a criança AGE e o número/descoberta vem DEPOIS. Erro = consequência gentil (sem X).
- [ ] O Byte **pergunta**, não entrega. Trava no objetivo (só conclui demonstrando a habilidade).
- [ ] **Adequação à turma/idade** (falas, mecânica, alvos, ritmo, velocidade do balão).

## 6. SUSTENTÁVEL e REUSÁVEL
- [ ] Todo asset/mecânica criado entra na **biblioteca** (reuso) — nada one-off.
- [ ] **Leve/compatível** (ES5, 1 HTML, sem CDN; roda em PC velho/celular).
- [ ] Gera 1x, reusa sempre (cache por hash); pago só onde é insubstituível (Gemini), cacheado.

---
**Como usar:** o roteirista preenche §1 no breakdown; Diretor de Arte cobre §2; Engenheiro cobre §3–4; Portão 0
cobre §5; todos respeitam §6. O **Portão de Coerência** roda esta lista inteira e **reprova** o que faltar —
volta pro profissional certo, **nunca pro colo do Marcos.**
