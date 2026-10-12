// E3 Ampel mit Fußgängerampel · Tinkercad und echter Arduino
// Autoampel: rot 13, gelb 12, grün 11 · Fußgängerampel: rot 10, grün 9 · je 220 Ω, Kathoden an GND.

void setze(int rot, int gelb, int gruen, int fRot, int fGruen, int ms) {
  digitalWrite(13, rot);
  digitalWrite(12, gelb);
  digitalWrite(11, gruen);
  digitalWrite(10, fRot);
  digitalWrite(9, fGruen);
  delay(ms);
}

void setup() {
  for (int pin = 9; pin <= 13; pin++) pinMode(pin, OUTPUT);
}

void loop() {
  //    rot   gelb  grün  F-rot F-grün  Dauer
  setze(LOW,  LOW,  HIGH, HIGH, LOW,   5000);  // Autos fahren
  setze(LOW,  HIGH, LOW,  HIGH, LOW,   1000);  // Gelb
  setze(HIGH, LOW,  LOW,  HIGH, LOW,   1000);  // Räumzeit: alle Rot
  setze(HIGH, LOW,  LOW,  LOW,  HIGH,  4000);  // Fußgänger gehen
  setze(HIGH, LOW,  LOW,  HIGH, LOW,   1000);  // Räumzeit
  setze(HIGH, HIGH, LOW,  HIGH, LOW,   1000);  // Rot-Gelb
}
