# 🤖 PESQUISA — Pensamento Computacional / BNCC Computação (guardado p/ ANO QUE VEM)

> O Marcos pediu pra DEIXAR computação de lado por enquanto (este ano = currículo
> normal; micro-mundos/simulações). Esta pesquisa fica ARQUIVADA para quando ele for
> adaptar o currículo de Computação. Fontes completas no fim.

## O contexto legal (é obrigatório e recente)
- **Complemento à BNCC — Computação** homologado pelo MEC em **out/2022** (Parecer
  CNE/CEB nº 2/2022 + Resolução CNE/CEB nº 1/2022); implementação até out/2023.
- **3 eixos:** Pensamento Computacional (decompor/modelar/algoritmos), Mundo Digital,
  Cultura Digital. Anos iniciais = **transversal**, não disciplina nova, focado em
  padrões + raciocínio lógico. Habilidades codificadas `EFxxCOyy` (ex.: EF01CO01 =
  organizar por padrões). Referência prática por ano: **CIEB** (curriculo.cieb.net.br).

## O que tem EVIDÊNCIA
- **Wing:** PC = formular problema com solução computacional (decomposição, padrões,
  abstração, algoritmos). **Papert/construcionismo:** a criança PROGRAMA a máquina.
- **Brennan & Resnick (2012):** o framework que a academia mede — 7 conceitos
  (sequência, loops, paralelismo, eventos, condicionais, operadores, dados), 4 práticas
  (iterar, **testar/depurar**, reusar, abstrair), 3 perspectivas.
- **Depuração = aprendizado** (productive failure, Kafai & DeLiema) — rodar e ver o
  robô errar transforma erro em informação. É barato (lógica, não arte).
- **Evidência BR:** tese Brackmann (UFRGS 2017) — ganho significativo, ~45% em PC só
  com desplugado.
- **Honestidade:** Scratch funciona COM pedagogia estruturada (não uso livre); Hour of
  Code engaja mas evidência FRACA de transferência durável → precisa de TRILHA mediada,
  não atividade avulsa.

## 🔑 A FERRAMENTA QUE RESOLVE O GARGALO DE ARTE
- **Blockly (Google, Apache-2.0):** blocos arrastáveis profissionais, **client-side,
  offline, 1 HTML, PC fraco, grátis**, blocos customizáveis. É o "Code.org caseiro".

## TOP formatos p/ construir (mais aprendizado × mensurabilidade ÷ arte)
1. ⭐ **"Programe o robô num grid"** (avatar + blocos + execução passo a passo +
   depuração). Melhor custo-benefício. Cobre sequência→loops→condicionais e as EFxxCO.
   Arte = 1 sprite + quadrados. Medição stealth trivial (tentativas, blocos vs. ótimo,
   uso de repetição). Motor reutilizável (troca só o mapa em JSON). Fazer como TRILHA.
2. **Turtle/Logo** (desenhar com código) — ZERO arte (a criança gera a arte); ótimo p/
   Matemática (ângulos/polígonos).
3. **Bebras / labirinto múltipla escolha (BCTt/cCTt validados)** — ZERO arte e é
   atividade + INSTRUMENTO DE MEDIDA validado (pré/pós auto-corrigido → ganho %).
4. **Parsons / "monte o algoritmo"** (arrastar linhas p/ ordenar) — quase zero arte,
   auto-corrigível, ponte "ler antes de escrever" (PRIMM / Use-Modify-Create).
5. **Música com código (Sonic Pi-like, Web Audio)** — zero arte visual, autoria e
   autoeficácia altas (efeito maior em meninas).
6. ScratchJr caseiro (1º-2º) — mais autoral mas + sprites; deixar p/ depois.

## MEDIÇÃO (3 camadas, todas em JS)
- **Stealth** (Shute): motor grava tentativas, blocos usados vs. ótimo, uso de
  repetição, tempo, nº de depurações → placar de PC sem "cheirar a prova".
- **Diagnóstica:** 8-10 itens BCTt/Bebras (labirinto múltipla escolha) pré/pós.
- **Parecer/nota:** IA converte indicadores em rubrica (à la Dr. Scratch — nota 0-21 em
  7 componentes, validado) + texto alinhado às EFxxCO.

## O que faz ser INCRÍVEL sem arte (Papert "hard fun"; Resnick 4 P's; SDT)
Autoria + o mundo REAGENDO + progressão. "Eu fiz isso" (turtle/música provam que não
depende do professor desenhar). Botão que gera link/QR do desafio que a criança criou
(compartilhar sem servidor). Modo sandbox "crie o seu mapa" depois das fases guiadas.

## Fontes principais
BNCC Computação (gov.br/MEC, CNE/CEB 2/2022, CIEB curriculo.cieb.net.br); Wing 2006/2008
(CMU); Papert (MIT); Brennan&Resnick AERA 2012; Brackmann UFRGS 2017; Blockly
(developers.google.com/blockly); Lightbot (Common Sense); Bebras/ABC-Thinking (Springer);
BCTt/cCTt (arXiv 2203.05980, Frontiers); Dr. Scratch (ACM); Shute Stealth Assessment
(MIT Press OA); Sonic Pi; Resnick "Give P's a Chance" (MIT). URLs no histórico da sessão.
