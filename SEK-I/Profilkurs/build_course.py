# -*- coding: utf-8 -*-
"""
Generator: Profil Informatik · Klasse 9 (14–15 J.) — Kursplan HJ1 & HJ2
Erzeugt index.html (Kursübersicht) + Lernpfad-Startseiten + nutzt geteilte Assets.
Einzige Quelle der Wahrheit für Inhalte, Kalender und Freischalt-Daten.
"""
import os, glob, html, base64, json
from datetime import date, timedelta
from urllib.parse import quote

BASE = os.path.dirname(os.path.abspath(__file__))
LP_DIR = os.path.join(BASE, "lernpfade")
ASSET_DIR = os.path.join(BASE, "assets")
os.makedirs(LP_DIR, exist_ok=True)

# ---------------------------------------------------------------- Kalender
START = date(2026, 8, 24)
SKIP = {date(2026,10,19), date(2026,10,26), date(2026,12,21), date(2026,12,28),
        date(2027,2,1), date(2027,3,22), date(2027,3,29)}
CAL = {}          # sjw -> (montag, freitag)
mon, sjw = START, 0
while sjw < 37:
    if mon in SKIP:
        mon += timedelta(days=7); continue
    sjw += 1
    CAL[sjw] = (mon, mon + timedelta(days=4))
    mon += timedelta(days=7)
CAL = {k - 1: v for k, v in CAL.items()}   # SJW zählt ab 0

def de(d):  # dd.mm.yyyy
    return d.strftime("%d.%m.%Y")
def dm(d):  # dd.mm.
    return d.strftime("%d.%m.")
def iso(d):
    return d.strftime("%Y-%m-%d")

def esc(s):
    return html.escape(s, quote=True)

# ---------------------------------------------------------------- Werkzeuge (URLs)
T = {
  "scratch": ("Scratch", "https://scratch.mit.edu/"),
  "makey": ("Makey Makey", "https://makeymakey.com/pages/how-to"),
  "tinker": ("Tinkercad Circuits", "https://www.tinkercad.com/circuits"),
  "arduino": ("Arduino", "https://www.arduino.cc/en/software"),
  "cloud": ("Arduino Cloud Editor", "https://app.arduino.cc/sketches"),
  "tinker3d": ("Tinkercad 3D-Entwurf (Gehäuse)", "https://www.tinkercad.com/"),
  "upload": ("Arduino hochladen (ohne Konto)", "https://nitrogen-ai.github.io/Informatik/SEK-I/Profilkurs/werkzeuge/arduino-hochladen.html"),
  "wtj": ("WebTigerJython", "https://webtigerjython.ethz.ch/"),
  "jsfiddle": ("jsfiddle.net", "https://jsfiddle.net/"),
  "github": ("GitHub", "https://github.com/"),
  "ref": ("Referenz-Tool: Verb-Trainer", "https://nitrogen-ai.github.io/training/verb_conjugation_trainer_year6.html"),
  "bincalc": ("Windows-Rechner (Programmierer-Modus)", "https://support.microsoft.com/de-de/windows/rechner-app-9b8ff34a-e3ff-9c5f-b0b0-a52a5b23c7a4"),
}

# ---------------------------------------------------------------- Vorwissen-Figuren (SVG)
# lp-Nummer -> Ordner mit typst/figN.svg bzw. Tutory/Stundenvorschlag/typst/figN.svg (color-Variante)
LESSON_DIRS = {
  0: "00 Systemstart - Was ist Informatik",
  1: "01 EVA & Algorithmus - wie ein Computer denkt",
  2: "02 Scratch-Grundlagen - Bühne, Figuren, Ereignisse",
  3: "03 Schleifen & Verzweigungen - ein Mini-Spiel",
  4: "04 Makey Makey - die Welt wird zum Controller",
  5: "05 Tinkercad Circuits - Stromkreis simulieren",
  6: "06 Arduino - Einführung in Tinkercad",
  # 07–09 Sensor-Projekte: 07 aus Version 3 des Projektordners, 08 und 09 mit eigenem Lektionsordner
  7: "07 Arduino-Projekte - Tinkercad trifft echte Hardware/Version 3",
  8: "08 Sensor-Projekte bauen und testen",
  9: "09 Sensor-Projekte Galerie",
  # alte Lektionen 08–10 (Ampel, OOP, Mini-Projekt) liegen seit 2026-10-16 im Archiv der Einheit
  10: "Archiv/10 Mini-Projekt Arduino - Ergebnissicherung",
}

# Die Lektionsordner (mit typst/figN.svg) liegen in der iCloud-Materialablage unter
# 1HJ/<Einheit>/<Lektion>/, nicht neben diesem Skript. Überschreibbar per PROFIL_MATERIAL.
MATERIAL_ROOT = os.environ.get("PROFIL_MATERIAL") or os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/Unterricht/Material SEK I/"
    "Informatik/Profilkurs/1HJ")

def find_material(lp_no, filename):
    folder = LESSON_DIRS.get(lp_no)
    if not folder:
        return None
    candidates = []
    # Nach dem Tutory-Einsatz liegt typst/ im Archiv der Lektion: Tutory/Stundenvorschlag/typst/
    for sub in ("typst", os.path.join("Tutory", "Stundenvorschlag", "typst"), "plickers",
                os.path.join("Tutory", "Typst", "grafiken")):
        rel = os.path.join(folder, sub, filename)
        candidates += [os.path.join(BASE, rel)] + sorted(glob.glob(os.path.join(MATERIAL_ROOT, "*", rel)))
    for path in candidates:
        if os.path.exists(path):
            return path
    return None

def load_svg(lp_no, fig):
    path = find_material(lp_no, fig + ".svg")
    if not path:
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_fig(lp_no, fig, alt=""):
    """SVG (Name ohne Endung) inline oder Foto (.jpg/.png) als data-URI."""
    if fig.lower().endswith((".jpg", ".jpeg", ".png")):
        path = find_material(lp_no, fig)
        if not path:
            return ""
        mime = "image/png" if fig.lower().endswith(".png") else "image/jpeg"
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
        return '<img src="data:%s;base64,%s" alt="%s" loading="lazy">' % (mime, data, esc(alt))
    return load_svg(lp_no, fig)

def render_figs(lp, entries):
    out = ""
    for e in entries or []:
        media = load_fig(lp["no"], e["fig"], e["cap"])
        if media:
            out += '<div class="fig">%s<div class="fig-cap">%s</div></div>' % (media, esc(e["cap"]))
    return out

# ---------------------------------------------------------------- LP05 · Vertiefung (Bauteile + Vorwiderstand-Rechner)
LP05_VERTIEFUNG = (
  '<p>Wähle eine oder beide Vertiefungen. Tinkercad Circuits folgt erst in der nächsten Stunde.</p>'
  '<h3>a) Weitere Bauteile anschließen und die Polung herausfinden</h3>'
  '<p>Schließe den Motor und den Buzzer nacheinander anstelle der LED an, den Tastschalter zusätzlich im LED-Stromkreis. Stecke jedes Bauteil einmal richtig herum und einmal umgedreht ein. '
  '<b>Notiere</b> jeweils: Funktioniert es in beiden Richtungen? Was ändert sich? Braucht das Bauteil einen Vorwiderstand?</p>'
  '<ul class="task-list">'
  '<li><b>Motor mit Propeller</b> (kleiner Gleichstrommotor) direkt an 5V und GND, <b>ohne</b> 220-Ω-Widerstand.</li>'
  '<li><b>Buzzer</b> (Summer): Achte auf ein „+“ oder das längere Beinchen. Probiere ihn ohne und mit 220-Ω-Widerstand.</li>'
  '<li><b>Tastschalter</b>: Stecke ihn quer über den Mittelgraben und baue ihn in den LED-Stromkreis ein, '
  'sodass die LED nur leuchtet, solange du den Taster gedrückt hältst.</li>'
  '</ul>'
  '<h3>b) Den Vorwiderstand berechnen</h3>'
  '<p>Am Widerstand liegt die Spannung an, die die LED „übrig lässt“: <code>U<sub>R</sub> = U − U<sub>LED</sub></code>. '
  'Mit der gewünschten Stromstärke gilt das ohmsche Gesetz <code>R = U<sub>R</sub> / I</code>. '
  'Eine rote LED braucht etwa 2 V und verträgt höchstens 20 mA. <b>Rechne</b> zuerst selbst und <b>überprüfe</b> dann mit dem Rechner. '
  'Plane anschließend drei parallel geschaltete LEDs und vergleiche sie mit einer Reihenschaltung. <b>Überprüfe</b> beides experimentell.</p>'
  '<div class="rechner" data-rechner>'
  '<div class="re-in">'
  '<label>Spannung U <select data-k="u"><option value="5" selected>5 V (Pin 5V)</option><option value="3.3">3,3 V (Pin 3.3V)</option></select></label>'
  '<label>LED-Farbe <select data-k="uf"><option value="2.0" selected>rot (≈ 2,0 V)</option><option value="2.1">gelb (≈ 2,1 V)</option>'
  '<option value="2.2">grün (≈ 2,2 V)</option><option value="3.1">blau / weiß (≈ 3,1 V)</option></select></label>'
  '<label>Stromstärke I <span><input type="range" min="5" max="20" step="1" value="20" data-k="i"> <b data-o="i">20 mA</b></span></label>'
  '<label>Schaltung <select data-k="art"><option value="reihe" selected>LEDs in Reihe (ein Widerstand)</option>'
  '<option value="parallel">LEDs parallel (jede mit eigenem Widerstand)</option></select></label>'
  '<label>Anzahl LEDs <span><input type="range" min="1" max="4" step="1" value="1" data-k="n"> <b data-o="n">1</b></span></label>'
  '</div>'
  '<div class="re-out" data-out></div>'
  '</div>'
  '<style>'
  '.vertiefung h3{font-size:1rem;margin:1.1rem 0 .4rem;color:var(--key)}'
  '.rechner{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));background:var(--panel-2);'
  'border:1px solid var(--line);border-radius:14px;padding:1rem;margin-top:.8rem}'
  '.re-in{display:grid;gap:.7rem}.re-in label{display:grid;gap:.25rem;font-size:.9rem;color:var(--ink-soft)}'
  '.re-in label>span{display:flex;align-items:center;gap:.6rem}.re-in input[type=range]{flex:1;accent-color:var(--key)}'
  '.re-in select{font:inherit;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:.35rem .5rem}'
  '.re-out{font-size:.92rem;line-height:1.55}.re-out .re-big{font-size:1.25rem;font-weight:700;color:var(--key)}'
  '.re-out .re-warn{color:var(--amber);font-weight:700}.re-out code{white-space:nowrap}'
  '</style>'
  '<script>(function(){'
  'var E12=[1,1.2,1.5,1.8,2.2,2.7,3.3,3.9,4.7,5.6,6.8,8.2];'
  'function norm(r){var d=Math.pow(10,Math.floor(Math.log10(r)));for(var k=0;k<3;k++){for(var j=0;j<E12.length;j++){var v=E12[j]*d;if(v>=r-1e-9)return Math.round(v);}d*=10;}return Math.round(r);}'
  'function f(x,n){return x.toFixed(n).replace(".",",");}'
  'document.querySelectorAll("[data-rechner]").forEach(function(box){'
  'function val(k){return box.querySelector("[data-k="+k+"]").value;}'
  'function upd(){var U=+val("u"),UF=+val("uf"),I=+val("i")/1000,n=+val("n"),art=val("art");'
  'box.querySelector("[data-o=i]").textContent=val("i")+" mA";box.querySelector("[data-o=n]").textContent=n;'
  'var reihe=art==="reihe",ul=reihe?n*UF:UF,ur=U-ul,h="";'
  'h+="<div><code>U<sub>LED</sub> = "+(reihe&&n>1?n+" · "+f(UF,1)+" V = ":"")+f(ul,1)+" V</code></div>";'
  'if(ur<=0.05){h+="<p class=re-warn>Die "+f(U,1)+" V reichen nicht: "+(reihe?n+" LEDs in Reihe":"die LED")+" brauchen schon "+f(ul,1)+" V. Die LEDs bleiben dunkel.</p>";}'
  'else{var R=ur/I,N=norm(R),I220=ur/220*1000;'
  'h+="<div><code>U<sub>R</sub> = "+f(U,1)+" V − "+f(ul,1)+" V = "+f(ur,1)+" V</code></div>";'
  'h+="<div><code>R = "+f(ur,1)+" V / "+f(I*1000,0)+" mA = "+f(R,0)+" Ω</code></div>";'
  'h+="<p class=re-big>mindestens "+f(R,0)+" Ω → nächster Normwert: "+N+" Ω</p>";'
  'h+="<p>Mit dem <b>220-Ω-Widerstand</b> aus dem Set fließen <code>"+f(ur,1)+" V / 220 Ω = "+f(I220,1)+" mA</code>"+(I220>20?" – <span class=re-warn>zu viel!</span>":(I220<5?" – die LED"+(reihe&&n>1?"s leuchten":" leuchtet")+" nur schwach.":" – sicher, die LED"+(n>1?"s leuchten":" leuchtet")+" gut."))+"</p>";'
  'if(!reihe&&n>1)h+="<p>Parallel bekommt jede LED ihren eigenen Widerstand und dieselbe Spannung, die Ströme addieren sich: <code>"+n+" · "+f(I220,1)+" mA = "+f(n*I220,1)+" mA</code> aus dem Pin 5V.</p>";'
  'if(reihe&&n>1)h+="<p>In Reihe fließt durch alle LEDs derselbe Strom, die Spannung teilt sich auf.</p>";}'
  'box.querySelector("[data-out]").innerHTML=h;}'
  'box.querySelectorAll("[data-k]").forEach(function(el){el.addEventListener("input",upd);});upd();});'
  '})();</script>'
)

UPLOAD_URL = T["upload"][1]

# ---------------------------------------------------------------- LP07 · Projektkarten (Quelle: extras/lp07/projekte.py → projekte.json)
LP07_MATERIAL = (
  "<p><b>Vom Tinkercad zum echten Arduino.</b> Tinkercad simuliert nur. Damit dein Schloss wirklich leuchtet und piept, lädst du den C++-Code auf einen echten Arduino Uno. "
  "Das geht mit unserer Seite <a href=\"" + UPLOAD_URL + "\" target=\"_blank\" rel=\"noopener\"><b>Arduino hochladen</b></a>: ohne Konto, ohne Installation, im Browser <b>Chrome</b> oder <b>Edge</b>.</p>"
  "<ol class=\"task-list\" style=\"list-style:decimal;padding-left:1.4rem\">"
  "<li>Schaltung auf dem Steckbrett nachbauen, <b>ohne</b> dass der Arduino am USB-Kabel hängt. Pins 0 und 1 bleiben frei.</li>"
  "<li>In Tinkercad: <b>Code</b> › oben <b>„Blöcke“</b> auf <b>„Text“</b> umstellen › in den Code klicken › <b>Strg + A</b>, <b>Strg + C</b>.</li>"
  "<li><a href=\"" + UPLOAD_URL + "\" target=\"_blank\" rel=\"noopener\"><b>Arduino hochladen</b></a> öffnen und den Code ins Feld einfügen (<b>Strg + V</b>).</li>"
  "<li>Arduino per USB anstecken › <b>„⬆ Auf Arduino laden“</b> › im Fenster oben den Arduino wählen (z. B. „Arduino Uno (COM3)“ oder „USB-SERIAL CH340“) › <b>Verbinden</b>.</li>"
  "<li>Nach „✅ Fertig!“ läuft dein Programm. Was der Arduino mit <code>Serial.println</code> schreibt, steht unten im <b>Monitor</b>.</li>"
  "</ol>"
  "<p><b>Klappt etwas nicht?</b> Hat der Code Fehler, markiert die Seite die Zeile rot und erklärt den Fehler auf Deutsch. Mit <b>„💡 Arduino testen“</b> prüfst du, ob der Arduino überhaupt erreichbar ist (die kleine LED „L“ blinkt). "
  "Mit <b>„💾 Als .ino speichern“</b> sicherst du deinen Code für die Abgabe.</p>"
  "<p><b>Sicherheit:</b> nur ohne Strom umstecken, jede LED mit Vorwiderstand, jeder Taster mit 10-kΩ-Widerstand nach GND.</p>")

def _code(datei):
    with open(os.path.join(BASE, "extras", "lp07", "code", datei), encoding="utf-8") as f:
        return f.read()

# LP07 Version 2 (Tastendruck und Farbschloss); Version 1 (9 Projektkarten) liegt in extras/lp07/version1
LP07_VERTIEFUNG = (
  "<p>Ein Escape Room lebt von Schlössern, die man nur mit dem richtigen Hinweis öffnen kann. Dein Farbschloss ist die Grundlage, "
  "du änderst nur, <b>was</b> auf den Tastern steht und <b>woher</b> der Hinweis kommt.</p>"
  "<h3>🔣 Symbolschloss</h3><p>Klebe Symbole (Stern, Mond, Herz, Blitz) auf die Taster. Der Hinweis ist ein Bild- oder Bilderrätsel, z. B. „Nacht folgt auf Tag …“.</p>"
  "<h3>👃 Duftschloss</h3><p>Stelle vor jeden Taster ein Döschen mit Duft (Zitrone, Zimt, Kaffee, Minze). Der Hinweis beschreibt eine Reihenfolge, z. B. ein Rezept.</p>"
  "<h3>🎵 Tonschloss</h3><p>Jeder Taster spielt mit <code>tone()</code> einen anderen Ton. Der Code ist eine kurze Melodie, die man nachspielen muss.</p>"
  "<p><b>Plane</b> dein Schloss nach dem EVA-Prinzip: Was wird gedrückt (Eingabe), wie wird der Code gebildet und geprüft (Verarbeitung), was passiert beim Öffnen (Ausgabe)? "
  "<b>Teste</b> es mit einer anderen Gruppe als „Spieler:innen“.</p>"
  "<style>.vertiefung h3{font-size:1rem;margin:1.1rem 0 .4rem;color:var(--key)}</style>")

LP07_LOESUNG = [
  "Aufgabe 2: Die Variable <code>Tastendruck</code> zählt die Tastendrücke (0, 1, 2, …). Jeder Druck lässt die LED an Pin 7 blinken und erhöht um 1. Bei <code>Tastendruck = 5</code> endet „bis … wiederholen“.",
  "Aufgabe 4: grün, weiß, blau, gelb → 2 → 24 → 241 → <b>2413</b>.",
  "Aufgabe 5: Bedingungen <code>Anschluss 12/11/10/9 = HOCH</code>, dann <code>Tastendruck = 4</code>, darin <code>Code = Geheimcode</code> (z. B. 1334).",
  '<details><summary><b>C++ Schritt 1</b> · 07-1-tastendruck.ino</summary><pre style="overflow:auto;font-size:.8rem"><code>%s</code></pre></details>' % esc(_code("07-1-tastendruck.ino")),
  '<details><summary><b>C++ Schritt 2</b> · 07-2-farbschloss.ino</summary><pre style="overflow:auto;font-size:.8rem"><code>%s</code></pre></details>' % esc(_code("07-2-farbschloss.ino")),
]

# ---------------------------------------------------------------- Stufen: Impulsfragen → Erwartungshorizont (LP07 Version 3)
# lp["stufen"] = dict(intro, projekte=[(kürzel, name, ort)], aufgaben=[dict(nr, titel, auftrag, fragen, eh)])
# fragen: Quiz-Dicts wie bei quiz, optional proj="AB" (nur für diese Projekte); eh: {kürzel: HTML}.
# Jede Aufgabe hat je Projekt einen eigenen Fragenblock. Sind alle Fragen richtig, erscheint der Erwartungshorizont.
STUFEN_CSS = (
  '<style>'
  '.stufen .st-wahl{display:flex;flex-wrap:wrap;gap:.5rem;margin:.8rem 0 1rem}'
  '.stufen .st-wahl button{font:inherit;font-weight:700;color:var(--ink);background:var(--panel-2);border:1px solid var(--line);'
  'border-radius:10px;padding:.55rem .9rem;cursor:pointer;text-align:left}'
  '.stufen .st-wahl button small{display:block;font-weight:500;color:var(--ink-soft);font-size:.78rem}'
  '.stufen .st-wahl button.on{border-color:var(--key);box-shadow:0 0 0 2px var(--key) inset}'
  '.stufen .st-aufgabe{border-top:1px solid var(--line);padding-top:1rem;margin-top:1.2rem}'
  '.stufen h3{font-size:1.05rem;margin:0 0 .4rem;color:var(--key)}'
  '.stufen .st-proj,.stufen .st-aufgabe{display:none}'
  '.stufen[data-wahl] .st-aufgabe{display:block}.stufen[data-wahl] .st-leer{display:none}'
  '.stufen[data-wahl="A"] .st-proj[data-p="A"],.stufen[data-wahl="B"] .st-proj[data-p="B"],.stufen[data-wahl="C"] .st-proj[data-p="C"]{display:block}'
  '.stufen .st-leer{color:var(--amber);font-weight:600}'
  '.stufen .st-lock{margin-top:.8rem;padding:.6rem .8rem;border:1px dashed var(--line);border-radius:10px;color:var(--ink-soft);font-size:.9rem}'
  '.stufen .st-eh{display:none;margin-top:1rem;padding:1rem;border:1px solid var(--matrix);border-radius:14px;background:rgba(52,255,158,.05)}'
  '.stufen .st-proj.offen .st-eh{display:block}.stufen .st-proj.offen .st-lock{display:none}'
  '.stufen .st-eh h4{margin:0 0 .6rem;color:var(--matrix);font-size:1rem}'
  '.stufen .st-eh h5{margin:1rem 0 .4rem;font-size:.92rem;color:var(--key)}'
  '.stufen table{width:100%;border-collapse:collapse;font-size:.86rem;margin:.4rem 0 .8rem}'
  '.stufen th,.stufen td{border:1px solid var(--line);padding:.35rem .45rem;text-align:left;vertical-align:top}'
  '.stufen th{background:var(--panel-2)}.stufen .gr{color:var(--ink-soft)}'
  '.stufen .tbl{overflow-x:auto}'
  '.stufen .st-tipp{border-left:4px solid var(--amber);padding:.5rem .7rem;background:rgba(255,194,61,.07);border-radius:8px;font-size:.88rem;margin:.6rem 0}'
  '.stufen pre{overflow:auto;font-size:.8rem}'
  '.led{display:inline-block;width:.8em;height:.8em;border-radius:50%;vertical-align:-.05em;margin-right:.2em}'
  '.led.g{background:#3fbf5a}.led.r{background:#e0414f}'
  # Struktogramm (Nassi-Shneiderman)
  '.ns{border:1.5px solid var(--ink-soft);max-width:540px;font-size:.86rem;background:var(--panel);margin:.4rem 0 .6rem}'
  '.ns-t{padding:.35rem .5rem;font-weight:700}'
  '.ns-a{padding:.35rem .5rem;border-top:1.5px solid var(--ink-soft)}'
  '.ns-l{border-top:1.5px solid var(--ink-soft)}.ns-l>.ns-k{padding:.35rem .5rem}'
  '.ns-lb{margin-left:1.4rem;border-left:1.5px solid var(--ink-soft)}'
  '.ns-w{border-top:1.5px solid var(--ink-soft)}'
  '.ns-wk{position:relative;height:3.4rem}.ns-wk svg{position:absolute;inset:0;width:100%;height:100%}'
  '.ns-wk line{stroke:var(--ink-soft);stroke-width:1.5;vector-effect:non-scaling-stroke}'
  '.ns-wk .ns-b{position:absolute;left:20%;right:20%;top:.25rem;text-align:center}'
  '.ns-wk .ns-ja,.ns-wk .ns-nein{position:absolute;bottom:.15rem;font-size:.74rem;color:var(--ink-soft)}'
  '.ns-wk .ns-ja{left:.4rem}.ns-wk .ns-nein{right:.4rem}'
  '.ns-wz{display:grid;grid-template-columns:1fr 1fr}.ns-wz>div:first-child{border-right:1.5px solid var(--ink-soft)}'
  '</style>')

STUFEN_JS = (
  '<script>(function(){'
  'document.querySelectorAll("[data-stufen]").forEach(function(sec){'
  'var key="stufen-"+location.pathname;'
  'function setze(p){sec.setAttribute("data-wahl",p);'
  'sec.querySelectorAll(".st-wahl button").forEach(function(b){b.classList.toggle("on",b.dataset.p===p);});'
  'try{localStorage.setItem(key,p);}catch(e){}}'
  'sec.querySelectorAll(".st-wahl button").forEach(function(b){b.addEventListener("click",function(){setze(b.dataset.p);});});'
  'try{var alt=localStorage.getItem(key);if(alt)setze(alt);}catch(e){}'
  'sec.querySelectorAll(".st-proj").forEach(function(box){'
  'box.addEventListener("click",function(){setTimeout(function(){'
  'var items=box.querySelectorAll(".qz-item"),ok=box.querySelectorAll(".qz-opt.correct").length;'
  'if(items.length&&ok===items.length&&!box.classList.contains("offen")){box.classList.add("offen");'
  'var eh=box.querySelector(".st-eh");if(eh)eh.scrollIntoView({behavior:"smooth",block:"nearest"});}'
  '},0);});});});'
  '})();</script>')

def ns_anw(x):
    return '<div class="ns-a">%s</div>' % x

def ns_immer(kopf, *body):
    return '<div class="ns-l"><div class="ns-k">%s</div><div class="ns-lb">%s</div></div>' % (kopf, "".join(body))

def ns_wenn(bed, ja, nein):
    return ('<div class="ns-w"><div class="ns-wk"><svg viewBox="0 0 100 10" preserveAspectRatio="none">'
            '<line x1="0" y1="0" x2="50" y2="10"/><line x1="100" y1="0" x2="50" y2="10"/></svg>'
            '<span class="ns-b">%s</span><span class="ns-ja">ja</span><span class="ns-nein">nein</span></div>'
            '<div class="ns-wz"><div>%s</div><div>%s</div></div></div>') % (bed, "".join(ja), "".join(nein))

def struktogramm(name, *body):
    return '<div class="ns"><div class="ns-t">Programm: %s</div>%s</div>' % (name, "".join(body))

def render_stufen(lp):
    st = lp["stufen"]
    wahl = "".join('<button type="button" data-p="%s">%s · %s<small>%s</small></button>' % (k, k, esc(n), esc(o))
                   for k, n, o in st["projekte"])
    aufgaben = ""
    for a in st["aufgaben"]:
        bloecke = ""
        for k, n, _ in st["projekte"]:
            fragen = [q for q in a["fragen"] if k in q.get("proj", "ABC")]
            items = ""
            for i, q in enumerate(fragen, 1):
                opts = ""
                for text, correct, hint in q["opts"]:
                    attr = ' data-correct="true"' if correct else (' data-hint="%s"' % esc(hint) if hint else "")
                    opts += '<button class="qz-opt"%s>%s</button>' % (attr, text)
                items += ('<div class="qz-item"><div class="qz-text"><span class="qn">%d.</span>%s</div>'
                          '<div class="qz-opts">%s</div><div class="qz-hint"></div><div class="qz-done">%s</div></div>'
                          ) % (i, q["q"], opts, q.get("done", "Richtig!"))
            bloecke += (
                '<div class="st-proj" data-p="%s">'
                '<div class="qz-wrap" data-qz><div class="qz-progress"><span class="qz-count">0 / %d richtig</span>'
                '<span class="qz-bar"><span class="qz-fill"></span></span></div>%s'
                '<div class="qz-solved">✔ Alle Impulse geschafft. Vergleicht jetzt mit dem Erwartungshorizont.</div></div>'
                '<div class="st-lock">🔒 Beantwortet alle Fragen richtig, dann erscheint hier der Erwartungshorizont zu Aufgabe %d für Projekt %s.</div>'
                '<div class="st-eh"><h4>🔓 Erwartungshorizont · Aufgabe %d · Projekt %s %s</h4>%s</div>'
                '</div>') % (k, len(fragen), items, a["nr"], k, a["nr"], k, esc(n), a["eh"][k])
        aufgaben += ('<div class="st-aufgabe"><h3>Aufgabe %d · %s</h3><p>%s</p>%s</div>'
                     % (a["nr"], esc(a["titel"]), a["auftrag"], bloecke))
    return ('<section class="lp-sec stufen" data-stufen><h2>Schritt für Schritt: prüfen und vergleichen</h2>%s'
            '<div class="st-wahl">%s</div><p class="st-leer">Wählt zuerst euer Projekt, dann erscheinen die Impulsfragen.</p>%s%s%s</section>'
            ) % (st["intro"], wahl, aufgaben, STUFEN_CSS, STUFEN_JS)

# ---------------------------------------------------------------- LP07–09 Version 3 · Sensor-Projekte (Wächter mit grüner und roter LED)
# Quelle: iCloud <07 Arduino-Projekte …>/Version 3/Tutory/Typst/: „07 Sensor-Projekte planen.typ“ (+ Erwartungshorizont),
# „07 Sensoren anschließen.typ“; <08 Sensor-Projekte bauen und testen>/ und <09 Sensor-Projekte Galerie>/ je mit Tutory/Typst/.
# Baupläne (Steckplan, Gehäuse): build_bauplan.py → grafiken/bauplan-*.svg, Code: extras/lp07/code/*.ino
SP_PROJEKTE = [("A", "Gießwächter", "Zimmerpflanze im Wohnzimmer"),
               ("B", "Filterwächter", "Wasserfilter in der Küche"),
               ("C", "Lüftungswächter", "Heizkeller im Haus")]

def _tab(kopf, zeilen):
    th = "".join("<th>%s</th>" % k for k in kopf)
    tr = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % z for z in zeile) for zeile in zeilen)
    return '<div class="tbl"><table><tr>%s</tr>%s</table></div>' % (th, tr)

def _fig(no, fig, cap):
    media = load_fig(no, fig, cap)
    return '<div class="fig">%s<div class="fig-cap">%s</div></div>' % (media, esc(cap)) if media else ""

def _codeblock(datei, titel):
    return ('<details><summary><b>%s</b> · %s</summary><pre><code>%s</code></pre></details>'
            % (titel, datei, esc(_code(datei))))

GRUEN_AN = ns_anw('<span class="led g"></span>Pin 7 auf HOCH<br><span class="led r"></span>Pin 8 auf NIEDRIG')
ROT_AN = ns_anw('<span class="led g"></span>Pin 7 auf NIEDRIG<br><span class="led r"></span>Pin 8 auf HOCH')

SP_ABLAUF = (
  '<div class="sp-ablauf">'
  '<div%s><b>Sitzung 07 · Planen &amp; programmieren</b><br>Tinkercad: Schaltung, Code, Gehäuse</div>'
  '<div%s><b>Sitzung 08 · Bauen &amp; testen</b><br>Gehäuse, echter Arduino, Projektbericht</div>'
  '<div%s><b>Sitzung 09 · Galerie</b><br>Gallery Walk, Bewertung, Rückmeldung</div></div>')
SP_CSS = (
  '<style>'
  '.sp-ablauf{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.5rem;margin:.4rem 0 1rem}'
  '.sp-ablauf div{border:1px solid var(--line);border-radius:10px;padding:.55rem .7rem;font-size:.88rem;color:var(--ink-soft)}'
  '.sp-ablauf div.an{border-color:var(--key);background:rgba(53,224,255,.08);color:var(--ink)}'
  '.sp-karten{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.7rem;margin:.6rem 0 1rem}'
  '.sp-karte{border:1px solid var(--line);border-radius:12px;padding:.8rem;background:var(--panel-2);font-size:.9rem}'
  '.sp-karte h3{margin:0 0 .15rem;font-size:1rem;color:var(--key)}.sp-karte .ort{color:var(--ink-soft);font-size:.8rem;margin-bottom:.4rem}'
  '.sp-karte p{margin:.3rem 0}.sp-karte .tk{color:var(--ink-soft);font-size:.82rem}'
  '.mat table{width:100%;border-collapse:collapse;font-size:.88rem;margin:.4rem 0 .9rem}'
  '.mat th,.mat td{border:1px solid var(--line);padding:.35rem .45rem;text-align:left;vertical-align:top}.mat th{background:var(--panel-2)}'
  '.mat .tbl{overflow-x:auto}.mat h3{font-size:1rem;margin:1.1rem 0 .4rem;color:var(--key)}'
  '.mat pre{overflow:auto;font-size:.8rem}'
  '.led{display:inline-block;width:.8em;height:.8em;border-radius:50%;vertical-align:-.05em;margin-right:.2em}'
  '.led.g{background:#3fbf5a}.led.r{background:#e0414f}'
  '.sp-hinweis{border-left:4px solid var(--amber);padding:.5rem .7rem;background:rgba(255,194,61,.07);border-radius:8px;font-size:.9rem;margin:.6rem 0}'
  '</style>')

def sp_ablauf(aktiv):
    return SP_ABLAUF % tuple(' class="an"' if n == aktiv else "" for n in ("07", "08", "09"))

def sp_karte(k, name, ort, kontext, sensor, gruen, rot, ersatz):
    return ('<div class="sp-karte"><h3>%s · %s</h3><div class="ort">%s</div><p>%s</p><p><b>Sensor:</b> %s</p>'
            '<p><span class="led g"></span>%s<br><span class="led r"></span>%s</p><p class="tk"><b>Tinkercad:</b> %s</p></div>'
            % (k, name, ort, kontext, sensor, gruen, rot, ersatz))

LP07_V3_MATERIAL = (
  sp_ablauf("07")
  + '<p>In <b>Zweierteams</b> baut ihr in drei Sitzungen einen <b>Wächter</b>: Ein echter Sensor misst, der Arduino vergleicht mit einem '
    '<b>Schwellenwert</b>, und zwei LEDs zeigen an: <span class="led g"></span><b>grün</b> = alles in Ordnung, <span class="led r"></span><b>rot</b> = jetzt handeln. '
    'Heute <b>plant</b> ihr, <b>programmiert</b> in Tinkercad, <b>übersetzt</b> die Blöcke in C++ und <b>modelliert</b> ein Gehäuse für den 3D-Drucker. Entscheidet euch für ein Projekt:</p>'
  + '<div class="sp-karten">'
  + sp_karte("A", "Gießwächter", "Zimmerpflanze im Wohnzimmer",
             "Die Pflanzen stehen in Übertöpfen mit Wasservorrat. Von außen sieht niemand, wie viel Wasser noch drin ist.",
             "Wasserstandssensor an A0, steht im Wasservorrat.", "genug Wasser im Topf",
             "Wasserstand unter dem Schwellenwert: gießen!", "Potentiometer an A0 als Ersatz für den Wasserstandssensor.")
  + sp_karte("B", "Filterwächter", "Wasserfilter in der Küche",
             "Der Tischwasserfilter holt gelöste Salze aus dem Leitungswasser. Ist die Kartusche verbraucht, schmeckt man es nicht sofort.",
             "TDS-Sensor an A1, misst gelöste Stoffe in ppm im gefilterten Wasser.", "Filter arbeitet",
             "TDS über dem Schwellenwert: Kartusche wechseln!", "Potentiometer an A1 als Ersatz für den TDS-Sensor.")
  + sp_karte("C", "Lüftungswächter", "Heizkeller im Haus",
             "Im Heizkeller ist es warm, oft trocknet dort Wäsche. Wird zu selten gelüftet, bildet sich Schimmel an den Wänden.",
             "DHT11 an Pin 2, misst Temperatur und Luftfeuchte.", "Luft in Ordnung",
             "Temperatur <b>und</b> Luftfeuchte zu hoch: lüften!",
             "TMP36 an A2 (Temperatur) und Potentiometer an A3 (Luftfeuchte), einen DHT11 gibt es dort nicht.")
  + '</div>'
  + '<h3>Für alle Projekte gleich: die Anzeige</h3>'
    '<p>LED grün an <b>Pin 7</b>, LED rot an <b>Pin 8</b>, jede über <b>220 Ω</b> (rot-rot-braun) an GND. Es leuchtet immer genau eine LED. '
    'Den Schwellenwert wählt ihr heute vorläufig, in Sitzung 08 messt ihr ihn am echten Sensor nach.</p>'
  + '<h3>Gehäuse aus dem 3D-Drucker: so geht\'s</h3><ol class="task-list" style="list-style:decimal;padding-left:1.4rem">'
    '<li>Tinkercad › <b>3D-Entwurf</b> anlegen, Quader auf <b>Außenmaß</b> ziehen. Einen zweiten Quader im <b>Innenmaß</b> als <b>Bohrung</b> einsetzen, 2 mm über dem Boden: Wand und Boden bleiben 2 mm stark.</li>'
    '<li><b>Aussparungen</b> als Bohrung: Zylinder Ø 5,2 mm für jede LED, Quader für USB-Buchse (12 × 11 mm) und Sensorkabel. Plant je Seite 0,5 mm Spiel ein.</li>'
    '<li><b>Deckel</b> als flache Platte extra bauen, gern mit eingeprägtem Namen (Text als Bohrung, 1 mm tief).</li>'
    '<li>Alles markieren, <b>gruppieren</b>, <b>Exportieren › .STL</b>. Die Lehrkraft druckt die Gehäuse bis Sitzung 08. Je kleiner, desto schneller.</li></ol>'
  + SP_CSS)

# Erwartungshorizont Aufgabe 1: gemeinsame Bauteile + projektabhängige Zeilen + Steckplan
_EH1_KOPF = ["Bauteil", "Material / Typ / Wert", "Anzahl", "Anschluss am Arduino"]
_EH1_ALLE = [
  ["Arduino Uno R3", "Mikrocontroller-Platine", "1", "USB-Buchse → Rechner"],
  ["USB-Kabel", "Typ A auf B", "1", "USB-Buchse des Arduino"],
  ["Steckbrett", "halbes, 400 Kontakte", "1", "Plus-Leiste an <b>5V</b>, Minus-Leiste an <b>GND</b>"],
  ['<span class="led g"></span>LED grün', "5 mm, Kunststoff", "1", "langes Bein an <b>Pin 7</b>"],
  ['<span class="led r"></span>LED rot', "5 mm, Kunststoff", "1", "langes Bein an <b>Pin 8</b>"],
  ["Widerstand", "<b>220 Ω</b> (rot-rot-braun)", "2", "je kurzes LED-Bein → <b>GND</b>"],
  ["Steckkabel", "Stecker–Stecker", "ca. 5–6", "5V, GND, Pin 7, Pin 8, Brücken"],
  ["Gehäuse + Deckel", "PLA, 3D-Druck", "1 + 1", "–"],
]
_EH1_PROJ = {
  "A": [["Wasserstandssensor", "Platine, analog, Pins S + −", "1", "S → <b>A0</b>, + → 5V, − → GND"],
        ["Steckkabel", "Buchse–Stecker, lang", "3", "vom Sensor im Übertopf zum Arduino"],
        ['<span class="gr">Tinkercad: Potentiometer</span>', "10 kΩ, Drehregler", "1", "Schleifer → A0, äußere Beine → 5V / GND"]],
  "B": [["TDS-Sensor (CQRobot)", "Sonde + Signalplatine", "1", "Signal (grün) → <b>A1</b>, + (rot) → 5V, − (schwarz) → GND"],
        ["Anschlusskabel", "3-adrig, aus der Packung", "1", "Platine (− + A) → Arduino"],
        ['<span class="gr">Tinkercad: Potentiometer</span>', "10 kΩ, Drehregler", "1", "Schleifer → A1, äußere Beine → 5V / GND"]],
  "C": [["DHT11", "Temperatur + Luftfeuchte, digital, 4 Beine", "1", "Bein 1 → 5V, Bein 2 → <b>Pin 2</b>, Bein 3 frei, Bein 4 → GND"],
        ["Widerstand", "<b>10 kΩ</b> (braun-schwarz-orange)", "1", "zwischen Bein 1 und Bein 2 (Pull-up)"],
        ['<span class="gr">Tinkercad: TMP36</span>', "Temperatursensor, analog", "1", "mittleres Bein → A2, außen → 5V / GND"],
        ['<span class="gr">Tinkercad: Potentiometer</span>', "10 kΩ, ersetzt Luftfeuchte", "1", "Schleifer → A3, äußere Beine → 5V / GND"]],
}
_EH1_LUECKE = {"A": "das Tinkercad-Ersatzteil steht statt des echten Sensors da",
               "B": "das Anschlusskabel der TDS-Platine fehlt, das Tinkercad-Ersatzteil steht statt des echten Sensors da",
               "C": "der 10-kΩ-Widerstand am DHT11 fehlt, TMP36 und Potentiometer fehlen für die Tinkercad-Fassung"}

def _eh1(k):
    return ('<h5>Für alle Projekte gleich (Anzeige und Grundaufbau)</h5>' + _tab(_EH1_KOPF, _EH1_ALLE)
            + '<h5>Projekt %s (echter Sensor in Sitzung 08, Ersatzteil in Tinkercad grau)</h5>' % k + _tab(_EH1_KOPF, _EH1_PROJ[k])
            + '<div class="st-tipp"><b>Woran man eine gute Liste erkennt:</b> Sie enthält <b>Kabel, Steckbrett und Gehäuse</b>. Pins und Widerstände stimmen mit dem Infokasten überein. '
              '<b>Häufige Lücken:</b> Vorwiderstände der LEDs fehlen, GND fehlt, %s. Beides eintragen ist ideal, eines genügt, wenn es gekennzeichnet ist.</div>' % _EH1_LUECKE[k]
            + '<h5>Bauplan · Steckplan in Tinkercad</h5>'
            + _fig(7, "bauplan-%s-steckplan" % k.lower(), "Steckplan Projekt %s · Tinkercad-Fassung" % k))

# Erwartungshorizont Aufgabe 2: Struktogramme
_EH2_NS = {
  "A": struktogramm("Gießwächter", ns_anw("schwelle ← 200"),
        ns_immer("wiederhole <b>für immer</b>", ns_anw("wert ← analogen Pin <b>A0</b> lesen"), ns_anw("wert im seriellen Monitor ausgeben"),
                 ns_wenn("wert <b>&lt;</b> schwelle ?", [ROT_AN], [GRUEN_AN]), ns_anw("warte 1 Sekunde"))),
  "B": struktogramm("Filterwächter", ns_anw("schwelle ← 600"),
        ns_immer("wiederhole <b>für immer</b>", ns_anw("wert ← analogen Pin <b>A1</b> lesen"), ns_anw("wert im seriellen Monitor ausgeben"),
                 ns_wenn("wert <b>&gt;</b> schwelle ?", [ROT_AN], [GRUEN_AN]), ns_anw("warte 1 Sekunde"))),
  "C": struktogramm("Lüftungswächter", ns_anw("maxT ← 25 &nbsp; maxH ← 60"),
        ns_immer("wiederhole <b>für immer</b>", ns_anw("t ← Temperatursensor an <b>A2</b> in °C lesen"),
                 ns_anw("h ← analogen Pin <b>A3</b> lesen, auf 0–100 abbilden"), ns_anw("t und h im seriellen Monitor ausgeben"),
                 ns_wenn("t <b>&gt;</b> maxT <b>und</b> h <b>&gt;</b> maxH ?", [ROT_AN], [GRUEN_AN]), ns_anw("warte 2 Sekunden"))),
}
_EH2_TIPP = {
  "A": "Rot heißt: zu wenig Wasser, also ein <b>kleiner</b> Wert. In Tinkercad liefert das Potentiometer 0 bis 1023, jeder Schwellenwert in diesem Bereich ist zulässig.",
  "B": "Rot heißt: viele gelöste Stoffe, also ein <b>großer</b> Wert, umgekehrt als bei A. Der Rohwert ersetzt heute die ppm. "
       "Mittelwert aus 30 Messungen und TDS-Formel kommen in Sitzung 08 hinzu, als Zusatz geht schon jetzt eine Zählschleife „wiederhole 30-mal“.",
  "C": "Rot nur, wenn <b>beide</b> Werte zu hoch sind. Gleichwertig ist eine <b>verschachtelte</b> Verzweigung: wenn t &gt; maxT, dann (wenn h &gt; maxH, dann rot, sonst grün), sonst grün. "
       "Ein <b>oder</b> ist fachlich falsch. Das Abbilden auf 0–100 % ist ein Plus, der Rohwert mit passend großem Schwellenwert (z. B. 600) ist auch richtig.",
}
_EH2_BEWERTUNG = (
  '<h5>Daran prüft ihr euer Struktogramm</h5><ul class="task-list">'
  '<li>Die Wiederholung „für immer“ umschließt Lesen, Vergleich und Anzeige.</li>'
  '<li>Der Sensorwert wird in einer <b>Variablen</b> gespeichert, am richtigen Pin.</li>'
  '<li>Die Verzweigung prüft in die richtige Richtung (A: &lt;, B: &gt;, C: und).</li>'
  '<li>Beide Zweige schalten <b>beide</b> LEDs, sonst bleibt eine an.</li>'
  '<li>Am Ende wird gewartet, sonst rauscht der Monitor.</li></ul>'
  '<p class="gr">Nicht verlangt: <code>pinMode</code> und <code>Serial.begin</code>, die erzeugt Tinkercad selbst in <code>setup()</code>.</p>')

def _eh2(k):
    return ('<h5>Bauplan · Struktogramm (Tinkercad-Fassung)</h5>' + _EH2_NS[k]
            + '<div class="st-tipp">%s</div>' % _EH2_TIPP[k] + _EH2_BEWERTUNG)

# Erwartungshorizont Aufgabe 3: Gehäuse
_EH3 = {
  "A": ("Wasserstandssensor ca. 62 × 20 × 8, <b>bleibt außen</b> im Übertopf, kommt nicht ins Innenmaß",
        "≈ 160 × 60 × 35", "L: 2 + 68,6 + 3 + 82 + 2 · B: 55 + 2 · 2 · H: 15 + 20", "≈ 164 × 64 × 37",
        "Kabeldurchführung für 3 Adern zum Sensor, ca. 10 × 5, seitlich unten"),
  "B": ("Signalplatine ca. 42 × 32 × 10 <b>innen</b>, die Sonde bleibt außen im Wasser",
        "≈ 160 × 95 × 35", "wie A, Platine vor dem Arduino · B: 53,3 + 3 + 32 + 2 · 3", "≈ 164 × 99 × 37",
        "Durchführung für das Sondenkabel samt Stecker, ca. 10 × 8"),
  "C": ("DHT11 ca. 15,5 × 12 × 5,5, sitzt auf dem Steckbrett und braucht keinen eigenen Platz",
        "≈ 160 × 60 × 35", "wie A", "≈ 164 × 64 × 37",
        "<b>Lüftungsschlitze</b> (z. B. 4 × 2 × 15) direkt neben dem DHT11, damit er die Raumluft misst und nicht die warme Luft im Gehäuse"),
}

def _eh3(k):
    sensor, innen, rechnung, aussen, oeffnung = _EH3[k]
    tab = _tab(["Teil", "Projekt %s · Richtwert in mm (L × B × H)" % k], [
        ["Arduino Uno", "68,6 × 53,3 × 15 (vorgegeben)"],
        ["Steckbrett (halb, 400)", "ca. 82 × 55 × 8,5"],
        ["Sensor / Platine", sensor],
        ["Kabelreserve oben", "ca. 20 mm (Steckkabel, LED-Beine ragen über das Steckbrett)"],
        ["<b>Innenmaß</b>", "<b>%s</b><br><span class=\"gr\">%s</span>" % (innen, rechnung)],
        ["<b>Außenmaß</b> (Innenmaß + 2 · 2 mm)", "<b>%s</b>" % aussen],
        ["Öffnungen (alle)", "2 × Ø 5,2 mm für die LEDs im Deckel über dem Steckbrett · USB-Buchse ca. 13 × 12 an der Stirnseite beim Arduino (12 × 11 + Spiel)"],
        ["Öffnungen (Projekt %s)" % k, oeffnung]])
    return ('<p>Annahme: <b>Arduino und Steckbrett liegen nebeneinander</b>, je 2–3 mm Luft zwischen den Teilen und zur Wand. '
            'Andere sinnvolle Anordnungen sind gleichwertig, wenn die Rechnung stimmt. Gemessene Werte dürfen um einige Millimeter abweichen.</p>'
            + tab
            + '<div class="st-tipp"><b>Höhe: + 2 oder + 4 mm?</b> Für die Höhe reicht + 2 mm (nur der Boden), weil der Deckel als eigene Platte gebaut wird. '
              'Beides ist richtig. <b>Länge und Breite</b> müssen + 4 mm sein (zwei Wände).</div>'
            + '<h5>Bauplan · Gehäuse</h5>' + _fig(7, "bauplan-%s-gehaeuse" % k.lower(), "Gehäuse Projekt %s · Draufsicht und Seitenansicht" % k)
            + '<h5>Daran prüft ihr euer Gehäuse</h5><ul class="task-list">'
              '<li>Alle Zeilen mit drei Maßen gefüllt, Einheit mm, Messwerte plausibel (± 5 mm).</li>'
              '<li>Das Innenmaß ergibt sich nachvollziehbar aus den Teilen plus Luft, nicht nur aus dem größten Teil.</li>'
              '<li>Außenmaß = Innenmaß + Wandstärken, richtig gerechnet.</li>'
              '<li>Öffnungen für LEDs, USB und Sensorkabel genannt%s.</li>'
              '<li><b>Plus:</b> 0,5 mm Spiel je Seite bei den Aussparungen, Name im Deckel, Gehäuse so klein wie möglich.</li></ul>'
            % (", bei C zusätzlich Lüftung" if k == "C" else ""))

# Erwartungshorizont Aufgabe 4: Block → C++
def _eh4(k):
    lesen = {"A": ["analogen Pin A0 lesen", "<code>analogRead(A0)</code>"],
             "B": ["analogen Pin A1 lesen", "<code>analogRead(A1)</code>"],
             "C": ["Temperatursensor an Pin A2 in °C lesen; analogen Pin A3 lesen",
                   "<code>-40 + 0.488155 * (analogRead(A2) - 20)</code><br><code>analogRead(A3)</code>"]}[k]
    festlegen = {"A": "<code>wert = analogRead(A0);</code>", "B": "<code>wert = analogRead(A1);</code>",
                 "C": "<code>t = -40 + 0.488155 * (analogRead(A2) - 20);</code><br><code>h = map(analogRead(A3), 0, 1023, 0, 100);</code>"}[k]
    variable = {"A": "Variable erstellen: wert", "B": "Variable erstellen: wert", "C": "Variablen erstellen: t, h, maxT, maxH"}[k]
    var_cpp = {"A": "<code>int wert = 0;</code> (oben, vor <code>setup</code>)", "B": "<code>int wert = 0;</code> (oben, vor <code>setup</code>)",
               "C": "<code>int t = 0;</code> usw. (oben, vor <code>setup</code>)"}[k]
    bed = {"A": ["wert &lt; schwelle", "<code>if (wert &lt; schwelle)</code>"], "B": ["wert &gt; schwelle", "<code>if (wert &gt; schwelle)</code>"],
           "C": ["(t &gt; maxT) und (h &gt; maxH)", "<code>if (t &gt; maxT &amp;&amp; h &gt; maxH)</code>"]}[k]
    warten = ["2 Sekunden warten", "<code>delay(2000);</code>"] if k == "C" else ["1 Sekunden warten", "<code>delay(1000);</code>"]
    tab = _tab(["Steuerelement", "Block in Tinkercad", "C++-Syntax"], [
        ["Wiederholung", "für immer", "<code>void loop() { … }</code>"],
        ["Ausgabe: LED an", "Pin 8 auf HOCH setzen", "<code>digitalWrite(8, HIGH);</code>"],
        ["Ausgabe: LED aus", "Pin 7 auf NIEDRIG setzen", "<code>digitalWrite(7, LOW);</code>"],
        ["Eingabe: Sensor lesen"] + lesen,
        ["Variable", variable + "<br>… festlegen auf …", var_cpp + "<br>" + festlegen],
        ["Verzweigung", "wenn … dann … sonst", "<code>if (…) { … } else { … }</code>"],
        ["Bedingung / Vergleich"] + bed,
        ["Warten"] + warten,
        ["Serieller Monitor", "auf seriellem Monitor ausgeben: wert, mit Zeilenumbruch",
         "<code>Serial.println(wert);</code><br>dazu in <code>setup()</code>: <code>Serial.begin(9600);</code>"]])
    weiter = {"A": "Nur der Schwellenwert wird am echten Sensor nachgemessen (Muster: 200).",
              "B": "Mittelwert aus 30 Messungen und TDS-Formel aus der Anschlusskarte, Vergleich in ppm (Muster: 400 ppm).",
              "C": "Bibliothek <code>DHT.h</code>: <code>dht.readTemperature()</code> und <code>dht.readHumidity()</code> ersetzen TMP36 und Potentiometer, Grenzen 25 °C und 60 %."}[k]
    datei = "tinkercad-projekt-%s.ino" % k.lower()
    return (tab
            + '<div class="st-tipp"><b>Worauf achten:</b> Semikolon nach jeder Anweisung, geschweifte Klammern bei <code>loop</code>, <code>if</code> und <code>else</code>. '
              '<code>HIGH</code>/<code>LOW</code> großgeschrieben, <code>analogRead</code> und <code>digitalWrite</code> mit großem R bzw. W. '
              '<code>=</code> legt fest, <code>&lt;</code> und <code>&gt;</code> vergleichen, „und“ heißt in C++ <code>&amp;&amp;</code>. '
              'Zeilen wie <code>pinMode(7, OUTPUT);</code> schreibt Tinkercad automatisch in <code>setup()</code>.</div>'
            + '<h5>Bauplan · Musterprogramm für Tinkercad</h5>' + _codeblock(datei, "Projekt %s · C++" % k)
            + '<p><b>Ausblick auf Sitzung 08:</b> %s</p>' % weiter)

# Impulsfragen (richtige Antwort an wechselnder Stelle; proj = nur für diese Projekte)
LP07_V3_STUFEN = dict(
  intro=('<p>Arbeitet zuerst auf dem Planungsblatt (Rückseite, Aufgaben 1–4). Kommt ihr nicht weiter oder seid fertig, helfen euch die <b>Impulsfragen</b>: '
         'Jede falsche Antwort gibt einen Tipp. Habt ihr alle Fragen einer Aufgabe richtig, erscheint der <b>Erwartungshorizont</b> mit dem passenden '
         '<b>Bauplan</b> (Steckplan, Struktogramm, Gehäuse, Musterprogramm). Ergänzt dann euer Blatt in einer anderen Farbe. Jede:r kann die Fragen für sich durchgehen.</p>'),
  projekte=SP_PROJEKTE,
  aufgaben=[
    dict(nr=1, titel="Bauteile und Materialien",
         auftrag="Tragt alle Bauteile ein, die ihr braucht, auch Kabel, Steckbrett und Gehäuse: Material / Typ / Wert, Anzahl und Anschluss am Arduino.",
         eh={k: _eh1(k) for k in "ABC"},
         fragen=[
           dict(q="Jede LED braucht einen Vorwiderstand. Welchen nehmt ihr, und wie viele?", done="Richtig: zwei Widerstände mit 220 Ω, je vom kurzen LED-Bein nach GND.",
                opts=[("10 kΩ (braun-schwarz-orange), einer für beide LEDs", False, "10 kΩ ist viel zu groß, die LED bliebe fast dunkel. Und jede LED bekommt ihren eigenen Widerstand."),
                      ("keinen, der Arduino begrenzt den Strom selbst", False, "Ohne Vorwiderstand fließt zu viel Strom, LED oder Pin können kaputtgehen."),
                      ("220 Ω (rot-rot-braun), je LED einer, also zwei", True, None),
                      ("220 Ω, einer reicht für beide LEDs", False, "Laut Infokasten geht jede LED über ihren eigenen 220-Ω-Widerstand an GND.")]),
           dict(q="An welchen Pin kommt das lange Bein (Anode) der roten LED?", done="Genau: rot an Pin 8, grün an Pin 7.",
                opts=[("Pin 7", False, "Pin 7 ist für die grüne LED."),
                      ("GND", False, "An GND kommt das kurze Bein, über den Widerstand."),
                      ("5V", False, "An 5V würde die LED immer leuchten, der Arduino könnte sie nicht schalten."),
                      ("Pin 8", True, None)]),
           dict(q="Was fehlt in vielen Bauteillisten, obwohl es ausdrücklich in der Aufgabe steht?", done="Richtig, ohne Kabel, Steckbrett und Gehäuse lässt sich nichts nachbauen.",
                opts=[("der Arduino selbst", False, "Der steht meist drin. Lies die Aufgabe noch einmal: Was soll ausdrücklich mit in die Liste?"),
                      ("Kabel, Steckbrett und Gehäuse", True, None),
                      ("der Rechner, an dem programmiert wird", False, "Der Rechner gehört nicht zum Wächter."),
                      ("die Uhrzeit der Messung", False, "Das ist kein Bauteil.")]),
           dict(q="Wie bekommen Sensor und LEDs auf dem Steckbrett Strom (5V) und Masse (GND)?", done="Genau, die Leisten am Rand verteilen 5V und GND an alle Bauteile.",
                opts=[("Jedes Bauteil bekommt ein eigenes Kabel direkt zum Pin 5V.", False, "Der Arduino hat nur einen 5V-Pin. Dafür gibt es die langen Leisten am Rand des Steckbretts."),
                      ("Über das USB-Kabel, das direkt im Steckbrett steckt.", False, "Das USB-Kabel steckt nur im Arduino."),
                      ("Plus-Leiste an 5V, Minus-Leiste an GND, die Bauteile holen sich Strom und Masse von dort.", True, None),
                      ("Die Leisten am Rand sind schon von selbst angeschlossen.", False, "Erst Kabel von 5V und GND verbinden die Leisten mit dem Arduino.")]),
           dict(proj="A", q="Tinkercad hat keinen Wasserstandssensor. Was nehmt ihr dort, und wie wird es angeschlossen?", done="Richtig, das Potentiometer liefert wie der Sensor Werte von 0 bis 1023.",
                opts=[("einen Taster an Pin 2", False, "Ein Taster kennt nur gedrückt oder nicht. Der Wasserstand hat viele Stufen."),
                      ("eine dritte LED an A0", False, "Eine LED ist eine Ausgabe. Gesucht ist eine Eingabe mit vielen Werten."),
                      ("einen TMP36 an A2", False, "Der TMP36 ist der Ersatz in Projekt C. Schaut auf eure Projektkarte."),
                      ("ein Potentiometer: mittleres Bein (Schleifer) an A0, äußere Beine an 5V und GND", True, None)]),
           dict(proj="A", q="Wo steckt der echte Wasserstandssensor, und was braucht ihr dafür zusätzlich?", done="Genau, deshalb gehören drei lange Kabel in die Liste.",
                opts=[("im Übertopf; ihr braucht drei lange Kabel (Buchse–Stecker) zum Arduino", True, None),
                      ("auf dem Steckbrett, er braucht nichts extra", False, "Er muss im Wasservorrat der Pflanze stecken, weit weg vom Steckbrett."),
                      ("im Gehäuse neben dem Arduino", False, "Im Gehäuse misst er keinen Wasserstand. Er bleibt außen im Übertopf."),
                      ("Er braucht einen 10-kΩ-Widerstand.", False, "Den Widerstand braucht der DHT11 aus Projekt C.")]),
           dict(proj="B", q="Was ersetzt in Tinkercad den TDS-Sensor?", done="Richtig, das Potentiometer liefert Werte von 0 bis 1023.",
                opts=[("ein Wasserstandssensor an A0", False, "Den gibt es in Tinkercad nicht, und A0 gehört zu Projekt A."),
                      ("ein Potentiometer: Schleifer an A1, äußere Beine an 5V und GND", True, None),
                      ("ein Fotowiderstand an Pin 7", False, "Pin 7 ist für die grüne LED reserviert, der TDS-Wert kommt an A1."),
                      ("gar nichts, das Programm erfindet Werte", False, "Ohne Eingabe gibt es nichts zu messen. Ihr braucht ein Bauteil mit Werten von 0 bis 1023.")]),
           dict(proj="B", q="Woraus besteht der echte TDS-Sensor?", done="Genau, Sonde, Platine und das Kabel aus der Packung gehören alle in die Liste.",
                opts=[("nur aus einer Sonde, die direkt in A1 steckt", False, "Zwischen Sonde und Arduino sitzt eine Platine, die das Signal aufbereitet."),
                      ("aus einem Taster und einer LED", False, "Das wäre eine Anzeige, kein Sensor."),
                      ("aus Sonde und Signalplatine, dazu das 3-adrige Kabel aus der Packung (grün an A1, rot an 5V, schwarz an GND)", True, None),
                      ("aus vier Beinchen wie der DHT11", False, "Vier Beinchen hat der DHT11 aus Projekt C.")]),
           dict(proj="C", q="Was braucht der DHT11 zusätzlich auf dem Steckbrett?", done="Richtig, ohne diesen Pull-up meldet er meist „Sensorfehler“.",
                opts=[("einen 10-kΩ-Widerstand (braun-schwarz-orange) zwischen Bein 1 und Bein 2", True, None),
                      ("einen 220-Ω-Widerstand vor Bein 4", False, "220 Ω sind für die LEDs. Der DHT11 braucht einen Widerstand zwischen Bein 1 (5V) und Bein 2 (Daten)."),
                      ("ein Potentiometer an Bein 3", False, "Bein 3 bleibt frei."),
                      ("nichts, er wird direkt in A0 gesteckt", False, "Der DHT11 sendet digitale Daten an Pin 2, nicht an einen Analog-Pin.")]),
           dict(proj="C", q="Tinkercad hat keinen DHT11. Womit messt ihr dort Temperatur und Luftfeuchte?", done="Genau, zwei Ersatzteile für zwei Messwerte.",
                opts=[("mit zwei Tastern, einer für warm, einer für feucht", False, "Taster liefern nur an oder aus. Ihr braucht Bauteile mit vielen Messwerten."),
                      ("mit einem TMP36 für beide Werte", False, "Der TMP36 misst nur die Temperatur. Für die Feuchte braucht ihr ein zweites Bauteil."),
                      ("mit einem Potentiometer an Pin 2", False, "Ein Potentiometer liefert einen analogen Wert und gehört an einen A-Pin."),
                      ("mit einem TMP36 an A2 (Temperatur) und einem Potentiometer an A3 (Ersatz für die Luftfeuchte)", True, None)]),
         ]),
    dict(nr=2, titel="Struktogramm",
         auftrag="Plant das Programm mit Anweisung, Verzweigung (wenn … dann … sonst) und Wiederholung (für immer), bevor ihr Blöcke setzt.",
         eh={k: _eh2(k) for k in "ABC"},
         fragen=[
           dict(q="Welcher Baustein umschließt Messen, Vergleichen und Anzeigen?", done="Richtig, der Wächter misst ständig neu.",
                opts=[("eine Verzweigung wenn … dann", False, "Die Verzweigung entscheidet nur. Der Wächter soll aber immer wieder neu messen."),
                      ("die Wiederholung „für immer“", True, None),
                      ("eine einzelne Anweisung", False, "Eine Anweisung läuft nur einmal."),
                      ("gar keiner, das Programm läuft einmal durch", False, "Dann würde der Wächter nur beim Start messen.")]),
           dict(q="Wo merkt sich das Programm den gemessenen Wert?", done="Genau, eine Variable ist das Gedächtnis des Programms.",
                opts=[("in der LED", False, "Die LED zeigt nur an, sie speichert nichts."),
                      ("im Schwellenwert", False, "Der Schwellenwert ist die feste Grenze. Der Messwert ändert sich und braucht einen eigenen Speicherplatz."),
                      ("im seriellen Monitor", False, "Der Monitor zeigt den Wert nur an."),
                      ("in einer Variablen, z. B. wert (bei C: t und h)", True, None)]),
           dict(proj="A", q="Wann soll beim Gießwächter die rote LED leuchten?", done="Richtig: wenig Wasser, kleiner Messwert.",
                opts=[("wenn wert > schwelle", False, "Ein großer Wert heißt: Der Sensor steckt tief im Wasser. Dann ist genug da."),
                      ("wenn wert < schwelle", True, None),
                      ("erst wenn wert = 0 ist", False, "Dann wäre der Topf schon ganz trocken. Ihr wollt vorher gewarnt werden."),
                      ("immer abwechselnd mit grün", False, "Die Farbe hängt vom Messwert ab, nicht von der Zeit.")]),
           dict(proj="B", q="Wann soll beim Filterwächter die rote LED leuchten?", done="Richtig: viele gelöste Stoffe, großer Messwert.",
                opts=[("wenn wert < schwelle", False, "Ein kleiner TDS-Wert heißt: wenig gelöste Stoffe, der Filter arbeitet."),
                      ("wenn wert genau gleich schwelle ist", False, "Genau gleich kommt fast nie vor. Ihr braucht einen Bereich."),
                      ("wenn wert > schwelle", True, None),
                      ("nie, ein Filter hält ewig", False, "Genau dafür baut ihr den Wächter.")]),
           dict(proj="C", q="Wann soll beim Lüftungswächter die rote LED leuchten?", done="Richtig, erst warm und feucht zusammen ist ein Schimmelrisiko.",
                opts=[("wenn t > maxT und h > maxH", True, None),
                      ("wenn t > maxT oder h > maxH", False, "Lest die Projektkarte: Temperatur und Luftfeuchte zu hoch. Nur warm ist noch kein Schimmelrisiko."),
                      ("wenn nur h > maxH", False, "Die Karte nennt zwei Bedingungen."),
                      ("wenn t < maxT", False, "Kühle Luft ist nicht das Problem.")]),
           dict(q="Im Ja-Zweig steht nur „Pin 8 auf HOCH“. Was passiert, wenn danach wieder der Nein-Zweig mit „Pin 7 auf HOCH“ läuft?", done="Genau, deshalb schaltet jeder Zweig beide LEDs.",
                opts=[("Das Programm stürzt ab.", False, "Der Code läuft, er tut nur nicht das Gewünschte."),
                      ("Die rote LED geht von selbst aus.", False, "Ein Pin bleibt HOCH, bis das Programm ihn auf NIEDRIG stellt."),
                      ("Am Ende leuchten beide LEDs, weil Pin 8 nie auf NIEDRIG gestellt wird.", True, None),
                      ("Nichts Besonderes, es leuchtet weiter nur eine LED.", False, "Probiert es in der Simulation aus: Rot bleibt an.")]),
           dict(q="Wozu steht am Ende der Wiederholung „warte 1 Sekunde“ (bei C 2 Sekunden)?", done="Richtig. Der DHT11 misst ohnehin nur alle 2 Sekunden neu.",
                opts=[("damit die LED heller wird", False, "Die Wartezeit hat mit der Helligkeit nichts zu tun."),
                      ("damit der Arduino abkühlt", False, "Der Arduino wird dabei nicht heiß."),
                      ("damit der Schwellenwert neu berechnet wird", False, "Der Schwellenwert bleibt fest."),
                      ("damit der Monitor nicht rauscht und die Werte lesbar bleiben", True, None)]),
           dict(proj="AB", q="Welche Werte liefert das Potentiometer in Tinkercad am Analog-Pin?", done="Genau, analogRead kennt 1024 Stufen. Jeder Schwellenwert dazwischen ist erlaubt.",
                opts=[("0 bis 5", False, "5 V ist die Spannung. analogRead übersetzt sie in eine Zahl mit 1024 Stufen."),
                      ("nur HOCH oder NIEDRIG", False, "Das liefert ein Digitalpin. Ein Analogpin kennt viele Stufen."),
                      ("0 bis 1023", True, None),
                      ("0 bis 100", False, "Auf 0 bis 100 rechnet erst map() um, wie bei Projekt C.")]),
           dict(proj="C", q="Wie wird aus dem Potentiometerwert an A3 eine Luftfeuchte in Prozent?", done="Richtig. Den Rohwert mit einem großen Schwellenwert (z. B. 600) zu vergleichen, ist auch erlaubt.",
                opts=[("Man teilt ihn durch 2.", False, "1023 / 2 wären über 500 %."),
                      ("Mit map: von 0 bis 1023 auf 0 bis 100 abbilden.", True, None),
                      ("Gar nicht, man vergleicht den Rohwert direkt mit 60.", False, "Der Rohwert geht bis 1023, 60 wäre fast immer überschritten. Entweder umrechnen oder den Schwellenwert anpassen."),
                      ("Der TMP36 rechnet das aus.", False, "Der TMP36 misst nur die Temperatur.")]),
         ]),
    dict(nr=3, titel="Gehäuse vermessen",
         auftrag="Messt mit Lineal oder Messschieber, alle Maße in mm. Rechnet Innen- und Außenmaß aus und plant die Öffnungen an Seite und Deckel. Baut das Gehäuse dann im Tinkercad-3D-Entwurf.",
         eh={k: _eh3(k) for k in "ABC"},
         fragen=[
           dict(q="Wie dick sind Wand und Boden des Gehäuses?", done="Richtig, 2 mm sind stabil und drucken schnell.",
                opts=[("0,5 mm", False, "0,5 mm ist das Spiel für Aussparungen, nicht die Wand."),
                      ("2 cm", False, "Das wäre ein schwerer Klotz mit sehr langer Druckzeit."),
                      ("10 mm", False, "Schaut in die Anleitung „Gehäuse aus dem 3D-Drucker“, Schritt 1."),
                      ("2 mm", True, None)]),
           dict(q="Arduino und Steckbrett liegen nebeneinander. Wie berechnet ihr die Innenlänge?", done="Genau: 2 + 68,6 + 3 + 82 + 2 ≈ 160 mm.",
                opts=[("nur die Länge des Steckbretts, weil es das größte Teil ist", False, "Beide Teile liegen nebeneinander, ihre Längen addieren sich."),
                      ("Länge Arduino + Länge Steckbrett + etwas Luft dazwischen und zur Wand", True, None),
                      ("Länge des Arduino mal 2", False, "Das Steckbrett ist länger als der Arduino. Messt beide Teile."),
                      ("Außenmaß minus 10 cm", False, "Ihr startet innen mit den Teilen und rechnet dann nach außen.")]),
           dict(q="Wie kommt ihr bei Länge und Breite vom Innenmaß zum Außenmaß?", done="Richtig, links und rechts je eine Wand.",
                opts=[("+ 2 mm", False, "Es gibt zwei Wände, auf jeder Seite eine."),
                      ("mal 2", False, "Das Gehäuse wäre doppelt so groß wie nötig."),
                      ("+ 4 mm (2 · 2 mm, zwei Wände)", True, None),
                      ("gar nicht, innen und außen sind gleich", False, "Die Wand hat eine Dicke. Die kommt außen dazu.")]),
           dict(q="Warum reicht bei der Höhe + 2 mm?", done="Genau. Wer + 4 mm rechnet, liegt auch richtig.",
                opts=[("Weil der Deckel eine eigene Platte ist, gerechnet wird nur der Boden.", True, None),
                      ("Weil das Gehäuse oben offen bleibt.", False, "Es gibt einen Deckel, er wird nur extra gebaut."),
                      ("Weil der Arduino nur 2 mm hoch ist.", False, "Der Arduino ist mit Buchsen etwa 15 mm hoch."),
                      ("Das stimmt nicht, man muss + 6 mm rechnen.", False, "Ein Boden von 2 mm, der Deckel kommt extra.")]),
           dict(q="Welcher Durchmesser passt für die Bohrung einer 5-mm-LED?", done="Richtig, ein wenig Spiel gleicht Ungenauigkeiten beim Druck aus.",
                opts=[("5,0 mm", False, "Ganz ohne Spiel klemmt die LED, der Druck wird nie ganz genau."),
                      ("3 mm", False, "Da passt die LED nicht durch."),
                      ("8 mm", False, "Dann fällt die LED durch."),
                      ("5,2 mm", True, None)]),
           dict(proj="A", q="Was gehört beim Gießwächter nicht ins Innenmaß?", done="Richtig, er steckt im Übertopf. Ins Gehäuse kommt nur eine Kabeldurchführung.",
                opts=[("der Arduino", False, "Der Arduino ist das Herz des Wächters und gehört ins Gehäuse."),
                      ("der Wasserstandssensor, er bleibt außen im Übertopf", True, None),
                      ("das Steckbrett", False, "Das Steckbrett liegt im Gehäuse."),
                      ("die Kabelreserve oben", False, "Ohne Reserve passt der Deckel nicht auf die Steckkabel.")]),
           dict(proj="B", q="Was macht das Gehäuse beim Filterwächter breiter als bei A?", done="Genau, deshalb wird es innen etwa 95 statt 60 mm breit.",
                opts=[("die TDS-Sonde", False, "Die Sonde hängt im Wasser, also außen."),
                      ("der längere Arduino", False, "Alle Projekte nutzen denselben Arduino Uno."),
                      ("die Signalplatine (ca. 42 × 32 mm), sie liegt innen vor dem Arduino", True, None),
                      ("die Lüftungsschlitze", False, "Lüftungsschlitze braucht Projekt C.")]),
           dict(proj="C", q="Welche Öffnung braucht nur der Lüftungswächter?", done="Richtig, sonst misst der DHT11 die warme Luft im Gehäuse.",
                opts=[("eine Durchführung für die Sonde", False, "Eine Sonde hat Projekt B."),
                      ("Lüftungsschlitze direkt neben dem DHT11, damit er die Raumluft misst", True, None),
                      ("eine zweite USB-Öffnung", False, "Ein USB-Anschluss reicht."),
                      ("ein Loch für einen Wasserschlauch", False, "Im Heizkeller wird Luft gemessen, kein Wasser.")]),
         ]),
    dict(nr=4, titel="Vom Block zur C++-Zeile",
         auftrag="Stellt in Tinkercad den Code auf „Blöcke + Text“ und tragt für jedes Steuerelement euren Block und die C++-Zeile daneben ein.",
         eh={k: _eh4(k) for k in "ABC"},
         fragen=[
           dict(q="Welche C++-Zeile gehört zum Block „Pin 8 auf HOCH setzen“?", done="Richtig, digitalWrite schaltet einen Ausgang.",
                opts=[("pinMode(8, HIGH);", False, "pinMode legt nur fest, ob der Pin Eingang oder Ausgang ist."),
                      ("digitalWrite(8, HIGH);", True, None),
                      ("analogRead(8);", False, "analogRead liest einen Wert ein. Eine LED ist eine Ausgabe."),
                      ("digitalwrite(8, high);", False, "C++ unterscheidet Groß- und Kleinschreibung: digitalWrite und HIGH.")]),
           dict(q="Wie heißt der Block „für immer“ in C++?", done="Genau, loop() wiederholt sich, solange der Arduino Strom hat.",
                opts=[("void setup() { … }", False, "setup() läuft nur einmal beim Start."),
                      ("if (immer) { … }", False, "if ist eine Verzweigung, keine Wiederholung."),
                      ("void loop() { … }", True, None),
                      ("delay(immer);", False, "delay wartet nur eine bestimmte Zeit.")]),
           dict(proj="A", q="Welche Zeile liest den Wert an A0 und speichert ihn?", done="Richtig, links die Variable, rechts der Messwert.",
                opts=[("wert == analogRead(A0);", False, "== vergleicht. Zum Festlegen braucht ihr ein einzelnes =."),
                      ("analogRead(A0) = wert;", False, "Links steht immer die Variable, die den Wert bekommt."),
                      ("digitalRead(A0);", False, "digitalRead kennt nur HIGH oder LOW, und gespeichert wird so nichts."),
                      ("wert = analogRead(A0);", True, None)]),
           dict(proj="B", q="Welche Zeile liest den Wert an A1 und speichert ihn?", done="Richtig, links die Variable, rechts der Messwert.",
                opts=[("wert = analogRead(A1);", True, None),
                      ("wert == analogRead(A1);", False, "== vergleicht. Zum Festlegen braucht ihr ein einzelnes =."),
                      ("analogRead(A1) = wert;", False, "Links steht immer die Variable, die den Wert bekommt."),
                      ("digitalRead(A1);", False, "digitalRead kennt nur HIGH oder LOW, und gespeichert wird so nichts.")]),
           dict(proj="C", q="Wie heißt die Bedingung „(t > maxT) und (h > maxH)“ in C++?", done="Richtig, && ist das „und“ in C++.",
                opts=[("if (t > maxT || h > maxH)", False, "|| bedeutet oder. Gesucht ist und."),
                      ("if (t > maxT && h > maxH)", True, None),
                      ("if (t > maxT und h > maxH)", False, "C++ versteht kein deutsches „und“."),
                      ("if (t > maxT; h > maxH)", False, "Ein Semikolon trennt Anweisungen, keine Bedingungen.")]),
           dict(q="Was ist der Unterschied zwischen = und < im Programm?", done="Genau, festlegen und vergleichen sind zwei verschiedene Dinge.",
                opts=[("Es gibt keinen, beide vergleichen.", False, "= legt einen Wert fest, < vergleicht zwei Werte."),
                      ("= vergleicht, < legt einen Wert fest.", False, "Genau umgekehrt."),
                      ("= legt einen Wert fest (wert = …), < vergleicht zwei Werte (wert < schwelle).", True, None),
                      ("< gibt es nur für Kommazahlen.", False, "< funktioniert für alle Zahlen.")]),
           dict(q="Welche Zeile wartet 1 Sekunde?", done="Richtig, delay zählt in Millisekunden. Bei C sind es 2000.",
                opts=[("delay(1000);", True, None),
                      ("delay(1);", False, "delay zählt in Millisekunden. 1 ms ist viel zu kurz."),
                      ("wait(1);", False, "Diesen Befehl kennt Arduino nicht."),
                      ("sleep(1000);", False, "Arduino nutzt delay, nicht sleep.")]),
           dict(q="In eurer Tabelle fehlen pinMode(…) und Serial.begin(9600). Ist das schlimm?", done="Richtig. Wer sie trotzdem erklärt, zeigt gutes Verständnis.",
                opts=[("Ja, ohne sie ist die Tabelle falsch.", False, "Für die Tabelle sind sie nicht verlangt, weil ihr dafür keinen eigenen Block setzt."),
                      ("Nein, Tinkercad schreibt sie selbst in setup().", True, None),
                      ("Nein, weil der Arduino sie nicht braucht.", False, "Der Arduino braucht sie, Tinkercad ergänzt sie nur automatisch."),
                      ("Ja, man muss sie in loop() schreiben.", False, "Sie gehören in setup(), weil sie nur einmal nötig sind.")]),
         ]),
  ])

LP07_V3_LOESUNG = [
  "Die Erwartungshorizonte zu den Aufgaben 1–4 erscheinen oben im Abschnitt „Schritt für Schritt“, sobald alle Impulsfragen eurer Aufgabe richtig beantwortet sind.",
  "Rot leuchtet bei A, wenn <code>wert &lt; schwelle</code> (wenig Wasser), bei B, wenn <code>wert &gt; schwelle</code> (viele gelöste Stoffe), bei C nur, wenn <code>t &gt; maxT &amp;&amp; h &gt; maxH</code>. Jeder Zweig schaltet beide LEDs.",
  "Gehäuse: innen ≈ 160 × 60 × 35 mm (A, C) bzw. 160 × 95 × 35 mm (B), außen + 4 mm in Länge und Breite, + 2 mm in der Höhe.",
  _codeblock("tinkercad-projekt-a.ino", "Projekt A · Gießwächter (Tinkercad)"),
  _codeblock("tinkercad-projekt-b.ino", "Projekt B · Filterwächter (Tinkercad)"),
  _codeblock("tinkercad-projekt-c.ino", "Projekt C · Lüftungswächter (Tinkercad)"),
]

LP07_V3_VERTIEFUNG = (
  "<p>Fertig und alles verglichen? Wählt eine Erweiterung, die ihr in Sitzung 08 am echten Arduino weiterbaut.</p>"
  "<h3>🟡 Vorwarnung</h3><p>Ergänzt eine <b>gelbe LED</b> an Pin 9 und einen zweiten Schwellenwert: grün = alles gut, gelb = bald handeln, rot = jetzt handeln. "
  "Im Struktogramm wird daraus eine verschachtelte Verzweigung.</p>"
  "<h3>🔁 Ruhige Messwerte (B)</h3><p>Messt mit einer Zählschleife „wiederhole 30-mal“ und bildet den Mittelwert. So arbeitet auch das Musterprogramm für den echten TDS-Sensor.</p>"
  "<h3>🏷️ Gehäuse mit Namen</h3><p>Prägt den Namen eures Wächters 1 mm tief in den Deckel und macht das Gehäuse so klein wie möglich: Jede gesparte Minute Druckzeit zählt.</p>"
  "<style>.vertiefung h3{font-size:1rem;margin:1.1rem 0 .4rem;color:var(--key)}</style>")

# ---------------------------------------------------------------- LP08 · Bauen und testen
def _anschlusskarte(nr, name, fig, kabel, stecker, monitor, achtung, code):
    rows = "".join("<tr><td>%s</td><td><b>%s</b></td><td>%s</td></tr>" % z for z in kabel)
    return ('<h3>Sensor %d · %s</h3>%s'
            '<div class="tbl"><table><tr><th>Kabel</th><th>Sensor</th><th>Arduino</th></tr>%s</table></div>'
            '<p>%s</p><p><b>Im Monitor:</b> %s</p><div class="sp-hinweis"><b>⚠ Achtung:</b> %s</div>%s'
            ) % (nr, name, _fig(8, fig, "Anschlusskarte Sensor %d · %s" % (nr, name)), rows, stecker, monitor, achtung,
                 _codeblock(code, "Testprogramm Sensor %d" % nr))

LP08_V3_MATERIAL = (
  sp_ablauf("08")
  + '<p>Heute zieht euer Wächter vom Bildschirm ins echte Leben: Ihr <b>baut</b> ihn ins gedruckte Gehäuse, <b>ersetzt</b> im Code das Ersatzbauteil durch den echten Sensor, '
    '<b>testet</b> ihn live und <b>legt</b> den Schwellenwert fest.</p>'
  + '<h3>Vom Ersatzbauteil zum echten Sensor</h3><p>Ersetzt im C++-Code nur die Zeilen, die den Sensor lesen, durch die Zeilen aus der Anschlusskarte. Vergleich und LEDs bleiben.</p>'
  + _tab(["Projekt", "in Tinkercad", "am echten Arduino"], [
      ["<b>A</b> Gießwächter", "Potentiometer an A0", "<code>analogRead(A0)</code> bleibt. Neu ist der Wertebereich: trocken etwa 0, tief im Wasser bis etwa 650."],
      ["<b>B</b> Filterwächter", "Potentiometer an A1", "Die <b>30 Messungen</b> und die <b>TDS-Formel</b> aus der Anschlusskarte einfügen, dann <code>tds</code> mit dem Schwellenwert vergleichen."],
      ["<b>C</b> Lüftungswächter", "TMP36 an A2, Potentiometer an A3", "<code>#include &lt;DHT.h&gt;</code> und <code>DHT dht(2, DHT11);</code> oben, <code>dht.begin();</code> im Setup, dann <code>dht.readTemperature()</code> und <code>dht.readHumidity()</code>."]])
  + '<h3>So ladet ihr den Code hoch</h3><ol class="task-list" style="list-style:decimal;padding-left:1.4rem">'
    '<li><b>USB-Kabel ab</b>, dann die Kabel nach der Anschlusskarte stecken. Die Farbe im Bild zeigt den Pin, das farbige Schild am Arduino den Namen.</li>'
    '<li>Arduino anstecken und <a href="' + UPLOAD_URL + '" target="_blank" rel="noopener"><b>Arduino hochladen</b></a> öffnen (Chrome oder Edge, ohne Konto).</li>'
    '<li>Code einfügen oder mit <b>„Datei öffnen“</b> laden, dann <b>„⬆ Auf Arduino laden“</b> klicken und den Arduino auswählen.</li>'
    '<li>Im <b>Monitor</b> unten auf der Seite erscheinen die Messwerte.</li></ol>'
  + _anschlusskarte(1, "DHT11: Temperatur und Luftfeuchte", "sensor-1-dht11",
      [("rot", "Bein 1", "5V"), ("blau", "Bein 2", "Pin 2"), ("–", "Bein 3", "frei"), ("schwarz", "Bein 4", "GND"), ("10 kΩ", "Widerstand", "zwischen Bein 1 und Bein 2")],
      "Haltet den Sensor mit dem <b>Gitter zu euch</b>: Die Beinchen zählen von links 1, 2, 3, 4.",
      "<code>Temperatur: 22.00 C, Luftfeuchte: 45.00 %</code>. Haucht den Sensor an: Die Luftfeuchte steigt.",
      "Ohne den 10-kΩ-Widerstand (braun-schwarz-orange) kommt meist „Sensorfehler“. Bein 3 bleibt frei. Der DHT11 misst nur ganze Zahlen und ist auf etwa ±2 °C genau.",
      "sensor-1-dht11.ino")
  + _anschlusskarte(2, "Wasserstandssensor", "sensor-2-wasserstand",
      [("gelb", "S", "A0"), ("rot", "+", "5V"), ("schwarz", "−", "GND")],
      "Die Beschriftung <b>S + −</b> steht auf der roten Platine unter den Pins. Die Kabelfarben dürft ihr frei wählen, wichtig ist, wo sie stecken.",
      "<code>Wasserstand: 412</code>. Trocken steht dort etwa 0, je tiefer der Sensor im Wasser steckt, desto größer die Zahl (bis etwa 600–700).",
      "Nur die Fläche mit den Streifen ins Wasser tauchen, Pins und Bauteile oben bleiben trocken. Den Sensor danach abtrocknen.",
      "sensor-2-wasserstand.ino")
  + _anschlusskarte(3, "CQRobot TDS: Leitfähigkeit von Wasser", "sensor-3-tds",
      [("grün", "Signal", "A1"), ("rot", "+", "5V"), ("schwarz", "−", "GND")],
      "Das Kabel aus der Packung steckt im <b>dreipoligen</b> Stecker der schwarzen Platine (− + A), die Sonde im <b>zweipoligen</b>. Die ersten Werte nach dem Start sind zu hoch, nach etwa 10 s ist die Messung ruhig.",
      "<code>Spannung: 1.47 V, TDS: 565 ppm</code> (Leitungswasser). Eine Prise Salz lässt den Wert steigen. Über etwa 1000 ppm misst der Sensor ungenau.",
      "Nur die Sonde ins Wasser, die Platine bleibt trocken. Sonde danach mit destilliertem Wasser abspülen. Nicht zusammen mit dem Wasserstandssensor im selben Gefäß messen.",
      "sensor-3-tds.ino")
  + '<h3>Wenn es nicht klappt</h3><ul class="task-list">'
    '<li><b>Keine LED leuchtet:</b> Das lange Bein der LED zeigt zum Pin, das kurze über den Widerstand zu GND.</li>'
    '<li><b>Monitor bleibt leer:</b> <code>Serial.begin(9600);</code> im Setup? Richtigen Anschluss gewählt?</li>'
    '<li><b>DHT11 meldet „Sensorfehler“:</b> 10-kΩ-Widerstand zwischen Bein 1 und Bein 2 prüfen.</li>'
    '<li><b>TDS-Werte springen:</b> Die ersten 10 s nach dem Start sind zu hoch, dann ist der Wert ruhig.</li>'
    '<li><b>Gehäuse noch nicht fertig:</b> Erst auf dem Steckbrett testen, dann einbauen.</li></ul>'
  + SP_CSS)

LP08_V3_TASKS = [
  "<b>Aufgabe 1 · Einbauen:</b> Baut den Wächter ins Gehäuse und schließt den Sensor nach der Anschlusskarte an. Hakt ab: Arduino passt, USB erreichbar · LEDs mit 220 Ω an Pin 7 und Pin 8 · Sensor mit USB ab gesteckt · Sensor bzw. Sonde außen, Platine trocken.",
  "<b>Aufgabe 2 · Vom Ersatzbauteil zum echten Sensor:</b> Ersetzt im C++-Code nur die Zeilen, die den Sensor lesen (Tabelle oben).",
  "<b>Aufgabe 3 · Hochladen:</b> Ladet den Code mit „Arduino hochladen“ auf den Arduino und beobachtet die Messwerte im Monitor.",
  "<b>Aufgabe 4 · Testen und Schwellenwert festlegen:</b> Testet mindestens drei Situationen, notiert Messwert, welche LED leuchten soll und welche wirklich leuchtet. Legt den Schwellenwert fest und begründet ihn.",
  "<b>Aufgabe 5 · Ergebnis prüfen und anpassen:</b> Notiert, was noch nicht wie geplant lief, und was ihr geändert habt (Code, Kabel, Gehäuse, Schwellenwert).",
  "<b>Aufgabe 6 · Projektbericht (3–5 Seiten):</b> 1 Problem und Ziel · 2 Aufbau (Bauteilliste, Schaltplan, Foto) · 3 Programm (Struktogramm, wichtige C++-Zeilen erklärt) · 4 Gehäuse · 5 Test (Tabelle, Schwellenwert) · 6 Reflexion · 7 Quellen.",
  "<b>Aufgabe 7 · Übersicht für die Galerie (1 Seite):</b> Name und Team, Problem in einem Satz, Foto, So funktioniert's (Sensor → Arduino → LED), Schwellenwert und Bedeutung von grün und rot, ein Testergebnis.",
]

LP08_V3_QUIZ = [
  dict(q="Was ändert ihr am Tinkercad-Code für den echten Sensor?", done="Richtig, nur das Lesen des Sensors ändert sich.",
       opts=[("alles, der echte Arduino braucht ein ganz neues Programm", False, "Vergleich, LEDs und Wiederholung bleiben genau gleich."),
             ("nur die Zeilen, die den Sensor lesen", True, None),
             ("nur die Pins der LEDs", False, "Die LEDs bleiben an Pin 7 und Pin 8."),
             ("gar nichts", False, "Bei B und C liest der echte Sensor anders als das Ersatzbauteil.")]),
  dict(q="Der DHT11 meldet im Monitor „Sensorfehler“. Was prüft ihr zuerst?", done="Genau, das ist die häufigste Ursache.",
       opts=[("den Schwellenwert", False, "Der Schwellenwert hat mit dem Lesen nichts zu tun."),
             ("die Farbe der LED", False, "Die LED ist nicht beteiligt."),
             ("die Wartezeit", False, "Zwei Sekunden Wartezeit sind richtig."),
             ("den 10-kΩ-Widerstand zwischen Bein 1 und Bein 2", True, None)]),
  dict(q="Der Monitor bleibt leer, obwohl der Upload geklappt hat. Woran kann es liegen?", done="Richtig, ohne Serial.begin schreibt der Arduino nichts.",
       opts=[("Serial.begin(9600); fehlt im Setup", True, None),
             ("die rote LED ist kaputt", False, "Eine kaputte LED hält den Monitor nicht an."),
             ("das Gehäuse ist zu klein", False, "Das Gehäuse beeinflusst den Monitor nicht."),
             ("der Schwellenwert ist zu hoch", False, "Auch dann würden Werte im Monitor erscheinen.")]),
  dict(q="Wie findet ihr einen guten Schwellenwert?", done="Genau, der Schwellenwert stammt aus euren eigenen Messungen.",
       opts=[("Man nimmt immer 500.", False, "Jeder Sensor und jede Situation liefert andere Werte. Messt nach."),
             ("Man misst die Situation „in Ordnung“ und die Situation „handeln“ und legt den Wert dazwischen.", True, None),
             ("Man schaut, welcher Wert gerade im Monitor steht.", False, "Ein einzelner Wert sagt nichts über die Grenze zwischen gut und schlecht."),
             ("Man übernimmt den Wert aus Tinkercad.", False, "In Tinkercad lief ein Potentiometer, der echte Sensor liefert andere Werte.")]),
  dict(q="Warum soll jemand den Wächter nach eurem Projektbericht nachbauen können?", done="Richtig, das ist das Kriterium „Nachvollziehbarkeit“ in Sitzung 09.",
       opts=[("Weil Berichte immer lang sein müssen.", False, "Es geht nicht um Länge, sondern darum, dass alles drinsteht."),
             ("Weil nur so der Drucker funktioniert.", False, "Der Bericht hat mit dem Drucker nichts zu tun."),
             ("Weil Bauteile, Schaltplan, Programm und Tests vollständig und verständlich drinstehen müssen.", True, None),
             ("Weil die Lehrkraft den Wächter sonst nicht einschalten kann.", False, "Einschalten geht über USB, dafür braucht niemand den Bericht.")]),
]

LP08_V3_LOESUNG = [
  "Aufgabe 2: A behält <code>analogRead(A0)</code>, B mittelt 30 Messungen und rechnet mit der TDS-Formel in ppm, C liest mit <code>dht.readTemperature()</code> und <code>dht.readHumidity()</code>.",
  "Aufgabe 4: Der Schwellenwert liegt zwischen den gemessenen Werten für „in Ordnung“ und „handeln“, z. B. A: trocken ≈ 0, halb voll ≈ 400 → Schwelle 200; B: Leitungswasser ≈ 565 ppm, frisch gefiltert ≈ 100 ppm → Schwelle 400 ppm; C: 25 °C und 60 %.",
  _codeblock("projekt-a-pflanze.ino", "Musterlösung A · Gießwächter (echter Sensor)"),
  _codeblock("projekt-b-wasserfilter.ino", "Musterlösung B · Filterwächter (echter Sensor)"),
  _codeblock("projekt-c-heizkeller.ino", "Musterlösung C · Lüftungswächter (echter Sensor)"),
]

LP08_V3_VERTIEFUNG = (
  "<p>Euer Wächter läuft zuverlässig? Dann macht ihn alltagstauglicher.</p>"
  "<h3>🔔 Alarm</h3><p>Schließt einen <b>Piezo-Summer</b> an und lasst ihn bei Rot alle zehn Sekunden kurz piepen (<code>tone()</code>, <code>noTone()</code>).</p>"
  "<h3>🟡 Vorwarnung</h3><p>Eine gelbe LED zeigt an, dass sich der Wert dem Schwellenwert nähert. Belegt im Bericht, ab welchem Wert sie leuchtet.</p>"
  "<style>.vertiefung h3{font-size:1rem;margin:1.1rem 0 .4rem;color:var(--key)}</style>")

# ---------------------------------------------------------------- LP09 · Galerie
LP09_V3_MATERIAL = (
  sp_ablauf("09")
  + '<p>Heute <b>präsentiert</b> ihr euren Wächter, <b>bewertet</b> andere Projekte anhand von zwei Kriterien und <b>gebt</b> eine wertschätzende, konkrete Rückmeldung.</p>'
  + '<h3>Ablauf des Gallery Walks</h3>'
  + _tab(["Phase", "Was passiert?"], [
      ["<b>Aufbauen</b>", "Wächter (läuft am USB-Strom), ausgedruckte Übersicht und Projektbericht auf euren Tisch legen."],
      ["<b>Runde 1</b>", "<b>Person 1</b> bleibt als Expert:in am Projekt und erklärt. <b>Person 2</b> besucht zwei andere Projekte und bewertet sie."],
      ["<b>Runde 2</b>", "Tauschen: Jetzt erklärt Person 2, Person 1 besucht zwei <b>andere</b> Projekte."],
      ["<b>Rückmelden</b>", "Im Team die Bewertungen besprechen. Jede:r schreibt für die zwei besuchten Projekte je eine Rückmeldekarte und gibt sie ab."],
      ["<b>Abschluss</b>", "Eure eigenen Karten lesen: Was nehmt ihr für die nächste Version mit?"]])
  + '<h3>Bewertungsmatrix</h3><p>Testet den Wächter selbst (z. B. Sensor ins Wasser, anhauchen) und lest in Bericht und Übersicht. Kreuzt je Aussage eine Stufe an: '
    '<b>++</b> voll erfüllt · <b>+</b> überwiegend · <b>o</b> teilweise · <b>–</b> noch nicht erfüllt.</p>'
  + _tab(["Kriterium", "Aussage"], [
      ["<b>1 · Funktion des Wächters</b><br>Sensor, Steuerung, Anzeige und Gehäuse arbeiten zusammen",
       "Der Sensor liefert glaubwürdige Messwerte.<br>Die LEDs wechseln am Schwellenwert zuverlässig zwischen grün und rot.<br>"
       "Das Gehäuse schützt die Technik, Anzeige und Sensor sind gut zugänglich.<br>Der Wächter löst das Alltagsproblem, der Schwellenwert ist begründet."],
      ["<b>2 · Nachvollziehbarkeit und Übersichtlichkeit des Projektberichts</b>",
       "Problem, Ziel und die Bedeutung von grün und rot sind klar.<br>Bauteile und Schaltplan reichen zum Nachbauen.<br>"
       "Das Programm ist mit Struktogramm und Code verständlich erklärt.<br>Tests und Reflexion sind mit Messwerten belegt.<br>Die Übersicht ist auf einen Blick verständlich."]])
  + '<h3>Rückmeldekarte</h3><p>Rückmeldung an Team … von …</p><ul class="task-list">'
    '<li><b>Das ist euch besonders gelungen:</b> …</li><li><b>Mein Tipp für die nächste Version:</b> …</li><li><b>Meine Frage an euch:</b> …</li></ul>'
    '<div class="sp-hinweis"><b>Satzanfänge:</b> „Besonders überzeugt hat uns …, weil …“ · „Ihr könntet noch …, dann …“ · „Uns ist aufgefallen, dass …“ · „Wie habt ihr … gelöst?“</div>'
  + SP_CSS)

LP09_V3_TASKS = [
  "<b>Aufgabe 1 · Gallery Walk:</b> Baut euren Wächter mit Übersicht und Bericht auf. In Runde 1 erklärt Person 1, Person 2 besucht zwei Projekte, in Runde 2 wird getauscht.",
  "<b>Aufgabe 2 · Bewerten:</b> Testet die besuchten Wächter selbst, lest Bericht und Übersicht und kreuzt in der Bewertungsmatrix je Aussage eine Stufe an.",
  "<b>Aufgabe 3 · Rückmeldekarten schreiben:</b> Schreibt für jedes besuchte Projekt eine Karte: Was ist gelungen, welcher umsetzbare Tipp, welche Frage. Gebt sie dem Team.",
  "<b>Aufgabe 4 · Unser Fazit:</b> Lest eure eigenen Karten. Was ändert ihr in einer nächsten Version eures Wächters zuerst?",
]

LP09_V3_QUIZ = [
  dict(q="Welche Rückmeldung hilft einem Team am meisten weiter?", done="Richtig: konkret, begründet und umsetzbar.",
       opts=[("„War gut.“", False, "Das freut, aber das Team weiß nicht, was genau gut war."),
             ("„Euer Gehäuse ist hässlich.“", False, "Das ist weder wertschätzend noch hilfreich. Was genau könnte besser werden?"),
             ("„Ihr könntet die rote LED näher an den Rand setzen, dann sieht man sie auch von der Tür aus.“", True, None),
             ("„Keine Ahnung, wie das funktioniert.“", False, "Stellt lieber eine konkrete Frage an das Team.")]),
  dict(q="Was bewertet ihr im Kriterium „Funktion des Wächters“?", done="Genau, Sensor, Steuerung, Anzeige und Gehäuse im Zusammenspiel.",
       opts=[("wie schön die Übersicht gestaltet ist", False, "Das gehört zu Kriterium 2, dem Bericht."),
             ("ob Sensor, Steuerung, Anzeige und Gehäuse zusammenarbeiten und der Schwellenwert begründet ist", True, None),
             ("wie lange das Team gearbeitet hat", False, "Bewertet wird das Ergebnis, nicht die Zeit."),
             ("welches Projekt (A, B oder C) gewählt wurde", False, "Alle drei Projekte sind gleich viel wert.")]),
  dict(q="Wie prüft ihr, ob die Anzeige zuverlässig umschaltet?", done="Richtig, selbst ausprobieren ist der beste Test.",
       opts=[("Man fragt das Team, ob es klappt.", False, "Glauben ist gut, testen ist besser."),
             ("Man liest nur den Code.", False, "Der Code zeigt die Idee, aber nicht, ob der echte Sensor mitspielt."),
             ("Man schaut, ob das Gehäuse zu ist.", False, "Ein geschlossenes Gehäuse sagt nichts über die Anzeige."),
             ("Man verändert die Messgröße selbst (Wasser, Salz, Anhauchen) und beobachtet, ob die LED am Schwellenwert wechselt.", True, None)]),
  dict(q="Was macht ihr mit den Rückmeldekarten, die ihr bekommt?", done="Genau, daraus entsteht euer Fazit für die nächste Version.",
       opts=[("Lesen, im Team besprechen und auswählen, was ihr zuerst verbessert.", True, None),
             ("Wegwerfen, das Projekt ist ja fertig.", False, "Die Karten zeigen euch, was andere sehen. Das ist wertvoll für eine nächste Version."),
             ("Nur die positiven Karten lesen.", False, "Gerade die Tipps helfen beim Verbessern."),
             ("Dem anderen Team widersprechen.", False, "Nachfragen ist erlaubt, aber erst einmal zuhören und überlegen.")]),
]

LP09_V3_LOESUNG = [
  "Gute Rückmeldungen sind <b>konkret</b> (was genau?), <b>begründet</b> (warum?) und <b>umsetzbar</b> (was könnte das Team tun?).",
  "Beispiel gelungen: „Besonders überzeugt hat uns, dass eure LED schon bei einer Prise Salz auf Rot springt, weil ihr den Schwellenwert mit Leitungs- und Filterwasser gemessen habt.“",
  "Beispiel Tipp: „Ihr könntet im Bericht ein Foto vom offenen Gehäuse zeigen, dann sieht man, wie die Kabel verlegt sind.“",
  "Beispiel Frage: „Wie habt ihr verhindert, dass der DHT11 die warme Luft vom Arduino misst?“",
]

# ---------------------------------------------------------------- Kursinhalt
# Jedes LP: no, sjw, title, goal, tasks[], tools[keys], fast, rlp[], solution[], kind
# optional: vorwissen[], quiz[], material (HTML, Informationstext), task_figs[] / solution_figs[]
#           (dict(fig=..., cap=...); fig = SVG-Name ohne Endung oder Foto .jpg/.png aus <Lektion>/typst/)
# ---------------------------------------------------------------- Archiv: LP10 Mini-Projekt Arduino
# Seit 2026-10-16 nicht mehr im Kurs, die Sensor-Projekte LP07–09 schließen die Arduino-Reihe ab.
# Seite: extras/lp10/archiv/lp10.html, Material: iCloud 02 Blockbasiert II …/Archiv/10 Mini-Projekt …
LP10_ARCHIV = dict(no=10, sjw=11, kind="projekt", title="Mini-Projekt Arduino + Ergebnissicherung",
     goal="Du planst und baust eine eigene kleine Schaltung (Lichtorgel, Würfel, Reaktionsspiel), dokumentierst sie und sicherst Code + Schaltplan als Backup.",
     tasks=["Projektidee wählen, Bauteile & Ablauf planen.",
            "Schaltung in Tinkercad aufbauen und Sketch schreiben & testen.",
            "Ergebnis sichern: Sketch (.ino), Screenshot des Schaltplans, kurze Doku — lokal + Cloud."],
     tools=["tinker", "arduino"],
     fast="Baue eine Zusatzfunktion ein (z. B. Helligkeitssteuerung per Poti) und beschreibe sie in der Doku.",
     rlp=["RLP 2.4 · Umsetzen", "2.6 Kommunizieren", "3.3 Projekt"],
     vorwissen=[
       dict(fig="fig1", cap="Bild 1 · Projektablauf", quiz=[
         dict(q="Was ist Schritt 1 im Projektablauf?",
              done="Richtig — die Projektidee wählen.",
              opts=[
                ("Projektidee wählen", True, None),
                ("Bauteile und Ablauf planen", False, "Das Planen folgt erst, nachdem eine Idee feststeht."),
                ("Aufbauen und Testen", False, "Aufgebaut wird erst nach Idee und Planung."),
                ("Ergebnis sichern", False, "Das Sichern steht ganz am Ende des Ablaufs."),
              ]),
         dict(q="Was ist Schritt 3 im Projektablauf?",
              done="Genau — Aufbauen und Testen in Tinkercad.",
              opts=[
                ("Aufbauen und Testen in Tinkercad", True, None),
                ("Projektidee wählen", False, "Die Idee steht ganz am Anfang, Schritt 1."),
                ("Bauteile und Ablauf planen", False, "Das Planen ist Schritt 2, vor dem Aufbauen."),
                ("Ergebnis sichern", False, "Das Sichern folgt erst nach dem Testen, als Schritt 4."),
              ]),
         dict(q="Warum führt vom Testen ein gestrichelter Pfeil zurück zum Planen?",
              done="Richtig — Anpassen ist erlaubt.",
              opts=[
                ("Weil man die Planung nach dem Testen bei Bedarf anpassen darf.", True, None),
                ("Weil das Testen komplett übersprungen werden soll.", False, "Getestet werden soll gerade gründlich, nicht übersprungen."),
                ("Weil ein Fehler das ganze Projekt ungültig macht.", False, "Ein Fehler beim Testen führt nur zu einer Anpassung, nicht zum Abbruch."),
                ("Das ist nur Dekoration ohne Bedeutung.", False, "Der Pfeil zeigt den iterativen Charakter eines echten Projekts."),
              ]),
         dict(q="Was passiert im letzten Schritt, dem Sichern?",
              done="Stimmt — Sketch, Schaltplan und Doku an zwei Orten.",
              opts=[
                ("Sketch, Schaltplan-Screenshot und Doku werden an zwei Orten gespeichert.", True, None),
                ("Das Projekt wird sofort gelöscht.", False, "Sichern bedeutet Aufbewahren, nicht Löschen."),
                ("Nur der Sketch wird auf dem Arduino belassen.", False, "Ohne separate Sicherung geht die Arbeit bei einem Defekt verloren."),
                ("Es passiert nichts Wichtiges mehr.", False, "Die Ergebnissicherung ist ein zentraler, bewerteter Schritt."),
              ]),
       ]),
       dict(fig="fig2", cap="Bild 2 · Bewertungskriterien", quiz=[
         dict(q="Was bedeutet Kriterium 1, Funktion?",
              done="Richtig — die Schaltung funktioniert wie geplant.",
              opts=[
                ("Die Schaltung funktioniert wie geplant.", True, None),
                ("Der Code ist besonders kurz.", False, "Die Länge des Codes ist kein Bewertungskriterium."),
                ("Es wurden viele Bauteile verwendet.", False, "Die Anzahl der Bauteile sagt nichts über die Funktion aus."),
                ("Das Projekt wurde schnell fertig.", False, "Geschwindigkeit ist kein Bewertungskriterium, Funktion schon."),
              ]),
         dict(q="Was bedeutet Kriterium 2, Verdrahtung?",
              done="Genau — sauber und sicher aufgebaut.",
              opts=[
                ("Die Schaltung ist sauber und sicher aufgebaut.", True, None),
                ("Der Code ist kommentiert.", False, "Das gehört zum Kriterium Code, nicht zur Verdrahtung."),
                ("Es gibt eine Dokumentation.", False, "Das ist ein eigenes Kriterium, nicht die Verdrahtung."),
                ("Das Backup liegt an zwei Orten.", False, "Das betrifft die Dokumentation/Ergebnissicherung, nicht die Verdrahtung."),
              ]),
         dict(q="Was bedeutet Kriterium 3, Code?",
              done="Stimmt — kommentiert und lesbar.",
              opts=[
                ("Der Code ist kommentiert und lesbar.", True, None),
                ("Die Schaltung funktioniert wie geplant.", False, "Das ist das Kriterium Funktion, nicht Code."),
                ("Die Verdrahtung ist sauber.", False, "Das ist ein eigenes Kriterium, nicht der Code."),
                ("Es gibt ein Backup.", False, "Das gehört zur Dokumentation, nicht zum Code selbst."),
              ]),
       ]),
     ],
     quiz=[
       dict(q="Was gehört zu einer guten Projektplanung vor dem Bauen?",
            done="Richtig — Idee, Bauteile und Ablauf zuerst planen.",
            opts=[
              ("Projektidee wählen sowie Bauteile und Ablauf planen", True, None),
              ("direkt ohne Plan drauflos bauen", False, "Ohne Plan führt der Aufbau meist zu unnötigen Umbauten und Fehlern."),
              ("nur den Sketch schreiben, ohne Schaltung zu planen", False, "Sketch und Schaltung müssen zusammenpassen — beides gehört zur Planung."),
              ("die Dokumentation erst nach der Abgabe beginnen", False, "Dann fehlen oft wichtige Details — Dokumentation sollte parallel entstehen."),
            ]),
       dict(q="Was bedeutet „Ergebnissicherung“ bei diesem Projekt?",
            done="Genau — Sketch, Schaltplan und Doku an zwei Orten sichern.",
            opts=[
              ("Sketch (.ino), Schaltplan-Screenshot und Doku sichern — lokal und in der Cloud", True, None),
              ("nur den Sketch auf dem Arduino lassen", False, "Ohne separate Sicherung geht die Arbeit bei einem Defekt verloren."),
              ("nichts, das Projekt bleibt nur im Kopf", False, "Ohne dokumentierte Sicherung ist das Projekt nicht nachvollziehbar oder abgebbar."),
              ("nur ein Foto des fertigen Aufbaus", False, "Ein Foto allein sichert weder den Code noch den Schaltplan im Detail."),
            ]),
       dict(q="Wonach wird das Mini-Projekt vor allem bewertet?",
            done="Stimmt — Funktion, Verdrahtung, Code, Doku.",
            opts=[
              ("Funktion, saubere Verdrahtung, kommentierter Code und Doku", True, None),
              ("nur die Originalität der Idee", False, "Originalität allein reicht nicht — die Umsetzung zählt ebenso."),
              ("nur die Geschwindigkeit der Fertigstellung", False, "Schnelligkeit ist kein Bewertungskriterium, Qualität schon."),
              ("nur die Anzahl der verwendeten Bauteile", False, "Mehr Bauteile bedeuten nicht automatisch ein besseres Projekt."),
            ]),
       dict(q="Warum ist ein kommentierter Code Teil der Bewertung?",
            done="Richtig — Kommentare machen den Code nachvollziehbar.",
            opts=[
              ("Er macht nachvollziehbar, was der Code tut, und erleichtert Verständnis und Korrektur.", True, None),
              ("Kommentare beschleunigen das Programm.", False, "Kommentare haben keinen Einfluss auf die Ausführungsgeschwindigkeit."),
              ("Kommentare sind für den Arduino zwingend nötig, sonst läuft der Sketch nicht.", False, "Ein Sketch läuft auch ganz ohne Kommentare — sie dienen nur dem Verständnis."),
              ("Kommentare ersetzen die Doku vollständig.", False, "Kommentare ergänzen die Doku, ersetzen sie aber nicht vollständig."),
            ]),
     ],
     solution=["Bewertet werden Funktion, saubere Verdrahtung, kommentierter Code und die Doku.",
               "Ergebnissicherung = reproduzierbar abgeben: .ino + Schaltplan + Beschreibung.",
               "Backup an zwei Orten (Rechner + Cloud/USB)."])

UNITS = [
 # =================== HALBJAHR 1 ===================
 dict(hj=1, num="00", title="Systemstart — Was ist Informatik?",
      key="#35e0ff", key2="#0bb7e0", tint="rgba(53,224,255,0.09)",
      lps=[
        dict(no=0, sjw=0, kind="lernpfad", title="Boot-Sequenz: Kurslandkarte & digitale Werkzeugkiste",
             goal="Du verschaffst dir einen Überblick über das Kursjahr, richtest Konto & Ordnerstruktur ein und lernst die Regeln zur Ergebnissicherung (Backups) kennen.",
             tasks=["Diese Kursseite als Landkarte erkunden: Halbjahre, Einheiten, Lernpfade, Sterne, Schlösser.",
                    "Persönliche Ordnerstruktur anlegen: <code>Informatik/HJ1</code>, <code>HJ2</code>, <code>_backups</code>.",
                    "Backup-Regel notieren: „Am Stundenende alles sichern — lokal UND in der Cloud/USB.“"],
             tools=[],
             fast="Ausblick auf euer erstes Makey-Makey-Projekt (LP04): Recherchiere im Internet drei kreative Makey-Makey-Projekte und halte Titel, Link und eine Kurznotiz (Was macht das Projekt besonders?) zu jedem Projekt in einer Datei in deiner heutigen Ordnerstruktur fest.",
             rlp=["RLP 2.3 · Bedienung", "3.2 Informatiksysteme"],
             vorwissen=[
               dict(fig="fig1", cap="Bild 1 · Was ist Informatik?", quiz=[
                 dict(q="Was gehört zu Teil 1, der Hardware?",
                      done="Richtig — das sind physische Bauteile.",
                      opts=[
                        ("physische Bauteile eines Computers (z. B. Prozessor, Bildschirm, Tastatur)", True, None),
                        ("Programme und Apps, die auf dem Computer laufen", False, "Das ist Software, nicht Hardware."),
                        ("Zahlen und Zeichen, die verarbeitet werden", False, "Das sind Daten, kein Bauteil."),
                        ("Schrittfolgen zur Lösung eines Problems", False, "Das beschreibt einen Algorithmus, kein Bauteil."),
                      ]),
                 dict(q="Was gehört zu Teil 2, der Software?",
                      done="Genau — das sind Programme und Apps.",
                      opts=[
                        ("Programme und Apps, die auf der Hardware laufen", True, None),
                        ("die physischen Bauteile eines Computers", False, "Das ist Hardware, nicht Software."),
                        ("nur das Internet allgemein", False, "Software ist viel mehr als nur das Internet."),
                        ("nur Daten ohne jede Verarbeitung", False, "Das beschreibt Daten, nicht Software."),
                      ]),
                 dict(q="Was verbindet Teil 3, Daten und Algorithmen?",
                      done="Stimmt — Algorithmen verarbeiten Daten.",
                      opts=[
                        ("Algorithmen verarbeiten Daten nach klaren, festgelegten Schritten", True, None),
                        ("Daten und Algorithmen haben nichts miteinander zu tun", False, "Algorithmen arbeiten gerade mit Daten — sie hängen eng zusammen."),
                        ("Algorithmen sind nur ein anderes Wort für Hardware", False, "Algorithmen sind Schrittfolgen, keine Bauteile."),
                        ("Daten sind nur Fotos und Videos", False, "Daten umfassen viel mehr, z. B. auch Text und Zahlen."),
                      ]),
                 dict(q="Was ist Informatik als Wissenschaft?",
                      done="Richtig — genau das ist Informatik.",
                      opts=[
                        ("die Wissenschaft von der systematischen Darstellung, Speicherung und Verarbeitung von Informationen mit Computern", True, None),
                        ("nur das Reparieren von Computern", False, "Das wäre reine Hardware-Wartung, nicht die Wissenschaft dahinter."),
                        ("nur das Programmieren von Spielen", False, "Programmieren ist nur ein Teilbereich der Informatik."),
                        ("ein Teilgebiet der Mathematik ohne eigene Methoden", False, "Informatik hat eigene Methoden und ist ein eigenständiges Fach."),
                      ]),
               ]),
               dict(fig="fig2", cap="Bild 2 · Kursorganisation", quiz=[
                 dict(q="Wie heißt Teil 1, die Ordnerstruktur für diesen Kurs?",
                      done="Richtig — genau diese drei Ordner.",
                      opts=[
                        ("Informatik mit den Unterordnern HJ1, HJ2 und _backups", True, None),
                        ("nur ein einziger Ordner ohne Unterordner", False, "Ohne Unterordner verlierst du schnell den Überblick."),
                        ("ein Ordner pro Mitschüler:in", False, "Die Struktur ist nach Halbjahren geordnet, nicht nach Personen."),
                        ("keine feste Struktur, Dateien bleiben verstreut", False, "Genau das soll die feste Ordnerstruktur verhindern."),
                      ]),
                 dict(q="Wie lautet die Backup-Regel zu Teil 2?",
                      done="Genau — zwei Orte, jede Stunde.",
                      opts=[
                        ("am Stundenende alles an zwei Orten sichern — Rechner UND Cloud/USB", True, None),
                        ("nur am Ende des Halbjahres sichern", False, "Das wäre viel zu selten — nach jeder Stunde sichern."),
                        ("nur lokal auf dem Rechner sichern", False, "Ohne zweiten Ort ist die Sicherung bei einem Defekt weg."),
                        ("Backups sind nicht nötig", False, "Ergebnissicherung ist fester Bestandteil jeder Stunde."),
                      ]),
                 dict(q="Was passiert bei Teil 3, wenn das Freischalt-Datum erreicht ist?",
                      done="Stimmt — automatische Freischaltung.",
                      opts=[
                        ("die Musterlösung wird automatisch sichtbar", True, None),
                        ("der Lernpfad wird gelöscht", False, "Der Lernpfad bleibt erhalten, nur die Lösung wird sichtbar."),
                        ("die Aufgabe wird automatisch als erledigt markiert", False, "Das Datum steuert nur die Lösungssichtbarkeit, nicht den Bearbeitungsstatus."),
                        ("nichts, man muss die Lehrkraft fragen", False, "Die Freischaltung passiert automatisch, ganz ohne Nachfrage."),
                      ]),
                 dict(q="Warum sind zwei Speicherorte für Backups sinnvoll?",
                      done="Richtig — Sicherheit durch eine zweite Kopie.",
                      opts=[
                        ("falls einer der beiden Orte ausfällt oder verloren geht, bleibt die andere Kopie erhalten", True, None),
                        ("zwei Kopien sehen ordentlicher aus", False, "Es geht um Sicherheit, nicht um Optik."),
                        ("das ist nicht sinnvoll, ein Ort reicht aus", False, "Ein einzelner Ort ist ein Risiko, falls er ausfällt."),
                        ("die Cloud braucht immer eine Bestätigung vom zweiten Ort", False, "Die beiden Orte sind unabhängige Kopien, keine gegenseitige Bestätigung."),
                      ]),
               ]),
             ],
             quiz=[
               dict(q="Wie lautet die Backup-Regel für diesen Kurs?",
                    done="Richtig — zwei Orte, jede Stunde.",
                    opts=[
                      ("Am Stundenende alles sichern — lokal UND in der Cloud/USB.", True, None),
                      ("Nur am Ende des Halbjahres sichern.", False, "Das wäre zu selten — Ergebnisse sollen nach jeder Stunde gesichert sein."),
                      ("Nur lokal auf dem Rechner sichern.", False, "Ohne eine zweite Kopie in der Cloud/USB ist ein Rechnerausfall riskant."),
                      ("Backups sind bei diesem Kurs nicht nötig.", False, "Ergebnissicherung ist ausdrücklich Teil jeder Stunde — Backups sind nötig."),
                    ]),
               dict(q="Wie viele Lernpfade umfasst der gesamte Kurs?",
                    done="Richtig — 37 Lernpfade über beide Halbjahre.",
                    opts=[
                      ("37", True, None),
                      ("12", False, "Das wären nur gut zwei Monate — der Kurs läuft über das ganze Schuljahr."),
                      ("20", False, "Es sind mehr — der Kurs deckt beide Halbjahre komplett ab."),
                      ("52", False, "So viele Schulwochen hat kein Schuljahr — Ferien und Feiertage fehlen dann."),
                    ]),
               dict(q="Wann wird die Musterlösung eines Lernpfads freigeschaltet?",
                    done="Genau — automatisch zu einem festen Datum.",
                    opts=[
                      ("Automatisch zu einem festgelegten Datum.", True, None),
                      ("Sofort beim ersten Öffnen der Seite.", False, "Die Seite prüft ein festgelegtes Datum, nicht den ersten Seitenaufruf."),
                      ("Nie, sie bleibt dauerhaft verborgen.", False, "Jede Lösung schaltet sich irgendwann frei — sie bleibt nicht für immer verborgen."),
                      ("Nur auf Anfrage per E-Mail.", False, "Es ist keine Anfrage nötig — die Seite schaltet automatisch frei."),
                    ]),
               dict(q="Wozu dienen die Sterne auf der Kursseite?",
                    done="Stimmt — reine Selbsteinschätzung, lokal gespeichert.",
                    opts=[
                      ("Für die eigene Selbsteinschätzung, wie sicher du dich fühlst.", True, None),
                      ("Für die Bewertung durch die Lehrkraft.", False, "Die Sterne werden nur lokal bei dir gespeichert, nicht an die Lehrkraft übertragen."),
                      ("Als Deko ohne Funktion.", False, "Sie speichern tatsächlich deinen Stand — keine reine Dekoration."),
                      ("Um Lernpfade freizuschalten.", False, "Das Freischalten der Lösung hängt vom Datum ab, nicht von den Sternen."),
                    ]),
             ],
             solution=["Ordnerstruktur steht, Backup-Regel im Heft.",
                       "Kurslandkarte verstanden: 4 Reihen a–d, 37 Lernpfade, Lösungen schalten sich datumsweise frei."]),
        dict(no=1, sjw=1, kind="lernpfad", title="EVA & Algorithmus — wie ein Computer „denkt“",
             goal="Du erklärst das EVA-Prinzip (Eingabe → Verarbeitung → Ausgabe) und beschreibst einen Alltagsablauf als Algorithmus (Schritt für Schritt, mit Verzweigung und Schleife).",
             tasks=["Zehn Alltagsgeräte dem EVA-Prinzip zuordnen (Ampel, Taschenrechner, Waschmaschine …).",
                    "Ein Rezept oder Weg als Algorithmus in nummerierten Schritten aufschreiben.",
                    "Eine Verzweigung („wenn … dann … sonst …“) und eine Schleife („wiederhole …“) markieren."],
             tools=[],
             fast="Formuliere den Algorithmus „Zähne putzen“ so präzise, dass ein Roboter ihn ausführen könnte — inklusive Abbruchbedingung.",
             rlp=["RLP 2.1 · Modellieren", "3.2 EVA-Prinzip", "2.2 Algorithmen"],
             vorwissen=[
               dict(fig="fig1", cap="Bild 1 · Die EVA-Kette", quiz=[
                 dict(q="Wofür steht das E in EVA (Teil 1)?",
                      done="Richtig — Eingabe.",
                      opts=[
                        ("Eingabe", True, None),
                        ("Ergebnis", False, "Das Ergebnis kommt am Ende bei der Ausgabe heraus."),
                        ("Ende", False, "EVA beschreibt einen Ablauf, kein Ende."),
                        ("Elektronik", False, "EVA steht für die drei Verarbeitungsschritte, nicht für Bauteile."),
                      ]),
                 dict(q="Bei Teil 3 kommt das Ergebnis heraus. Wie heißt dieser Schritt?",
                      done="Genau — Ausgabe.",
                      opts=[
                        ("Ausgabe", True, None),
                        ("Verarbeitung", False, "Verarbeitung ist der mittlere Schritt, nicht das Herauskommen des Ergebnisses."),
                        ("Eingabe", False, "Eingabe ist der erste Schritt, nicht der letzte."),
                        ("Anmeldung", False, "Anmeldung gehört nicht zur EVA-Kette."),
                      ]),
                 dict(q="Was passiert bei Teil 2 (Verarbeitung)?",
                      done="Stimmt — der Denk-Chip rechnet.",
                      opts=[
                        ("Der Denk-Chip rechnet und verarbeitet die Daten.", True, None),
                        ("Der Bildschirm zeigt ein Bild.", False, "Das ist Ausgabe, nicht Verarbeitung."),
                        ("Man tippt auf der Tastatur.", False, "Das ist Eingabe, nicht Verarbeitung."),
                        ("Der Computer schaltet sich aus.", False, "Das hat mit Verarbeitung nichts zu tun."),
                      ]),
                 dict(q="Wozu dient Teil 4, der Speicher?",
                      done="Richtig — er bewahrt Daten dauerhaft auf.",
                      opts=[
                        ("Er merkt sich Daten und bewahrt sie dauerhaft auf.", True, None),
                        ("Er zeigt Bilder an.", False, "Das ist die Aufgabe der Ausgabe, nicht des Speichers."),
                        ("Er macht Geräusche.", False, "Das wäre ein Ausgabegerät wie ein Lautsprecher."),
                        ("Man tippt darauf.", False, "Das beschreibt die Tastatur, nicht den Speicher."),
                      ]),
               ]),
               dict(fig="fig2", cap="Bild 2 · Geräte am Arbeitsplatz", quiz=[
                 dict(q="Gerät 1 ist der Bildschirm. Zu welchem EVA-Schritt gehört er?",
                      done="Richtig — Ausgabe.",
                      opts=[
                        ("Ausgabe — er zeigt etwas an.", True, None),
                        ("Eingabe — er filmt die Benutzenden.", False, "Ein normaler Bildschirm nimmt nichts auf, er zeigt nur an."),
                        ("Verarbeitung — er rechnet mit den Daten.", False, "Gerechnet wird im Prozessor, nicht im Bildschirm."),
                        ("Speicher — er speichert die eingegebenen Daten.", False, "Der Bildschirm speichert nichts dauerhaft."),
                      ]),
                 dict(q="Womit gibst du Buchstaben ein (Teil 2)?",
                      done="Genau — mit der Tastatur.",
                      opts=[
                        ("Tastatur", True, None),
                        ("Maus", False, "Die Maus steuert den Zeiger, sie tippt keine Buchstaben."),
                        ("Drucker", False, "Der Drucker ist ein Ausgabegerät."),
                        ("Lautsprecher", False, "Der Lautsprecher gibt nur Ton aus."),
                      ]),
                 dict(q="Welche zwei Geräte sind Ausgabegeräte?",
                      done="Stimmt — Bildschirm und Drucker.",
                      opts=[
                        ("Bildschirm und Drucker", True, None),
                        ("Tastatur und Maus", False, "Das sind beides Eingabegeräte."),
                        ("Maus und Drucker", False, "Die Maus ist ein Eingabegerät, der Drucker ein Ausgabegerät."),
                        ("Bildschirm und Tastatur", False, "Die Tastatur ist ein Eingabegerät, kein Ausgabegerät."),
                      ]),
                 dict(q="Was ist die Maus (Teil 3)?",
                      done="Richtig — ein Eingabegerät.",
                      opts=[
                        ("ein Eingabegerät", True, None),
                        ("ein Ausgabegerät", False, "Ausgabegeräte zeigen oder erzeugen etwas, die Maus steuert nur."),
                        ("der Denk-Chip", False, "Der Denk-Chip ist der Prozessor im Inneren, nicht die Maus."),
                        ("ein Speicher", False, "Die Maus speichert keine Daten dauerhaft."),
                      ]),
               ]),
               dict(fig="fig3", cap="Bild 3 · Blick ins Innere", quiz=[
                 dict(q='Teil 1 trägt die Aufschrift "CPU". Das ist ...',
                      done="Richtig — der Denk-Chip.",
                      opts=[
                        ("der Denk-Chip / Prozessor", True, None),
                        ("der Bildschirm", False, "Der Bildschirm sitzt außerhalb des Gehäuses und zeigt nur an."),
                        ("die Tastatur", False, "Die Tastatur ist ein externes Eingabegerät."),
                        ("der Lautsprecher", False, "Der Lautsprecher gibt nur Ton aus, er rechnet nicht."),
                      ]),
                 dict(q="Teil 3 ist die Festplatte. Wozu ist sie da?",
                      done="Genau — sie speichert Daten dauerhaft.",
                      opts=[
                        ("sie speichert Daten dauerhaft", True, None),
                        ("sie rechnet Aufgaben aus", False, "Das Rechnen übernimmt die CPU, nicht die Festplatte."),
                        ("sie zeigt Bilder an", False, "Bilder zeigt der Bildschirm, nicht die Festplatte."),
                        ("man tippt darauf", False, "Getippt wird auf der Tastatur, nicht auf der Festplatte."),
                      ]),
                 dict(q="Welches Bauteil erledigt den Schritt Verarbeitung?",
                      done="Stimmt — der Prozessor.",
                      opts=[
                        ("der Prozessor / Denk-Chip (CPU)", True, None),
                        ("der Arbeitsspeicher (RAM)", False, "RAM hält Daten kurzfristig bereit, gerechnet wird in der CPU."),
                        ("die Festplatte (HD)", False, "Die Festplatte speichert dauerhaft, sie rechnet nicht."),
                        ("das Gehäuse", False, "Das Gehäuse ist nur die Hülle, kein Rechenbauteil."),
                      ]),
                 dict(q="Wo stecken all diese Teile meistens?",
                      done="Richtig — im Gehäuse.",
                      opts=[
                        ("im Gehäuse", True, None),
                        ("im Bildschirm", False, "Der Bildschirm ist meist ein eigenes, externes Gerät."),
                        ("in der Tastatur", False, "Die Tastatur enthält nur ihre eigene Elektronik."),
                        ("in der Maus", False, "Die Maus enthält keine CPU oder Festplatte."),
                      ]),
               ]),
               dict(fig="fig4", cap="Bild 4 · Algorithmus-Bausteine", quiz=[
                 dict(q="Was ist Teil 1, die Sequenz?",
                      done="Richtig — feste Reihenfolge.",
                      opts=[
                        ("Schritte, die in fester Reihenfolge ausgeführt werden", True, None),
                        ("eine Entscheidung mit Bedingung", False, "Das beschreibt die Verzweigung, nicht die Sequenz."),
                        ("eine Wiederholung", False, "Das beschreibt die Schleife, nicht die Sequenz."),
                        ("ein Eingabegerät", False, "Das gehört zum EVA-Prinzip, nicht zu Algorithmus-Bausteinen."),
                      ]),
                 dict(q="Was macht Teil 2, die Verzweigung?",
                      done="Genau — sie entscheidet abhängig von einer Bedingung.",
                      opts=[
                        ("sie trifft abhängig von einer Bedingung eine Entscheidung (wenn ... dann ... sonst)", True, None),
                        ("sie wiederholt einen Schritt immer wieder", False, "Das ist die Aufgabe der Schleife, nicht der Verzweigung."),
                        ("sie beendet den Algorithmus sofort", False, "Eine Verzweigung entscheidet, sie beendet nicht automatisch alles."),
                        ("sie speichert Daten", False, "Speichern ist keine Aufgabe der Verzweigung."),
                      ]),
                 dict(q="Was macht Teil 3, die Schleife?",
                      done="Stimmt — sie wiederholt, bis eine Bedingung erfüllt ist.",
                      opts=[
                        ("sie wiederholt einen oder mehrere Schritte, bis eine Bedingung erfüllt ist", True, None),
                        ("sie trifft eine einmalige Entscheidung", False, "Das ist die Aufgabe der Verzweigung, nicht der Schleife."),
                        ("sie ist nur die Eingabe eines Algorithmus", False, "Die Schleife ist eine Kontrollstruktur, kein Eingabeschritt."),
                        ("sie hat in Algorithmen keine Funktion", False, "Die Schleife ist einer der zentralen Algorithmus-Bausteine."),
                      ]),
                 dict(q="Worin unterscheiden sich Verzweigung und Schleife grundsätzlich?",
                      done="Richtig — einmalig entscheiden vs. wiederholen.",
                      opts=[
                        ("die Verzweigung entscheidet einmalig, die Schleife wiederholt", True, None),
                        ("beide machen exakt dasselbe", False, "Sie erfüllen unterschiedliche Aufgaben im Algorithmus."),
                        ("die Schleife entscheidet, die Verzweigung wiederholt", False, "Das ist genau vertauscht."),
                        ("keins von beidem hat mit Algorithmen zu tun", False, "Beide sind zentrale Algorithmus-Bausteine."),
                      ]),
               ]),
             ],
             quiz=[
               dict(q="Wofür steht EVA?",
                    done="Richtig — genau in dieser Reihenfolge: E, V, A.",
                    opts=[
                      ("Eingabe, Verarbeitung, Ausgabe", True, None),
                      ("Entwicklung, Verifikation, Anwendung", False, "EVA beschreibt den Arbeitsablauf eines Computers, nicht den Softwareentwicklungsprozess."),
                      ("Eingabe, Verschlüsselung, Ausgabe", False, "Der mittlere Schritt heißt Verarbeitung, nicht Verschlüsselung."),
                      ("Einheit, Verzweigung, Algorithmus", False, "Das sind Begriffe aus dem Algorithmus-Teil, nicht die Bedeutung von EVA."),
                    ]),
               dict(q="Was ist ein Algorithmus?",
                    done="Genau — eine eindeutige, endliche Schrittfolge.",
                    opts=[
                      ("Eine eindeutige, endliche Schrittfolge zur Lösung eines Problems.", True, None),
                      ("Ein beliebiger Name für ein Programm.", False, "Ein Algorithmus ist die Schrittfolge dahinter, nicht einfach ein Name."),
                      ("Nur eine Schleife ohne Bedingung.", False, "Eine Schleife ist höchstens ein Baustein eines Algorithmus, nicht der ganze Begriff."),
                      ("Ein Gerät zur Dateneingabe.", False, "Das beschreibt ein Eingabegerät, keinen Algorithmus."),
                    ]),
               dict(q="Was macht eine Verzweigung in einem Algorithmus?",
                    done="Stimmt — eine Entscheidung anhand einer Bedingung.",
                    opts=[
                      ("Sie trifft abhängig von einer Bedingung eine Entscheidung (wenn … dann … sonst).", True, None),
                      ("Sie wiederholt einen Schritt immer wieder.", False, "Das beschreibt eine Schleife, keine Verzweigung."),
                      ("Sie beendet den Algorithmus sofort.", False, "Verzweigungen entscheiden, sie beenden den Algorithmus nicht zwangsläufig."),
                      ("Sie speichert Daten dauerhaft.", False, "Das ist die Aufgabe eines Speichers, nicht einer Verzweigung."),
                    ]),
               dict(q="Was macht eine Schleife in einem Algorithmus?",
                    done="Richtig — sie wiederholt Schritte.",
                    opts=[
                      ("Sie wiederholt einen oder mehrere Schritte.", True, None),
                      ("Sie trifft eine einmalige Entscheidung.", False, "Eine einmalige Entscheidung ist eine Verzweigung, keine Schleife."),
                      ("Sie ist nur die Eingabe eines Algorithmus.", False, "Eingabe ist ein EVA-Schritt, keine Schleife."),
                      ("Sie hat in Algorithmen keine Funktion.", False, "Schleifen sind einer der wichtigsten Bausteine von Algorithmen."),
                    ]),
             ],
             solution=["EVA = Eingabe (Sensoren/Tastatur) → Verarbeitung (Prozessor) → Ausgabe (Bildschirm/Aktor).",
                       "Ein Algorithmus ist eine eindeutige, endliche Schrittfolge; Bausteine: Sequenz, Verzweigung, Schleife.",
                       "Beispiel Ampel: Eingabe = Zeit/Sensor, Verarbeitung = Steuerlogik, Ausgabe = Lichtsignal."]),
      ]),
 dict(hj=1, num="01", title="Blockbasiert I — Scratch & Makey Makey",
      key="#34ff9e", key2="#12c47a", tint="rgba(52,255,158,0.09)",
      lps=[
        dict(no=2, sjw=2, kind="lernpfad", title="Scratch-Grundlagen: Bühne, Figuren, Ereignisse",
             goal="Du baust in Scratch dein erstes Programm: Figuren steuern, Ereignisse („Wenn Flagge geklickt“) nutzen und eine Sequenz aus Blöcken zusammensetzen.",
             tasks=["Eine Figur per Ereignisblock starten und über die Bühne bewegen.",
                    "Bewegung, Aussehen und Klang zu einer kleinen Szene kombinieren.",
                    "Programm als <code>.sb3</code> exportieren und im Backup-Ordner sichern."],
             tools=["scratch"],
             fast="Baue ein zweites Sprite, das auf das erste reagiert (z. B. per Nachricht senden/empfangen).",
             rlp=["RLP 2.2 · Algorithmen", "3.3 Blockbasierte Programmierung", "neu · Scratch"],
             vorwissen=[
               dict(fig="fig1", cap="Bild 1 · Die Scratch-Oberfläche", quiz=[
                 dict(q="Wie heißt Teil 1, der Bereich mit den sortierten Block-Kategorien?",
                      done="Richtig — die Blockpalette.",
                      opts=[
                        ("Blockpalette", True, None),
                        ("Skriptbereich", False, "Dort werden die Blöcke zusammengesetzt, nicht sortiert angeboten."),
                        ("Bühne", False, "Die Bühne zeigt das laufende Programm, keine Block-Kategorien."),
                        ("Figurenliste", False, "Dort wählst du Sprites aus, keine Blöcke."),
                      ]),
                 dict(q="Wozu dient Teil 2, der Skriptbereich?",
                      done="Genau — hier entsteht das Programm.",
                      opts=[
                        ("Hier werden Blöcke zu einem Programm zusammengesetzt.", True, None),
                        ("Hier läuft das fertige Programm ab.", False, "Das passiert auf der Bühne, nicht im Skriptbereich."),
                        ("Hier wählst du die Sprites aus.", False, "Das übernimmt die Figurenliste."),
                        ("Hier speicherst du dein Projekt.", False, "Gespeichert wird über das Datei-Menü, nicht im Skriptbereich."),
                      ]),
                 dict(q="Was zeigt Teil 3, die Bühne?",
                      done="Stimmt — das laufende Programm.",
                      opts=[
                        ("das laufende Programm mit der Figur", True, None),
                        ("die verfügbaren Blockkategorien", False, "Das zeigt die Blockpalette, nicht die Bühne."),
                        ("die Liste aller Sprites", False, "Das zeigt die Figurenliste, nicht die Bühne."),
                        ("den Programmcode als Text", False, "Scratch zeigt Code als Blöcke, nicht als Text."),
                      ]),
                 dict(q="Wozu dient Teil 4, die Figurenliste?",
                      done="Richtig — zum Wechseln zwischen Sprites.",
                      opts=[
                        ("um zwischen den Sprites (Figuren) im Projekt zu wechseln", True, None),
                        ("um Blöcke zu suchen", False, "Blöcke suchst du in der Blockpalette."),
                        ("um das Programm zu starten", False, "Gestartet wird meist über die grüne Flagge über der Bühne."),
                        ("um das Projekt zu exportieren", False, "Der Export läuft über das Datei-Menü."),
                      ]),
               ]),
               dict(fig="fig2", cap="Bild 2 · Vom Ereignis zum fertigen Projekt", quiz=[
                 dict(q='Wozu dient Teil 1, der Ereignisblock (z. B. "wenn Flagge geklickt")?',
                      done="Richtig — er startet die Sequenz.",
                      opts=[
                        ("Er startet die darunter angehängte Sequenz von Blöcken.", True, None),
                        ("Er speichert das Projekt.", False, "Gespeichert wird über das Datei-Menü, nicht durch einen Ereignisblock."),
                        ("Er löscht alle Blöcke.", False, "Ein Ereignisblock startet Blöcke, er löscht nichts."),
                        ("Er öffnet die Blockpalette.", False, "Die Blockpalette ist immer sichtbar, dafür braucht es keinen Ereignisblock."),
                      ]),
                 dict(q="Was passiert bei Teil 2, der Sequenz aus Blöcken?",
                      done="Genau — feste Reihenfolge.",
                      opts=[
                        ("Die Blöcke werden in fester Reihenfolge nacheinander abgearbeitet.", True, None),
                        ("Die Blöcke laufen alle gleichzeitig, in beliebiger Reihenfolge.", False, "Eine Sequenz läuft geordnet ab, nicht gleichzeitig."),
                        ("Nur der letzte Block wird ausgeführt.", False, "Alle Blöcke der Sequenz werden ausgeführt, nicht nur der letzte."),
                        ("Die Reihenfolge der Blöcke spielt keine Rolle.", False, "Die Reihenfolge ist bei einer Sequenz entscheidend."),
                      ]),
                 dict(q="Wie sicherst du dein fertiges Projekt (Teil 3)?",
                      done="Stimmt — als .sb3-Datei.",
                      opts=[
                        ("als .sb3-Datei über „Auf deinen Computer herunterladen“", True, None),
                        ("als .exe-Datei", False, "Scratch-Projekte werden im .sb3-Format gespeichert, nicht als .exe."),
                        ("gar nicht, Scratch speichert nichts", False, "Scratch bietet einen expliziten Speicher-/Download-Befehl."),
                        ("nur als Bildschirmfoto", False, "Ein Screenshot sichert kein lauffähiges Projekt."),
                      ]),
                 dict(q="Was haben Ereignisblock und Sequenz gemeinsam?",
                      done="Richtig — zusammen ein startbares Mini-Programm.",
                      opts=[
                        ("Zusammen bilden sie ein vollständiges, startbares Mini-Programm.", True, None),
                        ("Beide brauchen keine Bühne.", False, "Das Ergebnis wird immer auf der Bühne angezeigt."),
                        ("Beide speichern automatisch jede Sekunde.", False, "Gespeichert wird nur manuell über den Download-Befehl."),
                        ("Keins von beidem lässt sich exportieren.", False, "Das gesamte Projekt lässt sich als .sb3 exportieren."),
                      ]),
               ]),
             ],
             quiz=[
               dict(q="Womit startest du typischerweise eine Scratch-Sequenz?",
                    done="Richtig — ein Ereignisblock startet die Sequenz.",
                    opts=[
                      ("Mit einem Ereignisblock wie „Wenn Flagge geklickt“.", True, None),
                      ("Mit einem Schleifenblock.", False, "Schleifen wiederholen einen bereits laufenden Ablauf, sie starten ihn nicht."),
                      ("Nur durch Drücken der Leertaste.", False, "Das würde nur funktionieren, wenn extra ein Tastendruck-Ereignis eingerichtet wurde."),
                      ("Scratch startet nie automatisch.", False, "Ein Ereignisblock wie die grüne Flagge startet die Sequenz sehr wohl automatisch."),
                    ]),
               dict(q="Was ist eine Sequenz in Scratch?",
                    done="Genau — Blöcke in fester Reihenfolge.",
                    opts=[
                      ("Blöcke in fester Reihenfolge, die wie Puzzleteile verbunden sind.", True, None),
                      ("Ein einzelner, isolierter Block.", False, "Ein einzelner Block allein ist noch keine Sequenz."),
                      ("Eine Datei-Endung.", False, "Das meint z. B. .sb3 — das ist keine Sequenz."),
                      ("Ein Werkzeug zum Zeichnen.", False, "Zeichnen übernehmen Bewegungs-/Stift-Blöcke, nicht der Begriff Sequenz."),
                    ]),
               dict(q="Wie exportierst du dein Scratch-Projekt?",
                    done="Stimmt — als .sb3 über den Download-Befehl.",
                    opts=[
                      ("Als .sb3-Datei über Datei → „Auf deinen Computer herunterladen“.", True, None),
                      ("Als .exe-Datei.", False, "Scratch-Projekte werden als .sb3 gespeichert, nicht als ausführbare .exe-Datei."),
                      ("Es lässt sich nicht exportieren.", False, "Der Export ist möglich und sogar Teil der Aufgabe (Backup!)."),
                      ("Nur als Bildschirmfoto.", False, "Ein Bildschirmfoto sichert nicht den Code, nur der .sb3-Export tut das."),
                    ]),
               dict(q="Wie kann ein zweites Sprite auf ein erstes reagieren?",
                    done="Richtig — über Nachrichten senden/empfangen.",
                    opts=[
                      ("Über Nachrichten senden und empfangen.", True, None),
                      ("Das ist in Scratch nicht möglich.", False, "Genau das ermöglichen Nachrichtenblöcke in Scratch."),
                      ("Nur durch Zufall.", False, "Über Nachrichten lässt sich das gezielt und zuverlässig steuern, nicht dem Zufall überlassen."),
                      ("Nur wenn beide Sprites exakt gleich aussehen.", False, "Das Aussehen spielt dabei keine Rolle, nur die Nachricht selbst zählt."),
                    ]),
             ],
             solution=["Ereignisblock „Wenn 🏳 angeklickt“ startet die Sequenz.",
                       "Sequenz = Blöcke in fester Reihenfolge; Scratch verbindet sie wie Puzzleteile.",
                       "Export über Datei → „Auf deinen Computer herunterladen“."]),
        dict(no=3, sjw=3, kind="lernpfad", title="Schleifen & Verzweigungen: ein Mini-Spiel",
             goal="Du setzt „wiederhole“-Schleifen und „falls … dann“-Verzweigungen ein und programmierst ein einfaches Fang- oder Ausweichspiel.",
             tasks=["Eine Endlosschleife bauen, die ständig abfragt, ob eine Pfeiltaste gedrückt wurde, und die Figur entsprechend bewegen.",
                    "Eine Verzweigung ergänzen („falls Figur berührt Rand → dreht ab/prallt ab“), eine Punktevariable anlegen und bei einem Treffer erhöhen.",
                    "In zwei bis drei Sätzen erklären, warum man beim Testen einer Endlosschleife in Scratch besonders vorsichtig sein muss und wie man das Programm trotzdem sicher stoppen kann."],
             tools=["scratch"],
             fast="Vertiefungen aus Sitzung 00, 01, 02.<br>Füge einen Schwierigkeitsgrad hinzu: Das Spiel wird mit steigender Punktzahl schneller.<br>Nützliches: Erstelle eine Grußkarte unter Verwendung der Steuerelemente und einer Variable.",
             rlp=["RLP 2.2 · Kontrollstrukturen", "3.3 Schleife & Verzweigung"],
             vorwissen=[
               dict(fig="fig1", cap="Bild 1 · Endlosschleife + Tastaturabfrage", quiz=[
                 dict(q='Wozu dient Teil 1, die Endlosschleife ("wiederhole fortlaufend")?',
                      done="Richtig, sie prüft ständig.",
                      opts=[
                        ("Sie startet das Programm zum Bewegen der Figur.", False, "Gestartet wird das Programm durch einen Ereignisblock, die Schleife wiederholt nur."),
                        ("Sie prüft ständig, ob eine Bedingung eingetreten ist.", True, None),
                        ("Sie prüft die Bedingung genau einmal.", False, "Das würde eine einmalige Verzweigung tun, keine Endlosschleife."),
                        ("Sie beendet das Programm sofort.", False, "Eine Endlosschleife läuft weiter, sie beendet nichts."),
                      ]),
                 dict(q='Was passiert bei Teil 2, wenn die Bedingung "Taste links?" erfüllt ist?',
                      done="Genau, die Aktion wird ausgeführt.",
                      opts=[
                        ("Die angehängte Aktion wird ausgeführt (z. B. Bewegung nach links).", True, None),
                        ("Das ganze Programm stoppt sofort und muss neu gestartet werden.", False, "Eine erfüllte Bedingung löst die Aktion aus, sie stoppt nicht das Programm."),
                        ("Die Schleife wird vollständig beendet.", False, "Die Endlosschleife läuft weiter, nur die Aktion wird ausgeführt."),
                        ("Es muss erneut auf die grüne Flagge geklickt werden.", False, "Die Flagge startet das Programm einmal, danach läuft die Schleife von selbst weiter."),
                      ]),
                 dict(q="Was passiert bei Teil 3, wenn die Bedingung NICHT erfüllt ist?",
                      done="Stimmt, die Aktion wird übersprungen.",
                      opts=[
                        ("Das Programm stürzt ab.", False, "Eine nicht erfüllte Bedingung führt zu keinem Absturz."),
                        ("Die Aktion wird übersprungen, die Schleife läuft weiter.", True, None),
                        ("Die Aktion wird übersprungen, jedoch bricht die Schleife ab.", False, "Die Schleife bricht nicht ab, sie prüft im nächsten Durchlauf erneut."),
                        ("Die Aktion wird trotzdem ausgeführt.", False, "Ohne erfüllte Bedingung wird die Aktion gerade nicht ausgeführt."),
                      ]),
                 dict(q="Warum steckt die Verzweigung INNERHALB der Schleife und nicht davor?",
                      done="Richtig, so wird ständig neu geprüft.",
                      opts=[
                        ("Das spielt keine Rolle, beide Anordnungen sind identisch in ihrer Funktion für das Programm.", False, "Außerhalb der Schleife würde die Bedingung nur einmal geprüft."),
                        ("Es ist dafür wichtig, dass die Bedingung nur einmal beim Start geprüft wird.", False, "Genau das würde passieren, wenn sie außerhalb stünde. Das ist nicht gewollt."),
                        ("Es ist dafür wichtig, dass die Bedingung ständig neu geprüft wird, solange das Spiel läuft.", True, None),
                        ("Es ist dafür wichtig, dass das Programm schneller und fehlerfrei läuft.", False, "Die Position hat nichts mit der Geschwindigkeit zu tun."),
                      ]),
               ]),
               dict(fig="fig2", cap="Bild 2 · Punktevariable + Kollision", quiz=[
                 dict(q='Wozu dient Teil 1, die Variable „Punkte“?',
                      done="Richtig, sie speichert den Punktestand.",
                      opts=[
                        ("Sie steuert die Bühnenfarbe für das ablaufende Programm.", False, "Die Bühnenfarbe wird nicht über eine Punkte-Variable gesteuert."),
                        ("Sie zeichnet die Spielfigur (Sprite).", False, "Zeichnen übernimmt das Kostüm des Sprites, nicht die Variable."),
                        ("Sie speichert einen Zustand (den Punktestand), der sich über die Zeit verändert.", True, None),
                        ("Variablen werden in Scratch nicht benötigt.", False, "Variablen sind ein zentraler Baustein in Scratch."),
                      ]),
                 dict(q="Womit erkennst du eine Kollision (Teil 2)?",
                      done='Genau, der „wird … berührt?“-Block prüft das.',
                      opts=[
                        ("Mit der Drehung um 180 °.", False, "Eine Drehung ist eine Bewegung, sie erkennt keine Berührung."),
                        ("Mit einer Endlosschleife im Programm.", False, "Die Schleife wiederholt nur die Prüfung, sie erkennt selbst keine Berührung."),
                        ('Mit einem „wird … berührt?“-Block als Bedingung.', True, None),
                        ('Mit einem „Pfeil nach rechts gedrückt?“-Block als Bedingung.', False, "Dieser Block fragt die Tastatur ab, nicht die Berührung von zwei Figuren."),
                      ]),
                 dict(q='Warum sollte „ändere Punkte um 1“ INNERHALB der Kollisions-Verzweigung stehen?',
                      done="Richtig, nur bei einem echten Treffer.",
                      opts=[
                        ("Das spielt keine Rolle, die Position ist beliebig.", False, "Innerhalb der Verzweigung zählt nur ein echter Treffer."),
                        ("Damit der Punktestand nur bei einem echten Treffer steigt.", True, None),
                        ("Damit der Punktestand jede Sekunde automatisch steigt.", False, "Das würde passieren, wenn der Block außerhalb der Verzweigung stünde."),
                        ("Damit die Variable gelöscht wird.", False, "Der Block erhöht die Variable, er löscht sie nicht."),
                      ]),
                 dict(q="Wozu dient eine Endlosschleife beim Abfragen der Tastatur?",
                      done="Richtig, sie fragt ständig ab.",
                      opts=[
                        ("Damit ständig geprüft wird, ob eine Taste gedrückt wurde.", True, None),
                        ("Damit das Programm nach einem Tastendruck sofort endet.", False, "Eine Endlosschleife läuft weiter, sie beendet das Programm nicht."),
                        ("Damit die Tastatur ausgeschaltet wird.", False, "Die Schleife fragt die Tastatur ab, schaltet sie aber nicht aus."),
                        ("Sie hat damit nichts zu tun.", False, "Genau das ständige Abfragen ist ihre Aufgabe."),
                      ]),
                 dict(q='Wie implementierst du „ändere Punkte um 1“? (implementieren = umsetzen)',
                      done="Richtig, alter Wert plus 1.",
                      opts=[
                        ("Variablenblock „Setze Variable auf +1“", False, "Das würde die Variable jedes Mal nur auf +1 setzen, der bisherige Wert ginge verloren."),
                        ("Variablenblock „Setze Variable auf (Operatorenblock (Variablenblock Variable) + Tastendruck)“", False, "Ein Tastendruck ist keine Zahl, die man zum Punktestand addieren kann."),
                        ("Variablenblock „Setze Variable auf (Operatorenblock + 1)“", False, "Im Operatorenblock fehlt der bisherige Wert der Variable."),
                        ("Variablenblock „Setze Variable auf (Operatorenblock (Variablenblock Variable) + 1)“", True, None),
                      ]),
                 dict(q='Was passiert bei der Verzweigung „falls Figur berührt Rand“?',
                      done="Genau, die Bedingung löst eine Reaktion aus.",
                      opts=[
                        ("Die Figur verschwindet immer sofort und verlässt das Feld.", False, "Das würde nur passieren, wenn extra ein Verschwinden programmiert wäre."),
                        ("Das Spiel startet automatisch neu.", False, "Ein Neustart müsste eigens programmiert werden, das macht die Verzweigung allein nicht."),
                        ("Es passiert nichts, Verzweigungen (Fallunterscheidungen) wirken nicht auf Figuren.", False, "Verzweigungen steuern genau solche Reaktionen von Figuren."),
                        ("Die Figur reagiert (z. B. dreht ab/stößt zurück), wenn die Bedingung erfüllt ist.", True, None),
                      ]),
               ]),
             ],
             solution=["Bild 1: (1) Endlosschleife („wiederhole fortlaufend“), (2) Verzweigung (Tastenabfrage), (3) Aktion (Bewegung).",
                       "Bild 2: (1) Variable („Punkte“), (2) Kollisionsbedingung, (3) Punktezähler-Erhöhung.",
                       "Aufgabe 3: Eine Endlosschleife läuft ohne Pause weiter und kann Scratch sehr schnell ausbremsen oder dafür sorgen, dass du keine Blöcke mehr anklicken kannst, wenn darin zu viel auf einmal passiert. Du kannst das Programm sicher stoppen, indem du das rote Stopp-Zeichen klickst oder in die Schleife eine Abbruchbedingung einbaust (z. B. „falls Taste [Leertaste] gedrückt, dann stoppe alles“)."]),
        dict(no=4, sjw=4, kind="lernpfad", title="Makey Makey: die Welt wird zum Controller",
             goal="Du verbindest Makey Makey mit Scratch, schließt einen Stromkreis über leitfähige Alltagsgegenstände und erklärst, warum das ein greifbares Beispiel für Eingabe im EVA-Prinzip ist.",
             # lp04.html enthält zusätzlich handgebaute Abschnitte (Aufgaben mit Spiel-Links, Controller-Test,
             # Sondervertiefung Rundenspiel-Controller mit Bauplänen) — Quelle: extras/lp04/build.py.
             tasks=["Makey Makey anschließen, EARTH über eine Krokodilklemme mit jeweils einer Person verbinden (z. B. Armband aus Alufolie) und die Pfeiltasten aus euren Spielen der letzten Woche mit Bananenstücken über deren Schale verknüpfen.",
                    "Eure beiden Spiele um je einen weiteren Tastendruck per Makey Makey erweitern (z. B. einen Bühnenbildwechsel), mit Kommentaren versehen und als .sb3-Datei (Inhalt+Vorname.sb3) im Classroom abgeben.",
                    "Ein kreatives Projekt zur Umsetzung des EVA-Prinzips planen (z. B. ein rundenbasiertes Teamspiel mit Makey Makey und Scratch oder eine Anwendung aus Alltag oder Technik) und der Gruppe präsentieren."],
             tools=["makey", "scratch"],
             fast="Sondervertiefung: Baut einen eigenen Alufolien-Controller für ein Rundenspiel (Tic Tac Toe, Vier gewinnt, Schiffe versenken oder Schach) — Denkanstöße, Stufen und Baupläne gibt es auf Nachfrage per Klick.",
             rlp=["RLP 2.3 · Informatiksysteme", "3.2 Ein-/Ausgabe", "neu · Physical Computing"],
             vorwissen=[
               dict(fig="fig1", cap="Bild 1 · Das Makey-Makey-Board", quiz=[
                 dict(q="Wozu dient Teil 1, der EARTH-Anschluss?",
                      done="Richtig — er schließt den Stromkreis.",
                      opts=[
                        ("Er schließt den Stromkreis, meist indem man ihn selbst berührt (Erdung).", True, None),
                        ("Er lädt das Gerät auf.", False, "Makey Makey wird über USB versorgt, nicht über EARTH."),
                        ("Er verbindet Makey Makey mit dem Internet.", False, "EARTH hat mit einer Internetverbindung nichts zu tun."),
                        ("Er hat keine erkennbare Funktion.", False, "EARTH ist für den geschlossenen Stromkreis unverzichtbar."),
                      ]),
                 dict(q="Wofür stehen die Pins bei Teil 2?",
                      done="Genau — die Pfeiltasten.",
                      opts=[
                        ("für die vier Pfeiltasten (up, down, left, right)", True, None),
                        ("für Lautstärke und Helligkeit", False, "Dafür hat Makey Makey keine eigenen Pins."),
                        ("für den Ein-/Ausschalter", False, "Makey Makey hat keinen separaten Ein-/Ausschalter-Pin."),
                        ("für die Internetverbindung", False, "Makey Makey verbindet sich nicht mit dem Internet."),
                      ]),
                 dict(q="Wofür steht der Pin bei Teil 3?",
                      done="Stimmt — für die Leertaste.",
                      opts=[
                        ("für die Leertaste", True, None),
                        ("für die Eingabetaste (Enter)", False, "Dafür gibt es keinen eigenen Pin bei Makey Makey."),
                        ("für den Mauszeiger", False, "Makey Makey simuliert Tastendrücke, keine Mausbewegung."),
                        ("für die Umschalttaste", False, "Dafür ist kein eigener Pin vorgesehen."),
                      ]),
                 dict(q="Wozu dient Teil 4, das USB-Kabel?",
                      done="Richtig — es überträgt die Signale.",
                      opts=[
                        ("es verbindet Makey Makey mit dem Computer und überträgt die Signale", True, None),
                        ("es lädt nur den Akku auf", False, "Makey Makey hat keinen eigenen Akku."),
                        ("es verbindet zwei Makey-Makey-Boards miteinander", False, "Das USB-Kabel geht zum Computer, nicht zu einem zweiten Board."),
                        ("es hat keine Funktion beim Spielen", False, "Ohne USB-Verbindung erreichen die Signale den Computer nicht."),
                      ]),
               ]),
               dict(fig="fig2", cap="Bild 2 · Der Stromkreis", quiz=[
                 dict(q="Was ist Teil 1?",
                      done="Richtig — Makey Makey.",
                      opts=[
                        ("Makey Makey", True, None),
                        ("der Computer", False, "Der Computer empfängt nur die Signale von Makey Makey."),
                        ("die Banane", False, "Die Banane ist das leitfähige Objekt, nicht das Board."),
                        ("die Person", False, "Die Person schließt den Kreis, ist aber nicht das Board."),
                      ]),
                 dict(q="Was ist Teil 2, der leitfähige Gegenstand?",
                      done="Genau — die Banane.",
                      opts=[
                        ("die Banane, verbunden über eine Krokodilklemme", True, None),
                        ("ein Radiergummi", False, "Radiergummi leitet keinen Strom."),
                        ("ein Stück Holz", False, "Holz ist nicht leitfähig."),
                        ("eine Fensterscheibe", False, "Glas leitet keinen Strom."),
                      ]),
                 dict(q="Was macht Teil 3, die Person?",
                      done="Stimmt — sie schließt den Stromkreis.",
                      opts=[
                        ("Sie schließt den Stromkreis, indem sie Banane UND EARTH gleichzeitig berührt.", True, None),
                        ("Sie lädt das Makey-Makey-Board auf.", False, "Das Board wird über USB versorgt, nicht über die Person."),
                        ("Sie programmiert das Scratch-Skript.", False, "Das Skript wurde vorher am Rechner erstellt."),
                        ("Sie hat keine Funktion im Stromkreis.", False, "Ohne die Person bleibt der Stromkreis offen."),
                      ]),
                 dict(q="Was passiert bei Teil 4, wenn der Kreis geschlossen ist?",
                      done="Richtig — der Computer erkennt ein Signal.",
                      opts=[
                        ("der Computer erkennt ein Signal, so als wäre eine Taste gedrückt worden", True, None),
                        ("der Computer schaltet sich aus", False, "Ein geschlossener Kreis simuliert nur einen Tastendruck."),
                        ("nichts, es passiert nichts Sichtbares", False, "Im Scratch-Projekt löst das Signal eine Reaktion aus."),
                        ("die Banane wird beschädigt", False, "Die schwachen USB-Ströme schaden der Banane nicht."),
                      ]),
                 dict(q="Was ersetzt Makey Makey im Grunde?",
                      done="Richtig — Tastatur-/Maus-Signale.",
                      opts=[
                        ("Signale von Tastatur und Maus", True, None),
                        ("den gesamten Computer", False, "Makey Makey ersetzt nur die Eingabesignale, nicht den ganzen Computer."),
                        ("die Scratch-Software", False, "Scratch läuft weiterhin normal — Makey Makey liefert nur andere Eingaben."),
                        ("den Bildschirm", False, "Der Bildschirm gehört zur Ausgabe, damit hat Makey Makey nichts zu tun."),
                      ]),
                 dict(q="Wodurch entsteht ein „Tastendruck“ bei Makey Makey?",
                      done="Genau — ein geschlossener Stromkreis über den Körper.",
                      opts=[
                        ("durch einen geschlossenen Stromkreis, z. B. über den eigenen Körper", True, None),
                        ("durch lautes Klopfen auf den Tisch", False, "Es zählt der geschlossene Stromkreis, nicht die Lautstärke."),
                        ("durch eine WLAN-Verbindung", False, "Makey Makey arbeitet über Kabel und Stromkreise, nicht über WLAN."),
                        ("nur durch Drücken einer echten Computertaste", False, "Genau das will Makey Makey ersetzen — durch leitfähige Alltagsgegenstände."),
                      ]),
                 dict(q="Welche Alltagsgegenstände eignen sich als leitfähige „Tasten“?",
                      done="Stimmt — leitfähige Alltagsgegenstände.",
                      opts=[
                        ("z. B. Bananen, Alufolie und Wasser", True, None),
                        ("z. B. Plastik und Glas", False, "Plastik und Glas sind Isolatoren — sie leiten keinen Strom."),
                        ("z. B. Gummi, Steine und Papier", False, "Gummi, trockene Steine und Papier leiten Strom kaum."),
                        ("gar keine, es braucht spezielle Hardware", False, "Genau alltägliche, leitfähige Gegenstände funktionieren als Taste — keine Spezialhardware nötig."),
                      ]),
               ]),
             ],
             solution=["Bild 1: (1) EARTH (Erdung), (2) Pfeiltasten-Pins, (3) Leertaste-Pin, (4) USB-Anschluss zum Computer.",
                       "Bild 2: (1) Makey Makey, (2) leitfähiges Objekt (Banane), (3) Person (schließt den Stromkreis), (4) Signal im Computer.",
                       "Makey Makey ersetzt Signale von Tastatur und Maus. Ein „Tastendruck“ entsteht durch einen geschlossenen Stromkreis, z. B. über den eigenen Körper — erst wenn Objekt UND EARTH berührt werden, ist der Kreis geschlossen. Das ist der Eingabe-Schritt im EVA-Prinzip. Leitfähig sind z. B. Bananen, Alufolie und Wasser.",
                       "Aufgabe 2 (Beispiel Bühnenbildwechsel): <code>Wenn Taste [Leertaste] gedrückt wird → wechsle zu Bühnenbild [nächstes Bühnenbild]</code>, dazu ein Kommentar am Block, der erklärt, welche Makey-Makey-Taste was auslöst.",
                       "Aufgabe 3: Eingabe = was berührt/gedrückt wird (Makey-Makey-Taste), Verarbeitung = was das Scratch-Skript daraufhin prüft und berechnet, Ausgabe = was man sieht oder hört (Figur, Bühnenbild, Klang)."]),
      ]),
 dict(hj=1, num="02", title="Blockbasiert II — Tinkercad & Arduino",
      key="#a56bff", key2="#7d3ff0", tint="rgba(165,107,255,0.09)",
      lps=[
        dict(no=5, sjw=5, kind="lernpfad", title="Arduino: Einführung am Beispiel der LED",
             goal="Du lernst den Mikrocontroller Arduino und die Bauteile einer LED-Schaltung kennen, benennst sie, zeichnest deinen ersten geschlossenen Stromkreis und verstehst, warum der Widerstand die LED schützt.",
             # Quelle Arbeits-/Lösungsblatt: <Lektion>/typst/05-arduino-einfuehrung.typ, Grafiken: build_abb_arduino.py
             material=(
               "<p><b>Woher kommt der Name?</b> Der Arduino wurde 2005 im italienischen Städtchen Ivrea erfunden, damit Lernende günstig eigene Elektronik bauen und programmieren können. Die Entwickler trafen sich oft in der „Bar di Re Arduino“, benannt nach König Arduin von Ivrea, der um das Jahr 1000 König von Italien war. Der Name kommt aus dem Germanischen (Hartwin) und bedeutet etwa „starker Freund“. „Uno“ heißt auf Italienisch „eins“.</p>"
               "<p><b>Die Mikrocontroller-Platine Arduino Uno</b> hat als „Gehirn“ den langen schwarzen Chip ATmega328P, einen winzigen Computer, der ein Programm (einen <i>Sketch</i>) Schritt für Schritt ausführt. Über das USB-Kabel bekommt sie Strom und neue Programme vom Computer. Bauteile werden an den schwarzen Pinleisten am Rand angeschlossen.</p>"
               "<p><b>Plus- und Minuspol.</b> Strom fließt nur in einem geschlossenen Stromkreis zwischen zwei Polen. Am <b>Minuspol</b> gibt es einen Überschuss an Elektronen, am <b>Pluspol</b> einen Mangel (Unterschuss). Diesen Unterschied nennt man <b>Spannung</b>, gemessen in Volt (V). Ist der Kreis geschlossen, fließen die Elektronen vom Minus- zum Pluspol. Die <i>technische Stromrichtung</i> wurde festgelegt, bevor man Elektronen kannte, und zeigt deshalb andersherum von Plus nach Minus. Am Arduino heißt der Pluspol <b>5V</b>, er liegt 5 Volt über dem Minuspol. Der Minuspol heißt <b>GND</b> (engl. <i>ground</i>, Erde/Masse) und ist der Bezugspunkt mit 0 V, so wie EARTH am Makey Makey.</p>"
               "<p><b>Das Steckbrett</b> (engl. <i>breadboard</i>, „Brotbrett“: Früher wurden Schaltungen auf Holzbrettchen geschraubt) verbindet Bauteile ohne Löten. Die fünf Löcher einer Spalte (a–e bzw. f–j) sind innen leitend verbunden, die Mitte trennt beide Hälften. Die Schienen am Rand (+ rot, − blau) verlaufen waagerecht.</p>"
               "<p><b>Die LED</b> (engl. <i>light-emitting diode</i>, Leuchtdiode) lässt Strom nur in eine Richtung durch, wie eine Einbahnstraße. Ihr <b>langes Beinchen</b> ist die <b>Anode</b> (+) und zeigt Richtung 5V, das <b>kurze</b> die <b>Kathode</b> (−) Richtung GND. In Tinkercad ist das Anodenbeinchen geknickt.</p>"
               "<p><b>Der Widerstand</b> mit den Farbringen rot-rot-braun hat 220 Ω (Ohm). Als <b>Vorwiderstand</b> vor der LED begrenzt er die Stromstärke. Ohne ihn flösse zu viel Strom und die LED würde durchbrennen. Seine Einbaurichtung ist egal.</p>"),
             tasks=["<b>Benenne</b> mithilfe des Informationstextes die vier Bauteile aus Abbildung 1.",
                    "<b>Zeichne</b> LED, Widerstand und zwei Kabel (zu 5V rot, zu GND schwarz) so in Abbildung 2 auf deinem Arbeitsblatt ein, dass ein geschlossener Stromkreis entsteht. Achte auf Anode und Kathode. <b>Überprüfe</b> deine Skizze am echten Arduino.",
                    "<b>Fotografiere</b> deine funktionierende Schaltung, <b>beschrifte</b> das Foto und <b>lade</b> es im Classroom hoch (siehe Leistungsnachweis unten).",
                    "Vertiefung (Wahl, siehe unten, auf dem Arbeitsblatt Aufgabe 4): a) weitere Bauteile anschließen und ihre Polung herausfinden, b) den Vorwiderstand berechnen und drei LEDs parallel und in Reihe vergleichen."],
             task_figs=[dict(fig="abb1-bauteile", cap="Abbildung 1 · Bauteile (LED-Schaltung)"),
                        dict(fig="abb2-schaltkreis", cap="Abbildung 2 · Schaltkreis der angeschlossenen LED")],
             tools=[],
             fast="Schließe einen Propeller-Motor, einen Buzzer und einen Tastschalter an und finde ihre Polung heraus. Berechne den Vorwiderstand der LED und vergleiche drei LEDs parallel und in Reihe.",
             vertiefung=LP05_VERTIEFUNG,
             sicherung=("📷 Leistungsnachweis · Ergebnissicherung",
                        "Fotografiere deine <b>funktionierende Schaltung</b> (die LED leuchtet) so, dass Arduino, Steckbrett, Widerstand, LED und beide Kabel gut zu sehen sind. "
                        "<b>Beschrifte</b> auf dem Foto die vier Bauteile sowie <b>5V</b>, <b>GND</b>, <b>Anode (+)</b> und <b>Kathode (−)</b> und "
                        "<b>lade</b> es als Abgabe im <b>Google Classroom</b> hoch. Sichere das Foto zusätzlich in deinem Informatik-Ordner."),
             rlp=["RLP 2.3 · Informatiksysteme", "3.2 Hardware", "neu · Physical Computing"],
             quiz=[
               dict(q="Wie heißt Bauteil 1 in Abbildung 1?",
                    done="Richtig, die Mikrocontroller-Platine Arduino Uno.",
                    opts=[
                      ("ein Steckbrett", False, "Das Steckbrett ist die weiße Platte mit den vielen Löchern (Bauteil 2)."),
                      ("die Mikrocontroller-Platine Arduino Uno", True, None),
                      ("ein Netzteil", False, "Den Strom liefert hier das USB-Kabel vom Computer, ein Netzteil ist nicht abgebildet."),
                      ("eine Grafikkarte", False, "Die Platine trägt einen Mikrocontroller, der Programme ausführt, keine Grafikkarte."),
                    ]),
               dict(q="Wofür steht der Anschluss GND am Arduino?",
                    done="Genau, GND ist der Minuspol mit 0 V.",
                    opts=[
                      ("für den Pluspol mit 5 Volt", False, "Der Pluspol heißt am Arduino 5V."),
                      ("für einen Datenanschluss zum Internet", False, "GND hat nichts mit Daten zu tun, es ist ein Pol des Stromkreises."),
                      ("für ground (Erde/Masse): den Minuspol mit 0 V, wie EARTH am Makey Makey", True, None),
                      ("für einen Ein-/Ausschalter", False, "Der Arduino hat keinen GND-Schalter, GND ist der Bezugspunkt mit 0 V."),
                    ]),
               dict(q="Wie erkennst du an einer LED den Pluspol (Anode)?",
                    done="Stimmt, das lange Beinchen ist die Anode.",
                    opts=[
                      ("an der Farbe des Gehäuses", False, "Die Gehäusefarbe zeigt die Leuchtfarbe, nicht die Polung."),
                      ("am kurzen Beinchen", False, "Das kurze Beinchen ist die Kathode (−), sie zeigt Richtung GND."),
                      ("gar nicht, die Richtung ist egal", False, "Eine LED lässt Strom nur in eine Richtung durch, die Polung ist wichtig."),
                      ("am langen Beinchen, es zeigt Richtung 5V", True, None),
                    ]),
               dict(q="Wozu dient der 220-Ω-Widerstand vor der LED?",
                    done="Richtig, er begrenzt den Strom und schützt die LED.",
                    opts=[
                      ("Er begrenzt die Stromstärke, damit die LED nicht durchbrennt.", True, None),
                      ("Er macht die LED heller.", False, "Ein Widerstand begrenzt den Strom, er verstärkt ihn nicht."),
                      ("Er speichert Strom für später.", False, "Speichern kann ein Akku oder Kondensator, kein Widerstand."),
                      ("Er bestimmt die Farbe der LED.", False, "Die Farbe hängt von der LED selbst ab, nicht vom Widerstand."),
                    ]),
               dict(q="In welche Richtung fließen die Elektronen in einem geschlossenen Stromkreis?",
                    done="Genau, vom Elektronenüberschuss (−) zum Elektronenmangel (+).",
                    opts=[
                      ("vom Pluspol zum Minuspol", False, "Das ist die technische Stromrichtung, die festgelegt wurde, bevor man Elektronen kannte."),
                      ("vom Minuspol (Überschuss) zum Pluspol (Mangel)", True, None),
                      ("abwechselnd in beide Richtungen", False, "Am Arduino fließt Gleichstrom, also immer in dieselbe Richtung."),
                      ("gar nicht, sie bleiben stehen", False, "In einem geschlossenen Kreis fließen die Elektronen, deshalb leuchtet die LED."),
                    ]),
               dict(q="Welche Löcher des Steckbretts sind innen leitend miteinander verbunden?",
                    done="Stimmt, die fünf Löcher einer Spalte (a–e bzw. f–j).",
                    opts=[
                      ("alle Löcher des ganzen Bretts", False, "Dann wäre jede Schaltung kurzgeschlossen."),
                      ("die Löcher einer Zeile, z. B. a1 bis a30", False, "Waagerecht verbunden sind nur die Plus- und Minusschienen am Rand."),
                      ("die fünf Löcher einer Spalte, z. B. a1 bis e1", True, None),
                      ("gar keine, man muss löten", False, "Gerade das Steckbrett macht Löten überflüssig."),
                    ]),
               dict(fig="schaltungen-A-D", cap="Fehlersuche · Schaltungen A bis D (Lupe: LED-Beinchen und Widerstand)",
                    q="Nur eine der vier Schaltungen ist richtig aufgebaut. Welche?",
                    done="Richtig, B: Vorwiderstand mit rot-rot-braun (220 Ω), langes geknicktes Anodenbein Richtung 5V.",
                    opts=[
                      ("Schaltung A", False, "Schau in die Lupe: Wo ist der Widerstand? Das rote Kabel geht direkt an die Anode."),
                      ("Schaltung B", True, None),
                      ("Schaltung C", False, "Vergleiche die Farbringe: Der dritte Ring ist gelb statt braun."),
                      ("Schaltung D", False, "Achte auf das geknickte, lange Beinchen: Es zeigt hier Richtung GND."),
                    ]),
               dict(q="Was passiert in Schaltung C (Farbringe rot-rot-gelb)?",
                    done="Genau, 220 kΩ = 220 000 Ω lassen nur etwa 0,014 mA durch, die LED bleibt praktisch dunkel.",
                    opts=[
                      ("Die LED brennt sofort durch.", False, "Das droht ohne Widerstand (Schaltung A). Hier ist der Widerstand viel zu groß, nicht zu klein."),
                      ("Die LED leuchtet heller als in Schaltung B.", False, "Ein größerer Widerstand lässt weniger Strom durch, nicht mehr."),
                      ("Die LED bleibt (fast) dunkel, weil 220 kΩ den Strom tausendmal stärker begrenzen.", True, None),
                      ("Die LED blinkt.", False, "Blinken braucht ein Programm (Sketch), das kommt erst später."),
                    ]),
               dict(q="Warum leuchtet die LED in Schaltung D nicht?",
                    done="Richtig, die LED ist falsch herum eingesteckt und sperrt.",
                    opts=[
                      ("Weil der Widerstand falsch herum steckt.", False, "Beim Widerstand ist die Einbaurichtung egal."),
                      ("Weil das schwarze Kabel an 5V statt an GND steckt.", False, "Das schwarze Kabel steckt richtig an GND."),
                      ("Weil der Stromkreis über den Mittelgraben unterbrochen ist.", False, "Die LED-Beinchen überbrücken den Graben, der Kreis ist geschlossen."),
                      ("Weil die LED falsch gepolt ist: Die Anode (langes, geknicktes Bein) zeigt Richtung GND.", True, None),
                    ]),
             ],
             solution=["Aufgabe 1 (Abbildung 1): (1) Mikrocontroller-Platine Arduino Uno, (2) Steckbrett (Breadboard), (3) Widerstand (Vorwiderstand, 220 Ω), (4) LED (Leuchtdiode).",
                       "Aufgabe 2: 5V → rotes Kabel → a6 → Widerstand (b6–b2) → Anode e2 (langes Beinchen) → LED → Kathode e1 (kurzes Beinchen) → a1 → schwarzes Kabel → GND. Ist der Kreis offen oder die LED verdreht eingesteckt, leuchtet sie nicht.",
                       "Aufgabe 3 (Ergebnissicherung/Leistungsnachweis): beschriftetes Foto der leuchtenden Schaltung mit Arduino, Steckbrett, Widerstand, LED, 5V, GND, Anode und Kathode im Classroom.",
                       "Aufgabe 4 a) Vertiefung: Motor mit Propeller: läuft in beiden Richtungen, Umpolen kehrt die Drehrichtung um; kein 220-Ω-Widerstand, sonst bekommt er zu wenig Strom und läuft nicht an. Buzzer (aktiv): hat eine Polung („+“ bzw. langes Bein an 5V), piept nur richtig herum; er braucht keinen Vorwiderstand, mit 220 Ω piept er leiser. Ein passiver Buzzer bleibt an 5V stumm, er braucht ein Tonsignal aus einem Sketch. Tastschalter: keine Polung; in Reihe in den LED-Kreis (z. B. zwischen Widerstand und Anode) leuchtet die LED nur, solange er gedrückt ist.",
                       "Aufgabe 4 b) Vertiefung: U<sub>R</sub> = 5 V − 2 V = 3 V; R = 3 V / 20 mA = 150 Ω (nächster Normwert 150 Ω). Mit 220 Ω fließen 3 V / 220 Ω ≈ 13,6 mA, sicher unter 20 mA. Parallel (jede LED mit eigenem 220-Ω-Widerstand an 5V und GND) leuchten alle so hell wie eine einzelne LED, zusammen fließen etwa 41 mA. In Reihe teilen sich die 5 V auf: Zwei LEDs brauchen 4 V, es bleibt 1 V für den Widerstand (mit 220 Ω nur ≈ 4,5 mA, schwach); drei LEDs bräuchten 6 V, sie bleiben dunkel.",
                       "Fehlersuche (Schaltungen A–D): B ist richtig. A: kein Schutzwiderstand, die LED brennt durch. C: 220 kΩ (rot-rot-gelb) statt 220 Ω, die LED bleibt dunkel. D: LED falsch gepolt, sie sperrt."],
             solution_figs=[dict(fig="abb2-schaltkreis-loesung", cap="Lösung · Abbildung 2 mit LED, Widerstand und Kabeln"),
                            dict(fig="foto-aufbau-echt.jpg", cap="Abgleich · So sieht der Aufbau am echten Arduino aus")]),
        dict(no=6, sjw=6, kind="lernpfad", title="Arduino: Einführung in Tinkercad (die Ampel)",
             goal="Du planst eine Ampelschaltung mit Arduino, LEDs und Widerständen, konstruierst sie digital in Tinkercad und programmierst den Ampelzyklus mit Codeblöcken, die Tinkercad in C++ übersetzt.",
             # Quelle Arbeits-/Lösungsblatt: <Lektion>/Tutory/Typst/06 Arduino - Einführung in Tinkercad – Vorlage.typ (2 S. + Vertiefungsseite)
             # (gestrafft aus dem Arbeitsblatt des Praxissemesterstudenten), Bilder: plickers/fig1.png, fig2.png
             material=(
               "<p><b>Vom Stecken zum Programmieren.</b> In LP05 hat deine LED direkt an 5V und GND geleuchtet, also immer. Steckt sie stattdessen an einem <b>Digitalpin</b> (0–13), kann ein Programm sie schalten: <b>HOCH</b> (engl. <code>HIGH</code>) legt 5 V an, die LED leuchtet, <b>NIEDRIG</b> (<code>LOW</code>) legt 0 V an, sie ist aus. Jede LED braucht weiterhin ihren eigenen 220-Ω-Vorwiderstand, die kurzen Beinchen (Kathoden) führen zu GND.</p>"
               "<p><b>Tinkercad Circuits</b> ist ein kostenloser Simulator im Browser. Du ziehst Arduino, Steckbrett, LEDs und Widerstände aus der Komponenten-Bibliothek auf die Arbeitsfläche, verbindest sie mit Kabeln und startest die Simulation. Nichts kann kaputtgehen, und du siehst sofort, ob dein Programm funktioniert.</p>"
               "<p><b>Codeblöcke und C++.</b> Programmiert wird mit Blöcken, die an Scratch erinnern. Tinkercad übersetzt sie automatisch in die Sprache C++, die der echte Arduino versteht (Ansicht „Text“). Der Block „für immer“ heißt in C++ <code>void loop()</code> und wird endlos wiederholt, „Anschluss 13 auf HOCH einstellen“ wird zu <code>digitalWrite(13, HIGH);</code> und „3 Sekunden warten“ zu <code>delay(3000);</code>.</p>"
               "<p><b>Der Ampelzyklus</b> in Deutschland: <b>Rot</b> → <b>Rot-Gelb</b> (gleich wird es Grün) → <b>Grün</b> → <b>Gelb</b> (gleich wird es Rot) → wieder Rot. Jede Phase besteht im Programm aus zwei Schritten: alle drei Lampen einstellen und dann warten. Eine Lampe bleibt so lange an, bis du sie ausdrücklich auf NIEDRIG stellst.</p>"),
             tasks=["<b>Zeichne</b> den Ablauf einer Ampelphase, indem du die leuchtenden Lampen ausmalst (Aufgabe 1). Deine Skizze ist später dein Bauplan für das Programm.",
                    "<b>Benenne</b> die vier markierten Bestandteile von Tinkercad (Bild 1, Aufgabe 2) und der Codeblöcke (Bild 2, Aufgabe 3) und <b>ordne</b> den Blöcken ihren C++-Befehl zu.",
                    "<b>Baue</b> in Tinkercad eine Ampel aus Arduino, Steckbrett und drei LEDs (rot, gelb, grün), jede mit Vorwiderstand. <b>Programmiere</b> sie mit Codeblöcken so, dass sie den Ampelzyklus aus Aufgabe 1 endlos anzeigt, und <b>überprüfe</b> sie mit der Simulation (Aufgabe 4).",
                    "<b>Sichere</b> deinen C++-Code im Classroom (siehe Leistungsnachweis unten, Aufgabe 5).",
                    "Vertiefung (Wahl, siehe unten, Vertiefungsblatt Aufgabe 6): Wartezeiten anpassen, Fußgängerampel, Fehlersuche."],
             task_figs=[dict(fig="06-bild1-tinkercad.png", cap="Bild 1 · Tinkercad: die wichtigsten Bestandteile"),
                        dict(fig="06-bild2-codebloecke.png", cap="Bild 2 · Die Codeblöcke")],
             tools=["tinker"],
             fast="Erweitere deine Ampel um eine Fußgängerampel, die nur Grün zeigt, solange die Autos Rot haben.",
             vertiefung=(
               "<p>Wähle eine oder mehrere Vertiefungen (Vertiefungsblatt, Aufgabe 6).</p>"
               "<h3>★ Wartezeiten wie im echten Verkehr</h3><p><b>Ändere</b> die Wartezeiten so, dass Grün doppelt so lange leuchtet wie Rot und die Übergänge Rot-Gelb und Gelb nur eine Sekunde dauern.</p>"
               "<h3>★★ Fußgängerampel</h3><p><b>Erweitere</b> deine Ampel um eine rote LED an Pin 10 und eine grüne an Pin 9. <b>Programmiere</b>, dass Fußgänger:innen nur Grün haben, solange die Autos Rot haben. Plane die Phasen zuerst in einer Tabelle mit je einer Spalte pro LED. Tipp: Eine kurze „Räumzeit“, in der alle Rot haben, macht die Kreuzung sicher.</p>"
               "<h3>★★★ Fehlersuche</h3><p>Dieser Code soll eine Ampel steuern. <b>Erkläre</b>, warum nach dem ersten Durchlauf alle Lampen dauerhaft leuchten, und <b>korrigiere</b> ihn.</p>"
               "<pre style=\"background:var(--panel-2);border:1px solid var(--line);border-radius:10px;padding:.7rem;overflow:auto\"><code>void loop() {\n  digitalWrite(13, HIGH); delay(3000);   // Rot\n  digitalWrite(12, HIGH); delay(1000);   // Rot-Gelb\n  digitalWrite(11, HIGH); delay(3000);   // Grün\n  digitalWrite(12, HIGH); delay(1000);   // Gelb\n}</code></pre>"
               "<style>.vertiefung h3{font-size:1rem;margin:1.1rem 0 .4rem;color:var(--key)}</style>"),
             sicherung=("💾 Leistungsnachweis · Ergebnissicherung",
                        "Stelle die Code-Ansicht von „Blöcke“ auf <b>„Text“</b>, <b>kopiere</b> den C++-Code in ein Google-Dokument oder <b>lade</b> ihn mit dem Pfeil als <b>.ino</b>-Datei herunter. "
                        "Benenne die Datei z. B. „06 Ampel Lena“ und <b>gib</b> sie im <b>Google Classroom</b> ab. Bewertet wird (je 20 %): Dateiname mit Bezug zur Stunde, dein Vorname, Textformat (.docx, .txt oder .ino), "
                        "alle vier Phasen in richtiger Reihenfolge, Zyklus läuft endlos ohne Dauerlicht und ohne Dunkelphase."),
             rlp=["RLP 2.2 · Algorithmen", "2.3 · Informatiksysteme", "neu · Simulation & Physical Computing"],
             quiz=[
               dict(fig="06-bild1-tinkercad.png", cap="Bild 1 · Tinkercad: die wichtigsten Bestandteile",
                    q="Was ist Teil 1 in Bild 1?", done="Richtig, auf der Arbeitsfläche baust du die Schaltung.",
                    opts=[("die Arbeitsfläche, auf der die Schaltung gebaut wird", True, None),
                          ("die Komponenten-Bibliothek", False, "Die Bibliothek mit den Bauteilen ist rechts (Teil 4)."),
                          ("der Code-Editor", False, "Der Code-Editor öffnet sich erst über die Schaltfläche „Code“ (Teil 2)."),
                          ("das Schaltbild (Schema)", False, "Das Schema ist eine eigene Ansicht oben rechts, hier ist die Bauansicht zu sehen.")]),
               dict(q="Was öffnet Teil 2 („Code“)?", done="Genau, dort programmierst du den Arduino.",
                    opts=[("die Liste aller Bauteile", False, "Die Bauteile findest du in der Komponenten-Bibliothek (Teil 4)."),
                          ("den Code-Editor mit den Codeblöcken für den Arduino", True, None),
                          ("die Simulation", False, "Die Simulation startet Teil 3."),
                          ("die Tinkercad-Startseite", False, "Dafür klickst du auf das Tinkercad-Logo oben links.")]),
               dict(q="Was passiert, wenn du Teil 3 anklickst?", done="Stimmt, der Arduino führt dein Programm virtuell aus.",
                    opts=[("Der Code wird auf den echten Arduino geladen.", False, "Tinkercad ist ein Simulator, zum echten Arduino kommt der Code erst in LP07."),
                          ("Die Schaltung wird gelöscht.", False, "Löschen geht mit dem Papierkorb in der Werkzeugleiste."),
                          ("Der Arduino führt das Programm virtuell aus (Simulation).", True, None),
                          ("Die Schaltung wird an andere geschickt.", False, "Das wäre „Senden an“ ganz rechts.")]),
               dict(q="Wozu dient Teil 4?", done="Richtig, aus der Bibliothek ziehst du die Bauteile.",
                    opts=[("Codeblöcke auswählen", False, "Codeblöcke gibt es erst im Code-Editor (Bild 2)."),
                          ("die Farbe der Kabel einstellen", False, "Die Kabelfarbe stellst du in der Werkzeugleiste oben ein."),
                          ("Fehlermeldungen anzeigen", False, "Teil 4 enthält Bauteile wie Widerstand, LED und Drucktaster."),
                          ("Bauteile wie LED, Widerstand und Arduino auf die Arbeitsfläche ziehen", True, None)]),
               dict(fig="06-bild2-codebloecke.png", cap="Bild 2 · Die Codeblöcke",
                    q="Was stellst du bei Teil 1 in Bild 2 ein?", done="Genau, in der Ansicht „Text“ siehst du den C++-Code.",
                    opts=[("die Ansicht: Blöcke, Blöcke + Text oder nur Text (C++)", True, None),
                          ("die Version des Arduino", False, "Das Board steht rechts („1 (Arduino Uno R3)“)."),
                          ("die Sprache von Tinkercad", False, "Die Sprache stellst du in deinem Profil ein."),
                          ("die Geschwindigkeit der Simulation", False, "Die Geschwindigkeit hängt von deinen Warten-Blöcken ab.")]),
               dict(q="In welcher Kategorie (Teil 2) findest du „Anschluss … auf HOCH einstellen“?", done="Richtig, eine LED ist ein Ausgang.",
                    opts=[("Eingang", False, "Eingänge lesen etwas ein, z. B. einen Taster. Eine LED gibt etwas aus."),
                          ("Ausgang", True, None),
                          ("Steuerung", False, "In „Steuerung“ stehen „für immer“, „warten“ und „falls“."),
                          ("Mathematik", False, "Dort stehen Rechen- und Vergleichsblöcke.")]),
               dict(q="Was bedeutet „für immer“ bei Teil 3?", done="Stimmt, in C++ heißt das loop().",
                    opts=[("Die Blöcke darin laufen genau einmal beim Start.", False, "Das wäre „beim Start“, in C++ setup()."),
                          ("Die Blöcke darin laufen nur, wenn eine Taste gedrückt wird.", False, "Dafür bräuchtest du einen Eingang und „falls“."),
                          ("Die Blöcke darin werden nie ausgeführt.", False, "Sie laufen sogar endlos."),
                          ("Die Blöcke darin wiederholen sich endlos, in C++ loop().", True, None)]),
               dict(q="Was erhältst du über Teil 4 (Pfeil nach unten)?", done="Richtig, die .ino-Datei öffnet die Arduino-Software.",
                    opts=[("den Code als .ino-Datei für die Arduino-Software", True, None),
                          ("ein Foto der Schaltung", False, "Ein Foto machst du mit einem Screenshot."),
                          ("eine PDF mit dem Schaltplan", False, "Den Schaltplan zeigt die Ansicht „Schema“."),
                          ("eine Kopie der Komponenten-Bibliothek", False, "Die Bibliothek bleibt in Tinkercad.")]),
               dict(fig="ampel-loesung", cap="Der Ampelzyklus",
                    q="Welche Phase folgt bei einer deutschen Ampel auf Grün?", done="Genau, Gelb kündigt Rot an.",
                    opts=[("Rot-Gelb", False, "Rot-Gelb kommt nach Rot und kündigt Grün an."),
                          ("Rot", False, "Direkt von Grün auf Rot wäre gefährlich, dazwischen kommt eine Phase."),
                          ("Gelb", True, None),
                          ("Grün blinkend", False, "Blinkendes Grün gibt es in Deutschland nicht.")]),
               dict(q="Ein Ampelprogramm stellt nie eine Lampe auf NIEDRIG. Was passiert?", done="Richtig, deshalb gehört zu jeder Phase: alle Lampen einstellen.",
                    opts=[("Die Lampen gehen nach dem Warten automatisch aus.", False, "Ein Pin bleibt HOCH, bis das Programm ihn auf NIEDRIG stellt."),
                          ("Nach dem ersten Durchlauf leuchten alle Lampen dauerhaft.", True, None),
                          ("Die Simulation stoppt mit einer Fehlermeldung.", False, "Der Code ist gültig, er tut nur nicht, was du willst."),
                          ("Die Ampel läuft trotzdem richtig.", False, "Probiere es in der Simulation aus: Alle Lampen bleiben an.")]),
             ],
             solution=["Aufgabe 1: Rot → Rot-Gelb → Grün → Gelb → wieder Rot. Rot-Gelb kündigt Grün an, Gelb allein kündigt Rot an.",
                       "Aufgabe 2 (Bild 1): (1) Arbeitsfläche, (2) Code, öffnet die Codeblöcke, (3) Simulation starten, (4) Komponenten-Bibliothek.",
                       "Aufgabe 3 (Bild 2): (1) Ansicht Blöcke / Blöcke + Text / Text, (2) Kategorien (Ausgang, Steuerung …), (3) Programm im Block „für immer“, (4) Code als .ino herunterladen. Zuordnung: für immer = <code>void loop() { … }</code>, Anschluss 13 auf HOCH = <code>digitalWrite(13, HIGH);</code>, 3 Sekunden warten = <code>delay(3000);</code>.",
                       "Aufgabe 4/5 (rot 13, gelb 12, grün 11): Rot = HOCH/NIEDRIG/NIEDRIG, 3 s · Rot-Gelb = HOCH/HOCH/NIEDRIG, 1 s · Grün = NIEDRIG/NIEDRIG/HOCH, 3 s · Gelb = NIEDRIG/HOCH/NIEDRIG, 1 s. <code>void setup() { pinMode(13, OUTPUT); pinMode(12, OUTPUT); pinMode(11, OUTPUT); }</code> und in <code>loop()</code> je Phase alle drei <code>digitalWrite</code> plus <code>delay</code>, z. B. Rot-Gelb: <code>digitalWrite(13, HIGH); digitalWrite(12, HIGH); digitalWrite(11, LOW); delay(1000);</code>",
                       "Aufgabe 6 Fußgängerampel: Autos grün + F-rot → Gelb + F-rot → Räumzeit alle rot → Autos rot + F-grün → Räumzeit → Rot-Gelb + F-rot. Fehlersuche: Keine Lampe wird je auf LOW gestellt, deshalb bleibt jede an. Vor Grün <code>digitalWrite(13, LOW); digitalWrite(12, LOW);</code>, vor Gelb <code>digitalWrite(11, LOW);</code>, am Ende von Gelb <code>digitalWrite(12, LOW);</code>."],
             solution_figs=[dict(fig="ampel-loesung", cap="Lösung · Ampelzyklus")]),
        dict(no=7, sjw=8, kind="lernpfad", title="Sensor-Projekte planen: ein Wächter mit Arduino",
             goal="Ihr wählt ein Sensor-Projekt (Gießwächter, Filterwächter oder Lüftungswächter), plant Bauteile, Struktogramm und Gehäuse, programmiert den Wächter in Tinkercad, übersetzt die Blöcke in C++ und prüft eure Ergebnisse Schritt für Schritt am Erwartungshorizont.",
             # Quelle: <Lektion>/Version 3/Tutory/Typst/07 Sensor-Projekte planen.typ + Erwartungshorizont-07 Sensor-Projekte planen.typ
             material=LP07_V3_MATERIAL,
             tasks=["<b>Aufgabe 1 · Bauteile und Materialien:</b> Tragt alle Bauteile ein, die ihr braucht, auch Kabel, Steckbrett und Gehäuse (Material / Typ / Wert, Anzahl, Anschluss am Arduino).",
                    "<b>Aufgabe 2 · Struktogramm:</b> Plant das Programm mit Anweisung, Verzweigung (wenn … dann … sonst) und Wiederholung (für immer), bevor ihr Blöcke setzt.",
                    "<b>Aufgabe 3 · Gehäuse vermessen:</b> Messt Arduino, Steckbrett und Sensor, rechnet Innen- und Außenmaß aus, plant die Öffnungen und baut das Gehäuse im Tinkercad-3D-Entwurf.",
                    "<b>Aufgabe 4 · Vom Block zur C++-Zeile:</b> Programmiert den Wächter in Tinkercad mit Blöcken, stellt auf „Blöcke + Text“ und tragt zu jedem Steuerelement Block und C++-Zeile ein.",
                    "<b>Prüfen:</b> Wählt unten euer Projekt und beantwortet zu jeder Aufgabe die Impulsfragen. Sind alle richtig, erscheint der Erwartungshorizont mit Bauplan: Vergleicht und verbessert euer Blatt."],
             stufen=LP07_V3_STUFEN,
             tools=["tinker", "tinker3d"],
             fast="Ergänzt eine gelbe LED als Vorwarnung mit zweitem Schwellenwert oder prägt den Namen eures Wächters in den Gehäusedeckel.",
             vertiefung=LP07_V3_VERTIEFUNG,
             sicherung=("💾 Leistungsnachweis 07 · Abgabe im Classroom (eine Abgabe pro Team)",
                        "<b>1.</b> Programm als <b>.ino</b>: in Tinkercad „Code“ › „Text“ › Herunterladen-Symbol. <b>2.</b> Gehäuse und Deckel als <b>.stl</b> aus dem 3D-Entwurf. "
                        "Dateiname: <code>Projekt-A_Name1_Name2.ino</code> bzw. <code>.stl</code>"),
             rlp=["RLP 2.1 · Modellieren", "2.2 · Algorithmen", "neu · Physical Computing & 3D-Druck"],
             solution=LP07_V3_LOESUNG),
        dict(no=8, sjw=9, kind="projekt", title="Sensor-Projekte bauen und testen: der Wächter am echten Arduino",
             goal="Ihr baut euren Wächter ins gedruckte Gehäuse, ersetzt im Code das Ersatzbauteil durch den echten Sensor, testet ihn live, legt den Schwellenwert begründet fest und dokumentiert das Projekt in einem Bericht.",
             # Quelle: <08 Sensor-Projekte bauen und testen>/Tutory/Typst/08 Sensor-Projekte bauen und testen.typ + <07 …>/Version 3/Tutory/Typst/07 Sensoren anschließen.typ
             material=LP08_V3_MATERIAL,
             tasks=LP08_V3_TASKS,
             tools=["upload", "tinker"],
             fast="Ergänzt einen Piezo-Summer, der bei Rot piept, oder eine gelbe LED als Vorwarnung.",
             vertiefung=LP08_V3_VERTIEFUNG,
             sicherung=("💾 Leistungsnachweis 08 · Abgabe im Classroom (eine Abgabe pro Team)",
                        "<b>1.</b> Projektbericht als <b>PDF</b> <b>2.</b> Galerie-Übersicht als <b>PDF</b>. Gern zusätzlich die Originaldateien (z. B. .docx, .pages, Canva-Link) und den endgültigen Code als <b>.ino</b>. "
                        "Bringt den Wächter zu Sitzung 09 fertig mit."),
             rlp=["RLP 2.4 · Umsetzen", "2.3 · Informatiksysteme", "2.6 Kommunizieren"],
             quiz=LP08_V3_QUIZ,
             solution=LP08_V3_LOESUNG),
        dict(no=9, sjw=10, kind="lernpfad", title="Sensor-Projekte: Galerie und Rückmeldung",
             goal="Ihr präsentiert euren Wächter im Gallery Walk, bewertet andere Projekte nach Funktion und Projektbericht und gebt eine wertschätzende, konkrete Rückmeldung.",
             # Quelle: <09 Sensor-Projekte Galerie>/Tutory/Typst/09 Sensor-Projekte Galerie.typ
             material=LP09_V3_MATERIAL,
             tasks=LP09_V3_TASKS,
             tools=[],
             fast="Plant eure Version 2: Welche drei Verbesserungen aus den Rückmeldekarten setzt ihr zuerst um, und wie?",
             sicherung=("💾 Ergebnissicherung 09",
                        "Gebt eure <b>Rückmeldekarten</b> an die besuchten Teams. Fotografiert eure erhaltenen Karten und ladet das Foto zusammen mit eurem <b>Fazit</b> (Aufgabe 4) im Classroom hoch."),
             rlp=["RLP 2.5 · Reflektieren", "2.6 Kommunizieren"],
             quiz=LP09_V3_QUIZ,
             solution=LP09_V3_LOESUNG),
      ]),
 dict(hj=1, num="03", title="Wie Computer zählen — Zahlensysteme",
      key="#ffc23d", key2="#e39a00", tint="rgba(255,194,61,0.10)",
      lps=[
        dict(no=11, sjw=11, kind="lernpfad", title="Dual- & Dezimalsystem: Bits und Bytes",
             goal="Du erklärst Stellenwertsysteme, benennst Dual- und Dezimalsystem und wandelst kleine Zahlen zwischen beiden um.",
             tasks=["Das abgebildete Zahlensystem benennen (Dual- vs. Dezimalsystem).",
                    "Stellenwerte des Dualsystems (1,2,4,8,16 …) an Beispielen anwenden.",
                    "Bit und Byte definieren: 1 Byte = 8 Bit = 256 Zustände."],
             tools=["bincalc"],
             fast="Zähle von 0 bis 31 im Dualsystem mit fünf „Finger-Bits“ deiner Hand.",
             rlp=["RLP 2.1 · Modellieren", "3.5 Daten & Codierung", "neu · Zahlensysteme"],
             solution=["Dezimalsystem = Basis 10 (Ziffern 0–9), Dualsystem = Basis 2 (0/1).",
                       "Beispiel: 1101₂ = 8+4+0+1 = 13₁₀.",
                       "8 Bit ergeben 2⁸ = 256 mögliche Werte (0–255)."]),
        dict(no=12, sjw=12, kind="lernpfad", title="Umrechnen: Dezimal ↔ Dual ↔ Hexadezimal",
             goal="Du wendest Umwandlungs-Algorithmen an (Divisionsverfahren, Stellenwerte) und wechselst zwischen Dezimal-, Dual- und Hexadezimalsystem.",
             tasks=["Dezimal → Dual per fortgesetzter Division durch 2 (Rest notieren).",
                    "Dual → Hexadezimal per 4er-Gruppen (Nibble).",
                    "Übung „System (dual-hexadezimal)“ und Selbstkontrolle."],
             tools=["bincalc"],
             fast="Wandle deinen Geburtstag (TT.MM) ins Hexadezimalsystem um und wieder zurück.",
             rlp=["RLP 2.2 · Algorithmen", "3.5 Codierung"],
             solution=["Dezimal→Dual: fortlaufend durch 2 teilen, Reste rückwärts lesen.",
                       "Je 4 Dualstellen = 1 Hexziffer (0000=0 … 1111=F).",
                       "Beispiel: 2C₁₆ = 0010 1100₂ = 44₁₀."]),
        dict(no=13, sjw=13, kind="lernpfad", title="Rechnen im Dualsystem & negative Zahlen",
             goal="Du addierst im Dualsystem und lernst, wie negative Zahlen im Zweierkomplement dargestellt werden.",
             tasks=["Zwei Dualzahlen schriftlich addieren (Übertrag beachten).",
                    "Zweierkomplement bilden: invertieren + 1 addieren.",
                    "Warum kennt der Computer kein Minuszeichen? — begründen."],
             tools=["bincalc"],
             fast="Zeige, dass im 4-Bit-Zweierkomplement 0101 + 1011 = 0000 ergibt (also 5 + (−5) = 0).",
             rlp=["RLP 2.2 · Algorithmen", "3.5 Codierung", "neu · Zweierkomplement"],
             solution=["Dualaddition wie im Dezimalsystem, Übertrag bei 1+1=10.",
                       "Zweierkomplement: alle Bits kippen, dann +1 → das ist die negative Zahl.",
                       "So funktioniert Subtraktion als Addition — nur 0 und 1 nötig."]),
        dict(no=14, sjw=14, kind="lernpfad", title="Vertiefung: Zahlensystem-Challenge + Backup",
             goal="Vertiefung: Wettkampf-Aufgaben zu Zahlensystemen, Aufholen von Rückständen und gemeinsame Ergebnissicherung vor den Weihnachtsferien.",
             tasks=["Stationen-Challenge: Umrechnen auf Zeit (dezimal/dual/hex).",
                    "Offene Fragen aus Einheit 03 klären, Sterne aktualisieren.",
                    "HJ1-Zwischenstand sichern (alle Dateien ins Backup)."],
             tools=[],
             fast="Erstelle drei knifflige Umrechnungsaufgaben mit Lösung für die Mitschüler:innen.",
             rlp=["RLP 2.5 · Reflektieren"],
             solution=["Diese Stunde vertieft die Zahlensysteme (Sonderveranstaltung/Aufholen).",
                       "Ziel: sichere Beherrschung der Umrechnungen + vollständiges Backup."]),
      ]),
 dict(hj=1, num="04", title="Von Blöcken zu Zeilen — Python-Einstieg",
      key="#ff5db8", key2="#e0338f", tint="rgba(255,93,184,0.10)",
      lps=[
        dict(no=15, sjw=15, kind="lernpfad", title="Warum Python? + WebTigerJython-Oberfläche",
             goal="Du begründest, warum Python so verbreitet ist (Filmeffekte, KI, riesige Bibliotheken) und findest dich in WebTigerJython zurecht: Editor, Konsole, Zeichenfläche.",
             tasks=["Argumente für Python sammeln (z. B. Interstellar-Blackhole, KI-Systeme großer Firmen).",
                    "Bereiche von WebTigerJython zuordnen: Editor, Konsole, Zeichenfläche.",
                    "Erstes <code>print(\"Hallo Welt\")</code> ausführen und den Unterschied Block↔Syntax spüren."],
             tools=["wtj"],
             fast="Vergleiche ein „Hello World“ in Scratch und in Python — was ist gleich, was anders?",
             rlp=["RLP 2.3 · Sprachen", "3.6 Textbasierte Programmierung", "neu · Python"],
             solution=["Python ist einsteigerfreundlich (klare Struktur) und hat riesige Bibliotheken → schnelle Entwicklung, auch für KI.",
                       "Reihenfolge: Editor (Code), Konsole (Ausgaben/Fehler), Zeichenfläche (Turtle-Grafik).",
                       "Anders als Scratch tippt man Befehle als Text (Syntax)."]),
        dict(no=16, sjw=16, kind="lernpfad", title="Erste Turtle-Programme: Vierecke & Dreiecke",
             goal="Du steuerst die Turtle mit <code>makeTurtle()</code>, <code>forward()</code>, <code>right()</code> und zeichnest erste geometrische Figuren.",
             tasks=["Turtle erzeugen und ein Quadrat zeichnen (4× vorwärts + 90° drehen).",
                    "Ein Dreieck zeichnen (Außenwinkel 120°) — den Winkel begründen.",
                    "Ergebnis dem richtigen Code zuordnen (Dreieck/Viereck/zwei Figuren)."],
             tools=["wtj"],
             fast="Zeichne mit einer Schleife ein regelmäßiges Sechseck und finde die Formel für den Drehwinkel (360°/n).",
             rlp=["RLP 2.2 · Algorithmen", "3.6 Turtle-Grafik"],
             solution=["Quadrat: <code>repeat 4: forward(100); right(90)</code>.",
                       "Dreieck: Außenwinkel 120°, da 360°/3 = 120°.",
                       "Drehwinkel eines n-Ecks = 360° / n."]),
        dict(no=17, sjw=17, kind="lernpfad", title="Punkte, Positionen & Farben",
             goal="Du positionierst die Turtle mit <code>setPos()</code>, zeichnest Punkte in wählbarer Dicke (<code>dot()</code>) und setzt Farben ein.",
             tasks=["Turtle mit <code>setPos(x, y)</code> gezielt platzieren.",
                    "Punkte unterschiedlicher Dicke und Farbe setzen.",
                    "Odd-one-out: Von drei Codes finden, welcher nicht funktioniert — und warum."],
             tools=["wtj"],
             fast="Zeichne ein Koordinatenkreuz mit beschrifteten Punkten bei (0,0), (100,0), (0,100).",
             rlp=["RLP 2.2 · Algorithmen", "3.6 Koordinaten & Farbe"],
             solution=["<code>setPos(x,y)</code> springt zur Position, ohne zu zeichnen (Stift ggf. heben).",
                       "<code>dot(size)</code> zeichnet gefüllte Punkte; Farbe über <code>setPenColor()</code>/<code>setColor()</code>.",
                       "Der fehlerhafte Code vergisst meist <code>makeTurtle()</code> oder eine Klammer."]),
        dict(no=18, sjw=18, kind="lernpfad", title="Halbjahres-Check: vom Block zum Syntax-Code",
             goal="Du reflektierst den Übergang von blockbasiert zu textbasiert, sicherst deine HJ1-Ergebnisse und bereitest den Grafik-Schwerpunkt in HJ2 vor.",
             tasks=["Ein Scratch-Konzept (Schleife) in Python-Syntax übersetzen.",
                    "Selbsteinschätzung aller HJ1-Lernpfade aktualisieren.",
                    "Sammel-Backup HJ1 anlegen (alle .sb3, .ino, .py, Docs)."],
             tools=["wtj", "scratch"],
             fast="Schreibe eine Mini-Anleitung „Von Scratch zu Python in 5 Sätzen“ für den nächsten Jahrgang.",
             rlp=["RLP 2.5 · Reflektieren", "2.6 Kommunizieren"],
             solution=["Scratch „wiederhole 4“ → Python <code>for i in range(4):</code>.",
                       "Kernübergang: Blöcke ziehen → Befehle präzise tippen (Syntax zählt).",
                       "Vollständiges HJ1-Backup ist Voraussetzung für HJ2."]),
      ]),
 # =================== HALBJAHR 2 ===================
 dict(hj=2, num="05", title="Computergrafik mit Python (WebTigerJython)",
      key="#35e0ff", key2="#0bb7e0", tint="rgba(53,224,255,0.09)",
      lps=[
        dict(no=19, sjw=19, kind="lernpfad", title="Flaggen zeichnen: Rechtecke & Füllfarben",
             goal="Du strukturierst ein Python-Programm sauber und zeichnest Länderflaggen aus gefüllten Rechtecken.",
             tasks=["Ein Rechteck als Funktion/Baustein zeichnen und füllen.",
                    "Eine drei­streifige Flagge (z. B. Frankreich/Deutschland) programmieren.",
                    "Farben und Maße als Variablen auslagern (leicht änderbar)."],
             tools=["wtj"],
             fast="Programmiere eine Flagge mit Kreis oder Stern (z. B. Japan) und sichere sie als Bild.",
             rlp=["RLP 2.4 · Umsetzen", "3.6 Grafik & Struktur"],
             solution=["Wiederkehrende Formen in Funktionen kapseln (z. B. <code>def balken(...)</code>).",
                       "Füllen mit <code>startPath()/fill()</code> bzw. <code>fillToPoint()</code>.",
                       "Variablen für Farbe/Breite machen die Flagge anpassbar."]),
        dict(no=20, sjw=20, kind="lernpfad", title="For-Schleifen I: Muster mit Zähler",
             goal="Du nutzt <code>for</code>-Schleifen mit <code>range()</code>, um Muster, Treppen und Sternenreihen effizient zu zeichnen.",
             tasks=["<code>for i in range(n)</code> verstehen (Zähler, Start/Ende/Schritt).",
                    "Eine Treppe aus n Stufen zeichnen.",
                    "Variablendeklaration und Wiederholschleife im Code benennen."],
             tools=["wtj"],
             fast="Zeichne einen Farbverlauf, indem du in jeder Iteration die Stiftfarbe leicht änderst.",
             rlp=["RLP 2.2 · Kontrollstrukturen", "3.6 Schleifen"],
             solution=["<code>range(n)</code> liefert 0,1,…,n−1; die Schleifenvariable zählt mit.",
                       "Treppe: pro Durchlauf ein Schritt nach rechts + nach oben.",
                       "Schleifen sparen Wiederholung und machen Code kurz & lesbar."]),
        dict(no=21, sjw=21, kind="lernpfad", title="For-Schleifen II: verschachtelte Schleifen",
             goal="Du verschachtelst Schleifen (Schleife in Schleife) und erzeugst Raster, Kacheln und Mandalas.",
             tasks=["Ein n×n-Punkteraster mit zwei geschachtelten Schleifen zeichnen.",
                    "Ein Mandala aus rotierten Figuren (z. B. 12× ein Quadrat, je 30° gedreht) erstellen.",
                    "Innere vs. äußere Schleife erklären."],
             tools=["wtj"],
             fast="Erzeuge ein Schachbrettmuster mit abwechselnden Farben über eine Bedingung in der inneren Schleife.",
             rlp=["RLP 2.2 · Kontrollstrukturen", "3.6 Verschachtelung"],
             solution=["Äußere Schleife = Zeilen, innere = Spalten (bzw. Rotation).",
                       "Mandala: <code>for k in range(12): quadrat(); right(30)</code>.",
                       "Die innere Schleife läuft bei jedem äußeren Durchlauf komplett durch."]),
        dict(no=22, sjw=22, kind="lernpfad", title="While-Schleifen & Bedingungen",
             goal="Du unterscheidest <code>for</code> und <code>while</code> und wiederholst Code, bis eine Bedingung erfüllt ist.",
             tasks=["Eine <code>while</code>-Schleife mit Abbruchbedingung schreiben.",
                    "Eine Spirale zeichnen, die wächst, bis sie den Rand erreicht.",
                    "Endlosschleifen erkennen und vermeiden (Zähler/Abbruch)."],
             tools=["wtj"],
             fast="Baue eine Spirale, deren Schrittlänge in jedem Durchgang um 2 wächst — bis Länge > 200.",
             rlp=["RLP 2.2 · Kontrollstrukturen", "3.6 Bedingte Wiederholung"],
             solution=["<code>for</code> = feste Anzahl; <code>while</code> = solange Bedingung wahr ist.",
                       "Spirale: Länge in jedem Schritt erhöhen, Abbruch bei Grenze.",
                       "Ohne veränderliche Bedingung → Endlosschleife (vermeiden)."]),
        dict(no=23, sjw=23, kind="lernpfad", title="Raster- vs. Vektorgrafik: Pixel oder Formel?",
             goal="Du unterscheidest Raster- und Vektorgrafik, erklärst Vor-/Nachteile und ordnest Dateiformate zu. (Kurzwoche: Frauentag)",
             tasks=["Rastergrafik (Pixel) vs. Vektorgrafik (Formen/Formeln) gegenüberstellen.",
                    "Zoom-Test: Warum werden Fotos pixelig, Vektoren aber nicht?",
                    "Formate zuordnen: JPG/PNG (Raster) vs. SVG (Vektor)."],
             tools=["wtj"],
             fast="Zeichne dieselbe Form als Turtle-Vektor und beschreibe, wie sie als Pixelbild gespeichert würde.",
             rlp=["RLP 2.1 · Modellieren", "3.5 Digitale Bilder", "neu · Raster/Vektor"],
             solution=["Rastergrafik = Gitter aus Pixeln (auflösungsabhängig, wird beim Zoom pixelig).",
                       "Vektorgrafik = mathematische Formen (verlustfrei skalierbar).",
                       "JPG/PNG = Raster, SVG = Vektor."]),
        dict(no=24, sjw=24, kind="projekt", title="Grafik-Projekt + Ergebnissicherung",
             goal="Du planst und programmierst eine eigene Computergrafik (Landschaft, Muster, Logo), dokumentierst deinen Code und sicherst das Ergebnis.",
             tasks=["Motiv wählen und in Bausteine (Funktionen) zerlegen.",
                    "Mit Schleifen & Variablen umsetzen, Code kommentieren.",
                    "Grafik + <code>.py</code>-Datei + kurze Doku sichern (lokal + Cloud)."],
             tools=["wtj"],
             fast="Mache dein Motiv per Variablen parametrisierbar (z. B. Anzahl/Farbe per einer Zeile änderbar).",
             rlp=["RLP 2.4 · Umsetzen", "2.6 Kommunizieren", "3.6 Projekt"],
             solution=["Bewertet: kreatives Motiv, sinnvolle Funktionen/Schleifen, Kommentare, Doku.",
                       "Ergebnissicherung reproduzierbar: .py + Bild + Beschreibung.",
                       "Backup an zwei Orten."]),
      ]),
 dict(hj=2, num="06", title="Datensicherheit & Kryptographie",
      key="#ff5d6c", key2="#e0333f", tint="rgba(255,93,108,0.10)",
      lps=[
        dict(no=25, sjw=25, kind="lernpfad", title="Passwörter & Kontosicherheit",
             goal="Du erklärst, was ein starkes Passwort ausmacht, warum jedes Konto ein eigenes braucht und wie Passwortmanager und Zwei-Faktor-Authentisierung schützen.",
             tasks=["Merkmale starker Passwörter (Länge, Zufälligkeit, Einzigartigkeit) sammeln.",
                    "Passwortstärke schätzen: warum Länge wichtiger ist als Sonderzeichen-Chaos.",
                    "2FA und Passwortmanager (z. B. KeePass, Bitwarden) einordnen."],
             tools=[],
             fast="Baue aus einem Merksatz eine lange Passphrase und erkläre, warum sie sicher UND merkbar ist.",
             rlp=["RLP 2.3 · Sicherheit", "3.7 Datensicherheit", "neu · Kryptographie"],
             solution=["Stark = lang, zufällig, für jedes Konto einzigartig.",
                       "Länge schlägt Komplexität: mehr Zeichen = exponentiell mehr Möglichkeiten.",
                       "Passwortmanager erzeugt/merkt sichere Passwörter; 2FA ergänzt „Wissen“ um „Besitz“."]),
        dict(no=26, sjw=26, kind="lernpfad", title="Verschlüsselung verstehen: Cäsar & Substitution",
             goal="Du ver- und entschlüsselst mit der Cäsar-Verschiebung und einer Substitutionschiffre und erkennst deren Schwächen (Häufigkeitsanalyse).",
             tasks=["Nachrichten mit Cäsar-Verschiebung (Schlüssel = Verschiebung) codieren.",
                    "Eine fremde Nachricht ohne Schlüssel knacken (Häufigkeitsanalyse).",
                    "Optional: die Verschiebung als kleines Python-Programm umsetzen."],
             tools=["wtj"],
             fast="Schreibe ein Python-Snippet, das einen Text um k Stellen verschiebt und wieder zurück.",
             rlp=["RLP 2.2 · Algorithmen", "3.7 Verschlüsselung"],
             solution=["Cäsar verschiebt jeden Buchstaben um k Stellen im Alphabet.",
                       "Schwäche: nur 25 Schlüssel bzw. Buchstabenhäufigkeit verrät die Zuordnung (e/n häufig).",
                       "Sicherheit darf nicht auf Geheimhaltung des Verfahrens beruhen (Kerckhoffs)."]),
        dict(no=27, sjw=27, kind="lernpfad", title="Symmetrisch vs. asymmetrisch: der Schlüsseltausch",
             goal="Du unterscheidest symmetrische und asymmetrische Verschlüsselung und erklärst das Prinzip von öffentlichem und privatem Schlüssel.",
             tasks=["Symmetrisch (ein geheimer Schlüssel) vs. asymmetrisch (Schlüsselpaar) gegenüberstellen.",
                    "Das Schlüsseltausch-Problem beschreiben und mit dem „Vorhängeschloss“ lösen.",
                    "Alltag: HTTPS-Schloss im Browser deuten."],
             tools=[],
             fast="Erkläre in eigenen Worten, warum man mit dem öffentlichen Schlüssel ver-, aber nur mit dem privaten entschlüsseln kann.",
             rlp=["RLP 2.1 · Modellieren", "3.7 Public-Key"],
             solution=["Symmetrisch: gleicher Schlüssel zum Ver-/Entschlüsseln (schnell, aber Austauschproblem).",
                       "Asymmetrisch: öffentlicher Schlüssel verschlüsselt, privater entschlüsselt.",
                       "HTTPS-Schloss = verschlüsselte, authentisierte Verbindung."]),
        dict(no=28, sjw=28, kind="lernpfad", title="Hashing & Integrität: der Fingerabdruck von Daten",
             goal="Du erklärst, was eine Hashfunktion ist, wozu Hashes dienen (Integrität, Passwortspeicherung) und warum Hashing keine Verschlüsselung ist.",
             tasks=["Eigenschaften einer Hashfunktion (Einweg, fixe Länge, Lawineneffekt) sammeln.",
                    "Kleine Änderung → völlig anderer Hash: an einem Beispiel zeigen.",
                    "Warum werden Passwörter gehasht (nicht im Klartext) gespeichert?"],
             tools=[],
             fast="Recherchiere, was ein „Salt“ ist und warum es Rainbow-Table-Angriffe erschwert.",
             rlp=["RLP 2.3 · Sicherheit", "3.7 Integrität", "neu · Hashing"],
             solution=["Hash = Einwegfunktion: aus Daten ein fixer „Fingerabdruck“, nicht umkehrbar.",
                       "Integrität: gleicher Hash ⇒ Datei unverändert.",
                       "Keine Verschlüsselung, da man den Ursprung nicht zurückrechnen kann."]),
        dict(no=29, sjw=29, kind="lernpfad", title="Datenschutz im Alltag: Metadaten & Grundrechte",
             goal="Du erkennst, welche Daten du täglich hinterlässt (Metadaten), kennst Grundideen der DSGVO und triffst bewusste Entscheidungen zur sicheren Kommunikation. (Kurzwoche: Himmelfahrt/Brückentag)",
             tasks=["Metadaten aufspüren (Foto-Standort, Zeitstempel, Absender).",
                    "DSGVO-Grundrechte nennen (Auskunft, Löschung, Datensparsamkeit).",
                    "Messenger vergleichen: Ende-zu-Ende-Verschlüsselung ja/nein?"],
             tools=[],
             fast="Erstelle eine „digitale Selbstverteidigung“-Checkliste mit fünf konkreten Tipps.",
             rlp=["RLP 2.5 · Bewerten", "3.7 Datenschutz/DSGVO"],
             solution=["Metadaten = Daten über Daten (wann/wo/von wem) — oft aussagekräftiger als gedacht.",
                       "DSGVO: Datensparsamkeit, Zweckbindung, Recht auf Auskunft/Löschung.",
                       "Ende-zu-Ende-Verschlüsselung schützt Inhalte auch vor dem Anbieter."]),
      ]),
 dict(hj=2, num="07", title="Eigene Software — Vibe-Coding & Hosting",
      key="#34ff9e", key2="#12c47a", tint="rgba(52,255,158,0.09)",
      lps=[
        dict(no=30, sjw=30, kind="lernpfad", title="Vibe-Coding verstehen: präzises Prompting",
             goal="Du verstehst „Vibe-Coding“ (Code per KI-Prompt statt selbst tippen) und lernst, was einen starken Prompt ausmacht: Format · Funktion · Design · Technik · Kontext.",
             tasks=["Prompt-Anatomie an einem Beispiel (Pomodoro-Timer) analysieren.",
                    "Referenz-Tools ansehen: Verb-Trainer und chemical_communication_trainer.",
                    "Einen eigenen Beispielprompt für eine einfache Web-App entwerfen."],
             tools=["ref"],
             fast="Verbessere einen schwachen Prompt in drei Schritten und erkläre, was jede Ergänzung bewirkt.",
             rlp=["RLP 2.4 · Umsetzen", "3.8 KI & Werkzeuge", "neu · Prompting"],
             solution=["Vibe-Coding: eine KI (Claude/ChatGPT/Gemini) schreibt den Code, die Qualität hängt vom Prompt ab.",
                       "Starker Prompt = Format (standalone .html) + Funktion + Design + Technik + Kontext.",
                       "Je präziser die Anweisung, desto brauchbarer das Ergebnis."]),
        dict(no=31, sjw=31, kind="lernpfad", title="Themenwahl & KI-Recherche: Kurzvortrag ODER App",
             goal="Du wählst dein Projekt: (a) einen Kurzvortrag mit Schwerpunkt KI-Recherche und Produkterstellung durch präzises Prompting ODER (b) eine eigene .html-Anwendung. (Kurzwoche: Pfingsten)",
             tasks=["Anwendungsfall/Thema festlegen und eingrenzen.",
                    "Für (a): mit KI recherchieren und ein Produkt/Ergebnis präzise erzeugen.",
                    "Für (b): Funktion, Design und Technik der geplanten App skizzieren."],
             tools=["ref"],
             fast="Formuliere zwei alternative Prompts für dieselbe Idee und begründe, welcher bessere Ergebnisse verspricht.",
             rlp=["RLP 2.1 · Planen", "3.8 Projektidee"],
             solution=["Gute Themen sind klein & klar abgegrenzt (eine Aufgabe, ein Bildschirm).",
                       "Kurzvortrag = KI-Recherche + präzise Produkterstellung; App = eigenes .html.",
                       "Kriterien für die Präsentation frühzeitig anschauen."]),
        dict(no=32, sjw=32, kind="lernpfad", title="Prototyp bauen mit jsfiddle.net",
             goal="Du erzeugst mit einer KI eine einseitige HTML-Anwendung, testest sie in jsfiddle.net und verbesserst sie iterativ.",
             tasks=["KI-generierten HTML-Code (von <code>&lt;!DOCTYPE html&gt;</code> bis <code>&lt;/html&gt;</code>) in jsfiddle einfügen.",
                    "Testen, Fehler zurück an die KI melden, gezielt nachbessern.",
                    "Zwischenstände sichern (Backup!)."],
             tools=["jsfiddle"],
             fast="Erweitere deine App um eine sinnvolle Zusatzfunktion — nur über einen präzisen Folgeprompt.",
             rlp=["RLP 2.4 · Umsetzen", "3.8 Web-App"],
             solution=["jsfiddle zeigt HTML/CSS/JS live — ideal zum schnellen Testen.",
                       "Iteration: testen → Fehler beschreiben → KI nachbessern lassen.",
                       "Funktioniert es lokal/hier, läuft es später auch auf GitHub."]),
        dict(no=33, sjw=33, kind="lernpfad", title="Auf GitHub veröffentlichen (GitHub Pages)",
             goal="Du legst einen GitHub-Account und ein Repository an, aktivierst GitHub Pages und teilst deine .html-Anwendung über eine öffentliche URL — komplett im Browser.",
             tasks=["Account anlegen, Repository <code>vibe-apps</code> (Public) mit README erstellen.",
                    "GitHub Pages aktivieren: Settings → Pages → Branch <code>main</code>, Ordner <code>/ (root)</code>.",
                    "Datei per „Add file → Upload files“ hochladen, committen, öffentliche URL testen & teilen."],
             tools=["github"],
             fast="Lade eine zweite Anwendung hoch und verlinke beide von einer kleinen <code>index.html</code>-Startseite.",
             rlp=["RLP 2.6 · Kommunizieren", "3.8 Hosting", "neu · GitHub Pages"],
             solution=["URL-Schema: <code>https://&lt;username&gt;.github.io/vibe-apps/deine-datei.html</code>.",
                       "GitHub Pages hostet statische Dateien kostenlos (1–2 Min. bis live).",
                       "Public-Repo nötig, damit andere die Seite öffnen können."]),
        dict(no=34, sjw=34, kind="lernpfad", title="Die eigene Implementierung verstehen (Folien + Sprechtext)",
             goal="Du untersuchst die für dich interessanteste Stelle im KI-geschriebenen Code deiner App und erstellst dazu eine ca. 5–6-seitige Präsentation mit Sprechtexten — nach dem Vorbild „Das VSEPR-Modell im Code“.",
             tasks=["Eine interessante Implementierung im Code auswählen (Algorithmus/Trick).",
                    "Analyse-Prompt nutzen: „Erstelle eine ca. 5–6-seitige Präsentation zur .html-Syntax und algorithmischen Struktur von … im … (Dateiname). Formuliere zu jeder Folie Sprechtexte.“",
                    "Folien + Sprechtexte prüfen, kürzen und einüben."],
             tools=["ref"],
             fast="Erkläre deine Lieblingsstelle in 60 Sekunden frei — ohne Folien, nur mit einer Skizze.",
             rlp=["RLP 2.5 · Analysieren", "2.6 Präsentieren", "3.8 Code-Verständnis"],
             solution=["Ziel: nicht alles, sondern EINE Stelle wirklich verstehen und erklären können.",
                       "Beispiel VSEPR: Datenmodell → atan2-Winkel → Repulsions-Relaxation (1/d²) → drawLP.",
                       "Sprechtext pro Folie ca. 45–75 s; Folienzahl ~5–6."]),
        dict(no=35, sjw=35, kind="lernpfad", title="Präsentationen: Kurzvorträge nach Kriterien",
             goal="Du präsentierst dein Projekt (Kurzvortrag oder App-Analyse) nach den vereinbarten Kriterien und gibst/erhältst konstruktives Feedback.",
             tasks=["Vortrag nach Kriterien halten (Inhalt, Struktur, Fachsprache, Medien, Zeit).",
                    "Peer-Feedback mit klaren Kriterien geben.",
                    "Aus dem Feedback zwei Verbesserungen für die Abgabe ableiten."],
             tools=[],
             fast="Übernimm die Moderation einer Präsentationsrunde und fasse jede Vorstellung in einem Satz zusammen.",
             rlp=["RLP 2.6 · Präsentieren", "3.8 Bewertungskriterien"],
             solution=["Kriterien z. B.: fachliche Richtigkeit, roter Faden, Fachsprache, Medieneinsatz, Zeit.",
                       "Feedback: konkret, wertschätzend, umsetzbar.",
                       "Nach der Runde: gezielt überarbeiten, dann abgeben."]),
        dict(no=36, sjw=36, kind="projekt", title="Abgabe, Backup & Ausblick",
             goal="Du gibst alle Ergebnisse sinnvoll und einfach wiederverwendbar ab, sicherst finale Backups und blickst auf Informatik in Klasse 10.",
             tasks=["Alle Ergebnisse gebündelt & benannt abgeben (App-Link, Folien, Sprechtexte, Code).",
                    "Finale Backups an zwei Orten prüfen (Rechner + Cloud/USB).",
                    "Jahresrückblick: Was kann ich jetzt? Ausblick auf Klasse 10."],
             tools=["github"],
             fast="Schreibe deinem „Ich zu Schuljahresbeginn“ einen kurzen Brief: Was kannst du jetzt, was vorher nicht?",
             rlp=["RLP 2.5 · Reflektieren", "2.6 Kommunizieren", "Ausblick Kl. 10"],
             solution=["„Sinnvoll abgeben“ = benannt, gebündelt, mit funktionierendem Link — von anderen nutzbar.",
                       "Ergebnissicherung ist selbstständig zu gewährleisten (zwei Backup-Orte).",
                       "Ausblick: vertiefte Programmierung, Daten & Projekte in Klasse 10."]),
      ]),
]

# ---------------------------------------------------------------- Hilfen
def slug(no):
    return "lp%02d" % no

def kind_badge(kind):
    return {"lernpfad":"Lernpfad","projekt":"Projekt"}.get(kind,"Lernpfad")

def unlock_iso(sjw):
    # Lösung wird am Freitag der jeweiligen Schuljahreswoche freigeschaltet
    return iso(CAL[sjw][1])

TOTAL_LP = sum(len(u["lps"]) for u in UNITS)

# ---------------------------------------------------------------- Ordnerstruktur (HJ/Einheit)
UNIT_OF_LP = {lp["no"]: u for u in UNITS for lp in u["lps"]}

def einheit_dirname(u):
    return "%s %s" % (u["num"], u["title"].replace(" — ", " - ").rstrip("?"))

def lp_dir_parts(no):
    u = UNIT_OF_LP[no]
    return ["lernpfade", "%dHJ" % u["hj"], einheit_dirname(u)]

def lp_out_dir(no):
    return os.path.join(BASE, *lp_dir_parts(no))

def lp_filename(no):
    # href relativ zu index.html: Pfadsegmente einzeln URL-kodieren
    parts = lp_dir_parts(no) + ["%s.html" % slug(no)]
    return "/".join(quote(p, safe="") for p in parts)

# ---------------------------------------------------------------- gemeinsame Fragmente
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?'
         'family=Orbitron:wght@600;700;800;900&'
         'family=Space+Grotesk:wght@400;500;600;700&'
         'family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">')

with open(os.path.join(ASSET_DIR, "theme.css"), encoding="utf-8") as f:
    THEME_CSS = f.read()
with open(os.path.join(ASSET_DIR, "theme.js"), encoding="utf-8") as f:
    THEME_JS = f.read()

def render_tags(rlp):
    out = []
    for t in rlp:
        cls = "tag"
        low = t.lower()
        if low.startswith("neu") or " neu" in low or low.startswith("puffer") or low.startswith("ausblick"):
            cls = "tag neu"
        elif t.startswith("RLP") or t[0:1].isdigit():
            cls = "tag rlp"
        out.append('<span class="%s">%s</span>' % (cls, esc(t)))
    return "".join(out)

def render_lp_tile(lp):
    mon, fri = CAL[lp["sjw"]]
    fast = ('<div class="lp-fast"><span class="fast-badge">⚡ Schnellläufer:in</span>'
            '<span>%s</span></div>' % lp["fast"]) if lp.get("fast") else ""
    return ('<article class="lp" data-unlock="%s">\n'
            '  <div class="lp-key"><div class="lp-week">SJW %d</div>'
            '<div class="lp-no">%02d</div><div class="lp-date">%s</div></div>\n'
            '  <div class="lp-info" data-selfcheck="%s">\n'
            '    <a class="lp-name" href="%s">%s <span class="lp-badge">%s</span> <span class="arrow">→</span></a>\n'
            '    <p class="lp-goal"><b>Das lernst du:</b> %s</p>\n'
            '    %s\n'
            '    <p class="lp-rlp">%s</p>\n'
            '  </div>\n'
            '</article>\n') % (
        unlock_iso(lp["sjw"]), lp["sjw"], lp["no"], dm(mon), slug(lp["no"]),
        lp_filename(lp["no"]), esc(lp["title"]), kind_badge(lp["kind"]),
        lp["goal"], fast, render_tags(lp["rlp"]))

def render_unit(u):
    g = ' g' if False else ''
    weeks = [lp["sjw"] for lp in u["lps"]]
    wlabel = "SJW %d–%d" % (min(weeks), max(weeks)) if len(weeks) > 1 else "SJW %d" % weeks[0]
    tiles = "".join(render_lp_tile(lp) for lp in u["lps"])
    style = "--key:%s;--key-2:%s;--tint:%s;" % (u["key"], u["key2"], u["tint"])
    return ('<article class="unit" style="%s">\n'
            '  <div class="unit-bar"><span class="unit-chip">%s</span>'
            '<h3>%s</h3><span class="unit-weeks">%d Lernpfade<br>%s</span></div>\n'
            '  <div class="unit-body">\n%s  </div>\n'
            '</article>\n') % (style, u["num"], esc(u["title"]), len(u["lps"]), wlabel, tiles)

def render_semester(hj):
    units = [u for u in UNITS if u["hj"] == hj]
    lps = [lp for u in units for lp in u["lps"]]
    first_sjw, last_sjw = lps[0]["sjw"], lps[-1]["sjw"]
    d1, d2 = CAL[first_sjw][0], CAL[last_sjw][1]
    badge_cls = "sem-head" if hj == 1 else "sem-head g"
    title = ("Boot — von Blöcken zu Bytes" if hj == 1
             else "Runtime — Python, Krypto & eigene Software")
    body_units = "".join(render_unit(u) for u in units)
    return ('<section class="sem-content%s" id="hj%d-content">\n'
            '  <div class="%s">\n'
            '    <div class="sem-badge">HJ%d</div>\n'
            '    <div><h2>%s</h2><p class="period">%d Lernpfade · %s – %s</p></div>\n'
            '  </div>\n%s\n'
            '</section>\n') % (
        (" active" if hj == 1 else ""), hj, badge_cls, hj, esc(title),
        len(lps), de(d1), de(d2), body_units)

# ---------------------------------------------------------------- index.html
def build_index():
    hero = '''
<canvas id="matrix-canvas"></canvas>
<header class="hero">
  <div class="hero-scan"></div>
  <div class="floaters" aria-hidden="true">
    <span class="f1">01</span><span class="f2">{ }</span><span class="f3">&lt;/&gt;</span><span class="f4">#!</span>
  </div>
  <div class="wrap">
    <div class="hero-meta">
      <span>PROFIL INFORMATIK · KLASSE 9</span>
      <span>BERLIN · SJ 2026/27 · <span class="on">SYS.UPTIME</span> <span id="sysclock">--:--:--</span></span>
    </div>
    <span class="hero-eyebrow"><span class="dot"></span> Profilkurs Informatik · 1 Std/Woche · 37 Lernpfade</span>
    <h1 class="hero-title">Vom <span class="g">Block</span> zum <span class="c">Byte</span> — und zur eigenen <span class="v">Software</span>.</h1>
    <p class="hero-lead">Ein Schuljahr, vier Missionen: Wir starten <b>blockbasiert</b> mit Scratch, Makey&nbsp;Makey &amp; Arduino, wechseln in die <b>Syntax von Python</b> und malen mit Code, entschlüsseln die Welt der <span class="hl">Datensicherheit &amp; Kryptographie</span> und bauen zum Schluss eigene <b>Web-Apps per Vibe-Coding</b> — live gehostet auf GitHub. Diese Seite ist deine <b>Kommandozentrale</b>: Landkarte, Übungs-Archiv und Fortschritts-Konsole in einem.</p>
  </div>
</header>
'''
    why = '''
<section class="section why">
  <div class="wrap">
    <p class="kicker">// warum dieser Kurs?</p>
    <h2>Wer <span class="u">programmieren versteht</span>, gestaltet die digitale Welt — statt sie nur zu bedienen.</h2>
    <div class="why-grid">
      <div class="why-card"><div class="ic">🧩</div><h3>Erst greifen, dann tippen</h3><p>Vom bunten Block zu echtem Code: Scratch, Makey&nbsp;Makey und Arduino machen Programmieren begreifbar — bevor Python die Syntax dazu liefert.</p></div>
      <div class="why-card"><div class="ic">🎨</div><h3>Code, der etwas macht</h3><p>Mit Python zeichnest du Grafiken, mit Krypto schützt du Daten, mit Vibe-Coding baust du echte Web-Apps. Immer mit sichtbarem Ergebnis.</p></div>
      <div class="why-card"><div class="ic">🛡️</div><h3>Sicher &amp; mündig</h3><p>Passwörter, Verschlüsselung, Hashing, Datenschutz: Du verstehst, wie deine Daten geschützt werden — und triffst bewusste Entscheidungen.</p></div>
      <div class="why-card"><div class="ic">🚀</div><h3>Für Schnellläufer:innen</h3><p>Zu jedem Lernpfad wartet eine Extra-Mission. Wer schneller ist, geht tiefer — Langeweile ist hier nicht vorgesehen.</p></div>
    </div>
  </div>
</section>
'''
    guide = '''
<section class="section guide">
  <div class="wrap">
    <h2>So funktioniert diese Konsole</h2>
    <p class="sub">// kurz erklärt — dann geht der Kernel an</p>
    <div class="guide-grid">
      <div class="guide-item"><div class="num">1</div><h4>Eine Woche = ein Lernpfad</h4><p><b>SJW</b> = Schuljahres-Woche. Jede Kursstunde ist ein Lernpfad mit Datum.</p></div>
      <div class="guide-item"><div class="num">2</div><h4>Antippen öffnet den Pfad</h4><p>Ein Klick auf einen Lernpfad öffnet Aufgaben, Werkzeuge und die Musterlösung.</p></div>
      <div class="guide-item"><div class="num">3</div><h4>Lösungen schalten sich frei</h4><p>Jede <b>Lernpfadlösung</b> wird automatisch an ihrem Datum freigeschaltet — die Seite prüft das bei jedem Laden.</p></div>
      <div class="guide-item"><div class="num">4</div><h4>Sterne sind dein Check</h4><p>Wie sicher fühlst du dich? Tippe Sterne an — dein Stand bleibt lokal gespeichert.</p></div>
    </div>
    <div class="legend">
      <span class="lg-title">// Legende</span>
      <span class="lg-item"><span class="lp-badge" style="--key:#35e0ff;background:#35e0ff;color:#05070e">Lernpfad</span> reguläre Stunde</span>
      <span class="lg-item"><span class="lp-badge" style="background:#34ff9e;color:#05070e">Projekt</span> Projekt &amp; Ergebnissicherung</span>
      <span class="lg-item">🔒 Lösung gesperrt · 🔓 freigeschaltet</span>
      <span class="lg-item"><span class="tag rlp">RLP</span> Bezug zum Rahmenlehrplan</span>
      <span class="lg-item"><span class="tag neu">neu</span> neu für diesen Kurs</span>
    </div>
  </div>
</section>
'''
    # Selector
    lp1 = [lp for u in UNITS if u["hj"] == 1 for lp in u["lps"]]
    lp2 = [lp for u in UNITS if u["hj"] == 2 for lp in u["lps"]]
    selector = '''
<section class="section selector">
  <div class="wrap">
    <h2>Wähle dein Halbjahr</h2>
    <p class="sub">// zwei Etappen · ein Schuljahr · {tot} Lernpfade · 8 Einheiten</p>
    <div class="sem-grid">
      <button class="sem-tile t1 active" data-sem="hj1">
        <div class="st-id">1. HALBJAHR · BOOT</div>
        <div class="st-title">Von Blöcken zu Bytes</div>
        <div class="st-meta"><span>{n1} Lernpfade</span><span>Aug 2026 – Jan 2027</span></div>
      </button>
      <button class="sem-tile t2" data-sem="hj2">
        <div class="st-id">2. HALBJAHR · RUNTIME</div>
        <div class="st-title">Python, Krypto &amp; eigene Software</div>
        <div class="st-meta"><span>{n2} Lernpfade</span><span>Feb – Jun 2027</span></div>
      </button>
    </div>
  </div>
</section>
'''.replace("{tot}", str(TOTAL_LP)).replace("{n1}", str(len(lp1))).replace("{n2}", str(len(lp2)))

    classroom = '''
<section class="section classroom">
  <div class="wrap">
    <h2>Material im Google Classroom</h2>
    <p class="sub">// Aufgaben, Dateien &amp; Ankündigungen zu deinem Kurs</p>
    <div class="classroom-grid">
      <a class="classroom-tile" href="https://classroom.google.com/u/0/c/ODcxNDA2NjU5MTcy" target="_blank" rel="noopener">
        <span class="ct-id">KURS InP2</span>
        <span class="ct-title">Zum Google Classroom <span class="ex">↗</span></span>
      </a>
      <a class="classroom-tile" href="https://classroom.google.com/u/0/c/ODcxNDA1MTA1NTY2" target="_blank" rel="noopener">
        <span class="ct-id">KURS InP4</span>
        <span class="ct-title">Zum Google Classroom <span class="ex">↗</span></span>
      </a>
    </div>
  </div>
</section>
'''
    footer = '''
<footer>
  <div class="foot-inner">
    <div>
      <b class="h">PROFIL INFORMATIK · KLASSE 9</b><br>
      Profilkurs · Schuljahr 2026/27<br>
      Berlin · 1 Std/Woche · 37 Lernpfade
    </div>
    <div>
      Unterrichtsreihen:<br>
      a) Blockbasiert (Scratch·Makey·Arduino) · b) Python &amp; Grafik<br>
      c) Datensicherheit &amp; Kryptographie · d) Vibe-Coding &amp; Hosting
    </div>
    <div>
      Aufbau:<br>
      2 Halbjahre · 8 Einheiten · Übersicht + Übungs-Archiv<br>
      Lösungen mit zeitlicher Freischaltung
    </div>
  </div>
</footer>
'''
    html_doc = (
        '<!DOCTYPE html>\n<html lang="de">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>Profil Informatik · Klasse 9 — Kursübersicht 2026/27</title>\n'
        + FONTS + '\n<style>\n' + THEME_CSS + '\n</style>\n</head>\n<body>\n'
        + hero + why + guide + selector
        + render_semester(1) + render_semester(2)
        + classroom
        + footer
        + '\n<script>\n' + THEME_JS + '\n</script>\n</body>\n</html>\n'
    )
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_doc)

# ---------------------------------------------------------------- Wissens-Check (Quiz)
def render_quiz(lp):
    quiz = lp.get("quiz")
    if not quiz:
        return ""
    items = ""
    for i, q in enumerate(quiz, 1):
        opts = ""
        for text, correct, hint in q["opts"]:
            attr = ' data-correct="true"' if correct else (' data-hint="%s"' % esc(hint) if hint else "")
            opts += '<button class="qz-opt"%s>%s</button>' % (attr, text)
        fig = ""
        if q.get("fig"):
            media = load_fig(lp["no"], q["fig"], q.get("cap", ""))
            if media:
                fig = '<div class="fig">%s<div class="fig-cap">%s</div></div>' % (media, esc(q.get("cap", "")))
        items += (
            '<div class="qz-item">%s'
            '<div class="qz-text"><span class="qn">%d.</span>%s</div>'
            '<div class="qz-opts">%s</div>'
            '<div class="qz-hint"></div><div class="qz-done">%s</div>'
            '</div>'
        ) % (fig, i, q["q"], opts, q.get("done", "Richtig!"))
    return (
        '<section class="lp-sec"><h2>Wissens-Check</h2>'
        '<div class="qz-wrap" data-qz>'
        '<div class="qz-progress"><span class="qz-count">0 / %d richtig</span>'
        '<span class="qz-bar"><span class="qz-fill"></span></span></div>'
        '%s'
        '<div class="qz-solved">✔ Stark — Wissens-Check komplett gelöst!</div>'
        '</div></section>'
    ) % (len(quiz), items)

# ---------------------------------------------------------------- Vorwissen (SVG-Figuren + Bild-Quiz)
def render_vorwissen(lp):
    vw = lp.get("vorwissen")
    if not vw:
        return ""
    blocks = ""
    for entry in vw:
        svg = load_svg(lp["no"], entry["fig"])
        if not svg:
            continue
        quiz = entry["quiz"]
        items = ""
        for i, q in enumerate(quiz, 1):
            opts = ""
            for text, correct, hint in q["opts"]:
                attr = ' data-correct="true"' if correct else (' data-hint="%s"' % esc(hint) if hint else "")
                opts += '<button class="qz-opt"%s>%s</button>' % (attr, text)
            items += (
                '<div class="qz-item">'
                '<div class="qz-text"><span class="qn">%d.</span>%s</div>'
                '<div class="qz-opts">%s</div>'
                '<div class="qz-hint"></div><div class="qz-done">%s</div>'
                '</div>'
            ) % (i, q["q"], opts, q.get("done", "Richtig!"))
        blocks += (
            '<div class="vw-block">'
            '<div class="fig">%s<div class="fig-cap">%s</div></div>'
            '<div class="qz-wrap" data-qz>'
            '<div class="qz-progress"><span class="qz-count">0 / %d richtig</span>'
            '<span class="qz-bar"><span class="qz-fill"></span></span></div>'
            '%s'
            '<div class="qz-solved">✔ Stark — %s komplett gelöst!</div>'
            '</div></div>'
        ) % (svg, esc(entry["cap"]), len(quiz), items, esc(entry["cap"].split("·")[0].strip()))
    if not blocks:
        return ""
    return (
        '<section class="lp-sec"><h2>Schau genau hin — was weißt du schon?</h2>'
        '<p class="vw-intro">Sieh dir die Bilder an. Zu jedem Bild gehören einige Fragen. '
        'Tippe die richtige Antwort an — wird sie grün, ist sie richtig. Bei rot bekommst du einen Tipp.</p>'
        '%s</section>'
    ) % blocks

# ---------------------------------------------------------------- Lernpfad-Seiten
def build_lp_page(u, lp):
    mon, fri = CAL[lp["sjw"]]
    style = "--key:%s;--key-2:%s;--tint:%s;" % (u["key"], u["key2"], u["tint"])
    tasks = "".join("<li>%s</li>" % t for t in lp["tasks"])
    tools = ""
    if lp["tools"]:
        items = ""
        for k in lp["tools"]:
            label, url = T[k]
            items += ('<a class="tool" href="%s" target="_blank" rel="noopener">%s <span class="ex">↗</span></a>'
                      % (url, esc(label)))
        tools = ('<section class="lp-sec"><h2>Werkzeuge</h2><div class="tool-list">%s</div></section>' % items)
    fast = ""
    if lp.get("vertiefung"):
        fast = '<section class="lp-sec vertiefung"><h2>⚡ Vertiefung</h2>%s</section>' % lp["vertiefung"]
    elif lp.get("fast"):
        fast = ('<section class="lp-sec"><div class="fast-box"><span class="fb-t">⚡ Schnellläufer:in</span>%s</div></section>'
                % lp["fast"])
    backup = ('<section class="lp-sec"><div class="backup-box"><span class="bb-t">💾 Ergebnissicherung</span>'
              'Sichere deine Ergebnisse am Stundenende <b>einfach wiederverwendbar</b> (sinnvoll benannt) an '
              '<b>zwei Orten</b> — Rechner und Cloud/USB. Achte selbstständig auf Backups.</div></section>')
    if lp.get("sicherung"):
        backup = ('<section class="lp-sec"><div class="backup-box"><span class="bb-t">%s</span>%s</div></section>'
                  % lp["sicherung"])
    sol = "".join("<li>%s</li>" % s for s in lp["solution"])
    material = ('<section class="lp-sec mat"><h2>Material · Informationstext</h2>%s</section>' % lp["material"]
                if lp.get("material") else "")
    task_figs = render_figs(lp, lp.get("task_figs"))
    solution = ('<section class="sol" id="loesung" data-unlock="%s">'
                '<h2>Musterlösung <span class="sol-status">…</span></h2>'
                '<p class="sol-countdown"></p>'
                '<div class="sol-body" hidden><ul class="sol-list">%s</ul>%s</div>'
                '<p class="sol-hint">Die Lösung wird automatisch zum angegebenen Datum sichtbar — '
                'die Seite prüft das bei jedem Laden.</p>'
                '</section>') % (unlock_iso(lp["sjw"]), sol, render_figs(lp, lp.get("solution_figs")))

    doc = (
        '<!DOCTYPE html>\n<html lang="de">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>LP%02d · %s</title>\n' % (lp["no"], esc(lp["title"]))
        + FONTS + '\n<style>\n' + THEME_CSS + '\n</style>\n</head>\n'
        '<body style="%s">\n' % style
        + '<canvas id="matrix-canvas"></canvas>\n'
        + '<div class="lp-page">\n'
        + '  <a class="back" href="../../../index.html#hj%d-content">← zur Kursübersicht</a>\n' % u["hj"]
        + '  <div class="lp-hero">\n'
        + '    <div class="lp-meta"><span>Einheit %s · %s</span><span>SJW %d · %s</span><span>%s</span></div>\n'
          % (u["num"], esc(u["title"]), lp["sjw"], de(mon), kind_badge(lp["kind"]))
        + '    <h1>%s</h1>\n' % esc(lp["title"])
        + '    <div class="lp-big">%02d</div>\n' % lp["no"]
        + '  </div>\n'
        + '  <section class="lp-sec"><h2>Das lernst du</h2><p>%s</p><div data-selfcheck="%s"></div></section>\n'
          % (lp["goal"], slug(lp["no"]))
        + ('  %s\n' % render_vorwissen(lp) if lp.get("vorwissen") else '')
        + ('  %s\n' % material if material else '')
        + '  <section class="lp-sec"><h2>Aufgaben</h2><ul class="task-list">%s</ul>%s</section>\n' % (tasks, task_figs)
        + ('  %s\n' % render_stufen(lp) if lp.get("stufen") else '')
        + ('  %s\n' % render_quiz(lp) if lp.get("quiz") else '')
        + ('  %s\n' % tools if tools else '')
        + ('  %s\n' % fast if fast else '')
        + '  %s\n' % backup
        + '  %s\n' % solution
        + '  <a class="back" href="../../../index.html#hj%d-content" style="margin-top:1.6rem">← zurück zur Kursübersicht</a>\n' % u["hj"]
        + '</div>\n'
        + '<script>\n' + THEME_JS + '\n</script>\n</body>\n</html>\n'
    )
    out_dir = lp_out_dir(lp["no"])
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "%s.html" % slug(lp["no"])), "w", encoding="utf-8") as f:
        f.write(doc)

# ---------------------------------------------------------------- Lauf
build_index()
count = 0
for u in UNITS:
    for lp in u["lps"]:
        build_lp_page(u, lp)
        count += 1

print("OK — index.html erstellt.")
print("OK — %d Lernpfad-Seiten in lernpfade/ erstellt." % count)
print("Gesamt Lernpfade laut Daten:", TOTAL_LP)
print("HJ1 SJW0 Freischaltung:", unlock_iso(0), "| HJ2 letzte:", unlock_iso(36))
