# -*- coding: utf-8 -*-
# ============================================================
#  AUDITOR DE RESTO DE CLONE — "sobrou coisa da atividade de origem?"
#
#  Nasceu da Fábrica de Brinquedos do Bento (ago/2026). Clonar o MOTOR de uma
#  atividade pronta é a regra da casa e economiza dias de trabalho — mas traz de
#  carona pedaços que são CONTEÚDO, não motor, e que passam despercebidos porque
#  o app abre bonito e não dá erro nenhum:
#
#   1. `var IMGS=[...]` (pré-carga) apontando para as imagens da atividade de
#      ORIGEM: 16 requisições 404 e nenhuma imagem própria pré-carregada. Nos PCs
#      da escola isso faz cada imagem aparecer com atraso na primeira vez.
#      (Estava assim na Fábrica E na Doceria, sem ninguém ver.)
#   2. `var VOZOK={...}` da origem: o alto-falante aparece ao lado de respostas
#      cuja voz não existe nesta pasta. Botão que não faz nada é PIOR que botão
#      nenhum — a criança toca, não acontece nada, e ela desiste de usar.
#   3. `var DOM={...}` com os conceitos da origem: o boletim do fim mostrava
#      "grupos, soma, vezes" numa atividade de 4º ano.
#   4. fala usada sem o MP3 correspondente: o mascote fica mudo naquela tela.
#
#  Uso: python3 _qa/clone.py _fabrica/index.html
# ============================================================
import os, re, sys

# ⚠️ NEM TODA PASTA COM `_` E UMA ATIVIDADE. `_novo` e a area de PUBLICACAO: na
#    hora de publicar, a atividade e COPIADA para la inteirinha — e o portao,
#    varrendo as vizinhas, achava a copia e reprovava a atividade por ser igual
#    a SI MESMA ("o mascote daqui se chama 'Ara', o MESMO nome do mascote de
#    _novo"). Portao que reprova por causa da propria copia nao serve; e pior,
#    ensina a ignorar o portao justo no passo de publicar.
NAO_E_ATIVIDADE = ("_novo", "_recuperado", "_lote", "_cartelas", "_templates",
                   "_padrao", "_qa", "_audio", "_imagens", "_curriculo",
                   "_status", "_plano", "_demos", "_kit", "_lib_jogo")


def e_vizinha(nome):
    u"""a pasta e outra ATIVIDADE (e nao area de servico)?"""
    return nome.startswith("_") and nome not in NAO_E_ATIVIDADE


alvo = sys.argv[1] if len(sys.argv) > 1 else ""
if not alvo:
    print("uso: python3 _qa/clone.py <arquivo.html|pasta>")
    sys.exit(2)
pasta = alvo if os.path.isdir(alvo) else os.path.dirname(os.path.abspath(alvo))
pasta = os.path.relpath(pasta)
arq = alvo if os.path.isfile(alvo) else os.path.join(pasta, "index.html")
if not os.path.isfile(arq):
    print("%s -> sem index.html" % pasta)
    sys.exit(0)

html = open(arq, encoding="utf-8").read()
js = "".join(re.findall(r"<script>(.*?)</script>", html, re.S))
img = os.path.join(pasta, "img")
audio = os.path.join(pasta, "audio")
problemas = []

# ---- 1) pré-carga apontando para imagem que não existe aqui
m = re.search(r"var IMGS=\[(.*?)\];", js, re.S)
if m and os.path.isdir(img):
    nomes = re.findall(r'"([^"]+)"', m.group(1))
    faltam = [n for n in nomes
              if not os.path.exists(os.path.join(img, n + ".png"))
              and not os.path.exists(os.path.join(img, n + ".jpg"))]
    if faltam:
        problemas.append("pre-carga (var IMGS) aponta para %d imagem(ns) que NAO existem aqui: %s%s"
                         % (len(faltam), ", ".join(faltam[:5]), " ..." if len(faltam) > 5 else ""))
    elif nomes:
        print("   pre-carga: %d imagens, todas existem" % len(nomes))

# ---- 2) alto-falante prometendo voz que não existe
m = re.search(r"var VOZOK=\{(.*?)\};", js, re.S)
if m and os.path.isdir(audio):
    ks = re.findall(r'"([0-9a-z]+)"\s*:', m.group(1))
    faltam = [k for k in ks if not os.path.exists(os.path.join(audio, "op_%s.mp3" % k))]
    if faltam:
        problemas.append("alto-falante (VOZOK) promete %d voz(es) sem MP3 aqui: %s%s"
                         % (len(faltam), ", ".join(faltam[:5]), " ..." if len(faltam) > 5 else ""))
    elif ks:
        print("   alto-falante: %d vozes, todas com MP3" % len(ks))

# ---- 3) fala usada sem MP3
if os.path.isdir(audio):
    # so conta id FIXO: falar("x") fechando logo. falar("hv_cur_"+chave) monta o
    # nome em tempo de execucao e nao da para conferir por aqui.
    ids = set(re.findall(r'falar\("([a-z0-9_]+)"\s*\)', js))
    ids |= set(re.findall(r'depoisDaFala\("([a-z0-9_]+)"\s*,', js))
    ids |= set(re.findall(r'montaBarra\("([a-z0-9_]+)"\s*,', js))
    faltam = sorted(i for i in ids if not os.path.exists(os.path.join(audio, i + ".mp3")))
    if faltam:
        problemas.append("%d fala(s) usada(s) sem MP3 (o mascote fica mudo ali): %s%s"
                         % (len(faltam), ", ".join(faltam[:5]), " ..." if len(faltam) > 5 else ""))
    elif ids:
        print("   narracao: %d falas usadas, todas com MP3" % len(ids))

# ---- 4) conceitos medidos x conceitos registrados x rotulos do boletim
m = re.search(r"var DOM=\{(.*?)\}", js, re.S)
if m:
    dom = set(re.findall(r"([a-z_]+)\s*:", m.group(1)))
    regs = set(re.findall(r'reg\("([a-z_]+)"', js))
    orfaos = sorted(regs - dom)
    mudos = sorted(dom - regs)
    if orfaos:
        problemas.append("reg() usa conceito que NAO esta no DOM (nao entra no boletim nem no relatorio): %s"
                         % ", ".join(orfaos))
    if mudos:
        problemas.append("DOM tem conceito que NENHUMA fase registra (aparece sempre zerado): %s"
                         % ", ".join(mudos))
    mr = re.search(r"var ROTCRI=\{(.*?)\};", js, re.S)
    if mr:
        rot = set(re.findall(r"([a-z_]+)\s*:", mr.group(1)))
        semrot = sorted(dom - rot)
        if semrot:
            problemas.append("conceito sem rotulo em ROTCRI (o boletim mostra o nome tecnico): %s"
                             % ", ".join(semrot))
    if not orfaos and not mudos:
        print("   medicao: %d conceitos, todos registrados por alguma fase" % len(dom))

# ---- 5) fase de arrastar sem o guarda do evento fantasma do celular
# so conta como ARRASTO se houver touchmove + fantasma/clone; o touchstart
# sozinho costuma ser o gesto secreto da medalha (segurar 2s), que nao arrasta.
temArrasto = bool(re.search(r'addEventListener\("touchmove"', js)) and \
             bool(re.search(r"cloneNode|fantasma", js))
if temArrasto:
    if not re.search(r"ultimoToque", js):
        problemas.append("tem fase de ARRASTAR sem guarda de evento fantasma do celular "
                         "(o mouse de compatibilidade desmarca a peca e o TOQUE simples nao funciona)")
    else:
        print("   arrasto: guarda de evento fantasma presente")

# ---- 6) SERVICE WORKER: nome de cache alheio, lista de outra atividade, e o
# apagador que come o cache das VIZINHAS.
#   ⚠️ LIÇÃO PAGA (ago/2026): TODAS as atividades moram no MESMO endereço
#   (vidalprof.github.io), então elas dividem o mesmo armazenamento de cache do
#   navegador. Duas coisas quebravam por causa disso:
#     (a) a Legenda tinha ficado com o CACHE e a LISTA da Redação (resto de
#         clone): nada era pré-carregado, e as duas brigavam pelo mesmo nome;
#     (b) o activate apagava TODO cache com nome diferente do seu — ou seja,
#         abrir uma atividade DELETAVA o modo offline de todas as outras.
#   Conserto: prefixo próprio por atividade e apagar só as versões dela mesma.
sw = os.path.join(pasta, "sw.js")
if os.path.exists(sw):
    txt = open(sw, encoding="utf-8").read()
    def familia(t):
        """nome do cache SEM a versao: 'legenda-clique-v2' e 'legenda-clique-' viram
           a mesma familia, senao um so bump de versao esconderia o nome alheio."""
        m = re.search(r'var (?:PREFIXO|CACHE)\s*=\s*"([^"]+)"', t)
        if not m:
            return ""
        return re.sub(r"-?v\d+$", "", m.group(1)).rstrip("-")
    nome = familia(txt)
    # o nome tem que lembrar ESTA pasta, nao a de origem
    raiz = pasta.strip("_/").split("/")[0]
    for outra in sorted(os.listdir(".")):
        if not e_vizinha(outra) or outra.strip("_") == raiz:
            continue
        osw = os.path.join(outra, "sw.js")
        if not os.path.exists(osw):
            continue
        outro = familia(open(osw, encoding="utf-8").read())
        if nome and outro == nome:
            problemas.append("o sw.js usa o MESMO nome de cache de %s (\"%s\") — as duas dividem "
                             "o armazenamento do navegador e se atrapalham" % (outra, nome))
    if re.search(r"k\s*!==\s*CACHE\s*\)\s*return\s+caches\.delete", txt):
        problemas.append("o sw.js APAGA todo cache que nao seja o dele — como todas as atividades "
                         "moram no mesmo endereco, isso derruba o modo offline das vizinhas "
                         "(use um PREFIXO e apague so as versoes desta atividade)")
    ma = re.search(r"var ATIVOS=\[(.*?)\];", txt, re.S)
    if ma:
        sumidos = [i for i in re.findall(r'"\./([^"]*)"', ma.group(1))
                   if i and i != "index.html" and not os.path.exists(os.path.join(pasta, i))]
        if sumidos:
            problemas.append("o sw.js manda pre-carregar %d arquivo(s) que NAO existem nesta "
                             "atividade (lista da origem): %s" % (len(sumidos), ", ".join(sumidos[:4])))
        else:
            print("   service worker: nome proprio e lista de arquivos batendo")


# ---- 7) O RELATORIO DO PROFESSOR falando de OUTRA materia
#   ⚠️ LIÇÃO PAGA (o Marcos pegou, ago/2026): a Máquina do Tempo (História) tinha
#   o painel INTEIRO da Legenda do Clique — "Concordância nominal", "Formar
#   adjetivo por sufixo", "Montar o grupo nominal", e o trecho do currículo de
#   Português. O `var DOM` estava certo, as fases estavam certas, mas os rótulos
#   do parecer eram strings soltas que ninguém trocou. O professor ia imprimir
#   um parecer da matéria errada.
#   Regra: os rótulos do parecer (CONCN) têm que cobrir EXATAMENTE os conceitos
#   do DOM — nem sobrando o da origem, nem faltando o daqui.
mdom = re.search(r"var DOM=\{(.*?)\}", js, re.S)
mcon = re.search(r"var CONCN=\{(.*?)\};", js, re.S)
if mdom and mcon:
    dom2 = set(re.findall(r"([a-z_]+)\s*:", mdom.group(1)))
    con = set(re.findall(r"([a-z_]+)\s*:", mcon.group(1)))
    sobra = sorted(con - dom2)
    falta = sorted(dom2 - con)
    if sobra:
        problemas.append("o parecer do professor (CONCN) tem rotulo de conceito que NAO existe "
                         "nesta atividade — e da atividade de origem: %s" % ", ".join(sobra))
    if falta:
        problemas.append("o parecer do professor (CONCN) nao tem rotulo para: %s "
                         "(o professor le o nome tecnico)" % ", ".join(falta))
    if not sobra and not falta:
        print("   parecer do professor: rotulos batendo com os conceitos daqui")

# ---- 7b) campo de MED que o painel le e ninguem preenche
for campo in sorted(set(re.findall(r"MED\.([a-z]+)(?:&&|\.length|\[)", js))):
    if not re.search(r"MED\.%s\s*=|%s\s*:" % (campo, campo), js):
        problemas.append("o painel le MED.%s, mas nada nesta atividade preenche esse campo "
                         "(era da origem)" % campo)

# ---- 8) ⭐ PREFIXO DE OUTRA ATIVIDADE — a rede que pega o resto de clone GERAL
#   Ordem do Marcos (ago/2026): *"favor nao poder mais haver resto do clone, faca
#   com que isso nao aconteca mais"*. Os itens 1-7 acima pegam um TIPO de resto
#   cada um, e a cada rodada aparecia um tipo novo (o zeraProgresso com os
#   conceitos da Legenda; o verso da carta apontando para img/cq_base.png, de
#   outra atividade). Este item nao pergunta "qual tipo": ele pergunta se ha
#   qualquer coisa com a MARCA de outra atividade.
#
#   Como funciona: cada atividade tem o seu prefixo (hv_, jd_, fb_, dc_...),
#   descoberto pelos nomes dos arquivos de img/ e audio/ dela. Se o HTML desta
#   atividade cita um prefixo que e a marca de OUTRA pasta e NAO desta, e resto
#   de clone — nao importa se e imagem, voz, variavel ou comentario.
def prefixo_de(pasta_):
    """o prefixo dominante dos arquivos de uma atividade (ex.: 'hv_')"""
    from collections import Counter
    c = Counter()
    for sub in ("img", "audio"):
        d = os.path.join(pasta_, sub)
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            m = re.match(r"([a-z]{2,6}_)", f)
            if m:
                c[m.group(1)] += 1
    if not c:
        return None
    pref, n = c.most_common(1)[0]
    return pref if n >= 4 else None


meu = prefixo_de(pasta)
if meu:
    raiz = os.path.dirname(os.path.abspath(pasta)) or "."
    alheios = {}
    for outra in sorted(os.listdir(raiz)):
        cam = os.path.join(raiz, outra)
        if not e_vizinha(outra) or not os.path.isdir(cam) or os.path.abspath(cam) == os.path.abspath(pasta):
            continue
        pf = prefixo_de(cam)
        if pf and pf != meu:
            alheios.setdefault(pf, outra)
    achados = []
    for pf, dona in sorted(alheios.items()):
        # so conta se aparecer como NOME de arquivo/identificador, nao dentro de palavra
        for m in re.finditer(r"[\"'/(]\s*(%s\w+)" % re.escape(pf), html):
            achados.append((m.group(1), dona))
            break
    if achados:
        problemas.append("%d marca(s) de OUTRA atividade no arquivo (prefixo alheio): %s"
                         % (len(achados),
                            ", ".join("%s (e da %s)" % (a, d) for a, d in achados[:6])))
    else:
        print("   prefixo: nada com a marca de outra atividade (o meu e '%s')" % meu)

# ---- 9) MANIFESTO com o nome de OUTRA atividade
#   Achado ao criar a cartografia (ago/2026): o manifest.json da Maquina do
#   Tempo ainda dizia "A Legenda do Pingo". Ninguem ve isso na tela — mas e o
#   nome que aparece quando a crianca INSTALA a atividade no celular, e o que
#   o professor le na lista de apps. Resto de clone que passa despercebido
#   justamente por morar fora do index.html.
man = os.path.join(pasta, "manifest.json")
if os.path.exists(man):
    try:
        import json as _json
        nome_man = (_json.load(io.open(man, encoding="utf-8")).get("name") or "").strip()
    except Exception:
        nome_man = ""
    mt = re.search(r"<title>(.*?)</title>", html, re.S)
    titulo = re.sub(r"\s+", " ", (mt.group(1) if mt else "")).strip()
    def _chave(x):
        x = re.sub(r"&#\d+;", "", x).lower()
        return set(w for w in re.findall(r"[a-zà-ú]{4,}", x))
    if nome_man and titulo and not (_chave(nome_man) & _chave(titulo)):
        problemas.append("o manifest.json chama a atividade de %r, mas o titulo aqui e %r "
                         "(e o nome que aparece ao INSTALAR no celular)" % (nome_man, titulo))
    elif nome_man:
        print("   manifesto: o nome bate com o titulo da atividade")

# ---- 10) ⭐ O NOME DE OUTRA ATIVIDADE NO TEXTO
#   Ordem do Marcos, cobrada DUAS vezes (ago/2026): o titulo da Maquina do Tempo
#   ficou na cartografia — no <title>, no H1 DA CAPA (a crianca le!) e no
#   cabecalho do relatorio do professor. O item 8 (prefixo) nao pega isto,
#   porque nome de atividade nao tem prefixo; e a troca que eu fazia na mao
#   falhava porque o mesmo texto aparece com ACENTO e com ENTIDADE (&#225;),
#   entao um replace pegava dois lugares e deixava o terceiro.
#   Aqui a comparacao e feita com as entidades RESOLVIDAS, e a busca cobre TODAS
#   as atividades vizinhas.
def _texto(x):
    x = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), x or "")
    return re.sub(r"\s+", " ", x).strip()

mt = re.search(r"<title>(.*?)</title>", html, re.S)
meu_titulo = _texto(mt.group(1)) if mt else ""
# o HUB e a excecao legitima: o trabalho dele e justamente listar as atividades
# pelo nome. Qualquer OUTRA pasta citando nome alheio e resto de clone.
if os.path.basename(os.path.abspath(pasta)) in ("_site", "_educaverso"):
    meu_titulo = ""
    print("   nome: (hub — citar as atividades pelo nome e o trabalho dele)")
if meu_titulo:
    raiz2 = os.path.dirname(os.path.abspath(pasta)) or "."
    alheios2 = []
    for outra in sorted(os.listdir(raiz2)):
        cam = os.path.join(raiz2, outra, "index.html")
        if not e_vizinha(outra) or not os.path.exists(cam): continue
        if os.path.abspath(os.path.dirname(cam)) == os.path.abspath(pasta): continue
        # ⚠️ nada de `except: continue` aqui. Na estreia este bloco usava
        #    io.open() sem importar `io`, o NameError caia no except e a lista
        #    de vizinhas vinha VAZIA: o portao dizia "ok" sem ter olhado nada.
        #    Portao que engole o proprio erro e pior que portao nenhum.
        mo = re.search(r"<title>(.*?)</title>",
                       open(cam, encoding="utf-8", errors="replace").read(), re.S)
        t = _texto(mo.group(1)) if mo else ""
        if len(t) >= 12 and t != meu_titulo:
            alheios2.append((t, outra))
    corpo_txt = _texto(html)
    achou2 = [(t, d) for t, d in alheios2 if t in corpo_txt]
    if achou2:
        problemas.append("o NOME de outra atividade aparece no texto: %s"
                         % ", ".join('%r (e da %s)' % (t, d) for t, d in achou2[:3]))
    else:
        print("   nome: so o titulo desta atividade aparece no texto (%r)" % meu_titulo)

# ---- 11) FRASE QUE SO EXISTE AQUI E NO MOTOR (aviso, nao reprova)
#   O Marcos perguntou "a atividade nao copiou no fim a de historia?" — e tinha
#   copiado: "a viagem no tempo esta completa" (tela da medalha) e "quem vai
#   viajar no tempo hoje?" (tela de entrada). Nao e prefixo nem titulo: e a
#   HISTORIA da outra atividade sobrando na boca do mascote.
#   Nao da para decidir isto sozinho — "Pode seguir para o proximo conteudo" e
#   mobiliario do motor e DEVE ser igual em todas. O que da para fazer, e ajuda
#   muito, e separar o joio: frase que existe aqui e em UMA outra atividade so
#   (justamente o motor de onde clonei) merece ser lida uma a uma antes de
#   publicar. Frase que existe em tres ou mais e mobiliario.
def _frases(caminho):
    try:
        t = open(caminho, encoding="utf-8", errors="replace").read()
    except Exception:
        return set()
    j = "".join(re.findall(r"<script>(.*?)</script>", t, re.S))
    fora = set()
    for m in re.finditer(r'"((?:[^"\\]|\\.){25,200})"', j):
        x = re.sub(r"<[^>]+>", "", m.group(1))
        x = re.sub(r"&#(\d+);", lambda g: chr(int(g.group(1))), x)
        x = re.sub(r'"\s*\+.*', "", x)
        x = re.sub(r"\s+", " ", x).strip()
        if len(x) < 25: continue
        if re.search(r"[{}();=]|function|http|px|rgba|webkit", x): continue
        if not re.search(r"[a-z\u00e0-\u00fc]{4}", x): continue
        fora.add(x)
    return fora

minhas = _frases(arq)
if minhas:
    raiz3 = os.path.dirname(os.path.abspath(pasta)) or "."
    conta, dono = {}, {}
    for outra in sorted(os.listdir(raiz3)):
        cam = os.path.join(raiz3, outra, "index.html")
        if not e_vizinha(outra) or not os.path.exists(cam): continue
        if os.path.abspath(os.path.dirname(cam)) == os.path.abspath(pasta): continue
        for f in (minhas & _frases(cam)):
            conta[f] = conta.get(f, 0) + 1
            dono[f] = outra
    so_do_motor = sorted(f for f in conta if conta[f] == 1)
    if so_do_motor:
        print("   aviso: %d frase(s) que so existem aqui e em UMA outra atividade "
              "— leia antes de publicar:" % len(so_do_motor))
        for f in so_do_motor[:8]:
            print("      [%s] %s" % (dono[f], f[:96]))
    else:
        print("   frases: nenhuma frase exclusiva do motor sobrou")

# ---- 12) ⭐ O NOME DO MASCOTE DE OUTRA ATIVIDADE
#   Ago/2026, Terra dos Papagaios: a tela de entrada perguntava "Quem vai VOAR
#   COM O NICO hoje?" e o crachá era "de cartógrafo" — o mascote e o papel da
#   CARTOGRAFIA, na primeira tela que a criança vê, numa atividade de História.
#   O relatório do professor ainda trazia o currículo de Geografia do 3º ano
#   inteirinho. Nenhum item anterior pegava: não tem prefixo (item 8), não é o
#   título (item 10) e a frase aparecia em UMA outra atividade só, então caía no
#   AVISO do item 11 — que é para ler, e é fácil não ler.
#   Tentei achar isso por estatística (nome próprio raro aqui e frequente lá) e
#   o resultado foi lixo: "Agora", "Vamos", "Vale", "Terra". Portão que grita à
#   toa ensina a ignorar portão. Então a solução é DECLARAR: cada atividade tem
#   `var MASCOTE_NOME="..."`, e aqui a conta é exata.
mm = re.search(r'var\s+MASCOTE_NOME\s*=\s*"([^"]+)"', html)
meu_masc = _texto(mm.group(1)) if mm else ""
if not meu_masc:
    print("   aviso: esta atividade nao declara `var MASCOTE_NOME` — sem isso eu nao "
          "consigo conferir se o mascote de outra atividade sobrou no texto")
else:
    raiz4 = os.path.dirname(os.path.abspath(pasta)) or "."
    # ⚠️ COMENTARIO NAO CHEGA NA CRIANCA — e este portao existe para o que ela
    #    LE. Sem tirar os comentarios, a propria licao escrita aqui ("foi assim
    #    que 'com o Nico' ficou na tela de outra atividade") reprovava as quatro
    #    atividades de uma vez. Portao que reprova a si mesmo nao serve.
    corpo4 = re.sub(r"/\*.*?\*/", " ", html, flags=re.S)
    corpo4 = re.sub(r"(?m)^\s*//.*$", " ", corpo4)
    corpo4 = _texto(re.sub(r"var\s+MASCOTE_NOME\s*=\s*\"[^\"]+\"", "", corpo4))
    alheios4, gemeos = [], []
    for outra in sorted(os.listdir(raiz4)):
        cam = os.path.join(raiz4, outra, "index.html")
        if not e_vizinha(outra) or not os.path.exists(cam): continue
        if os.path.abspath(os.path.dirname(cam)) == os.path.abspath(pasta): continue
        mo = re.search(r'var\s+MASCOTE_NOME\s*=\s*"([^"]+)"',
                       open(cam, encoding="utf-8", errors="replace").read())
        if not mo: continue
        nome_o = _texto(mo.group(1))
        if nome_o == meu_masc:
            gemeos.append(outra); continue
        if len(nome_o) >= 3 and re.search(r"\b" + re.escape(nome_o) + r"\b", corpo4):
            alheios4.append((nome_o, outra))
    if gemeos:
        problemas.append("o mascote daqui se chama %r, o MESMO nome do mascote de %s "
                         "— clonei o motor e esqueci de trocar o nome"
                         % (meu_masc, ", ".join(gemeos)))
    if alheios4:
        problemas.append("o nome do mascote de OUTRA atividade aparece no texto: %s"
                         % ", ".join("%r (e da %s)" % (n, d) for n, d in alheios4[:3]))
    if not gemeos and not alheios4:
        print("   mascote: so o nome daqui aparece no texto (%r)" % meu_masc)

print("%s -> resto de clone conferido" % pasta)
if not problemas:
    print("   clone ok: nada da atividade de origem sobrou")
    sys.exit(0)
print("   %d RESTO(S) DA ATIVIDADE DE ORIGEM:" % len(problemas))
for p in problemas:
    print("    - %s" % p)
sys.exit(1)
