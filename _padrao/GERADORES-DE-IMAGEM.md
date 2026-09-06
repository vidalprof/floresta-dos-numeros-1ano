# 🎨 GERADORES DE IMAGEM — qual usar, quanto custa, como acionar (set/2026)

> Pedido do Marcos (2026-09-06): *"Essas imagens do Pollinations ficam ruins,
> melhore e otimize nosso banco de imagens, procure por algum gerador de imagens
> no nível do Gemini ou ChatGPT."*
>
> Este documento é a resposta MEDIDA. A parte do banco (o que temos, o que está
> errado) está em `_banco/AUDITORIA.md`. Fontes: `pesquisar.yml` (a internet do
> GitHub) em `_pesquisa/web/precos-openai-gemini-imagem.md`,
> `recraft-ideogram-stability-api-precos.md` e `geradores-imagem-flux-gratis-api.md`.
> Preço de serviço externo tem **data** e se **remede** antes de decidir de novo.

## 1. A resposta curta

**Não existe gerador GRÁTIS no nível do Gemini/ChatGPT.** O que é grátis
(Pollinations) roda o FLUX *schnell*, um modelo rápido de 4 passos: acerta objeto
simples e erra mão, rosto, cena com vários elementos e, sobretudo, não sabe
EDITAR uma imagem (as três camadas do mascote). Os geradores do nível que ele
pediu são pagos, mas baratos: **entre US$ 0,01 e US$ 0,07 por figura** — uma
atividade inteira (40 figuras) sai por **US$ 0,5 a US$ 2,7**, menos que um lanche.

O que já está pronto para usar, sem tocar em código:

| caminho | o que precisa | qualidade | por figura (1024²) | 40 figuras |
|---|---|---|---|---|
| `modelo=openai` (gpt-image-1) **← implementado hoje** | secret `OPENAI_API_KEY` com crédito pré-pago | nível ChatGPT; **fundo transparente nativo**; edita base | low ~US$0,011 · **medium ~US$0,042** · high ~US$0,167 | US$0,44 · **US$1,68** · US$6,7 |
| `modelo=openai-mini` (gpt-image-1-mini) | idem | um degrau abaixo, ótimo p/ peça simples | low ~US$0,005 · medium ~US$0,011 · high ~US$0,036 | US$0,20 · US$0,44 · US$1,44 |
| `modelo=gemini` (já existia) | reativar o faturamento da `GEMINI_API_KEY` (está em **429 sem cota desde 2026-08-12**) | nível Gemini; edita base | 2.5 Flash Image **US$0,039** · 3.1 Flash-Lite Image **US$0,034** (promo 0,017) · 3.1 Flash Image US$0,067 · Pro Image US$0,134 | US$1,56 · US$1,34 · US$2,68 · US$5,4 |
| `modelo=pollinations` (padrão) | nada | FLUX schnell; sem edição; recorte pelo `rembg` | **R$ 0,00** | R$ 0,00 |

Os preços do OpenAI vêm da tabela pública que eu conheço (a página de preços
deles é montada por JavaScript e o robô do `pesquisar.yml` não conseguiu ler —
**conferir no painel dele antes de comprar crédito**). Os do Google saíram da
página oficial em 2026-09-06 (tokens por imagem: 1290 no 2.5 Flash Image, 1120
nos 3.1). Câmbio: multiplicar por ~R$5–6.

## 2. O que eu recomendo (e por quê)

1. **OpenAI gpt-image-1 como gerador "nível ChatGPT" da casa.** Três razões
   medidas:
   - **Fundo transparente NATIVO** (`background: transparent`). Metade dos
     defeitos que o Marcos vê na arte grátis não é o desenho, é o **recorte**:
     halo branco, sombra comida, caco solto (`so_a_figura`), figura cortada. Com
     a peça já nascendo recortada, o `rembg` sai do caminho.
   - **Edita imagem base** (`/v1/images/edits`): as três camadas do mascote
     (parada → falando → piscando) saem da MESMA pose. É o que destrava o portão
     3d do Trem (`tr_coru_fala` é cópia da pose parada) e os mascotes sem camada
     de `_central` e `_agora` — hoje bloqueados porque o Gemini está sem cota.
   - **Pré-pago**: o crédito é comprado antes (mínimo US$5), não há surpresa na
     fatura. Com US$5 saem ~120 figuras `medium` ou ~450 `low`.
2. **Qualidade `low` para provar, `medium` para valer.** A prova de uma cartela
   (3 sementes, o Marcos escolhe a família) custa centavos em `low`; a versão
   final vai em `medium`. `high` só para capa/cena larga que vai ao projetor.
3. **Pollinations continua** para o que ele faz bem e de graça: cena/fundo
   largo (não precisa de recorte), peça simples de objeto único, e como
   **reserva automática** quando o pago falha (o workflow cai para ele sozinho e
   REGISTRA no `.origem.txt` que não foi o pago).
4. **Gemini fica como segunda opção paga**, já integrada: se o Marcos preferir
   pagar no Google (mesma conta do resto), basta reativar o faturamento da chave
   que já existe. O Nano Banana 2 Lite (US$0,034) é o mais barato dos pagos
   "de verdade".

## 3. O que NÃO recomendo agora (apurado, não achismo)

- **Recraft V3 / Ideogram 3**: fortes em vetor e em TEXTO dentro da imagem —
  não é o nosso caso (a casa proíbe letra na figura). Recraft vende "API Units"
  pré-pagos, não reembolsáveis; sem preço por imagem legível na página.
- **Midjourney**: API em liberação limitada e licença mais restrita
  (comparativo abr/2026).
- **fal.ai FLUX schnell a US$0,003/MP**: é o MESMO modelo do Pollinations, só
  pago e mais estável. Não sobe o nível; só vale se o Pollinations cair de vez.
  O **FLUX Kontext [dev]** (edição de imagem, ~US$0,025) seria a alternativa
  aberta para editar mascote — segunda escolha, sem fundo transparente nativo.
- **Cloudflare Workers AI / Together "free"**: as páginas de preço não abriram
  pelo robô (bloqueadas). **Não apurado** — não prometer.
- **Pollinations `turbo`**: visivelmente pior que o `flux`. O workflow agora dá
  DUAS chances ao `flux` antes de cair no `turbo`, e quando cai grita
  `::warning::` — peça de turbo é candidata a refazer, não é "pronta".

## 4. Como acionar (passo a passo)

**Uma vez só, o Marcos:** cria a chave em platform.openai.com → Billing → compra
crédito (US$5 basta para começar) → API keys → cria a chave → cola em
**GitHub → Settings → Secrets and variables → Actions → New secret →
`OPENAI_API_KEY`**. ⚠️ **A chave NUNCA passa pelo chat** — eu não peço, não
aceito e não preciso ver; o workflow lê `secrets.OPENAI_API_KEY` sozinho.
Sem o secret, `modelo=openai` avisa e cai para o Pollinations (a produção não para).

**Uma imagem:**
```
gerar-imagens.yml  prompt="..."  nome=tr_coru_fala  modelo=openai  qualidade=medium
                   base=_trem/img/tr_coru_feliz.png     ← edição (camada do mascote)
                   fundo=auto  (peça = transparente; nome com fundo/cena = opaco)
```

**Cartela / lote** (`lote=<arquivo.json>`): o input `modelo=openai` vale para
todas as peças; ou peça a peça, com `"modelo": "openai"` no item (as outras
seguem no Pollinations). A peça do OpenAI já vem transparente e **não passa pelo
rembg** (só apara a borda); a cena (`grupo: cena` ou nome com `fundo`) sai opaca.
Portão do custo continua: `python3 _qa/cartela.py <lote.json>` antes de acionar.

**Ler o resultado sem gastar contexto:** `git fetch` + `_status/imagens-<lote>.json`
(agora traz `motores` e `custo_usd`) e o `.origem.txt` ao lado de cada PNG.

## 5. O plano do banco (o que faço com o gerador aprovado)

Já feito hoje: **portão 1c2 `_qa/duplicatas.py`** (duas imagens idênticas com
nomes diferentes que a criança vê → reprova; cópia declarada em
`<pasta>/_copias_ok.json` com a razão). Reprova hoje: `_clima` (o sol servindo de
estrela), `_trem`, `_central`, `_agora` (mascote sem camadas). `_blu` declarou
`bl_mapa = bl_fundo` (a confirmar com o Marcos).

Fila de refazer, na ordem em que chega à criança:
1. **Camadas de mascote** (`tr_coru_fala`, `ce_mascote_fala/_pisca`,
   `rn_pixel_fala/_pisca`, a pose `nara_acena` que hoje é a `nara_aponta`) —
   precisam de EDIÇÃO da base: só com OpenAI ou Gemini pago. 2 a 3 chamadas por
   mascote (~US$0,10 cada mascote em `medium`).
2. **`estrela_grande` do Clima** (é um sol) e **`pd_l_I` da Padaria** (é o H) —
   objeto neutro, sai pelo Pollinations em `_novo/_lote_banco_refazer.json`
   (acionado hoje) para o Marcos aprovar antes de entrar na atividade.
3. **Figuras que o testador humano (olho) marcou**: Trem `bola` (fundo não
   transparente), `elefante` e `abelha` (cortados) — refazer em `medium` com fundo
   transparente nativo, que resolve as duas famílias de defeito de uma vez.
4. **As 800 figuras abaixo de 300 px**: por atividade, na ordem em que o Marcos
   usa em sala; piso novo de 512 px já está no workflow (sobe para 1024 sozinho).
5. **Banco com nota**: `_banco/montar.py` passa a guardar `motor`/`semente`
   (lidos do `.origem.txt`) para escolher a melhor versão quando há duas.
