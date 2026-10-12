// K3 Umweltstation: Temperatur auf dem Lichtring · Version für den ECHTEN Arduino
// DHT22 an Pin 2 (wie M3), WS2812-Ring (12 LEDs) DI über 330 Ω an Pin 6, 5V, GND.
// Bonus: TDS-Sensor (CQRobot) A an A1, + an 5V, − an GND: misst gelöste Stoffe im Wasser in ppm.
// Bibliotheken: „Adafruit NeoPixel“, „DHT sensor library“.
#include <Adafruit_NeoPixel.h>
#include <DHT.h>

Adafruit_NeoPixel ring(12, 6, NEO_GRB + NEO_KHZ800);
DHT dht(2, DHT22);

void zeigeTemperatur(float t) {
  int an = map((int)(t * 10), 150, 300, 1, 12);
  an = constrain(an, 1, 12);
  uint32_t farbe;
  if (t < 20)       farbe = ring.Color(0, 0, 255);
  else if (t <= 24) farbe = ring.Color(0, 255, 0);
  else              farbe = ring.Color(255, 0, 0);
  for (int i = 0; i < 12; i++) {
    ring.setPixelColor(i, i < an ? farbe : 0);
  }
  ring.show();
}

float tdsMessen(float temperatur) {
  float u = analogRead(A1) * 5.0 / 1024.0;                // Spannung in V
  float u25 = u / (1.0 + 0.02 * (temperatur - 25.0));     // auf 25 °C umrechnen
  return (133.42 * u25 * u25 * u25 - 255.86 * u25 * u25 + 857.39 * u25) * 0.5;  // Formel des Herstellers
}

void setup() {
  ring.begin();
  ring.setBrightness(40);   // USB liefert nur ca. 500 mA
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(2000);
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  if (isnan(t)) {
    Serial.println("Sensorfehler: DHT22-Kabel prüfen");
    return;
  }
  Serial.print("Temperatur: "); Serial.print(t); Serial.print(" °C   Luftfeuchte: "); Serial.print(h);
  Serial.print(" %   TDS: "); Serial.print(tdsMessen(t)); Serial.println(" ppm");
  zeigeTemperatur(t);
}
