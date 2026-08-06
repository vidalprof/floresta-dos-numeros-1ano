# 📐 O CONTRATO DO ESQUELETO — como uma mecânica se encaixa no motor

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
