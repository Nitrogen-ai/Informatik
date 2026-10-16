// Sensor 3 · CQRobot Ocean TDS (Leitfähigkeit)
// Kabel: grün (Signal) an A1, rot (+) an 5V, schwarz (-) an GND
// Formel aus dem CQRobot-Wiki, Wassertemperatur fest 25 °C
float wassertemperatur = 25.0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // 30 Messungen mitteln
  long summe = 0;
  for (int i = 0; i < 30; i++) {
    summe += analogRead(A1);
    delay(20);
  }
  float spannung = summe / 30.0 * 5.0 / 1024.0;
  float faktor = 1.0 + 0.02 * (wassertemperatur - 25.0);
  float v = spannung / faktor;
  float tds = (133.42 * v * v * v - 255.86 * v * v + 857.39 * v) * 0.5;
  Serial.print("Spannung: ");
  Serial.print(spannung, 2);
  Serial.print(" V, TDS: ");
  Serial.print(tds, 0);
  Serial.println(" ppm");
  delay(1000);
}
