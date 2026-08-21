# 🏭 ESQUEMA DE PRODUÇÃO — como nasce uma aventura de 55 min (EducaVerso)

> A regra que o Marcos fixou: **a HISTÓRIA nasce primeiro** (a partir de um
> objetivo), e **dela geramos tudo**. Este é o esquema fixo, com **todos os
> profissionais**, que produz QUALQUER aula. Montado uma vez → cada aula nova é
> rodar o mesmo esquema com um objetivo novo.

## O FLUXO (design primeiro → gera → monta)

```
OBJETIVO (ex.: "números até 30")
   │
   ▼
1. PEDAGOGO/CURRICULISTA  → amarra na BNCC + define o que o aluno deve alcançar
   │                         + a estrutura de 55 min (5/35/10/5) + como avaliar (invisível)
   ▼
2. ROTEIRISTA            → cria a HISTÓRIA: mundo amplo + VÁRIOS pontos de parada,
   │                         currículo INVISÍVEL (conceito nomeado só no fim)
   ▼
3. GAME DESIGNER         → escolhe a MECÂNICA (do catálogo) e a progressão em degraus
   │                         por parada
   ▼
4. DIRETOR DE ARTE +     → define o ESTILO (limpo de jogo) e a LISTA DE ASSETS que a
   ESPECIALISTA EM PROMPT   história pede (por parada)
   │
   ▼
5. FÁBRICAS (IA)         → geram o KIT a partir da lista: personagens (cartela de
   │  (Pollinations/Gemini)  poses), objetos, chãos — recorte/alinhamento automático
   ▼
6. SOUND DESIGNER        → som ambiente em camadas + efeitos + VOZ ANTONIO (edge-tts)
   │
   ▼
7. ENGENHEIRO / MONTADOR → o motor (Phaser) LÊ os dados da história e ARMA o mundo:
   │                         paradas, personagens animados, objetos com vida, física,
   │                         mecânica, transições (fora↔interior)
   ▼
8. AUDITOR / QA          → portões (Filosofia, Técnico, Arte, Pedagogia) + QA por
   │                         SCREENSHOT no build (pega erro antes do Marcos ver)
   ▼
9. PROFESSOR MARCOS      → 3 aprovações (pedagogia · arte · mundo jogável) → PUBLICA
```

## Por que é REAPROVEITÁVEL
- A **mecânica** é cartucho do catálogo (algoritmo, contar/quantidade, …): montada
  1x, reusada. **Aula nova = história nova (dados) + kit novo (IA), mesma máquina.**
- O **estilo** é fixo (traço limpo) → tudo combina.
- A **avaliação invisível** é padrão → todo jogo gera relatório do professor.

## RECOMENDAÇÃO (resposta ao Marcos: "montar tudo antes ou já a 1ª atividade?")
**Montar o ESQUEMA e PROVAR com a 1ª atividade juntos** — não um esquema abstrato
sem atividade (não testado = risco), nem uma atividade sem esquema (não escala).
A **1ª aventura ("Números até 30")** é o **piloto** que roda o esquema de ponta a
ponta e o valida. Depois dela, as próximas aulas saem rápido pelo mesmo trilho.

### Ordem prática do piloto (Números até 30)
1. ✅ Pedagogo + Roteirista: história com 6 paradas (`aventuras/numeros-ate-30.md`).
2. Game Designer: fecha a mecânica "contar/quantidade" (degraus P1–P6).
3. Diretor de Arte: lista de assets do roteiro → Fábricas geram o kit (estilo limpo).
4. Engenheiro: montador lê os dados → mundo amplo com as 6 paradas + vida.
5. QA (screenshot) → Marcos aprova → publica → testa no Chrome 109.
