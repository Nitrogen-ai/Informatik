/* ============================================================
   LP04 · Druckvorlagen: A4-Controller im Maßstab 1:1 (mm)
   nutzt CTRL_PAD aus games.js · Vorderseite + gespiegelte Rückseite
   ============================================================ */
(function () {
  'use strict';
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  var W = 297, H = 210, S = 0.9, OX = (W - W * S) / 2, OY = 12;
  var SHEETS = [
    { spec: CTRL_PAD.pad('SPACE'), name: 'Steuerkreuz', use: 'Tic Tac Toe · Schiffe versenken · Schach', hint: 'SPACE-Taste beschriften: SETZEN / FEUER / WÄHLEN' },
    { spec: CTRL_PAD.einwurf(), name: 'Einwurf-Leiste', use: 'Vier gewinnt', hint: '' },
    { spec: CTRL_PAD.tttFeld(), name: 'Feld-Controller 3 × 3', use: 'Tic Tac Toe · Profi', hint: 'W–G an die Rückseiten-Buchsen (Steckkabel), Rest vorne' },
    { spec: CTRL_PAD.c4Feld(), name: 'Spalten-Controller', use: 'Vier gewinnt · Profi', hint: 'W–G an die Rückseiten-Buchsen (Steckkabel), 7. Spalte = SPACE' }
  ];
  function T(x, y, mirror) { var X = OX + x * S, Y = OY + y * S; return [mirror ? W - X : X, Y]; }
  function sheetSVG(sh, back) {
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg" font-family="Space Grotesk, Arial, sans-serif">';
    s += '<rect x="0" y="0" width="' + W + '" height="' + H + '" fill="#fff"/>';
    var f = T(0, 0, false), g = T(W, H, false);
    s += '<rect x="' + f[0] + '" y="' + f[1] + '" width="' + (g[0] - f[0]) + '" height="' + (g[1] - f[1]) + '" fill="none" stroke="#bbb" stroke-width=".3" stroke-dasharray="2 2"/>';
    s += '<text x="' + OX + '" y="7" font-size="4.2" font-weight="700" fill="#222">' + esc(sh.name) + ' · ' + (back ? 'RÜCKSEITE (gespiegelt)' : 'VORDERSEITE') + '</text>';
    s += '<text x="' + (W - OX) + '" y="7" text-anchor="end" font-size="3.2" fill="#666">' + esc(sh.use) + ' · Profil Informatik LP04</text>';
    sh.spec.pads.forEach(function (p) {
      var c = T(p.x, p.y, back);
      if (back) {
        var pts = [[p.x, p.y]].concat(p.route).map(function (q) { return T(q[0], q[1], true).join(','); }).join(' ');
        s += '<polyline points="' + pts + '" fill="none" stroke="#8a95a8" stroke-width="' + (6 * S) + '" stroke-linecap="round" stroke-linejoin="round" opacity=".45"/>';
        s += '<polyline points="' + pts + '" fill="none" stroke="#333" stroke-width=".3" stroke-dasharray="1.5 1.2"/>';
        var e = p.route[p.route.length - 1], E = T(e[0], e[1], true);
        s += '<rect x="' + (E[0] - 3) + '" y="' + (E[1] - 3) + '" width="6" height="6" fill="#222"/>';
        var lx = E[0], ly = E[1], anc = 'middle';
        if (e[1] <= 0) ly += 9;
        else if (e[1] >= H) ly -= 5;
        else if (e[0] <= 0) { lx -= 2; anc = 'end'; ly -= 5; }   // links → gespiegelt rechts
        else { lx += 2; anc = 'start'; ly -= 5; }
        s += '<text x="' + lx + '" y="' + ly + '" text-anchor="' + anc + '" font-size="4" font-weight="700" fill="#0b6b87">Klemme → ' + esc(p.key) + '</text>';
      } else {
        var P = T(p.x, p.y, false);
        if (p.r) s += '<circle cx="' + P[0] + '" cy="' + P[1] + '" r="' + p.r * S + '" fill="#f1f3f6" stroke="#333" stroke-width=".4" stroke-dasharray="2 1.2"/>';
        else s += '<rect x="' + (P[0] - p.w * S / 2) + '" y="' + (P[1] - p.h * S / 2) + '" width="' + p.w * S + '" height="' + p.h * S + '" rx="2" fill="#f1f3f6" stroke="#333" stroke-width=".4" stroke-dasharray="2 1.2"/>';
        var big = p.t.length > 2;
        s += '<text x="' + P[0] + '" y="' + (P[1] - 5) + '" text-anchor="middle" font-size="' + (big ? 6 : 9) + '" font-weight="700" fill="#555">' + esc(p.t) + '</text>';
        s += '<text x="' + P[0] + '" y="' + (P[1] + 8) + '" text-anchor="middle" font-size="2.6" fill="#888">Alufolie</text>';
        var e2 = p.route[p.route.length - 1], E2 = T(e2[0], e2[1], false);
        s += '<text x="' + E2[0] + '" y="' + (e2[1] <= 0 ? E2[1] + 5 : e2[1] >= H ? E2[1] - 2 : E2[1] + 1.5) + '" text-anchor="' + (e2[0] <= 0 ? 'start' : e2[0] >= W ? 'end' : 'middle') + '" font-size="4.5" font-weight="700" fill="#0b6b87">' + esc(e2[0] <= 0 ? '◂ ' + p.key : e2[0] >= W ? p.key + ' ▸' : e2[1] >= H ? p.key + ' ▾' : p.key + ' ▴') + '</text>';
      }
      s += '<circle cx="' + c[0] + '" cy="' + c[1] + '" r="2.4" fill="none" stroke="#c0392b" stroke-width=".4"/>';
      s += '<path d="M' + (c[0] - 4) + ' ' + c[1] + 'h8M' + c[0] + ' ' + (c[1] - 4) + 'v8" stroke="#c0392b" stroke-width=".3"/>';
    });
    var foot = back ? 'Streifen (grau) mit Alufolie bekleben, Streifen dürfen sich nicht berühren · schwarze Punkte = Krokodilklemme · Lochkreuze müssen über denen der Vorderseite liegen'
      : 'Gestrichelte Flächen mit Alufolie bekleben · rotes Kreuz = Loch stanzen, Druckknopf durchstecken' + (sh.hint ? ' · ' + sh.hint : '');
    s += '<text x="' + OX + '" y="' + (H - 4) + '" font-size="3" fill="#666">' + esc(foot) + '</text>';
    return s + '</svg>';
  }
  document.addEventListener('DOMContentLoaded', function () {
    var host = document.getElementById('sheets'); if (!host) return;
    var sel = document.getElementById('which');
    SHEETS.forEach(function (sh, i) {
      var o = document.createElement('option'); o.value = i; o.textContent = sh.name + ' — ' + sh.use; sel.appendChild(o);
      [false, true].forEach(function (back) {
        var d = document.createElement('div');
        d.className = 'sheet'; d.dataset.i = i; d.dataset.side = back ? 'back' : 'front';
        d.innerHTML = sheetSVG(sh, back);
        host.appendChild(d);
      });
    });
    function apply() {
      var v = sel.value, side = document.querySelector('input[name="side"]:checked').value;
      host.querySelectorAll('.sheet').forEach(function (d) {
        var on = (v === 'all' || d.dataset.i === v) && (side === 'both' || d.dataset.side === side);
        d.classList.toggle('off', !on);
      });
    }
    sel.addEventListener('change', apply);
    document.querySelectorAll('input[name="side"]').forEach(function (r) { r.addEventListener('change', apply); });
    var m = /[?&]v=(\w+)/.exec(location.search);
    if (m) { var idx = { pad: 0, einwurf: 1, ttt: 2, c4: 3 }[m[1]]; if (idx !== undefined) sel.value = String(idx); }
    apply();
    document.getElementById('print').addEventListener('click', function () { window.print(); });
  });
})();
