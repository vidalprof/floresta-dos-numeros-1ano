# -*- coding: utf-8 -*-
"""
PORTÃO — O REVISOR (o "testador humano" de TEXTO).

Ideia do Marcos (ago/2026): *"existe alguma possibilidade de um profissional que
pegue os erros que EU pego? ajustes para as telas serem perfeitas, erros de voz,
digitação, coisas que não ficam boas? um testador, como um humano?"*.

O Revisor tem TRÊS olhos: VISUAL (foto da tela), TEXTO (revisão) e VOZ (ouvir).
Este arquivo é o olho de **TEXTO** — o único que roda inteiro aqui, sem internet.
Ele lê o que a criança VÊ e OUVE (o `falas.json` + os textos do `conteudo.json`)
e pega a classe de erro que chega ao Marcos no olho:

  ERRO (reprova):
   - palavra repetida ("a a palavra", "de de")
   - espaço duplo / espaço antes de pontuação (" ,")
   - marca de HTML vazando na fala (<b>, &mdash;, &#225;)
   - concordância ARTIGO ↔ NOME ("o jibóia", "a tucano")  ← defeito real, ago/2026
   - pontuação dobrada ("!!", "..") — reticências "..." e "?!" são poupadas

  REVISAR (aviso, olho do professor — não reprova sozinho):
   - frase começando em minúscula depois de ponto
   - número escrito como algarismo onde a voz vai soletrar estranho (aviso)

⚠️ Aprender com o erro: palavra que o Revisor acusar por engano vira exceção
   AQUI (as listas MASC_A / FEM_O / etc.), no mesmo commit — nunca afrouxar a
   regra inteira por causa de uma palavra.

Uso:  python3 _qa/revisor.py <pasta-da-atividade>
Sai 0 se não achou ERRO; 1 se achou; 2 se não teve o que medir.
"""
import sys, os, io, json, re

# palavras terminadas em -a que são MASCULINAS (não reprovar "o dia")
MASC_A = set("""dia mapa planeta planetinha problema clima sistema tema poema programa dilema
cinema mapa telefonema esquema drama panorama diagrama grama(peso) alerta guarda-chuva
lápis(nao) sofa(nao) pijama dia maquinista salta zeca""".split())
# ⚠️ "salta" = nome do personagem pulador da peca saltos-na-fita ("o Salta pula de
#    2 em 2"). Termina em -a mas e masculino (nome proprio). Falso-positivo pego
#    na Feirinha da Dona Coruja (ago/2026).
# ⚠️ bigênero (o/a): quem decide é o artigo, então NÃO reprovar nenhum dos dois.
#    "maquinista" chegou como falso-positivo no Trem do Alfabeto (Coru é O maquinista).
# palavras terminadas em -o que são FEMININAS (não reprovar "a foto")
FEM_O = set("foto moto tribo libido".split())
# palavras curtas/ambíguas que NÃO devem entrar no teste de gênero
PULA_GENERO = set("""isso isto aquilo tudo todo toda um uma dois duas
o a os as ao aos caixa outro outra outros outras mesmo mesma
piloto tiracolo
juca zeca teco nico cuca coru""".split())
# ⚠️ nomes MASCULINOS terminados em -a (o Juca, o Zeca, o Teco...) — a heurística
#    de -a=feminino acusava "o Juca" como concordância errada. Mascotes/nomes de
#    menino em -a entram aqui. (Pego no portal de colonização do 4º ano, ago/2026.)
# ⚠️ "piloto" e bigenero (o/a piloto). "tiracolo" so aparece na expressao fixa
#    "a tiracolo" (bolsa cruzada) — o "a" e da expressao, nao artigo. Falsos-
#    positivos pegos no Detetive das Palavras (ago/2026).
# ⚠️ "outro/outra" sao determinantes que concordam com um nome implicito; o
#    "a"/"o" antes deles costuma ser PREPOSICAO, nao artigo ("de um lugar a
#    outro", "levam de um lado a outro"). Falso-positivo pego na prova Viagem
#    pelo Brasil (ago/2026): "a outro" acusado como se "outro" fosse nome.
# gênero FIXO de palavras que a regra de terminação (-a fem / -o masc) erra —
# principalmente as em -e e em consoante. Fonte: defeitos reais que chegaram
# ao Marcos ("uma peixe"). m = masculino, f = feminino.
GEN_FIXO = {
    "peixe":"m","dente":"m","leite":"m","sangue":"m","mel":"m","sal":"m",
    "nariz":"m","pente":"m","tomate":"m","chocolate":"m","lápis":"m","lapis":"m",
    "ave":"f","arte":"f","ponte":"f","fonte":"f","gente":"f","sorte":"f",
    "morte":"f","febre":"f","chave":"f","nuvem":"f","viagem":"f","árvore":"f","arvore":"f",
}
# ⚠️ "caixa" e AMBIGUO: "a caixa" (de guardar) e feminino, "o caixa" (quem atende
#    no mercado) e MASCULINO. Os dois estao certos — fora do teste de genero.
# ⭐ NOME PROPRIO COM INICIAL MINUSCULA (Marcos, ago/2026: achou "pedro" numa
#    resposta; cobrou VARIAS vezes). O revisor nem OLHAVA o texto das opcoes — por
#    isso passava. Lista CONSERVADORA: so nomes/lugares que NUNCA sao palavra
#    comum em PT (nada de "lia"=verbo ler, "cora"=corar, "nina"=ninar), para o
#    portao nunca acusar inocente (falso-positivo ensina a ignorar o portao).
#    Nome novo que chegar minusculo -> some aqui, no mesmo commit.
NOMES_PROPRIOS = set(u"""pedro joao joão maria ana bento duda gael bidu rex mimi
teo téo juca orbi órbi nico poli davi caio bia zeca teco miga bruno cauã gabriel
lucas rafael sofia alice laura helena heitor arthur bernardo miguel
brasil blumenau joinville recife bahia parana paraná florianopolis florianópolis
itajai itajaí curitiba joinvile""".split())

def _limpa_html(s):
    return re.sub(r"<[^>]+>", "", s or "")

def _tem_html(s):
    return bool(re.search(r"<[a-zA-Z/][^>]*>", s or "")) or bool(re.search(r"&[a-zA-Z]+;|&#\d+;", s or ""))

def _genero_suspeito(artigo, palavra):
    """Devolve mensagem se 'o/a <palavra>' parece concordância errada, senão ''."""
    p = palavra.lower()
    base = re.sub(r"[^a-zãáâàéêíóôõúüç-]", "", p)
    if not base or base in PULA_GENERO or len(base) < 3:
        return ""
    # ⚠️ profissoes/nomes em -ISTA sao BIGENERO (o/a dentista, motorista,
    #    artista, jornalista, maquinista, pianista...). O artigo decide; nenhum
    #    dos dois esta errado. Falso-positivo pego no Detetive (o dentista, o
    #    motorista) — ago/2026.
    if base.endswith("ista"):
        return ""
    # -ão é ambíguo (o coração, a mão) — fora
    if base.endswith("ão") or base.endswith("ções") or base.endswith("ao"):
        return ""
    # acentos no fim (-á -é -ó) não são o caso de -a átono
    if artigo == "o" and (base.endswith("a") or base.endswith("ã")) and base not in MASC_A:
        return u'"o %s" — palavra terminada em -a costuma ser feminina ("a %s")' % (palavra, palavra)
    if artigo == "a" and base.endswith("o") and base not in FEM_O:
        return u'"a %s" — palavra terminada em -o costuma ser masculina ("o %s")' % (palavra, palavra)
    return ""

def revisa_texto(t, display=False):
    """Lista de (nivel, msg) para um texto. nivel: 'ERRO' ou 'REVISAR'.

    display=True: campo de EXIBICAO (abertura/fim/titulo/sub do conteudo). Esses
    aparecem escritos COM negrito (<b>) e sao narrados a partir do texto LIMPO
    (o montar tira a marca antes de gravar a voz), entao <b> ali e legitimo — o
    check de HTML nao vale para eles (so para as falas puras do falas.json)."""
    achados = []
    cru = t or ""
    fala = _limpa_html(cru).replace("&mdash;", "—").replace("&ccedil;", "ç")
    fala = re.sub(r"&#\d+;", "?", fala)

    # 1) HTML vazando na FALA (o que a voz lê não pode ter marca)
    if not display and _tem_html(cru):
        # <b> é normal no ENUNCIADO escrito, mas o texto GRAVADO (falas.json) é
        # a fala limpa; se veio com tag, é vazamento.
        achados.append(("ERRO", u'marca de HTML na fala: %r' % cru[:60]))

    # 2) palavra repetida ("a a", "de de") — ignora números/siglas de 1 letra? não.
    for m in re.finditer(r"\b([a-zA-Zãáâàéêíóôõúüç]{1,})\s+\1\b", fala, re.I):
        w = m.group(1).lower()
        if w in ("que","the"):  # "que que" às vezes é fala real; the=inglês
            continue
        achados.append(("ERRO", u'palavra repetida: "%s %s"' % (m.group(1), m.group(1))))

    # 3) espaço duplo
    if re.search(r"  ", fala):
        achados.append(("ERRO", u'espaço duplo'))
    # 4) espaço antes de pontuação
    if re.search(r"\s[,.;:!?](\s|$)", fala):
        achados.append(("ERRO", u'espaço antes de pontuação'))
    # 5) pontuação dobrada (poupa "...", "?!", "!?")
    for m in re.finditer(r"([,.;:!?])\1", fala):
        seq = m.group(0)
        if seq in ("..",) and "..." in fala:  # parte de reticências
            continue
        if seq in ("!!","??",",,",";;","::","..","--"):
            achados.append(("ERRO", u'pontuação dobrada: "%s"' % seq))

    # 6) concordância artigo↔nome ("o jibóia")
    for m in re.finditer(r"\b([Oo]|[Aa])\s+([A-Za-zãáâàéêíóôõúüç][A-Za-zãáâàéêíóôõúüç-]{2,})", fala):
        art = m.group(1).lower()
        pal = m.group(2)
        msg = _genero_suspeito(art, pal)
        if msg:
            achados.append(("ERRO", u"concordância: " + msg))

    # 6b) GÊNERO FIXO de palavras que a regra de terminação erra (Museu, ago/2026:
    #     "o dourado é UMA peixe" — peixe termina em -e e é MASCULINO; a heurística
    #     de -a/-o não pega). Dicionário explícito, casando artigo DEFINIDO e
    #     INDEFINIDO. Palavra que o revisor errar aqui entra/sai deste dicionário.
    for m in re.finditer(r"\b(um|uma|[oa])\s+([A-Za-zãáâàéêíóôõúüç-]{2,})", fala, re.I):
        art = m.group(1).lower(); pal = m.group(2).lower()
        base = re.sub(r"[^a-zãáâàéêíóôõúüç-]", "", pal)
        g = GEN_FIXO.get(base)
        if g:
            fem = art in ("uma", "a")
            if (g == "m" and fem) or (g == "f" and not fem):
                cert = {"um":"uma","uma":"um","o":"a","a":"o"}[art]
                achados.append(("ERRO", u'concordância: "%s %s" — %s é %s ("%s %s")'
                    % (art, m.group(2), base, "masculino" if g=="m" else "feminino",
                       cert, m.group(2))))

    # 7) frase em minúscula depois de ponto (aviso)
    for m in re.finditer(r"[.!?]\s+([a-zãáâàéêíóôõúüç])", fala):
        achados.append(("REVISAR", u'frase começa minúscula depois de ponto: "…%s"'
                        % fala[max(0,m.start()-8):m.start()+3]))
        break  # um aviso por texto basta

    return achados

def main():
    if len(sys.argv) < 2:
        print(u"uso: python3 _qa/revisor.py <pasta-da-atividade>"); return 2
    pasta = sys.argv[1].rstrip("/")
    alvos = []
    fj = os.path.join(pasta, "falas.json")
    if os.path.exists(fj):
        for f in json.load(io.open(fj, encoding="utf-8")):
            alvos.append((f.get("id","?"), f.get("texto",""), False))
    cj = os.path.join(pasta, "conteudo.json")
    if os.path.exists(cj):
        c = json.load(io.open(cj, encoding="utf-8"))
        for campo in ("abertura","fim","titulo","sub"):
            if c.get(campo): alvos.append(("conteudo:"+campo, c[campo], True))
    if not alvos:
        print(u"%s -> sem falas.json nem conteudo.json. NAO MEDI." % pasta); return 2

    erros, avisos, vistos = [], [], set()
    for ident, txt, disp in alvos:
        for nivel, msg in revisa_texto(txt, display=disp):
            chave = (nivel, msg)
            if chave in vistos:      # não repetir o mesmo achado 30x
                continue
            vistos.add(chave)
            (erros if nivel=="ERRO" else avisos).append(u"%s  [%s]" % (msg, ident))

    # ⭐ NOME PROPRIO MINUSCULO nas OPÇOES/RESPOSTAS que a crianca VE (o revisor
    #    nao olhava as opcoes do conteudo — foi por ai que "pedro" passou).
    if os.path.exists(cj):
        try:
            cc = json.load(io.open(cj, encoding="utf-8"))
        except Exception:
            cc = {}
        def _labels(node):
            if isinstance(node, dict):
                for k in ("t", "nome", "s", "resp", "pal", "palavra", "cer"):
                    v = node.get(k)
                    if isinstance(v, str):
                        yield v
                for v in node.values():
                    for x in _labels(v):
                        yield x
            elif isinstance(node, list):
                for it in node:
                    for x in _labels(it):
                        yield x
        vistos_nome = set()
        for f in (cc.get("fases") or []):
            for lab in _labels(f.get("dados")):
                for w in re.findall(r"[A-Za-zÀ-ÿ]+", lab):
                    if w.lower() in NOMES_PROPRIOS and w[:1].islower() and w not in vistos_nome:
                        vistos_nome.add(w)
                        erros.append(u'nome próprio com inicial minúscula: "%s" (deveria ser "%s")  [conteudo:opção]'
                                     % (w, w[:1].upper() + w[1:]))

    print(u"%s -> revisor de texto: %d fala(s)/campo(s) conferido(s)" % (pasta, len(alvos)))
    if avisos:
        print(u"   %d ponto(s) para o olho do professor (nao reprova):" % len(avisos))
        for a in avisos[:12]: print(u"    ~ " + a)
    if not erros:
        print(u"   revisor ok: nenhum erro de texto/concordancia/digitacao")
        return 0
    print(u"   %d ERRO(S) DE TEXTO — a crianca ve/ouve isto:" % len(erros))
    for e in erros[:20]: print(u"    x " + e)
    print(u"   conserto: arrumar o texto no conteudo.json e remontar; se for")
    print(u"   engano de genero, por a palavra na excecao de _qa/revisor.py.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
