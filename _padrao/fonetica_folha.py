# -*- coding: utf-8 -*-
u"""
============================================================
 A PRONÚNCIA DA VOZ — a tabela que a FOLHA VIVA nunca teve

 ⚠️ POR QUE ISTO NASCEU (Marcos, 25/set/2026, urgente): *"na atividade do 5 ano
    aprendendo a ortografia a palavra cigano está sendo dita cigrano"*.
    A palavra está escrita CERTO em todo lugar — no `falas.json`, no quadro, no
    item. Quem erra é a VOZ.

 ⚠️⚠️ E O BURACO ERA ESTRUTURAL, não desta palavra. O motor (`montar.py`) tem a
    `_FONETICA_VOZ` desde ago/2026 — foi ela que consertou "face" virando
    "feice", "sandboard" virando sândiboárdi e o "ilefante" que custou três
    rodadas. **A folha viva nunca recebeu esse mecanismo.** Dezenas de cadernos
    de folha viva no ar não tinham NENHUM jeito de corrigir uma pronúncia sem
    mexer no que a criança lê na tela. Este arquivo é esse jeito.

 COMO FUNCIONA, e o detalhe que não pode ser trocado de ordem:
    O `id` do mp3 sai do TEXTO da tela (é o que casa o áudio com o que a criança
    vê). Então a troca fonética vale **só para o texto que vai ao TTS**, aplicada
    DEPOIS de o id já existir: o arquivo continua com o nome do texto original,
    mas o áudio sai com a pronúncia certa. Mexer no `texto` do `falas.json`
    mudaria o id e a criança ouviria silêncio — o pior defeito que existe,
    porque não deixa marca (lição dos portões 1p/1q).

 ⚠️ UMA FONTE DE VERDADE: as palavras que o motor já conserta são importadas
    dele. Regra escrita duas vezes é regra que desencontra — foi assim que 17
    palavras ficaram mudas no 2º ano.
============================================================
"""
from __future__ import print_function

import os
import re
import sys

# ------------------------------------------------------------------
# 1. O que o MOTOR já conserta — importado, nunca recopiado.
# ------------------------------------------------------------------
_DO_MOTOR = []
try:
    _aqui = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(_aqui, "ESQUELETO"))
    import montar as _montar                       # noqa: E402
    _DO_MOTOR = list(getattr(_montar, "_FONETICA_VOZ", []))
except Exception as _e:                            # pragma: no cover
    # ⚠️ Se o motor não importar aqui (o `entregar.yml` roda com o mínimo
    #    instalado), NÃO se inventa uma cópia da tabela dele: segue só com as
    #    trocas próprias da folha viva, e o aviso sai impresso. Melhor consertar
    #    menos do que consertar com uma cópia que vai desencontrar amanhã.
    print(u"fonetica_folha: nao consegui ler a tabela do motor (%s)" % _e)


# ------------------------------------------------------------------
# 2. O que é da FOLHA VIVA
#    ⚠️ Sempre em minúsculas fonéticas: caixa alta empurra a voz a soletrar.
# ------------------------------------------------------------------
_DA_FOLHA = [
    # ⚠️ Marcos ouviu (25/set/2026), no caderno da ortografia do 5º ano:
    #    *"a palavra cigano está sendo dita cigrano"* — a voz enfia um R depois
    #    do G. O acento circunflexo fixa a sílaba tônica fechada (ci-GÂ-no) e
    #    tira a margem de a voz "inventar" o encontro consonantal.
    #    A TELA continua escrevendo CIGANO, que é a grafia que a folha ensina —
    #    e ainda bem, porque o caderno é justamente de ortografia.
    (re.compile(u"\\bciganos\\b", re.I | re.U), u"cigânos"),
    (re.compile(u"\\bcigano\\b", re.I | re.U), u"cigâno"),
]

TABELA = _DO_MOTOR + _DA_FOLHA


def aplica(texto):
    u"""Devolve o texto COMO A VOZ DEVE LER. Só para o TTS — nunca para a tela."""
    t = texto or u""
    for rx, sub in TABELA:
        t = rx.sub(sub, t)
    return t


def mudou(texto):
    u"""True quando esta fala tem pronúncia corrigida (serve ao portão)."""
    return aplica(texto) != (texto or u"")


if __name__ == "__main__":
    print(u"%d troca(s): %d do motor + %d da folha viva"
          % (len(TABELA), len(_DO_MOTOR), len(_DA_FOLHA)))
    for t in (u"cigano.", u"Isso! Cigano. Nao existe nenhuma palavra.",
              u"os ciganos", u"CIGANO", u"cigarra"):
        print(u"   %-46s -> %s" % (t, aplica(t)))
