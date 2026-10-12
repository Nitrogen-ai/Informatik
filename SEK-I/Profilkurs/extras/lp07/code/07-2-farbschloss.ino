// 07 Schritt 2 · Das Farbschloss (Escape Room)
// Taster blau 12, grün 11, gelb 10, weiß 9 (je mit 10 kΩ Pull-down nach GND, anderes Bein an 5V)
// LEDs blau 7, grün 6, gelb 5, weiß 4 (je über 220 Ω), Piezo/Buzzer an Pin 8.
// Jede Farbe ist eine Ziffer: blau 1, grün 2, gelb 3, weiß 4.
// Nach vier Tastendrücken wird Code mit dem Geheimcode verglichen.

int Code = 0;
int Tastendruck = 0;

void setup()
{
  pinMode(12, INPUT);
  pinMode(11, INPUT);
  pinMode(10, INPUT);
  pinMode(9, INPUT);
  pinMode(7, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);
  Serial.begin(9600);

  Code = 0;
  Tastendruck = 0;
}

void loop()
{
  if (digitalRead(12) == HIGH) {        // blau = 1
    digitalWrite(7, HIGH);
    delay(500); // Wait for 500 millisecond(s)
    digitalWrite(7, LOW);
    Code = (Code * 10 + 1);
    Tastendruck = (Tastendruck + 1);
    Serial.println(Code);
  }
  if (digitalRead(11) == HIGH) {        // grün = 2
    digitalWrite(6, HIGH);
    delay(500); // Wait for 500 millisecond(s)
    digitalWrite(6, LOW);
    Code = (Code * 10 + 2);
    Tastendruck = (Tastendruck + 1);
    Serial.println(Code);
  }
  if (digitalRead(10) == HIGH) {        // gelb = 3
    digitalWrite(5, HIGH);
    delay(500); // Wait for 500 millisecond(s)
    digitalWrite(5, LOW);
    Code = (Code * 10 + 3);
    Tastendruck = (Tastendruck + 1);
    Serial.println(Code);
  }
  if (digitalRead(9) == HIGH) {         // weiß = 4
    digitalWrite(4, HIGH);
    delay(500); // Wait for 500 millisecond(s)
    digitalWrite(4, LOW);
    Code = (Code * 10 + 4);
    Tastendruck = (Tastendruck + 1);
    Serial.println(Code);
  }
  if (Tastendruck == 4) {
    if (Code == 1334) {                 // Geheimcode: blau, gelb, gelb, weiß
      Serial.println("offen");
      tone(8, 880, 1000); // play tone 69 (A5 = 880 Hz)
      delay(1000); // Wait for 1000 millisecond(s)
    } else {
      Serial.println("falsch");
      tone(8, 131, 1000); // play tone 48 (C3 = 131 Hz)
      delay(1000); // Wait for 1000 millisecond(s)
    }
    Code = 0;
    Tastendruck = 0;
  }
  delay(10); // Delay a little bit to improve simulation performance
}
