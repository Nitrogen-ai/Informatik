# -*- coding: utf-8 -*-
"""
Generator: Profil Informatik · Klasse 9 (14–15 J.) — Kursplan HJ1 & HJ2
Erzeugt index.html (Kursübersicht) + Lernpfad-Startseiten + nutzt geteilte Assets.
Einzige Quelle der Wahrheit für Inhalte, Kalender und Freischalt-Daten.
"""
import os, html
from datetime import date, timedelta

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
  "wtj": ("WebTigerJython", "https://webtigerjython.ethz.ch/"),
  "jsfiddle": ("jsfiddle.net", "https://jsfiddle.net/"),
  "github": ("GitHub", "https://github.com/"),
  "ref": ("Referenz-Tool: Verb-Trainer", "https://nitrogen-ai.github.io/training/verb_conjugation_trainer_year6.html"),
  "bincalc": ("Windows-Rechner (Programmierer-Modus)", "https://support.microsoft.com/de-de/windows/rechner-app-9b8ff34a-e3ff-9c5f-b0b0-a52a5b23c7a4"),
}

# ---------------------------------------------------------------- Vorwissen-Figuren (SVG)
# lp-Nummer -> Ordner mit typst/figN.svg (color-Variante, vollständig beschriftet)
LESSON_DIRS = {
  1: "01 Systemstart - Was ist Informatik",
  2: "02 EVA & Algorithmus - wie ein Computer denkt",
  3: "03 Scratch-Grundlagen - Bühne, Figuren, Ereignisse",
  4: "04 Schleifen & Verzweigungen - ein Mini-Spiel",
  5: "05 Makey Makey - die Welt wird zum Controller",
  6: "06 Tinkercad Circuits - Stromkreis simulieren",
  7: "07 Der Mikrocontroller - Arduino Uno kennenlernen",
  8: "08 Erster Sketch - die interne LED blinkt",
  9: "09 Steuerstrukturen im Sketch - das Ampelprogramm",
  10: "10 Objektorientierung entdecken - Attribute & Methoden",
  11: "11 Mini-Projekt Arduino - Ergebnissicherung",
}

def load_svg(lp_no, fig):
    folder = LESSON_DIRS.get(lp_no)
    if not folder:
        return ""
    path = os.path.join(BASE, folder, "typst", fig + ".svg")
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# ---------------------------------------------------------------- Kursinhalt
# Jedes LP: no, sjw, title, goal, tasks[], tools[keys], fast, rlp[], solution[], kind
UNITS = [
 # =================== HALBJAHR 1 ===================
 dict(hj=1, num="01", title="Systemstart — Was ist Informatik?",
      key="#35e0ff", key2="#0bb7e0", tint="rgba(53,224,255,0.09)",
      lps=[
        dict(no=1, sjw=1, kind="puffer", title="Boot-Sequenz: Kurslandkarte & digitale Werkzeugkiste",
             goal="Du verschaffst dir einen Überblick über das Kursjahr, richtest Konto & Ordnerstruktur ein und lernst die Regeln zur Ergebnissicherung (Backups) kennen.",
             tasks=["Diese Kursseite als Landkarte erkunden: Halbjahre, Einheiten, Lernpfade, Sterne, Schlösser.",
                    "Persönliche Ordnerstruktur anlegen: <code>Informatik/HJ1</code>, <code>HJ2</code>, <code>_backups</code>.",
                    "Backup-Regel notieren: „Am Stundenende alles sichern — lokal UND in der Cloud/USB.“"],
             tools=["ref"],
             fast="Erkunde die Referenz-Anwendung (Verb-Trainer) und notiere drei Dinge, die dir am Interface auffallen.",
             rlp=["RLP 2.3 · Bedienung", "3.2 Informatiksysteme", "neu · Orga & Backup"],
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
        dict(no=2, sjw=2, kind="lernpfad", title="EVA & Algorithmus — wie ein Computer „denkt“",
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
 dict(hj=1, num="02", title="Blockbasiert I — Scratch & Makey Makey",
      key="#34ff9e", key2="#12c47a", tint="rgba(52,255,158,0.09)",
      lps=[
        dict(no=3, sjw=3, kind="lernpfad", title="Scratch-Grundlagen: Bühne, Figuren, Ereignisse",
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
        dict(no=4, sjw=4, kind="lernpfad", title="Schleifen & Verzweigungen: ein Mini-Spiel",
             goal="Du setzt „wiederhole“-Schleifen und „falls … dann“-Verzweigungen ein und programmierst ein einfaches Fang- oder Ausweichspiel.",
             tasks=["Endlosschleife zum ständigen Abfragen der Tastatur bauen.",
                    "Verzweigung: „falls Figur berührt Rand → drehe/prallende ab“.",
                    "Punktevariable anlegen und bei Treffer erhöhen."],
             tools=["scratch"],
             fast="Füge einen Schwierigkeitsgrad hinzu: Das Spiel wird mit steigender Punktzahl schneller.",
             rlp=["RLP 2.2 · Kontrollstrukturen", "3.3 Schleife & Verzweigung"],
             vorwissen=[
               dict(fig="fig1", cap="Bild 1 · Endlosschleife + Tastaturabfrage", quiz=[
                 dict(q='Wozu dient Teil 1, die Endlosschleife ("wiederhole fortlaufend")?',
                      done="Richtig — sie prüft ständig.",
                      opts=[
                        ("Sie prüft ständig, ohne von selbst zu enden, ob eine Bedingung eingetreten ist.", True, None),
                        ("Sie prüft die Bedingung genau einmal.", False, "Das würde eine einmalige Verzweigung tun, keine Endlosschleife."),
                        ("Sie beendet das Programm sofort.", False, "Eine Endlosschleife läuft weiter, sie beendet nichts."),
                        ("Sie speichert nur Daten, ohne etwas zu prüfen.", False, "Speichern ist keine Aufgabe einer Schleife."),
                      ]),
                 dict(q='Was passiert bei Teil 2, wenn die Bedingung "Taste links?" erfüllt ist?',
                      done="Genau — die Aktion wird ausgeführt.",
                      opts=[
                        ("Die angehängte Aktion wird ausgeführt (z. B. Bewegung nach links).", True, None),
                        ("Das ganze Programm stoppt.", False, "Eine erfüllte Bedingung löst die Aktion aus, sie stoppt nicht das Programm."),
                        ("Die Schleife wird beendet.", False, "Die Endlosschleife läuft weiter, nur die Aktion wird einmal ausgeführt."),
                        ("Nichts, Verzweigungen lösen keine Aktionen aus.", False, "Genau das ist die Aufgabe einer Verzweigung."),
                      ]),
                 dict(q="Was passiert bei Teil 3, wenn die Bedingung NICHT erfüllt ist?",
                      done="Stimmt — die Aktion wird übersprungen.",
                      opts=[
                        ("Die Aktion wird übersprungen, die Schleife läuft weiter.", True, None),
                        ("Das Programm stürzt ab.", False, "Eine nicht erfüllte Bedingung führt zu keinem Absturz."),
                        ("Die Aktion wird trotzdem ausgeführt.", False, "Ohne erfüllte Bedingung wird die Aktion gerade nicht ausgeführt."),
                        ("Die Schleife startet von vorne bei Frage 1.", False, "Die Schleife läuft einfach weiter, sie springt nicht zurück."),
                      ]),
                 dict(q="Warum steckt die Verzweigung INNERHALB der Schleife und nicht davor?",
                      done="Richtig — ständige Neuprüfung.",
                      opts=[
                        ("Damit die Bedingung ständig neu geprüft wird, solange das Spiel läuft.", True, None),
                        ("Das spielt keine Rolle, beide Anordnungen sind identisch.", False, "Außerhalb der Schleife würde die Bedingung nur einmal geprüft."),
                        ("Damit die Bedingung nur einmal beim Start geprüft wird.", False, "Genau das würde passieren, wenn sie AUSSERHALB stünde — nicht gewollt."),
                        ("Damit das Programm schneller läuft.", False, "Die Position hat nichts mit der Geschwindigkeit zu tun."),
                      ]),
               ]),
               dict(fig="fig2", cap="Bild 2 · Punktevariable + Kollision", quiz=[
                 dict(q='Wozu dient Teil 1, die Variable "Punkte"?',
                      done="Richtig — sie speichert den Punktestand.",
                      opts=[
                        ("Sie speichert einen Zustand (den Punktestand), der sich über die Zeit verändert.", True, None),
                        ("Sie zeichnet die Spielfigur.", False, "Zeichnen übernimmt das Kostüm des Sprites, nicht die Variable."),
                        ("Sie steuert die Bühnenfarbe.", False, "Die Bühnenfarbe wird nicht über eine Punkte-Variable gesteuert."),
                        ("Variablen werden in Scratch nicht benötigt.", False, "Variablen sind ein zentraler Baustein in Scratch."),
                      ]),
                 dict(q="Womit erkennst du eine Kollision (Teil 2)?",
                      done='Genau — mit "wird … berührt?".',
                      opts=[
                        ('mit einem "wird … berührt?"-Block als Bedingung', True, None),
                        ("nur durch genaues Hinschauen ohne Code", False, "Scratch bietet dafür einen eigenen Berührungs-Block."),
                        ("mit einer Endlosschleife allein", False, "Die Schleife wiederholt nur die Prüfung, sie erkennt selbst keine Berührung."),
                        ("das ist in Scratch nicht möglich", False, "Scratch hat einen eingebauten Berührungs-Block."),
                      ]),
                 dict(q='Was macht Teil 3, "ändere Punkte um 1"?',
                      done="Stimmt — der Wert steigt um 1.",
                      opts=[
                        ("Es erhöht den Wert der Variable Punkte bei jedem Durchlauf um 1.", True, None),
                        ("Es setzt die Variable auf genau 1 zurück.", False, "Das würde „setze Punkte auf 1“ tun, nicht „ändere um 1“."),
                        ("Es löscht die Variable.", False, "Die Variable bleibt erhalten, ihr Wert wird nur erhöht."),
                        ("Es hat keinen Effekt ohne Bildschirmaktualisierung.", False, "Der Wert ändert sich unabhängig von der Anzeige."),
                      ]),
                 dict(q='Warum sollte "ändere Punkte um 1" INNERHALB der Kollisions-Verzweigung stehen?',
                      done="Richtig — nur bei echtem Treffer.",
                      opts=[
                        ("Damit der Punktestand nur bei einem echten Treffer steigt.", True, None),
                        ("Damit der Punktestand jede Sekunde automatisch steigt.", False, "Das würde passieren, wenn der Block außerhalb der Verzweigung stünde."),
                        ("Das spielt keine Rolle, die Position ist beliebig.", False, "Innerhalb der Verzweigung zählt nur ein echter Treffer."),
                        ("Damit die Variable gelöscht wird.", False, "Der Block erhöht die Variable, er löscht sie nicht."),
                      ]),
               ]),
             ],
             quiz=[
               dict(q="Wozu dient eine Endlosschleife beim Abfragen der Tastatur?",
                    done="Richtig — sie fragt ständig ab.",
                    opts=[
                      ("Damit ständig geprüft wird, ob eine Taste gedrückt wurde.", True, None),
                      ("Damit das Programm nach einem Tastendruck sofort endet.", False, "Eine Endlosschleife läuft weiter, sie beendet das Programm nicht."),
                      ("Damit die Tastatur ausgeschaltet wird.", False, "Die Schleife fragt die Tastatur ab, schaltet sie aber nicht aus."),
                      ("Sie hat damit nichts zu tun.", False, "Genau das ständige Abfragen ist ihre Aufgabe."),
                    ]),
               dict(q="Was passiert bei der Verzweigung „falls Figur berührt Rand“?",
                    done="Genau — die Bedingung löst eine Reaktion aus.",
                    opts=[
                      ("Die Figur reagiert (z. B. dreht ab), wenn die Bedingung erfüllt ist.", True, None),
                      ("Die Figur verschwindet immer sofort.", False, "Das würde nur passieren, wenn extra ein Lösch-Befehl programmiert wäre."),
                      ("Das Spiel startet automatisch neu.", False, "Ein Neustart müsste eigens programmiert werden, das macht die Verzweigung allein nicht."),
                      ("Nichts, Verzweigungen wirken nicht auf Figuren.", False, "Verzweigungen steuern genau solche Reaktionen von Figuren."),
                    ]),
               dict(q="Wozu dient eine Variable wie „Punkte“ in einem Spiel?",
                    done="Stimmt — sie merkt sich einen Zustand über die Zeit.",
                    opts=[
                      ("Sie speichert einen Zustand (den Punktestand), der sich über die Zeit verändert.", True, None),
                      ("Sie zeichnet nur die Spielfigur.", False, "Das Zeichnen übernehmen Aussehen-Blöcke, nicht die Variable."),
                      ("Sie ist nur für die Farbe der Bühne zuständig.", False, "Die Bühnenfarbe hat mit einer Punkte-Variable nichts zu tun."),
                      ("Variablen werden in Scratch nicht benötigt.", False, "Ohne Variable ließe sich kein Punktestand über die Zeit merken."),
                    ]),
               dict(q="Womit erkennst du eine Kollision zwischen zwei Figuren?",
                    done="Richtig — der „wird berührt?“-Block prüft das.",
                    opts=[
                      ("Mit einem „wird berührt?“-Block als Bedingung.", True, None),
                      ("Nur durch genaues Hinschauen ohne Code.", False, "Das Spiel muss die Kollision selbst erkennen, nicht nur die spielende Person."),
                      ("Mit einer Endlosschleife allein.", False, "Die Schleife fragt nur wiederholt ab, die Kollision erkennt der Berührt-Block."),
                      ("Das ist in Scratch nicht möglich.", False, "Der „wird berührt?“-Block macht genau das möglich."),
                    ]),
             ],
             solution=["Schleife = Wiederholung; Verzweigung = Entscheidung mit Bedingung.",
                       "Variable „Punkte“ speichert den Zustand über die Zeit.",
                       "Kollision per „wird berührt?“-Block als Bedingung."]),
        dict(no=5, sjw=5, kind="lernpfad", title="Makey Makey: die Welt wird zum Controller",
             goal="Du verbindest Makey Makey mit Scratch und steuerst dein Programm über leitfähige Alltagsgegenstände — Eingabe wird begreifbar (Sensorik & Stromkreis).",
             tasks=["Makey Makey anschließen und einen Stromkreis über Erde (EARTH) schließen.",
                    "Bananen/Alufolie als Tasten für Pfeil/Leertaste einrichten.",
                    "Dein Scratch-Spiel aus LP04 mit den neuen „Tasten“ steuern."],
             tools=["makey", "scratch"],
             fast="Baue ein „Banana-Piano“ mit fünf Tönen und erkläre, warum ein geschlossener Stromkreis nötig ist.",
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
                 dict(q="Was ist Teil 1, das violette Board?",
                      done="Richtig — Makey Makey.",
                      opts=[
                        ("Makey Makey — es erkennt den geschlossenen Stromkreis.", True, None),
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
               ]),
             ],
             quiz=[
               dict(q="Was ersetzt Makey Makey im Grunde?",
                    done="Richtig — Tastatur-/Maus-Signale.",
                    opts=[
                      ("Signale von Tastatur und Maus.", True, None),
                      ("Den gesamten Computer.", False, "Makey Makey ersetzt nur die Eingabesignale, nicht den ganzen Computer."),
                      ("Die Scratch-Software.", False, "Scratch läuft weiterhin normal — Makey Makey liefert nur andere Eingaben."),
                      ("Den Bildschirm.", False, "Der Bildschirm gehört zur Ausgabe, damit hat Makey Makey nichts zu tun."),
                    ]),
               dict(q="Wodurch entsteht ein „Tastendruck“ bei Makey Makey?",
                    done="Genau — ein geschlossener Stromkreis über den Körper.",
                    opts=[
                      ("Durch einen geschlossenen Stromkreis, z. B. über den eigenen Körper.", True, None),
                      ("Durch lautes Klopfen auf den Tisch.", False, "Es zählt der geschlossene Stromkreis, nicht die Lautstärke."),
                      ("Durch eine WLAN-Verbindung.", False, "Makey Makey arbeitet über Kabel und Stromkreise, nicht über WLAN."),
                      ("Nur durch Drücken einer echten Computertaste.", False, "Genau das will Makey Makey ersetzen — durch leitfähige Alltagsgegenstände."),
                    ]),
               dict(q="Welche Alltagsgegenstände eignen sich als leitfähige „Tasten“?",
                    done="Stimmt — leitfähige Alltagsgegenstände.",
                    opts=[
                      ("Bananen, Alufolie oder Wasser.", True, None),
                      ("Nur Holz und Papier.", False, "Holz und Papier leiten Strom kaum — sie funktionieren nicht als Makey-Makey-Taste."),
                      ("Nur Glas.", False, "Glas ist ein Isolator, kein Leiter."),
                      ("Gar keine, es braucht spezielle Hardware.", False, "Genau alltägliche, leitfähige Gegenstände funktionieren als Taste — keine Spezialhardware nötig."),
                    ]),
               dict(q="Zu welchem Teil des EVA-Prinzips gehört Makey Makey vor allem?",
                    done="Richtig — zur Eingabe.",
                    opts=[
                      ("Zur Eingabe.", True, None),
                      ("Zur Verarbeitung.", False, "Verarbeitet wird im Prozessor/der Software, nicht im Makey Makey selbst."),
                      ("Zur Ausgabe.", False, "Ausgabe wäre z. B. der Bildschirm — Makey Makey liefert stattdessen Eingaben."),
                      ("Zu keinem der drei Schritte.", False, "Makey Makey liefert Eingabesignale — das ordnet es klar der Eingabe zu."),
                    ]),
             ],
             solution=["Makey Makey ersetzt Tastatur/Maus-Signale; ein Tastendruck = geschlossener Stromkreis über den Körper.",
                       "Leitfähige Objekte (Obst, Folie, Wasser) leiten den schwachen Strom.",
                       "Eingabe = Kern des EVA-Prinzips, hier physisch erlebbar."]),
      ]),
 dict(hj=1, num="03", title="Blockbasiert II — Tinkercad & Arduino",
      key="#a56bff", key2="#7d3ff0", tint="rgba(165,107,255,0.09)",
      lps=[
        dict(no=6, sjw=6, kind="lernpfad", title="Tinkercad Circuits: Stromkreis simulieren",
             goal="Du baust im Browser einen virtuellen Stromkreis mit LED, Vorwiderstand und Steckplatine und verstehst, warum der Widerstand die LED schützt.",
             tasks=["LED + Widerstand + Batterie auf der Steckplatine verdrahten.",
                    "Simulation starten und den Stromfluss beobachten.",
                    "Widerstandswert variieren und Helligkeit/Schutz erklären."],
             tools=["tinker"],
             fast="Schalte drei LEDs parallel und vergleiche mit einer Reihenschaltung — was passiert mit der Helligkeit?",
             rlp=["RLP 2.3 · Informatiksysteme", "3.2 Hardware", "neu · Schaltungssimulation"],
             vorwissen=[
               dict(fig="fig1", cap="Bild 1 · Stromkreis-Aufbau", quiz=[
                 dict(q="Was ist Teil 1?",
                      done="Richtig — die Batterie.",
                      opts=[
                        ("die Batterie (Stromquelle, 9V)", True, None),
                        ("der Widerstand", False, "Der Widerstand ist das Zickzack-Symbol, nicht die Batterie."),
                        ("die LED", False, "Die LED ist das Dreieck-Symbol weiter rechts."),
                        ("die Steckplatine", False, "Die Steckplatine ist das Raster im Hintergrund."),
                      ]),
                 dict(q="Wofür steht Teil 2, das Zickzack-Symbol?",
                      done="Genau — der Widerstand.",
                      opts=[
                        ("der Widerstand — er begrenzt den Strom", True, None),
                        ("die Batterie", False, "Die Batterie ist das Symbol mit den zwei parallelen Linien."),
                        ("die LED", False, "Die LED ist das Dreieck-Symbol, nicht das Zickzack."),
                        ("das USB-Kabel", False, "Diese Schaltung hat gar kein USB-Kabel."),
                      ]),
                 dict(q="Was ist Teil 3, das Dreieck-Symbol?",
                      done="Stimmt — die LED.",
                      opts=[
                        ("die LED — das lange Beinchen ist die Anode, das kurze die Kathode", True, None),
                        ("der Widerstand", False, "Der Widerstand ist das Zickzack-Symbol."),
                        ("die Steckplatine", False, "Die Steckplatine ist das Hintergrundraster."),
                        ("der Schalter", False, "Diese Schaltung enthält keinen eigenen Schalter."),
                      ]),
                 dict(q="Wozu dient Teil 4, die Steckplatine?",
                      done="Richtig — sie verbindet Bauteile ohne Löten.",
                      opts=[
                        ("sie verbindet Bauteile elektrisch, ohne dass gelötet werden muss", True, None),
                        ("sie speichert Strom wie ein Akku", False, "Eine Steckplatine speichert keine Energie."),
                        ("sie zeigt den Simulationsstatus an", False, "Der Status wird in Tinkercad separat angezeigt, nicht auf der Platine."),
                        ("sie hat keine erkennbare Funktion", False, "Sie verbindet die Bauteile elektrisch — das ist ihre Hauptfunktion."),
                      ]),
               ]),
               dict(fig="fig2", cap="Bild 2 · Widerstand als Schutz", quiz=[
                 dict(q="Was passiert bei Fall 1, ohne Widerstand?",
                      done="Richtig — zu viel Strom, LED brennt durch.",
                      opts=[
                        ("Es fließt zu viel Strom, die LED brennt durch.", True, None),
                        ("Die LED leuchtet besonders lange.", False, "Ohne Schutz brennt sie eher schnell durch, statt lange zu halten."),
                        ("Nichts, das ist unproblematisch.", False, "Zu viel Strom beschädigt die LED dauerhaft."),
                        ("Die Batterie lädt sich auf.", False, "Batterien laden sich dadurch nicht auf."),
                      ]),
                 dict(q="Was passiert bei Fall 2, mit 220 Ω Widerstand?",
                      done="Genau — normale Helligkeit.",
                      opts=[
                        ("Die LED leuchtet normal und ist geschützt.", True, None),
                        ("Die LED brennt sofort durch.", False, "Der passende Widerstand schützt gerade davor."),
                        ("Die LED leuchtet gar nicht.", False, "Mit passendem Widerstand fließt genug Strom zum Leuchten."),
                        ("Der Widerstand hat keine Wirkung.", False, "Der Widerstand begrenzt den Strom spürbar."),
                      ]),
                 dict(q="Was passiert bei Fall 3, mit 1 kΩ Widerstand?",
                      done="Stimmt — weniger Strom, dunkler.",
                      opts=[
                        ("Weniger Strom fließt, die LED leuchtet dunkler.", True, None),
                        ("Die LED leuchtet heller als bei 220 Ω.", False, "Ein größerer Widerstand lässt weniger Strom fließen, nicht mehr."),
                        ("Die LED brennt durch.", False, "Ein höherer Widerstand schützt die LED noch stärker."),
                        ("Es ändert sich nichts gegenüber 220 Ω.", False, "Der höhere Widerstandswert verändert die Helligkeit spürbar."),
                      ]),
               ]),
             ],
             quiz=[
               dict(q="Wozu dient der Vorwiderstand in einem LED-Stromkreis?",
                    done="Richtig — er schützt die LED.",
                    opts=[
                      ("Er begrenzt den Strom und schützt die LED vor dem Durchbrennen.", True, None),
                      ("Er macht die LED heller.", False, "Ein Widerstand begrenzt den Strom, er verstärkt ihn nicht."),
                      ("Er speichert Energie für später.", False, "Das wäre die Aufgabe eines Kondensators oder Akkus, nicht eines Widerstands."),
                      ("Er hat keine Funktion, ist nur Deko.", False, "Ohne Widerstand brennt die LED durch — er hat eine echte Schutzfunktion."),
                    ]),
               dict(q="Was passiert ohne Vorwiderstand?",
                    done="Genau — zu viel Strom zerstört die LED.",
                    opts=[
                      ("Es fließt zu viel Strom, die LED brennt durch.", True, None),
                      ("Die LED leuchtet gar nicht.", False, "Ohne Widerstand leuchtet sie zunächst sogar sehr hell, bevor sie durchbrennt."),
                      ("Nichts, das ist unproblematisch.", False, "Zu viel Strom beschädigt die LED dauerhaft."),
                      ("Die Batterie lädt sich automatisch auf.", False, "Batterien laden sich dadurch nicht auf."),
                    ]),
               dict(q="Wie erkennst du Anode und Kathode an einer LED?",
                    done="Stimmt — am langen bzw. kurzen Beinchen.",
                    opts=[
                      ("am langen (Anode) und kurzen (Kathode) Beinchen", True, None),
                      ("an der Farbe des Gehäuses", False, "Die Gehäusefarbe zeigt die Leuchtfarbe, nicht die Polung."),
                      ("am Gewicht", False, "Das Gewicht einer LED verrät nichts über die Polung."),
                      ("das ist bei jeder LED zufällig", False, "Die Beinchenlänge kennzeichnet die Polung zuverlässig."),
                    ]),
               dict(q="Was passiert, wenn du mehrere LEDs parallel statt in Reihe schaltest?",
                    done="Richtig — parallel bleiben sie gleich hell.",
                    opts=[
                      ("Sie leuchten alle etwa gleich hell.", True, None),
                      ("Sie werden alle dunkler, da sich die Spannung aufteilt.", False, "Das passiert bei einer Reihenschaltung, nicht bei einer Parallelschaltung."),
                      ("Sie funktionieren gar nicht.", False, "Parallelschaltung ist eine gängige, funktionierende Schaltungsart."),
                      ("Die Reihenfolge spielt keine Rolle.", False, "Reihen- vs. Parallelschaltung macht einen deutlichen Unterschied in der Helligkeit."),
                    ]),
             ],
             solution=["Ohne Vorwiderstand fließt zu viel Strom → LED brennt durch.",
                       "Steckplatine verbindet Reihen elektrisch; lange/kurze LED-Beinchen = Anode/Kathode.",
                       "Parallel: gleich hell; Reihe: dunkler, da Spannung sich aufteilt."]),
        dict(no=7, sjw=7, kind="lernpfad", title="Der Mikrocontroller: Arduino Uno kennenlernen",
             goal="Du benennst die Bauteile einer Arduino-Schaltung (Widerstand, LED, Mikrocontroller, Steckplatine) und verstehst die Rolle von GND (Minuspol) und 5 V.",
             tasks=["Bauteile im Schaltbild korrekt benennen und ordnen.",
                    "Die technische Anpassung für LEDs erklären: Stromkreisschluss zum Minuspol (GND).",
                    "Pins des Arduino Uno erkunden: digital, analog, 5 V, GND."],
             tools=["tinker", "arduino"],
             fast="Recherchiere den Unterschied zwischen digitalen und analogen Pins und nenne je ein Beispiel-Bauteil.",
             rlp=["RLP 2.3 · Informatiksysteme", "3.2 Mikrocontroller"],
             vorwissen=[
               dict(fig="fig1", cap="Bild 1 · Das Arduino-Board", quiz=[
                 dict(q="Was ist Teil 1, der violette Chip?",
                      done="Richtig — der Mikrocontroller.",
                      opts=[
                        ("der Mikrocontroller — das „Gehirn“ des Boards", True, None),
                        ("der USB-Anschluss", False, "Der USB-Anschluss sitzt am Rand des Boards, nicht mittig als Chip."),
                        ("ein Widerstand", False, "Ein Widerstand ist ein winziges Einzelbauteil, kein zentraler Chip."),
                        ("die Steckplatine", False, "Die Steckplatine ist ein separates Bauteil, kein Teil des Arduino-Boards."),
                      ]),
                 dict(q="Wofür stehen die Pins bei Teil 2?",
                      done="Genau — die Digitalpins.",
                      opts=[
                        ("für die Digitalpins (0-13), sie kennen nur HIGH oder LOW", True, None),
                        ("für die Analogpins, sie messen Zwischenwerte", False, "Analogpins sind separat beschriftet (A0-A5), das ist Teil 3."),
                        ("für den Stromanschluss", False, "Die Stromversorgung ist ein eigener Bereich (5V/GND)."),
                        ("für den Reset-Knopf", False, "Der Reset-Knopf ist kein Pin und hier nicht markiert."),
                      ]),
                 dict(q="Wofür stehen die Pins bei Teil 3?",
                      done="Stimmt — die Analogpins.",
                      opts=[
                        ("für die Analogpins (A0-A5), sie können Zwischenwerte messen", True, None),
                        ("für die Digitalpins, sie kennen nur an/aus", False, "Die Digitalpins sind die nummerierte Reihe 0-13, Teil 2."),
                        ("für den USB-Anschluss", False, "Der USB-Anschluss ist ein eigenes Bauteil am Rand des Boards."),
                        ("für den Mikrocontroller-Chip", False, "Der Chip ist Teil 1, nicht die Pin-Reihe."),
                      ]),
                 dict(q="Wozu dienen die Pins bei Teil 4?",
                      done="Richtig — Stromversorgung.",
                      opts=[
                        ("zur Stromversorgung — 5V und GND (Minuspol)", True, None),
                        ("zum Programmieren über USB", False, "Programmiert wird über den USB-Anschluss, nicht über 5V/GND."),
                        ("zur drahtlosen Datenübertragung", False, "Ein Arduino Uno hat serienmäßig kein WLAN."),
                        ("sie haben keine erkennbare Funktion", False, "5V und GND versorgen die Schaltung mit Strom — eine zentrale Funktion."),
                      ]),
               ]),
               dict(fig="fig2", cap="Bild 2 · Vom Digitalpin zur LED", quiz=[
                 dict(q="Was ist Teil 1, der violette Chip links im Bild?",
                      done="Richtig — der Mikrocontroller.",
                      opts=[
                        ("der Mikrocontroller — er gibt das Signal am Digitalpin aus", True, None),
                        ("die LED", False, "Die LED ist das Dreieck-Symbol rechts im Bild."),
                        ("der Widerstand", False, "Der Widerstand ist das Zickzack-Symbol in der Mitte."),
                        ("die Steckplatine", False, "Die Steckplatine ist das Hintergrundraster."),
                      ]),
                 dict(q="Wozu dient Teil 2, das Zickzack-Symbol?",
                      done="Genau — der Widerstand.",
                      opts=[
                        ("der Widerstand — er begrenzt den Strom und schützt die LED", True, None),
                        ("die Batterie", False, "Diese Schaltung wird vom Mikrocontroller-Pin gespeist, nicht von einer Batterie."),
                        ("der Mikrocontroller", False, "Der Mikrocontroller ist der Chip links im Bild."),
                        ("das USB-Kabel", False, "Diese Schaltung zeigt kein USB-Kabel."),
                      ]),
                 dict(q="Was ist Teil 3, das Dreieck-Symbol?",
                      done="Stimmt — die LED.",
                      opts=[
                        ("die LED", True, None),
                        ("der Widerstand", False, "Der Widerstand ist das Zickzack-Symbol."),
                        ("die Steckplatine", False, "Die Steckplatine ist das Hintergrundraster, kein Symbol im Stromkreis."),
                        ("der Mikrocontroller", False, "Der Mikrocontroller ist der Chip links im Bild."),
                      ]),
                 dict(q="Wozu dient Teil 4, die Steckplatine?",
                      done="Richtig — Bauteile ohne Löten verbinden.",
                      opts=[
                        ("sie verbindet die Bauteile elektrisch, ohne dass gelötet werden muss", True, None),
                        ("sie speichert das Arduino-Programm", False, "Das Programm wird im Speicher des Mikrocontrollers abgelegt, nicht auf der Platine."),
                        ("sie ersetzt den GND-Anschluss", False, "GND ist ein eigener Pin am Board, die Platine ersetzt ihn nicht."),
                        ("sie hat keine erkennbare Funktion", False, "Sie verbindet die Bauteile elektrisch — das ist ihre Hauptfunktion."),
                      ]),
               ]),
             ],
             quiz=[
               dict(q="In welcher Reihenfolge ist eine einfache LED-Schaltung aufgebaut?",
                    done="Richtig — LED, Widerstand, Mikrocontroller, Steckplatine.",
                    opts=[
                      ("LED, Widerstand, Mikrocontroller, Steckplatine", True, None),
                      ("Steckplatine, Mikrocontroller, LED, Widerstand", False, "Das ist nicht die übliche Bauteil-Reihenfolge im Stromkreis."),
                      ("nur LED und Mikrocontroller, ohne Widerstand", False, "Ohne Widerstand würde die LED durchbrennen."),
                      ("die Reihenfolge ist beliebig", False, "Die Bauteile stehen in einer festen, sinnvollen Reihenfolge im Stromkreis."),
                    ]),
               dict(q="Wozu muss eine LED mit GND (Minuspol) verbunden sein?",
                    done="Genau — sonst fließt kein Strom.",
                    opts=[
                      ("damit der Stromkreis geschlossen ist und Strom fließen kann", True, None),
                      ("damit sie heller leuchtet", False, "Die Helligkeit hängt vom Widerstand ab, nicht von GND allein."),
                      ("GND wird für LEDs nicht benötigt", False, "Ohne GND-Verbindung ist der Stromkreis nicht geschlossen."),
                      ("damit sie vor Wasser geschützt ist", False, "GND hat nichts mit Wasserschutz zu tun."),
                    ]),
               dict(q="Was können Digitalpins am Arduino Uno?",
                    done="Stimmt — nur HIGH oder LOW.",
                    opts=[
                      ("nur HIGH oder LOW (an/aus) erkennen bzw. ausgeben", True, None),
                      ("beliebige Zwischenwerte messen", False, "Das können Analogpins, nicht die digitalen Pins."),
                      ("nur Ton ausgeben", False, "Digitalpins sind nicht auf Toncodierung beschränkt."),
                      ("nur WLAN-Signale senden", False, "Der Arduino Uno hat serienmäßig kein WLAN."),
                    ]),
               dict(q="Was können Analogpins, was Digitalpins nicht können?",
                    done="Richtig — Zwischenwerte messen.",
                    opts=[
                      ("Zwischenwerte (nicht nur an/aus) messen", True, None),
                      ("nur HIGH/LOW erkennen", False, "Das ist die Einschränkung der Digitalpins, nicht die Fähigkeit der Analogpins."),
                      ("den Arduino aufladen", False, "Analogpins dienen dem Messen/Ausgeben von Werten, nicht dem Aufladen."),
                      ("Programme speichern", False, "Programme werden im Speicher des Mikrocontrollers abgelegt, nicht über Analogpins."),
                    ]),
             ],
             solution=["Reihenfolge: LED, Widerstand, Mikrocontroller, Steckplatine.",
                       "LEDs benötigen Stromkreisschluss zum Minuspol (GND).",
                       "Digitalpins kennen nur HIGH/LOW, Analogpins messen Zwischenwerte."]),
        dict(no=8, sjw=8, kind="lernpfad", title="Erster Sketch: die interne LED blinkt",
             goal="Du schreibst einen Arduino-Sketch mit <code>setup()</code>, <code>loop()</code>, <code>digitalWrite()</code> und <code>delay()</code>, der die interne LED (Pin 13) im Sekundentakt blinken lässt.",
             tasks=["Struktur eines Sketches verstehen: <code>setup()</code> läuft einmal, <code>loop()</code> endlos.",
                    "LED an Pin 13 in einer Dauerschleife 1 s an / 1 s aus schalten.",
                    "Sketch simulieren (Tinkercad) oder auf echte Hardware laden."],
             tools=["arduino", "tinker"],
             fast="Lass die LED ein Morsezeichen (z. B. SOS) blinken, indem du die delay-Zeiten variierst.",
             rlp=["RLP 2.2 · Algorithmen", "3.3 Textbasierte Steuerung", "neu · Arduino-Sketch"],
             vorwissen=[
               dict(fig="fig1", cap="Bild 1 · Sketch-Struktur", quiz=[
                 dict(q="Was passiert im Block bei Teil 1, setup()?",
                      done="Richtig — setup() läuft nur einmal.",
                      opts=[
                        ("Der Code darin läuft genau einmal beim Start.", True, None),
                        ("Der Code darin läuft endlos.", False, "Das ist die Aufgabe von loop(), nicht von setup()."),
                        ("setup() wird nie ausgeführt.", False, "setup() wird beim Start immer einmal ausgeführt."),
                        ("setup() pausiert das Programm.", False, "Pausieren übernimmt delay(), nicht setup() selbst."),
                      ]),
                 dict(q="Wozu dient die Zeile bei Teil 2, pinMode(13, OUTPUT)?",
                      done="Genau — Pin 13 wird zum Ausgang.",
                      opts=[
                        ("Sie legt fest, dass Pin 13 ein Ausgang ist.", True, None),
                        ("Sie liest einen Sensorwert an Pin 13.", False, "Das würde digitalRead() erledigen, nicht pinMode()."),
                        ("Sie schaltet Pin 13 sofort ein.", False, "Das übernimmt digitalWrite(), nicht pinMode()."),
                        ("Sie hat keine Wirkung im Sketch.", False, "Ohne pinMode() weiß der Pin nicht, ob er Ein- oder Ausgang ist."),
                      ]),
                 dict(q="Was passiert im Block bei Teil 3, loop()?",
                      done="Stimmt — loop() wiederholt sich endlos.",
                      opts=[
                        ("Der Code darin wiederholt sich endlos.", True, None),
                        ("Der Code darin läuft nur einmal.", False, "Das ist die Aufgabe von setup(), nicht von loop()."),
                        ("loop() wird nur bei Fehlern ausgeführt.", False, "loop() läuft immer wieder, unabhängig von Fehlern."),
                        ("loop() startet den Computer neu.", False, "loop() betrifft nur den Arduino-Sketch, nicht den Computer."),
                      ]),
                 dict(q="Was bewirkt die Sequenz bei Teil 4?",
                      done="Richtig — LED blinkt im Sekundentakt.",
                      opts=[
                        ("Sie schaltet die LED abwechselnd 1 Sekunde an und 1 Sekunde aus.", True, None),
                        ("Sie schaltet die LED dauerhaft ein.", False, "Die delay-Befehle sorgen für einen Wechsel zwischen an und aus."),
                        ("Sie liest einen Tasterzustand.", False, "Das würde digitalRead() erledigen, hier wird nur geschrieben."),
                        ("Sie hat keine sichtbare Wirkung.", False, "Die LED blinkt dadurch sichtbar im Sekundentakt."),
                      ]),
               ]),
               dict(fig="fig2", cap="Bild 2 · LED-Blink-Ablauf", quiz=[
                 dict(q="Was passiert bei Schritt 1?",
                      done="Richtig — die LED wird eingeschaltet.",
                      opts=[
                        ("digitalWrite(13,HIGH) — die LED wird eingeschaltet.", True, None),
                        ("delay(1000) — das Programm wartet.", False, "Das Warten ist Schritt 2, nicht Schritt 1."),
                        ("digitalWrite(13,LOW) — die LED wird ausgeschaltet.", False, "Das Ausschalten ist Schritt 3, nicht Schritt 1."),
                        ("Das Programm startet neu.", False, "Der Ablauf beginnt mit dem Einschalten der LED, nicht mit einem Neustart."),
                      ]),
                 dict(q="Was passiert bei Schritt 2?",
                      done="Genau — 1 Sekunde Pause.",
                      opts=[
                        ("delay(1000) — das Programm pausiert für 1 Sekunde.", True, None),
                        ("Die LED wird sofort ausgeschaltet.", False, "Das Ausschalten kommt erst danach, in Schritt 3."),
                        ("Der Sketch wird beendet.", False, "Der Sketch läuft in loop() endlos weiter."),
                        ("Pin 13 wird neu konfiguriert.", False, "Die Pin-Konfiguration passiert nur einmal in setup()."),
                      ]),
                 dict(q="Was passiert bei Schritt 3?",
                      done="Stimmt — die LED wird ausgeschaltet.",
                      opts=[
                        ("digitalWrite(13,LOW) — die LED wird ausgeschaltet.", True, None),
                        ("digitalWrite(13,HIGH) — die LED wird eingeschaltet.", False, "Das Einschalten ist Schritt 1, nicht Schritt 3."),
                        ("Das Programm wartet 1 Sekunde.", False, "Das Warten nach dem Ausschalten ist Schritt 4."),
                        ("loop() wird verlassen.", False, "loop() wiederholt sich endlos, sie wird nicht verlassen."),
                      ]),
               ]),
             ],
             quiz=[
               dict(q="Was passiert im Block setup()?",
                    done="Richtig — setup() läuft nur einmal.",
                    opts=[
                      ("Der Code darin läuft genau einmal beim Start.", True, None),
                      ("Der Code darin läuft endlos.", False, "Das ist die Aufgabe von loop(), nicht von setup()."),
                      ("setup() wird nie ausgeführt.", False, "setup() wird beim Start immer einmal ausgeführt."),
                      ("setup() pausiert das Programm.", False, "Pausieren übernimmt delay(), nicht setup() selbst."),
                    ]),
               dict(q="Was passiert im Block loop()?",
                    done="Genau — loop() wiederholt sich endlos.",
                    opts=[
                      ("Der Code darin wiederholt sich endlos.", True, None),
                      ("Der Code darin läuft nur einmal.", False, "Das ist die Aufgabe von setup(), nicht von loop()."),
                      ("loop() wird nur bei Fehlern ausgeführt.", False, "loop() läuft immer wieder, unabhängig von Fehlern."),
                      ("loop() startet den Computer neu.", False, "loop() betrifft nur den Arduino-Sketch, nicht den Computer."),
                    ]),
               dict(q="Wozu dient digitalWrite(13, HIGH)?",
                    done="Stimmt — es schaltet Pin 13 ein.",
                    opts=[
                      ("Es schaltet Pin 13 (z. B. eine LED) ein.", True, None),
                      ("Es liest einen Sensorwert an Pin 13.", False, "Das würde digitalRead() oder analogRead() erledigen, nicht digitalWrite()."),
                      ("Es wartet eine Sekunde.", False, "Das Warten übernimmt delay(1000), nicht digitalWrite()."),
                      ("Es startet das Programm neu.", False, "digitalWrite() schaltet nur einen Pin, startet kein Programm neu."),
                    ]),
               dict(q="Wozu dient delay(1000)?",
                    done="Richtig — eine Sekunde Pause.",
                    opts=[
                      ("Das Programm pausiert für 1000 Millisekunden (1 Sekunde).", True, None),
                      ("Das Programm läuft 1000-mal schneller.", False, "delay() verlangsamt den Ablauf durch eine Pause, es beschleunigt nicht."),
                      ("Es schaltet eine LED aus.", False, "Das Schalten übernimmt digitalWrite(), delay() nur das Warten."),
                      ("Es hat keine Wirkung im Sketch.", False, "delay() blockiert den Ablauf tatsächlich für die angegebene Zeit."),
                    ]),
             ],
             solution=["<code>pinMode(13, OUTPUT);</code> in setup(); in loop(): <code>digitalWrite(13,HIGH); delay(1000); digitalWrite(13,LOW); delay(1000);</code>",
                       "<code>loop()</code> sorgt für die Dauerschleife (Wiederholung).",
                       "<code>delay(ms)</code> pausiert das Programm für Millisekunden."]),
        dict(no=9, sjw=9, kind="lernpfad", title="Steuerstrukturen im Sketch: das Ampelprogramm",
             goal="Du überträgst Verzweigung und Schleife in Arduino-Code und programmierst eine Fußgänger-/Auto-Ampel mit mehreren LEDs.",
             tasks=["Rot–Gelb–Grün-Phasen als Sequenz in <code>loop()</code> umsetzen.",
                    "Die Steuerstruktur im Ampelprogramm benennen (Dauerschleife).",
                    "Einen Taster als Eingabe ergänzen (Fußgängeranforderung, Verzweigung)."],
             tools=["arduino", "tinker"],
             fast="Ergänze eine zweite, um 90° versetzte Kreuzungsampel, die niemals gleichzeitig grün zeigt.",
             rlp=["RLP 2.2 · Kontrollstrukturen", "3.3 Verzweigung & Schleife"],
             vorwissen=[
               dict(fig="fig1", cap="Bild 1 · Ampelphasen als Sequenz", quiz=[
                 dict(q="Welche Phase zeigt Teil 1?",
                      done="Richtig — Rot.",
                      opts=[
                        ("Rot — die Ampel steht auf Halt.", True, None),
                        ("Gelb — Achtung, es wechselt gleich.", False, "Gelb ist Teil 2, das mittlere Feld."),
                        ("Grün — freie Fahrt.", False, "Grün ist Teil 3, das letzte Feld der Sequenz."),
                        ("Der Taster wird ausgewertet.", False, "Der Taster kommt erst in der nächsten Stunde vor, nicht in diesem Bild."),
                      ]),
                 dict(q="Welche Phase zeigt Teil 3?",
                      done="Genau — Grün.",
                      opts=[
                        ("Grün — freie Fahrt.", True, None),
                        ("Rot — die Ampel steht auf Halt.", False, "Rot ist Teil 1, das erste Feld."),
                        ("Gelb — Achtung, es wechselt gleich.", False, "Gelb ist Teil 2, das mittlere Feld."),
                        ("Der Sketch startet neu.", False, "Das Bild zeigt eine Ampelphase, keinen Neustart."),
                      ]),
                 dict(q="Wie heißt die Steuerstruktur bei Teil 4, die das Ganze wiederholt?",
                      done="Stimmt — die Dauerschleife.",
                      opts=[
                        ("die Dauerschleife (loop())", True, None),
                        ("eine einmalige Verzweigung", False, "Eine Verzweigung entscheidet einmalig, sie wiederholt nichts von selbst."),
                        ("eine Variable", False, "Eine Variable speichert nur einen Wert, sie wiederholt keine Abläufe."),
                        ("ein Kommentar im Code", False, "Kommentare haben keine Auswirkung auf den Programmablauf."),
                      ]),
                 dict(q="Warum müssen die drei Phasen ausgerechnet in loop() stehen?",
                      done="Richtig — sie sollen sich wiederholen.",
                      opts=[
                        ("Weil sie sich wiederholen sollen, solange die Ampel läuft.", True, None),
                        ("Weil sie nur einmal beim Start gebraucht werden.", False, "Genau das wäre die Aufgabe von setup(), nicht von loop()."),
                        ("Weil setup() dafür zu langsam ist.", False, "Geschwindigkeit ist nicht der Grund — es geht um Wiederholung."),
                        ("Das ist egal, sie könnten auch in setup() stehen.", False, "In setup() würden die Phasen nur einmal ablaufen, nicht wiederholt."),
                      ]),
               ]),
               dict(fig="fig2", cap="Bild 2 · Taster als Verzweigung", quiz=[
                 dict(q="Was ist Teil 1?",
                      done="Richtig — der Taster.",
                      opts=[
                        ("der Taster — er liefert HIGH oder LOW", True, None),
                        ("der Mikrocontroller", False, "Der Mikrocontroller ist der violette Chip, Teil 2."),
                        ("die Verzweigung", False, "Die Verzweigung ist die Raute weiter unten, Teil 3."),
                        ("eine LED", False, "In diesem Bild ist keine LED als eigenes Bauteil markiert."),
                      ]),
                 dict(q="Was ist Teil 2, der violette Chip?",
                      done="Genau — der Mikrocontroller.",
                      opts=[
                        ("der Mikrocontroller — er liest den Tasterzustand ein", True, None),
                        ("der Taster", False, "Der Taster ist das Bauteil links im Bild, Teil 1."),
                        ("die Steckplatine", False, "Eine Steckplatine ist in diesem Schaubild nicht eigens markiert."),
                        ("das USB-Kabel", False, "Ein USB-Kabel ist in diesem Bild nicht dargestellt."),
                      ]),
                 dict(q="Was ist Teil 3, die Raute?",
                      done="Stimmt — die Verzweigung.",
                      opts=[
                        ("die Verzweigung (if) — sie prüft den Tasterzustand", True, None),
                        ("die Dauerschleife", False, "Die Dauerschleife ist keine Raute, sie steckt im loop()-Block."),
                        ("eine Variable", False, "Eine Variable würde man nicht als Raute darstellen."),
                        ("der Mikrocontroller", False, "Der Mikrocontroller ist der Chip weiter oben, Teil 2."),
                      ]),
               ]),
             ],
             quiz=[
               dict(q="Welche Steuerstruktur sorgt dafür, dass sich die Ampelphasen ständig wiederholen?",
                    done="Richtig — die Dauerschleife.",
                    opts=[
                      ("die Dauerschleife (loop())", True, None),
                      ("eine einmalige Verzweigung", False, "Eine Verzweigung entscheidet einmalig, sie wiederholt nichts von selbst."),
                      ("eine Variable", False, "Eine Variable speichert nur einen Wert, sie wiederholt keine Abläufe."),
                      ("ein Kommentar im Code", False, "Kommentare haben keine Auswirkung auf den Programmablauf."),
                    ]),
               dict(q="Wie liest man einen Taster im Arduino-Sketch aus?",
                    done="Genau — als HIGH/LOW-Signal.",
                    opts=[
                      ("als HIGH- oder LOW-Signal, meist mit einer Verzweigung (if) abgefragt", True, None),
                      ("nur als Text", False, "Taster liefern elektrische Zustände (HIGH/LOW), keinen Text."),
                      ("er kann nicht ausgelesen werden", False, "Taster lassen sich sehr wohl über einen Digitalpin auslesen."),
                      ("nur über WLAN", False, "Ein einfacher Taster wird über ein Kabel am Digitalpin ausgelesen, nicht über WLAN."),
                    ]),
               dict(q="Wozu dient eine Verzweigung (if) beim Taster?",
                    done="Stimmt — sie entscheidet abhängig vom Tasterzustand.",
                    opts=[
                      ("um abhängig vom Tasterzustand zu entscheiden, was als Nächstes passiert (z. B. Fußgängeranforderung)", True, None),
                      ("um die Ampel dauerhaft auszuschalten", False, "Eine Verzweigung schaltet nicht automatisch alles aus, sie trifft eine Entscheidung."),
                      ("um die Schleife zu beenden", False, "Die Dauerschleife läuft weiter, die Verzweigung entscheidet nur über die nächste Aktion."),
                      ("um Strom zu sparen", False, "Das ist nicht die Funktion einer Verzweigung im Code."),
                    ]),
               dict(q="Wie setzt man die Reihenfolge Rot-Gelb-Grün typischerweise um?",
                    done="Richtig — als feste Sequenz mit digitalWrite und delay.",
                    opts=[
                      ("als Sequenz aus digitalWrite- und delay-Befehlen in fester Reihenfolge", True, None),
                      ("als zufällige Reihenfolge", False, "Eine Ampel muss eine feste, vorhersagbare Reihenfolge einhalten."),
                      ("nur mit einer einzigen LED", False, "Für Rot-Gelb-Grün braucht es mindestens drei separate LEDs."),
                      ("ganz ohne delay-Befehle", False, "Ohne delay() würden die Phasen nicht sichtbar lange anhalten."),
                    ]),
             ],
             solution=["Die Ampel wiederholt sich → Dauerschleife (<code>loop()</code>).",
                       "Taster liefert HIGH/LOW → Verzweigung mit <code>if</code>.",
                       "Phasen über <code>digitalWrite</code> + <code>delay</code> nacheinander."]),
        dict(no=10, sjw=10, kind="lernpfad", title="Objektorientierung entdecken: Attribute & Methoden",
             goal="Du lernst die Grundidee moderner Software (OOP): Objekte bündeln Daten (Attribute) und Fähigkeiten (Methoden). Du ordnest Code-Bereiche korrekt zu.",
             tasks=["An einem Beispiel Attribute (Eigenschaften) und Methoden (Aktionen) unterscheiden.",
                    "Fachbegriffe im Code zuordnen: Dauerschleife, Fallunterscheidung, Attribut, Methode.",
                    "Ein Alltagsobjekt (z. B. „Ampel“) als Klasse mit Attributen/Methoden skizzieren."],
             tools=[],
             fast="Modelliere das Objekt „Spielfigur“ mit drei Attributen und drei Methoden auf Papier.",
             rlp=["RLP 2.1 · Modellieren", "3.4 Objektorientierung", "neu · OOP-Einstieg"],
             vorwissen=[
               dict(fig="fig1", cap="Bild 1 · Klasse Ampel", quiz=[
                 dict(q="Was ist Teil 1?",
                      done="Richtig — der Klassenname.",
                      opts=[
                        ("der Klassenname (Ampel) — der Bauplan", True, None),
                        ("ein Attribut", False, "Attribute stehen im mittleren Bereich der Klassenbox, nicht im Kopf."),
                        ("eine Methode", False, "Methoden stehen im unteren Bereich der Klassenbox."),
                        ("ein konkretes Objekt", False, "Das konkrete Objekt ist die separate Box rechts im Bild."),
                      ]),
                 dict(q="Was zeigt Teil 3, der untere Bereich der Klassenbox?",
                      done="Genau — die Methoden.",
                      opts=[
                        ("die Methoden — ausführbare Aktionen wie naechstePhase()", True, None),
                        ("die Attribute — Eigenschaften wie aktuellePhase", False, "Attribute stehen im mittleren Bereich, nicht im unteren."),
                        ("den Klassennamen", False, "Der Klassenname steht ganz oben in der Box."),
                        ("ein konkretes Objekt", False, "Das konkrete Objekt ist eine eigene Box rechts im Bild."),
                      ]),
                 dict(q="Was ist Teil 4, die Box rechts?",
                      done="Stimmt — ein konkretes Objekt.",
                      opts=[
                        ("ein konkretes Objekt (meineAmpel) mit eigenen Werten", True, None),
                        ("die Klasse selbst", False, "Die Klasse ist die linke Box, der Bauplan."),
                        ("eine Methode", False, "Methoden stehen innerhalb einer Klassenbox, nicht als eigene Box."),
                        ("ein Attribut ohne Wert", False, "Die Werte rechts sind konkret gefüllt, nicht leer."),
                      ]),
                 dict(q='Warum hat das Objekt rechts konkrete Werte wie "rot" oder 3000?',
                      done="Richtig — ein Objekt ist eine Instanz mit echten Werten.",
                      opts=[
                        ("Weil ein Objekt eine Instanz der Klasse mit eigenen, echten Werten ist.", True, None),
                        ("Weil die Klasse ihre Attribute verliert, sobald ein Objekt entsteht.", False, "Die Klasse bleibt unverändert der Bauplan für beliebig viele Objekte."),
                        ("Weil Methoden automatisch Werte erzeugen.", False, "Die Werte kommen aus der konkreten Instanz, nicht automatisch aus Methoden."),
                        ("Das ist Zufall, es hat keine Bedeutung.", False, "Die konkreten Werte sind der ganze Sinn eines Objekts."),
                      ]),
               ]),
               dict(fig="fig2", cap="Bild 2 · Fachbegriffe im Code", quiz=[
                 dict(q="Wie heißt der Codeabschnitt 1?",
                      done="Richtig — die Dauerschleife.",
                      opts=[
                        ("die Dauerschleife — sie wiederholt sich endlos", True, None),
                        ("die Fallunterscheidung", False, "Die Fallunterscheidung ist der if/else-Abschnitt weiter unten."),
                        ("das Attribut", False, "Das Attribut ist die einzelne Variablenzeile ganz oben."),
                        ("die Methode", False, "Die Methode ist der Abschnitt mit dem Funktionskopf darüber."),
                      ]),
                 dict(q="Wie heißt der Codeabschnitt 2?",
                      done="Genau — die Fallunterscheidung.",
                      opts=[
                        ("die Fallunterscheidung — sie prüft eine Bedingung mit if/else", True, None),
                        ("die Dauerschleife", False, "Die Dauerschleife ist der loop()-Abschnitt darüber."),
                        ("das Attribut", False, "Das Attribut ist die einzelne Variablenzeile ganz oben."),
                        ("die Methode", False, "Die Methode hat einen eigenen Funktionskopf, keine if/else-Struktur."),
                      ]),
                 dict(q="Wie heißt der Codeabschnitt 3?",
                      done="Stimmt — das Attribut.",
                      opts=[
                        ("das Attribut — eine gespeicherte Eigenschaft", True, None),
                        ("die Methode", False, "Die Methode hat einen Funktionskopf mit Klammern, das Attribut nicht."),
                        ("die Dauerschleife", False, "Die Dauerschleife ist der loop()-Abschnitt."),
                        ("die Fallunterscheidung", False, "Die Fallunterscheidung ist der if/else-Abschnitt."),
                      ]),
               ]),
             ],
             quiz=[
               dict(q="Was ist ein Attribut in der Objektorientierung?",
                    done="Richtig — eine Eigenschaft bzw. ein Zustand.",
                    opts=[
                      ("eine Eigenschaft bzw. ein Zustand eines Objekts (z. B. farbe)", True, None),
                      ("eine ausführbare Aktion", False, "Das beschreibt eine Methode, kein Attribut."),
                      ("eine Dauerschleife", False, "Eine Dauerschleife ist eine Kontrollstruktur, kein Attribut."),
                      ("ein Kommentar im Code", False, "Kommentare sind reine Erklärtexte, keine Objekteigenschaften."),
                    ]),
               dict(q="Was ist eine Methode in der Objektorientierung?",
                    done="Genau — eine ausführbare Aktion.",
                    opts=[
                      ("eine ausführbare Aktion eines Objekts (z. B. schalteUm())", True, None),
                      ("eine Eigenschaft eines Objekts", False, "Das beschreibt ein Attribut, keine Methode."),
                      ("eine Variable ohne Funktion", False, "Methoden sind Aktionen, keine reinen Werte."),
                      ("ein Bauteil der Hardware", False, "Methoden gehören zur Softwarestruktur, nicht zur Hardware."),
                    ]),
               dict(q="Was gehört bei einer Klasse „Ampel“ zu den Attributen?",
                    done="Stimmt — die aktuelle Phase.",
                    opts=[
                      ("die aktuelle Phase (z. B. „rot“)", True, None),
                      ("die Methode naechstePhase()", False, "Das ist eine Methode (Aktion), kein Attribut."),
                      ("der Quellcode der Klasse", False, "Der Quellcode ist die Klasse selbst, kein einzelnes Attribut."),
                      ("die Steckplatine", False, "Die Steckplatine ist ein Hardware-Bauteil, kein Software-Attribut."),
                    ]),
               dict(q="Was bezeichnet man als Fallunterscheidung im Code?",
                    done="Richtig — eine if/else-Struktur.",
                    opts=[
                      ("eine if/else-Struktur, die abhängig von einer Bedingung entscheidet", True, None),
                      ("eine Dauerschleife", False, "Das ist eine Wiederholung, keine Entscheidung."),
                      ("eine Methode ohne Rückgabewert", False, "Das beschreibt eine bestimmte Art von Methode, keine Fallunterscheidung."),
                      ("ein Attribut", False, "Attribute speichern Eigenschaften, sie treffen keine Entscheidungen."),
                    ]),
             ],
             solution=["Attribut = Eigenschaft/Zustand (z. B. farbe); Methode = ausführbare Aktion (z. B. schalteUm()).",
                       "Dauerschleife = wiederholender Codeblock; Fallunterscheidung = if/else.",
                       "Klasse „Ampel“: Attribute (aktuellePhase), Methoden (naechstePhase())."]),
        dict(no=11, sjw=11, kind="projekt", title="Mini-Projekt Arduino + Ergebnissicherung",
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
                       "Backup an zwei Orten (Rechner + Cloud/USB)."]),
      ]),
 dict(hj=1, num="04", title="Wie Computer zählen — Zahlensysteme",
      key="#ffc23d", key2="#e39a00", tint="rgba(255,194,61,0.10)",
      lps=[
        dict(no=12, sjw=12, kind="lernpfad", title="Dual- & Dezimalsystem: Bits und Bytes",
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
        dict(no=13, sjw=13, kind="lernpfad", title="Umrechnen: Dezimal ↔ Dual ↔ Hexadezimal",
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
        dict(no=14, sjw=14, kind="lernpfad", title="Rechnen im Dualsystem & negative Zahlen",
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
        dict(no=15, sjw=15, kind="puffer", title="Puffer & Vertiefung: Zahlensystem-Challenge + Backup",
             goal="Reservestunde (Puffer): Wettkampf-Aufgaben zu Zahlensystemen, Aufholen von Rückständen und gemeinsame Ergebnissicherung vor den Weihnachtsferien.",
             tasks=["Stationen-Challenge: Umrechnen auf Zeit (dezimal/dual/hex).",
                    "Offene Fragen aus Einheit 04 klären, Sterne aktualisieren.",
                    "HJ1-Zwischenstand sichern (alle Dateien ins Backup)."],
             tools=[],
             fast="Erstelle drei knifflige Umrechnungsaufgaben mit Lösung für die Mitschüler:innen.",
             rlp=["RLP 2.5 · Reflektieren", "Puffer ~10 %"],
             solution=["Diese Stunde ist bewusst als Zeitpuffer eingeplant (Sonderveranstaltung/Aufholen).",
                       "Ziel: sichere Beherrschung der Umrechnungen + vollständiges Backup."]),
      ]),
 dict(hj=1, num="05", title="Von Blöcken zu Zeilen — Python-Einstieg",
      key="#ff5db8", key2="#e0338f", tint="rgba(255,93,184,0.10)",
      lps=[
        dict(no=16, sjw=16, kind="lernpfad", title="Warum Python? + WebTigerJython-Oberfläche",
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
        dict(no=17, sjw=17, kind="lernpfad", title="Erste Turtle-Programme: Vierecke & Dreiecke",
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
        dict(no=18, sjw=18, kind="lernpfad", title="Punkte, Positionen & Farben",
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
        dict(no=19, sjw=19, kind="lernpfad", title="Halbjahres-Check: vom Block zum Syntax-Code",
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
 dict(hj=2, num="06", title="Computergrafik mit Python (WebTigerJython)",
      key="#35e0ff", key2="#0bb7e0", tint="rgba(53,224,255,0.09)",
      lps=[
        dict(no=20, sjw=20, kind="lernpfad", title="Flaggen zeichnen: Rechtecke & Füllfarben",
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
        dict(no=21, sjw=21, kind="lernpfad", title="For-Schleifen I: Muster mit Zähler",
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
        dict(no=22, sjw=22, kind="lernpfad", title="For-Schleifen II: verschachtelte Schleifen",
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
        dict(no=23, sjw=23, kind="lernpfad", title="While-Schleifen & Bedingungen",
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
        dict(no=24, sjw=24, kind="lernpfad", title="Raster- vs. Vektorgrafik: Pixel oder Formel?",
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
        dict(no=25, sjw=25, kind="projekt", title="Grafik-Projekt + Ergebnissicherung",
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
 dict(hj=2, num="07", title="Datensicherheit & Kryptographie",
      key="#ff5d6c", key2="#e0333f", tint="rgba(255,93,108,0.10)",
      lps=[
        dict(no=26, sjw=26, kind="lernpfad", title="Passwörter & Kontosicherheit",
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
        dict(no=27, sjw=27, kind="lernpfad", title="Verschlüsselung verstehen: Cäsar & Substitution",
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
        dict(no=28, sjw=28, kind="lernpfad", title="Symmetrisch vs. asymmetrisch: der Schlüsseltausch",
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
        dict(no=29, sjw=29, kind="lernpfad", title="Hashing & Integrität: der Fingerabdruck von Daten",
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
        dict(no=30, sjw=30, kind="lernpfad", title="Datenschutz im Alltag: Metadaten & Grundrechte",
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
 dict(hj=2, num="08", title="Eigene Software — Vibe-Coding & Hosting",
      key="#34ff9e", key2="#12c47a", tint="rgba(52,255,158,0.09)",
      lps=[
        dict(no=31, sjw=31, kind="lernpfad", title="Vibe-Coding verstehen: präzises Prompting",
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
        dict(no=32, sjw=32, kind="lernpfad", title="Themenwahl & KI-Recherche: Kurzvortrag ODER App",
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
        dict(no=33, sjw=33, kind="lernpfad", title="Prototyp bauen mit jsfiddle.net",
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
        dict(no=34, sjw=34, kind="lernpfad", title="Auf GitHub veröffentlichen (GitHub Pages)",
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
        dict(no=35, sjw=35, kind="lernpfad", title="Die eigene Implementierung verstehen (Folien + Sprechtext)",
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
        dict(no=36, sjw=36, kind="lernpfad", title="Präsentationen: Kurzvorträge nach Kriterien",
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
        dict(no=37, sjw=37, kind="projekt", title="Abgabe, Backup & Ausblick",
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

def lp_filename(no):
    return "lernpfade/%s.html" % slug(no)

def kind_badge(kind):
    return {"lernpfad":"Lernpfad","projekt":"Projekt","puffer":"Puffer"}.get(kind,"Lernpfad")

def unlock_iso(sjw):
    # Lösung wird am Freitag der jeweiligen Schuljahreswoche freigeschaltet
    return iso(CAL[sjw][1])

TOTAL_LP = sum(len(u["lps"]) for u in UNITS)

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
    if hj == 1:
        pause = ('<div class="holiday"><b>// Unterrichtspausen im 1. Halbjahr:</b><br>'
                 'Herbstferien 19.10.–31.10.2026 · Weihnachtsferien ab 23.12.2026 (Wiederbeginn 04.01.2027)<br>'
                 'Kurzwochen je nach Kurstag beachten</div>')
    else:
        pause = ('<div class="holiday"><b>// Unterrichtspausen im 2. Halbjahr:</b><br>'
                 'Winterferien 01.02.–06.02.2027 · Frauentag (Mo 08.03.) · Osterferien 22.03.–02.04.2027<br>'
                 'Christi Himmelfahrt (Do 06.05.) + Brückentag (Fr 07.05.) · Pfingstmontag (Mo 17.05.) + frei (Di 18.05.)<br>'
                 'Schuljahresende vor den Sommerferien ab 01.07.2027</div>')
    buf = ('<div class="buffer"><b>// Zeitpuffer ~10&nbsp;%%:</b> Reserve- und Projektstunden (z. B. LP&nbsp;%s) '
           'sowie ferien-/feiertagsbedingte Kurzwochen federn Sonderveranstaltungen, Exkursionen und '
           'Aufholbedarf ab.</div>') % ("15 · 19" if hj == 1 else "25 · 30 · 32")
    return ('<section class="sem-content%s" id="hj%d-content">\n'
            '  <div class="%s">\n'
            '    <div class="sem-badge">HJ%d</div>\n'
            '    <div><h2>%s</h2><p class="period">%d Lernpfade · %s – %s</p></div>\n'
            '  </div>\n%s%s\n%s\n'
            '</section>\n') % (
        (" active" if hj == 1 else ""), hj, badge_cls, hj, esc(title),
        len(lps), de(d1), de(d2), body_units, pause, buf)

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
      <span>PROFIL INFORMATIK · KLASSE 9 · 14–15 J.</span>
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
      <span class="lg-item"><span class="lp-badge" style="background:#a56bff;color:#05070e">Puffer</span> Reserve (~10 %)</span>
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

    footer = '''
<footer>
  <div class="foot-inner">
    <div>
      <b class="h">PROFIL INFORMATIK · KLASSE 9</b><br>
      Profilkurs · 14–15 Jahre · Schuljahr 2026/27<br>
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
      Lösungen mit zeitlicher Freischaltung · ~10 % Puffer
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
        items += (
            '<div class="qz-item">'
            '<div class="qz-text"><span class="qn">%d.</span>%s</div>'
            '<div class="qz-opts">%s</div>'
            '<div class="qz-hint"></div><div class="qz-done">%s</div>'
            '</div>'
        ) % (i, q["q"], opts, q.get("done", "Richtig!"))
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
    if lp.get("fast"):
        fast = ('<section class="lp-sec"><div class="fast-box"><span class="fb-t">⚡ Schnellläufer:in</span>%s</div></section>'
                % lp["fast"])
    backup = ('<section class="lp-sec"><div class="backup-box"><span class="bb-t">💾 Ergebnissicherung</span>'
              'Sichere deine Ergebnisse am Stundenende <b>einfach wiederverwendbar</b> (sinnvoll benannt) an '
              '<b>zwei Orten</b> — Rechner und Cloud/USB. Achte selbstständig auf Backups.</div></section>')
    sol = "".join("<li>%s</li>" % s for s in lp["solution"])
    solution = ('<section class="sol" id="loesung" data-unlock="%s">'
                '<h2>Musterlösung <span class="sol-status">…</span></h2>'
                '<p class="sol-countdown"></p>'
                '<div class="sol-body" hidden><ul class="sol-list">%s</ul></div>'
                '<p class="sol-hint">Die Lösung wird automatisch zum angegebenen Datum sichtbar — '
                'die Seite prüft das bei jedem Laden.</p>'
                '</section>') % (unlock_iso(lp["sjw"]), sol)

    doc = (
        '<!DOCTYPE html>\n<html lang="de">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>LP%02d · %s</title>\n' % (lp["no"], esc(lp["title"]))
        + FONTS + '\n<style>\n' + THEME_CSS + '\n</style>\n</head>\n'
        '<body style="%s">\n' % style
        + '<canvas id="matrix-canvas"></canvas>\n'
        + '<div class="lp-page">\n'
        + '  <a class="back" href="../index.html#hj%d-content">← zur Kursübersicht</a>\n' % u["hj"]
        + '  <div class="lp-hero">\n'
        + '    <div class="lp-meta"><span>Einheit %s · %s</span><span>SJW %d · %s</span><span>%s</span></div>\n'
          % (u["num"], esc(u["title"]), lp["sjw"], de(mon), kind_badge(lp["kind"]))
        + '    <h1>%s</h1>\n' % esc(lp["title"])
        + '    <div class="lp-big">%02d</div>\n' % lp["no"]
        + '  </div>\n'
        + '  <section class="lp-sec"><h2>Das lernst du</h2><p>%s</p><div data-selfcheck="%s"></div></section>\n'
          % (lp["goal"], slug(lp["no"]))
        + ('  %s\n' % render_vorwissen(lp) if lp.get("vorwissen") else '')
        + '  <section class="lp-sec"><h2>Aufgaben</h2><ul class="task-list">%s</ul></section>\n' % tasks
        + ('  %s\n' % render_quiz(lp) if lp.get("quiz") else '')
        + ('  %s\n' % tools if tools else '')
        + ('  %s\n' % fast if fast else '')
        + '  %s\n' % backup
        + '  %s\n' % solution
        + '  <a class="back" href="../index.html#hj%d-content" style="margin-top:1.6rem">← zurück zur Kursübersicht</a>\n' % u["hj"]
        + '</div>\n'
        + '<script>\n' + THEME_JS + '\n</script>\n</body>\n</html>\n'
    )
    with open(os.path.join(LP_DIR, "%s.html" % slug(lp["no"])), "w", encoding="utf-8") as f:
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
print("HJ1 SJW1 Freischaltung:", unlock_iso(1), "| HJ2 letzte:", unlock_iso(37))
