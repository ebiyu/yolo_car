#define PIN_Key 2
#define PIN_RBGLED 4

#define PIN_Motor_STBY 3
#define PIN_Motor_PWMA 5
#define PIN_Motor_PWMB 6
#define PIN_Motor_AIN_1 7
#define PIN_Motor_BIN_1 8

#define PIN_Servo_1 10
#define PIN_Servo_2 11

void receiveI2CHandler();
void onI2CRegSet(uint8_t addr, uint8_t val);

//Servo myservo;

void setup() {
  pinMode(PIN_Motor_STBY, OUTPUT);
  pinMode(PIN_Motor_PWMA, OUTPUT);
  pinMode(PIN_Motor_AIN_1, OUTPUT);
  pinMode(PIN_Motor_PWMB, OUTPUT);
  pinMode(PIN_Motor_BIN_1, OUTPUT);

  digitalWrite(PIN_Motor_STBY, HIGH);
  digitalWrite(PIN_Motor_PWMA, LOW);
  digitalWrite(PIN_Motor_AIN_1, LOW);
  digitalWrite(PIN_Motor_PWMB, LOW);
  digitalWrite(PIN_Motor_BIN_1, LOW);

//  myservo.attach(PIN_Servo_1);

  Serial.begin(9600);
  Serial.println("HEllo");
}

constexpr int BUF_SIZE = 256;
char buf[BUF_SIZE];
int buf_ptr = 0;
char send_buf[255];

void loop() {
    if(Serial.available() > 0) {
        char c = Serial.read();
        Serial.write(c);
        if (c == '\n' || c == '\r') {
            buf[buf_ptr] = '\0';
            buf_ptr = 0;
            int l, r;
            int n = sscanf(buf, "%d %d", &l, &r);
            if (n != 2) return;

            l = constrain(l, -255, 255);
            r = constrain(r, -255, 255);

            if (l == 0) {
                digitalWrite(PIN_Motor_PWMA, LOW);
            } else if (l > 0) {
                digitalWrite(PIN_Motor_AIN_1, HIGH);
                analogWrite(PIN_Motor_PWMA, l);
            } else {
                digitalWrite(PIN_Motor_AIN_1, LOW);
                analogWrite(PIN_Motor_PWMA, -l);
            }

            if (r == 0) {
                digitalWrite(PIN_Motor_PWMB, LOW);
            } else if (r > 0) {
                digitalWrite(PIN_Motor_BIN_1, HIGH);
                analogWrite(PIN_Motor_PWMB, r);
            } else {
                digitalWrite(PIN_Motor_BIN_1, LOW);
                analogWrite(PIN_Motor_PWMB, -r);
            }

//            myservo.write(cam); 

            // handle input
        } else {
            buf[buf_ptr] = c;
            buf_ptr++;
            if (buf_ptr == BUF_SIZE) {
                buf_ptr = 0;
            }
        }
    }
}