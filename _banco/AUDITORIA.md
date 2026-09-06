# 🔎 AUDITORIA DO BANCO DE IMAGENS — 2026-09-06

> Pedido do Marcos: *"Essas imagens do Pollinations ficam ruins, melhore e otimize
> nosso banco de imagens, procure por algum gerador de imagens no nível do Gemini ou
> ChatGPT."* Esta é a parte MEDIDA (o que temos hoje). A parte dos geradores está
> em `_padrao/GERADORES-DE-IMAGEM.md`.

## 1. O que há (medido com `md5`, Pillow, `glob _*/img/*.png`)

| medida | valor |
|---|--:|
| figuras PNG nas pastas das atividades (fora `_banco` e `_cobaia`) | 1 912 |
| peso total | 279 MB |
| com transparência (RGBA) | 1 570 |
| sem transparência (RGB 276 + paleta 66 — cenas, fundos, fotos) | 342 |
| menores que 300 px nos dois lados | 800 |
| grupos de arquivos IDÊNTICOS com nomes diferentes | 697 |

Os 697 grupos são, em quase todos os casos, **cópias legítimas**: o `_banco/img/`
guarda uma cópia de cada figura das atividades (é para isso que ele existe) e as
atividades da mesma família reaproveitam a arte (`hv_rio` = `rio`). Não é
desperdício: é o banco funcionando.

## 2. O que É defeito: duplicata DENTRO da mesma atividade, com nomes diferentes

A criança vê a MESMA figura em dois lugares que prometem coisas diferentes — a
família do "OVO apontando para o mamão" e do kiwi na letra H (achado do testador
humano hoje, já consertado).

| atividade | arquivos iguais | veredito |
|---|---|---|
| `_padaria` | `pd_l_H` = `pd_l_I` | **DEFEITO**: a letra I em pão é a figura do H. (Hoje não está referenciada no `index.html`; se a fita do alfabeto entrar, aparece.) Regerar `pd_l_I`. |
| `_clima` | `nara_aponta` = `nara_acena` | **DEFEITO**: duas poses do mascote com o mesmo desenho — a Nara "aponta" e "acena" iguais. |
| `_clima` | `estrela_grande` = `estrela_no` = `ic_sol` | **suspeito**: um ícone de sol servindo de estrela grande e de estrela "não"? Olhar. |
| `_blu` | `bl_mapa` = `bl_fundo` | provável decisão (o mapa é o fundo). Confirmar. |
| `_museu` | `mv_cr1..6` = `mv_av1..6` | crachá = avatar, cópia intencional. OK. |
| `_trem` | `tr_coru_fala` = `tr_coru_feliz` | **DEFEITO conhecido** (portão 3d): a coruja fala de boca fechada. Depende de edição da pose (Gemini + `base=`). |
| `_central` | `ce_mascote_fala` = `_pisca` = `_feliz` | **DEFEITO**: mascote sem camadas — não fala nem pisca. |
| `_agora` | `rn_pixel_fala` = `_pisca` = `_feliz` | idem (atividade não publicada). |

**Regra que nasce daqui (para o portão `_qa/clone.py` ou `_qa/imagens.js`):** dois
arquivos idênticos com nomes diferentes na MESMA pasta reprovam, exceto quando o
par está numa lista de cópias declaradas (crachá = avatar).

## 3. Por que a arte do Pollinations sai "ruim" — o que a medição mostra

1. **Motor de segunda quando o primeiro falha.** O workflow tenta `flux`, depois
   `turbo`, depois `flux-realism`; `turbo` é visivelmente pior e entrava calado —
   hoje o commit já registra o motor (`.origem.txt`), mas a peça ruim fica no
   banco do mesmo jeito.
2. **Sem semente, sem família.** As peças de uma atividade saíam cada uma de um
   sorteio diferente: luz, escala e traço desirmanados. A semente fixa por cartela
   existe desde ago/2026, mas o banco antigo é anterior a ela.
3. **Recorte automático (`rembg`) em arte de fundo branco**: sobra halo, corta
   sombra, às vezes come parte da peça (o portão `0o6 halo` e o `moldura corta`
   pegam alguns casos, não todos).
4. **Tamanho**: 800 figuras com menos de 300 px — nasceram pequenas ou foram
   apertadas para o peso; em tela grande (projetor) ficam borradas.
5. **O modelo em si**: o `flux` (schnell) do Pollinations é um modelo rápido de
   4 passos. Ele acerta objeto simples e erra em mão, rosto, texto e cena com
   mais de um elemento — exatamente onde o Marcos vê a diferença para o Gemini
   e para o ChatGPT.

## 4. Plano de otimização (o que faço assim que houver gerador aprovado)

1. **Portão novo**: duplicata idêntica com nomes diferentes na mesma pasta →
   reprova (lista de exceções declaradas).
2. **Refazer primeiro o que a criança vê e está errado**: `pd_l_I`,
   `nara_aponta`/`nara_acena`, as camadas do mascote de `_central` e `_trem`.
3. **Refazer em cartela, por atividade, as figuras que o olho (nuvem, quando
   houver cota) marcar** com "cortada", "fundo não transparente", "texto na
   figura" — hoje já anotados no Trem: bola (fundo), elefante e abelha (corte).
4. **Tamanho mínimo 512 px** no lado maior para toda figura nova; as 800
   pequenas ficam na fila, por atividade, na ordem em que o Marcos usa em sala.
5. **Banco com nota**: o `_banco/index.json` ganha `motor` (quem desenhou),
   `semente` e `nota_olho` (o veredito do testador), para escolher a melhor
   versão quando há duas e para saber o que ainda precisa ser refeito.
