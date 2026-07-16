# ♻️ EducaVerso — Plano de SUSTENTABILIDADE (produção + dados)

> Pedido do Marcos (jul/2026): *"tudo tem que ser sustentável, a produção e os dados, visto que
> isso cresce — tentar ser gratuito ou gastar o mínimo possível, pensando lá na frente."*
> Regra-mãe: **gerar UMA vez e reusar sempre; guardar o MÍNIMO; tudo em camada grátis; backend
> PLUGÁVEL (trocável sem mexer no jogo).**

---

## 1. PRODUÇÃO (arte, voz, mundos) — já é ~grátis, e fica MAIS barato com o tempo

| Recurso | Escolha sustentável | Custo |
|---|---|---|
| Arte (tiles/cenários) | **Pollinations (flux)** — padrão | **grátis** |
| Arte (fantasia do Byte, edição da âncora) | **Gemini** só onde precisa editar a âncora, com **prompt econômico** (especialista de prompt) | pago, raro, **cacheado** |
| Voz (maioria das falas) | **Web Speech (speechSynthesis)** no navegador | **grátis** |
| Voz (falas fixas de qualidade) | **edge-tts** (workflow) | **grátis** |
| Geração/compute | **GitHub Actions em repo PÚBLICO** | **grátis** |
| Hospedagem dos jogos | **GitHub Pages** (estático, HTML autossuficiente) | **grátis** |

**Os 3 multiplicadores que seguram o custo lá na frente:**
1. **Biblioteca LEGO (reuso):** uma peça gerada 1x serve N mundos. Mundo novo reaproveita ~90% dos
   assets; só o "tema" (paleta/mascote) é novo. **Quanto mais a biblioteca cresce, MENOS se gera.**
2. **Cache por hash (idempotência):** mesmo prompt = não regera. **Nunca se paga 2x pela mesma imagem.**
   Vale ouro pro Gemini (o único pago).
3. **Content-addressed + `.git` limpo** (`republicar-limpo`): assets nomeados por hash, histórico
   enxuto → o repositório não incha e o Pages não engasga, com qualquer volume.

➡️ **Conclusão:** produção é essencialmente **grátis**, e o custo por mundo **cai** com o tempo. O único
gasto é Gemini na fantasia do Byte — raro, cacheado, com prompt mínimo/preciso.

---

## 2. DADOS (progresso + avaliação por aluno) — o que cresce; precisa de disciplina

O que cresce é o **save por aluno** (progresso + avaliação descritiva) ao longo do ano, para muitas
turmas e muitos alunos. Estratégia para ficar grátis/barato **por muito tempo**:

### 2.1 Guardar o MÍNIMO (a regra que segura tudo)
- Por aluno, **um registro compacto (~2 KB)**: habilidades demonstradas + contadores (acertou de
  primeira / errou-e-consertou / tentativas), **não** um log de cada clique.
- **Avaliação descritiva é CALCULADA na leitura** (agrega mês/semestre/ano a partir do registro
  compacto) — não se guarda relatório redundante.
- **LGPD = menos dado:** só **primeiro nome + código de turma** (já é a decisão do projeto). Menos
  dado = menos risco, menos peso, mais barato.
- **Rollup anual:** no fim do ano, "congela" um JSON pequeno do relatório e **zera o corrente** → o
  banco **não cresce sem parar**.

### 2.2 Onde guardar (começar grátis, poder trocar)
- **Começar no Firebase (free tier "Spark")** — é o caminho mais robusto e já parcialmente previsto
  (`/mundos/<turma>/<aluno>`, ~2 KB). Com dado mínimo, o free tier aguenta **muitíssimo** crescimento:
  o gargalo não é o armazenamento (dado é minúsculo) e sim as **cotas diárias** de leitura/escrita —
  e um registro compacto por aluno cabe folgado.
- **Se um dia estourar** (muitas escolas): (a) o custo pago é de **centavos** (dado é minúsculo), ou
  (b) migra pra alternativa grátis — **Cloudflare (KV/D1)**, **Supabase**, ou até **Google Sheets +
  Apps Script** (o professor já vive no Google; exportável). 
- **A chave da sustentabilidade "lá na frente":** o jogo NÃO fala direto com o backend. Fala com uma
  **interface simples `salvar(aluno,dados)` / `carregar(aluno)`**. Assim dá pra **trocar o backend**
  (Firebase → Cloudflare → Sheets) **sem tocar no jogo**. Nunca ficamos presos a um serviço.

### 2.3 Barato e resiliente
- **localStorage como cache** (grátis, offline) + **sync** para o backend quando houver rede → menos
  escritas no servidor (economiza cota) e funciona mesmo com internet ruim de escola.
- **Escrita só quando muda** (no fim de uma missão), não a cada frame.

---

## 3. Regras de ouro (checar em toda decisão nova)
1. **Gerar 1x, reusar sempre** (biblioteca + cache por hash).
2. **Guardar o mínimo** (registro compacto + rollup anual + só 1º nome).
3. **Só camadas grátis** (Pollinations, Web Speech, edge-tts, Actions público, Pages, Firebase free).
4. **Backend plugável** (interface `salvar/carregar`) — trocável sem mexer no jogo.
5. **Pago só onde é insubstituível** (Gemini na fantasia do Byte), sempre cacheado e com prompt mínimo.
6. **Medir antes de assustar:** dado por aluno é ~2 KB; mesmo milhares de alunos = poucos MB. O "custo
   que cresce" é pequeno e previsível — a disciplina acima o mantém em zero/centavos por muito tempo.
