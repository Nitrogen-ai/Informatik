// E1 Lauflicht (Lichterkette) · Tinkercad und echter Arduino
// 4 LEDs (blau, gelb, weiß, grün) je mit 220-Ω-Widerstand an Pin 2, 3, 4, 5; Kathoden an GND.

void setup() {
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
}

void loop() {
  // Hinweg: jede LED kurz an, dann wieder aus
  digitalWrite(2, HIGH); delay(150); digitalWrite(2, LOW);
  digitalWrite(3, HIGH); delay(150); digitalWrite(3, LOW);
  digitalWrite(4, HIGH); delay(150); digitalWrite(4, LOW);
  digitalWrite(5, HIGH); delay(150); digitalWrite(5, LOW);
  // Rückweg (wie beim Auto „K.I.T.T.“)
  digitalWrite(4, HIGH); delay(150); digitalWrite(4, LOW);
  digitalWrite(3, HIGH); delay(150); digitalWrite(3, LOW);
}

// Erweiterung: dieselbe Bewegung mit einer for-Schleife
// for (int pin = 2; pin <= 5; pin++) { digitalWrite(pin, HIGH); delay(150); digitalWrite(pin, LOW); }
