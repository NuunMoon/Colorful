
#define R_PIN 3
#define G_PIN 5
#define B_PIN 6

String x;
int RGB_data[3];

void setup()
{
  // initialize pinout
  pinMode(R_PIN, OUTPUT);
  pinMode(G_PIN, OUTPUT);
  pinMode(B_PIN, OUTPUT);
  Serial.begin(9600); 
  
  while(!Serial);
  establishContact();
}


void loop(){
  if (Serial.available()>0)
  {
    x = Serial.readString();
  }

  RGB_data[0] = x.substring(x.indexOf('r') + 1, x.indexOf('g') + 1).toInt();
  RGB_data[1] = x.substring(x.indexOf('g') + 1, x.indexOf('b') + 1).toInt();
  RGB_data[2] = x.substring(x.indexOf('b') + 1, x.length()).toInt();
  
 
  for (int i = 0; i < 3; i++)
  {
    //Serial.println(RGB_data[i]);
  }
  digitalWrite(R_PIN, RGB_data[0]);
  digitalWrite(G_PIN, RGB_data[1]);
  digitalWrite(B_PIN, RGB_data[2]);

  delay(100);
}

void establishContact() {

  while (Serial.available() <= 0) {
    //Serial.print("r");   // send a byte

    delay(1000);

  }
}
