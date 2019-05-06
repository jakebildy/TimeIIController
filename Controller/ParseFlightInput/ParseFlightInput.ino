// Flight status
#define PRELAUNCH 0
#define LIFTOFF 1
#define MGRAV_BEGIN 2
#define MGRAV_END 3
#define LANDING 4
#define OTHER 5
#define FINISHED 6

//Pins

#define LED_LIFTOFF 2
#define LED_MG_BEGIN 3
#define LED_MG_END 4

int flightStatus = PRELAUNCH;

void setup() {
  Serial.begin(115200);     // opens serial port, sets baudrate to 115200 bps
  pinMode(LED_LIFTOFF, OUTPUT);
  pinMode(LED_MG_BEGIN, OUTPUT);
  pinMode(LED_MG_END, OUTPUT);
}

void loop() {
   
   
  if (Serial.available() >= 1) {
      char inputChar = Serial.read();

        if (inputChar == '@') {
          flightStatus = PRELAUNCH;
           displayLED();
        }
        
        else if (inputChar == 'A') {
          flightStatus = LIFTOFF;
           displayLED();
        }
        
        else if (inputChar == 'D') {
          flightStatus = MGRAV_BEGIN;
           displayLED();
        }
        
        else if (inputChar == 'F') {
          flightStatus = MGRAV_END;
           displayLED();
        }
        
        else if (inputChar == 'H') {
          flightStatus = LANDING;
           displayLED();
        }    

        else if (inputChar == 'J') {
          flightStatus = FINISHED;
           displayLED();
        }    

        else if (isAlpha(inputChar)) {
          flightStatus = OTHER;
          displayLED();
        }
  }

    

}


void displayLED() {

  if (flightStatus == LIFTOFF) {
    digitalWrite(LED_LIFTOFF, HIGH);
    digitalWrite(LED_MG_BEGIN, LOW);
    digitalWrite(LED_MG_END, LOW);
  }

  else if (flightStatus == MGRAV_BEGIN) {
    digitalWrite(LED_LIFTOFF, LOW);
    digitalWrite(LED_MG_BEGIN, HIGH);
    digitalWrite(LED_MG_END, LOW);
  }

  else if (flightStatus == MGRAV_END) {
    digitalWrite(LED_LIFTOFF, LOW);
    digitalWrite(LED_MG_BEGIN, LOW);
    digitalWrite(LED_MG_END, HIGH);
  }

  else if (flightStatus == FINISHED) {
    digitalWrite(LED_LIFTOFF, HIGH);
    digitalWrite(LED_MG_BEGIN, HIGH);
    digitalWrite(LED_MG_END, HIGH);

    delay(500);  
    
    digitalWrite(LED_LIFTOFF, HIGH);
    digitalWrite(LED_MG_BEGIN, HIGH);
    digitalWrite(LED_MG_END, HIGH);

    delay(500); 
    
    digitalWrite(LED_LIFTOFF, HIGH);
    digitalWrite(LED_MG_BEGIN, HIGH);
    digitalWrite(LED_MG_END, HIGH);

   delay(500); 

    digitalWrite(LED_LIFTOFF, LOW);
    digitalWrite(LED_MG_BEGIN, LOW);
    digitalWrite(LED_MG_END, LOW);
  }

  else {
    digitalWrite(LED_LIFTOFF, LOW);
    digitalWrite(LED_MG_BEGIN, LOW);
    digitalWrite(LED_MG_END, LOW);
  }
}
