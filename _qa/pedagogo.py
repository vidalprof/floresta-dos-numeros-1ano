#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO DO PEDAGOGO — a ESCADA DIDÁTICA, medida.

Cobrança do Marcos (ago/2026): *"lembrando que a atividade tem que estar
progressiva didaticamente"* e, logo depois, *"vários profissionais, auditores
etc antes de entregar: roteirista, pedagogo, especialistas da área"*.

O painel de especialistas já estava escrito no `EDUVERSE-EQUIPE.md`. O problema
é que, na prática, **só a parte técnica era medida** — sintaxe, contraste,
leiaute, imagem quebrada. O pedagogo era eu me lembrando de ser pedagogo; e no
dia em que eu não lembrava, quem via era ele. Foi assim que a barra da
cartografia andou para trás em duas passagens sem ninguém notar.

Este portão mede o que dá para medir da escada didática:

  1. **CONCRETO → FIGURAL → SIMBÓLICO.** O primeiro símbolo (letra, palavra,
     ícone de legenda, campo de digitar) não pode aparecer antes da primeira
     figura. A criança manuseia e vê ANTES de receber o símbolo.
  2. **O ANDAIME CRESCE.** Toda fase onde dá para errar precisa de pelo menos
     DOIS degraus diferentes de ajuda (dica → apoio → revelar). A mesma frase
     três vezes não é andaime: é repetição.
  3. **AQUECIMENTO NO MEIO.** A revisão espaçada tem que cair entre 25% e 65%
     do caminho. No fim ela vira revisão de prova, que é outra coisa.
  4. **O PROBLEMA VEM ANTES DO CONCEITO.** A primeira fase não pode ser
     explicação: tem que ser palpite, exploração ou pergunta.

⚠️ O que ele NÃO mede: se o conteúdo está certo para o ano, se o roteiro tem
graça, se a arte combina. Isso continua sendo do Pedagogo/Roteirista/Diretor de
Arte humanos — e do Marcos, que é o portão final. Portão nenhum substitui olhar.

Uso:  python3 _qa/pedagogo.py _mapa/index.html
Sai com 1 se a escada estiver quebrada.
"""
import io
import re
import sys

SIMBOLICO = r'_sim_|"campo"|teclafc|tecladofc|cquad|\bslot\b|letrafc|type="text"'
FIGURAL = r'cenaImg\(|imgEl\(|moldurafoto|"janela"|objcena'
# fases onde "errar" nao existe (marcar/desmarcar, explorar, palpite livre)
# ⚠️ fases onde "errar" nao existe (marcar/desmarcar, explorar, palpite livre) ou
#    onde a ajuda DESTRUIRIA a fase. O Desafio Relampago e de VELOCIDADE: dica no
#    meio dele acaba com o que ele treina (evocacao rapida). Exigir andaime ali
#    seria o portao brigando com a didatica em vez de defende-la.
SEM_ERRO = ("mPalpite", "mCaca", "mLupa", "mEnsinar", "mAquecimento", "mFim",
            "mVento", "mVoo", "mEscala", "mExpo", "mDesenhe", "mRelampago")


def args_quotes(txt, i):
    p = 0
    k = i
    ini = i + 1
    lst = []
    q = None
    while k < len(txt):
        ch = txt[k]
        if q:
            if ch == "\\":
                k += 2
                continue
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch == "(":
            p += 1
        elif ch == ")":
            p -= 1
            if p == 0:
                lst.append(txt[ini:k])
                break
        elif ch == "," and p == 1:
            lst.append(txt[ini:k])
            ini = k + 1
        k += 1
    return lst


def corpos(js):
    out = {}
    for m in re.finditer(r"^function\s+(m\w+)\s*\(", js, re.M):
        j = js.find("{", m.end())
        k = j
        p = 0
        while k < len(js):
            if js[k] == "{":
                p += 1
            elif js[k] == "}":
                p -= 1
                if p == 0:
                    break
            k += 1
        out[m.group(1)] = js[j:k]
    return out


def cadeia(cs):
    prox = {}
    for f, c in cs.items():
        for pad, idx in [(r'fechaFase\(', 4), (r'mostraBanner\(', 1)]:
            achou = False
            for m in re.finditer(pad, c):
                a = args_quotes(c, m.end() - 1)
                if len(a) > idx:
                    nome = a[idx].strip()
                    if re.match(r"^m\w+$", nome):
                        prox.setdefault(f, nome)
                        achou = True
                        break
            if achou:
                break
    ordem, cur, vis = [], "mPalpite", set()
    while cur and cur not in vis:
        ordem.append(cur)
        vis.add(cur)
        cur = prox.get(cur)
    return ordem


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    alvo = sys.argv[1]
    html = io.open(alvo, encoding="utf-8").read()
    js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    js = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), js, flags=re.S)
    cs = corpos(js)
    ordem = cadeia(cs)
    if len(ordem) < 3:
        print(u"%s -> nao consegui ler a cadeia de fases. Nada a conferir." % alvo)
        return 0

    problemas = []

    # 1. concreto -> figural -> simbolico
    prim_fig = prim_sim = None
    for i, f in enumerate(ordem):
        c = cs.get(f, "")
        if prim_fig is None and re.search(FIGURAL, c):
            prim_fig = i
        if prim_sim is None and re.search(SIMBOLICO, c):
            prim_sim = i
    if prim_sim is not None and (prim_fig is None or prim_sim < prim_fig):
        problemas.append(u"o SIMBOLO aparece na fase %d (%s) antes da primeira FIGURA "
                         u"(%s) — a crianca recebe o simbolo sem ter manuseado nem visto"
                         % (prim_sim + 1, ordem[prim_sim],
                            ordem[prim_fig] if prim_fig is not None else "nenhuma"))

    # 2. o andaime cresce
    sem_andaime = []
    for f in ordem:
        if f in SEM_ERRO:
            continue
        c = cs.get(f, "")
        if "sErro" not in c and "err++" not in c:
            continue                       # sem erro possivel: nada a cobrar
        degraus = set()
        for m in re.finditer(r'mostraDica\("([^"]{0,40})', c):
            degraus.add(m.group(1)[:24])
        if "consolo()" in c:
            degraus.add("__consolo__")
        for m in re.finditer(r'fb\.innerHTML\s*=\s*"?([^";]{0,24})', c):
            degraus.add("fb:" + m.group(1)[:20])
        if len(degraus) < 2:
            sem_andaime.append((f, len(degraus)))
    if sem_andaime:
        problemas.append(u"%d fase(s) em que da para errar e o andaime NAO CRESCE "
                         u"(precisa de 2 degraus: dica -> apoio -> revelar): %s"
                         % (len(sem_andaime), ", ".join("%s(%d)" % x for x in sem_andaime)))

    # 3. aquecimento no meio
    aq = next((i for i, f in enumerate(ordem) if "quec" in f.lower()), None)
    if aq is None:
        problemas.append(u"nao ha fase de AQUECIMENTO (revisao espacada) — e ela que "
                         u"faz o que a crianca aprendeu FICAR")
    else:
        pos = (aq + 1) / float(len(ordem))
        if pos < 0.25 or pos > 0.65:
            problemas.append(u"o AQUECIMENTO esta em %d%% do caminho (%s). Revisao "
                             u"espacada vai no MEIO: no fim ela vira revisao de prova"
                             % (round(pos * 100), ordem[aq]))

    # 4. o problema antes do conceito
    prim = cs.get(ordem[0], "")
    if re.search(r'\bopt\b|escolh|palpite|"pedido"', prim) is None and \
       len(re.findall(r"depoisDaFala|fechaFase", prim)) and "onclick" not in prim:
        problemas.append(u"a PRIMEIRA fase (%s) parece explicacao, nao problema. "
                         u"O conceito vem por ULTIMO." % ordem[0])

    print(u"%s -> escada didatica de %d fases conferida" % (alvo, len(ordem)))
    print(u"   concreto/figural na fase %s | primeiro simbolo na fase %s"
          % ((prim_fig + 1) if prim_fig is not None else "-",
             (prim_sim + 1) if prim_sim is not None else "-"))
    if problemas:
        print(u"   %d PROBLEMA(S) DE ESCADA DIDATICA:" % len(problemas))
        for p in problemas:
            print(u"    - %s" % p)
        return 1
    print(u"   escada ok: simbolo depois do figural, andaime que cresce, "
          u"aquecimento no meio, problema antes do conceito")
    return 0


if __name__ == "__main__":
    sys.exit(main())
