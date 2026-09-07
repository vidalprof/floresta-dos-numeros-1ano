# -*- coding: utf-8 -*-
u"""Despeja a tabela fonetica do montador (`_FONETICA_VOZ`) como JSON, para os
portoes em JavaScript aplicarem a MESMA troca antes de comparar tela x voz.

Por que existe (set/2026, Solidos): o montador grava "face" como "fásse" — so no
audio, a tela continua "face". Os portoes 0g (`vozigual.js`) e 0n
(`fala_o_escrito.js`) tiram acento e comparam letras: "fasse" != "face" e acusavam
6 defeitos numa atividade certa. A tabela e UMA (a do montar.py); aqui ela so e
lida, nunca copiada — copiar seria a segunda fonte de verdade que um dia diverge.

Saida: [[padrao, flags, substituto], ...] — `padrao` e a regex Python (as que a
tabela usa sao simples e valem em JS: \\b, \\s*, [\\s-]*), `flags` e "i" quando
re.I. Uso: python3 _qa/fonetica_dump.py
"""
import io, json, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "_padrao", "ESQUELETO"))
import montar  # noqa: E402  (tem guarda __main__; importar nao monta nada)

saida = []
for rx, sub in montar._FONETICA_VOZ:
    saida.append([rx.pattern, "i" if (rx.flags & re.I) else "", sub])
sys.stdout.write(json.dumps(saida, ensure_ascii=False))
