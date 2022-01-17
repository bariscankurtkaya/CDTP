#include <LiquidCrystal.h>
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

int x;

void setup() {
 Serial.begin(115200);
 Serial.setTimeout(1);
 lcd.begin(16, 2);
  // Print a message to the LCD.
}

void loop() {
 while (!Serial.available());
 x = Serial.readString().toInt();
 Serial.print(x + 1);
 lcd.setCursor(0, 1);
 // print the number of seconds since reset:
 lcd.clear();
 if (x == 1) {
   lcd.print("Dur Levhasi");
 }else if (x == 2){
   lcd.print("Insan");
 }else if (x == 3){
   lcd.print("Hayvan");
 }else if (x == 4){
   lcd.print("Tir");
 }else if (x == 5){
   lcd.print("Tas");
 }else{
   lcd.print("Iyi Yolculuklar");
 }
}
