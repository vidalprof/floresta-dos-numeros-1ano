# 🤖 QA que APRENDE — cada bug vira uma trava (não repete)

> Pedido do Marcos: "quem acha bug, aprende pra não acontecer de novo".
> Aqui mora a memória do auditor. **Toda vez que um erro novo aparecer, vira uma
> REGRA nova** (no `src/motor/auditor.ts` ou uma checagem no build) — assim ele
> **nunca mais passa silencioso**.

## As 3 camadas de trava automática

1. **Trava de ERRO DE JS (runtime)** — `index.html`: qualquer erro de código
   pinta uma **faixa vermelha** na tela → o **QA por screenshot pega na hora**.
   *(Foi o que faltou quando a colisão travou o `create()` sem avisar.)*
2. **Trava de DADOS (Zod)** — `motor/aventura.ts`: dado torto **não monta**
   (tipo errado, faltando campo → erro claro antes de montar).
3. **AUDITOR DE COERÊNCIA** — `motor/auditor.ts`: confere a cena e mostra uma
   faixa (o QA pega). Regras que ele já aprendeu:
   - peça com **asset que não existe** no kit;
   - peça **fora do mundo** (fora dos limites);
   - **COQUEIRO DENTRO DO MAR** (peça de terra numa zona de água);
   - **água/poça na terra seca**;
   - **sobreposição feia** (duas peças no mesmo lugar);
   - **herói começando na água / fora do mundo**;
   - **fala sem áudio** (cobertura de voz).

## Bugs já aprendidos nesta jornada (viraram trava)
- ⛔ `setCollideWorldBounds` numa imagem sem corpo → travava o `create()`.
  → Trava 1 (faixa vermelha) + usar `body.collideWorldBounds`.
- ⛔ Fundo **esticado** = distorção. → Regra de arte: nunca esticar (aspecto nativo).
- ⛔ **Perspectiva misturada** (poça de cima + praia de lado). → Cena coesa 3/4.
- ⛔ Personagem **flutuando** / papagaio subindo e descendo. → âncora nos pés + plantado.
- ⛔ Peça no lugar errado / coqueiro no mar. → **Auditor de coerência** (acima).

## Como CRESCE (o combinado)
Quando um erro novo escapar: (a) reproduz, (b) vira uma **regra no auditor** (ou
uma checagem no build), (c) anota aqui. O auditor **só cresce** — o mesmo erro
não volta duas vezes.
