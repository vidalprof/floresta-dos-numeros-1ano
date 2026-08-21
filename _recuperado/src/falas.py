#!/usr/bin/env python3
# Enumera as falas fixas da Confeitaria, calcula a chave (igual ao JS _chaveVoz(limparFala))
# e gera: (a) lote.json p/ o gerar-audio.yml  (b) audio_map.json {chave: "audio/<chave>.mp3"}
import re, json

def limparFala(t):
    t=re.sub(r'<[^>]+>'," ",str(t))
    t=re.sub(r'[_*#~|<>=\[\]{}]'," ",t)
    t=re.sub(r'\bdivisao\b',"divisão",t,flags=re.I); t=re.sub(r'\bmultiplicacao\b',"multiplicação",t,flags=re.I)
    t=re.sub(r'\s+([,.!?:])',r'\1',t); t=re.sub(r'\s\s+'," ",t); t=t.strip()
    if t and t[-1] not in ".!?:": t+="."
    return t
def base36(n):
    if n==0: return "0"
    d="0123456789abcdefghijklmnopqrstuvwxyz"; s=""
    while n>0: s=d[n%36]+s; n//=36
    return s
def chave(t):
    s=re.sub(r'\s+'," ",limparFala(t)).strip()
    h=5381
    for ch in s: h=((h*33)+ord(ch))&0xFFFFFFFF
    return "v"+base36(h)

PAR=[
 dict(ch="p1",tipo="repartir",modo=None,hist="Bem-vindo à Confeitaria Mágica! Sou o Chef Confeito. Nossa 1ª tarefa: repartir os biscoitos em partes iguais nos pratos. Repartir igual é dividir!",
   gancho="Ótimo! Agora vamos ver quantas caixas cabem os doces.",des=[(6,2),(8,4),(10,5),(12,3),(9,3),(15,5)]),
 dict(ch="p2",tipo="repartir",modo="caixas",hist="Agora o contrário do prato: quantas caixas dá pra encher? Se cada caixa leva um tanto, quantas caixas cabem?",
   gancho="Show! Chegou um pedido grande pra festa. Vamos ler o problema.",des=[(12,6),(15,5),(20,4),(18,3),(14,7),(24,8)]),
 dict(ch="p3",tipo="escolha",hist="Chegaram os pedidos da Festa da Cidade! Leia cada situação e descubra a divisão certa.",
   gancho="Você é rápido! Agora um segredo dos confeiteiros: multiplicar e dividir são contrários.",
   en=["A festa tem 4 mesas. O Chef fez 20 brigadeiros para repartir igualmente. Quantos em cada mesa?","São 24 biscoitos em 6 sacolinhas iguais. Quantos biscoitos por sacolinha?","A dona tem 18 docinhos e dá 3 para cada criança. Para quantas crianças dá?","São 30 balas em 5 potes iguais. Quantas balas por pote?","Há 16 fatias de bolo, 2 para cada visitante. Para quantos visitantes?","São 21 pães em 3 cestas iguais. Quantos pães por cesta?"]),
 dict(ch="p4",tipo="escolha",hist="Segredo da receita: a divisão é o contrário da multiplicação! Se você sabe a de vezes, sabe a de dividir.",
   gancho="Boa memória! Que tal um joguinho pra descansar?",
   en=["3 bandejas com 4 biscoitos cada dão 12. Então 12 ÷ 4 = ?","5 caixas com 6 doces cada dão 30. Então 30 ÷ 6 = ?","Se 7 × 3 = 21, quanto é 21 ÷ 7?","Se 6 × 8 = 48, quanto é 48 ÷ 8?","Se 4 × 9 = 36, quanto é 36 ÷ 4?","Se 8 × 5 = 40, quanto é 40 ÷ 5?"]),
 dict(ch="j1",tipo="memoria",hist="Vira as cartas e junte cada conta de vezes com a divisão do contrário que dá o mesmo doce!",
   gancho="Que memória boa! Agora vamos calcular de cabeça, usando a tabuada."),
 dict(ch="p5",tipo="tabuada",hist="Pra dividir de cabeça, pense na tabuada: divisor vezes quanto dá o dividendo? A vitrine te ajuda!",
   gancho="Rápido como um confeiteiro! Agora o desafio: é de multiplicar ou de repartir?",des=[(24,6),(35,7),(42,6),(48,8),(27,9),(56,7)]),
 dict(ch="p6",tipo="escolha",hist="Cuidado agora: em cada pedido, decida se é pra JUNTAR grupos iguais (multiplicar) ou REPARTIR em partes iguais (dividir).",
   gancho="Você pensa como um mestre! Vamos montar a conta certa no próximo jogo.",
   en=["Cada caixa tem 8 doces. São 4 caixas. Quantos doces ao todo?","São 32 doces repartidos em 4 caixas iguais. Quantos por caixa?","6 amigos comeram 3 biscoitos cada. Quantos biscoitos ao todo?","São 18 biscoitos repartidos entre 6 amigos. Quantos para cada um?","5 bandejas com 7 cupcakes cada. Quantos cupcakes ao todo?","São 35 cupcakes em 5 bandejas iguais. Quantos por bandeja?"]),
 dict(ch="j2",tipo="montar",hist="Arraste os números para montar a divisão certa. Lembre: na divisão a ordem importa!",
   gancho="Perfeito! Agora, e quando não dá pra repartir tudo igual? Sobra!",des=[(24,6),(20,5),(18,3),(40,8),(30,6)]),
 dict(ch="p7",tipo="resto",hist="Nem sempre dá pra repartir tudo igual. O que não dá é o RESTO! Diga quanto fica em cada e quanto sobra.",
   gancho="Você entendeu o resto! Falta só a grande encomenda final.",des=[(13,4,3,1),(17,5,3,2),(22,4,5,2),(10,3,3,1),(19,6,3,1),(25,7,3,4)]),
 dict(ch="p8",tipo="escolha",hist="A encomenda final da festa! Números maiores: reparta as dezenas e depois as unidades. Você consegue!",
   gancho="Você conseguiu! A Festa da Cidade vai ser um sucesso!",
   en=["48 ÷ 4 = ?","36 ÷ 3 = ?","60 ÷ 5 = ?","84 ÷ 4 = ?","55 ÷ 5 = ?","72 ÷ 6 = ?"]),
]
falas=set()
falas.add("Oi! Eu sou o Chef Confeito. Preciso da sua ajuda pra preparar os doces da Festa da Cidade, e tudo tem que ser repartido em partes iguais! Escreva seu nome e toque em começar.")
falas.add("Quase! Pense de novo, com calma. Você consegue!")
falas.add("Sem pressa! Vou te ajudar. Olha com calma e tenta de novo.")
falas.add("Ache os pares! Junte cada conta de vezes com a divisão do contrário que dá o mesmo doce.")
falas.add("Par certo!")
falas.add("Você acertou tudo! Quer encarar um desafio extra, um pouquinho mais difícil?")
falas.add("Vamos treinar juntos, com calma, pra você fixar. Você consegue!")
falas.add("Muito bem! Agora você fixou.")
for p in PAR:
    falas.add(p["hist"]); falas.add("Parada concluída! "+p["gancho"])
    if p["tipo"]=="escolha":
        for e in p["en"]: falas.add(e)
    if p["tipo"]=="repartir":
        for tot,gr in p["des"]:
            if p.get("modo")=="caixas": falas.add("Temos "+str(tot)+" doces. Cada caixa leva "+str(gr)+". Quantas caixas dá pra encher?")
            else: falas.add("Reparta "+str(tot)+" biscoitos igualmente em "+str(gr)+" pratos. Quantos em cada prato?")
    if p["tipo"]=="tabuada":
        for d,v in p["des"]: falas.add(str(d)+" dividido por "+str(v)+". Use a tabuada do "+str(v)+".")
    if p["tipo"]=="resto":
        for d,v,q,s in p["des"]: falas.add(str(d)+" doces em "+str(v)+" pratos iguais. Quantos em cada prato?")
    if p["tipo"]=="montar":
        for d,v in p["des"]: falas.add("Monte a divisão certa: "+str(d)+" repartido em "+str(v)+" partes.")

lote=[]; amap={}
for t in falas:
    k=chave(t); amap[k]="audio/"+k+".mp3"; lote.append({"id":k,"texto":limparFala(t)})
json.dump(lote,open("_novo/lote_audio.json","w"),ensure_ascii=False)
json.dump(amap,open("_novo/audio_map.json","w"),ensure_ascii=False)
print(len(lote),"falas ->", "_novo/lote_audio.json / audio_map.json")
