// **********************************************
// Define the Arduino pins used for SPI interface
// **********************************************
#define SELPIN 10    // Selection pin (CS)
#define DATAOUT 11   // MOSI (Din)
#define DATAIN 12    // MISO (Dout)
#define SPICLOCK 13  // Clock (DCLK)

//O slave é o conversor AD

// ************************************************************************************
// Declare (and initialize where necessary) global variables available to all functions
// ************************************************************************************
long readValue;
double readVoltage;


// *********************************************************
// Setup function - initializes the board and sets pin modes
// *********************************************************
void setup() {
 // set pin modes
 pinMode(SELPIN, OUTPUT);
 pinMode(DATAOUT, OUTPUT);
 pinMode(DATAIN, INPUT);
 pinMode(SPICLOCK, OUTPUT);
 
 // disable device at the outset
 digitalWrite(SELPIN, HIGH);
 digitalWrite(DATAOUT, LOW);
 digitalWrite(SPICLOCK, LOW);
 
 // Setup communications rate
 Serial.begin(9600);
 analogReference(DEFAULT);
}

// ****************************
// Loop function - main program
// ****************************
void loop() {
 int iChannel = 1;

 for(iChannel=1; iChannel <= 5; iChannel++) {
   // Loop to read all five channels and send it to serial
   readValue = read_adc(iChannel);
   if (readValue < 0) { readValue += 65535; }
   readVoltage = (double(readValue)*5000)/65535;
   Serial.print(readVoltage);
   if (iChannel < 5) {
     Serial.print(",");
   }
 }
 Serial.println();
 // Wait a bit for the analog-to-digital converter
 // to stabilize after the last reading:
 delay(10);
}


// *********************************************
// Function that reads the requested ADC channel
// *********************************************
int read_adc(int channel) {
 long adcvalue = 0;
 byte commandbits = B00000000;  // Read nothing....

 switch(channel)  // Switch case to select channel
 {
   case 1:  {
     commandbits = B10000111;  // Select channel 0 (LPS-1 Uout)
     }
     break;
   case 2:  {
     commandbits = B11000111;  // Select channel 1 (LPS-2 Uout)
     }
     break;
   case 3:  {
     commandbits = B10010111;  // Select channel 2 (LPS-2 Kout)
     }
     break;
   case 4:  {
     commandbits = B11010111;  // Select channel 3 (External)
     }
     break;
   case 5:  {
     commandbits = B10100111;  // Select channel 4 (2.500V Reference)
     }
     break;
 }

 digitalWrite(SELPIN,LOW); // Select adc
 // We need 24 cycles for a full conversion
 // 8 cycles for control byte and 16 for
 // setup bits to be written
 for (int i=7; i>=0; i--) {
    digitalWrite(DATAOUT,commandbits&1<<i);
   // Cycle the clock 8 times
   digitalWrite(SPICLOCK,HIGH);
   digitalWrite(SPICLOCK,LOW);
 }
 // Read bits from adc
 for (int i=16; i>=0; i--) {
   adcvalue+=digitalRead(DATAIN)<<i;//le bit a bit do MSB pro LSB

   // Cycle the clock 17 times
   digitalWrite(SPICLOCK,HIGH);
   digitalWrite(SPICLOCK,LOW);
 }
 
 // Shift in 7 zeros to complete conversion cycle
 for (int i=6; i>=0; i--) {
   digitalRead(DATAIN)<<0;
   
   // Cycle the clock 7 times
   digitalWrite(SPICLOCK,HIGH);
   digitalWrite(SPICLOCK,LOW);
 }
 
 // 32 cycles total
 digitalWrite(SELPIN, HIGH); //turn off device
 return adcvalue;
}
