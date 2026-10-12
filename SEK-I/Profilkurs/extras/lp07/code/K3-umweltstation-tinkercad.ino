// K3 Umweltstation: Temperatur auf dem Lichtring · Version für TINKERCAD
// TMP36 an A0 (wie M3), NeoPixel-Ring 12 an Pin 6, Potentiometer an A1 als Ersatz für den TDS-Sensor.
#include <Adafruit_NeoPixel.h>

Adafruit_NeoPixel ring(12, 6, NEO_GRB + NEO_KHZ800);

void zeigeTemperatur(float t) {
  // 15 °C → 1 LED, 30 °C → 12 LEDs
  int an = map((int)(t * 10), 150, 300, 1, 12);
  an = constrain(an, 1, 12);
  uint32_t farbe;
  if (t < 20)       farbe = ring.Color(0, 0, 255);    // kalt: blau
  else if (t <= 24) farbe = ring.Color(0, 255, 0);    // angenehm: grün
  else              farbe = ring.Color(255, 0, 0);    // warm: rot
  for (int i = 0; i < 12; i++) {
    ring.setPixelColor(i, i < an ? farbe : 0);
  }
  ring.show();
}

void setup() {
  ring.begin();
  ring.setBrightness(40);
  Serial.begin(9600);
}

void loop() {
  float t = (analogRead(A0) * 5.0 / 1024.0 - 0.5) * 100.0;
  int wasser = analogRead(A1);             // Platzhalter für den TDS-Sensor
  Serial.print("Temperatur: "); Serial.print(t); Serial.print(" °C   Wasserwert: "); Serial.println(wasser);
  zeigeTemperatur(t);
  delay(1000);
}
