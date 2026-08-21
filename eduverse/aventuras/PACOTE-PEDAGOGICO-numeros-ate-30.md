# 📚 PACOTE PEDAGÓGICO — "A Ilha das Trinta Moedas" (Números até 30)

> **Passada do PEDAGOGO** (pedido do Marcos: *"o pedagogo verificou a BNCC e tudo?"*). Antes eu
> tinha **alinhado sem documentar** — falha de rigor. Aqui está a verificação formal, o que o
> professor leva à **coordenação**. **Currículo invisível:** a criança NUNCA vê o objetivo; ela
> vive o problema do mundo (o mar espalhou o tesouro) e só no fim descobre que estava "contando".
>
> **Fonte:** BNCC **nacional** de Matemática, 1º ano (Blumenau **adere** à BNCC). A redação exata
> do currículo de Blumenau pode ser puxada com `.github/workflows/baixar-curriculo.yml` se a
> coordenação exigir a citação municipal literal.

- **Componente:** Matemática · **Ano:** 1º (anos iniciais) · **Tema/unidade:** Números — contagem e quantidade até 30
- **Aula/aventura:** ~55 min (5 intro / 35 missão / 10 desafio / 5 síntese)

## 🎯 Objetivos de Aprendizagem (BNCC — texto oficial)
| Código | Objetivo (BNCC) | Onde acontece na aventura |
|---|---|---|
| **EF01MA01** | Utilizar números naturais como **indicador de quantidade** em situações cotidianas. | Toda parada: o número diz "quantos cocos/gaivotas/moedas". |
| **EF01MA02** | **Contar** de maneira exata, usando estratégias como o **pareamento** (um a um). | A mecânica central: tocar **cada** objeto **uma vez**, sem pular nem repetir. |
| **EF01MA04** | Contar a quantidade de objetos de coleções e **apresentar o resultado por registros verbais e simbólicos**. | A criança **ouve** o número (voz do Antonio) **e vê o numeral** grande na tela — verbal **+** simbólico, exatamente o objetivo. |

### ➕ Na versão aprofundada (Game Designer — prever→contar→conferir; comparar)
| Código | Objetivo (BNCC) | Como entra |
|---|---|---|
| **EF01MA03** | **Estimar e comparar** quantidades ("tem mais", "tem menos", "a mesma quantidade"). | No fim de cada parada: *"o barco tinha 5 furos e caíram 6 cocos — **sobrou** 1!"* (comparar coleção contada × necessidade). |
| **EF01MA05** | **Comparar números naturais** de até duas ordens em situações cotidianas. | A progressão 6→12→18→24→30 e o "faltou/sobrou" fazem a criança comparar quantidades ao longo da aventura. |

## 🗺️ Progressão (as 5 paradas)
| Parada | Cenário (problema do mundo) | Objeto | Quantidade |
|---|---|---|---|
| 1 | Praia — o barco furou | cocos | **6** |
| 2 | Enseada — o farol apagado | gaivotas | **12** |
| 3 | Gruta — a ponte não aparece no escuro | tochas | **18** |
| 4 | Convés — o capitão não solta a chave | barris | **24** |
| 5 | Câmara — o baú só fecha com o tesouro | moedas | **30** |

*Progressão didática:* começa em quantidade pequena e concreta (6), cresce até 30; a repetição da
**mesma ação de contar** em contextos diferentes consolida o conceito (transferência).

## 🧭 Princípio pedagógico (por que NÃO é prova disfarçada)
1. **Problema do mundo primeiro** — a criança conta porque o **mundo precisa** (o barco vaza), não porque "responda X".
2. **O Byte PERGUNTA** ("quantos serão?"), nunca corrige.
3. **Erro = consequência gentil** — se ela "termina" sem contar tudo, o Byte aponta ("e aquele ali no canto?"); os não-contados brilham. Nunca "errou".
4. **Conceito nomeado por ÚLTIMO** — a palavra "**contar**" só aparece na reflexão final.
5. **Multissensorial** — toca (motor), ouve (verbal), vê (simbólico) — os três registros do número juntos.

## 📊 Avaliação diagnóstica (o que o sistema registra → vira nota)
Salvo no **Firebase** (`/turmas/<turma>/alunos/<aluno>`), por parada:
- **acertos** (contou a coleção completa?), **tentativas**, **tempo**.
- **Evidência por objetivo:** completou 1–2 paradas → EF01MA01/02 em desenvolvimento; completou
  as 5 (até 30) com registro verbal+simbólico → EF01MA04 demonstrado; usou "faltou/sobrou" →
  EF01MA03/05.
- **Nota por aproveitamento:** % de paradas concluídas + autonomia (tentativas/tempo). Converte
  numa rubrica (Ainda não / Em desenvolvimento / Demonstrou) → o professor arbitra a nota.
- **Documentos automáticos:** preenche o **Planejamento** e o **Plano de Aula** nos moldes do Marcos
  (ver `eduverse/curriculo/modelos-documentos.md`) — o professor imprime e entrega.

## 🔎 Ressalva honesta (rigor)
- Alinhamento contra **BNCC nacional**; a **redação municipal de Blumenau** pode ser anexada
  (workflow `baixar-curriculo.yml`) se a coordenação pedir a citação literal.
- A dinâmica atual ("tocar e contar") cobre **EF01MA01/02/04** com força. **EF01MA03/05
  (comparar) entram na versão aprofundada** (o "faltou/sobrou") — recomendado pelo Game Designer
  para a atividade ficar **plenamente diferenciada** (contar como ferramenta de resolver, não só repetir).
