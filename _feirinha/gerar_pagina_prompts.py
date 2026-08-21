# -*- coding: utf-8 -*-
u"""Lê _feirinha/PROMPTS-IMAGENS.md e gera uma PÁGINA (HTML) com cada prompt num
cartão e um botão COPIAR — como o Marcos gosta ('como antes, com botão de copiar').
Saída: _feirinha/prompts.html (publicada como artifact)."""
import io, os, re, html

BASE = os.path.dirname(os.path.abspath(__file__))
md = io.open(os.path.join(BASE, u"PROMPTS-IMAGENS.md"), encoding="utf-8").read()

# --- parse: (secao H1, rotulo H2, "vem nela", codigo) ---
linhas = md.split(u"\n")
sec = u""; rot = u""; vem = u""
itens = []           # (sec, rot, vem, codigo)
i = 0
while i < len(linhas):
    ln = linhas[i]
    if ln.startswith(u"# "):
        sec = ln[2:].strip(); rot = u""; vem = u""
    elif ln.startswith(u"## "):
        rot = ln[3:].strip(); vem = u""
    elif ln.startswith(u"Vem nela:"):
        vem = ln.replace(u"Vem nela:", u"").strip()
    elif ln.strip().startswith(u"```"):
        buf = []
        i += 1
        while i < len(linhas) and not linhas[i].strip().startswith(u"```"):
            buf.append(linhas[i]); i += 1
        itens.append((sec, rot, vem, u"\n".join(buf).strip()))
    i += 1

def limpa_rot(r):
    return r.replace(u"`", u"").strip()
def md_neg(t):
    return re.sub(r"\*\*(.+?)\*\*", lambda m: u"<b>"+html.escape(m.group(1))+u"</b>", html.escape(t))

# agrupa por seção, na ordem de aparição
ordem = []
grupos = {}
for sec, rot, vem, cod in itens:
    if sec not in grupos:
        grupos[sec] = []; ordem.append(sec)
    grupos[sec].append((limpa_rot(rot), vem, cod))

# ícones por seção
def icone(sec):
    s = sec.lower()
    if u"cartela" in s or u"peca" in s: return u"🗂️"
    if u"mascote" in s and u"camada" not in s: return u"🦉"
    if u"camada" in s: return u"🎭"
    if u"cracha" in s: return u"🧒"
    if u"fundo" in s: return u"🏞️"
    if u"medalha" in s: return u"🏅"
    if u"figura" in s: return u"🍎"
    return u"🎨"

cards = []
n = 0
for sec in ordem:
    cards.append(u'<h2 class="sec">%s %s</h2>' % (icone(sec), html.escape(sec)))
    for rot, vem, cod in grupos[sec]:
        n += 1
        vh = (u'<div class="vem">Vem nela: %s</div>' % md_neg(vem)) if vem else u""
        cards.append(
          u'<div class="card">'
          u'<div class="chead"><span class="fn">%s</span>'
          u'<button class="cp" onclick="copiar(this)">Copiar</button></div>'
          u'%s<pre>%s</pre></div>' % (html.escape(rot) or u"(sem nome)", vh, html.escape(cod)))

CARDS = u"\n".join(cards)

PAGE = u"""<title>Prompts — Feirinha da Dona Coruja</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Nunito:wght@600;700;800&display=swap');
:root{
  --creme:#fff6e6; --papel:#fffdf7; --madeira:#8a5a2b; --madeira-esc:#6e4420;
  --tinta:#43301a; --tinta2:#7a5c3c; --linha:#eddcb8; --verde:#4c9a4a;
  --laranja:#f0902f; --code-bg:#fffaf0; --code-tt:#4a3a10; --chip:#ffeccb;
  --sombra:0 8px 22px rgba(90,60,20,.14);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --creme:#1a1510; --papel:#241d15; --madeira:#d5a86a; --madeira-esc:#e7c48c;
  --tinta:#f2e9db; --tinta2:#c9b79c; --linha:#3a2e20; --verde:#7ac074;
  --laranja:#f0a24f; --code-bg:#15100a; --code-tt:#f0e2c8; --chip:#33281a;
  --sombra:0 8px 22px rgba(0,0,0,.4);
}}
:root[data-theme="dark"]{
  --creme:#1a1510; --papel:#241d15; --madeira:#d5a86a; --madeira-esc:#e7c48c;
  --tinta:#f2e9db; --tinta2:#c9b79c; --linha:#3a2e20; --verde:#7ac074;
  --laranja:#f0a24f; --code-bg:#15100a; --code-tt:#f0e2c8; --chip:#33281a;
  --sombra:0 8px 22px rgba(0,0,0,.4);
}
*{box-sizing:border-box}
body{margin:0;background:var(--creme);color:var(--tinta);
  font-family:'Nunito',system-ui,Segoe UI,Arial,sans-serif;line-height:1.5}
.wrap{max-width:820px;margin:0 auto;padding:22px 18px 60px}
.top{text-align:center;margin:6px 0 18px}
.top h1{font-family:'Baloo 2','Nunito',cursive;font-weight:800;margin:.1em 0;
  font-size:clamp(26px,6vw,38px);color:var(--madeira-esc);line-height:1.05}
.top p{margin:.3em auto;max-width:600px;color:var(--tinta2);font-weight:600}
.nota{background:var(--chip);border:2px dashed var(--laranja);border-radius:14px;
  padding:10px 14px;margin:14px 0;font-weight:600;color:var(--madeira-esc)}
.sec{font-family:'Baloo 2','Nunito',cursive;font-weight:800;color:var(--madeira-esc);
  margin:26px 0 8px;padding-bottom:6px;border-bottom:3px solid var(--linha);font-size:20px}
.card{background:var(--papel);border:1px solid var(--linha);border-radius:16px;
  box-shadow:var(--sombra);padding:12px 14px 14px;margin:12px 0}
.chead{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:6px}
.fn{font-family:'Baloo 2','Nunito',monospace;font-weight:800;color:var(--madeira-esc);
  font-size:15px;word-break:break-all}
.vem{font-size:14px;color:var(--tinta2);margin:0 0 8px}
.cp{flex:none;cursor:pointer;border:none;border-radius:12px;font-weight:800;
  font-family:'Nunito',sans-serif;font-size:14px;padding:9px 16px;color:#fff;
  background:linear-gradient(var(--laranja),#d97d1e);
  box-shadow:0 4px 0 rgba(120,70,10,.35);transition:transform .08s,box-shadow .08s}
.cp:active{transform:translateY(2px);box-shadow:0 2px 0 rgba(120,70,10,.35)}
.cp.ok{background:linear-gradient(var(--verde),#3a7a38);box-shadow:0 4px 0 rgba(20,80,20,.4)}
pre{background:var(--code-bg);color:var(--code-tt);border:1px solid var(--linha);
  border-radius:12px;padding:12px;margin:0;white-space:pre-wrap;word-wrap:break-word;
  font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;line-height:1.45;
  max-height:none;overflow-x:auto}
.foot{text-align:center;color:var(--tinta2);font-size:13px;margin-top:30px}
</style>

<div class="wrap">
  <div class="top">
    <h1>🦉 Prompts da Feirinha da Dona Coruja</h1>
    <p>Matemática · 2º ano · problemas de +/−. Estilo <b>clay 3D storybook</b> da casa.
    Toque em <b>Copiar</b> e cole no gerador. Nome do arquivo = o que está no cartão.</p>
  </div>
  <div class="nota">💰 <b>Prefira as CARTELAS</b> (várias peças numa folha só): saem irmãs
   (mesma luz/escala) e é mais barato. As frutas comuns já vêm do banco — não precisa gerar.</div>
  __CARDS__
  <div class="foot">Gerado do <code>PROMPTS-IMAGENS.md</code> · %d prompts · salve tudo em <code>_feirinha/img/</code></div>
</div>

<script>
function copiar(btn){
  var pre=btn.closest('.card').querySelector('pre');
  var txt=pre.innerText;
  var ok=function(){var o=btn.textContent;btn.textContent='Copiado!';btn.classList.add('ok');
    setTimeout(function(){btn.textContent='Copiar';btn.classList.remove('ok');},1400);};
  var fb=function(){var ta=document.createElement('textarea');ta.value=txt;
    ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);
    ta.focus();ta.select();try{document.execCommand('copy');ok();}catch(e){}
    document.body.removeChild(ta);};
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(txt).then(ok,fb);
  }else{fb();}
}
</script>
""" % (n,)

PAGE = PAGE.replace(u"__CARDS__", CARDS)
out = os.path.join(BASE, u"prompts.html")
io.open(out, "w", encoding="utf-8").write(PAGE)
print(u"prompts:", n, u"->", out)
