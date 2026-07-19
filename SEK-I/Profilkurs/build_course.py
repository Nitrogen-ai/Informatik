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
