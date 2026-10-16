// Projekt B · Filterwächter für den Wasserfilter (Musterlösung)
// CQRobot TDS: grün (Signal) an A1, rot (+) an 5V, schwarz (-) an GND
// LED grün an Pin 7, LED rot an Pin 8 (je mit 220 Ohm an GND)
// Schwellenwert selbst messen: Leitungswasser und frisch gefiltertes Wasser vergleichen
float schwelle = 400.0;
float wassertemperatur = 25.0;

void setup() {
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
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
  Serial.print("TDS: ");
  Serial.print(tds, 0);
  Serial.println(" ppm");
  if (tds > schwelle) {
    // Filter filtert kaum noch: rot
    digitalWrite(7, LOW);
    digitalWrite(8, HIGH);
  } else {
    // Filter arbeitet: grün
    digitalWrite(7, HIGH);
    digitalWrite(8, LOW);
  }
  delay(1000);
}
