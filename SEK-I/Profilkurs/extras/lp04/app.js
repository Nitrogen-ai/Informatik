/* ============================================================
   LP04 · Blöcke zeichnen · Controller-Pläne · Controller-Test ·
   Spielpfade (Denkanstöße → Stufen → Bauplan)
   ============================================================ */
(function () {
  'use strict';
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) { return null; } }

  /* ---------- Scratch-Blöcke ---------- */
  var CLOSE = { '(': ')', '[': ']', '{': '}', '⟨': '⟩' };
  function inline(s) {
    var pos = 0;
    function run(closer) {
      var out = '';
      while (pos < s.length) {
        var ch = s[pos];
        if (ch === closer) { pos++; return out; }
        if (CLOSE[ch]) {
          pos++;
          var cat = '';
          if (ch === '{' || ch === '⟨') {
            var m = /^([a-z]+) /.exec(s.slice(pos));
            if (m) { cat = m[1]; pos += m[0].length; }
          }
          var inner = run(CLOSE[ch]);
          if (ch === '(') out += '<span class="slot">' + inner + '</span>';
          else if (ch === '[') out += '<span class="dd">' + inner + '</span>';
          else if (ch === '{') out += '<span class="rep c-' + (cat || 'op') + '">' + inner + '</span>';
          else out += '<span class="bool c-' + (cat || 'op') + '">' + inner + '</span>';
          continue;
        }
        out += esc(ch); pos++;
      }
      return out;
    }
    return run(null);
  }
  function parseScript(src) {
    var root = { kids: [] }, stack = [{ ind: -1, node: root, list: root.kids }];
    src.split('\n').forEach(function (line) {
      if (!line.trim()) return;
      var ind = line.match(/^ */)[0].length / 2;
      var m = /^([a-z]+): ?(.*)$/.exec(line.trim());
      var node = { cat: m ? m[1] : 'ctl', text: m ? m[2] : line.trim(), kids: [] };
      while (stack.length > 1 && stack[stack.length - 1].ind >= ind) stack.pop();
      var parent = stack[stack.length - 1];
      if (node.cat === 'ctl' && node.text === 'sonst') {
        var prev = parent.list[parent.list.length - 1];
        prev.els = [];
        stack.push({ ind: ind, node: prev, list: prev.els });
        return;
      }
      parent.list.push(node);
      stack.push({ ind: ind, node: node, list: node.kids });
    });
    return root.kids;
  }
  function renderNodes(nodes) {
    return nodes.map(function (n) {
      if (n.cat === 'note') return '<div class="sb-note">' + esc(n.text) + '</div>';
      var cls = 'c-' + n.cat;
      var txt = inline(n.text);
      if (n.kids.length || n.els) {
        var h = '<div class="cblk ' + cls + '"><div class="ctop">' + txt + '</div><div class="cin">' + renderNodes(n.kids) + '</div>';
        if (n.els) h += '<div class="cmid">sonst</div><div class="cin">' + renderNodes(n.els) + '</div>';
        return h + '<div class="cbot"></div></div>';
      }
      var hat = n.cat === 'ev' && /^Wenn /.test(n.text) ? ' hat' : (n.cat === 'def' ? ' def' : '');
      return '<div class="blk ' + cls + hat + '">' + txt + '</div>';
    }).join('');
  }
  function renderScripts(src) {
    return src.split(/\n\s*\n/).map(function (part) { return '<div class="sb">' + renderNodes(parseScript(part)) + '</div>'; }).join('');
  }
  function codeBox(list) {
    return list.map(function (c) {
      return '<div class="sb-wrap"><div class="sb-sprite">' + esc(c[0]) + '</div>' + renderScripts(c[1]) + '</div>';
    }).join('');
  }

  /* ---------- Controller-Plan (SVG, A4 quer) ---------- */
  var svgId = 0;
  function ctrlSVG(spec, caption) {
    var W = 297, H = 210, s = '', gid = 'foil' + (++svgId);
    s += '<svg viewBox="-34 -30 365 272" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="' + esc(caption) + '">';
    s += '<defs><linearGradient id="' + gid + '" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#eef2f7"/><stop offset=".5" stop-color="#aab4c3"/><stop offset="1" stop-color="#dfe5ee"/></linearGradient></defs>';
    s += '<rect x="0" y="0" width="' + W + '" height="' + H + '" rx="4" fill="#f4f1e8" stroke="#8a8272" stroke-width="1"/>';
    s += '<text x="' + (W - 6) + '" y="' + (H - 6) + '" text-anchor="end" font-family="JetBrains Mono,monospace" font-size="7" fill="#8a8272">DIN A4</text>';
    spec.pads.forEach(function (p) {
      var pts = [[p.x, p.y]].concat(p.route), d = pts.map(function (q) { return q.join(','); }).join(' ');
      s += '<polyline points="' + d + '" fill="none" stroke="#7d8797" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="7 4" opacity=".85"/>';
    });
    spec.pads.forEach(function (p) {
      if (p.r) s += '<circle cx="' + p.x + '" cy="' + p.y + '" r="' + p.r + '" fill="url(#' + gid + ')" stroke="#6b7486" stroke-width="1.2"/>';
      else s += '<rect x="' + (p.x - p.w / 2) + '" y="' + (p.y - p.h / 2) + '" width="' + p.w + '" height="' + p.h + '" rx="5" fill="url(#' + gid + ')" stroke="#6b7486" stroke-width="1.2"/>';
      var big = p.t.length > 2;
      s += '<text x="' + p.x + '" y="' + (p.y + (big ? -6 : -4)) + '" text-anchor="middle" font-family="Space Grotesk,sans-serif" font-weight="700" font-size="' + (big ? 9 : 13) + '" fill="#1c2433">' + esc(p.t) + '</text>';
      s += '<circle cx="' + p.x + '" cy="' + (p.y + 8) + '" r="3.6" fill="#e0a526" stroke="#8a6410" stroke-width="1"/>';
      var e = p.route[p.route.length - 1], lx = e[0], ly = e[1], anc = 'middle';
      if (ly <= 0) ly = -10; else if (ly >= H) ly = H + 18; else if (lx <= 0) { lx = -5; anc = 'end'; ly += 3; } else { lx = W + 5; anc = 'start'; ly += 3; }
      s += '<rect x="' + (e[0] - 4) + '" y="' + (e[1] - 4) + '" width="8" height="8" rx="1.5" fill="#1c2433"/>';
      s += '<text x="' + lx + '" y="' + ly + '" text-anchor="' + anc + '" font-family="JetBrains Mono,monospace" font-weight="700" font-size="8.5" fill="#35e0ff">' + esc(p.key) + '</text>';
    });
    s += '</svg>';
    return '<div class="ctrl-fig">' + s + '<div class="fig-cap">' + esc(caption) + '</div>' +
      '<div class="legend-row"><span><i class="sw" style="background:#c3cad6"></i>Folien-Taste (vorne)</span><span><i class="sw" style="background:#e0a526;border-radius:50%;width:10px"></i>Loch + Druckknopf</span><span><i class="sw" style="background:repeating-linear-gradient(90deg,#7d8797 0 5px,transparent 5px 8px)"></i>Alustreifen (Rückseite)</span><span><i class="sw" style="background:#1c2433;border:1px solid #9fb0d8"></i>Krokodilklemme → Anschluss</span><span>EARTH: Alu-Armband</span></div></div>';
  }
  function sandwichSVG() {
    return '<svg viewBox="0 0 620 210" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Querschnitt Folientaste mit Druckknopf">' +
      '<defs><linearGradient id="foil2" x1="0" x2="1"><stop offset="0" stop-color="#eef2f7"/><stop offset=".5" stop-color="#aab4c3"/><stop offset="1" stop-color="#dfe5ee"/></linearGradient></defs>' +
      '<text x="20" y="22" font-family="JetBrains Mono,monospace" font-size="12" font-weight="700" fill="#35e0ff">QUERSCHNITT · EINE TASTE</text>' +
      '<rect x="120" y="70" width="140" height="10" fill="url(#foil2)" stroke="#6b7486"/>' +
      '<rect x="40" y="80" width="520" height="16" fill="#f4f1e8" stroke="#8a8272"/>' +
      '<rect x="176" y="96" width="330" height="9" fill="url(#foil2)" stroke="#6b7486"/>' +
      '<rect x="183" y="62" width="14" height="52" rx="3" fill="#e0a526" stroke="#8a6410"/>' +
      '<ellipse cx="190" cy="62" rx="20" ry="7" fill="#e0a526" stroke="#8a6410"/>' +
      '<path d="M183 114 l-12 10 M197 114 l12 10" stroke="#8a6410" stroke-width="4" stroke-linecap="round"/>' +
      '<path d="M500 92 l40 -6 l0 26 l-40 -6 z" fill="#1c2433"/><path d="M540 99 C 575 99, 580 150, 600 160" fill="none" stroke="#ff5d6c" stroke-width="3"/>' +
      '<text x="190" y="44" text-anchor="middle" font-family="Space Grotesk,sans-serif" font-size="13" fill="#e6eeff">Druckknopf im Loch</text>' +
      '<text x="340" y="66" font-family="Space Grotesk,sans-serif" font-size="13" fill="#e6eeff">① Folien-Taste (Vorderseite)</text>' +
      '<line x1="336" y1="62" x2="262" y2="74" stroke="#9fb0d8"/>' +
      '<text x="40" y="130" font-family="Space Grotesk,sans-serif" font-size="13" fill="#e6eeff">② Papier (isoliert)</text>' +
      '<text x="220" y="150" font-family="Space Grotesk,sans-serif" font-size="13" fill="#e6eeff">③ Alustreifen (Rückseite) → zum Rand</text>' +
      '<line x1="300" y1="138" x2="300" y2="106" stroke="#9fb0d8"/>' +
      '<text x="600" y="182" text-anchor="end" font-family="Space Grotesk,sans-serif" font-size="13" fill="#e6eeff">④ Klemme → Makey Makey</text>' +
      '<text x="20" y="200" font-family="JetBrains Mono,monospace" font-size="11" fill="#9fb0d8">Finger auf ① + EARTH-Armband = Stromkreis geschlossen → „Tastendruck“</text>' +
      '</svg><div class="fig-cap">Zwei-Seiten-Prinzip: Taste vorne, Leiterbahn hinten, Druckknopf als Brücke</div>';
  }

  /* ---------- Spielpfade ---------- */
  var AUFSTELLUNG = [].concat(
    ['sT', 'sS', 'sL', 'sD', 'sK', 'sL', 'sS', 'sT'], Array(8).fill('sB'), Array(32).fill('--'),
    Array(8).fill('wB'), ['wT', 'wS', 'wL', 'wD', 'wK', 'wL', 'wS', 'wT']);

  function buildGames() {
    var gHost = document.getElementById('games'), tHost = document.getElementById('tracks');
    if (!gHost || typeof GAMES === 'undefined') return;
    GAMES.forEach(function (g) {
      var card = document.createElement('button');
      card.type = 'button'; card.className = 'game'; card.style.setProperty('--gc', g.color); card.dataset.game = g.id;
      card.innerHTML = '<div class="g-ic">' + g.icon + '</div><div class="g-t">' + esc(g.title) + '</div><div class="g-lv">' + esc(g.level) + '</div><div class="g-d">' + esc(g.blurb) + '</div><div class="g-prog"></div>';
      gHost.appendChild(card);

      var tr = document.createElement('div');
      tr.className = 'track'; tr.id = 'track-' + g.id; tr.style.setProperty('--gc', g.color);
      var h = '<div class="track-head"><h3>' + g.icon + ' ' + esc(g.title) + '</h3><span class="g-lv">' + esc(g.level) + '</span></div>';
      h += '<h3 style="margin-top:.2rem">Denkanstöße — erst selbst überlegen</h3><div class="denk">';
      g.denk.forEach(function (d) { h += '<details><summary><span class="dk-t">' + esc(d[0]) + '</span>' + esc(d[1]) + '</summary><div class="ans">' + d[2] + '</div></details>'; });
      h += '</div><div class="stepper">';
      g.stages.forEach(function (st, i) { h += '<button type="button" class="chip" data-i="' + i + '">' + (i + 1) + ' · ' + esc(st.t) + '</button>'; });
      h += '<button type="button" class="chip bp" data-i="' + g.stages.length + '">★ Bauplan</button></div>';
      g.stages.forEach(function (st, i) {
        h += '<div class="stage" data-i="' + i + '"><div class="stage-top"><h4>Stufe ' + (i + 1) + ' · ' + esc(st.t) + '</h4><span class="time">' + esc(st.time) + '</span></div>';
        h += '<span class="lbl">Ziel</span><p>' + esc(st.goal) + '</p><span class="lbl">So geht’s</span>' + st.html;
        if (st.ctrl) st.ctrl.forEach(function (c) { var sp = CTRL_PAD[c[0]](c[1]); h += ctrlSVG(sp, c[2]); });
        if (st.tip) h += '<p class="note"><b>Denk-Tipp:</b> ' + st.tip + '</p>';
        var hasCode = st.code && st.code.length;
        if (hasCode) h += '<div class="codebox" hidden>' + codeBox(st.code) + '</div>';
        h += '<div class="stage-actions">' + (hasCode ? '<button type="button" class="btn ghost" data-act="code">🧩 Blöcke zeigen</button>' : '') +
          '<button type="button" class="btn" data-act="next">Weiter →</button><label><input type="checkbox" data-act="done"> geschafft</label></div></div>';
      });
      h += '<div class="stage" data-i="' + g.stages.length + '"><div class="stage-top"><h4>★ Vollständiger Bauplan</h4><span class="time">alles auf einen Blick</span></div>';
      h += '<span class="lbl">Das braucht dein Projekt</span><div class="setup">' + g.setup.map(function (x) { return '<div><b>' + esc(x[0]) + '</b>' + esc(x[1]) + '</div>'; }).join('') + '</div>';
      h += '<span class="lbl">Alle Skripte</span>' + codeBox(g.plan) + '<p class="note">' + g.extra + '</p>';
      h += '<div class="stage-actions"><label><input type="checkbox" data-act="done"> Spiel läuft!</label></div></div>';
      tr.innerHTML = h;
      tHost.appendChild(tr);

      var chips = tr.querySelectorAll('.chip'), stages = tr.querySelectorAll('.stage');
      function show(i) {
        chips.forEach(function (c) { c.classList.toggle('active', +c.dataset.i === i); });
        stages.forEach(function (s) { s.classList.toggle('active', +s.dataset.i === i); });
        store('pi9_lp04_stage_' + g.id, String(i));
      }
      function refreshDone() {
        var n = 0;
        stages.forEach(function (s) {
          var i = s.dataset.i, done = store('pi9_lp04_done_' + g.id + '_' + i) === '1';
          var cb = s.querySelector('[data-act="done"]'); if (cb) cb.checked = done;
          tr.querySelector('.chip[data-i="' + i + '"]').classList.toggle('done', done);
          if (done) n++;
        });
        card.querySelector('.g-prog').textContent = n ? n + ' / ' + stages.length + ' Stufen geschafft' : '';
      }
      chips.forEach(function (c) { c.addEventListener('click', function () { show(+c.dataset.i); }); });
      stages.forEach(function (s) {
        var i = +s.dataset.i;
        s.addEventListener('click', function (ev) {
          var a = ev.target.closest('[data-act]'); if (!a) return;
          if (a.dataset.act === 'code') {
            var box = s.querySelector('.codebox'); box.hidden = !box.hidden;
            a.textContent = box.hidden ? '🧩 Blöcke zeigen' : '🧩 Blöcke verbergen';
          } else if (a.dataset.act === 'next') {
            show(Math.min(i + 1, stages.length - 1));
            tr.querySelector('.stepper').scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        });
        var cb = s.querySelector('[data-act="done"]');
        if (cb) cb.addEventListener('change', function () { store('pi9_lp04_done_' + g.id + '_' + i, cb.checked ? '1' : null); refreshDone(); });
      });
      var saved = parseInt(store('pi9_lp04_stage_' + g.id), 10);
      show(isNaN(saved) ? 0 : Math.min(saved, stages.length - 1));
      refreshDone();

      card.addEventListener('click', function () { openGame(g.id, true); });
    });
    function openGame(id, scroll) {
      gHost.querySelectorAll('.game').forEach(function (c) { c.classList.toggle('active', c.dataset.game === id); });
      tHost.querySelectorAll('.track').forEach(function (t) { t.classList.toggle('active', t.id === 'track-' + id); });
      store('pi9_lp04_game', id);
      if (scroll) setTimeout(function () { document.getElementById('track-' + id).scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 60);
    }
    var last = store('pi9_lp04_game');
    if (last && document.getElementById('track-' + last)) openGame(last, false);

    document.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-dl="aufstellung"]'); if (!b) return;
      var blob = new Blob([AUFSTELLUNG.join('\n') + '\n'], { type: 'text/plain' });
      var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'aufstellung.txt';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    });
  }

  /* ---------- Controller-Test + Mini-Tic-Tac-Toe ---------- */
  function initTester() {
    var btn = document.getElementById('ct-toggle'); if (!btn) return;
    var status = document.getElementById('ct-status'), active = false;
    var lamps = {}; document.querySelectorAll('#controller-test .lamp').forEach(function (l) { lamps[l.dataset.k] = l; });
    var grid = document.getElementById('ttt'), msg = document.getElementById('ttt-msg'), cells = [];
    for (var i = 0; i < 9; i++) { var c = document.createElement('div'); grid.appendChild(c); cells.push(c); }
    var board, cur, player, over;
    function reset() { board = Array(9).fill(0); cur = 4; player = 1; over = false; paint(); msg.textContent = active ? 'Spieler ✕ ist dran.' : 'Starte den Test, dann: Spieler ✕ ist dran.'; }
    function paint() { cells.forEach(function (c, i) { c.textContent = board[i] === 1 ? '✕' : board[i] === 2 ? '○' : ''; c.className = (i === cur ? 'cur ' : '') + (board[i] ? 'p' + board[i] : ''); }); }
    var LINES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
    function place() {
      if (over) { reset(); return; }
      if (board[cur]) { msg.textContent = 'Feld belegt — anderes wählen.'; return; }
      board[cur] = player;
      var win = LINES.some(function (l) { return l.every(function (k) { return board[k] === player; }); });
      if (win) { over = true; msg.textContent = (player === 1 ? '✕' : '○') + ' gewinnt! SPACE = neues Spiel'; }
      else if (board.every(Boolean)) { over = true; msg.textContent = 'Unentschieden! SPACE = neues Spiel'; }
      else { player = 3 - player; msg.textContent = 'Spieler ' + (player === 1 ? '✕' : '○') + ' ist dran.'; }
      paint();
    }
    function norm(k) { return k.length === 1 ? k.toLowerCase() : k; }
    function lamp(k, on) { var l = lamps[k]; if (l) l.classList.toggle('on', on); }
    document.addEventListener('keydown', function (e) {
      if (!active) return;
      var k = norm(e.key);
      if (lamps[k]) { e.preventDefault(); lamp(k, true); status.textContent = 'Signal: ' + ({ ' ': 'Leertaste', ArrowUp: 'Pfeil nach oben', ArrowDown: 'Pfeil nach unten', ArrowLeft: 'Pfeil nach links', ArrowRight: 'Pfeil nach rechts' }[k] || k.toUpperCase()); }
      if (e.repeat) return;
      var r = Math.floor(cur / 3), col = cur % 3;
      if (k === 'ArrowRight' && col < 2) cur++;
      else if (k === 'ArrowLeft' && col > 0) cur--;
      else if (k === 'ArrowDown' && r < 2) cur += 3;
      else if (k === 'ArrowUp' && r > 0) cur -= 3;
      else if (k === ' ') place();
      paint();
    });
    document.addEventListener('keyup', function (e) { if (active) lamp(norm(e.key), false); });
    document.addEventListener('mousedown', function (e) { if (active && e.target !== btn) { lamp('click', true); status.textContent = 'Signal: Klick'; } });
    document.addEventListener('mouseup', function () { lamp('click', false); });
    btn.addEventListener('click', function () {
      active = !active;
      btn.textContent = active ? '■ Test beenden' : '▶ Test starten';
      btn.classList.toggle('on', active);
      status.textContent = active ? 'Test läuft — Pfeiltasten und Leertaste werden hier abgefangen.' : 'Test ist aus — Pfeiltasten scrollen normal.';
      reset();
    });
    reset();
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('pre.sbsrc').forEach(function (p) {
      var d = document.createElement('div'); d.className = 'sb'; d.innerHTML = renderNodes(parseScript(p.textContent.trim()));
      p.replaceWith(d);
    });
    var sw = document.getElementById('fig-sandwich'); if (sw) sw.innerHTML = sandwichSVG();
    buildGames();
    initTester();
  });
})();
