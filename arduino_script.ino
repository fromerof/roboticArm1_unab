#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;

int servoSpeeds[] = {20, 20, 20, 10, 10, 10}; // Velocidad para cada servo

void setup() {
  Serial.begin(9600);

  servo1.attach(11); // Servo 1 en pin 11
  servo2.attach(10); // Servo 2 en pin 10
  servo3.attach(9);  // Servo 3 en pin 9
  servo4.attach(6);  // Servo 4 en pin 6
  servo5.attach(5);  // Servo 5 en pin 5
  servo6.attach(3);  // servo 6 en pin 3

  // Inicializar servos a una posición conocida y velocidades para cada servo
  moveServoSmooth(servo1, 90, servoSpeeds[0]);
  moveServoSmooth(servo2, 180, servoSpeeds[1]); 
  moveServoSmooth(servo3, 140,servoSpeeds[2]);
  moveServoSmooth(servo4, 90,servoSpeeds[3]);
  moveServoSmooth(servo5, 50, servoSpeeds[4]);
  moveServoSmooth(servo6, 40, servoSpeeds[5]); 

  Serial.println("Servo Control Ready");
}

void loop() {
  if (Serial.available() >= 2) {
    // valores para mover servos
    String input = Serial.readStringUntil('\n'); // Leer input como string hasta salto de linea
    int servoNumber = input.charAt(0) - '0'; // Convertir primer char a int restando el 0 en ASCII. ej: '1' - '0' = 49 - 48 = 1
    int angle = input.substring(1).toInt(); // Convertir el resto a int. Angulo.

    Serial.print("Raw input: ");
    Serial.println(input);
    Serial.print("Parsed servo number: ");
    Serial.println(servoNumber);
    Serial.print("Parsed angle: ");
    Serial.println(angle);

    if (servoNumber == 2) {
      angle = constrain(angle, 0, 180); 
    }

    if (servoNumber >=1 && servoNumber <= 6 && angle >= 0 && angle <= 180) {
      switch (servoNumber) {
        case 1: moveServoSmooth(servo1, angle, servoSpeeds[0]); break;
        case 2: moveServoSmooth(servo2, angle, servoSpeeds[1]); break;
        case 3: moveServoSmooth(servo3, angle, servoSpeeds[2]); break;
        case 4: moveServoSmooth(servo4, angle, servoSpeeds[3]); break;
        case 5: moveServoSmooth(servo5, angle, servoSpeeds[4]); break;
        case 6: moveServoSmooth(servo6, angle, servoSpeeds[5]); break;
      }
      Serial.println("ACK");
    }
    else {
      Serial.println("Invalid angle received:");
    }
  }
}

void moveServoSmooth(Servo &servo, int targetAngle, int speed) { 
  int currentAngle = servo.read();
  int step = (currentAngle < targetAngle) ? 1 : -1;
  while (currentAngle != targetAngle) {
    currentAngle += step;
    servo.write(currentAngle);
    delay(speed); // delay se ajusta segun velocidad establecida para cada servo
  }
}
