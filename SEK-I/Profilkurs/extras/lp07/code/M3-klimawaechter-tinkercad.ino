// M3 Klimawächter fürs Klassenzimmer · Version für TINKERCAD (Temperatursensor TMP36)
// TMP36: linkes Bein 5V, Mitte an A0, rechtes Bein GND (flache Seite zu dir).
// LEDs mit 220 Ω: blau 12 (zu kalt), grün 11 (angenehm), gelb 10 (zu warm).

void setup() {
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  float spannung = analogRead(A0) * 5.0 / 1024.0;   // Messwert in Volt
  float temperatur = (spannung - 0.5) * 100.0;      // TMP36: 0,5 V = 0 °C, 10 mV pro °C
  Serial.print("Temperatur: ");
  Serial.print(temperatur);
  Serial.println(" °C");

  digitalWrite(10, LOW); digitalWrite(11, LOW); digitalWrite(12, LOW);
  if (temperatur < 20) {
    digitalWrite(12, HIGH);
  } else if (temperatur <= 24) {
    digitalWrite(11, HIGH);
  } else {
    digitalWrite(10, HIGH);
  }
  delay(1000);
}
