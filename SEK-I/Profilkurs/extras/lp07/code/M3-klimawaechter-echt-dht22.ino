// M3 Klimawächter fürs Klassenzimmer · Version für den ECHTEN Arduino mit DHT22
// Bibliothek: „DHT sensor library“ (Adafruit), im Cloud Editor schon vorhanden.
// DHT22-Modul: + an 5V, out an Pin 2, − an GND. (Sensor ohne Platine: Pin 1 5V, Pin 2 Daten + 10 kΩ nach 5V, Pin 4 GND)
// LEDs mit 220 Ω: blau 12 (zu kalt), grün 11 (angenehm), gelb 10 (zu warm), weiß 9 (Luft zu feucht: lüften!)
#include <DHT.h>

DHT dht(2, DHT22);

void setup() {
  for (int pin = 9; pin <= 12; pin++) pinMode(pin, OUTPUT);
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(2000);                              // der DHT22 misst höchstens alle 2 Sekunden
  float temperatur = dht.readTemperature();
  float feuchte = dht.readHumidity();
  if (isnan(temperatur) || isnan(feuchte)) {
    Serial.println("Sensorfehler: Kabel prüfen");
    return;
  }
  Serial.print("Temperatur: "); Serial.print(temperatur); Serial.print(" °C   ");
  Serial.print("Luftfeuchte: "); Serial.print(feuchte); Serial.println(" %");

  digitalWrite(10, LOW); digitalWrite(11, LOW); digitalWrite(12, LOW);
  if (temperatur < 20) {
    digitalWrite(12, HIGH);
  } else if (temperatur <= 24) {
    digitalWrite(11, HIGH);
  } else {
    digitalWrite(10, HIGH);
  }
  digitalWrite(9, feuchte > 60 ? HIGH : LOW);
}
