# 👂 TESTADOR HUMANO — OUVIDO — `_trem`

> 458 fala(s) do `falas.json` ouvidas com faster-whisper (small, CPU) em 918 s. Sai 1 se alguma voz NAO diz o texto. Isto é o olho de VOZ do Revisor (`_qa/revisor.py` é o de TEXTO).

| resultado | quantas |
|---|--:|
| ✅ diz o que está escrito | 404 |
| ❌ diz OUTRA coisa / cortada | 3 |
| 🔇 muda ou não abre | 0 |
| 🟡 conferir no ouvido (curta/parecida) | 36 |
| 🗑 mp3 órfão (nenhuma fala do falas.json usa; peso morto, não defeito) | 213 |

## ❌ Vozes que não dizem o texto

| id | texto esperado | o que ouvi | parecido | motivo |
|---|---|---|--:|---|
| `op_v82k1n` | K de kiwi. | Kadkiuri. | 59 | diz OUTRA coisa |
| `op_15hwt1k` | T de trem. | TeideTrain | 53 | diz OUTRA coisa |
| `op_1b785et` | Y de yoyo. | e epsilon de olho. | 46 | diz OUTRA coisa |

## 🟡 Conferir no ouvido

| id | texto | ouvi | parecido | por quê |
|---|---|---|--:|---|
| `op_11yqf0o` | W de waffle. | W de UFO. | 67 | parecido mas nao igual |
| `op_smm1cd` | Letra Dáblio. Dáblio de waffle. | Letra W. W de UFO. | 73 | parecido mas nao igual |
| `op_3t3x` | Xis | Cheese! | 22 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `op_10odgye` | Letra Ípsilon. Ípsilon de yoyo. | Letra Y. Y de Iroio. | 76 | parecido mas nao igual |
| `op_1g6g899` | bo... la | BULLA | 60 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `op_3ho4p` | ca | Ka! | 50 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `op_3hojd` | sa | S. | 67 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `op_ykmrdp` | maçã | Massa! | 67 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `op_3hoko` | to | Do. | 50 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `op_3hodc` | lo | Lu. | 50 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `op_3hoke` | te | Che. | 40 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `op_1xsbf6y` | va... ca | V-A-K | 60 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `op_4fox1e` | navio | NA VIEU! | 67 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `op_3homc` | vi | Z. | 0 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `op_3hom8` | ré | Here. | 67 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `op_3hoig` | ra | Ah! | 50 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `op_ko10f9` | ra... to | Ah, tu! | 60 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3a` | Á | Ah. | 67 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3b` | Bê | B. | 67 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3c` | Cê | C | 67 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3f` | Éfe | F | 50 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3g` | Gê | G | 67 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3j` | Jóta | J. | 40 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3k` | Cá | Ka! | 50 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3n` | Ene | Any. | 33 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3o` | Ó | Oh. | 67 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3p` | Pê | PIR | 40 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3r` | Érre | R | 40 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3t` | Tê | Till! | 33 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3u` | Ú | O. | 0 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3v` | Vê | Z | 0 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3w` | Dáblio | W. | 0 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3x` | Xis | Cheese! | 22 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `3t3z` | Zê | Z. | 67 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `op_377ezv` | ova | Ovo! | 67 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |
| `op_ykrme0` | sopa | Super! | 44 | fala curta: o reconhecedor erra em nome de letra/silaba — conferir no ouvido |

