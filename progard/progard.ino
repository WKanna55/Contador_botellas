void setup(){
  Serial.begin(9600);
}

void loop(){
  for (int i = 1; i<1000; i++){

    Serial.print("CUENTA: ");
    Serial.println(i);
    Serial.println("mostrar");
    delay(2500);
    if (i % 5 == 0){
      delay(25000);
      Serial.println("mostrar");
      delay(4000);
    }
  }
}