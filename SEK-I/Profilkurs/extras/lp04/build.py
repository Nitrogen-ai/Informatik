# Baut lp04.html (Aufruf: python3 extras/lp04/build.py): geteiltes Theme (aus bisheriger lp04.html) + Vorwissen/Quiz aus build_course.py + LP04-Inhalte
import os, random, re
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(PK, "lernpfade/1HJ/blockbasiert-scratch/lp04.html")

src = open(os.path.join(PK, "build_course.py"), encoding="utf-8").read()
src = src.split("# ---------------------------------------------------------------- Lauf")[0]
ns = {"__file__": os.path.join(PK, "build_course.py")}
exec(compile(src, "build_course.py", "exec"), ns)
lp4 = next(lp for u in ns["UNITS"] for lp in u["lps"] if lp["no"] == 4)

# Antwortreihenfolge mischen (wie LP03), reproduzierbar
rng = random.Random(404)
def shuffle(q):
    opts = list(q["opts"])
    first = next(i for i, o in enumerate(opts) if o[1])
    while True:
        rng.shuffle(opts)
        if next(i for i, o in enumerate(opts) if o[1]) != first or len(opts) < 2:
            break
    q["opts"] = opts
for entry in lp4["vorwissen"]:
    for q in entry["quiz"]:
        shuffle(q)
for q in lp4["quiz"]:
    shuffle(q)

vorwissen = ns["render_vorwissen"](lp4)
assert vorwissen, "Vorwissen-SVGs nicht gefunden"
quiz = ns["render_quiz"](lp4)
sol_items = "".join("<li>%s</li>" % s for s in lp4["solution"])
solution = ('<section class="sol" id="loesung" data-unlock="%s"><h2>Musterlösung <span class="sol-status">…</span></h2>'
            '<p class="sol-countdown"></p><div class="sol-body" hidden><ul class="sol-list">%s</ul></div>'
            '<p class="sol-hint">Die Lösung wird automatisch zum angegebenen Datum sichtbar — die Seite prüft das bei jedem Laden.</p></section>'
            ) % (ns["unlock_iso"](lp4["sjw"]), sol_items)

old = open(OUT, encoding="utf-8").read()
head = old.split("</style>")[0].split("\n/* ===== LP04 ·")[0].rstrip("\n") + "\n"
theme_js = re.search(r"<script>\n(.*?)\n</script>", old, re.S).group(1)
hero_start = old.index("<body")
hero_end = old.index('  <section class="lp-sec"><h2>Das lernst du')
hero = old[hero_start:hero_end]

css = open(os.path.join(HERE, "extra.css"), encoding="utf-8").read()
body = open(os.path.join(HERE, "body.html"), encoding="utf-8").read()
body = body.replace("{{VORWISSEN}}", vorwissen).replace("{{QUIZ}}", quiz).replace("{{SOLUTION}}", solution)
games = open(os.path.join(HERE, "games.js"), encoding="utf-8").read()
app = open(os.path.join(HERE, "app.js"), encoding="utf-8").read()

doc = (head + css + "</style>\n</head>\n" + hero + body +
       '  <a class="back" href="../../../index.html#hj1-content" style="margin-top:1.6rem">← zurück zur Kursübersicht</a>\n</div>\n'
       "<script>\n" + theme_js + "\n</script>\n<script>\n" + games + "\n" + app + "\n</script>\n</body>\n</html>\n")
open(OUT, "w", encoding="utf-8").write(doc)
print("OK", OUT, len(doc))
