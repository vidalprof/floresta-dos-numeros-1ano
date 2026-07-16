#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditor de SOM para o padrao AUDIO_TXT + pasta audio/ (padrao novo, ex.: Confeitaria).
O auditar-som.py original valida o padrao do Climas (mapa AUDIO embutido); este valida:
  1) todo valor de AUDIO_TXT aponta p/ um mp3 EXISTENTE (>=800 bytes) ao lado do HTML;
  2) toda fala LITERAL do codigo (falar("..."), falarDepois("..."), ELOGIOS, DIAG,
     STREAK_FALA, UAU_FASE, PARADAS hist/gancho compostas "Uau! ..."/"Parada concluida! ...")
     tem chave em AUDIO_TXT (senao cai no MUDO — informacao so na tela);
  3) zero speechSynthesis como caminho de fala (regra: ZERO voz de navegador).
Uso: python3 _circo/auditar-som-audio-txt.py <pasta>/index.html
"""
import sys, os, re, json

def limparFala(t):
    t=re.sub(r'<[^>]+>',' ',t)
    t=re.sub(r'[_*#~|<>=\[\]{}]',' ',t)
    t=re.sub(r'\bdivisao\b','divisão',t,flags=re.I)
    t=re.sub(r'\bmultiplicacao\b','multiplicação',t,flags=re.I)
    t=re.sub(r'\s+([,.!?:])',r'\1',t)
    t=re.sub(r'\s\s+',' ',t).strip()
    if t and t[-1] not in '.!?:': t+='.'
    return t

def chave(t):
    s=re.sub(r'\s+',' ',t).strip()
    h=5381
    for ch in s: h=((h*33)+ord(ch))&0xffffffff
    if h==0: return 'v0'
    digs='0123456789abcdefghijklmnopqrstuvwxyz';out='';n=h
    while n>0: out=digs[n%36]+out; n//=36
    return 'v'+out

def main():
    if len(sys.argv)<2:
        print(__doc__); sys.exit(2)
    path=sys.argv[1]
    base=os.path.dirname(os.path.abspath(path))
    src=open(path,encoding='utf-8').read()
    problemas=[]

    m=re.search(r'var AUDIO_TXT=(\{.*?\});',src)
    if not m:
        print("REPROVADO: sem mapa AUDIO_TXT"); sys.exit(1)
    AUD=json.loads(m.group(1))
    print("AUDIO_TXT: %d chaves"%len(AUD))

    # 1) arquivos existem
    faltam=[k for k,v in AUD.items() if not os.path.exists(os.path.join(base,v)) or os.path.getsize(os.path.join(base,v))<800]
    for k in faltam: problemas.append("mp3 ausente/pequeno: %s -> %s"%(k,AUD[k]))

    # 2) falas literais do codigo tem chave
    falas=set()
    for mm in re.finditer(r'falar(?:Depois)?\(\s*"((?:[^"\\]|\\.)*)"\s*[,)]',src):
        s=mm.group(1)
        if '"+' in s: continue
        falas.add(s.replace('\\"','"'))
    # arrays de frases fixas
    for nome in ['ELOGIOS','FESTApool']:
        ma=re.search(nome+r'=\[(.*?)\];',src,re.S)
        if ma and nome=='ELOGIOS':
            for x in re.finditer(r'"((?:[^"\\]|\\.)*)"',ma.group(1)): falas.add(x.group(1))
    for nome in ['DIAG','STREAK_FALA']:
        ma=re.search(r'var '+nome+r'=\{(.*?)\};',src,re.S)
        if ma:
            for x in re.finditer(r':\s*"((?:[^"\\]|\\.)*)"',ma.group(1)): falas.add(x.group(1))
    # UAU + ganchos compostos
    ma=re.search(r'var UAU_FASE=\{(.*?)\};',src,re.S)
    uaus={}
    if ma:
        for x in re.finditer(r'(\w+)\s*:\s*"((?:[^"\\]|\\.)*)"',ma.group(1)): uaus[x.group(1)]=x.group(2)
    for u in uaus.values(): falas.add("Uau! "+u)
    for x in re.finditer(r'gancho\s*:\s*"((?:[^"\\]|\\.)*)"',src):
        falas.add("Parada concluída! "+x.group(1))
    for x in re.finditer(r'hist\s*:\s*"((?:[^"\\]|\\.)*)"',src):
        falas.add(x.group(1))

    mudas=[]
    for f in falas:
        k=chave(limparFala(f))
        if k not in AUD: mudas.append((k,f[:70]))
    for k,f in sorted(mudas): problemas.append('fala MUDA (sem chave): %s "%s"'%(k,f))

    # 3) zero voz de navegador
    if re.search(r'speechSynthesis\.speak',src):
        problemas.append("usa speechSynthesis.speak (regra: zero voz de navegador)")

    print("falas literais varridas: %d | mudas: %d | mp3 faltando: %d"%(len(falas),len(mudas),len(faltam)))
    if problemas:
        for p in problemas[:25]: print("  - REPROVA:",p)
        print("== RESUMO SOM(AUDIO_TXT): REPROVADO — %d problema(s) =="%len(problemas)); sys.exit(1)
    print("== RESUMO SOM(AUDIO_TXT): APROVADO ==")

main()
