# -*- coding: utf-8 -*-
u"""
============================================================
 PORTÃO DO ARQUIVO INVISÍVEL — "existe no disco, não existe no git"

 ⚠️⚠️ LIÇÃO PAGA (set/2026), e da pior espécie: silenciosa.

 Eu fui commitar um arquivo novo e o git respondeu **"nothing to commit,
 working tree clean"** — com o arquivo ali, na minha frente. Cheguei a dizer ao
 Marcos que o trabalho estava salvo. Não estava.

 A CAUSA: o arquivo **`.git/info/exclude`** tinha duas linhas — `_padrao/` e
 `_trem/` — marcando como ignoradas duas pastas do CORAÇÃO do projeto. Esse
 arquivo é local, não vai para o git, não aparece em revisão nenhuma e ninguém
 pensa em olhar para ele. E ele só afeta arquivo NOVO: os já rastreados seguem
 funcionando, o que faz tudo parecer normal.

 O QUE ESTAVA FORA DO GIT quando eu descobri:
   · `_padrao/pecas/divisao-dourado.html` (46 KB) — a mecânica inteira da
     Bancada da Divisão, e justamente o arquivo que eu precisava editar naquele
     momento para atender um pedido dele;
   · mais três peças-fonte (`arranjo`, `quociente-parcial`, `resto`);
   · o `sw.js` do Trem.

 As mecânicas FUNCIONAVAM nas atividades publicadas, porque já estavam
 compiladas dentro do `pecas.js` (esse sim versionado). O que não existia era a
 FONTE. E esta máquina é descartável: um reinício e a regra da casa ("conserte
 na peça-fonte, NUNCA no gerado") viraria impossível — sobraria engenharia
 reversa em cima de um arquivo gerado de 1,9 MB.

 O que este portão cobra:
   1. **Nenhuma pasta do projeto (`_*/`) escondida no `.git/info/exclude`.**
      ⚠️ O `.gitignore` NÃO conta: ele é commitado, visível e revisado, e o que
      está lá é decisão da casa (saída de workflow, cache). Tratar os dois igual
      foi o erro da 1ª versão deste portão — ela cuspiu 138 reprovações
      legítimas, que é como um portão vira ruído e acaba desligado.
   2. **Toda peça-fonte de mecânica** (`_padrao/pecas/*.html`) rastreada pelo
      git. Peça que existe só no disco é peça que vai sumir.
   3. **Todo `conteudo.json` e todo `index.html` de atividade** rastreado.
   4. Avisa sobre qualquer outro arquivo não rastreado em pasta de projeto
      (fora o lixo conhecido: `__pycache__`, `.pyc`, saída de workflow).

 ⚠️ O QUE ELE NÃO PEGA: arquivo que foi commitado e depois apagado, e arquivo
 que está no git mas nunca foi publicado — para esse segundo caso existe o
 carimbo do `_status/` e o aviso de "conserto preso no repo".

 Uso:  python3 _qa/invisivel.py
 Sai 0 se está tudo visível, 1 se há trabalho fora do git, 2 se não deu para medir.
============================================================
"""
import io
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

# lixo de verdade: pode e deve ficar fora do git
LIXO = ("__pycache__", ".pyc", ".DS_Store", "Thumbs.db", "node_modules",
        "/build/", "/fetched/", ".origem.txt")


def _git(*args):
    return subprocess.check_output(["git"] + list(args), cwd=RAIZ).decode("utf-8", "replace")


def _e_lixo(caminho):
    return any(x in caminho for x in LIXO)


def confere():
    if not os.path.isdir(os.path.join(RAIZ, ".git")):
        print(u"NAO MEDI: nao e um repositorio git")
        return 2

    problemas, avisos = [], []

    # ⚠️ A DISTINÇÃO QUE FAZ ESTE PORTÃO PRESTAR (e que eu errei na 1ª versão):
    #    · `.gitignore` é COMMITADO, visível e revisado — o que está lá é uma
    #      DECISÃO da casa (saída de workflow, cache, node_modules). Não é
    #      problema, e reprovar isso só gera ruído até alguém desligar o portão.
    #    · `.git/info/exclude` é LOCAL: não vai para o git, ninguém revisa, não
    #      aparece em lugar nenhum. É ele que esconde trabalho sem avisar.
    #    A primeira versão deste arquivo tratava os dois igual e cuspiu 138
    #    reprovações — o defeito exato que eu mandei a banca evitar.
    exc = os.path.join(RAIZ, ".git", "info", "exclude")
    if os.path.exists(exc):
        for n, ln in enumerate(io.open(exc, encoding="utf-8", errors="replace").read().splitlines(), 1):
            t = ln.strip()
            if not t or t.startswith("#") or t.startswith("**"):
                continue
            alvo = t.rstrip("/")
            if alvo.startswith("_") and os.path.isdir(os.path.join(RAIZ, alvo)):
                problemas.append(
                    u".git/info/exclude:%d esconde a pasta do projeto `%s`. Esse "
                    u"arquivo e LOCAL: nao vai para o git e ninguem o revisa. "
                    u"Arquivo NOVO ali vira invisivel — o git diz \"working tree "
                    u"clean\" e o trabalho fica so no disco desta maquina, que e "
                    u"descartavel." % (n, alvo))

    # o que existe no disco e o git nao rastreia
    try:
        soltos = [x for x in _git("ls-files", "--others", "--exclude-standard").splitlines()
                  if x.strip() and not _e_lixo(x)]
    except Exception as e:                       # noqa: BLE001
        print(u"NAO MEDI: o git nao respondeu (%s)" % e)
        return 2

    escondidos = []
    for x in soltos:
        alvo = (x.startswith("_padrao/pecas/") or x.endswith("/conteudo.json")
                or x.endswith("/index.html") or x.startswith("_qa/"))
        (problemas if alvo else avisos).append(
            u"%s: `%s` nao esta no git." % (u"FORA DO GIT" if alvo else u"solto", x))

    print(u"invisivel -> %d arquivo(s) fora do git, %d escondido(s) por regra local"
          % (len(soltos), len(escondidos)))

    if avisos:
        print(u"   avisos (%d):" % len(avisos))
        for a in avisos[:8]:
            print(u"    - %s" % a)

    if problemas:
        print(u"   REPROVOU (%d):" % len(problemas))
        for p in problemas:
            print(u"    - %s" % p)
        return 1

    print(u"   tudo o que e do projeto esta no git")
    return 0


if __name__ == "__main__":
    sys.exit(confere())
