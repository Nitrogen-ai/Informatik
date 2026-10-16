// Sensor 1 · DHT11 (Temperatur und Luftfeuchte)
// Bein 1 an 5V, Bein 2 an Pin 2, Bein 3 frei, Bein 4 an GND
// 10 kΩ (braun-schwarz-orange) zwischen Bein 1 und Bein 2
#include <DHT.h>

DHT dht(2, DHT11);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  // nur alle 2 s messen
  delay(2000);
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  if (isnan(t) || isnan(h)) {
    Serial.println("Sensorfehler: Kabel pruefen");
    return;
  }
  Serial.print("Temperatur: ");
  Serial.print(t);
  Serial.print(" C, Luftfeuchte: ");
  Serial.print(h);
  Serial.println(" %");
}
