// Projekt A · Gießwächter, Tinkercad-Fassung (Sitzung 07)
// Potentiometer statt Wasserstandssensor: Schleifer an A0, äußere Beine an 5V und GND
// LED grün an Pin 7, LED rot an Pin 8 (je mit 220 Ohm an GND)
int wert = 0;
int schwelle = 200;

void setup()
{
  pinMode(A0, INPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  wert = analogRead(A0);
  Serial.println(wert);
  if (wert < schwelle) {
    // zu wenig Wasser: rot
    digitalWrite(7, LOW);
    digitalWrite(8, HIGH);
  } else {
    // genug Wasser: grün
    digitalWrite(7, HIGH);
    digitalWrite(8, LOW);
  }
  delay(1000); // 1 Sekunde warten
}
