#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO — "a VOZ da resposta é a PALAVRA que a criança VÊ?"  (0j2)

Esta é a MAIOR classe de erro do projeto, e o Marcos a ouviu mais de uma vez:
*"voz do rato só A e O"*, *"fala ilefante"*, botão que fala diferente do que
está escrito. A causa mora num lugar que NENHUM portão via: a opção/ficha pode
carregar um campo `voz` DIGITADO À MÃO, e a peça declara esse texto como
`data-voz` (o motor: `elm.getAttribute("data-voz") ? ... : textoVisivel(elm)`).
Quando o autor digita o `voz` errado — ou uma divergência que não era de
propósito — a criança VÊ "ELEFANTE" e OUVE outra coisa. E os portões de voz que
já existiam ficavam TODOS verdes:

  · `vozresposta.js`/`fala_o_escrito.js` conferem que o `data-voz` TEM gravação
    e que o mp3 carrega — mas comparam o falado com o TEXTO GRAVADO (que é o
    próprio `voz` re-hasheado), nunca com a PALAVRA na tela. `voz:"cavalo"` numa
    opção "ELEFANTE" tem mp3 de "cavalo", carrega, e passa.
  · `vozdica.py` cuida da DICA; `voztela`/`vozpergunta` do ENUNCIADO; nenhum
    olha o `voz` da RESPOSTA contra o texto visível dela.

O que ESTE portão faz, estático e barato (lê o `conteudo.json` — a mesma verdade
que o `montar.py` usa — e o `falas.json`): para cada ficha/opção TOCÁVEL que
tem TEXTO visível, calcula o que a criança OUVE (o campo `voz` se houver, senão
o texto — que é o que a peça declara em `data-voz`) e exige que bata com o que
ela VÊ. "Bater" aceita as divergências LEGÍTIMAS e SÓ elas:
  · leitura de NÚMERO por extenso  ("5"→"cinco", "2"→"duas/dois", "DÁ 10"→"dá dez");
  · caixa/acento                    ("CASINHA"→"casinha");
  · dica de SÍLABA                  ("BOLA"→"bo... la");
  · EXPLICAÇÃO que começa/termina na palavra ("PASSADO"→"passado, já aconteceu",
    "VERTEBRADO<br>(tem coluna)"→"vertebrado");
  · respelling fonético de uma palavra (mesma inicial, quase igual: "face"→"fásse").
Qualquer outra divergência é o defeito, e o portão TRAVA (exit 1). Também
reprova VOZ AUSENTE: opção com texto visível cujo falado não foi gravado no
`falas.json` — a criança que ainda não lê tocaria o alto-falante e ouviria
silêncio, exatamente o que ele existe para evitar.

FICHA DE IMAGEM sai de fora de propósito: em `memoria`/`ligar` o tocável é uma
FIGURA (tem `img`/`fig`), a `voz` NOMEIA o desenho (a casa = "casa") e não há
TEXTO na tela para divergir. Comparar ali é inventar defeito (`ligar` mostra o
desenho da CASA ligado à palavra "CASINHA": a voz "casa" está certa). E o
ENUNCIADO/pergunta de rodada (`comparar`, `estimar`) não é rótulo de opção —
não tem `t`/`n`, então também fica fora (quem cuida do enunciado é o 0d/0f).

⚠️ Dicas NÃO entram aqui — já são medidas pelo `vozdica.py` (0j). Este é o
irmão que faltava, para as RESPOSTAS.

Uso:  python3 _qa/voz_bate.py <pasta-da-atividade>   (ou o index.html dela)
Sai 0 = tudo bate | 1 = alguma voz diverge/falta | 2 = não medi (sem dados).
"""
import io
import json
import os
import re
import sys
import unicodedata

try:
    unichr
except NameError:
    unichr = chr


# ── a MESMA conta do `chaveVoz` do motor / do `chave_voz` do montar.py ────────
#    Duplicada aqui de propósito (o portão não deve depender do caminho do
#    montador); se um dia a conta mudar, muda nos TRÊS — motor.html, montar.py e
#    aqui — senão o id não bate e o portão mede o arquivo errado.
def chave_voz(s):
    s = re.sub(r"\s+", " ", s or "").strip().lower()
    h = 5381
    for ch in s:
        h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
    if h == 0:
        return "0"
    dig, out = "0123456789abcdefghijklmnopqrstuvwxyz", ""
    while h:
        out = dig[h % 36] + out
        h //= 36
    return out


def texto_limpo(h):
    s = re.sub(r"&#(\d+);", lambda m: unichr(int(m.group(1))), h or "")
    s = s.replace("&amp;", "&").replace("&nbsp;", " ")
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# ── normalização para COMPARAR o que se ouve com o que se vê ──────────────────
#    Caixa, acento e pontuação não contam (a criança OUVE, não soletra); a
#    sílaba "bo... la" é a MESMA palavra "BOLA". O que sobra são as PALAVRAS.
def _norm(s):
    s = texto_limpo(s)
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower()


def _tokens(s):
    return re.findall(r"[a-z0-9]+", _norm(s))


# número (0..20) → formas por extenso aceitas (com variação de gênero) ─────────
_NUM_FORMS = {
    0: ["zero"], 1: ["um", "uma"], 2: ["dois", "duas"], 3: ["tres"],
    4: ["quatro"], 5: ["cinco"], 6: ["seis"], 7: ["sete"], 8: ["oito"],
    9: ["nove"], 10: ["dez"], 11: ["onze"], 12: ["doze"], 13: ["treze"],
    14: ["catorze", "quatorze"], 15: ["quinze"], 16: ["dezesseis"],
    17: ["dezessete"], 18: ["dezoito"], 19: ["dezenove"], 20: ["vinte"],
}


# nome de cada LETRA (a MESMA tabela do `fala_o_escrito.js` e do `montar.py`):
#    o vagão "D" fala "Dê", o "I" fala "Í" — a criança do 1º ano aprende a NOMEAR
#    a letra, e a voz crua do "I" saía em inglês ("ai"). Comparar o glifo "D" com
#    a gravação "Dê" e gritar é inventar defeito; aqui "D" == "Dê" (e "letra dê")
#    é ACERTO. Já normalizada (sem acento/caixa), como o `_norm`.
_NOME_LETRA = {
    "a": "a", "b": "be", "c": "ce", "d": "de", "e": "e", "f": "efe", "g": "ge",
    "h": "aga", "i": "i", "j": "jota", "k": "ca", "l": "ele", "m": "eme",
    "n": "ene", "o": "o", "p": "pe", "q": "que", "r": "erre", "s": "esse",
    "t": "te", "u": "u", "v": "ve", "w": "dablio", "x": "xis", "y": "ipsilon",
    "z": "ze",
}


def _nome_de_letra(tv, ts):
    u"""visível é UMA letra e a voz a NOMEIA (com o "letra" na frente ou não)?
    "P"→"pê", "A"→"letra á", "S"→"esse". É o coração da alfabetização."""
    if len(tv) != 1 or len(tv[0]) != 1 or tv[0] not in _NOME_LETRA:
        return False
    fala = ts[1:] if (len(ts) >= 2 and ts[0] == "letra") else ts
    if len(fala) != 1:
        return False
    nome = _NOME_LETRA[tv[0]]
    # igual, ou variação ortográfica do MESMO nome ("dablio"/"dabliu" p/ W) —
    # respell guarda a inicial, então não deixa "bê" passar por "P".
    return fala[0] == nome or _respell(nome, fala[0])


def _formas_do_token(tok):
    u"""o que este token da TELA pode virar na VOZ: ele mesmo; e, se for número
    de 0 a 20, também a palavra por extenso (qualquer gênero)."""
    formas = {tok}
    if tok.isdigit():
        n = int(tok)
        for w in _NUM_FORMS.get(n, []):
            formas.add(w)
    return formas


def _lev(a, b):
    if a == b:
        return 0
    if not a or not b:
        return len(a) + len(b)
    ant = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        atu = [i]
        for j, cb in enumerate(b, 1):
            atu.append(min(ant[j] + 1, atu[j - 1] + 1,
                           ant[j - 1] + (ca != cb)))
        ant = atu
    return ant[-1]


def _respell(v, s):
    u"""uma palavra dita foneticamente (o autor escreveu o `voz` assim de
    propósito): mesma inicial e quase igual. Conservador — não deixa passar
    palavra trocada ('gato'->'pato' tem inicial diferente; 'rato'->'ramo' tem
    duas letras trocadas numa palavra curta)."""
    if not v or not s or v[0] != s[0]:
        return False
    d = _lev(v, s)
    return d <= max(1, len(v) // 4) + (1 if abs(len(v) - len(s)) <= 1 else 0)


def _prefixo(curto, longo):
    u"""`curto` é o começo de `longo`, palavra a palavra? ('passado' é o começo
    de 'passado ja aconteceu'). Aceita EXPLICAÇÃO acrescentada à palavra."""
    return len(curto) <= len(longo) and longo[:len(curto)] == curto


def voz_bate(falado, visivel):
    u"""o que a criança OUVE (`falado`) é a palavra que ela VÊ (`visivel`)?
    devolve (ok, motivo)."""
    tv = _tokens(visivel)
    ts = _tokens(falado)
    if not tv:
        return True, u"sem texto visível (figura/rótulo mudo)"
    if not ts:
        return False, u"voz vazia"

    # 1) MESMA sequência de palavras, com número por extenso permitido em cada
    #    posição ("DÁ 10" ~ "dá dez"; "5" ~ "cinco"; "2" ~ "duas"/"dois").
    if len(tv) == len(ts) and all(ts[i] in _formas_do_token(tv[i])
                                  for i in range(len(tv))):
        return True, u"igual (ou número por extenso)"

    # 2) sílaba/caixa: as MESMAS letras, sem os espaços da sílaba ("bo... la").
    if "".join(tv) == "".join(ts):
        return True, u"sílaba/caixa"

    # 3) EXPLICAÇÃO: a voz começa OU termina na palavra da tela, ou vice-versa
    #    ("PASSADO" -> "passado, já aconteceu"; "VERTEBRADO (tem coluna)" -> "vertebrado").
    if _prefixo(tv, ts) or _prefixo(ts, tv) \
            or (len(tv) <= len(ts) and ts[-len(tv):] == tv) \
            or (len(ts) <= len(tv) and tv[-len(ts):] == ts):
        return True, u"explicação/rótulo estendido"

    # 4) NOME da letra ("P" -> "pê"; "A" -> "letra á").
    if _nome_de_letra(tv, ts):
        return True, u"nome da letra"

    # 5) respelling fonético de UMA palavra ("face" -> "fásse").
    if len(tv) == 1 and len(ts) == 1 and _respell(tv[0], ts[0]):
        return True, u"respelling fonético"

    return False, u"palavra diferente"


# ── colher as RESPOSTAS que têm `voz` À MÃO ──────────────────────────────────
# Os campos onde mora o RÓTULO que a criança LÊ na própria ficha tocável. A voz
# tem de bater com UM deles. Cada peça usa um nome, então checamos TODOS e passa
# se casar com qualquer um (o `tracar-letra` mostra `letra` "P" e tem `palavra`
# "PÃO" de contexto: a voz "pê" nomeia a LETRA, não a palavra).
# ⚠️ FORA de propósito: `s` é o par do OUTRO lado no `ligar` (a voz nomeia a
#    FIGURA, não esse rótulo distante), e `nome`/`info` são legenda de card de
#    imagem (`vitrine`), onde a voz é uma FRASE que descreve o desenho. Incluí-
#    los faria o portão gritar em cima do certo.
_ROTULOS = ("t", "n", "pal", "palavra", "letra")
_IMG = ("img", "fig", "foto", "imagem", "cena", "verso", "imga", "imgb",
        "imgsen", "icone", "sombra")


def _labels(d):
    out = []
    for k in _ROTULOS:
        v = d.get(k)
        if isinstance(v, str) and texto_limpo(v):
            out.append(v)
    return out


def _tem_imagem(d):
    for k in _IMG:
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return True
    return False


def _etiqueta(rotulo):
    u"""este rótulo é uma ETIQUETA — uma letra ou um número solto — e não a
    PALAVRA da resposta? ("P", "10" são etiqueta; "PÃO", "DÁ 10" são palavra)."""
    toks = _tokens(rotulo)
    return len(toks) == 1 and (toks[0].isdigit() or len(toks[0]) == 1)


def _so_metadata(rotulos):
    u"""TODOS os rótulos são só etiqueta? Num card de banco `{img, letra:"P",
    voz:"pão"}` o "P" é a inicial, não o que a criança lê no tocável — ela vê a
    FIGURA do pão e ouve "pão". Já um `{t:"MAÇÃ", img, voz:...}` tem PALAVRA: aí
    a voz TEM de bater com ela."""
    return bool(rotulos) and all(_etiqueta(r) for r in rotulos)


def colhe(dados, saco):
    u"""desce o `dados`/`dadosExtra` da fase e junta os dicts que carregam um
    campo `voz` À MÃO — a ÚNICA fonte de divergência (sem ele a peça declara
    `data-voz`=texto e a voz sai do texto sozinha)."""
    if isinstance(dados, dict):
        vz = dados.get("voz")
        if isinstance(vz, str) and vz.strip():
            saco.append(dados)
        for v in dados.values():
            colhe(v, saco)
    elif isinstance(dados, list):
        for x in dados:
            colhe(x, saco)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    alvo = sys.argv[1].rstrip("/")
    pasta = os.path.dirname(alvo) if alvo.endswith(".html") else alvo
    cam = os.path.join(pasta, "conteudo.json")
    jf = os.path.join(pasta, "falas.json")
    if not os.path.exists(cam):
        print(u"%s -> sem conteudo.json (atividade feita à mão?): NÃO MEDI as "
              u"vozes das respostas." % pasta)
        return 2
    c = json.load(io.open(cam, encoding="utf-8"))
    ids = set()
    if os.path.exists(jf):
        for f in json.load(io.open(jf, encoding="utf-8")):
            if f.get("id"):
                ids.add(f["id"])

    diverge, ausente, conferidas = [], [], 0
    for i, f in enumerate(c.get("fases") or []):
        onde = u"fase %d (%s)" % (i + 1, f.get("id") or "?")
        saco = []
        colhe(f.get("dados"), saco)
        colhe(f.get("dadosExtra"), saco)
        for d in saco:
            falado = d["voz"]              # `colhe` só junta quem tem `voz` à mão
            rotulos = _labels(d)
            if not rotulos:
                # sem rótulo de TEXTO na ficha: a voz NOMEIA a figura (carta da
                # `memoria`, desenho do `ligar`, card da `vitrine`) e não há
                # palavra escrita para divergir. Fora do escopo — de propósito.
                continue
            conferidas += 1
            # basta a voz bater com UM rótulo da ficha (o `tracar-letra` tem
            # `letra`="P" E `palavra`="PÃO": "pê" nomeia a letra, e é acerto).
            if not any(voz_bate(falado, r)[0] for r in rotulos):
                # a voz NÃO bate com o texto; se a ficha tem FIGURA e os rótulos
                # são só etiqueta (letra/número), a voz está nomeando a FIGURA —
                # legítimo (card de banco). Só é defeito quando há PALAVRA na
                # ficha e a voz diz outra.
                if _tem_imagem(d) and _so_metadata(rotulos):
                    conferidas -= 1
                    continue
                diverge.append((onde, texto_limpo(rotulos[0]),
                                texto_limpo(falado)))
                continue
            # a criança LÊ uma PALAVRA e OUVE `falado` -> a peça declara
            # data-voz=falado -> motor toca op_<chaveVoz(falado)>. Foi gravado?
            # ⚠️ só cobro AUSÊNCIA quando NENHUM rótulo é etiqueta (letra/número):
            #    o card de LETRA ("B" fala "bê", tracar-letra "P"/"PÃO" fala "pê")
            #    tem a voz gravada por outro caminho do montador (nome de letra),
            #    sob a chave da LETRA, não a do nome — cobrar op_<chaveVoz("bê")>
            #    aqui gritava à toa. Ausência de verdade nesses é do `vozfalta.py`
            #    /`vozresposta.js`, que RODAM a tela e sabem o que temVoz resolve.
            if ids and not any(_etiqueta(r) for r in rotulos):
                _id = "op_" + chave_voz(texto_limpo(falado))
                if _id not in ids:
                    ausente.append((onde, texto_limpo(rotulos[0]),
                                    texto_limpo(falado), _id))

    print(u"%s -> %d resposta(s) com texto conferida(s)" % (pasta, conferidas))
    if not conferidas:
        print(u"  NÃO MEDI: nenhuma resposta com texto visível — isso não é "
              u"'passou'.")
        return 2

    erros = len(diverge) + len(ausente)
    if diverge:
        print(u"  %d RESPOSTA(S) QUE FALAM DIFERENTE DO ESCRITO "
              u"(a criança vê uma palavra e ouve outra):" % len(diverge))
        for onde, vis, falado in diverge[:14]:
            print(u"   [%s] vê \"%s\"  →  ouve \"%s\"" % (onde, vis, falado))
    if ausente:
        print(u"  %d RESPOSTA(S) COM ALTO-FALANTE SEM GRAVAÇÃO "
              u"(quem não lê ouve silêncio):" % len(ausente))
        for onde, vis, falado, _id in ausente[:14]:
            print(u"   [%s] \"%s\" fala \"%s\" mas falta %s.mp3 no falas.json"
                  % (onde, vis, falado, _id))
    if not erros:
        print(u"  voz bate: toda resposta fala a palavra que está escrita nela")
        return 0
    print(u"  conserto: tire o campo `voz` da opção (a voz sai do TEXTO VISÍVEL "
          u"sozinha), ou corrija-o. `voz` à mão só para NÚMERO por extenso, "
          u"sílaba ou pronúncia fonética.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
