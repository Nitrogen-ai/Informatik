// K1 Lichtring mit Drehregler · Tinkercad (NeoPixel-Ring 12) und echter Arduino (WS2812-Ring, 12 LEDs)
// Ring: DI/IN an Pin 6 (echt: über 330 Ω), 5V an 5V, GND an GND. Potentiometer: Mitte an A0, außen 5V und GND.
// Bibliothek: „Adafruit NeoPixel“ (in Tinkercad und im Cloud Editor vorhanden).
#include <Adafruit_NeoPixel.h>

const int ANZAHL = 12;
Adafruit_NeoPixel ring(ANZAHL, 6, NEO_GRB + NEO_KHZ800);

// Farbrad: 0..255 → Regenbogenfarbe (aus dem Adafruit-Beispiel „strandtest“)
uint32_t farbrad(byte pos) {
  pos = 255 - pos;
  if (pos < 85) return ring.Color(255 - pos * 3, 0, pos * 3);
  if (pos < 170) { pos -= 85; return ring.Color(0, pos * 3, 255 - pos * 3); }
  pos -= 170;
  return ring.Color(pos * 3, 255 - pos * 3, 0);
}

int start = 0;

void setup() {
  ring.begin();
  ring.setBrightness(40);   // WICHTIG am echten Ring: USB liefert nur ca. 500 mA
}

void loop() {
  int poti = analogRead(A0);                 // 0..1023
  int tempo = map(poti, 0, 1023, 30, 300);   // Wartezeit in ms
  for (int i = 0; i < ANZAHL; i++) {
    ring.setPixelColor(i, 0);                // alle aus
  }
  for (int k = 0; k < 4; k++) {              // Schweif aus 4 LEDs mit Regenbogenfarben
    int pos = (start + k) % ANZAHL;
    ring.setPixelColor(pos, farbrad((pos * 256 / ANZAHL) & 255));
  }
  ring.show();
  start = (start + 1) % ANZAHL;
  delay(tempo);
}
