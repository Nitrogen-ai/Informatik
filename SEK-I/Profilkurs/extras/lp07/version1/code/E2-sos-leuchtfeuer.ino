// E2 SOS-Leuchtfeuer · Tinkercad und echter Arduino
// LED (weiß) mit 220 Ω an Pin 8, Piezo/Buzzer an Pin 9 und GND.
// Morse: kurz = 1 Einheit, lang = 3 Einheiten, Pause zwischen Buchstaben = 3 Einheiten.

const int LED = 8;
const int TON = 9;
const int EINHEIT = 200;   // Millisekunden

void zeichen(int dauer) {
  digitalWrite(LED, HIGH);
  tone(TON, 880);          // Ton mit 880 Hz
  delay(dauer);
  digitalWrite(LED, LOW);
  noTone(TON);
  delay(EINHEIT);          // kurze Pause nach jedem Zeichen
}

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  zeichen(EINHEIT); zeichen(EINHEIT); zeichen(EINHEIT);              // S  · · ·
  delay(2 * EINHEIT);
  zeichen(3 * EINHEIT); zeichen(3 * EINHEIT); zeichen(3 * EINHEIT);  // O  − − −
  delay(2 * EINHEIT);
  zeichen(EINHEIT); zeichen(EINHEIT); zeichen(EINHEIT);              // S  · · ·
  delay(7 * EINHEIT);      // Pause vor der Wiederholung
}
