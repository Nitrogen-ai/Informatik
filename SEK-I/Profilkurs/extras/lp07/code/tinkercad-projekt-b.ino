// Projekt B · Filterwächter, Tinkercad-Fassung (Sitzung 07)
// Potentiometer statt TDS-Sensor: Schleifer an A1, äußere Beine an 5V und GND
// LED grün an Pin 7, LED rot an Pin 8 (je mit 220 Ohm an GND)
int wert = 0;
int schwelle = 600;

void setup()
{
  pinMode(A1, INPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  wert = analogRead(A1);
  Serial.println(wert);
  if (wert > schwelle) {
    // viele gelöste Stoffe: Kartusche wechseln, rot
    digitalWrite(7, LOW);
    digitalWrite(8, HIGH);
  } else {
    // Filter arbeitet: grün
    digitalWrite(7, HIGH);
    digitalWrite(8, LOW);
  }
  delay(1000); // 1 Sekunde warten
}
