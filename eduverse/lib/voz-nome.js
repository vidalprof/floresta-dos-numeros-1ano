/* ============================================================================
 * voz-nome.js — GANCHO REUTILIZÁVEL: o personagem FALA o nome do aluno.
 * Padrão EduVerse (obrigatório em TODO projeto — ver EDUCAVERSO-CHECKLIST-DE-CENA.md).
 *
 * A voz é SEMPRE gravada por API (edge-tts, voz Antonio) — NUNCA a voz do
 * navegador (SpeechSynthesis é proibida: robótica, inconsistente, e não é a
 * identidade do Byte). Nome fora do banco cai no texto + saudação genérica.
 *
 * COMO USAR (qualquer projeto — voxel/three.js, Phaser, HTML puro):
 *   1) inclua este arquivo:  <script src="voz-nome.js"></script>
 *   2) copie os mp3 do banco pra pasta de áudio do projeto:
 *        cp eduverse/vozes/nomes/*.mp3  <projeto>/audio/
 *   3) no início (após o aluno se identificar):
 *        var idNome = VozNome.idDe(nome);   // 'nome_marina' ou '' se não tiver
 *   4) toque a saudação em cadeia (nome -> saudação -> problema), sem cortar:
 *        VozNome.cadeia(['audio/'+idNome, 'audio/vx_ola_nome'], aoFim);
 *      (use a saudação SEM apelido quando idNome existir; genérica quando não —
 *       senão vira "Marina!... Ôa, grumete!", que soa como duas pessoas).
 *
 * EXPANDIR o banco: acrescente nomes em _lote_falas.json {id:"nome_<slug>",
 * texto:"<Nome>!"} e rode o workflow [audio]; copie os novos mp3 pro banco.
 * ========================================================================== */
(function (glob) {
  // slug do PRIMEIRO nome, IGUAL ao que o workflow gera (NFD, sem acento, minúsculo, só a-z0-9)
  function slug(s) {
    return (s || '').trim().split(/\s+/)[0]
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .toLowerCase().replace(/[^a-z0-9]/g, '');
  }
  // nomes com voz gravada (banco Antonio). Fonte da verdade: eduverse/vozes/nomes-banco.json
  var BANCO = new Set(['agatha','alexandre','alice','amanda','ana','analu','analuz','anthony','antonella','antonio','arthur','aurora','ayla','beatriz','benicio','benjamin','bento','bernardo','bianca','bruna','bruno','bryan','caio','caleb','camila','carolina','catarina','caua','cecile','cecilia','clara','daniel','danilo','davi','diego','duda','eduardo','elisa','eloa','emanuel','emanuelly','emilly','enzo','erick','ester','esther','felipe','fernanda','fernando','gabriel','gabriela','gael','giovanna','guilherme','gustavo','heitor','helena','heloisa','henrique','ian','igor','isaac','isabela','isadora','joao','jose','julia','juliana','kaique','lara','larissa','laura','leo','leticia','levi','live','livia','liz','lorena','lorenzo','luan','lucas','luiza','maite','malu','manuela','marcos','maria','mariana','marina','matheus','melissa','miguel','milena','murilo','nathan','nicolas','nicole','noah','olivia','otavio','pedro','pietra','pietro','rael','rafael','rafaela','ravi','rebeca','rodrigo','ryan','samuel','sarah','sofia','sophia','stella','theo','thiago','valentina','vicente','vitor','vitoria','yasmin','yuri']);
  // toca uma CADEIA de mp3 em ordem, um não corta o outro; ignora id vazio e erro (404)
  function cadeia(ids, aoFim) {
    var f = (ids || []).filter(Boolean);
    (function nxt(k) {
      if (k >= f.length) { if (aoFim) aoFim(); return; }
      var a; try { a = new Audio(f[k] + '.mp3'); a.volume = 0.95; } catch (e) { return nxt(k + 1); }
      a.onended = function () { nxt(k + 1); };
      a.onerror = function () { nxt(k + 1); };
      a.play().catch(function () { nxt(k + 1); });
    })(0);
  }
  glob.VozNome = {
    slug: slug,
    tem: function (nome) { return BANCO.has(slug(nome)); },
    // id do arquivo do nome ('nome_marina') ou '' se não estiver no banco
    idDe: function (nome) { var s = slug(nome); return BANCO.has(s) ? 'nome_' + s : ''; },
    cadeia: cadeia,
    total: BANCO.size
  };
})(typeof window !== 'undefined' ? window : this);
