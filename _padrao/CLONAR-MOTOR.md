# CLONAR O MOTOR DE UMA ATIVIDADE — a lista do que É CONTEÚDO e tem que trocar

> Nasceu da **Fábrica de Brinquedos do Bento** (ago/2026). Clonar o motor de uma
> atividade pronta é a regra da casa: economiza dias e traz de graça o lip-sync,
> o boletim, o relatório do professor, o "Treinar o que faltou" e a
> compatibilidade com os PCs velhos da escola.
>
> **O perigo é outro:** junto do motor vêm pedaços que são **CONTEÚDO da
> atividade de origem**, e eles não dão erro nenhum. O app abre bonito, o
> `node --check` passa, o print fica perfeito — e o defeito só aparece com a
> criança na frente. Nesta rodada foram **seis** defeitos assim, todos do mesmo
> parentesco.
>
> Rodar sempre: **`bash _qa/auditar.sh <pasta>/index.html`** — os portões 1c
> (resto de clone) e 3d (mascote) existem justamente por causa desta lista.

---

## 1. O que trocar SEMPRE ao clonar (a lista curta)

| o quê | onde | o que acontece se esquecer |
|---|---|---|
| **`var IMGS=[...]`** | topo do `<script>` | pré-carrega as imagens da OUTRA atividade: 404 em série e nenhuma imagem sua pronta. Nos PCs da escola, cada imagem aparece com atraso na primeira vez. |
| **`var VOZOK={...}`** | bloco do alto-falante | o botãozinho de voz aparece ao lado de respostas cujo MP3 não existe aqui. **Botão que não faz nada é pior que botão nenhum.** |
| **`var DOM={...}`** | bloco de medição | o boletim do fim e o relatório do professor mostram os conceitos da atividade de origem. |
| **`ROTCRI`, `TREINO`, `CONCD`** | fim do arquivo | mesmos conceitos, em linguagem de criança / mapa de treino / texto do professor. |
| **prefixo dos áudios** | `falar("xx_...")` | o mascote fica mudo na tela inteira. |
| **`sw.js` e `manifest.json`** | raiz da pasta | o nome do app e o cache ficam com o nome da outra. |
| **as 3 camadas do mascote** | `img/` | ver §2 — é o pior de todos. |
| **classes que o molde não pinta** | CSS | ver §3. |

---

## 2. ⭐ O MASCOTE: as poses NUNCA se geram do zero

O mascote são **três imagens empilhadas** (parado / falando / piscando) e o motor
cruza elas ~60 vezes por segundo para o lip-sync. Se as três forem desenhos
diferentes, o cruzamento **não anima a boca: morfa o boneco inteiro.** O Marcos
viu na hora: *"ao falar ou piscar o mascote se treme todo"*.

**A IA não obedece "mantenha exatamente igual" quando gera do zero.** Na Fábrica
a pose de piscar veio com outro tom de pele e outro cabelo.

**O jeito certo (e o único):**
1. Gerar só a pose **parada**.
2. Gerar as outras duas **EDITANDO** essa: `gerar-imagens.yml` com
   `modelo=gemini` + `base=_novo/<mascote>_base.png`, pedindo para mudar **só a
   boca** (ou **só os olhos**) e mais nada.
3. Recortar as três com a **MESMA bbox** (senão a imagem pula ao trocar de camada).
4. Conferir com `python3 _qa/mascote.py <pasta>` — reprova acima de 15%.

**Medida real do projeto** (quanto do corpo muda entre a pose parada e as outras):

| atividade | falar | piscar |
|---|---|---|
| Legenda do Clique | 0,7% | 2,5% |
| Jardim do Broto | 1,9% | 7,2% |
| Fábrica do Bento (depois do conserto) | 2,8% | 4,5% |
| Doceria do Cacau | 6,3% | 4,9% |
| Observatório do Órbi | 7,8% | 3,2% |
| **Fábrica do Bento (gerada do zero)** | **77%** | **78%** |

> No print parado as três parecem iguais. **O defeito só existe em movimento** —
> por isso tem que ser medido, não olhado.

---

## 3. Classe do molde que não é pintada aqui

A `.pc` (peça) da Legenda do Clique ganha cor de uma classe de FORMA
(`.pc.oval`, `.pc.ret`...). Reaproveitada na Fábrica sem essa classe, virou
**texto branco solto no ar** — 2,76:1 de contraste, e uma peça que a criança
deveria pegar não parecia pegável.

**Regra:** ao reusar uma classe do molde numa mecânica nova, **renderizar e
olhar** antes de seguir. O portão de contraste pega o pior caso, mas "existe
regra base" (portão 3) não quer dizer "está com a cara certa".

---

## 4. Fase de ARRASTAR: testar os TRÊS caminhos, sempre

O Marcos pegou este defeito **duas vezes** (Legenda e Fábrica).

**A armadilha:** no celular o navegador dispara `mousedown`/`mouseup`/`click`
**de compatibilidade** depois do toque. Sem barrar, o `mouseup` fantasma roda o
`solta()` de novo e **desmarca a peça que a criança acabou de escolher** — o
arrasto com mouse funciona, então passa despercebido, e só o toque quebra.

**Guarda obrigatório:**
```js
var ultimoToque=0;
function ehMouseFantasma(e){
  return e.type.indexOf("mouse")===0 && ((new Date()).getTime()-ultimoToque)<800;
}
// em pega(e) e solta(e):  if(ehMouseFantasma(e)) return;
// e nos handlers de toque: ultimoToque=(new Date()).getTime();
```
**Guardar só o `onclick` não basta** — tem que barrar o mouse inteiro.

**E o outro lado da mesma moeda:** NÃO dar `preventDefault` no `touchstart` —
isso cancela o clique sintético e mata justamente a opção do toque.

**Teste obrigatório antes de publicar** (Playwright, os três separados):
arrastar com mouse · tocar com o dedo (`hasTouch:true`) · clicar. Os três têm
que fechar a fase inteira.

---

## 5. Conteúdo: o que o clone NÃO resolve

- **Produtos repetidos** numa fase de "ache o número no quadro": o quadro guarda
  cada número uma vez só, então a segunda conta com o mesmo total cai numa
  célula já marcada e a criança **fica presa sem ter errado nada**. Conferir que
  todos os resultados são diferentes.
- **Uma função de apoio que ficou para trás** (`normal()`, na Legenda): o
  `node --check` passa, a tela abre, e o app estoura no clique. Portão 1b
  (`_qa/funcoes.py`) existe por causa disso.
- **`xxxBase(cfg)` sem guarda para `cfg` vazio**: os auditores de contraste e
  leiaute abrem TODA tela sem argumento; se a base estoura, eles morrem na
  primeira tela e o portão imprime **nada** — o que não é "passou", é **rodou
  cego**. Sempre `if(!cfg){ <telaPadrão>(); return; }`.
- **O vício do motor**: a mecânica preferida da atividade de origem se espalha.
  Na Fábrica, o teclado numérico tinha tomado 9 das 20 fases. Contar as
  mecânicas antes de entregar; se uma passa de um terço, faltou variedade.

---

## 6. A ordem que funcionou (repetir)

1. **Currículo primeiro**, lendo o `_curriculo/blumenau.txt` no bloco do ano —
   nunca de memória.
2. **Clonar o motor por recorte de arquivo**: cabeça (CSS + engine) + conteúdo
   NOVO + cauda (capa, painel, boletim, treino), e renome mecânico do prefixo.
3. **Arte em lote logo no começo** (é o que demora) — mascote parado primeiro,
   depois as poses por EDIÇÃO.
4. **Voz depois**, pelo input `lote` inline do `gerar-audio.yml` (não precisa
   commitar `_lote_falas.json` só para isso).
5. **Banca inteira**, e só então publicar.

---

## ⚡ NÃO CLONE À MÃO: use o `_padrao/nova-atividade.sh` (ago/2026)

Ordem do Marcos: *"por que está demorando tanto a criação de uma atividade?
Melhor otimizar a linha de produção, claro, com padrão de qualidade altíssimo"*.

A demora **não estava** em escrever as fases — estava em clonar o motor à mão e
depois caçar o que ficou da origem. Só na cartografia foram **cinco** restos de
clone, cada um achado numa rodada diferente da banca (manifesto com o nome de
outra atividade, relatório do professor da outra disciplina, conceitos errados
no `zeraProgresso`, falas de elogio/consolo apontando para MP3 que não existem,
prefixo das imagens). Cada rodada da banca custa ~4 minutos.

```bash
bash _padrao/nova-atividade.sh _pasta pref "T&#237;tulo" "Disciplina &#183; ano" "conc1,conc2,conc3"
```

Ele faz de uma vez o que eu fazia em seis etapas: troca o prefixo em TUDO,
escreve `sw.js` e `manifest.json` próprios, põe os conceitos no `DOM`, no
`zeraProgresso`, no `ROTCRI`, no `CONCN` e no `TREINO`, esvazia `IMGS`/`CENAS`/
`VOZOK` (a lista da origem é resto de clone) e confere o `node --check`.

**E o ritmo do trabalho mudou:**
- `bash _qa/rapido.sh <arquivo>` — **0,4 segundo**, a cada mudança. São os
  portões de texto (sintaxe, função inexistente, resto de clone, classe sem CSS,
  progressão, padrão da casa, narração).
- `bash _qa/auditar.sh <arquivo>` — ~4 minutos, **uma vez, antes de entregar**.
  É quem abre o navegador e vê o que a criança vê.

Antes eu gastava 4 minutos para descobrir um erro de uma linha.

**E pare de chutar coordenada:** `python3 _qa/pontos.py <imagem>` diz onde está
cada mancha de cor, em % da largura e da altura. Alvo chutado cai AO LADO da
coisa, e a criança toca no lugar certo e leva "errado".
