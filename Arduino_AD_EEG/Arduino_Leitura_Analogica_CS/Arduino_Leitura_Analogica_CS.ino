byte MSB, LSB;
char SB='S',EB='E',C3='3',CZ='Z',C4='4';
int i=0;
unsigned short int val;
void setup() {
  Serial.begin(250000);
  pinMode(A0,INPUT);
}

void loop() {
    Serial.write(SB);//start byte
    val=analogRead(A0);
    //dados do eletrodo C3
    MSB=byte(val>>8);
    LSB=byte(val&0xff);
    Serial.write(C3);//identificador eletrodo C3
    Serial.write(MSB);//more significant byte C3
    Serial.write(LSB);//less significant byte C3
    //Serial.println(val);
    Serial.write(EB);//end byte
  
    delay(4);//delay 4 ms = 250 Hz 
  
}
