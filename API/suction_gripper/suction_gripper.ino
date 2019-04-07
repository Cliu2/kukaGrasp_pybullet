#define EN1 4
#define PWM1 5
#define IN1 6
#define IN2 7

int ch_buf_len = 0;
char ch_buf[50];      // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete

char key;
int value;

void setup() {
  // put your setup code here, to run once:
  pinMode(EN1, OUTPUT);
  pinMode(PWM1, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN1, OUTPUT);

  digitalWrite(EN1, HIGH);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  analogWrite(PWM1, 0);

  Serial.begin(115200);
  
}

void loop() {
  if (stringComplete) {
    int matched = sscanf(ch_buf, "%c%d", &key, &value);
    if (matched < 2)
    {
      Serial.println("Invaild argument.");
      for (int i=0; i<ch_buf_len-1; i++) {
        Serial.print(ch_buf[i]);
      }
      Serial.println();
    }
    Serial.print(key); Serial.print(" "); Serial.println(value);
    
    // clear the string:
    stringComplete = false;
    ch_buf_len = 0;

    if (key == 'm')
    {
      analogWrite(PWM1, constrain(value, 0, 255));
    } else if (key == 'e') {
      digitalWrite(EN1, value>0);
    }
    
  }
  delay(10);
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    // add it to the inputString:
    if (ch_buf_len < 50 and !stringComplete) {
      ch_buf[ch_buf_len++] = inChar;
    }
    if (inChar == '\n') {
      stringComplete = true;
      ch_buf[ch_buf_len] = 0;
      break;
    }
  }
}
