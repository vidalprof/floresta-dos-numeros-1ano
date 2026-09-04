# -*- coding: utf-8 -*-
u"""
PORTÃO DO WORKFLOW — "o bash dos passos compila?"

NASCEU DE UM ERRO MEU, duas vezes no mesmo dia (set/2026). Ao plugar portões
novos no `entregar.yml` eu editei o `run:` de um passo e deixei um `if` VAZIO:

    if [ -f "$pasta/conteudo.json" ]; then
    fi

O YAML continuava válido — para o YAML aquilo é só uma string. O GitHub aceitou,
rodou, e o passo morreu em 51 segundos com "syntax error near unexpected token
`fi'". A publicação do conserto ficou parada até eu ir olhar o log.

E antes disso, no mesmo arquivo, eu já tinha escrito uma função de portão que o
`bash -e` matava por dentro. Duas vezes o mesmo padrão: **o YAML valida, o bash
não** — e ninguém conferia o bash.

O que ele faz: abre cada workflow, pega o `run:` de cada passo e roda
`bash -n` nele. É a mesma pergunta que o `node --check` faz no JS da atividade,
só que para a esteira. Barato, instantâneo, e teria poupado as duas paradas.

⚠️ Ele não executa nada: só confere que o script COMPILA. Erro de lógica
(chamar portão que não existe, variável vazia) continua por conta dos testes.

Uso:  python3 _qa/workflow_bash.py [arquivo.yml ...]   (sem argumento: todos)
Sai 0 se todos compilam, 1 se algum não, 2 se não deu para medir.
"""
import glob, os, subprocess, sys, tempfile

try:
    import yaml
except ImportError:
    print(u"NAO MEDI: falta o pyyaml"); sys.exit(2)


def confere(arqs):
    ruins, medidas = [], 0
    for a in arqs:
        try:
            y = yaml.safe_load(open(a, encoding="utf-8"))
        except Exception as e:
            ruins.append((a, "(o YAML nem carrega)", str(e)[:120])); continue
        if not isinstance(y, dict):
            continue
        for job in (y.get("jobs") or {}).values():
            if not isinstance(job, dict):
                continue
            for passo in (job.get("steps") or []):
                run = passo.get("run")
                if not run or not isinstance(run, str):
                    continue
                # shell explícito que não seja bash/sh: não é nosso caso
                sh = (passo.get("shell") or "bash").split()[0]
                if sh not in ("bash", "sh"):
                    continue
                medidas += 1
                nome = passo.get("name") or "(sem nome)"
                with tempfile.NamedTemporaryFile("w", suffix=".sh",
                                                 delete=False, encoding="utf-8") as f:
                    # `set -e` como o GitHub usa: `bash -e {0}`
                    f.write("set -e\n" + run)
                    cam = f.name
                r = subprocess.run(["bash", "-n", cam], capture_output=True)
                os.unlink(cam)
                if r.returncode:
                    ruins.append((os.path.basename(a), nome,
                                  r.stderr.decode("utf-8", "replace").strip()[:200]))

    if not medidas:
        print(u"NAO MEDI: nenhum passo com `run:` de bash"); return 2
    if ruins:
        print(u"-> %d passo(s) com BASH QUEBRADO (de %d conferidos):" % (len(ruins), medidas))
        for arq, nome, err in ruins:
            print(u"    ✗ %s / %s" % (arq, nome))
            for l in err.splitlines()[:3]:
                print(u"         %s" % l)
        print(u"   (o YAML valida mesmo assim — para ele o `run:` e so texto)")
        return 1
    print(u"-> workflows ok: %d passo(s) de bash, todos compilam." % medidas)
    return 0


if __name__ == "__main__":
    arqs = sys.argv[1:] or sorted(glob.glob(".github/workflows/*.yml") +
                                  glob.glob(".github/workflows/*.yaml"))
    if not arqs:
        print(u"NAO MEDI: nao achei workflows"); sys.exit(2)
    sys.exit(confere(arqs))
