// K2 Reaktionsspiel · Tinkercad und echter Arduino
// LED (grün) mit 220 Ω an Pin 8, Taster zwischen Pin 2 und GND, Piezo/Buzzer an Pin 9.
// Ergebnisse im Seriellen Monitor (9600 Baud).

const int LED = 8, TASTER = 2, TON = 9;
unsigned long rekord = 0;    // 0 = noch kein Rekord

void setup() {
  pinMode(LED, OUTPUT);
  pinMode(TASTER, INPUT_PULLUP);
  Serial.begin(9600);
  randomSeed(analogRead(A5)); // offener Pin liefert Zufallsrauschen
}

void loop() {
  Serial.println("Mach dich bereit ...");
  while (digitalRead(TASTER) == LOW) {}      // warten, bis der Taster losgelassen ist
  unsigned long ziel = millis() + random(2000, 5000);
  while (millis() < ziel) {
    if (digitalRead(TASTER) == LOW) {        // Mogelschutz
      Serial.println("Zu früh gedrückt!");
      tone(TON, 200, 400);
      delay(1500);
      return;                                // neue Runde
    }
  }
  digitalWrite(LED, HIGH);
  tone(TON, 1000, 100);
  unsigned long start = millis();
  while (digitalRead(TASTER) == HIGH) {}     // warten auf den Druck
  unsigned long zeit = millis() - start;
  digitalWrite(LED, LOW);

  Serial.print("Reaktionszeit: ");
  Serial.print(zeit);
  Serial.println(" ms");
  if (rekord == 0 || zeit < rekord) {
    rekord = zeit;
    Serial.println("Neuer Rekord!");
    tone(TON, 1500, 300);
  }
  delay(2000);
}
