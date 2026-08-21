# ⭐ CONTINUAR DE ONDE PAROU — toda atividade nova nasce com isto

**Pedido do Marcos, ago/2026 (regra permanente):**
> *"outra coisa é ter a opção de continuar de onde parou caso o aluno saia sem
> querer, e isso durar o tempo de uma aula, 55 minutos. Tem como? Pode ser
> aplicado a toda atividade nova criada."*

Na escola isso acontece o tempo todo e não é culpa de ninguém: a criança fecha
a aba sem querer, o navegador atualiza, o PC trava, cai a energia, o professor
troca o aluno de máquina. Sem retomada ela volta para a **capa** e perde tudo o
que fez — e uma atividade premium dura quase a aula inteira. Perder 30 minutos
de trabalho de uma criança de 9 anos é o tipo de coisa que faz ela não querer
mais abrir a atividade.

**Por que 55 minutos e não "para sempre":** 55 min é a aula. Dentro da aula, a
criança que voltar é a MESMA criança — retomar é o certo. Passada a aula, quem
senta naquele PC é da **outra turma**: se o convite continuasse ali, ela cairia
no meio da viagem de um colega, com o crachá do colega e o boletim do colega.
Por isso o convite **expira sozinho**. Nada de botão "apagar" para o professor
lembrar de apertar.

---

## O código (copiar, não reescrever)

### 1) O estado — junto de `salva()`/`carrega()`

```js
/* ⭐ CONTINUAR DE ONDE PAROU — DURA UMA AULA (55 min) */
var AULA_MS=55*60*1000, faseAtual="", _retomaFase="", _retomaQuando=0;
function marcaFase(nome){ faseAtual=nome; salva(); }
function salva(){ try{ localStorage.setItem("<slug>_med",JSON.stringify(
  {MED:MED,DOM:DOM,perfil:perfil,fase:faseAtual,quando:(new Date()).getTime()})); }catch(e){} }
function carrega(){ try{ var s=localStorage.getItem("<slug>_med"); if(s){ var d=JSON.parse(s);
  if(d&&d.DOM)DOM=d.DOM; if(d&&d.perfil)perfil=d.perfil;
  if(d&&d.MED&&d.MED.ev)MED=d.MED;
  if(d&&d.fase&&d.quando&&((new Date()).getTime()-d.quando)<AULA_MS){
    _retomaFase=d.fase; _retomaQuando=d.quando; } } }catch(e){} }
function podeRetomar(){
  return !!(_retomaFase && typeof window[_retomaFase]==="function" &&
            ((new Date()).getTime()-_retomaQuando)<AULA_MS);
}
```

⚠️ **A chave do `localStorage` é a da atividade** (`historia_med`, `jardim_med`…).
Duas atividades com a mesma chave se atropelam — todas moram no mesmo domínio
`vidalprof.github.io`. É o mesmo cuidado do `PREFIXO` do `sw.js`.

⚠️ **`carrega()` agora restaura o `MED` também.** Sem isso a criança volta para a
fase certa mas com o relatório do professor zerado — a metade do trabalho dela
some sem ninguém ver.

### 2) O gancho — envelopa cada fase para ela anotar o próprio nome

Vai **depois das fases existirem e ANTES do objeto `TREINO`**:

```js
(function(){
  var extras=[["hAcervo",""],["hMuseu",""],["hAbertura",""]], lista=FASES_MESTRE.concat(extras), i;
  for(i=0;i<lista.length;i++){(function(n){
    var f=window[n];
    if(typeof f!=="function") return;
    window[n]=function(){ marcaFase(n); return f.apply(this,arguments); };
  })(lista[i][0]);}
})();
```

⚠️ **A ORDEM É O PULO DO GATO.** `TREINO={mudanca:hAntesAgora,...}` guarda as
funções **por referência**, no momento em que a linha roda. Se o envelope vier
depois, o "Treinar o que faltou" chama as versões **antigas** e não anota nada —
e o defeito é invisível: tudo funciona, só a retomada mente. As chamadas soltas
(`hCaca()`, `mostraBanner(...,hFim)`) não têm esse problema: o nome resolve na
hora da chamada, então elas já pegam o envelope.

⚠️ Fases fora do `FASES_MESTRE` (acervo, museu, abertura) entram na lista `extras`.

### 3) O convite — na capa, e só quando há para onde voltar

```js
if(podeRetomar()){
  var quem=perfil.nome?(", "+perfil.nome):"";
  c.appendChild(el("div","balao pequeno","Você parou no meio da viagem"+quem+
    ". Quer <b>continuar de onde parou</b>?"));
  var bc=el("button","btn dourado","Continuar de onde parei");bc.style.marginTop="8px";
  bc.onclick=function(){ arma(); sTap();
    var f=window[_retomaFase];
    if(typeof f==="function"){ f(); } else { telaQuem(); } };
  c.appendChild(bc);
}
var b=el("button","btn",podeRetomar()?"Começar do início":"Começar");
b.onclick=function(){arma();sTap(); if(podeRetomar()) zeraProgresso(); telaQuem();};
```

O convite vem **antes** do "Começar": quem fechou a aba sem querer quer isso e
mais nada. E "Começar do início" **zera de verdade** (`zeraProgresso()`), senão a
criança recomeça carregando o domínio antigo e o boletim mente no fim.

---

## Como TESTAR (não vale "parece que funciona")

`localStorage` **não existe em `file://`** — o teste tem que servir o HTML por
`http://`. No container, com Playwright + `page.route` (ver `/tmp/retoma.js` do
dia; o mesmo molde serve). Os **três** casos:

1. abrir uma fase no meio → o `localStorage` guarda o nome dela;
2. **recarregar** → a capa mostra "Continuar de onde parei" e o clique volta
   para a MESMA fase (conferir pelo `.selo` da tela);
3. empurrar o `quando` para **56 minutos atrás** → o convite **some** e a capa
   volta a ser só "Começar".

Medido na estreia (A Máquina do Tempo do Vale, ago/2026): os três passaram.
