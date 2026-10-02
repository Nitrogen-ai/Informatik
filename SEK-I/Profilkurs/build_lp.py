# -*- coding: utf-8 -*-
"""Baut einzelne Lernpfad-Seiten aus build_course.py neu, ohne den Rest anzufassen.

Aufruf: python3 build_lp.py 5 [6 ...]

Nötig, weil die veröffentlichten Seiten inzwischen in Slug-Ordnern liegen
(lernpfade/1HJ/blockbasiert-arduino/...) und ihre Lösungen dienstags statt
freitags freischalten (siehe Commit 10b4e24). Ausgabepfad (aus dem Link in
index.html) und Freischaltdatum (aus der bisherigen Seite) werden übernommen,
Inhalte kommen aus UNITS in build_course.py.
"""
import os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(BASE, "build_course.py"), encoding="utf-8").read()
src = src.split("# ---------------------------------------------------------------- Lauf")[0]
ns = {"__file__": os.path.join(BASE, "build_course.py")}
exec(compile(src, "build_course.py", "exec"), ns)
index = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()

for arg in sys.argv[1:]:
    no = int(arg)
    rel = re.search(r'href="(lernpfade/[^"]*/lp%02d\.html)"' % no, index).group(1)
    path = os.path.join(BASE, rel)
    old = open(path, encoding="utf-8").read()
    unlock = re.search(r'id="loesung" data-unlock="([^"]+)"', old).group(1)
    ns["unlock_iso"] = lambda sjw, d=unlock: d
    ns["lp_out_dir"] = lambda n, d=os.path.dirname(path): d
    u = ns["UNIT_OF_LP"][no]
    lp = next(l for l in u["lps"] if l["no"] == no)
    ns["build_lp_page"](u, lp)
    print("OK", rel, "· Lösung ab", unlock)
