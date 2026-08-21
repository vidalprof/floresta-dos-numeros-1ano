# Planilha da prova "Aventura das Direções" (nome, turma, nota)

A prova envia `nome`, `turma`, `nota`, `acertos`, `respostas` e `data` para **dois lugares**
(pra você testar os dois):

1. **Firebase** (já ligado, funciona sozinho) — registro automático; eu consigo puxar pra
   conferir. Se quiser ver numa página, eu te monto um painelzinho.
2. **Planilha Google (Apps Script)** — a "planilha de verdade", igual Formulário. Precisa de
   um setup de **~5 minutos** (uma vez). Passo a passo abaixo.

## Como ligar a Planilha Google (uma vez, ~5 min)

1. Abra o **Google Planilhas** e crie uma planilha nova em branco.
2. Menu **Extensões → Apps Script**.
3. Apague o que estiver lá e **cole o código abaixo**. Salve (💾).
4. Clique em **Implantar → Nova implantação**.
   - Tipo: **App da Web**
   - Executar como: **Eu**
   - Quem pode acessar: **Qualquer pessoa**
   - **Implantar** e **autorize** (é a sua conta).
5. Copie o **link do app da Web** (termina em `/exec`).
6. **Me mande esse link** — eu colo na prova (`URL_PLANILHA`) e republico. Pronto!

A planilha vai ter:
- Aba **"Respostas"** = tudo na ordem que chegou (**preservada para conferência**).
- Aba **"Resumo A-Z"** = nome, turma e nota **em ordem alfabética** (refeita a cada envio).

## Código do Apps Script (cole tudo)

```javascript
function doPost(e){
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var p  = (e && e.parameter) ? e.parameter : {};

  // 1) Aba "Respostas" — append (nunca apaga; preservada p/ conferencia)
  var sh = ss.getSheetByName("Respostas");
  if(!sh){ sh = ss.insertSheet("Respostas"); }
  if(sh.getLastRow() === 0){
    sh.appendRow(["Data e hora","Nome","Turma","Nota","Acertos","Respostas"]);
  }
  sh.appendRow([p.data || new Date(), p.nome || "", p.turma || "",
                p.nota || "", p.acertos || "", p.respostas || ""]);

  // 2) Aba "Resumo A-Z" — nome/turma/nota em ordem alfabetica (refeita a cada envio)
  var rs = ss.getSheetByName("Resumo A-Z");
  if(!rs){ rs = ss.insertSheet("Resumo A-Z"); }
  rs.clear();
  rs.appendRow(["Nome","Turma","Nota"]);
  var n = sh.getLastRow() - 1;
  if(n > 0){
    var dados = sh.getRange(2, 2, n, 3).getValues(); // Nome, Turma, Nota
    dados = dados.filter(function(r){ return (""+r[0]).replace(/\s/g,"") !== ""; });
    dados.sort(function(a,b){ return (""+a[0]).localeCompare(""+b[0], "pt", {sensitivity:"base"}); });
    if(dados.length){ rs.getRange(2, 1, dados.length, 3).setValues(dados); }
  }

  return ContentService.createTextOutput("ok");
}
```

> Observação: a prova **não mostra a nota nem o certo/errado** para o aluno — a nota vai
> silenciosamente só para a planilha/Firebase (pedido da professora).
