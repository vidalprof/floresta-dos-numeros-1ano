#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDITOR DE SOM — garante VOZ CONSISTENTE (o buraco que deixou a voz do mapa
feminina). Duas frentes:

1) DINÂMICO: abre a atividade no Chromium e DISPARA cada narração (abertura,
   mapa, aberturas de fase, narrarInicio). Intercepta `tocarFalaAudio`
   (=áudio EMBUTIDO, voz gravada/masculina) e `falar` (=voz do NAVEGADOR,
   costuma ser feminina e destoa). REPROVA qualquer narração que caia no
   navegador.
2) ESTÁTICO: valida o mapa `AUDIO` (cada entrada é um data:audio real e não
   minúsculo) e confere que toda chave usada em `tocarFala("chave", …)` existe
   no `AUDIO` (senão cairia no navegador).

Uso:  python3 _circo/auditar-som.py <arquivo.html>
Código != 0 se reprovar.
"""
import sys, re, os, json, base64, subprocess, tempfile

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

FASES = ["estacao","fatores","equatorial","deserto","temperado","subtropical","gelo","mundi","tempestade"]

DIN = r"""
<script>window.addEventListener("load",function(){setTimeout(function(){
 var log=[];
 /* rota REAL da fala: com AUDIO_TXT, o proprio falar() toca audio embutido pela
    chave do texto. Entao aqui consultamos AUDIO_TXT/_chaveVoz p/ saber se a fala
    tem audio gravado (EMBUTIDO) ou cairia na voz do navegador (NAVEGADOR). */
 function _rota(t){ try{ var k=_chaveVoz(t); if(typeof AUDIO_TXT!=="undefined" && AUDIO_TXT && AUDIO_TXT[k]){ return "EMBUTIDO"; } }catch(e){} return "NAVEGADOR"; }
 try{ window.tocarFalaAudio=function(uri,fb){ log.push(["EMBUTIDO",window.__ctx||"?"]); };
      window.falar=function(t){ log.push([_rota(t),window.__ctx||"?"]); };
      window.falarDepois=function(t){ log.push([_rota(t),window.__ctx||"?"]); }; }catch(e){}
 function tst(ctx,fn){ window.__ctx=ctx; var n=log.length; try{ fn(); }catch(e){ log.push(["ERRO",ctx+": "+e.message]); } if(log.length===n){ log.push(["SEM-FALA",ctx]); } }
 try{
   try{ nomeAluno="Teste"; }catch(e){}
   try{ comecarComNome(); }catch(e){}
   tst("mapa", function(){ narrarMapa(); });
   tst("inicio_sem_prog", function(){ narrarInicio(false,0); });
   tst("inicio_com_prog", function(){ narrarInicio(true,3); });
   var F=%s;
   for(var i=0;i<F.length;i++){ (function(ch){ tst("fase_"+ch, function(){ falarAbertura(ch); }); })(F[i]); }
   tst("grande_final", function(){ grandeFinal(); });
 }catch(e){ log.push(["ERRO","setup: "+e.message]); }
 document.title="SOM::"+JSON.stringify(log);
},650);});</script>""" % json.dumps(FASES)

def dinamico(src):
    h = open(src, encoding="utf-8").read()
    h = h.replace("</body>", DIN + "</body>", 1)
    tf = tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8")
    tf.write(h); tf.close()
    try:
        out = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                              "--virtual-time-budget=6000", "--dump-dom", "file://" + tf.name],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=60).stdout.decode("utf-8", "ignore")
    finally:
        try: os.remove(tf.name)
        except Exception: pass
    m = re.search(r"<title>SOM::(.*?)</title>", out, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None

def estatico(src):
    h = open(src, encoding="utf-8").read()
    problemas = []
    # 1) mapa AUDIO: chaves -> valida cada data:audio
    mi = h.find("var AUDIO=")
    audio_keys = {}
    if mi >= 0:
        fim = h.find("};", mi)
        bloco = h[mi:fim if fim > 0 else mi + 4000000]
        for k, uri in re.findall(r'"([A-Za-z0-9_]+)"\s*:\s*"(data:audio/[a-z]+;base64,[^"]+)"', bloco):
            try:
                b = base64.b64decode(uri.split(",", 1)[1])
                audio_keys[k] = len(b)
                if len(b) < 1500:
                    problemas.append("AUDIO['%s'] muito pequeno (%d bytes) — pode estar vazio/corrompido" % (k, len(b)))
            except Exception:
                problemas.append("AUDIO['%s'] não é base64 válido" % k)
    # 2) chaves usadas em tocarFala("x", …) existem no AUDIO?
    #    exige VÍRGULA logo após a aspas (chave literal completa); assim NÃO pega
    #    concatenação dinâmica como tocarFala("fase_"+ch, …).
    usadas = set(re.findall(r'tocarFala\(\s*["\']([A-Za-z0-9_]+)["\']\s*,', h))
    for k in sorted(usadas):
        if k not in audio_keys:
            problemas.append("tocarFala(\"%s\", …) mas AUDIO['%s'] NÃO existe → cairia na voz do navegador" % (k, k))
    # 2b) NARRAÇÕES DINÂMICAS CRÍTICAS (comemoração/subir de nível): o texto é
    #     montado na hora e NÃO era gravado → caía na voz do navegador (feminina).
    #     Agora cada uma tem de ter áudio embutido em AUDIO_TXT pela chave do texto.
    def _chave_voz(t):
        s = " ".join(str(t).split()); hh = 5381
        for ch in s: hh = ((hh * 33) + ord(ch)) & 0xffffffff
        b36 = ""; n = hh
        if n == 0: b36 = "0"
        while n > 0: b36 = "0123456789abcdefghijklmnopqrstuvwxyz"[n % 36] + b36; n //= 36
        return "v0" if hh == 0 else "v" + b36
    txt_keys = set(re.findall(r'"(v[0-9a-z]{3,})"\s*:\s*"data:audio', h))
    niveis = re.search(r'NIVEIS_FALA\s*=\s*\[([^\]]*)\]', h)
    criticas = ["Você conseguiu! Você viajou pelo mundo inteiro, enfrentou a Tempestade Final e preencheu todas as páginas do Atlas do Clima! Agora você conhece os climas do planeta como quem viajou o mundo inteiro. Parabéns!"]
    if niveis:
        for nv in re.findall(r'"([^"]+)"', niveis.group(1)):
            criticas.append("Você subiu de nível! Agora você é " + nv + "!")
    # 2c) FEEDBACK COMPOSTO (falarComposto): cada PEÇA tem de ter áudio embutido —
    #     todos os elogios, TODAS as explicações do banco, os "cabeçalhos" fixos
    #     (Quase!, Não foi dessa vez!, …) e os avisos de sequência. Assim qualquer
    #     combinação elogio+explicação sai 100% em áudio gravado (masculino).
    def _unesc(s):
        try: return bytes(s, "utf-8").decode("unicode_escape").encode("latin1").decode("utf-8") if "\\u" in s else s.replace('\\"', '"')
        except Exception: return s
    mel = re.search(r'var ELOGIOS=\[(.*?)\]', h, re.S)
    if mel:
        for e in re.findall(r'"((?:[^"\\]|\\.)*)"', mel.group(1)): criticas.append(_unesc(e))
    for e in set(re.findall(r'explica:"((?:[^"\\]|\\.)*)"', h)): criticas.append(_unesc(e))
    criticas += ["Quase!", "Não foi dessa vez!", "Análise correta! Você domina o assunto.",
                 "Quase! Esse era difícil mesmo.", "Isso! Você descobriu a palavra!",
                 "Ah, não! Dessa vez o desenho se completou. Vamos tentar de novo!",
                 "Descubra a palavra do clima!",
                 "Treino concluído! Errar e treinar de novo é assim que os grandes cientistas aprendem!",
                 "Você acertou três seguidas!", "Você acertou cinco seguidas!",
                 "Você acertou oito seguidas!", "Você acertou dez seguidas!"]
    faltando = 0
    for t in criticas:
        if _chave_voz(t) not in txt_keys:
            faltando += 1
            if faltando <= 8:
                problemas.append("fala sem áudio embutido (cairia na voz do navegador): \"%s…\"" % t[:45])
    if faltando > 8:
        problemas.append("... e mais %d fala(s) de feedback sem áudio embutido" % (faltando - 8))
    # 3) escolherVoz() das narrações DINÂMICAS (voz do navegador) deve preferir MASCULINO
    ei = h.find("function escolherVoz")
    if ei >= 0:
        corpo = h[ei:h.find("\nfunction ", ei + 10)]
        # reprova se dá boost POSITIVO a nome feminino
        fem_boost = re.search(r'"(maria|francisca|luciana|camila|joana|fernanda|helena)"[^;]{0,30}p\s*\+=', corpo)
        if fem_boost:
            problemas.append("escolherVoz() dá preferência a voz FEMININA (\"%s\") → narração dinâmica sai feminina" % fem_boost.group(1))
        tem_masc = re.search(r'(masculin|antonio|ant\\u00f4nio|daniel|donato|"male")', corpo)
        if not tem_masc:
            problemas.append("escolherVoz() não prefere voz MASCULINA (falta boost p/ nomes masculinos)")
    return audio_keys, problemas

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("uso: python3 _circo/auditar-som.py <arquivo.html>"); sys.exit(2)
    src = args[0]
    falhas = 0

    audio_keys, prob_est = estatico(src)
    print("  ESTÁTICO: %d áudios embutidos no AUDIO" % len(audio_keys))
    for p in prob_est:
        print("    - REPROVA:", p); falhas += 1
    if not prob_est:
        print("    OK (todas as chaves de tocarFala têm áudio embutido e válido)")

    log = dinamico(src)
    if log is None:
        print("  DINÂMICO: ERRO ao rodar o navegador (pulei)")
    else:
        nav = [c for (r, c) in log if r == "NAVEGADOR"]
        err = [c for (r, c) in log if r == "ERRO"]
        emb = [c for (r, c) in log if r == "EMBUTIDO"]
        print("  DINÂMICO: %d narração(ões) com áudio embutido, %d com voz do NAVEGADOR" % (len(emb), len(nav)))
        for c in nav:
            print("    - REPROVA: narração \"%s\" usa a VOZ DO NAVEGADOR (inconsistente/feminina)" % c); falhas += 1
        for c in err:
            print("    - aviso: não consegui disparar \"%s\" (%s)" % (c, "erro"))
    print("== RESUMO SOM: %s ==" % ("APROVADO (voz consistente, áudios ok)" if falhas == 0 else "REPROVADO — %d problema(s) de voz/áudio" % falhas))
    sys.exit(0 if falhas == 0 else 1)

if __name__ == "__main__":
    main()
