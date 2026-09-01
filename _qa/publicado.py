#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""PORTÃO "COMMITADO ≠ PUBLICADO" — avisa conserto preso no repo.

Cobrança/lição paga (Marcos, set/2026): a prova de matemática foi CORRIGIDA e
commitada, mas eu ESQUECI de publicar. No ar continuou a versão velha, e eu ainda
disse que estava publicado. O erro é bobo e invisível: `git status` fica limpo
(está tudo commitado), então nada grita — só a criança na escola vê a versão
antiga.

Este portão fecha esse buraco. Para cada atividade que JÁ foi publicada por
workflow (tem um `_status/entrega-<repo>.json`), ele compara:

  • a data do ÚLTIMO COMMIT DE CONTEÚDO que tocou a pasta da atividade
    (ignora os commits do próprio Entregador — "audio: vozes que faltavam" e
     "entrega: recado do que foi ao ar" — que fazem parte da publicação);
  • contra o `quando` gravado no `_status` (a hora em que o site confirmou).

Se o commit de conteúdo é MAIS NOVO que a última publicação, o conserto está
PRESO no repo, sem ir ao ar — e o portão AVISA, com o comando pronto para
publicar.

Roda de graça (só git + leitura de arquivo), no início da sessão (chamado pelo
`.claude/hooks/sync-remoto.sh`) e antes de dizer "está no ar".

Uso:  python3 _qa/publicado.py            # avisa (exit 0, informativo)
       python3 _qa/publicado.py --estrito  # exit 1 se houver algo não publicado
Saída sempre lista o que está pendente; --estrito é para CI/portão duro.
"""
import io
import json
import os
import re
import subprocess
import sys
import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# quem publica é o workflow: os commits dele NÃO contam como "conteúdo novo".
AUTORES_ROBO = {u"Entregador", u"github-actions", u"github-actions[bot]"}


def _epoch_iso(s):
    u"""'2026-09-01T12:01:02Z' -> epoch (int). Tolera +00:00 e sem Z."""
    s = (s or "").strip()
    if not s:
        return None
    s = s.replace("Z", "+00:00")
    try:
        return int(datetime.datetime.fromisoformat(s).timestamp())
    except Exception:
        return None


def _ultimo_commit_conteudo(pasta):
    u"""epoch do último commit que tocou `pasta` e NÃO é do robô de publicação.
    Devolve (epoch, sha, assunto) ou (None, None, None)."""
    try:
        r = subprocess.run(
            ["git", "-C", RAIZ, "log", "-n", "40", "--format=%ct%x09%an%x09%h%x09%s",
             "--", pasta],
            capture_output=True, text=True, timeout=20)
    except Exception:
        return (None, None, None)
    if r.returncode != 0:
        return (None, None, None)
    for linha in r.stdout.splitlines():
        partes = linha.split("\t", 3)
        if len(partes) < 4:
            continue
        ct, autor, sha, assunto = partes
        if autor.strip() in AUTORES_ROBO:
            continue
        # os commits do robô às vezes vêm com outro nome; a MENSAGEM os denuncia.
        if re.match(r"^(audio: vozes|entrega: recado|Atualiza a atividade|fotos: baixa)", assunto):
            continue
        try:
            return (int(ct), sha, assunto)
        except ValueError:
            return (None, None, None)
    return (None, None, None)


def main():
    estrito = "--estrito" in sys.argv
    stdir = os.path.join(RAIZ, "_status")
    if not os.path.isdir(stdir):
        print(u"publicado: nao ha _status/ (nada publicado por workflow ainda).")
        return 0

    pendentes, conferidas, sem_data = [], 0, []
    for nome in sorted(os.listdir(stdir)):
        m = re.match(r"^entrega-(.+)\.json$", nome)
        if not m:
            continue
        try:
            d = json.load(io.open(os.path.join(stdir, nome), encoding="utf-8"))
        except Exception:
            continue
        pasta = (d.get("pasta") or "").strip().strip("/")
        destino = (d.get("destino") or m.group(1)).strip()
        quando = _epoch_iso(d.get("quando"))
        if not pasta or not os.path.isdir(os.path.join(RAIZ, pasta)):
            continue                      # pasta sumiu/renomeou — não é deste portão
        if quando is None:
            sem_data.append((pasta, destino))
            continue
        commit_ct, sha, assunto = _ultimo_commit_conteudo(pasta)
        if commit_ct is None:
            continue
        # margem de 90s: o commit de conteúdo pode ser segundos antes do carimbo
        # na MESMA publicação; só é "preso" quando é claramente mais novo.
        if commit_ct > quando + 90:
            pendentes.append({
                "pasta": pasta, "destino": destino, "sha": sha, "assunto": assunto,
                "commit": datetime.datetime.utcfromtimestamp(commit_ct).strftime("%Y-%m-%d %H:%M"),
                "publicado": datetime.datetime.utcfromtimestamp(quando).strftime("%Y-%m-%d %H:%M"),
            })
        else:
            conferidas += 1

    if pendentes:
        print(u"⛔ CONSERTO PRESO NO REPO — commitado mas NAO publicado:")
        for p in pendentes:
            print(u"   • %s -> %s" % (p["pasta"], p["destino"]))
            print(u"       ultimo conteudo: %s (%s \"%s\")" % (p["commit"], p["sha"], p["assunto"][:50]))
            print(u"       ultima publicacao: %s  <-- MAIS VELHA" % p["publicado"])
        alvos = ",".join("%s:%s" % (p["pasta"], p["destino"]) for p in pendentes)
        print(u"   PUBLIQUE (workflow entregar.yml, input alvos):")
        print(u"       %s" % alvos)
        print(u"   (o site so troca depois disso; ate la a crianca ve a versao velha.)")
        print(u"   ⚠️ ressalva: este carimbo so e atualizado pelo entregar.yml. Se")
        print(u"      voce publicou por atualizar.yml/republicar-limpo.yml (espelho),")
        print(u"      o carimbo fica velho e isto pode ser FALSO ALARME — confirme.")
    if sem_data:
        print(u"   ~ %d _status sem 'quando' (nao da p/ comparar): %s"
              % (len(sem_data), ", ".join(d for _, d in sem_data)))
    if not pendentes:
        print(u"✅ publicado: as %d atividade(s) publicadas estao com a versao do repo no ar."
              % conferidas)
        return 0
    return 1 if estrito else 0


if __name__ == "__main__":
    sys.exit(main())
