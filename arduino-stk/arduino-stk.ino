#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);

#define SENSOR_PIN A2
#define WET_THRESHOLD 210
#define DRY_THRESHOLD 510

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
}

void loop() {
  int value = analogRead(SENSOR_PIN);

  // 1) Pintar en el LCD
  lcd.setCursor(1,0);
  lcd.print("Moisture value");
  lcd.setCursor(3,1);
  lcd.print(value);
  lcd.print("   ");
  int pct = map(value, WET_THRESHOLD, DRY_THRESHOLD, 100, 0);
  pct = constrain(pct, 0, 100);
  lcd.setCursor(10,1);
  lcd.print(pct);
  lcd.print("% ");

  // 2) Enviar por Serial
  Serial.print("Raw: ");
  Serial.print(value);
  Serial.print("  |  H2O%: ");
  Serial.print(pct);
  Serial.println("%");

  delay(500);
}
