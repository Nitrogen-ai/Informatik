// M2 Füllstandswarner (Hochwasser-Alarm) · Tinkercad und echter Arduino
// Tinkercad: Bodenfeuchtigkeitssensor · echt: Wasserstandssensor (S an A0, + an 5V, − an GND)
// LEDs mit 220 Ω: grün 11, gelb 12, blau 13 (Alarm); Buzzer/Piezo an Pin 9.
// Die Grenzwerte 100 und 350 sind Startwerte: im Seriellen Monitor messen und anpassen!

const int SENSOR = A0;

void setup() {
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int wert = analogRead(SENSOR);     // 0 (trocken) bis 1023
  Serial.print("Wasserstand: ");
  Serial.println(wert);

  digitalWrite(11, LOW); digitalWrite(12, LOW); digitalWrite(13, LOW);
  noTone(9);
  if (wert < 100) {
    digitalWrite(11, HIGH);          // trocken bis niedrig
  } else if (wert < 350) {
    digitalWrite(12, HIGH);          // Wasser steigt
  } else {
    digitalWrite(13, HIGH);          // Alarm
    tone(9, 1000);
  }
  delay(500);
}
