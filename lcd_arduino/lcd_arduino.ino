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
   lcd.print("1. Dur Levhasi");
 }else if (x == 2){
   lcd.print("1. Insan");
 }else if (x == 3){
   lcd.print(" Hayvan Var");
 }else if (x == 4){
   lcd.print("Tir Yanlis Serit");
 }else if (x == 5){
   lcd.print("1. Tas");
 }else if (x == 6) {
   lcd.print("2. Dur Levhasi");
 }else if (x == 7){
   lcd.print("2. Insan");
 }else if (x == 8){
   lcd.print("2. Hayvan");
 }else if (x == 9){
   lcd.print("2. Tir");
 }else if (x == 10){
   lcd.print("2. Tas");
 }
 else{
   lcd.print("Iyi Yolculuklar");
 }
}
