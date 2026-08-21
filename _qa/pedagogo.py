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
import json
import os
import re
import subprocess
import sys

# ⚠️ DUAS CEGUEIRAS DESTE PORTAO, achadas na atividade de ortografia do 5o ano
#    (ago/2026) — e as duas da mesma familia das outras: ele foi escrito
#    olhando a atividade ESCRITA A MAO e nao conhece a MONTADA.
#      · `"campo"` estava aqui para pegar o CAMPO DE DIGITAR (o motor escreve
#        `el("input","campo")` na tela do nome). Numa atividade sobre a palavra
#        CAMPO — o campo de futebol do bairro — a chave `k:"campo"` do jogo da
#        memoria batia no regex e o portao dizia que o SIMBOLO chegou antes da
#        FIGURA. Agora ele pede o contexto do input: `el("input","campo"`.
#      · a FIGURA da atividade montada nao entra por `imgEl(`, e sim pelo
#        `figEl(` da ponte do integrador. Sem esse nome, TODA atividade montada
#        aparecia como "figura: nenhuma" — e ai qualquer simbolo reprovava.
SIMBOLICO = (r'_sim_|el\("input","campo"|teclafc|tecladofc|cquad|\bslot\b'
             r'|letrafc|type="text"')
FIGURAL = r'cenaImg\(|imgEl\(|figEl\(|moldurafoto|"janela"|objcena'
# fases onde "errar" nao existe (marcar/desmarcar, explorar, palpite livre)
# ⚠️ fases onde "errar" nao existe (marcar/desmarcar, explorar, palpite livre) ou
#    onde a ajuda DESTRUIRIA a fase. O Desafio Relampago e de VELOCIDADE: dica no
#    meio dele acaba com o que ele treina (evocacao rapida). Exigir andaime ali
#    seria o portao brigando com a didatica em vez de defende-la.
# ⚠️ era uma lista de NOMES EXATOS, todos do estilo `m*` de UMA atividade. No
#    Jardim as mesmas fases se chamam `telaAquecimento`, `telaRelampagoJd`,
#    `telaMemoria`, `telaEnsinar` — e o portao cobrava andaime justamente das
#    fases onde andaime estraga o que se treina. Agora casa pelo ASSUNTO do
#    nome, que e o que importa, e nao pela grafia de uma atividade so.
SEM_ERRO_PALAVRAS = ("palpite", "caca", "lupa", "ensinar", "aquec", "fim",
                     "vento", "voo", "escala", "expo", "desenh", "relampago",
                     "memoria", "pintar", "galeria", "prever")


def sem_erro(nome):
    n = nome.lower()
    return any(p in n for p in SEM_ERRO_PALAVRAS)


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
    # ⚠️ era so `m\w+` — e por isso o Jardim (telaXxx) era invisivel para ele.
    for m in re.finditer(r"^function\s+((?:m|tela|peca|fase)[A-Z_]\w*)\s*\(", js, re.M):
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


# ⚠️⚠️ LICAO PAGA (ago/2026): ESTE PORTAO ESTAVA CEGO NA CASA INTEIRA.
#
# Ele so sabia ler UM formato de atividade: fases chamadas `mAlgumaCoisa` e a
# corrente comecando numa fase com nome FIXO no codigo, `mPalpite` — o nome de
# uma fase da Doceria. Resultado: no Jardim do Broto (fases `telaXxx`) e em toda
# atividade MONTADA pelo esqueleto (fases que sao DADOS, nem funcao existe) ele
# imprimia "nao consegui ler a cadeia de fases. Nada a conferir." e saia com
# codigo 0. A banca lia aquilo e seguia em frente.
#
# E o que ele mede e o que o Marcos mais cobra: o simbolo depois do figural, o
# andaime que cresce, o aquecimento no meio, o problema antes do conceito. Ou
# seja: a escada didatica das atividades da casa nao estava sendo medida por
# ninguem — nem no Jardim, que esta no ar.
#
# Agora ele le os TRES formatos, e quem descobre onde a corrente comeca e a
# propria corrente (a fase que ninguem aponta), nao um nome escrito aqui dentro.
NOME_FASE = re.compile(r"^(m|tela|peca|fase)[A-Z_]\w*$")


def cadeia(cs):
    prox, apontado = {}, set()
    for f, c in cs.items():
        for pad, idx in [(r'fechaFase\(', 4), (r'mostraBanner\(', 1),
                         (r'depoisDaFala\(', 2)]:
            achou = False
            for m in re.finditer(pad, c):
                a = args_quotes(c, m.end() - 1)
                if len(a) > idx:
                    nome = a[idx].strip()
                    if NOME_FASE.match(nome) and nome in cs:
                        prox.setdefault(f, nome)
                        apontado.add(nome)
                        achou = True
                        break
            if achou:
                break

    # o comeco e a fase que ninguem aponta (e que aponta alguem). Se houver mais
    # de uma, vale a que estiver primeiro no arquivo — a ordem em que foi escrita.
    fases = [f for f in cs if NOME_FASE.match(f)]
    raizes = [f for f in fases if f in prox and f not in apontado]
    inicio = raizes[0] if raizes else ("mPalpite" if "mPalpite" in cs else
                                       (fases[0] if fases else None))

    ordem, cur, vis = [], inicio, set()
    while cur and cur not in vis:
        ordem.append(cur)
        vis.add(cur)
        cur = prox.get(cur)
    return ordem


def cadeia_mestre(js, cs):
    u"""⭐ O JARDIM (e os irmaos dele) publicam a ordem REAL das fases num array
    `FASES_MESTRE` — e usam um ajudante generico (`mostraBanner(cfg.msg, cfg.prox)`)
    para andar. Seguir a corrente pelos ARGUMENTOS so achava 5 das 17 fases, e
    com uma cadeia curta o portao acusava o AQUECIMENTO de estar "em 100% do
    caminho" quando ele esta no meio dos 17. Portao que acusa o inocente ensina
    a ignorar portao — entao aqui ele le a ordem onde ela esta escrita."""
    m = re.search(r"FASES_MESTRE\s*=\s*(\[[\s\S]*?\]);", js)
    if not m:
        return []
    nomes = re.findall(r'\[\s*"([A-Za-z_$][\w$]*)"', m.group(1))
    return [n for n in nomes if n in cs]


def cadeia_montada(html):
    u"""⭐ ATIVIDADE MONTADA: as fases nao sao funcoes, sao DADOS (`var FASES=[...]`).

    A escada didatica esta la do mesmo jeito — so que escrita em outro lugar.
    Aqui cada fase vira um "corpo" de mentira, com o texto que a crianca ve
    (selo, enunciado, dica, conceito) e o conteudo da gaveta. As mesmas quatro
    perguntas do portao passam a valer, sem regra nova nenhuma."""
    # ⚠️ o montador declara `var FASES = [];` no topo e ATRIBUI o conteudo la
    #    embaixo (`FASES = [...]`). Procurando so por `var FASES` eu achava a
    #    declaracao VAZIA e concluia "nao consegui ler" — com as 32 fases logo
    #    ali. Pego todas as atribuicoes e fico com a maior.
    achados = re.findall(r"(?:var\s+)?FASES\s*=\s*(\[[\s\S]*?\]);\s*\n", html)
    if not achados:
        return [], {}, []
    crua = max(achados, key=len)
    if len(crua) < 20:
        return [], {}, []
    m = type("M", (), {"group": lambda self, i: crua})()
    try:
        r = subprocess.run(["node", "-e",
                            "console.log(JSON.stringify(%s))" % m.group(1)],
                           capture_output=True, text=True, timeout=30)
        fases = json.loads(r.stdout) if r.returncode == 0 else None
    except Exception:
        fases = None
    if not fases:
        return [], {}, []

    ordem, cs = [], {}
    for i, f in enumerate(fases):
        nome = f.get("id") or ("fase%02d" % (i + 1))
        ordem.append(nome)
        pedacos = [f.get("selo") or "", f.get("enunciado") or "",
                   f.get("dica") or "", f.get("conceito") or "",
                   f.get("mec") or ""]
        try:
            pedacos.append(json.dumps(f.get("dados"), ensure_ascii=False))
            pedacos.append(json.dumps(f.get("dadosExtra"), ensure_ascii=False))
        except Exception:
            pass
        corpo = "\n".join(p for p in pedacos if p)
        # a dica do conteudo.json E o 1o degrau do andaime; o motor poe os
        # outros dois. Escrevo isso na lingua que o portao ja sabe ler.
        if f.get("dica"):
            corpo += '\nmostraDica("%s")\nconsolo()\n' % re.sub(r'["\n]', " ", f["dica"])[:40]
        cs[nome] = corpo
    return ordem, cs, fases


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    alvo = sys.argv[1]
    # ⭐ atividade CRIATIVA (livro de colorir): producao, nao treino — nao tem
    #    escada de dificuldade nem aquecimento. Isencao declarada no conteudo.
    _lado = os.path.join(os.path.dirname(os.path.abspath(alvo)), "conteudo.json")
    try:
        if os.path.exists(_lado):
            _t = json.load(io.open(_lado, encoding="utf-8")).get("tipo", "")
            if str(_t).strip().lower() in ("criativa", "livre", "colorir"):
                print(u"%s -> atividade CRIATIVA (colorir): producao, sem escada/"
                      u"aquecimento. Nada a conferir aqui." % alvo)
                return 0
    except Exception:
        pass
    html = io.open(alvo, encoding="utf-8").read()
    js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    js = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), js, flags=re.S)
    # ⭐ atividade MONTADA primeiro: la as fases sao dados, nao funcoes
    ordem, cs, fases_montadas = cadeia_montada(html)
    if len(ordem) < 3:
        cs = corpos(js)
        ordem = cadeia_mestre(js, cs) or cadeia(cs)
    # ⚠️⚠️ A REGRA QUE FALTAVA, e que custou uma acusacao falsa: CADEIA CURTA NAO
    #    SE JULGA. Com 5 das 17 fases do Jardim na mao, este portao disse que o
    #    AQUECIMENTO estava "em 100% do caminho" — ele esta em 35%, no meio, como
    #    manda. A conta estava certa; o material e que estava pela metade.
    #    Agora, se o arquivo tem muito mais fase do que a corrente que eu
    #    consegui seguir, eu me declaro CEGO em vez de dar veredito.
    quantas = len(re.findall(r"^function\s+(?:m|tela|peca|fase)[A-Z_]\w*\s*\(",
                             js, re.M))
    if 0 < len(ordem) < 8 and quantas >= len(ordem) * 2:
        print(u"%s -> so consegui seguir %d fase(s) de ~%d que existem no arquivo. "
              u"Cadeia pela metade NAO se julga (a conta sairia errada). "
              u"Nada a conferir." % (alvo, len(ordem), quantas))
        return 0
    if len(ordem) < 3:
        print(u"%s -> nao consegui ler a cadeia de fases. Nada a conferir." % alvo)
        return 0

    problemas = []

    # 0. UM DEGRAU POR VEZ — a progressao DIDATICA (correcao do Marcos, ago/2026:
    #    "quando eu falo em progressao eu falo progressao didatica").
    #
    #    Entre duas fases seguidas muda UMA coisa: ou o CONTEUDO (o objetivo) ou
    #    o GESTO (a mecanica). Nunca as duas. Fase que troca as duas nao e um
    #    degrau: e uma atividade nova comecando do zero, e a crianca de 6 anos
    #    perde as duas ancoras ao mesmo tempo — nao sabe o que esta aprendendo
    #    nem o que tem que fazer com a mao.
    #
    #    ⚠️ o AQUECIMENTO e o FECHO LIVRE ficam de fora de proposito: o
    #    aquecimento retoma conteudo antigo com gesto novo por desenho (revisao
    #    espacada), e o fecho nao ensina habilidade nenhuma.
    duplo, vistas = [], set()
    if fases_montadas:
        ant = None
        for f in fases_montadas:
            if (f.get("conceito") or "") == "livre" or "aquec" in (f.get("id") or ""):
                ant = None
                continue
            if ant is not None:
                mudou_conc = (f.get("conceito") or "") != (ant.get("conceito") or "")
                # ⚠️ a primeira versao disto reprovou 27 das 32 passagens — e
                #    estava errada. Trocar de mecanica entre fases e o PADRAO DA
                #    CASA (nenhum gesto acima de 40%, para a crianca nao cansar):
                #    um portao que briga com outra regra da casa e portao mal
                #    escrito. O que de fato machuca e mais estreito: o gesto
                #    ESTREAR junto com o conteudo novo. Mecanica que a crianca ja
                #    conhece e ancora, mesmo sendo diferente da fase anterior.
                estreia = (f.get("mec") or "") not in vistas
                # ⚠️ SEGUNDA correcao da mesma regra, e a que faltava: no COMECO
                #    da atividade TODO gesto e estreia — a crianca ainda nao tem
                #    repertorio nenhum, entao nao existe gesto conhecido em que
                #    ancorar. Cobrar isso da fase 2 e cobrar o impossivel, e
                #    portao que cobra o impossivel vira ruido que se aprende a
                #    ignorar. A regra so vale depois que ha repertorio: tres
                #    gestos ja vistos. Antes disso, estrear e o unico caminho.
                if mudou_conc and estreia and len(vistas) >= 3:
                    duplo.append((ant.get("id"), f.get("id"),
                                  ant.get("mec"), f.get("mec")))
            vistas.add(f.get("mec") or "")
            ant = f
    # ⚠️ AVISO ou REPROVACAO? Depende do que esta na mao de quem monta.
    #    Reordenar as fases resolve PARTE disto; o resto depende do CONTEUDO —
    #    se cada objetivo so tem mecanicas proprias, nao existe gesto conhecido
    #    para abrir o bloco, e nenhuma ordem conserta. Cobrar reprovacao de algo
    #    que a ordem nao resolve seria portao mandando reescrever a atividade
    #    inteira. Entao: acima de metade das viradas, e defeito de escada e
    #    reprova; abaixo disso, e recado para quem escreve o conteudo.
    viradas = max(1, sum(1 for i in range(1, len(fases_montadas))
                         if (fases_montadas[i].get("conceito") or "") !=
                            (fases_montadas[i - 1].get("conceito") or "")))
    if len(duplo) > viradas // 2:
        problemas.append(
            u"%d fase(s) estreiam um GESTO NOVO no mesmo passo em que o CONTEUDO muda "
            u"(ex.: %s -> %s, gesto '%s' visto pela primeira vez com objetivo novo). "
            u"A crianca perde as duas ancoras juntas: nao sabe o que esta aprendendo "
            u"nem o que fazer com a mao. Ensine o gesto num conteudo ja conhecido "
            u"antes de usa-lo para ensinar conteudo novo."
            % (len(duplo), duplo[0][0], duplo[0][1], duplo[0][3]))

    elif duplo:
        print(u"   aviso: %d gesto(s) estreiam junto com conteudo novo (ex.: %s). "
              u"Resolve-se no CONTEUDO: uma fase de ponte que use o gesto novo "
              u"num objetivo que a crianca ja domina." % (len(duplo), duplo[0][1]))

    # 1. concreto -> figural -> simbolico
    #
    # ⚠️ ESTE ITEM NAO SE MEDE NA ATIVIDADE MONTADA, e dizer isso e a unica
    #    resposta honesta (ago/2026). Ele procura no CODIGO da fase o desenho
    #    (`imgEl(`) e o simbolo (o campo de digitar) — e numa atividade montada
    #    a fase nao tem codigo: ela e DADO, e o codigo mora na mecanica, que e
    #    compartilhada por varias fases. O portao imprimia "figura: -" e
    #    "simbolo: -" e seguia como se tivesse aprovado: silencio que parece
    #    aprovacao e o pior resultado possivel.
    #    ⚠️ E NAO da para trocar por "a fase tem campo de figura no dado": numa
    #    atividade de ORTOGRAFIA o objeto de estudo E a palavra escrita, entao
    #    exigir figura antes da primeira palavra reprovaria o certo. A escada
    #    dessa disciplina se confere com o olho do professor.
    if fases_montadas:
        print(u"   concreto->figural->simbolico: NAO MEDI nesta atividade "
              u"(montada: a fase e dado, o codigo e da mecanica). Olho do professor.")
    prim_fig = prim_sim = None
    for i, f in enumerate(ordem):
        c = cs.get(f, "")
        if prim_fig is None and re.search(FIGURAL, c):
            prim_fig = i
        if prim_sim is None and re.search(SIMBOLICO, c):
            prim_sim = i
    if (not fases_montadas) and prim_sim is not None and (prim_fig is None or prim_sim < prim_fig):
        problemas.append(u"o SIMBOLO aparece na fase %d (%s) antes da primeira FIGURA "
                         u"(%s) — a crianca recebe o simbolo sem ter manuseado nem visto"
                         % (prim_sim + 1, ordem[prim_sim],
                            ordem[prim_fig] if prim_fig is not None else "nenhuma"))

    # 2. o andaime cresce
    sem_andaime = []
    for f in ordem:
        if sem_erro(f):
            continue
        c = cs.get(f, "")
        if "sErro" not in c and "err++" not in c:
            continue                       # sem erro possivel: nada a cobrar
        degraus = set()
        for m in re.finditer(r'mostraDica\("([^"]{0,40})', c):
            degraus.add(m.group(1)[:24])
        # ⚠️ ACUSACAO DE INOCENTE, medida no Jardim do Broto (ago/2026): ele
        #    reprovava 14 das 17 fases por "andaime que nao cresce", e o andaime
        #    esta la — so que num AJUDANTE. O Jardim chama `ajudaJd(err, {dica,
        #    apoio, revelar})`, e cada chave dessas E um degrau. Contar so
        #    `mostraDica("...")` literal era medir o estilo de escrita, nao a
        #    didatica. Toda casa tem o seu ajudante; o portao conta as CHAVES.
        for m in re.finditer(r'ajuda\w*\(\s*\w+\s*,\s*\{([^}]{0,600})', c):
            for k in re.findall(r"(\w+)\s*:", m.group(1)):
                if k in ("dica", "apoio", "revelar", "concreto", "mostrar",
                         "pista", "acender", "piscar"):
                    degraus.add("ajuda:" + k)
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
