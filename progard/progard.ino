void setup(){
  Serial.begin(9600);
}

void loop(){
  for (int i = 0; i<1000; i++){

    Serial.print("CUENTA: ");
    Serial.println(i);
    delay(1000);
  }
}