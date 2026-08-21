#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""
============================================================
VER A DINÂMICA FUNCIONANDO ANTES DE CLONAR — e copiar igual

⚠️ NASCEU DE UMA PERGUNTA DO MARCOS (ago/2026), e ela apontou o buraco exato:
   *"foi feita a pesquisa das dinâmicas, mas nessas pesquisas dizem como
   programar? você verifica ela funcionando da fonte que você buscou para clonar
   igual? Interessante seria você ver ela funcionando e copiar igual, isso iria
   economizar tempo com menos erros"*.

**A resposta honesta era NÃO.** As pesquisas dizem o que a mecânica ENSINA e o
que observar — não dizem como programar. Quem diz onde está o código bom é o
`_padrao/DINAMICAS.md`. Só que, na hora de usar, eu **abria o arquivo, LIA a
função e reescrevia adaptando**. Nunca abria a fase da origem para VER
funcionando. E é na adaptação que o defeito nasce: some uma linha de guarda,
troca-se um nome de classe, esquece-se a terceira porta do toque.

ESTE PROGRAMA FAZ O QUE ELE PEDIU, em um comando:
  1. lê o `_padrao/DINAMICAS.md` e descobre em QUAL atividade mora a versão boa;
  2. abre aquela fase no navegador e **joga**: clica, arrasta, escreve;
  3. salva as fotos (`_padrao/_fonte/<mecanica>/`) e imprime o que ela faz;
  4. imprime a FUNÇÃO INTEIRA da fase, pronta para copiar — com os ajudantes que
     ela chama, para não sobrar chamada órfã.

⚠️ A regra que fica: **copiar é COPIAR**. Trocar só os dados e os ids de voz.
   Se a função nova ficar com menos linhas que a de origem, alguma guarda foi
   perdida no caminho — e guarda perdida é defeito na mão da criança.

Uso:  python3 _padrao/ver_fonte.py arrastar
      python3 _padrao/ver_fonte.py ligar --so-codigo
============================================================
"""
import io
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


def onde_mora(mecanica):
    u"""lê a tabela do DINAMICAS.md e devolve (pasta, dica da fase, armadilhas)"""
    cam = os.path.join(AQUI, u"DINAMICAS.md")
    if not os.path.exists(cam):
        return None
    for linha in io.open(cam, encoding=u"utf-8"):
        if not linha.startswith(u"|"):
            continue
        col = [c.strip() for c in linha.strip().strip(u"|").split(u"|")]
        if len(col) < 4:
            continue
        nome = re.sub(r"[*`]", u"", col[0]).lower()
        if mecanica.lower() not in nome:
            continue
        fonte = col[1]
        pasta = re.search(r"`(_\w+)`", fonte)
        fase = re.search(r'"([^"]+)"', fonte)
        return (pasta.group(1) if pasta else None,
                fase.group(1) if fase else None,
                col[3])
    return None


def acha_funcao(html, pista):
    u"""acha a funcao da fase. ⚠️ procurar o titulo solto pelo arquivo falhava
    (o selo usa entidade, maiuscula, acento). O caminho que nao mente e o
    `FASES_MESTRE`: ele casa o NOME da funcao com o titulo que o professor le."""
    js = u"".join(re.findall(r"<script>(.*?)</script>", html, re.S))

    def corpo_de(nome):
        m = re.search(r"^function\s+" + re.escape(nome) + r"\s*\(", js, re.M)
        if not m:
            return None
        ini = js.find(u"{", m.end())
        prof, k = 0, ini
        while k < len(js):
            if js[k] == u"{":
                prof += 1
            elif js[k] == u"}":
                prof -= 1
                if prof == 0:
                    break
            k += 1
        return js[m.start():k + 1]

    if pista:
        chave = re.sub(r"[^A-Za-z ]", u"", pista).strip().upper()[:12]
        for f, tit in re.findall(r'\["(\w+)","([^"]*)"\]', js):
            limpo = re.sub(r"&#\d+;", u"", tit)
            limpo = re.sub(r"[^A-Za-z ]", u"", limpo).strip().upper()
            if chave and chave in limpo:
                c = corpo_de(f)
                if c:
                    return (f, c)
    return None


def ajudantes(corpo, js):
    u"""quais funções de fora esta fase chama (para não sobrar chamada órfã)"""
    chamadas = set(re.findall(r"\b([a-zA-Z_$][\w$]*)\s*\(", corpo))
    de_fora = []
    for c in sorted(chamadas):
        if re.search(r"^function\s+" + re.escape(c) + r"\s*\(", js, re.M):
            de_fora.append(c)
    return de_fora


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    mec = sys.argv[1]
    so_codigo = u"--so-codigo" in sys.argv

    achado = onde_mora(mec)
    if not achado:
        print(u"nao achei '%s' na tabela do _padrao/DINAMICAS.md." % mec)
        print(u"mecanica nova? entao ela ENTRA na tabela no mesmo commit.")
        return 2
    pasta, fase, armadilhas = achado
    print(u"=== %s ===" % mec.upper())
    print(u"a versao boa mora em: %s%s" % (pasta or u"(nao dito)",
                                           u"  fase \"%s\"" % fase if fase else u""))
    print(u"armadilhas ja pagas: %s" % armadilhas)

    if not pasta:
        return 2
    cam = os.path.join(RAIZ, pasta, u"index.html")
    if not os.path.exists(cam):
        print(u"a pasta %s nao existe aqui." % pasta)
        return 2
    html = io.open(cam, encoding=u"utf-8").read()
    js = u"".join(re.findall(r"<script>(.*?)</script>", html, re.S))
    alvo = acha_funcao(html, fase)
    if not alvo:
        print(u"NAO MEDI: nao consegui localizar a funcao da fase pelo titulo.")
        return 2
    nome, corpo = alvo
    print(u"funcao: %s  (%d linhas)" % (nome, corpo.count(u"\n") + 1))
    aj = [a for a in ajudantes(corpo, js) if a != nome]
    print(u"ajudantes que ela chama: %s" % u", ".join(aj[:14]))

    if not so_codigo:
        # 2) VER FUNCIONANDO: abre a fase da ORIGEM e joga nela
        dest = os.path.join(AQUI, u"_fonte", mec)
        if not os.path.isdir(dest):
            os.makedirs(dest)
        js_teste = os.path.join(dest, u"ver.js")
        io.open(js_teste, u"w", encoding=u"utf-8").write(u"""
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const fs=require('fs'),path=require('path');
(async()=>{
  const orig=process.argv[2], fase=process.argv[3], dest=process.argv[4];
  const tmp=path.join(dest,'palco.html');
  let h=fs.readFileSync(orig,'utf8');
  h=h.replace('</body>','<script>window.addEventListener("load",function(){setTimeout(function(){try{'+fase+'();}catch(e){document.title="ERRO:"+e.message;}},220);});</script></body>');
  fs.writeFileSync(tmp,h);
  const b=await chromium.launch({args:['--no-sandbox']});
  const p=await b.newPage({viewport:{width:640,height:940}});
  await p.goto('file://'+tmp); await p.waitForTimeout(2600);
  await p.screenshot({path:path.join(dest,'1-entrada.png'),fullPage:true});
  const antes=await p.evaluate(()=>document.body.innerHTML.length);
  // toca no primeiro alvo clicavel da fase e fotografa a REACAO
  const clicou=await p.evaluate(()=>{
    const a=[...document.querySelectorAll('.tela .opt,.tela .lig,.tela .peca,.tela .tec,.tela .bin,.tela .pal,.tela .mcarta,.tela .cel')]
      .filter(e=>e.getBoundingClientRect().height>0);
    if(!a.length) return null; a[0].click(); return a[0].className;
  });
  await p.waitForTimeout(900);
  await p.screenshot({path:path.join(dest,'2-depois-do-toque.png'),fullPage:true});
  const depois=await p.evaluate(()=>document.body.innerHTML.length);
  console.log(JSON.stringify({clicou:clicou, mudou: depois!==antes}));
  await b.close();
})();
""")
        r = subprocess.run([u"node", js_teste, cam, nome, dest],
                           capture_output=True, text=True, cwd=RAIZ)
        print(u"vendo funcionar: %s" % (r.stdout or r.stderr).strip()[:200])
        print(u"fotos em %s" % dest)

    print(u"")
    print(u"--- COPIE DAQUI (troque SO os dados e os ids de voz) ---")
    print(corpo)
    print(u"--- ate aqui ---")
    print(u"⚠️ se a sua versao ficar MENOR que esta, alguma guarda se perdeu.")
    return 0


if __name__ == u"__main__":
    sys.exit(main())
