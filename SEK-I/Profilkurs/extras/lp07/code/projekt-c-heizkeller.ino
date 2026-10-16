// Projekt C · Lüftungswächter für den Heizkeller (Musterlösung)
// DHT11: Bein 1 an 5V, Bein 2 an Pin 2, Bein 3 frei, Bein 4 an GND, 10 kOhm zwischen Bein 1 und 2
// LED grün an Pin 7, LED rot an Pin 8 (je mit 220 Ohm an GND)
#include <DHT.h>

DHT dht(2, DHT11);
float maxTemperatur = 25.0;
float maxFeuchte = 60.0;

void setup() {
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
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
  if (t > maxTemperatur && h > maxFeuchte) {
    // warm und feucht: lüften, rot
    digitalWrite(7, LOW);
    digitalWrite(8, HIGH);
  } else {
    // alles in Ordnung: grün
    digitalWrite(7, HIGH);
    digitalWrite(8, LOW);
  }
}
