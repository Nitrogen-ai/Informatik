// 07 Schritt 1 · Der Tastendruck als Variable
// So erzeugt Tinkercad den Code aus den Codeblöcken (Ansicht „Text“).
// Taster: ein Bein an 5V, das andere an Pin 12 und über 10 kΩ an GND (Pull-down).
// LED (blau): über 220 Ω an Pin 7, Kathode an GND.

int Tastendruck = 0;

void setup()
{
  pinMode(12, INPUT);
  pinMode(7, OUTPUT);
  Serial.begin(9600);

  Tastendruck = 0;
  Serial.println(Tastendruck);
  while (!(Tastendruck == 5)) {
    if (digitalRead(12) == HIGH) {
      digitalWrite(7, HIGH);
      delay(500); // Wait for 500 millisecond(s)
      digitalWrite(7, LOW);
      delay(500); // Wait for 500 millisecond(s)
      Tastendruck = (Tastendruck + 1);
      Serial.println(Tastendruck);
    }
  }
}

void loop()
{
  delay(10); // Delay a little bit to improve simulation performance
}
