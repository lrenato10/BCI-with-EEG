unsigned short int Vc3[10]={
33713,
33599,
34101,
34054,
33499,
33803,
33550,
33809,
33648,
33530
};
unsigned short int Vcz[10]={
32676,
33104,
33158,
33553,
33239,
34010,
33665,
33544,
34200,
33873
};
unsigned short int Vc4[10]={
34079,
34023,
33992,
33804,
33884,
33835,
33684,
33599,
33645,
33379
};

byte MSB, LSB;
char SB='S',EB='E',C3='3',CZ='Z',C4='4';
int i=0;
void setup() {
  Serial.begin(9600);

}

void loop() {
  if (i<10){
    Serial.write(SB);//start byte
  
    //dados do eletrodo C3
    MSB=byte(Vc3[i]>>8);
    LSB=byte(Vc3[i]&0xff);
    Serial.write(C3);//identificador eletrodo C3
    Serial.write(MSB);//more significant byte C3
    Serial.write(LSB);//less significant byte C3
    
    //dados do eletrodo CZ
    MSB=byte(Vcz[i]>>8);
    LSB=byte(Vcz[i]&0xff);
    Serial.write(CZ);
    Serial.write(MSB);
    Serial.write(LSB);
    
    //dados do eletrodo C4
    MSB=byte(Vc4[i]>>8);
    LSB=byte(Vc4[i]&0xff);
    Serial.write(C4);
    Serial.write(MSB);
    Serial.write(LSB);
  
    Serial.write(EB);//end byte
    
    i++;
    delay(4);//delay 4 ms = 250 Hz 
  }
}
