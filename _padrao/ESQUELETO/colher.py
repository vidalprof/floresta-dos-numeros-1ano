#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""COLHE AS FALAS QUE SÓ EXISTEM JOGANDO — e fecha o pilar sonoro.

O `falas.json` sai do `conteudo.json`, e isso resolve tudo o que está escrito
no conteúdo. Mas a peça monta frases **em tempo de jogo**, com pedaços que só
existem ali:

    "Achou as <b>" + PAL.length + "</b> palavras da horta!"
    "<b>" + (w.ac || w.p) + "</b> — era essa mesmo!"

O montador não tem como saber que "Achou as 4 palavras da horta!" vai aparecer
na tela — o número vem do próprio jogo. E foi exatamente isso que a banca
mediu: *"16 perguntas que mudam na tela sem mudar a voz — quem não lê aperta o
alto-falante e ouve outra coisa"*.

A saída não é adivinhar: é **JOGAR e anotar**. O auditor-jogador já atravessa a
atividade inteira e já sabe colher todo texto que aparece (`COLHEITA=`). Aqui a
colheita dele vira `falas.json`:

    montar → colher (joga e anota) → montar de novo → gravar a voz

⚠️ NÃO é opcional numa entrega. Sem este passo, as telas de fecho de rodada e as
   respostas de segunda volta ficam MUDAS, e a criança que ainda não lê perde
   justamente o retorno do acerto.

Uso:  python3 _padrao/ESQUELETO/colher.py <pasta>
      python3 _padrao/ESQUELETO/colher.py <pasta> --so-ver
"""
import io
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)

from montar import (chave_voz, eh_fala, texto_limpo,          # noqa: E402
                    _fonetica_voz, _desentidade_voz)


def texto_comparavel(s):
    u"""O MESMO texto, na forma em que o `falas.json` o guarda.

    ⚠️ LIÇÃO PAGA (set/2026, Bancada da Divisão) — e das piores, porque era um
    LAÇO SEM FIM. A banca reprovava a atividade dizendo que duas frases apareciam
    na tela sem voz:

        + Bem-vindo à oficina! ... a gente REPARTE com as mãos.
        + Três algarismos: comece pelas CENTENAS e desça.

    Só que a voz das duas ESTAVA gravada (`gi_abertura.mp3`, `gi_f19_intro.mp3`)
    e a criança ouvia. O que ninguém via é que o montador passa TODA fala por
    `_fonetica_voz(_desentidade_voz(...))` antes de guardá-la: ele baixa a caixa das palavras em
    maiúscula (senão a voz SOLETRA "C-E-N-T-E-N-A-S"), tira o travessão (que a
    voz arrastava), tira o "(va-ca)"... Ou seja, o `falas.json` guarda
    `centenas` onde a tela escreve `CENTENAS`, e `material dourado placas` onde
    a tela escreve `material dourado — placas`. **De propósito.** E a colheita
    comparava as duas formas letra a letra.

    Por isso a cura não é "ignorar a caixa": é passar os dois lados pela MESMA
    função que gerou o texto guardado. Ignorar só a caixa consertava a frase das
    centenas e deixava a da abertura acusada — foi o que aconteceu na primeira
    tentativa, e o portão continuou pedindo uma voz que já existia.

    O estrago não é só o susto: rodar o colher NÃO resolvia. Ele criava uma fala
    `op_<hash>` para o texto em maiúscula, o montador regerava o `falas.json` do
    `conteudo.json` e a fala sumia — e na banca seguinte a acusação voltava
    igual. Portão que acusa inocente e que não dá para calar ensina a ignorar
    portão, que é o pior que pode acontecer com um portão.

    A cura é comparar na MESMA forma em que a fala foi guardada."""
    return _fonetica_voz(_desentidade_voz(texto_limpo(s)))


def joga_e_anota(pasta, voltas=6, secas=2):
    u"""roda o auditor-jogador em modo colheita e devolve o que ele viu.

    ⚠️ UMA PASSADA NAO BASTA, e a segunda colheita provou: sobraram justamente
    as DICAS DO ANDAIME — "uma das cartas fala de semente", "vou abrir este par
    para voce". Elas so aparecem para quem ERRA varias vezes, e numa partida de
    sorte o jogador nao erra o bastante. E e a crianca que erra quem MAIS precisa
    da voz: sem isso, quem esta perdida e justamente quem fica sem ajuda falada.

    Entao ele joga de novo ate DUAS partidas inteiras nao trazerem nada de novo.
    Nao e "rodei uma vez e deu": e "rodei mais duas vezes inteiras e nao apareceu
    mais nada".

    ⚠️ E por que DUAS: as dicas do andaime SORTEIAM qual par revelar ("uma das
    cartas fala de chuva", "...de abelha"). Cada partida trazia uma frase nova, e
    uma unica rodada seca podia ser so falta de sorte. Duas seguidas ja e sinal
    de que o baralho de frases acabou. O teto de 6 partidas existe para a
    entrega nao ficar refem de um sorteio infeliz."""
    # ⚡ AS PARTIDAS SAO INDEPENDENTES — ENTAO VAO JUNTAS. Em fila, seis partidas
    #    de 32 fases levavam uns doze minutos; e o Marcos pediu que o processo
    #    fosse "bem mais agil". Cada partida escreve no SEU arquivo (senao uma
    #    sobrescreve a colheita da outra) e no fim tudo se junta.
    juntos = {}

    def uma(n):
        saco = os.path.join(pasta, "_colheita%d.json" % n)
        if os.path.exists(saco):
            os.remove(saco)
        r = subprocess.run(["node", os.path.join(RAIZ, "_qa", "jogador.js"),
                            os.path.join(pasta, "index.html")],
                           env=dict(os.environ, COLHEITA=saco), cwd=RAIZ,
                           capture_output=True, text=True)
        fim = [l for l in (r.stdout or "").splitlines()
               if "CHEGOU NO FIM" in l or "PRESO" in l]
        d = {}
        if os.path.exists(saco):
            d = json.load(io.open(saco, encoding="utf-8"))
            os.remove(saco)
        return fim, d

    import concurrent.futures as cf
    # ⚠️ LIÇÃO PAGA (container apertado, ago/2026): TRÊS partidas de jogador ao
    #    mesmo tempo (cada uma percorre a atividade inteira no Chromium) estouram
    #    o container e a colheita morre SEM imprimir — e derruba o pai junto (o
    #    `; echo EXIT` nem roda). É o mesmo defeito do jogador paralelo que já
    #    tinha derrubado a banca. Agora o teto de partidas simultâneas segue o
    #    QA_MAX_PAR (mesmo botão da banca): runner folgado fica em 3 (rápido),
    #    container apertado põe QA_MAX_PAR=1 e roda em fila (lento, mas TERMINA).
    try:
        _PAR = max(1, int(os.environ.get("QA_MAX_PAR", "3")))
    except ValueError:
        _PAR = 3
    antes, seco, rodada = -1, 0, 0
    while rodada < voltas:
        lote = min(_PAR, voltas - rodada)       # QA_MAX_PAR de cada vez
        with cf.ThreadPoolExecutor(max_workers=lote) as ex:
            for k, (fim, d) in enumerate(ex.map(uma, range(rodada, rodada + lote))):
                for l in fim:
                    print(u"   partida %d: %s" % (rodada + k + 1, l.strip()))
                for cx in ("op", "bal"):
                    juntos.update(d.get(cx) or {})
        rodada += lote
        agora = len(juntos)
        print(u"   %d texto(s) vistos ate agora" % agora)
        if agora == antes:
            seco += 1
            if seco >= 1:      # um LOTE inteiro sem nada novo ja e sinal
                print(u"   um lote inteiro de partidas sem nada novo — fechada")
                break
        else:
            seco = 0
        antes = agora
    if not juntos:
        print(u"   o jogador nao deixou colheita — a atividade abriu?")
    return juntos


COLAGEM = re.compile(
    u"^([A-ZÀ-Ú])\\1"                       # "BBOLO": o cracha da letra + a palavra
    u"|[A-ZÀ-Ú]{2,}[a-zà-ú]"                # "BOLOja": palavra em caixa colada na proxima
    u"|[a-zà-ú][A-ZÀ-Ú]{2,}"                # "paoPAO": frase colada num rotulo
    # ⚠️ SEGUNDA LICAO (ago/2026), vista quando o jogador passou a percorrer a
    #    atividade inteira: existe colagem que NAO muda a caixa — ela junta no
    #    PONTO FINAL. Veio assim: "As outras tres terminam com o mesmo som.e
    #    esta" (a frase da fase + o rotulo "e esta", de outro canto da tela).
    #    Escrita de verdade nao tem ponto final grudado em minuscula. As
    #    reticencias ficam de fora ("vazio...vem me ajudar" e uma frase so).
    u"|[^.][.!?][a-zà-ú]", re.UNICODE)


def eh_colagem(t):
    u"""⚠️ LICAO PAGA (ago/2026): a colheita trouxe SETE falas assim —
    *"BBOLOjá tentamos"*, *"LLEITEjá tentamos"*, *"MMELjá tentamos"*...

    Não é texto: é o `textContent` de um pai que juntou DOIS filhos que na tela
    estão separados — o crachá da letra ("B"), a palavra ("BOLO") e o aviso de
    outro canto ("já tentamos"). Na tela a criança lê três coisas distintas; no
    texto colhido vira uma palavra que não existe.

    Se isso passa, o Edge TTS grava a bobagem e a criança que aperta o
    alto-falante ouve **"bêbolojá tentamos"** — exatamente o tipo de defeito
    que o Marcos cobra como "a voz não diz o que está escrito", e o pior: no 1º
    ano, quem ainda não lê acredita na voz.

    A marca da colagem é a MUDANÇA DE CAIXA SEM ESPAÇO. Palavra em caixa alta
    grudada em minúscula (ou o contrário) não acontece em frase escrita para
    criança; acontece quando dois elementos viram um texto só.
    """
    return bool(COLAGEM.search(t or ""))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    pasta = sys.argv[1].rstrip("/")
    so_ver = "--so-ver" in sys.argv
    cam = os.path.join(pasta, "falas.json")
    if not os.path.exists(cam):
        print(u"nao achei %s — rode o montador antes" % cam)
        return 2

    falas = json.load(io.open(cam, encoding="utf-8"))
    ja = set(f["id"] for f in falas)
    # ⚠️ e tambem pelo TEXTO: a mesma frase escrita no conteudo e vista em jogo
    #    nao pode virar dois mp3 (dinheiro e tempo de gravacao a toa)
    ja_txt = set(texto_comparavel(f["texto"]) for f in falas)

    print(u"COLHEITA — %s" % pasta)
    # ⚡ CONFERIR E COLHER NAO CUSTAM O MESMO (ago/2026, medido).
    #    O modo de COLHER precisa das seis partidas: as dicas do andaime
    #    sorteiam de que carta falam, e so a repeticao esgota o baralho de
    #    frases. Ja o modo de CONFERIR (`--so-ver`, o que a BANCA usa) tem
    #    outra pergunta: "sobrou alguma?". Para isso duas partidas bastam —
    #    o que falta de forma SISTEMATICA aparece na primeira; o que e sorteado
    #    ja foi recolhido pelas duas voltas de colheita do processo.
    #    Media: a banca inteira caiu de 11m12 para o tempo dos outros portoes.
    #    Se um dia isso deixar passar alguma, o conserto e subir este numero —
    #    e nao fingir que a banca e o lugar de colher.
    vistos = joga_e_anota(pasta, voltas=(2 if so_ver else 6))

    novas = []
    descartadas = []
    for txt in sorted(vistos):
        t = texto_limpo(txt)
        if not eh_fala(t) or texto_comparavel(t) in ja_txt:
            continue
        if eh_colagem(t):
            descartadas.append(t)
            continue
        ident = "op_" + chave_voz(t)
        if ident in ja:
            continue
        ja.add(ident)
        ja_txt.add(t)
        novas.append({"id": ident, "texto": t})

    print(u"   %d texto(s) vistos em jogo | %d fala(s) novas a gravar"
          % (len(vistos), len(novas)))
    if descartadas:
        print(u"   %d descartada(s) por COLAGEM de elementos (nao sao frases):"
              % len(descartadas))
        for d in descartadas[:6]:
            print(u"      x %s" % d[:64])
    # ⚠️ LICAO PAGA (ago/2026): as duas listas sairam GRUDADAS — as descartadas
    #    e, logo abaixo, as novas, com o mesmo recuo e sem titulo. Eu li a
    #    minha propria saida e conclui que frases boas estavam sendo jogadas
    #    fora. Relatorio que se deixa ler errado custa o mesmo que medicao
    #    errada: leva a consertar o que nao esta quebrado.
    if novas:
        print(u"   as %d FALA(S) A GRAVAR (aparecem na tela e nao tem voz):"
              % len(novas))
    for n in novas[:8]:
        print(u"      + %s" % n["texto"][:74])
    if not novas:
        print(u"   nada a acrescentar: a voz ja cobre o que aparece jogando")
        return 0
    if so_ver:
        # ⚠️⚠️ LICAO PAGA (ago/2026), e e a mesma da casa inteira: PORTAO QUE
        #    NAO REPROVA NAO E PORTAO, E COMENTARIO. O `--so-ver` e o modo que a
        #    BANCA usa (portao 0f2, "a voz da rodada") — e ele saia com ZERO
        #    mesmo listando 32 falas sem voz. A banca lia "ok" e seguia.
        #    Descoberto junto com o jogador cego: enquanto ele parava na 3a
        #    fase, a lista vinha vazia e o defeito nao aparecia. Consertado o
        #    jogador, a lista encheu — e o portao continuou aprovando.
        #    Agora: no modo de CONFERIR, fala faltando REPROVA. O caminho e o
        #    que ja esta escrito no processo: rodar o colher SEM `--so-ver`
        #    (ele grava no falas.json) e montar de novo.
        print(u"   (--so-ver: nada foi escrito)")
        print(u"   ⛔ FALTA VOZ para %d fala(s) que a crianca VE na tela."
              % len(novas))
        print(u"      rode:  python3 _padrao/ESQUELETO/colher.py %s"
              % os.path.basename(pasta))
        print(u"      e depois o montador de novo (o VOZOK sai do falas.json).")
        return 1

    falas.extend(novas)
    io.open(cam, "w", encoding="utf-8").write(
        json.dumps(falas, ensure_ascii=False, indent=1))
    print(u"   %s atualizado. AGORA RODE O MONTADOR DE NOVO" % cam)
    print(u"   (e o `VOZOK` do index.html sai do falas.json — sem isso o "
          u"alto-falante nao aparece)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
