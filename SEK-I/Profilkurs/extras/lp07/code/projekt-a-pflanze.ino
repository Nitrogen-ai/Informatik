// Projekt A · Gießwächter für Zimmerpflanzen (Musterlösung)
// Wasserstandssensor: S an A0, + an 5V, - an GND
// LED grün an Pin 7, LED rot an Pin 8 (je mit 220 Ohm an GND)
// Schwellenwert selbst messen: Sensor fast trocken = nachgießen
int schwelle = 200;

void setup() {
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int wert = analogRead(A0);
  Serial.print("Wasserstand: ");
  Serial.println(wert);
  if (wert < schwelle) {
    // zu wenig Wasser: rot
    digitalWrite(7, LOW);
    digitalWrite(8, HIGH);
  } else {
    // genug Wasser: grün
    digitalWrite(7, HIGH);
    digitalWrite(8, LOW);
  }
  delay(1000);
}
