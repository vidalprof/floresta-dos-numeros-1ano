# 🎙️ BANCO DE VOZES — 1.341 falas já gravadas (achado em ago/2026)

Esta pasta **não é lixo**: é um banco de narrações que foi gerado numa sessão
antiga e ficou esquecido, sem ninguém usar. O Marcos perguntou se dava para
existir *"uma fábrica de narrações... reaproveitar, para não ter sempre que gravar
tudo"* — e a resposta é que **ela já existia aqui dentro**.

**Como o nome funciona:** cada arquivo se chama pela **assinatura do texto falado**
(a mesma conta do `chaveVoz` das atividades: djb2 em base 36). Ou seja, a mesma
frase sempre dá o mesmo nome — é o que permite perguntar "esta fala já existe?"
sem gravar de novo.

**Para que serve, na prática:**
- as ~40 frases que se repetem em toda atividade ("Muito bem!", "Quase!",
  "Ouvir de novo", "Vamos lá") saem **idênticas** em todas, em vez de cada
  atividade gravar a sua com entonação um pouco diferente;
- os alto-falantes de palavras comuns (RAIZ, FLOR, MAPA, CENOURA) também.

⚠️ **O ganho aqui NÃO é tempo.** Gravar as 200 falas de uma atividade custa hoje
~30 segundos e zero centavo (`entregar.yml`, 8 ao mesmo tempo). O ganho é
**consistência**: a voz da casa igual em todo lugar.

**Nunca apagar.** Regravar tudo daria trabalho e o resultado não seria idêntico.
