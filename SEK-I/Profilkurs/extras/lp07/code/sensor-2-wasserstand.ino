// Sensor 2 · Wasserstandssensor
// Kabel: S an A0 (gelb), + an 5V (rot), - an GND (schwarz)

void setup() {
  Serial.begin(9600);
}

void loop() {
  // 0 = trocken ... ca. 600-700 = tief im Wasser
  int wert = analogRead(A0);
  Serial.print("Wasserstand: ");
  Serial.println(wert);
  delay(1000);
}
