// M1 Bedarfsampel mit Taster · Tinkercad und echter Arduino
// Autoampel rot 13, gelb 12, grün 11 · Fußgänger rot 10, grün 9 (je 220 Ω)
// Taster: ein Bein an Pin 2, das gegenüberliegende an GND (INPUT_PULLUP: gedrückt = LOW).

const int TASTER = 2;

void setze(int rot, int gelb, int gruen, int fRot, int fGruen, int ms) {
  digitalWrite(13, rot); digitalWrite(12, gelb); digitalWrite(11, gruen);
  digitalWrite(10, fRot); digitalWrite(9, fGruen);
  delay(ms);
}

void setup() {
  for (int pin = 9; pin <= 13; pin++) pinMode(pin, OUTPUT);
  pinMode(TASTER, INPUT_PULLUP);
}

void loop() {
  setze(LOW, LOW, HIGH, HIGH, LOW, 0);       // Grundzustand: Autos grün, Fußgänger rot
  if (digitalRead(TASTER) == LOW) {          // jemand drückt
    delay(2000);                             // kurze Wartezeit wie an einer echten Ampel
    setze(LOW,  HIGH, LOW, HIGH, LOW,  1000); // Gelb
    setze(HIGH, LOW,  LOW, HIGH, LOW,  1000); // alle Rot
    setze(HIGH, LOW,  LOW, LOW,  HIGH, 5000); // Fußgänger grün
    setze(HIGH, LOW,  LOW, HIGH, LOW,  1000); // Räumzeit
    setze(HIGH, HIGH, LOW, HIGH, LOW,  1000); // Rot-Gelb
  }
}
