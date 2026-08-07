# 📐 O CONTRATO DO ESQUELETO — como uma mecânica se encaixa no motor

> ## ⭐ O MODELO É O **JARDIM DO BROTO** (ordem do Marcos, ago/2026)
>
> Palavras dele: *"só lembrando que o nosso modelo de atividade é a atividade do
> Broto por enquanto"*. **O esqueleto se parece com o Broto**, não com o Circo do
> Teo nem com nenhuma outra. Ele está no ar, as crianças estão gostando, e ele
> mesmo disse: *"achei que a atividade do Broto está perfeita"*. Quando houver
> dúvida sobre como uma tela deve ser, a resposta é **abrir o `_jardim/index.html`
> e olhar**.
>
> **A espinha do Broto, que o esqueleto herda inteira:**
> `telaCapa` → `telaQuem` (o crachá: quem vai jogar) → as fases → `telaFim`
> (boletim animado + medalha) → **relatório do professor escondido**
> (`segredoRelatorio`: abre segurando a medalha 2 segundos, nunca botão à vista).
>
> **E as peças do motor dele, pelos nomes que já existem:**
> - `ajudaJd(n, ops)` — o andaime que cresce: 1º erro dica · 2º consolo + apoio
>   concreto · 3º revela e segue;
> - `reg(conceito, acertouDePrimeira, tentativas)` — a medição invisível que vira
>   o parecer do professor;
> - `fracos()` + `treinarFracos()` — o "Treinar o que faltou", só para quem tem
>   objetivo abaixo de 75%;
> - `resumoAnimado()` — o boletim que conta estrelas e acertos, sem nota e sem a
>   palavra "errou";
> - `crachaEl()` — o crachá com o nome e a figurinha escolhida;
> - `setProg` · `montaBarra(dicaId, dicaTxt)` · `falar`/`falaDaTela` · `VOZOK`
>   (alto-falante em cada resposta) · `salvaEstado` (continuar de onde parou).
>
> **O que MUDA em relação ao Broto:** 32 fases no lugar de 17, e 16 mecânicas
> diferentes (10–12 para pré/1º/2º, onde o gesto ainda é conteúdo). O resto é o
> Broto — inclusive o jeito, o tom e o ritmo.


> Decisão do Marcos (ago/2026): **32 fases** por atividade, **16 mecânicas
> diferentes** (10–12 para pré/1º/2º, onde o gesto ainda é conteúdo). E a meta:
> *"conseguir deixar uma atividade inteira com o esqueleto em minutos e não em
> horas, e claro que fique profissional e fantástica"*.
>
> A ideia que torna isso possível: **a atividade deixa de ser código e passa a ser
> conteúdo.** O motor já tem as 16 mecânicas dentro; eu escrevo o `conteudo.json`
> e o montador gera o HTML, o `falas.json` e a lista de arte.

---

## 1. O QUE O MOTOR FAZ (a mecânica não precisa se preocupar)

Antes de chamar a mecânica, o motor já montou:

| Já pronto | O quê |
|---|---|
| `limpa()` | a tela anterior saiu |
| barra de progresso | na posição certa da fase (calculada da ordem real) |
| selo | o nome da fase |
| `.balao` | **o enunciado**, com o botão de ouvir |
| voz | o enunciado é falado (a dose muda com o ano — §3-A da RECEITA) |
| `cen` | o `<div class="centro">` onde a mecânica desenha |
| barra de dica | com o texto da dica e a voz dela |
| **o andaime** | `ajuda(n)`: 1º erro dica · 2º apoio concreto · 3º revela e segue |
| medição | `reg(conceito, acertouDePrimeira, tentativas)` alimenta o relatório |
| retomar | o ponto é salvo a cada fase (55 min) |

Depois que a mecânica chama `fim()`, o motor cuida da comemoração, do banner e
da fase seguinte.

## 2. O QUE A MECÂNICA TEM QUE FAZER

```js
MEC["nome-da-mecanica"] = function (f, cen, fim) {
  /* f   = o objeto desta fase, vindo do conteudo.json
     cen = onde desenhar (o enunciado já está acima)
     fim = chamar quando a fase terminar                         */
};
```

**Obrigações (é isto que os portões medem):**

1. **Alvo de toque ≥ 44 px** (≥ 40 px dentro de grade).
2. **Nada essencial só na cor** — sempre cor + forma/ícone/texto.
3. **Funciona no mudo**: todo som tem gêmeo visual.
4. **As duas portas**: se tem teclado na tela, aceita `document.onkeydown`;
   se tem arrastar, aceita **também o toque simples**.
5. **`data-qa`** no que o auditor-jogador precisa para conseguir terminar.
6. **Nunca trava**: sempre existe caminho para fechar a fase.
7. **Voz por rodada**: se o enunciado muda dentro da fase, `falaDaTela(id)` na
   mesma hora em que o texto muda.
8. **Erro não pune**: `sErro()` + `ajuda(n)`, nunca X vermelho nem "errou".
9. **Toda opção tocável ganha alto-falante** (`op_<chave>.mp3`) — o motor põe
   sozinho nas classes `.opt,.pc,.lig,.bin`; use essas classes.

## 3. OS AJUDANTES QUE A MECÂNICA PODE USAR

`el(tag,classe,html)` · `imgEl(nome,classe)` · `baguncar(lista)` ·
`falaDaTela(id)` · `mostraDica(txt)` · `ajuda(n)` · `reg(conceito,ok,tent)` ·
`sCerto() sErro() sTap() sPop()` · `festa()` · `faisca(x,y,cor,n)` ·
`centroTela(el)` · `depoisDaFala(id,ms,cb)`

## 4. O FORMATO DE UMA FASE NO `conteudo.json`

```json
{
  "id": "cores",
  "mec": "classificar",
  "selo": "AS DUAS GAVETAS",
  "enunciado": "Onde vai cada um?",
  "dica": "Pense de onde a coisa veio.",
  "conceito": "origem",
  "gavetas": [{"k":"aqui","n":"Já estava aqui"},{"k":"fora","n":"Veio de fora"}],
  "itens": [{"img":"milho","n":"MILHO","alvo":"aqui"}]
}
```

O montador confere: mecânica existe, campos obrigatórios presentes, imagens no
banco ou na lista de arte, e **gera o `falas.json` a partir dos próprios textos**
— é isso que torna impossível a voz dizer coisa diferente da tela.

## 5. A ESCADA (o motor cobra, o portão do pedagogo mede)

- fase 1 é **problema**, nunca explicação;
- o primeiro símbolo só depois do primeiro figural;
- **aquecimento entre 25% e 65%** do caminho;
- a mesma mecânica **nunca em fases vizinhas**, e a segunda vez é **um degrau
  acima** (a primeira com apoio, a segunda sem);
- fecho com gancho.


---

## 6. LIÇÕES DAS PRIMEIRAS PEÇAS (achadas construindo, ago/2026)

Cada uma destas foi descoberta por quem montou a peça, não por mim. Estão aqui
para a próxima não repetir.

- **Distratores demais ou de menos quebram o andaime.** Um quiz com 2 distratores
  faz a criança eliminar tudo antes do 3º erro — o degrau "revelar" vira **código
  morto**. Use 3 distratores, e tenha a rede: se as erradas acabarem antes,
  revele na hora em vez de deixar uma tela com uma opção só.
- **Marcar no `mousedown` quebra o mouse.** O `click` que vem logo atrás cai em
  "já estava marcada" e desmarca — com mouse de verdade, a criança clica e nada
  acontece. A marca é do **clique**; o arrasto só marca quando anda mesmo.
- **O clique FANTASMA do celular desmarca a escolha.** Quem vem do dedo resolve no
  `touchend`, e o clique sintético de trás é engolido por um guarda de tempo.
  ⚠️ Isto **o portão não pega**: só aparece com dedo de verdade.
- **A peça tem que terminar numa `.medal`.** Sem isso o auditor-jogador roda os
  5200 giros (~20 min) sem reconhecer que acabou. Com ela, fecha em ~10.
- **`preventDefault` só no `touchmove`, e só com peça na mão** — e longe do
  `touchstart`, que é a janela que o portão inspeciona.
- **O CSS da peça mora no PRIMEIRO `<style>`**: o `_qa/classes.py` só lê esse.
- **Nada de emoji para a criança.** A estrela da medalha é `content:"\2605"`.
- **Nunca citar `limpa()` num comentário dentro de uma função.** O detector de
  telas lê o **texto cru** do corpo — comentário não é comentário para ele. Uma
  função de acerto virou "tela", foi chamada sozinha sem argumento e derrubou
  três portões com `TypeError`. O comentário vai para FORA do corpo.
- **O `MOLDE.html` sozinho NÃO passa a bancada** (o jogador dá PRESO: não há
  `.medal`). Toda peça precisa da sua `telaFim()` com a medalha.
- **Cuidado com nome de propriedade que colide com nome de classe.** Uma
  propriedade `r.pal` fez o portão reconhecer a peça como marca-texto. Nome de
  dado ≠ nome de classe.
- **O enunciado não pode PROMETER o que a grade não tem.** No caça-palavras, com
  a direção sorteada palavra a palavra, saíam grades **sem nenhuma diagonal** — e
  o enunciado prometia diagonal sempre. A criança varre a diagonal à toa. Cura:
  as direções são um **plano embaralhado** (todas entram) **e** o enunciado é
  montado a partir de onde as palavras realmente ficaram.
- **Sorteio que nunca exercita a armadilha esconde o defeito.** As palavras quase
  nunca se cruzavam, então a armadilha da palavra cruzada (que conferia só `mark`
  e não `ok`) não era testada de verdade. A colocação passou a **preferir**
  posições que cruzam.
- **Tom: "Faltam 0 tentativas" soa como bronca.** No fim da forca virou "Vamos
  olhar a palavra juntos" — que é o que a peça de fato faz.
- **A CORRIDA DE EVENTOS: o toque que chega no meio da comemoração.** Ao acertar,
  a fase agenda a próxima etapa em ~700ms — mas continuava aceitando toque nesse
  intervalo. Um segundo toque rápido fazia a fase avançar com o estado ERRADO (a
  fita cortada em outro número de partes). Toda fase precisa de uma trava
  (`travada = true`) no instante do acerto, não só no fim da animação. **Criança
  toca duas vezes; é o normal dela, não o excepcional.**
- **Ajudante chamado antes do elemento existir.** Uma função de limpeza era
  chamada no começo da fase e lia um elemento criado mais abaixo — `TypeError` na
  primeira carga, derrubando quatro portões de uma vez. Todo ajudante que toca no
  DOM começa com `if(!elemento) return;`.
