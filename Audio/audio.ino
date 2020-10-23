#define button 7
#define volume A4
bool music_state = 0;
bool prev_b = 0;
int prev_v = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(button, INPUT);
  pinMode(volume, INPUT);
  pinMode(13, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  bool b = digitalRead(button);
  int v = analogRead(volume);
  if(music_state) digitalWrite(13, HIGH);
  else digitalWrite(13, LOW);
    
  if(prev_b != b){
    if(!prev_b && b){
      Serial.print("b\n");
      music_state = !music_state;
    }
    prev_b = b;
  }
  
  if(abs(prev_v - v) > 60){
    Serial.print("v\n");
    Serial.print(v);
    Serial.print("\n");
    prev_v = v;
  }
  
  delay(10);
}
