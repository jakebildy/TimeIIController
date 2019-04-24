#define SRCLR 12
#define SRCLK 8
#define SER 11
#define RCLK 10

// Flight status
#define PRELAUNCH 0
#define START 1
#define MGRAV_BEGIN 2
#define MGRAV_END 3
#define END 4

int flightStatus = PRELAUNCH;
double temperature = -274;
int valves[40] = { 0 };
  
void setup() {
  // put your setup code here, to run once:
  pinMode(SRCLR, OUTPUT);
  pinMode(SRCLK, OUTPUT);
  pinMode(SER, OUTPUT);
  pinMode(RCLK, OUTPUT);
 
  shift();
}

void loop() {
//   put your main code here, to run repeatedly:
    parseStatusFromRocket();
    updateValves();
    thermoRegulation();
}

void shift(){
  digitalWrite(RCLK, LOW);
  for(int i=0; i < 40; i++){
    digitalWrite(SRCLR, HIGH);
    digitalWrite(SRCLK, LOW);
    if(valves[i] == 1){
      digitalWrite(SER,HIGH);
    }else{
      digitalWrite(SER,LOW);
    }
  }
  digitalWrite(RCLK, HIGH);
  return;
}

void parseStatusFromRocket() {
 if (Serial.available() > 0) {
                // read the incoming byte:
                byte incomingByte = Serial.read();

                // say what you got:
                Serial.print("Received: ");
                Serial.println(incomingByte, DEC);

                flightStatus = START;
        }
        return;
}


void updateValves() {
  return;
}

void thermoRegulation() {
  return;
}


//helper function  to convert naming convention to value in array

// EXAMPLE: 412 corresponds to plate four, valve 12. Its array index would be (4-1)*16 + 12 = 60
int nameToValue(int nameInt) {

  int plate = nameInt / 100;
  int spot = nameInt - plate;
  
  return (plate - 1) * 16 + spot;
}
