# 🚀 FASE 0 — EXECUÇÃO (arranque da fábrica) — checklist acionável

> Marcos aprovou "partir para a fábrica". Este é o **roteiro concreto** da Fase 0, pra
> executar direto (sem re-planejar) na próxima sessão. Risco ZERO: só reorganiza o que já
> funciona e prova reconstruindo a Floresta a partir de dados. Base: `EDUVERSE-PLANO.md`
> (planta dos 2 engenheiros), motor já provado em `_demos/educaverso/floresta/build_floresta3.py`
> (andar/mundo vivo/câmera/y-sort/áudio/QA) e `build_floresta2.py` (programar-robô/missões).

## Estrutura da fábrica (criada no arranque) — pasta `eduverse/`
```
eduverse/
  motor/        kit.js         (motor genérico: loop, câmera, tiles, y-sort, sprites,
                                mundo vivo, VM do robô, entrada teclado/D-pad, hooks QA)
  biblioteca/   raw/ proc/ recipes/ registro.json   (assets LEGO reprodutíveis)
  mundos/       <slug>/mundo.json                    (chão/tiles/objetos/ambiente)
  missoes/      <slug>/missao.json                   (arco pedagógico + falas-pergunta)
  builders/     montar.py      (dados + biblioteca + motor -> dist/<slug>/index.html)
  audit/        runner.py      (Portões 0/1/2 automáticos: node --check, render, DIRIGIR
                                a mecânica, colisão, sobreposição, filosofia)
  style-bible/  estilo.md  estilo-base.png  prompt-base.txt   (identidade visual travada)
  dist/         <slug>/index.html
```

## Passos (nesta ordem — cada um commitado)
1. **[ ] Criar a estrutura `eduverse/`** (feito no arranque) + mover a `estilo-base` (o Byte
   como âncora) para `style-bible/`.
2. **[ ] Extrair `motor/kit.js`** do `build_floresta3.py` (andar/câmera/y-sort/mundo vivo/áudio)
   + trechos do `build_floresta2.py` (VM do robô: setas → executa → erra na tela → depura).
   Regra: o kit **nunca** contém "floresta"/"gato"/coordenadas de atividade.
3. **[ ] Migrar assets da Floresta** para `biblioteca/` como `raw/` + `recipes/` (receita
   determinística de recorte) + `proc/` + `registro.json` (id, estilo, licença=IA).
4. **[ ] `builders/montar.py`** genérico: lê `mundos/floresta` + `missoes/floresta` + `kit.js`
   + embute **só os ids da missão** → `dist/floresta/index.html`.
5. **[ ] `audit/runner.py`** (o robô-auditor) com os Portões automáticos:
   - Portão 0: valida o **arco** (8 etapas na ordem), Byte **pergunta** (não instrui),
     sem "pergunta-para-abrir-porta" (proibido).
   - Portão 1: `node --check`; render headless sem erro; **DIRIGIR a mecânica** (`_qaSolve`
     + `--dump-dom`, ler `document.title`); **DIRIGIR a colisão** (andar contra borda/objeto
     e exigir bloqueio — a lição do navio!); peso < 2,5 MB; offline (sem URL externa).
   - Portão 2: **sobreposição** de imagens; y-sort/âncora nos pés; regressão visual.
6. **[ ] MARCO 0 (a prova):** reconstruir **"A Floresta do Byte" só a partir de dados** e
   confirmar, pelo runner, que ficou **igual/aprovada** (risco zero). ← fim da Fase 0.

## Depois da Fase 0
- **Fase 2 (a tese):** a missão **"O Rio" (Condição/SE)** montada **só com dados** reusando o
  kit — prova que **atividade nova nasce sem motor novo**.
- Temas: floresta, **navio pirata**, taberna viking, Vale das Máquinas — cada um = trocar as
  peças (chão/objetos/personagens) + a história. Mesmo motor, mesmo auditor.
- **TUDO temático, inclusive o BYTE** (regra do Marcos): o protagonista tem **cartela de
  costumes por tema** — Byte-pirata (chapéu/casaco/tapa-olho), Byte-viking (capacete), etc.,
  **gerados editando a imagem-âncora do Byte** (Gemini `base=byte`), pra continuar sendo o
  MESMO personagem, só vestido do tema. O auditor confere que o costume bate com o mundo.

## Lições pagas que JÁ viram regra do auditor (não repetir)
- "Personagem não se move" → o auditor **dirige** o boneco e exige movimento.
- "Colisão furada" → o auditor **dirige contra borda/objeto** e exige bloqueio (SEMPRE_NO_MAPA).
- Screenshot com tempo virtual **engana** → provar dirigindo + `--dump-dom`; foto ≥ 500px.
- Estilo derivando → **editar a imagem-âncora** (Gemini `base=`); prompt por motor (o
  **Especialista em Prompts**): Pollinations = tokens de estilo fortes; Gemini = linguagem natural.
