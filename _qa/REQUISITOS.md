# O que a banca precisa ter instalado (e o que acontece se faltar)

⚠️ **Portão que não acha a ferramenta dele diz `NÃO MEDI` (código 2) e IMPRIME
isso.** Nunca "passa calado" — foi a lição paga em 16/set/2026, quando o
`_qa/silabas.py` rodou sem ffmpeg, imprimiu "ok" e deixou passar uma reprovação
de verdade.

| ferramenta | quem usa | como instalar | sem ela |
|---|---|---|---|
| `pyphen` (traz o dicionário de hifenização **pt_BR** do LibreOffice) | `_qa/silaba_dicionario.py` (portão **1w**) | `pip install pyphen` — o PyPI é alcançável do chat (medido 17/set/2026) | código 2, `NÃO MEDI` |
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
