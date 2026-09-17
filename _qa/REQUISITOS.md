# O que a banca precisa ter instalado (e o que acontece se faltar)

⚠️ **Portão que não acha a ferramenta dele diz `NÃO MEDI` (código 2) e IMPRIME
isso.** Nunca "passa calado" — foi a lição paga em 16/set/2026, quando o
`_qa/silabas.py` rodou sem ffmpeg, imprimiu "ok" e deixou passar uma reprovação
de verdade.

| ferramenta | quem usa | como instalar | sem ela |
|---|---|---|---|
| `pyphen` (traz o dicionário de hifenização **pt_BR** do LibreOffice) | `_qa/silaba_dicionario.py` (portão **1w**) | `pip install pyphen` — o PyPI é alcançável do chat (medido 17/set/2026) | código 2, `NÃO MEDI` |
| `espeak-ng` (pronúncia pt-br em IPA) | `_qa/silaba_dicionario.py`, segunda medida (contagem de sílabas) | `apt-get install espeak-ng` — **funciona no chat** (medido 17/set/2026) | a contagem diz `NÃO MEDI` |
| `ffmpeg` / `ffprobe` | `_qa/silabas.py` (duração dos recortes) e o `_padrao/silabas_voz.py` | `apt-get install ffmpeg` — **não vem no contêiner do chat**; vem no runner do Actions | código 2, `NÃO MEDI` |
| `ctc-forced-aligner` + `torch` | `_padrao/silabas_voz.py`, para cortar a sílaba de dentro da palavra | roda no `entregar.yml` | cai para o corte por silêncio, que o portão `_qa/silabas.py` reprova |
| Chromium (`/opt/pw-browsers/chromium-1194/…`) | os portões que abrem o navegador | já vem | código 2 |

## O que NÃO dá para fazer do chat, e por quê (medido em 17/set/2026)

| host | resposta | o que morre com isso |
|---|---|---|
| `pypi.org` | **200** | nada — dá para instalar biblioteca |
| `huggingface.co` | **403** (o proxy recusa o túnel) | o reconhecedor de fala (ASR) para conferir o mp3 **tem de rodar no Actions** |
| `alphacephei.com` (modelos Vosk) | **000 / recusado** | idem |

⚠️ **Aviso de rede tem DATA e se remede antes de repetir.** Estes números são de
17/set/2026.

## Os bancos de português que foram TESTADOS, e o que cada um deu (17/set/2026)

| ferramenta | o que dá | veredito medido |
|---|---|---|
| **`pyphen`** (dicionário pt_BR do LibreOffice) | onde a palavra se corta | ✅ **em uso** (portão 1w). Mão única: só acusa corte a mais |
| **`espeak-ng`** pt-br | a pronúncia em IPA | ✅ **em uso** (portão 1w, 2ª medida). Acertou `CHATO → ʃˈatʊ`, `ABACAXI → …kaʃˈi`, `BICICLETA → bˌisiklˈɛtæ` |
| `epitran` (`por-Latn`) | idem | ❌ **errado em português**: `CHATO → kɐto`, `BICICLETA → biziklɛtɐ`, `ABACAXI → ɐbɐkɐksi`. Não usar |
| `jonatasgrosman/wav2vec2-…-portuguese` | áudio → letras | ⚠️ bom em palavra inteira, **inútil em recorte de 250 ms** (850 medidos, mediana de erro 0,50) |
| `faster-whisper` | áudio → frase | ⏳ em teste, para as FALAS inteiras (é onde ele é forte) |
| `allosaurus` (`por`) | áudio → fones IPA | ❌ **também falha em 250 ms**: `SA` saiu como `i a ŋ` |
| MFCC + DTW entre irmãs | o mesmo pedaço, de palavras diferentes | ⚠️ separa 79%/94% depois de corrigir por POSIÇÃO. Serve de **lista de suspeitos**, não de reprovação |

⚠️ **A conclusão medida, e ela é incômoda:** **nenhum reconhecedor de fala lê um
recorte de sílaba de 250 ms com confiança** — três testados, três falharam. A
defesa do áudio da sílaba continua sendo (1) o alinhador, que corta de dentro da
palavra real, (2) a duração, que pega soletração, e (3) estes dois bancos de
TEXTO, que pegam a divisão errada. O que falta ainda é ouvir as FALAS inteiras,
onde o reconhecedor é forte.
