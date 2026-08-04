# -*- coding: utf-8 -*-
# ============================================================
#  AUDITOR DO PADRÃO DA CASA — "didática, ilustrada, sonora e variada?"
#
#  Nasceu de uma frase do Marcos (ago/2026), dita quando já estávamos na
#  sétima atividade: *"ela tem que ser bem didática progressiva didaticamente,
#  bem ilustrada, sonora lembra? isso deve ser guardado para todas as
#  atividades a serem produzidas"*. Estava no costume, não estava escrito em
#  lugar nenhum — e o que não está escrito, um dia sai errado.
#
#  Ele já tinha cobrado o quarto pilar antes, na Legenda: *"tem muita dinâmica
#  parecida... temos um leque bem grande de interatividade"*. Lá a medição
#  mostrou 8 das 19 fases com o MESMO gesto. Por isso este auditor conta
#  GESTO, não conteúdo: duas fases podem ensinar coisas diferentes e mesmo
#  assim ser, para a criança, a mesma tela pela terceira vez.
#
#  Reprova quando:
#    1. um único gesto passa de 40% das fases (atividade repetitiva);
#    2. alguma fase é MUDA (nenhuma narração) — o padrão é toda tela falada;
#    3. sobram menos de 4 gestos diferentes na atividade inteira.
#  Avisa (sem reprovar) sobre fases sem ilustração — há fases que são texto
#  por natureza (caça-palavras, cruzadinha).
#
#  Uso: python3 _qa/padrao.py _historia/index.html
# ============================================================
import os, re, sys

alvo = sys.argv[1] if len(sys.argv) > 1 else ""
if not alvo:
    print("uso: python3 _qa/padrao.py <arquivo.html>")
    sys.exit(2)
html = open(alvo, encoding="utf-8").read()
js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))

# ---- as telas: mesma regra do _qa/fluxo.py (funcao que chama limpa())
def corpo_de(nome, texto, pos):
    j = texto.find("{", pos)
    k, d = j, 0
    while k < len(texto):
        if texto[k] == "{":
            d += 1
        elif texto[k] == "}":
            d -= 1
            if d == 0:
                break
        k += 1
    return texto[j:k]

telas = []
for m in re.finditer(r"^function\s+([A-Za-z_$][\w$]*)\s*\(", js, re.M):
    c = corpo_de(m.group(1), js, m.end())
    if re.search(r"\blimpa\(\)", c):
        telas.append((m.group(1), c))

# telas de serviço não contam como fase de conteúdo
SERVICO = ("telaCapa", "telaQuem", "telaMestre", "telaPainel", "telaFim")
def so_narrativa(c):
    """tela de historia: fala, mostra, e tem SO o botao de seguir.
       ⚠️ contar `.onclick=` nao basta: uma fase que monta 8 botoes dentro de um
       `for` tem UMA ocorrencia de onclick no texto e parecia narrativa. A marca
       de verdade da tela narrativa e ter o botao grande de seguir e mais nada:
       nada de campo de escrever, nada de deslizar, nada de alvo em laco."""
    if re.search(r'type\s*=\s*"text"|el\("textarea"|oninput|onchange|type="range"', c):
        return False
    if not re.search(r'el\("button","btn', c):
        return False
    return len(re.findall(r"\.onclick\s*=", c)) <= 1

fases = [(n, c) for n, c in telas
         if not any(n.lower().startswith(s.lower()) for s in SERVICO)
         and not n.lower().endswith("fim")]
narrativas = [n for n, c in fases if so_narrativa(c)]
fases = [(n, c) for n, c in fases if not so_narrativa(c)]

# ---- que GESTO cada fase pede da criança
GESTOS = [
    ("digitar",    r'type\s*=\s*"text"|el\("input"|"campo"'),
    ("ordenar",    r'\bprox\b.*?ordem|ordem.*?\bprox\b'),
    ("deslizar",   r'type\s*=\s*"range"|"termo"'),
    ("arrastar",   r'addEventListener\("touchmove"'),
    ("pintar",     r'"pal pint|pint "|marcaTexto|"paragrafo"'),
    ("memoria",    r'"mcarta"'),
    ("forca",      r'"forca"|"letrasfc"|"boneco"|forcaErros'),
    ("simulador",  r'"simul"|"medidor"|regula\(|"linhatempo"'),
    ("grade",      r'el\("div","cel"'),
    ("ligar",      r'el\("div","lig"'),
    ("classificar", r'el\("div","cx"|el\("div","bin"|"gav"'),
    ("montar",     r'el\("div","vaga|"tvaga"|"slot"|el\("div","tec"|"fichaP"'),
    ("virar",      r'el\("div","carta|"vira"'),
    ("explorar",   r'"filtro"|style\.filter|"maquina"|"moldura"'),
    ("escolher",   r'el\("div","opt"|el\("div","tecl"|el\("div","pc |"alim"|"rpos"'),
]

conta, porfase, mudas, semimg = {}, [], [], []
for n, c in fases:
    g = None
    for nome, pad in GESTOS:
        if re.search(pad, c):
            g = nome
            break
    g = g or "outro"
    conta[g] = conta.get(g, 0) + 1
    porfase.append((n, g))
    if not re.search(r"falar\(|depoisDaFala\(", c):
        mudas.append(n)
    if not re.search(r"imgEl\(|fotoEl\(|cenaEl\(|<img", c):
        semimg.append(n)

print("%s -> padrao da casa: %d fase(s) com gesto (+%d tela(s) so de narrativa)"
      % (alvo, len(fases), len(narrativas)))
if not fases:
    print("   (nenhuma fase encontrada)")
    sys.exit(0)

for g in sorted(conta, key=lambda k: -conta[k]):
    pct = 100.0 * conta[g] / len(fases)
    print("   %-12s %2d fase(s)  %4.1f%%" % (g, conta[g], pct))

problemas = []
nomeados = dict((k, v) for k, v in conta.items() if k != "outro")
maior = max(nomeados, key=lambda k: nomeados[k]) if nomeados else "outro"
pct = 100.0 * conta.get(maior, 0) / len(fases)
if conta.get("outro", 0) > len(fases) * 0.3:
    print("   aviso: %d fase(s) que eu nao consegui classificar — o auditor precisa "
          "aprender esses gestos" % conta["outro"])
if nomeados and pct > 40.0:
    quais = [n for n, g in porfase if g == maior]
    problemas.append("o gesto \"%s\" e %.0f%% da atividade (%d de %d fases) — para a crianca "
                     "e a mesma tela de novo. Limite: 40%%. Fases: %s"
                     % (maior, pct, conta[maior], len(fases), ", ".join(quais)))
if len(conta) < 4:
    problemas.append("so %d gesto(s) diferentes na atividade inteira (minimo 4) — o leque de "
                     "interatividade da casa e bem maior que isso" % len(conta))
if mudas:
    problemas.append("%d fase(s) MUDA(S), sem nenhuma narracao (o padrao e toda tela falada): %s"
                     % (len(mudas), ", ".join(mudas)))
if semimg:
    print("   aviso: %d fase(s) sem ilustracao (confira se e texto por natureza): %s"
          % (len(semimg), ", ".join(semimg)))

if not problemas:
    print("   padrao ok: variada, falada e ilustrada")
    sys.exit(0)
print("   %d PROBLEMA(S) DE PADRAO:" % len(problemas))
for p in problemas:
    print("    - %s" % p)
sys.exit(1)
