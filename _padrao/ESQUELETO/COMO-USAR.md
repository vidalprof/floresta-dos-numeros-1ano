# ⚡ COMO MONTAR UMA ATIVIDADE COM O ESQUELETO

> Meta do Marcos (ago/2026): *"uma atividade inteira em minutos e não em horas"*,
> e *"pronta no máximo em 1 hora e meia"*.

O que levava horas era **reescrever o motor** a cada atividade. Isso acabou. O
que sobra é o que só se faz uma vez: **o conteúdo**.

---

## Os 7 passos

### 0. O ESBOÇO (3 segundos) — comece SEMPRE por aqui

```bash
python3 _padrao/ESQUELETO/esboco.py <pasta> \
    --ano "3º ano" --prefixo abc --titulo "..." --mascote nino
```

Sai um `conteudo.json` com **as 32 fases, 16 mecânicas e todas as gavetas de cada
uma já no formato certo**, com os textos marcados `«assim»`. Só se troca o que
está entre `«»`.

**Por que isto existe** (cobrança do Marcos: *"o processo precisa ser mais ágil e
SEM ERROS"*, e a pergunta certeira: *"por que sai erro se a fábrica entrega tudo
pronto?"*): a fábrica de peças **não** estava errando — as 74 passam a bancada. O
erro nascia na **junta entre o conteúdo e a peça**, sempre do mesmo jeito:

| o que eu fazia | o que a criança via |
|---|---|
| campo com o nome trocado | a fase anunciava "0 diferenças" e se concluía sozinha |
| gaveta meia-cheia | as chaves não casavam: nenhuma ficha podia ser posta |
| palavra de 17 letras numa grade de 8 | 857 erros de JS e a fase sem saída |

Os portões pegam os três — **mas portão avisa depois que se errou**. O esboço faz
melhor: não deixa errar. E preserva as **chaves de ligação** (`k` ↔ `alvo`), que
são justamente o que não se pode trocar.

### 1. O conteúdo (é aqui que vai o tempo — ~30 min)

Preencher o que está entre `«»` no `<pasta>/conteudo.json` do esboço. Antes disso, o de sempre: BNCC do ano,
`_curriculo/blumenau.txt`, `EDUVERSE-FILOSOFIA.md` (o problema primeiro, o
conceito por último) e o `CATALOGO-DINAMICAS-INTERATIVAS.md` para escolher os
gestos **por encaixe**, não por lista.

```jsonc
{
  "titulo": "...", "sub": "Ciências · 3º ano · ...",
  "ano": "3º ano",
  "prefixo": "abc",              // ⚠️ NUNCA o de outra atividade
  "mascote": "nome",             // as figuras viram abc_nome_feliz/fala/pisca
  "mascoteNome": "Nome",
  "crachas": 6,
  "fundo": "abc_fundo.jpg",
  "abertura": "O que o mascote diz na primeira tela",
  "fim": "O que ele diz na medalha",
  "conceitos": { "chave": "Nome em linguagem de criança (vai no boletim)" },
  "fases": [
    { "id": "f01", "mec": "escolher", "selo": "ESCOLHA",
      "enunciado": "...", "dica": "...", "conceito": "chave",
      "dados": [ /* o formato desta mecânica — ver pecas.json */ ] }
  ]
}
```

**O formato de `dados` de cada uma das 74 mecânicas está em `pecas.json`**, com
o exemplo da própria peça ao lado. Fase **sem** `dados` roda com o exemplo da
peça — serve para ver a mecânica de pé, **nunca** para entregar.

O que o montador **cobra e reprova**: 32 fases · 16 mecânicas diferentes (10 até
o 2º ano) · nenhum gesto acima de 40% · nada de gesto repetido colado · o
AQUECIMENTO entre 25% e 65% do caminho.

### 2. Montar (~2 segundos)

```bash
python3 _padrao/ESQUELETO/montar.py <pasta>
```

Saem três arquivos: `index.html` (a atividade), `falas.json` (o que gravar) e
`arte.json` (o que desenhar, já dizendo **o que o banco resolve**).

### 2b. Colher as falas que só existem jogando (~3 min) — **não é opcional**

```bash
python3 _padrao/ESQUELETO/colher.py <pasta>   # joga a atividade e anota
python3 _padrao/ESQUELETO/montar.py  <pasta>  # e monta de novo
```

O `falas.json` sai do `conteudo.json`, e isso resolve tudo o que está **escrito**.
Mas a peça monta frases **em tempo de jogo** — *"Achou as 4 palavras da horta!"*
— e o montador não tem como adivinhar o número, que vem do próprio jogo. A saída
não é adivinhar: é **jogar e anotar**. O auditor-jogador já atravessa a atividade
inteira; o `colher.py` transforma a colheita dele em `falas.json`.

Sem este passo, as telas de fecho de rodada ficam **mudas** e a criança que ainda
não lê perde justamente o retorno do acerto. O portão `0f` cobra isso.

*Medido na atividade de teste: 61 falas que só apareceram jogando.*

### 3. A arte (~15 min de espera)

`arte.json` diz o que falta. **Antes de gerar, o portão do custo:**

```bash
python3 _qa/cartela.py <pasta>/_gerar_imagens.json     # reprova peça a peça
python3 _padrao/cartela.py plano                       # agrupa em folha
```

Depois `gerar-imagens.yml`. **Fora da cartela** ficam só as camadas do mascote
(`_fala`/`_pisca` são **EDIÇÃO** da pose parada — geradas do zero, ele treme) e
as cenas largas (Pollinations, de graça).

> ✅ **O Gemini TEM CRÉDITO** — medido em 2026-08-07: uma geração de teste voltou
> com imagem 1024×1024. O aviso de "sem crédito" que estava aqui era de 05/08 e
> ficou velho.
>
> ⚠️ **A lição, que vale para qualquer serviço de fora:** aviso de saldo tem
> **data de validade**. Eu repeti o de 05/08 ao Marcos como se fosse de hoje, e
> ele é que estranhou ("coloquei 60 reais, como pode?"). Conferir custa **um
> minuto e centavos**: `gerar-imagens.yml` com `modelo=gemini` e um prompt
> qualquer. Medir antes de repetir.

### 4. A voz (~1 min)

`entregar.yml` com `alvos=<pasta>:<repo>`. Ele lê o `falas.json`, grava só o que
mudou (carimbo sha1) e publica. **8 falas ao mesmo tempo.**

### 5. A banca (~10 min)

```bash
bash _qa/auditar.sh <pasta>/index.html
```

**O portão que decide é o que JOGA** (`_qa/jogador.js`): atividade montada não
se entrega sem ele ter chegado à medalha. Portão que imprime NADA não é
"passou": é "rodou cego" — rodar na mão, sem `2>/dev/null`, e ler o erro.

### 6. Publicar

`fabrica.yml` (repo novo) ou `atualizar.yml` (repo que já existe). Confirmar o
build (`deploy-pages.yml` → `built`).

### 7. Mandar o link ao Marcos

E parar por aí: **atividade nova não entra no hub** até ele pedir com todas as
letras.

---

## Se alguma coisa der errado

| sintoma | o que é |
|---|---|
| `montar.py` reprova o conteúdo | é ele fazendo o trabalho dele. Ler a linha: diz a fase e o quê. |
| a fase abre e diz "(mecanica 'x' nao registrada)" | a peça não existe em `_padrao/pecas/`. Escrever a peça primeiro, e só ela. |
| o jogador fica PRESO numa fase | rodar `node _qa/jogador.js <arquivo>` sozinho e ler os "ERROS JS". |
| a atividade abre e a tela fica branca | quase sempre é ordem de boot. `node --check` no JS extraído e olhar o console. |

## Quando o motor ou as peças mudarem

```bash
python3 _padrao/ESQUELETO/extrair_motor.py   # o Broto mudou
python3 _padrao/ESQUELETO/integrar.py --escrever   # uma peça nova/corrigida
```

Os dois **se recusam a escrever** se acharem defeito: o extrator, se sobrar
marca do Broto no código; o integrador, se as peças chamarem nome que o motor
não tem — ou que ele tem com **outro tipo** (foi o caso do `ac`, e não dá erro
nenhum até a criança tocar).
