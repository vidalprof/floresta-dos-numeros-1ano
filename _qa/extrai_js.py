# -*- coding: utf-8 -*-
u"""Extrai o JS embutido de um index.html (só <script> SEM src) e grava num .js,
para o `node --check` conferir a sintaxe. Uso: python3 _qa/extrai_js.py <html> <out.js>
Nasceu do PORTÃO PRÉ-ENTREGA (entregar.yml): heredoc de Python dentro do YAML
quebrava o arquivo, então a extração virou este helper reutilizável."""
import re, sys

if len(sys.argv) < 3:
    print("uso: extrai_js.py <index.html> <saida.js>")
    sys.exit(2)
h = open(sys.argv[1], encoding="utf-8").read()
blocos = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", h, re.S)
open(sys.argv[2], "w", encoding="utf-8").write("\n;\n".join(blocos))
