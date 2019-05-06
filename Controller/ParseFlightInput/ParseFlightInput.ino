// Flight status
#define PRELAUNCH 0
#define LIFTOFF 1
#define MGRAV_BEGIN 2
#define MGRAV_END 3
#define LANDING 4
#define OTHER 5

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
   
   
  if (Serial.available() >= 92) {
    for (int i=0; i<92; i++) {
      char inputChar = Serial.read();

      if (i == 0) {
        if (inputChar == '@') {
          flightStatus = PRELAUNCH;
        }
        
        else if (inputChar == 'A') {
          flightStatus = LIFTOFF;
        }
        
        else if (inputChar == 'D') {
          flightStatus = MGRAV_BEGIN;
        }
        
        else if (inputChar == 'F') {
          flightStatus = MGRAV_END;
        }
        
        else if (inputChar == 'H') {
          flightStatus = LANDING;
        }    

        else {
          flightStatus = OTHER;
        }
        
      }
    }
  }

 displayLED();

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

  else {
    digitalWrite(LED_LIFTOFF, LOW);
    digitalWrite(LED_MG_BEGIN, LOW);
    digitalWrite(LED_MG_END, LOW);
  }
}
