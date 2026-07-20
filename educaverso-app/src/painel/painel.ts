// ============================================================================
// PAINEL DO PROFESSOR (?painel) — a camada PROVA visível: evidências por turma e
// aluno, nível da rubrica BNCC, PARECER DESCRITIVO em rascunho (editável) e nota
// sugerida por tabela fixa. Login = a MESMA conta da Agenda de Aulas (matrícula +
// senha); a leitura só funciona para o professor-admin (regra do RTDB). Sem
// internet/regra, mostra as evidências locais desta máquina (aviso honesto).
// ============================================================================
import { RAIZ, type Evidencia, evidenciasLocais, nivelRubrica, gerarParecer, NOTA_SUGERIDA, san } from '../fabrica/evidencias'

const API_KEY = 'AIzaSyCWX-lK7pr6yW_E5jDvDhVewe20lB3E6Ks'
const DB = 'https://atividades-educativas-16860-default-rtdb.firebaseio.com'

async function fx (url: string, opts?: RequestInit, ms = 9000): Promise<Response> {
  const ctl = new AbortController()
  const t = setTimeout(() => ctl.abort(), ms)
  try { return await fetch(url, { ...opts, signal: ctl.signal }) } finally { clearTimeout(t) }
}

async function loginProf (matricula: string, senha: string): Promise<string | null> {
  try {
    const email = `${san(matricula)}@vidalramos.agenda`
    const r = await fx(`https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=${API_KEY}`,
      { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password: senha, returnSecureToken: true }) })
    if (!r.ok) return null
    const j = await r.json()
    return j.idToken || null
  } catch { return null }
}

type Arvore = Record<string, Record<string, Record<string, Evidencia>>>   // turma -> aluno -> id -> ev

export function montarPainel (): void {
  document.body.style.background = '#0e1524'
  const host = document.createElement('div')
  host.style.cssText = 'position:fixed;inset:0;overflow:auto;background:linear-gradient(160deg,#10203f,#0a1226);color:#eaf1ff;font-family:system-ui,Arial,sans-serif;padding:20px 14px;z-index:60'
  host.innerHTML = `
    <div style="max-width:760px;margin:0 auto">
      <h1 style="font-size:22px;margin:.2em 0">📋 Painel do Professor — EducaVerso</h1>
      <p style="color:#a9bde6;font-size:13px;margin:.3em 0 12px">Evidências das missões → rubrica BNCC → parecer descritivo (rascunho editável) → nota sugerida. <b>A evidência sugere; quem avalia é o professor.</b></p>
      <div id="plogin" style="display:grid;gap:8px;max-width:340px">
        <input id="p_mat" placeholder="Matrícula (a mesma da Agenda)" style="padding:10px;border-radius:8px;border:0">
        <input id="p_sen" type="password" placeholder="Senha" style="padding:10px;border-radius:8px;border:0">
        <button id="p_entrar" style="padding:12px;font-weight:800;border:0;border-radius:10px;background:#57e08a;color:#0b2350;cursor:pointer">Entrar</button>
        <div id="p_erro" style="color:#ffb3b3;font-size:13px;min-height:18px"></div>
        <button id="p_local" style="padding:8px;border:0;border-radius:8px;background:#26355c;color:#cdd9f5;cursor:pointer;font-size:13px">Ver só as evidências DESTA máquina (sem login)</button>
      </div>
      <div id="pconteudo"></div>
    </div>`
  document.body.appendChild(host)
  const $ = (id: string): HTMLElement => document.getElementById(id)!

  function render (arv: Arvore, aviso: string): void {
    $('plogin').style.display = 'none'
    const cont = $('pconteudo')
    const turmas = Object.keys(arv).sort()
    if (!turmas.length) { cont.innerHTML = `<p>${aviso}</p><p style="color:#a9bde6">Nenhuma evidência registrada ainda. Peça às crianças para jogarem identificadas (nome + turma na abertura do jogo).</p>`; return }
    let html = aviso ? `<p style="color:#ffd27f;font-size:13px">${aviso}</p>` : ''
    for (const turma of turmas) {
      html += `<h2 style="font-size:18px;margin:16px 0 6px">🏫 ${turma}</h2>`
      for (const aluno of Object.keys(arv[turma]).sort()) {
        const evs = Object.values(arv[turma][aluno]).sort((a, b) => (a.quando < b.quando ? -1 : 1))
        const nome = evs[0]?.nome || aluno
        const ult = evs[evs.length - 1]
        const nivel = nivelRubrica(ult)
        const cor = nivel === 'Consolidado' ? '#57e08a' : nivel === 'Em desenvolvimento' ? '#ffd166' : '#ff9f7f'
        const linhas = evs.map(e => `<tr><td>${new Date(e.quando).toLocaleDateString('pt-BR')}</td><td>${e.mecanica}${e.estrategia ? ' (' + e.estrategia + ')' : ''}</td><td>${e.erros}</td><td>${['sem ajuda', 'pergunta', 'passo a passo'][e.nivelAjuda]}</td><td>${nivelRubrica(e)}</td></tr>`).join('')
        const parecer = gerarParecer(nome, evs)
        const idp = `par_${san(turma)}_${san(aluno)}`
        html += `
        <details style="background:#16244a;border-radius:12px;padding:10px 14px;margin:8px 0">
          <summary style="cursor:pointer;font-weight:700">${nome} — <span style="color:${cor}">${nivel}</span> <span style="color:#8fa3cf;font-weight:400">(${evs.length} missão(ões) · nota sugerida ${NOTA_SUGERIDA[nivel]})</span></summary>
          <table style="width:100%;font-size:12px;border-collapse:collapse;margin:10px 0;color:#cdd9f5">
            <tr style="text-align:left;color:#8fa3cf"><th>Data</th><th>Missão</th><th>Erros</th><th>Ajuda</th><th>Nível</th></tr>${linhas}
          </table>
          <label style="font-size:13px;color:#a9bde6">Parecer descritivo (rascunho — edite à vontade):</label>
          <textarea id="${idp}" style="width:100%;min-height:110px;border-radius:8px;border:0;padding:8px;font:13px system-ui;margin:6px 0">${parecer}</textarea>
          <button onclick="navigator.clipboard.writeText(document.getElementById('${idp}').value).then(()=>this.textContent='✅ Copiado!')" style="padding:8px 14px;border:0;border-radius:8px;background:#57e08a;color:#0b2350;font-weight:700;cursor:pointer">Copiar parecer</button>
        </details>`
      }
    }
    html += `<p style="color:#7f93bd;font-size:12px;margin-top:14px">Rubrica (regra fixa e auditável): sem ajuda e sem erro = <b>Consolidado</b> · acertou após refletir (pergunta do mentor / botão ❓) = <b>Em desenvolvimento</b> · precisou do passo a passo = <b>Iniciando</b>. Régua de nota sugerida: Consolidado 8,5–10 · Em desenvolvimento 6,0–8,4 · Iniciando &lt;6,0 (ajuste à régua da escola).</p>`
    cont.innerHTML = html
  }

  ;($('p_entrar') as HTMLButtonElement).onclick = async () => {
    const erro = $('p_erro'); erro.textContent = ''
    const tok = await loginProf((document.getElementById('p_mat') as HTMLInputElement).value, (document.getElementById('p_sen') as HTMLInputElement).value)
    if (!tok) { erro.textContent = 'Login falhou. Confira matrícula e senha (as mesmas da Agenda).'; return }
    try {
      const r = await fx(`${DB}${RAIZ}.json?auth=${tok}`)
      if (r.status === 401 || r.status === 403) { erro.textContent = 'Sem permissão: este acesso é só do professor administrador (veja FIREBASE-EDUCAVERSO.md).'; return }
      if (!r.ok) { erro.textContent = 'Não consegui ler as evidências (rede/regra). Tente "só desta máquina".'; return }
      render((await r.json()) || {}, '')
    } catch { erro.textContent = 'Sem internet até o banco. Tente "só desta máquina".' }
  }

  ;($('p_local') as HTMLButtonElement).onclick = () => {
    const arv: Arvore = {}
    evidenciasLocais().forEach((e, i) => {
      const t = e.turma || '(sem turma)'; const a = san(e.nome || 'sem-nome')
      arv[t] = arv[t] || {}; arv[t][a] = arv[t][a] || {}; arv[t][a]['l' + i] = e
    })
    render(arv, '⚠️ Modo local: mostrando apenas as evidências gravadas NESTE computador.')
  }
  ;(window as any).__painel = { render }   // QA
}
