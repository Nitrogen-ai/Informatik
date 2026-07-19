/* ============================================================
   PROFIL INFORMATIK · KLASSE 9 — geteiltes Skript
   Matrix-Regen · Halbjahr-Umschaltung · Freischaltung nach
   Datum (prüft stets, ob das Datum erreicht ist) · Sterne
   ============================================================ */
(function () {
  'use strict';

  /* ---------- Matrix-Regen (Schaltkreis/Space) ---------- */
  function startMatrix() {
    var c = document.getElementById('matrix-canvas');
    if (!c) return;
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var ctx = c.getContext('2d');
    var glyphs = '01ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜｵｶｷ<>[]{}/\\=+*01アカサ01'.split('');
    var fontSize = 15, cols = 0, drops = [];
    function resize() {
      c.width = window.innerWidth; c.height = window.innerHeight;
      cols = Math.floor(c.width / fontSize);
      drops = new Array(cols).fill(0).map(function () { return Math.random() * -80; });
    }
    resize();
    window.addEventListener('resize', resize);
    var last = 0;
    function draw(t) {
      requestAnimationFrame(draw);
      if (t - last < 55) return; // ~18 fps, ruhig
      last = t;
      ctx.fillStyle = 'rgba(5,7,14,0.28)';
      ctx.fillRect(0, 0, c.width, c.height);
      ctx.font = fontSize + "px 'JetBrains Mono', monospace";
      for (var i = 0; i < drops.length; i++) {
        var ch = glyphs[Math.floor(Math.random() * glyphs.length)];
        var x = i * fontSize, y = drops[i] * fontSize;
        ctx.fillStyle = Math.random() < 0.03 ? '#9dffd0' : '#1f9d6b';
        ctx.fillText(ch, x, y);
        if (y > c.height && Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
      }
    }
    requestAnimationFrame(draw);
  }

  /* ---------- Halbjahr-Umschaltung ---------- */
  function initSemesters() {
    var tiles = document.querySelectorAll('.sem-tile');
    var contents = document.querySelectorAll('.sem-content');
    if (!tiles.length) return;
    tiles.forEach(function (tile) {
      tile.addEventListener('click', function () {
        var sem = tile.dataset.sem;
        tiles.forEach(function (t) { t.classList.remove('active'); });
        tile.classList.add('active');
        contents.forEach(function (cc) { cc.classList.remove('active'); });
        var target = document.getElementById(sem + '-content');
        if (target) {
          target.classList.add('active');
          setTimeout(function () { target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 60);
        }
      });
    });
  }

  /* ---------- Datum-Helfer ---------- */
  function parseISO(s) { var p = (s || '').split('-'); return new Date(+p[0], (+p[1] || 1) - 1, +p[2] || 1, 0, 0, 0); }
  function fmt(d) {
    function z(n) { return (n < 10 ? '0' : '') + n; }
    return z(d.getDate()) + '.' + z(d.getMonth() + 1) + '.' + d.getFullYear();
  }

  /* ---------- Freischaltung der Lernpfadlösung (Übersicht) ----------
     Jede Kachel mit [data-unlock="YYYY-MM-DD"] bekommt einen Status.
     Es wird STETS beim Laden geprüft, ob das Datum erreicht wurde. */
  function initUnlockBadges() {
    var now = new Date();
    document.querySelectorAll('.lp[data-unlock]').forEach(function (el) {
      var unlock = parseISO(el.dataset.unlock);
      var host = el.querySelector('.lp-info') || el;
      var badge = document.createElement('span');
      badge.className = 'lp-lock';
      if (now >= unlock) {
        badge.classList.add('open');
        badge.textContent = '🔓 Lösung freigeschaltet';
      } else {
        badge.classList.add('locked');
        badge.textContent = '🔒 Lösung ab ' + fmt(unlock);
      }
      host.appendChild(badge);
    });
  }

  /* ---------- Freischaltung auf der Lernpfad-Seite ----------
     Element #loesung mit [data-unlock] wird nur gezeigt, wenn erreicht. */
  function initSolutionGate() {
    var box = document.getElementById('loesung');
    if (!box) return;
    var now = new Date();
    var unlock = parseISO(box.dataset.unlock);
    var body = box.querySelector('.sol-body');
    var status = box.querySelector('.sol-status');
    if (now >= unlock) {
      if (body) body.hidden = false;
      if (status) { status.textContent = '🔓 freigeschaltet seit ' + fmt(unlock); status.className = 'sol-status open'; }
    } else {
      if (body) body.hidden = true;
      if (status) { status.textContent = '🔒 Freischaltung am ' + fmt(unlock); status.className = 'sol-status locked'; }
      var ms = unlock - now, days = Math.ceil(ms / 86400000);
      var cd = box.querySelector('.sol-countdown');
      if (cd) cd.textContent = 'noch ' + days + ' Tag' + (days === 1 ? '' : 'e');
    }
  }

  /* ---------- Selbsteinschätzung (Sterne, localStorage) ---------- */
  function initSelfcheck() {
    var starSvg = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 18.9 6.1 21l1.2-6.5L2.5 9.9l6.6-.9z"/></svg>';
    var messages = { 1: 'Startpunkt gesetzt — dranbleiben.', 2: 'Wird sicherer.', 3: 'Sitzt gut!', 4: 'Voll gecheckt — stark!' };
    document.querySelectorAll('[data-selfcheck]').forEach(function (host) {
      var key = 'pi9_sc_' + host.getAttribute('data-selfcheck');
      var box = document.createElement('div');
      box.className = 'selfcheck';
      var s = '';
      for (var n = 1; n <= 4; n++) s += '<button class="sc-star" type="button" data-level="' + n + '" aria-label="Stufe ' + n + '">' + starSvg + '</button>';
      box.innerHTML = '<span class="sc-label">Wie sicher?</span><div class="sc-stars">' + s + '</div><span class="sc-feedback"></span>';
      host.appendChild(box);
      var stars = box.querySelectorAll('.sc-star'), fb = box.querySelector('.sc-feedback');
      function paint(lvl) {
        stars.forEach(function (st, i) { if (i < lvl) st.classList.add('on'); else st.classList.remove('on'); });
        if (lvl > 0) { fb.textContent = messages[lvl]; fb.classList.add('show'); }
        else { fb.textContent = ''; fb.classList.remove('show'); }
      }
      var saved = 0;
      try { saved = parseInt(localStorage.getItem(key), 10) || 0; } catch (e) {}
      paint(saved);
      stars.forEach(function (star, i) {
        star.addEventListener('click', function () {
          var lvl = i + 1;
          var isLast = stars[i].classList.contains('on') && (i === stars.length - 1 || !stars[i + 1].classList.contains('on'));
          if (isLast) { paint(0); try { localStorage.removeItem(key); } catch (e) {} }
          else { paint(lvl); try { localStorage.setItem(key, lvl); } catch (e) {} }
        });
      });
    });
  }

  /* ---------- Wissens-Check (Quiz) ---------- */
  function initQuiz() {
    var LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];
    document.querySelectorAll('[data-qz]').forEach(function (quiz) {
      var items = quiz.querySelectorAll('.qz-item');
      var total = items.length, solved = 0;
      var pcount = quiz.querySelector('.qz-count');
      var pfill = quiz.querySelector('.qz-fill');
      var doneBox = quiz.querySelector('.qz-solved');
      function updateProgress() {
        if (pcount) pcount.textContent = solved + ' / ' + total + ' richtig';
        if (pfill) pfill.style.width = (total ? (solved / total * 100) : 0) + '%';
        if (doneBox && solved === total) doneBox.classList.add('show');
      }
      items.forEach(function (q) {
        var opts = q.querySelectorAll('.qz-opt');
        var hint = q.querySelector('.qz-hint');
        var done = q.querySelector('.qz-done');
        var answered = false;
        opts.forEach(function (opt, i) {
          var lett = document.createElement('span');
          lett.className = 'lett';
          lett.textContent = LETTERS[i];
          opt.insertBefore(lett, opt.firstChild);
          opt.addEventListener('click', function () {
            if (answered) return;
            if (opt.getAttribute('data-correct') === 'true') {
              answered = true;
              opt.classList.add('correct');
              opts.forEach(function (o) { o.setAttribute('disabled', 'disabled'); });
              if (hint) hint.classList.remove('show');
              if (done) done.classList.add('show');
              solved++;
              updateProgress();
            } else {
              opt.classList.add('wrong');
              opt.setAttribute('disabled', 'disabled');
              if (hint) {
                hint.textContent = opt.getAttribute('data-hint') || 'Nicht ganz — versuch es nochmal.';
                hint.classList.add('show');
              }
            }
          });
        });
      });
      updateProgress();
    });
  }

  /* ---------- Live-Uhr im Hero (optional) ---------- */
  function initClock() {
    var el = document.getElementById('sysclock');
    if (!el) return;
    function tick() {
      var d = new Date();
      function z(n) { return (n < 10 ? '0' : '') + n; }
      el.textContent = z(d.getHours()) + ':' + z(d.getMinutes()) + ':' + z(d.getSeconds());
    }
    tick(); setInterval(tick, 1000);
  }

  document.addEventListener('DOMContentLoaded', function () {
    startMatrix();
    initSemesters();
    initUnlockBadges();
    initSolutionGate();
    initSelfcheck();
    initQuiz();
    initClock();
  });
})();
