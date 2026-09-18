# -*- coding: utf-8 -*-
u"""
============================================================
 IDENTIDADE PRÓPRIA DE CADA CADERNO DE FOLHA VIVA — cor, capa e animação.

 ⚠️ POR QUE EXISTE — ordem do Marcos, 18/set/2026, com a turma na frente:
    *"cada caderno precisa ter capa diferente, cor diferente animações etc, pois
    são muito parecidos e os estudantes acham que é a mesma atividade, mesmo o
    título sendo diferente"*. Medido no dia: 23 cadernos em DUAS cores (14 roxos
    `#6d5ae6`, 9 telha `#b0562a`) e duas capas.

 O QUE ESTE SCRIPT FAZ, para cada pasta da tabela ESPEC abaixo:
   1. troca a COR do caderno (tokens `--cor/--cor2/--corclara` ou, nos cadernos
      antigos sem token, os literais roxos) pela cor escolhida PELO ASSUNTO;
   2. substitui o bloco de CSS da capa (do `.capa{` ao `#fim,#retomar{`) por uma
      CENA do assunto — mecanismo + adereço + figuras do próprio caderno — com
      `@keyframes` de NOME PRÓPRIO (sufixo da pasta: nome de keyframe é global e
      já apagou um título inteiro por colisão);
   3. reescreve o `f0` do `folhas.js` (a capa), mantendo o NOME e o SUBTÍTULO
      que já estavam lá.
   Depois: `node --check`, `_qa/css_fechado.py`, `_qa/cor_fixa.py`,
   `_qa/css_atregra.py`, `_qa/identidade.py` e `_padrao/versionar.py`.

 REGRAS QUE ELE CUMPRE SOZINHO (e falha alto se não conseguir):
   · cor com contraste >= 4,5:1 sobre branco (o botão tem letra branca);
   · nenhuma cor repetida entre duas pastas;
   · toda figura citada existe em `<pasta>/img/`;
   · nenhum emoji, nenhum SVG na tela da criança (só CSS e PNG das folhas);
   · tinta ESCRITA no `.sub` e no `.chamada` (a capa pinta o próprio fundo —
     `_qa/cor_fixa.py`), e `prefers-reduced-motion` desliga tudo.

 Uso: python3 _padrao/identidade_capa.py <pasta> [<pasta> ...]
      python3 _padrao/identidade_capa.py --todos
============================================================
"""
from __future__ import print_function
import io
import json
import os
import re
import sys


# ---------------------------------------------------------------- cores
def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexa(t):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(v)))) for v in t)


def escurece(h, f=0.72):
    return hexa([v * f for v in rgb(h)])


def clareia(h, f=0.88):
    return hexa([v + (255 - v) * f for v in rgb(h)])


def lum(h):
    def c(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb(h)
    return 0.2126 * c(r) + 0.7152 * c(g) + 0.0722 * c(b)


def contraste_branco(h):
    return 1.05 / (lum(h) + 0.05)


# ---------------------------------------------------------------- a tabela
# pasta: cor (pelo ASSUNTO) · cena (mecanismo) · figs (arquivos em img/, sem .png)
# · rot (rótulo sob cada figura, opcional) · letra (como o título entra) · fundo
ESPEC = {
    "_abc1":   dict(cor="#d32f2f", cena="desfile", letra="pula",
                    figs=["ab_abelha", "ab_bola", "ab_casa", "ab_dado", "ab_estrela"], rot=["A", "B", "C", "D", "E"],
                    fundo=("#fde3e3", "#fff7f7"), nota="o desfile: as figuras marcham no tapete, uma letra em cada uma"),
    "_alfa1":  dict(cor="#00838f", cena="esteira", letra="desliza",
                    figs=["al_bola", "al_bolo", "al_boneca", "al_bota"], rot=["BOLA", "BOLO", "BONECA", "BOTA"],
                    fundo=("#d9f2f4", "#f6fdfd"), nota="a fábrica: esteira com roletes girando e as palavras saindo"),
    "_casa1":  dict(cor="#b0562a", cena="rua", letra="cai",
                    figs=["mo_casa", "mo_iglu", "mo_oca", "mo_palafita", "mo_castelo"], rot=None,
                    fundo=("#cbe7f7", "#fdf3ea"), nota="a rua do mundo: casas vizinhas sob o sol — é o tema DESTE caderno, os outros é que a emprestavam"),
    "_fra1":   dict(cor="#2e7d32", cena="tecla", letra="pula",
                    figs=["fr_bola", "fr_sol", "fr_pato"], rot=None,
                    fundo=("#dff3e0", "#f7fcf7"), nota="a tecla de espaço afundando e as palavras pulando separadas"),
    "_ing8":   dict(cor="#8d6e00", cena="balcao", letra="desliza",
                    figs=["lf_suitcase", "lf_mouse", "lf_tea", "lf_music"], rot=None,
                    fundo=("#f3ead0", "#fdfaf1"), nota="o balcão de achados e perdidos com as etiquetas penduradas balançando"),
    "_ini1":   dict(cor="#bf360c", cena="brota", letra="cresce",
                    figs=["in_bola", "in_bolo", "in_boneca", "in_bota", "in_boca"], rot=["BO", "BO", "BO", "BO", "BO"],
                    fundo=("#fbe2d8", "#fff8f5"), nota="a família: as palavras que começam igual brotam da mesma terra"),
    "_jogo1":  dict(cor="#8e5572", cena="rola", letra="gira",
                    figs=["jg_dado", "jg_pipa", "jg_bola", "jg_peixe"], rot=None,
                    fundo=("#f2e2ea", "#fbf5f8"), nota="o grande jogo: o dado rola e as peças pulam no tabuleiro"),
    "_let1":   dict(cor="#1565c0", cena="vira", letra="vira",
                    figs=["le_bola", "le_bota", "le_gato", "le_pato", "le_mala", "le_mola"], rot=["BOLA", "BOTA", "GATO", "PATO", "MALA", "MOLA"],
                    fundo=("#dbe8fa", "#f5f9ff"), nota="a letra que muda tudo: cartas que viram e trocam UMA letra"),
    "_mont1":  dict(cor="#8d6e63", cena="junta", letra="desliza",
                    figs=["mo_bola", "mo_gato", "mo_pipa", "mo_sino"], rot=["BO·LA", "GA·TO", "PI·PA", "SI·NO"],
                    fundo=("#ece3df", "#faf7f6"), nota="a máquina de juntar: os dois pedaços deslizam e se encaixam"),
    "_mult2":  dict(cor="#33691e", cena="brota", letra="cresce",
                    figs=["ho_morango", "ho_laranja", "ho_maca", "ho_pera", "ho_melancia"], rot=None,
                    fundo=("#e4f1d8", "#f8fcf4"), nota="a horta: as frutas brotam da terra em fileiras"),
    "_mult3":  dict(cor="#b23a48", cena="luz", letra="cai",
                    figs=["mu_maca", "mu_laranja", "mu_bolo", "mu_sorvete"], rot=["3", "3", "3", "3"],
                    fundo=("#f6dfe2", "#fdf6f7"), nota="o armazém: prateleira com grupos do mesmo tanto e o foco de luz varrendo"),
    "_nasal2": dict(cor="#6d1b7b", cena="pula", letra="pula",
                    figs=["nz_elefante", "nz_bombom", "nz_tambor"], rot=["~", "M", "N"],
                    fundo=("#efdcf3", "#faf4fb"), nota="as três marcas do nariz pulando sobre as figuras"),
    "_ort5":   dict(cor="#4e342e", cena="lupa", letra="desliza",
                    figs=["o5_sal", "o5_sol", "o5_anel", "o5_anzol"], rot=["SAL", "SOL", "ANEL", "ANZOL"],
                    fundo=("#e9e1de", "#f9f6f5"), nota="o caso: a lupa do detetive varre os pares que soam igual"),
    "_ort5b":  dict(cor="#283593", cena="rola", letra="gira",
                    figs=["ls_sapo", "ls_sino", "ls_osso", "ls_passaro"], rot=["S", "S", "SS", "SS"],
                    fundo=("#dfe2f4", "#f6f7fd"), nota="a loteria: as bolas com S rolando no globo"),
    "_ponto2": dict(cor="#0277bd", cena="casinha", letra="pula",
                    figs=["cs_final", "cs_interrogacao", "cs_exclamacao"], rot=[".", "?", "!"],
                    fundo=("#d8ecf8", "#f4faff"), nota="a casinha: três janelas, um ponto em cada, piscando"),
    "_reinos": dict(cor="#8e24aa", cena="coroa", letra="cresce",
                    figs=["rn_reino_animal", "rn_reino_plantae", "rn_reino_fungi", "rn_reino_protista", "rn_reino_monera"], rot=None,
                    fundo=("#eedcf3", "#faf4fc"), nota="a coroa: os cinco reinos em arco, a coroa brilhando"),
    "_rima1":  dict(cor="#6a1b9a", cena="balao", letra="pula",
                    figs=["ri_gato", "ri_pato", "ri_bola", "ri_cebola"], rot=["GATO", "PATO", "BOLA", "CEBOLA"],
                    fundo=("#e9dcf3", "#f8f3fb"), nota="o bando: as rimas penduradas em pares, balançando"),
    "_roda1":  dict(cor="#00796b", cena="roda", letra="gira",
                    figs=["ro_lata", "ro_leao", "ro_limao", "ro_lobo", "ro_lupa"], rot=["LA", "LE", "LI", "LO", "LU"],
                    fundo=("#d8efec", "#f3faf9"), nota="a roda das sílabas girando com o L no meio"),
    "_sil1":   dict(cor="#c2185b", cena="palmas", letra="pula",
                    figs=["sl_bola", "sl_borboleta", "sl_flor"], rot=["2", "4", "1"],
                    fundo=("#fadbe6", "#fef5f8"), nota="o bate-palma: ondas de som pulsando no ritmo dos pedaços"),
    "_sil2":   dict(cor="#8e5c1e", cena="gaveta", letra="desliza",
                    figs=["gv_gato", "gv_vaca", "gv_porco", "gv_rato"], rot=["GA", "VA", "POR", "RA"],
                    fundo=("#f1e6d6", "#fbf7f1"), nota="o armário: as gavetas abrindo com uma sílaba em cada"),
    "_som1":   dict(cor="#827717", cena="luz", letra="cresce",
                    figs=["so_bola", "so_boneca", "so_bota", "so_banana"], rot=["B", "B", "B", "B"],
                    fundo=("#eeedd6", "#fafaf2"), nota="o som que abre: o foco de luz acende cada palavra que começa igual"),
    "_subst5": dict(cor="#455a64", cena="esteira", letra="desliza",
                    figs=["sb_ana", "sb_davi", "sb_brasil", "sb_pluto"], rot=["Ana", "Davi", "Brasil", "Pluto"],
                    fundo=("#e1e7ea", "#f7f9fa"), nota="a fábrica de nomes: as placas de nome saindo pela esteira"),
    "_verbo4": dict(cor="#00695c", cena="esteira", letra="desliza",
                    figs=["vr_comer", "vr_correr", "vr_brincar", "vr_ler", "vr_estudar"],
                    rot=["come", "corre", "brincam", "lê", "anda"],
                    fundo=("#d5ebe7", "#f4faf8"), nota="o motor da frase: as crianças em ação passam na esteira, e embaixo de cada uma o verbo que a nomeia (figuras recortadas da folha de papel d33)"),
    "_aumdim2": dict(cor="#b5197e", cena="par", letra="cresce",
                     figs=["gp_sapo_p", "gp_sapo_g", "gp_gato_p", "gp_gato_g", "gp_bolo_p", "gp_bolo_g"],
                     rot=None,
                     fundo=("#f9dcef", "#fef6fb"), nota="o par de tamanhos: o mesmo desenho pequeno e grande lado a lado, e o pequeno cresce e volta (figuras recortadas da folha de papel d39)"),
    "_troca2": dict(cor="#c62828", cena="troca", letra="vira",
                    figs=["mq_gato", "mq_pato", "mq_lata", "mq_lama"], rot=["GA-TO", "PA-TO", "LA-TA", "LA-MA"],
                    fundo=("#fadada", "#fef5f5"), nota="a máquina de trocar: os pares trocam de lugar, uma sílaba por vez"),
}

# literais da família ROXA (cadernos antigos, sem token) -> papel de cada um
# ⚠️ `#3b3560` (tinta de texto escura) fica de fora: trocado por um cor2 quase preto, o
#    `_qa/cor_fixa.py` reprova "quase preto sem fundo" (aconteceu em _jogo1 e _mont1).
ROXOS = {"#6d5ae6": "cor", "#5b4fc4": "cor2", "#4c3cbb": "cor2",
         "#f4f2ff": "corclara", "#eceefa": "corclara", "#f2efff": "corclara", "#d9ddf2": "corclara2"}
TELHAS = {"#b0562a": "cor", "#8d4120": "cor2", "#fdf1e9": "corclara"}


def cor_atual(html):
    u"""a cor que o caderno tem AGORA — para trocar os literais dela na regeração"""
    m = re.search(r"--cor\s*:\s*(#[0-9a-fA-F]{6})", html)
    if m:
        return m.group(1).lower()
    m = re.search(r"#topo\{[^}]*border-bottom\s*:\s*\d+px\s+solid\s+(#[0-9a-fA-F]{6})", html)
    return m.group(1).lower() if m else None


# ---------------------------------------------------------------- CSS do título
def css_letra(kind, S):
    a = "letra" + S
    if kind == "cai":
        kf = "from{opacity:0;transform:translateY(-26px) rotate(-8deg)}to{opacity:1;transform:none}"
    elif kind == "vira":
        kf = "from{opacity:0;transform:rotateY(90deg) translateX(10px)}to{opacity:1;transform:none}"
    elif kind == "pula":
        kf = "0%{opacity:0;transform:translateY(30px)}60%{opacity:1;transform:translateY(-8px)}100%{opacity:1;transform:none}"
    elif kind == "desliza":
        kf = "from{opacity:0;transform:translateX(-40px)}to{opacity:1;transform:none}"
    elif kind == "cresce":
        kf = "0%{opacity:0;transform:scale(0)}70%{opacity:1;transform:scale(1.15)}100%{opacity:1;transform:scale(1)}"
    else:  # gira
        kf = "from{opacity:0;transform:rotate(-180deg) scale(.4)}to{opacity:1;transform:none}"
    return a, kf


def css_base(p, S):
    cor, cor2, clara = p["cor"], p["cor2"], p["corclara"]
    f1, f2 = p["fundo"]
    anim, kf = css_letra(p["letra"], S)
    return u"""/* ================= A CAPA =================
   IDENTIDADE PRÓPRIA deste caderno (Marcos, 18/set/2026: "cada caderno precisa ter
   capa diferente, cor diferente, animações"). Cena: %(nota)s.
   Gerado por _padrao/identidade_capa.py — editar LÁ, não aqui. Só CSS e PNG das
   folhas: nada de SVG, nada de emoji. @keyframes com sufixo %(S)s (nome é global).
   Medido pelo portão 0b11 (_qa/identidade.py). */
.capa{position:relative;text-align:center;padding:18px 16px 24px;overflow:hidden;
  background:-webkit-linear-gradient(top,%(f1)s 0%%,%(f2)s 60%%,#fff 100%%);
  background:linear-gradient(180deg,%(f1)s 0%%,%(f2)s 60%%,#fff 100%%)}
.capa .ceu{position:absolute;left:0;right:0;top:0;bottom:0;pointer-events:none;overflow:hidden}
.capa .titu,.capa .sub,.capa .chamada,.capa .cena{position:relative;z-index:1}
.capa h1.titu{margin:12px 0 4px;line-height:1;display:flex;flex-wrap:wrap;justify-content:center;gap:2px;
  -webkit-perspective:600px;perspective:600px}
.capa .titu .cptpal{display:inline-flex;white-space:nowrap;gap:2px}
.capa .titu .lt{display:inline-block;font-size:clamp(22px,5.8vw,42px);font-weight:900;letter-spacing:0;
  color:%(cor2)s;text-shadow:0 3px 0 %(clara)s,0 5px 10px rgba(0,0,0,.16);
  -webkit-animation:%(anim)s .7s both;animation:%(anim)s .7s both}
.capa .titu .cpesp{display:inline-block;width:14px}
@-webkit-keyframes %(anim)s{%(kfw)s}
@keyframes %(anim)s{%(kf)s}
.capa .sub{font-weight:700;color:#2c3745;font-size:clamp(13px,3.6vw,18px);margin:6px 0 4px}
.capa .chamada{margin-top:14px;font-weight:700;color:#3a4658;font-size:clamp(13px,3.4vw,16px)}
.capa .cena{margin:14px auto 4px;max-width:620px}
.capa .capfig{width:auto;height:clamp(74px,19vw,124px);max-width:100%%;object-fit:contain;display:block}
.capa .pl{display:block;font-weight:900;font-size:clamp(16px,4.6vw,26px);color:#fff;background:%(cor)s;border-radius:12px;
  padding:8px 14px;box-shadow:0 5px 0 %(cor2)s;letter-spacing:.02em;white-space:nowrap}
.capa .rt{display:block;font-weight:900;font-size:clamp(12px,3.4vw,17px);color:#fff;background:%(cor)s;
  border-radius:9px;padding:2px 8px;margin-top:4px;letter-spacing:.03em;white-space:nowrap}
""" % dict(nota=p["nota"], S=S, f1=f1, f2=f2, cor=cor, cor2=cor2, clara=clara, anim=anim,
           kf=kf, kfw=kf.replace("transform", "-webkit-transform"))


def kfs(nome, corpo):
    return ("@-webkit-keyframes %s{%s}\n@keyframes %s{%s}\n"
            % (nome, corpo.replace("transform", "-webkit-transform"), nome, corpo))


# ---------------------------------------------------------------- as cenas
# cada cena devolve (css, html_js) — html_js é uma EXPRESSÃO JavaScript (string)
# ⚠️ A CLASSE DA FIGURA DA CAPA É `capfig`, E NUNCA `cf` (18/set/2026, `_verbo4`).
#    `.cf` é o CONFETE do motor: `position:absolute` + `animation:cai`, que termina
#    em `opacity:0` e `translateY(105vh)`. As cinco crianças da capa ficavam com
#    opacidade ZERO e 950 px abaixo da tela — visíveis no DOM, com tamanho certo,
#    e invisíveis na tela. Nenhum portão viu; quem viu foi a FOTO.
def fig(f, cls="capfig"):
    return "'<img class=\"%s\" draggable=\"false\" src=\"img/%s.png?v=' + V + '\" alt=\"\">'" % (cls, f)


def rot(p, i):
    r = p.get("rot")
    return "'<span class=\"rt\">%s</span>'" % r[i].replace("'", "\\'") if r else "''"


def item(p, i, cls="it", extra=""):
    # figura None = item so de PALAVRA (caderno sem figura, como o de verbos)
    f = p["figs"][i]
    corpo = (fig(f) + extra) if f else "'<span class=\"pl\">' + '" + (p["rot"][i] if p.get("rot") else "") + "' + '</span>'"
    return "'<div class=\"%s\" style=\"animation-delay:%.2fs\">' + %s + %s + '</div>'" % (
        cls, i * 0.35, corpo, rot(p, i) if f else "''")


def cena_desfile(p, S):
    css = u""".capa .cena{display:flex;justify-content:center;align-items:flex-end;gap:clamp(6px,2vw,14px);flex-wrap:nowrap}
.capa .it{display:flex;flex-direction:column;align-items:center;-webkit-animation:marcha%(S)s 1.6s ease-in-out infinite;animation:marcha%(S)s 1.6s ease-in-out infinite}
.capa .tapete{height:16px;max-width:620px;margin:-4px auto 0;border-radius:4px;background:%(cor)s;
  box-shadow:0 6px 14px rgba(0,0,0,.18);position:relative;z-index:1}
.capa .tapete:after{content:"";position:absolute;left:6%%;right:6%%;top:6px;height:4px;border-radius:2px;background:rgba(255,255,255,.55)}
""" % dict(S=S, cor=p["cor"]) + kfs("marcha" + S, "0%,100%{transform:translateX(-6px) rotate(-3deg)}50%{transform:translateX(6px) rotate(3deg)}")
    html = " + ".join(item(p, i) for i in range(len(p["figs"])))
    return css, "'<div class=\"cena\">' + " + html + " + '</div><div class=\"tapete\"></div>'"


def cena_esteira(p, S):
    css = u""".capa .cena{display:flex;justify-content:center;align-items:flex-end;gap:clamp(8px,2.5vw,18px);flex-wrap:nowrap}
.capa .it{display:flex;flex-direction:column;align-items:center;-webkit-animation:sobe%(S)s 2.4s ease-in-out infinite;animation:sobe%(S)s 2.4s ease-in-out infinite}
.capa .esteira2{position:relative;max-width:620px;margin:0 auto;height:26px;border-radius:13px;background:#4a4a52;
  box-shadow:inset 0 3px 0 rgba(255,255,255,.18),0 6px 14px rgba(0,0,0,.2);display:flex;justify-content:space-around;align-items:center;padding:0 10px}
.capa .rolo{width:16px;height:16px;border-radius:50%%;background:%(clara)s;border:3px solid %(cor)s;position:relative;
  -webkit-animation:gira%(S)s 1.4s linear infinite;animation:gira%(S)s 1.4s linear infinite}
.capa .rolo:after{content:"";position:absolute;left:50%%;top:-1px;width:2px;height:6px;margin-left:-1px;background:%(cor)s}
""" % dict(S=S, cor=p["cor"], clara=p["corclara"]) + kfs("sobe" + S, "0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}") \
        + kfs("gira" + S, "to{transform:rotate(360deg)}")
    html = " + ".join(item(p, i) for i in range(len(p["figs"])))
    rolos = "'<div class=\"esteira2\">' + " + " + ".join(["'<i class=\"rolo\"></i>'"] * 7) + " + '</div>'"
    return css, "'<div class=\"cena\">' + " + html + " + '</div>' + " + rolos


def cena_rua(p, S):
    css = u""".capa .nv{position:absolute;display:block;border-radius:50%%;
  background:-webkit-radial-gradient(circle,rgba(255,255,255,.85),rgba(255,255,255,0) 70%%);
  background:radial-gradient(circle,rgba(255,255,255,.85),rgba(255,255,255,0) 70%%)}
.capa .n1{width:220px;height:130px;left:-40px;top:14px}.capa .n2{width:280px;height:150px;right:-70px;top:44px}
.capa .sol{position:absolute;right:22px;top:16px;width:56px;height:56px;border-radius:50%%;
  background:radial-gradient(circle at 40%% 38%%,#fff2b8,#f5b301);box-shadow:0 0 26px rgba(245,179,1,.55)}
.capa .cena{display:flex;justify-content:center;align-items:flex-end;gap:6px;flex-wrap:nowrap}
.capa .it{-webkit-animation:sobe%(S)s 2.6s ease-in-out infinite;animation:sobe%(S)s 2.6s ease-in-out infinite}
.capa .calcada{display:flex;gap:6px;justify-content:center;background:#7b6a5c;border-radius:9px;max-width:620px;margin:0 auto;
  padding:6px 8px;box-shadow:0 6px 14px rgba(70,40,20,.22)}
.capa .calcada i{display:block;width:26px;height:9px;background:#cbb9a8;border-radius:5px}
""" % dict(S=S) + kfs("sobe" + S, "0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}")
    html = " + ".join(item(p, i) for i in range(len(p["figs"])))
    ceu = "'<div class=\"ceu\"><i class=\"nv n1\"></i><i class=\"nv n2\"></i><i class=\"sol\"></i></div>'"
    calc = "'<div class=\"calcada\">' + " + " + ".join(["'<i></i>'"] * 8) + " + '</div>'"
    return css, ceu + " + '<div class=\"cena\">' + " + html + " + '</div>' + " + calc, True


def cena_tecla(p, S):
    css = u""".capa .cena{display:flex;flex-direction:column;align-items:center;gap:10px}
.capa .cpfila{display:flex;justify-content:center;align-items:flex-end;gap:clamp(14px,5vw,40px)}
.capa .it{-webkit-animation:pula%(S)s 1.8s ease-in-out infinite;animation:pula%(S)s 1.8s ease-in-out infinite}
.capa .tecla{width:min(78%%,420px);height:46px;border-radius:12px;background:#f7f7f9;border:3px solid %(cor)s;
  box-shadow:0 7px 0 %(cor2)s,0 12px 18px rgba(0,0,0,.18);font-weight:900;color:%(cor2)s;letter-spacing:.2em;line-height:40px;
  -webkit-animation:aperta%(S)s 1.8s ease-in-out infinite;animation:aperta%(S)s 1.8s ease-in-out infinite}
""" % dict(S=S, cor=p["cor"], cor2=p["cor2"]) + kfs("aperta" + S, "0%,100%{transform:translateY(0);box-shadow:0 7px 0 " + p["cor2"] + ",0 12px 18px rgba(0,0,0,.18)}50%{transform:translateY(6px);box-shadow:0 1px 0 " + p["cor2"] + ",0 4px 8px rgba(0,0,0,.18)}") \
        + kfs("pula" + S, "0%,40%,100%{transform:translateY(0)}55%{transform:translateY(-14px)}")
    html = " + ".join(item(p, i) for i in range(len(p["figs"])))
    return css, "'<div class=\"cena\"><div class=\"cpfila\">' + " + html + " + '</div><div class=\"tecla\">ESPAÇO</div></div>'"


def cena_balao(p, S, balcao=False):
    css = u""".capa .cena{display:flex;justify-content:center;align-items:flex-start;gap:clamp(8px,3vw,22px);flex-wrap:nowrap;padding-top:4px}
.capa .it{display:flex;flex-direction:column;align-items:center;transform-origin:50%% 0;
  -webkit-animation:balanca%(S)s 2.8s ease-in-out infinite;animation:balanca%(S)s 2.8s ease-in-out infinite}
.capa .it:nth-child(even){animation-direction:reverse}
.capa .fio{display:block;width:3px;height:clamp(18px,5vw,34px);background:%(cor2)s;border-radius:2px}
.capa .cpbarra{max-width:620px;margin:0 auto;height:10px;border-radius:5px;background:%(cor)s;box-shadow:0 4px 10px rgba(0,0,0,.2)}
""" % dict(S=S, cor=p["cor"], cor2=p["cor2"]) + kfs("balanca" + S, "0%,100%{transform:rotate(-5deg)}50%{transform:rotate(5deg)}")
    if balcao:
        css += u""".capa .balcao{max-width:620px;margin:0 auto;height:34px;border-radius:0 0 12px 12px;background:%(cor)s;
  box-shadow:inset 0 -8px 0 %(cor2)s,0 8px 16px rgba(0,0,0,.2);font-weight:900;color:#fff;letter-spacing:.14em;line-height:26px;font-size:13px}
""" % dict(cor=p["cor"], cor2=p["cor2"])
    html = " + ".join(item(p, i, extra="", cls="it").replace("+ '<img", "+ '<i class=\"fio\"></i><img") for i in range(len(p["figs"])))
    fim = "'<div class=\"balcao\">LOST &amp; FOUND</div>'" if balcao else "''"
    return css, "'<div class=\"cpbarra\"></div><div class=\"cena\">' + " + html + " + '</div>' + " + fim


def cena_brota(p, S):
    css = u""".capa .cena{display:flex;justify-content:center;align-items:flex-end;gap:clamp(6px,2vw,14px);flex-wrap:nowrap}
.capa .it{display:flex;flex-direction:column;align-items:center;transform-origin:50%% 100%%;
  -webkit-animation:brota%(S)s 3s ease-in-out infinite;animation:brota%(S)s 3s ease-in-out infinite}
.capa .terra{max-width:620px;margin:-6px auto 0;height:22px;border-radius:0 0 14px 14px;background:%(cor)s;
  box-shadow:inset 0 6px 0 %(cor2)s,0 6px 14px rgba(0,0,0,.2);position:relative;z-index:1}
""" % dict(S=S, cor=p["cor"], cor2=p["cor2"]) + kfs("brota" + S, "0%{transform:scaleY(.86) translateY(4px)}50%{transform:scaleY(1) translateY(0)}100%{transform:scaleY(.86) translateY(4px)}")
    html = " + ".join(item(p, i) for i in range(len(p["figs"])))
    return css, "'<div class=\"cena\">' + " + html + " + '</div><div class=\"terra\"></div>'"


def cena_rola(p, S):
    css = u""".capa .cena{display:flex;justify-content:center;align-items:flex-end;gap:clamp(4px,2.5vw,24px);flex-wrap:wrap;min-height:110px;padding:0 4px}
.capa .it{display:flex;flex-direction:column;align-items:center;-webkit-animation:rola%(S)s 2.2s ease-in-out infinite;animation:rola%(S)s 2.2s ease-in-out infinite}
.capa .it:first-child .capfig{-webkit-animation:gira%(S)s 2.2s linear infinite;animation:gira%(S)s 2.2s linear infinite}
.capa .tabu{max-width:620px;margin:0 auto;height:14px;border-radius:7px;background:%(cor)s;box-shadow:0 5px 12px rgba(0,0,0,.2);
  background-image:repeating-linear-gradient(90deg,transparent 0 22px,rgba(255,255,255,.35) 22px 24px)}
""" % dict(S=S, cor=p["cor"]) + kfs("rola" + S, "0%,100%{transform:translateY(0)}50%{transform:translateY(-16px)}") \
        + kfs("gira" + S, "to{transform:rotate(360deg)}")
    html = " + ".join(item(p, i) for i in range(len(p["figs"])))
    return css, "'<div class=\"cena\">' + " + html + " + '</div><div class=\"tabu\"></div>'"


def cena_vira(p, S):
    css = u""".capa .cena{display:flex;justify-content:center;gap:clamp(6px,2vw,12px);flex-wrap:wrap;-webkit-perspective:700px;perspective:700px}
.capa .carta{width:clamp(60px,16vw,100px);border-radius:12px;background:#fff;border:3px solid %(cor)s;padding:6px 4px;
  display:flex;flex-direction:column;align-items:center;box-shadow:0 6px 14px rgba(0,0,0,.14);
  -webkit-animation:vira%(S)s 4s ease-in-out infinite;animation:vira%(S)s 4s ease-in-out infinite}
.capa .carta .capfig{width:clamp(44px,12vw,72px);height:clamp(44px,12vw,72px)}
""" % dict(S=S, cor=p["cor"]) + kfs("vira" + S, "0%,40%{transform:rotateY(0)}50%{transform:rotateY(52deg)}60%,100%{transform:rotateY(0)}")
    # ⚠️ 52 graus e nao 88: a 88 a carta fica de perfil e some da foto (largura 3 px).
    #    Vira o bastante para a crianca ver o gesto, sem desaparecer.
    html = " + ".join(item(p, i, cls="carta") for i in range(len(p["figs"])))
    return css, "'<div class=\"cena\">' + " + html + " + '</div>'"


def cena_junta(p, S):
    css = u""".capa .cena{display:flex;justify-content:center;gap:clamp(6px,2vw,14px);flex-wrap:nowrap}
.capa .it{display:flex;flex-direction:column;align-items:center}
.capa .it .capfig{-webkit-animation:junta%(S)s 2.6s ease-in-out infinite;animation:junta%(S)s 2.6s ease-in-out infinite}
.capa .it:nth-child(even) .capfig{animation-direction:reverse}
.capa .engr{max-width:620px;margin:0 auto;height:18px;border-radius:9px;background:%(cor)s;box-shadow:0 5px 12px rgba(0,0,0,.2);
  background-image:repeating-linear-gradient(90deg,%(cor2)s 0 10px,transparent 10px 20px)}
""" % dict(S=S, cor=p["cor"], cor2=p["cor2"]) + kfs("junta" + S, "0%,100%{transform:translateX(-10px)}50%{transform:translateX(10px)}")
    html = " + ".join(item(p, i) for i in range(len(p["figs"])))
    return css, "'<div class=\"cena\">' + " + html + " + '</div><div class=\"engr\"></div>'"


def cena_troca(p, S):
    css = u""".capa .cena{display:flex;justify-content:center;gap:clamp(10px,3vw,24px);flex-wrap:nowrap}
.capa .par{display:flex;gap:clamp(4px,1.5vw,10px);padding:6px;border-radius:14px;background:rgba(255,255,255,.6);border:3px dashed %(cor)s}
.capa .it{display:flex;flex-direction:column;align-items:center}
.capa .par .it:first-child{-webkit-animation:trocaA%(S)s 3s ease-in-out infinite;animation:trocaA%(S)s 3s ease-in-out infinite}
.capa .par .it:last-child{-webkit-animation:trocaB%(S)s 3s ease-in-out infinite;animation:trocaB%(S)s 3s ease-in-out infinite}
""" % dict(S=S, cor=p["cor"]) + kfs("trocaA" + S, "0%,20%{transform:translateX(0)}45%,75%{transform:translateX(calc(100% + 8px))}100%{transform:translateX(0)}") \
        + kfs("trocaB" + S, "0%,20%{transform:translateX(0)}45%,75%{transform:translateX(calc(-100% - 8px))}100%{transform:translateX(0)}")
    pares = []
    for i in range(0, len(p["figs"]) - 1, 2):
        pares.append("'<div class=\"par\">' + " + item(p, i) + " + " + item(p, i + 1) + " + '</div>'")
    return css, "'<div class=\"cena\">' + " + " + ".join(pares) + " + '</div>'"


def cena_luz(p, S, lupa=False):
    css = u""".capa .cena{position:relative;display:flex;justify-content:center;align-items:flex-end;gap:clamp(8px,2.5vw,18px);flex-wrap:nowrap;padding:8px 0 0}
.capa .it{display:flex;flex-direction:column;align-items:center}
.capa .prat{max-width:620px;margin:-4px auto 0;height:14px;border-radius:4px;background:%(cor)s;box-shadow:0 8px 0 %(cor2)s,0 12px 16px rgba(0,0,0,.2)}
.capa .foco{position:absolute;top:-10px;bottom:-4px;width:clamp(64px,18vw,110px);border-radius:50%%;pointer-events:none;
  background:radial-gradient(ellipse at center,rgba(255,240,150,.7),rgba(255,240,150,0) 72%%);left:0;
  -webkit-animation:varre%(S)s 3.6s ease-in-out infinite;animation:varre%(S)s 3.6s ease-in-out infinite}
""" % dict(S=S, cor=p["cor"], cor2=p["cor2"]) + kfs("varre" + S, "0%,100%{left:0}50%{left:calc(100% - clamp(64px,18vw,110px))}")
    if lupa:
        css += u""".capa .foco{background:none;border:6px solid %(cor2)s;border-radius:50%%;top:auto;bottom:22px;height:clamp(64px,18vw,110px);
  box-shadow:inset 0 0 0 4px rgba(255,255,255,.55);z-index:2}
.capa .foco:after{content:"";position:absolute;right:-26px;bottom:-22px;width:36px;height:12px;border-radius:6px;background:%(cor2)s;transform:rotate(40deg)}
""" % dict(cor2=p["cor2"])
    html = " + ".join(item(p, i) for i in range(len(p["figs"])))
    return css, "'<div class=\"cena\"><i class=\"foco\"></i>' + " + html + " + '</div><div class=\"prat\"></div>'"


def cena_gaveta(p, S):
    css = u""".capa .cena{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;max-width:480px}
.capa .gav{display:flex;align-items:center;justify-content:center;gap:8px;padding:6px 10px;border-radius:10px;background:%(clara)s;
  border:3px solid %(cor)s;box-shadow:inset 0 -6px 0 rgba(0,0,0,.08),0 4px 10px rgba(0,0,0,.15);
  -webkit-animation:abre%(S)s 3.2s ease-in-out infinite;animation:abre%(S)s 3.2s ease-in-out infinite}
.capa .gav .capfig{width:clamp(40px,11vw,66px);height:clamp(40px,11vw,66px)}
.capa .gav .rt{margin:0}
.capa .puxa{width:26px;height:8px;border-radius:4px;background:%(cor2)s;flex:none}
""" % dict(S=S, cor=p["cor"], cor2=p["cor2"], clara=p["corclara"]) + kfs("abre" + S, "0%,100%{transform:translateX(0)}50%{transform:translateX(10px)}")
    html = " + ".join(("'<div class=\"gav\" style=\"animation-delay:%.2fs\">' + %s + %s + '<i class=\"puxa\"></i></div>'"
                       % (i * 0.4, fig(p["figs"][i]), rot(p, i))) for i in range(len(p["figs"])))
    return css, "'<div class=\"cena\">' + " + html + " + '</div>'"


def cena_casinha(p, S):
    css = u""".capa .cena{max-width:360px}
.capa .telhado{width:0;height:0;margin:0 auto;border-left:min(48vw,180px) solid transparent;border-right:min(48vw,180px) solid transparent;border-bottom:60px solid %(cor2)s}
.capa .parede{background:%(clara)s;border:3px solid %(cor)s;border-top:0;border-radius:0 0 14px 14px;padding:12px 10px 14px;display:flex;justify-content:space-around;gap:8px}
.capa .jan{width:clamp(64px,20vw,96px);border:3px solid %(cor2)s;border-radius:8px;background:#fff;padding:4px;display:flex;flex-direction:column;align-items:center;
  -webkit-animation:pisca%(S)s 3s ease-in-out infinite;animation:pisca%(S)s 3s ease-in-out infinite}
.capa .jan .capfig{width:clamp(40px,12vw,64px);height:clamp(40px,12vw,64px)}
.capa .jan .rt{font-size:clamp(16px,4.6vw,24px);margin-top:2px;padding:0 10px}
""" % dict(S=S, cor=p["cor"], cor2=p["cor2"], clara=p["corclara"]) + kfs("pisca" + S, "0%,100%{background:#fff}50%{background:#fff3b0;box-shadow:0 0 18px rgba(255,220,90,.9)}")
    html = " + ".join(item(p, i, cls="jan") for i in range(len(p["figs"])))
    return css, "'<div class=\"cena\"><div class=\"telhado\"></div><div class=\"parede\">' + " + html + " + '</div></div>'"


def cena_coroa(p, S):
    css = u""".capa .cena{display:flex;justify-content:center;align-items:flex-end;gap:clamp(4px,1.5vw,12px);flex-wrap:nowrap}
.capa .it{display:flex;flex-direction:column;align-items:center}
.capa .it:nth-child(1),.capa .it:nth-child(5){transform:translateY(18px)}
.capa .it:nth-child(2),.capa .it:nth-child(4){transform:translateY(8px)}
.capa .it .capfig{-webkit-animation:brilha%(S)s 2.6s ease-in-out infinite;animation:brilha%(S)s 2.6s ease-in-out infinite}
.capa .coroa{width:min(60%%,300px);height:34px;margin:8px auto 0;background:%(cor)s;border-radius:6px 6px 10px 10px;position:relative;
  box-shadow:0 6px 14px rgba(0,0,0,.2)}
.capa .coroa:before{content:"";position:absolute;left:0;right:0;top:-22px;height:22px;
  background:linear-gradient(135deg,transparent 50%%,%(cor)s 50%%) 0 0/20%% 100%%,linear-gradient(225deg,transparent 50%%,%(cor)s 50%%) 0 0/20%% 100%%}
.capa .coroa:after{content:"";position:absolute;left:12%%;right:12%%;top:12px;height:8px;border-radius:4px;background:#ffd54f;box-shadow:0 0 12px #ffd54f}
""" % dict(S=S, cor=p["cor"]) + kfs("brilha" + S, "0%,100%{filter:drop-shadow(0 0 0 rgba(255,213,79,0))}50%{filter:drop-shadow(0 0 10px rgba(255,213,79,.9))}")
    html = " + ".join(item(p, i) for i in range(len(p["figs"])))
    return css, "'<div class=\"cena\">' + " + html + " + '</div><div class=\"coroa\"></div>'"


def cena_roda(p, S):
    n = len(p["figs"])
    css = u""".capa .cena{position:relative;width:min(78vw,300px);height:min(78vw,300px);margin:8px auto 0}
.capa .aro{position:absolute;left:0;top:0;right:0;bottom:0;border-radius:50%%;border:8px dashed %(cor)s}
.capa .cporbe{position:absolute;left:0;top:0;right:0;bottom:0;-webkit-animation:roda%(S)s 16s linear infinite;animation:roda%(S)s 16s linear infinite}
.capa .miolo{position:absolute;left:50%%;top:50%%;width:clamp(52px,16vw,76px);height:clamp(52px,16vw,76px);margin:calc(clamp(52px,16vw,76px) / -2) 0 0 calc(clamp(52px,16vw,76px) / -2);
  border-radius:50%%;background:%(cor)s;color:#fff;font-weight:900;font-size:clamp(26px,8vw,40px);line-height:clamp(52px,16vw,76px);box-shadow:0 6px 14px rgba(0,0,0,.25)}
.capa .it{position:absolute;width:64px;margin-left:-32px;margin-top:-36px;display:flex;flex-direction:column;align-items:center;
  -webkit-animation:roda%(S)s 16s linear infinite reverse;animation:roda%(S)s 16s linear infinite reverse}
.capa .it .capfig{width:clamp(36px,10vw,56px);height:clamp(36px,10vw,56px)}
.capa .it .rt{font-size:12px;padding:1px 6px}
""" % dict(S=S, cor=p["cor"]) + kfs("roda" + S, "to{transform:rotate(360deg)}")
    itens = []
    import math
    for i in range(n):
        ang = -90 + i * 360.0 / n
        x = 50 + math.cos(math.radians(ang)) * 42
        y = 50 + math.sin(math.radians(ang)) * 42
        itens.append("'<div class=\"it\" style=\"left:%.1f%%;top:%.1f%%\">' + %s + %s + '</div>'"
                     % (x, y, fig(p["figs"][i]), rot(p, i)))
    return css, ("'<div class=\"cena\"><i class=\"aro\"></i><div class=\"miolo\">L</div><div class=\"cporbe\">' + "
                 + " + ".join(itens) + " + '</div></div>'")


def cena_palmas(p, S):
    css = u""".capa .cena{display:flex;justify-content:center;align-items:center;gap:clamp(10px,4vw,30px);flex-wrap:nowrap}
.capa .it{position:relative;display:flex;flex-direction:column;align-items:center;padding:14px 10px 6px}
.capa .it:before,.capa .it:after{content:"";position:absolute;left:50%%;top:42%%;width:20px;height:20px;margin:-10px 0 0 -10px;border-radius:50%%;
  border:4px solid %(cor)s;opacity:0;-webkit-animation:onda%(S)s 1.8s ease-out infinite;animation:onda%(S)s 1.8s ease-out infinite}
.capa .it:after{animation-delay:.6s}
.capa .it .capfig{position:relative;z-index:1;-webkit-animation:bate%(S)s 1.8s ease-in-out infinite;animation:bate%(S)s 1.8s ease-in-out infinite}
""" % dict(S=S, cor=p["cor"]) + kfs("onda" + S, "0%{transform:scale(1);opacity:.8}100%{transform:scale(5.5);opacity:0}") \
        + kfs("bate" + S, "0%,100%{transform:scale(1)}12%{transform:scale(1.12)}")
    html = " + ".join(item(p, i) for i in range(len(p["figs"])))
    return css, "'<div class=\"cena\">' + " + html + " + '</div>'"


def cena_pula(p, S):
    css = u""".capa .cena{display:flex;justify-content:center;align-items:flex-end;gap:clamp(12px,4vw,34px);flex-wrap:nowrap}
.capa .it{display:flex;flex-direction:column-reverse;align-items:center}
.capa .it .rt{margin:0 0 6px;font-size:clamp(22px,7vw,36px);padding:0 14px;border-radius:12px;
  -webkit-animation:pula%(S)s 1.5s ease-in-out infinite;animation:pula%(S)s 1.5s ease-in-out infinite}
.capa .it:nth-child(2) .rt{animation-delay:.25s}.capa .it:nth-child(3) .rt{animation-delay:.5s}
""" % dict(S=S) + kfs("pula" + S, "0%,100%{transform:translateY(0)}50%{transform:translateY(-18px) scale(1.08)}")
    html = " + ".join(item(p, i) for i in range(len(p["figs"])))
    return css, "'<div class=\"cena\">' + " + html + " + '</div>'"


def cena_par(p, S):
    u"""O PAR DE TAMANHOS — a cena do caderno do grandão e do pequenininho.

    ⚠️ Ela precisou existir: nas outras dezoito cenas a figura aparece UMA vez, e
       neste caderno o conceito É o par. As peças vêm aos dois: `figs` traz
       pequeno e grande alternados, e a cena os junta dois a dois.

    ⚠️⚠️ E A REGRA DE ALTURA DA CAPA TEVE DE SER QUEBRADA AQUI, de propósito. O
       `.capa .capfig` dá a TODA figura a mesma altura — o que é certo em
       qualquer outra capa e é exatamente o defeito nesta: com os dois do mesmo
       tamanho, a capa deste caderno deixa de dizer o que o caderno ensina. Aqui
       a ALTURA DO PAR é que é fixa, e dentro dela cada peça entra na proporção
       REAL do arquivo (lida do PNG, não chutada): o grande ocupa a altura toda
       e o pequeno, a fração medida. Sem isso a capa ainda estourava a tela: as
       peças saíam no tamanho natural (até 300 px) e o terceiro par ficava fora
       do celular.
    """
    try:
        from PIL import Image
    except ImportError:                                    # pragma: no cover
        raise SystemExit("cena_par precisa do Pillow para medir a proporcao do par")
    css = u""".capa .cena{display:flex;justify-content:center;align-items:flex-end;
  gap:clamp(8px,3vw,22px);flex-wrap:nowrap}
.capa .cppar{display:flex;align-items:flex-end;gap:clamp(2px,1vw,7px);padding:0 clamp(3px,1vw,7px);
  height:clamp(66px,17vw,116px);border-bottom:5px solid %(cor)s;border-radius:0 0 8px 8px}
.capa .cppar .capfig{height:100%%;width:auto;max-width:none;display:block}
.capa .cppeq{-webkit-animation:crescePar%(S)s 2.6s ease-in-out infinite;animation:crescePar%(S)s 2.6s ease-in-out infinite;
  -webkit-transform-origin:bottom center;transform-origin:bottom center}
.capa .cena>.cppar:nth-child(2) .cppeq{-webkit-animation-delay:.45s;animation-delay:.45s}
.capa .cena>.cppar:nth-child(3) .cppeq{-webkit-animation-delay:.9s;animation-delay:.9s}
.capa .cpgra{-webkit-animation:pisaPar%(S)s 2.6s ease-in-out infinite;animation:pisaPar%(S)s 2.6s ease-in-out infinite;
  -webkit-transform-origin:bottom center;transform-origin:bottom center}
""" % dict(S=S, cor=p["cor"]) + kfs("crescePar" + S, "0%,100%{transform:scale(1)}50%{transform:scale(1.18)}") \
        + kfs("pisaPar" + S, "0%,100%{transform:scale(1)}50%{transform:scale(.95)}")

    def alt(f):
        return Image.open(os.path.join(p["pasta"], "img", f + ".png")).size[1]

    fs, pares = p["figs"], []
    for i in range(0, len(fs), 2):
        peq, gra = fs[i], fs[i + 1]
        pct = 100.0 * alt(peq) / float(alt(gra))
        img_peq = ("'<img class=\"capfig cppeq\" draggable=\"false\" style=\"height:%.1f%%\" "
                   "src=\"img/%s.png?v=' + V + '\" alt=\"\">'" % (pct, peq))
        pares.append("'<div class=\"cppar\">' + " + img_peq + " + " + fig(gra, "capfig cpgra")
                     + " + '</div>'")
    return css, "'<div class=\"cena\">' + " + " + ".join(pares) + " + '</div>'"


CENAS = {
    "desfile": cena_desfile, "esteira": cena_esteira, "rua": cena_rua, "tecla": cena_tecla,
    "balao": cena_balao, "balcao": lambda p, S: cena_balao(p, S, True), "brota": cena_brota,
    "rola": cena_rola, "vira": cena_vira, "junta": cena_junta, "troca": cena_troca,
    "luz": cena_luz, "lupa": lambda p, S: cena_luz(p, S, True), "gaveta": cena_gaveta,
    "casinha": cena_casinha, "coroa": cena_coroa, "roda": cena_roda, "palmas": cena_palmas,
    "pula": cena_pula, "par": cena_par,
}

ANTIGOS = {
    "entraDupla": "from{opacity:0;transform:translateY(-18px) scale(.85)}to{opacity:1;transform:none}",
    "caiLetra": "from{opacity:0;transform:translateY(-26px) rotate(-8deg)}to{opacity:1;transform:none}",
    "caiCasa": "from{opacity:0;transform:translateY(-26px) rotate(-8deg)}to{opacity:1;transform:none}",
    "sobe": "0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}",
    "sobeCasa": "0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}",
}

REDUZ = u"""@media (prefers-reduced-motion: reduce){
  .capa *,.capa *:before,.capa *:after{-webkit-animation:none!important;animation:none!important}
}

"""


# ---------------------------------------------------------------- aplicar
def sufixo(pasta):
    s = re.sub(r"[^a-z0-9]", "", pasta.lower())
    return s[:1].upper() + s[1:]


def aplica(pasta):
    p = dict(ESPEC[pasta])
    p["pasta"] = pasta
    S = sufixo(pasta)
    p["cor2"] = escurece(p["cor"])
    p["corclara"] = clareia(p["cor"])
    p["corclara2"] = clareia(p["cor"], 0.72)
    if contraste_branco(p["cor"]) < 4.5:
        raise SystemExit("%s: cor %s tem contraste %.2f sobre branco (< 4,5) — escolha outra" % (pasta, p["cor"], contraste_branco(p["cor"])))
    # ⚠️ 18/set/2026: nos cadernos antigos o literal que virou `cor2` era TINTA DE
    #    TEXTO. Com uma cor base escura, o `cor2` sai quase preto e o
    #    `_qa/cor_fixa.py` reprova ("tinta extrema sem fundo proprio") — aconteceu
    #    em `_jogo1` (#37474f) e `_mont1` (#795548). A cor do caderno tem de ser
    #    clara o bastante para o seu tom escuro ainda ser TINTA, nao breu.
    # ⚠️ NAO INVENTAR LIMIAR AQUI. Eu tentei um piso de luminancia para o tom
    #    escuro e ele reprovava 19 das 25 cores — porque o tom escuro so machuca
    #    quando o caderno o usa como TINTA DE TEXTO sem fundo, e isso depende do
    #    caderno, nao da cor. Quem sabe e' o `_qa/cor_fixa.py`, que le o arquivo
    #    GERADO. Por isso a conferencia e' no fim de `aplica()`, com a medida dele.
    for f in p["figs"]:
        if f and not os.path.isfile(os.path.join(pasta, "img", f + ".png")):
            raise SystemExit("%s: figura %s.png nao existe em img/" % (pasta, f))

    ih = os.path.join(pasta, "index.html")
    jf = os.path.join(pasta, "folhas.js")
    h = io.open(ih, encoding="utf-8").read()
    h_antes = h
    j = io.open(jf, encoding="utf-8").read()

    # --- 1) a cor
    if "--cor:" in h:
        h = re.sub(r"--cor\s*:\s*#[0-9a-fA-F]{6};", "--cor:%s;" % p["cor"], h, count=1)
        h = re.sub(r"--cor2\s*:\s*#[0-9a-fA-F]{6};", "--cor2:%s;" % p["cor2"], h, count=1)
        h = re.sub(r"--corclara\s*:\s*#[0-9a-fA-F]{6};", "--corclara:%s;" % p["corclara"], h, count=1)
        for lit, papel in TELHAS.items():
            h = re.sub(re.escape(lit), p[papel], h, flags=re.I)
    else:
        for lit, papel in ROXOS.items():
            h = re.sub(re.escape(lit), p[papel], h, flags=re.I)
    # ⚠️ REGERAR DUAS VEZES: na 2a passada os literais ja nao sao os roxos/telha
    #    originais, e sim a cor que EU pus na 1a. Sem isto sobra a cor velha no
    #    arquivo (aconteceu com `#37474f` em `_jogo1`) e o `_qa/cor_fixa.py` acusa.
    velha = cor_atual(h_antes)
    if velha and velha != p["cor"].lower():
        for lit, papel in ((velha, "cor"), (escurece(velha), "cor2"),
                           (clareia(velha), "corclara"), (clareia(velha, 0.72), "corclara2")):
            h = re.sub(re.escape(lit), p[papel], h, flags=re.I)

    # --- 2) o bloco da capa
    m_ini = re.search(r"^/\* ================= A CAPA.*?$", h, re.M)
    if m_ini:
        ini = m_ini.start()
    else:
        m = re.search(r"^\.capa\{", h, re.M)
        if not m:
            raise SystemExit("%s: nao achei `.capa{` no CSS" % pasta)
        ini = m.start()
    fim = h.find("#fim,#retomar{", ini)
    if fim < 0:
        raise SystemExit("%s: nao achei `#fim,#retomar{` depois da capa" % pasta)
    # ⚠️ 18/set/2026, `_verbo4`: este trecho e' APAGADO e reescrito. Se alguem
    #    guardou o CSS das PECAS entre a capa e o `#fim`, ele some em silencio —
    #    e foi o que aconteceu: `.palav` e `.cpcel` sumiram, os alvos viraram
    #    21 px e so o `leiaute_mao` viu, depois da banca inteira. O bloco das
    #    pecas mora DEPOIS do `#fim` (ou antes do `</style>`), nunca aqui.
    trecho = h[ini:fim]
    if "/*PECAS-CSS-INI*/" in trecho or "/*PECAS-CSS-FIM*/" in trecho:
        raise SystemExit("%s: o bloco PECAS-CSS esta DENTRO do trecho da capa e "
                         "seria apagado. Mova-o para depois do `#fim,#retomar{`." % pasta)
    alheios = [m for m in re.findall(r"^([.#][\w.#\-> ]+)\{", trecho, re.M)
               if not m.startswith(".capa") and m not in (".capa", "#fim")]
    if len(alheios) > 3:
        raise SystemExit("%s: o trecho da capa tem %d seletor(es) que nao sao `.capa` "
                         "(%s...) — nao vou apagar o que nao e' capa."
                         % (pasta, len(alheios), ", ".join(alheios[:4])))
    gen = CENAS[p["cena"]](p, S)
    css_cena, html_js = gen[0], gen[1]
    tem_ceu = len(gen) > 2
    bloco = css_base(p, S) + css_cena + REDUZ
    h = h[:ini] + bloco + h[fim:]
    # peças FORA da capa (a dupla da rima, o silbox…) usavam @keyframes que moravam
    # no bloco antigo da capa; sem eles o elemento com opacity:0 fica invisível
    # para sempre (portão 4c3). Repor só os que ainda são usados.
    for nome, corpo in ANTIGOS.items():
        if re.search(r"animation\s*:\s*" + nome + r"\b", h) and not re.search(r"@keyframes\s+" + nome + r"\b", h):
            h = h.replace(REDUZ, kfs(nome, corpo) + REDUZ, 1)

    # --- 3) o f0
    m = re.search(r"function f0\(d\)\{.*?\n\}\n", j, re.S)
    if not m:
        raise SystemExit("%s: nao achei `function f0(d){` no folhas.js" % pasta)
    velho = m.group(0)
    mn = re.search(r'nome\s*=\s*"([^"]*)"', velho)
    ms = re.search(r"<div class=\"sub\">(.*?)</div>", velho, re.S)
    if not mn or not ms:
        raise SystemExit("%s: nao achei nome/sub no f0 antigo" % pasta)
    nome, sub = mn.group(1), ms.group(1)
    ceu = "" if tem_ceu else "'<div class=\"ceu\"></div>' + "
    f0 = u'''function f0(d){
  /* CAPA COM IDENTIDADE PRÓPRIA — gerada por _padrao/identidade_capa.py (editar lá).
     Cena: %(nota)s. O título entra letra a letra (%(letra)s), palavra por palavra
     (nowrap, para não quebrar no meio); as figuras são as do próprio caderno. */
  var c = el("div", "capa"), nome = "%(nome)s", k, letras = "", pos = 0;
  var V = typeof VIMG !== "undefined" ? VIMG : 2;
  nome.split(" ").forEach(function(pal, w){
    var s = "";
    for(k = 0; k < pal.length; k++, pos++){
      s += '<span class="lt" style="animation-delay:' + (0.05 * pos).toFixed(2) + 's">' + pal.charAt(k) + '</span>';
    }
    pos++;
    letras += (w ? '<span class="cpesp"></span>' : '') + '<span class="cptpal">' + s + '</span>';
  });
  c.innerHTML =
    %(ceu)s'<h1 class="titu">' + letras + '</h1>' +
    '<div class="sub">%(sub)s</div>' +
    %(html)s +
    '<div class="chamada">Escreva o seu nome ali embaixo e toque em <b>Começar</b>.</div>';
  d.appendChild(c);
}
''' % dict(nota=p["nota"], letra=p["letra"], nome=nome, sub=sub, ceu=ceu, html=html_js)
    j = j[:m.start()] + f0 + j[m.end():]

    io.open(ih, "w", encoding="utf-8").write(h)
    io.open(jf, "w", encoding="utf-8").write(j)
    # ⚠️ A MEDIDA E' DO PORTAO, nao minha: se a cor nova virou tinta extrema sem
    #    fundo em alguma regra do caderno, o `_qa/cor_fixa.py` acusa. Aconteceu com
    #    `_jogo1` (#37474f) e `_mont1` (#795548), cujos literais antigos eram TEXTO.
    import subprocess
    r = subprocess.run(["python3", "_qa/cor_fixa.py", ih], capture_output=True, text=True)
    if r.returncode == 1:
        linhas = [l for l in r.stdout.split("\n") if l.strip().startswith("-")][:4]
        raise SystemExit("%s: com a cor %s o `_qa/cor_fixa.py` reprova (tinta extrema sem "
                         "fundo proprio):\n%s\n   escolha uma cor base mais clara para este caderno."
                         % (pasta, p["cor"], "\n".join(linhas)))
    print("%-9s cor %s  cena %-8s  letra %-8s  figs %d  -> gravado" % (pasta, p["cor"], p["cena"], p["letra"], len(p["figs"])))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cores = {}
    for k, v in ESPEC.items():
        cores.setdefault(v["cor"].lower(), []).append(k)
    rep = [(c, ps) for c, ps in cores.items() if len(ps) > 1]
    if rep:
        raise SystemExit("cor repetida na tabela: %r" % rep)
    alvos = sorted(ESPEC) if sys.argv[1] == "--todos" else [a.rstrip("/") for a in sys.argv[1:]]
    for a in alvos:
        if a not in ESPEC:
            raise SystemExit("%s nao esta na tabela ESPEC — acrescente a linha (cor pelo assunto, cena, figuras)" % a)
        aplica(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
