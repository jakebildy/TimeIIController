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

void setup() {
  // put your setup code here, to run once:
  pinMode(SRCLR, OUTPUT);
  pinMode(SRCLK, OUTPUT);
  pinMode(SER, OUTPUT);
  pinMode(RCLK, OUTPUT);
  boolean BoolArray[16] = {1,1,1,1,0,0,0,0};
 
  shift(BoolArray);
}

void loop() {
//   put your main code here, to run repeatedly:
    parseStatusFromRocket();
    updateValves();
    thermoRegulation();
}


void parseStatusFromRocket() {
 if (Serial.available() > 0) {
                // read the incoming byte:
                incomingByte = Serial.read();

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

void shift(boolean Array[]){
  digitalWrite(RCLK, LOW);
  for(int i=0;i<sizeof(Array);i++){
    digitalWrite(SRCLR, HIGH);
    digitalWrite(SRCLK, LOW);
    if(Array[i]){
      digitalWrite(SER,HIGH);
    }else{
      digitalWrite(SER,LOW);
    }
  }
  digitalWrite(RCLK, HIGH);
  return;
}
