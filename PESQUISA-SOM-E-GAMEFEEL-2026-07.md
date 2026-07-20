# Pesquisa — SOM que ensina + GAME FEEL barato (2026-07)

> Parte da rodada "reúna o pessoal". Especialista de Som & UX. Complementa
> `PESQUISA-APPS-AMAR-E-NEUROCIENCIA` e `PESQUISA-FORMATOS`. Alvo: 1 HTML, PC fraco,
> crianças 6-12, muito interativo e SONORO, som que ENSINA (não enfeita).
> Força: [FORTE] meta/RCT · [MODERADA] · [CONSENSO] prática profissional · [OPINIÃO] design fundamentado.
> Advertência honesta: a evidência FORTE é sobre os MECANISMOS (música-memória, dupla codificação,
> dopamina-surpresa, feedback imediato) e CONSENSO sobre as TÉCNICAS (juice, manipulação direta);
> o desenho específico "site educativo com Web Audio em PC de escola" não tem RCT — extrapolações marcadas.

## A — SOM COMO APRENDIZADO
- **Música/ritmo ajudam memória e atenção em crianças [FORTE].** Sequências CANTADAS com pulso
  regular > faladas. Aplicação: decorar ordem (números, passos, tabuada) = melodia curta com pulso.
- **Modalidade de Mayer [FORTE, d≈1,02]:** animação + narração FALADA > animação + texto (o canal
  visual não sobrecarrega). Aplicação: o mascote FALA (MP3) enquanto o mundo se mexe; o texto é
  legenda curta, não o canal principal. (Também atende acessibilidade.)
- **Sonificação didática [CONSENSO técnico + OPINIÃO no design infantil]:** pitch = quantidade
  (maior→mais agudo); **fração/proporção = intervalo musical** (oitava 2:1, quinta 3:2, tríade maior
  4:5:6 — dá pra OUVIR a fração); ritmo/pulso = contagem/subitização. Honesto: blocos físicos FORTES,
  "reta que canta" ensina melhor = não provado. Usar sem prometer efeito.
- **Feedback MUSICAL [FORTE no mecanismo]:** consonância ativa recompensa (accumbens/dopamina);
  dissonância ativa desconforto; a RESOLUÇÃO (tensão→consonância) dá alívio. Acerto = tríade maior
  que "assenta"; erro = dissonância curtíssima e suave (~140ms), nunca estridente/punitiva.
- **Voz humana/neural (MP3 edge-tts) > voz do navegador [FORTE, ressalva MODERADA]:** voice
  principle d≈0,78; TTS neural moderno estreitou a diferença, mas o `speechSynthesis` do navegador é
  o pior E inconsistente entre PCs da escola. MP3 pré-gerado = determinístico, com legenda. Confirma
  a regra do projeto (voz do Antônio, nunca navegador).
- **Som como recompensa VARIÁVEL (dopamina da surpresa) [FORTE mec./MODERADA aplic.]:** o som de
  acerto NÃO deve ser idêntico toda vez; varie pitch/timbre e, às vezes (não sempre), solte um brilho
  extra. Ressalva overjustification: recompensa ligada à COMPETÊNCIA (celebra o que ela entendeu),
  nunca o único motivo de continuar.
- **LADO ESCURO do som [FORTE]:** (1) *Irrelevant Sound Effect* — som de fundo que MUDA de estado
  atrapalha a memória de sequência (às vezes pior em crianças) → **música de fundo durante o pensar
  PREJUDICA**. (2) *Seductive details* — som "interessante mas inútil" impõe carga. **Regra de ouro:
  silêncio (ou pulso mínimo) durante o raciocínio; som rico NO evento** (ação/acerto/erro/transição).

## B — GAME FEEL BARATO (só transform/opacity)
- **Swink [CONSENSO]:** resposta em tempo real (<100ms), espaço simulado, polimento. **Juice é
  camada POR CIMA de algo que já funciona — nunca o que faz funcionar** (Vlambeer). Ordem: mecânica +
  aprendizagem primeiro; suco depois.
- **Vlambeer/Juice it or lose it:** empilhar camadas — som → animação → partículas → screenshake.
- **Disney [CONSENSO]:** squash & stretch (peso/elasticidade, tatilidade) + antecipação (movimento
  preparatório que deixa prever o resultado).
- **Manipulação direta / Shneiderman [FORTE/CONSENSO]:** objeto contínuo; ação física (arrastar);
  operações incrementais e reversíveis com efeito imediato. Arraste gruda no dedo (sem delay), inércia
  leve, squash ao pegar e ao assentar; alvo certo = acorde+partícula; errado = volta com mola+dissonância.
- **Haptics (Vibration API) [FORTE técnico, limites]:** `navigator.vibrate(50-200ms)`; **bônus
  Android** (iOS nunca teve; Firefox removeu v129+). Nunca canal único; sempre parear com visual/áudio.

## C — ACESSIBILIDADE E PC FRACO
- **Autoplay travado até 1º gesto [FORTE]:** criar/retomar AudioContext DENTRO de um gesto;
  `if(AC.state==='suspended') AC.resume()`. O botão **"Ouvir" é o start 100% garantido** (mover mouse
  às vezes não conta); destravar também no 1º `pointerdown` global.
- **Latência [FORTE]:** <10ms imperceptível; <100ms dentro do "tempo real". **Feedback imediato
  (acerto/erro/toque) = Web Audio sintetizado** (osc, latência mínima); **narração = MP3** (atraso ok).
  Nunca usar MP3 pro "ding".
- **Anti-clique [CONSENSO]:** envelope — rampa de ganho ~12-15ms no ataque e no decaimento (exponencial
  soa linear). Osciladores são baratos; criar por evento e deixar morrer (`stop`).
- **Não depender só de som [FORTE]:** todo evento sonoro tem **gêmeo visual**; legenda sincronizada da
  narração (WCAG 1.2); alvos ≥44×44px; contraste nos dois temas; jogo 100% jogável sem som.
- **`prefers-reduced-motion` [FORTE]:** cortar/atenuar screenshake, escalas grandes e partículas.

## D — SOM/INTERAÇÃO COMO STEALTH ASSESSMENT
- Cada momento sonoro-interativo é um carimbo de evidência: **tentativas até o acorde de acerto**
  (domínio), **hesitação inicial** (ms até a 1ª ação), tempo total e variabilidade.
- **Nuance honesta [FORTE]:** rápido ≠ sempre bom (bom aluno às vezes vai devagar de propósito). Use
  tempo/hesitação pra **decidir quando o mascote oferece dica** (andaime), não como nota. Se hesitação
  alta E 2+ erros → o mascote PERGUNTA algo que reencaminha ("o Byte pergunta, não responde").

## RECEITA (evento → som → visual → háptico → sinal medido)
| Evento | Som (Web Audio) | Visual (transform/opacity) | Háptico (Android) | Sinal |
|---|---|---|---|---|
| Pegar objeto | clique 12ms | squash 1.15/0.88 | vibrate(15) | 1ª ação (hesitação) |
| Arrastar | silêncio (é raciocínio) | gruda no dedo, sombra cresce | — | trajetória/tempo |
| Soltar CERTO | tríade maior que resolve | assenta com mola + 3-5 partículas | vibrate(30) | tentativas até acerto |
| Soltar ERRADO | dissonância suave 140ms | volta com mola, shake 2-3px | vibrate([20,40,20]) | conta erro |
| Contar / reta | pitch sobe por unidade, pulso | número acende no compasso | pulso leve | — |
| Fração/proporção | razão = intervalo (3:2=quinta) | duas barras proporcionais | — | — |
| Acerto de fase | arpejo + brilho VARIÁVEL | confete leve, medalha | vibrate([30,50,30]) | domínio |
| Narração | MP3 edge-tts humano | legenda sincronizada | — | — |

**Regras de ouro:** (1) ding = Web Audio; narração = MP3. (2) todo som tem gêmeo visual; jogável sem
som. (3) silêncio no pensar, som no evento. (4) consonância resolve no acerto; dissonância curta/gentil
no erro. (5) varie o acerto (surpresa); brilho extra ocasional. (6) 1 AudioContext, destrava no "Ouvir"
+ 1º pointerdown. (7) envelope ~12-15ms (sem clique). (8) respeita reduced-motion; alvos ≥44px. (9)
háptico é bônus Android. (10) cada acorde de acerto TAMBÉM é log → stealth assessment que apoia, não julga.

## CÓDIGO (colável — mas ADAPTAR ao padrão de compatibilidade do manual premium!)
> ⚠️ O manual premium exige: só `var`/`function`/`for` clássico; PROIBIDO `=>`, `let`/`const`, crase,
> `?.`, `??`, spread. O bloco abaixo veio em ES6 — reescrever em var/function antes de usar (a função
> `nota()` do próprio Circo já é a referência do estilo compatível).

```
/* 1) 1 AudioContext, destravado no gesto */
var AC;
function ac(){ if(!AC){ AC=new (window.AudioContext||window.webkitAudioContext)(); }
  if(AC.state==='suspended'){ AC.resume(); } return AC; }
document.addEventListener('pointerdown', function(){ ac(); }, {passive:true});
/* botao "Ouvir" = start garantido: btnOuvir.onclick = function(){ ac(); tocarNarracao(); }; */

/* 2) nota com envelope anti-clique */
function nota(freq, dur, tipo, vol){ dur=dur||0.18; tipo=tipo||'sine'; vol=vol||0.2;
  var c=ac(), t=c.currentTime, o=c.createOscillator(), g=c.createGain();
  o.type=tipo; o.frequency.value=freq;
  g.gain.setValueAtTime(0.0001,t);
  g.gain.exponentialRampToValueAtTime(vol, t+0.012);   /* ataque ~12ms */
  g.gain.exponentialRampToValueAtTime(0.0001, t+dur);  /* decai suave  */
  o.connect(g); g.connect(c.destination); o.start(t); o.stop(t+dur+0.02); }

/* acerto: triade maior que resolve | erro: 2a menor curta e gentil */
function acerto(){ var f=[523.25,659.25,783.99],i; for(i=0;i<f.length;i++){ (function(fr,k){
  setTimeout(function(){ nota(fr,0.35,'triangle',0.18); }, k*55); })(f[i],i); } buzz(30); }
function erro(){ nota(300,0.14,'sine',0.14); nota(318,0.14,'sine',0.10); buzz([20,40,20]); }

/* 3) sonificacao: reta que canta / fracao como intervalo */
function cantaAte(n){ var k; for(k=0;k<=n;k++){ (function(j){
  setTimeout(function(){ nota(220*Math.pow(2,j/12),0.13,'sine',0.18); }, j*180); })(k); } }
function fracao(num,den){ var b=330, r=num/den; nota(b,0.6); nota(b*(r>1?r:1/r),0.6,'sine',0.16); }

/* 4) haptico (Android; no-op no resto) */
function buzz(p){ if(navigator.vibrate){ try{ navigator.vibrate(p); }catch(e){} } }

/* 5) sinais stealth */
var S={ t0:0, first:0, tries:0 };
function abriu(){ S={t0:(new Date()).getTime(), first:0, tries:0}; }
function agiu(){ if(!S.first){ S.first=(new Date()).getTime()-S.t0; } }
function checou(ok){ S.tries++; if(ok){ acerto();
  log({ hesitacaoMs:Math.round(S.first), tentativas:S.tries, msAteAcerto:(new Date()).getTime()-S.t0 });
} else { erro(); } }
```
```
/* CSS: squash&stretch, shake — so transform/opacity, com par -webkit- */
@keyframes pop{0%{transform:scale(1)}40%{transform:scale(1.15,.88)}70%{transform:scale(.96,1.04)}100%{transform:scale(1)}}
@keyframes shake{0%,100%{transform:translate(0,0)}25%{transform:translate(-3px,2px)}75%{transform:translate(3px,-2px)}}
.pop{animation:pop .18s ease-out} .shake{animation:shake .12s linear}
@media (prefers-reduced-motion: reduce){ .pop,.shake{animation:none} }
button,.alvo{ min-width:44px; min-height:44px; }
```
(hit-stop barato: no impacto, micro-pausa ~50ms antes de retomar a animação = "peso". Partículas: 3-5
divs com transform+opacity removidos no animationend.)

## FONTES (principais)
Música/cognição https://pmc.ncbi.nlm.nih.gov/articles/PMC12420879/ · modality (Mayer)
https://www.cambridge.org/core/books/abs/multimedia-learning/modality-principle/7FFD4737F95CD9124CE369B0BD075800
· sonificação https://www.frontiersin.org/articles/10.3389/fcomm.2020.00046 · fração-intervalo
https://nrich.maths.org/problems/tuning-and-ratio · consonância/emoção https://pmc.ncbi.nlm.nih.gov/articles/PMC3002933/
· música-recompensa/dopamina https://www.pnas.org/doi/10.1073/pnas.1809855116 · voice principle
https://files.eric.ed.gov/fulltext/EJ1341358.pdf · voice revisitado https://www.researchgate.net/publication/360876002
· irrelevant sound https://www.nature.com/articles/s41598-025-85855-w · seductive details
https://www.sciencedirect.com/science/article/abs/pii/S0747563210001263 · Swink game feel
https://eolt.org/articles/game-feel/ · juice https://www.youtube.com/watch?v=Fy0aCDmgnxg · Disney 12
https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation · manipulação direta
https://www.nngroup.com/articles/direct-manipulation/ · Vibration API
https://developer.mozilla.org/en-US/docs/Web/API/Vibration_API · autoplay/unlock
https://developer.chrome.com/blog/web-audio-autoplay/ · latência
https://dl.acm.org/doi/fullHtml/10.1145/3678299.3678331 · WCAG https://webaim.org/standards/wcag/checklist
· reduced-motion https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion ·
stealth (Shute) https://direct.mit.edu/books/oa-monograph/3700/Stealth-Assessment · tempo/hesitação
https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2015.01046/full
