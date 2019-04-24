#define SRCLR 12
#define SRCLK 8
#define SER 11
#define RCLK 10


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
