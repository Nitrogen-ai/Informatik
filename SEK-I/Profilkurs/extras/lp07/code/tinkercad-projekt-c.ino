// Projekt C · Lüftungswächter, Tinkercad-Fassung (Sitzung 07)
// TMP36 an A2 (Temperatur), Potentiometer an A3 (ersetzt die Luftfeuchte)
// LED grün an Pin 7, LED rot an Pin 8 (je mit 220 Ohm an GND)
int t = 0;
int h = 0;
int maxT = 25;
int maxH = 60;

void setup()
{
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  t = -40 + 0.488155 * (analogRead(A2) - 20);
  h = map(analogRead(A3), 0, 1023, 0, 100);
  Serial.print("Temperatur: ");
  Serial.print(t);
  Serial.print(" C, Luftfeuchte: ");
  Serial.print(h);
  Serial.println(" %");
  if (t > maxT && h > maxH) {
    // warm und feucht: lüften, rot
    digitalWrite(7, LOW);
    digitalWrite(8, HIGH);
  } else {
    // Luft in Ordnung: grün
    digitalWrite(7, HIGH);
    digitalWrite(8, LOW);
  }
  delay(2000); // 2 Sekunden warten
}
