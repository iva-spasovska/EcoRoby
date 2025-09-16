#include <Servo.h>

// Create servo objects
Servo servo01; // Base rotation
Servo servo02; // Shoulder
Servo servo03; // Elbow
Servo servo04; // Wrist up/down
Servo servo05; // Wrist rotate
Servo servo06; // Gripper

// Define pins for each servo
const int servo01Pin = 5;
const int servo02Pin = 6;
const int servo03Pin = 7;
const int servo04Pin = 8;
const int servo05Pin = 9;
const int servo06Pin = 10;

// Initial position
int baseInit = 0;
int shoulderInit = 120;
int elbowInit = 90;
int wristInit = 70;
int wristRotInit = 110;

int gripperOpen = 180;
int gripperClosed = 130;

// Pick position
int shoulderPick = 50;
int elbowPick = 140;
int wristPick = 90;
int wristRotPick = 130;

int shoulderPos = 70;
int elbowPos = 120;
int wristRotPos = 150;

// Place position
int basePlace;
int baseOption1 = 90;
int baseOption2 = 50;
int baseOption3 = 30;

int shoulderPlace;
int shoulderOption1 = 110;
int shoulderOption23 = 90;

int elbowPlace;
int elbowOption1 = 130;
int elbowOption2 = 110;
int elbowOption3 = 90;

int wristRotPlace;
int wristRotPlace12 = 10;
int wristRotPlace3 = 60;

// Speed delay (lower = faster)
int speedDelay = 50;

void setup() {
  Serial.begin(9600);
  servo01.attach(servo01Pin);
  servo02.attach(servo02Pin);
  servo03.attach(servo03Pin);
  servo04.attach(servo04Pin);
  servo05.attach(servo05Pin);
  servo06.attach(servo06Pin);

  // Move to initial position
  servo01.write(baseInit);
  servo02.write(shoulderInit);
  servo03.write(elbowInit);
  servo04.write(wristInit);
  servo05.write(wristRotInit);
  servo06.write(gripperOpen); 
  delay(1000);
}

void loop() {
  if (Serial.available()) {
    int val = Serial.parseInt();
    if (val == 1) {
      basePlace = baseOption1;
      shoulderPlace = shoulderOption1;
      elbowPlace = elbowOption1;
      wristRotPlace = wristRotPlace12;
      runSequence();
    }
    else if (val == 2) {
      basePlace = baseOption2;
      shoulderPlace = shoulderOption23;
      elbowPlace = elbowOption2;
      wristRotPlace = wristRotPlace12;
      runSequence();
    }
    else if (val == 3) {
      basePlace = baseOption3;
      shoulderPlace = shoulderOption23;
      elbowPlace = elbowOption3;
      wristRotPlace = wristRotPlace3;
      runSequence();
    }
    else {
      servo01.write(0);
      Serial.print("Received: ");
      Serial.println(val);
    }
  }
}

// Function to execute pick & place sequence
void runSequence() {
  // Move to pick position
  moveServoSmooth(servo02, shoulderInit, shoulderPick);
  moveServoSmooth(servo05, wristRotInit, wristRotPick);
  moveServoSmooth(servo03, elbowInit, elbowPick);
  moveServoSmooth(servo04, wristInit, wristPick);
  
  // Close gripper
  moveServoSmooth(servo06, gripperOpen, gripperClosed);
  
  // Pick up
  moveServoSmooth(servo05, wristRotPick, wristRotPos);
  moveServoSmooth(servo03, elbowPick, elbowPos);
  moveServoSmooth(servo02, shoulderPick, shoulderPos);
  delay(1000);

  // Move to place position (base changes depending on key pressed)
  moveServoSmooth(servo01, baseInit, basePlace);
  moveServoSmooth(servo02, shoulderPos, shoulderPlace);
  moveServoSmooth(servo03, elbowPos, elbowPlace);
  moveServoSmooth(servo05, wristRotPos, wristRotPlace);

  // Open gripper
  moveServoSmooth(servo06, gripperClosed, gripperOpen);
  delay(1000);

  // Return to initial position
  moveServoSmooth(servo05, wristRotPlace, wristRotInit);
  moveServoSmooth(servo04, wristPick, wristInit);
  moveServoSmooth(servo03, elbowPlace, elbowInit);
  moveServoSmooth(servo02, shoulderPlace, shoulderInit);
  moveServoSmooth(servo01, basePlace, baseInit);

  delay(2000);
}

// Function to move servo smoothly
void moveServoSmooth(Servo &servo, int startPos, int endPos) {
  if (startPos < endPos) {
    for (int pos = startPos; pos <= endPos; pos++) {
      servo.write(pos);
      delay(speedDelay);
    }
  } else {
    for (int pos = startPos; pos >= endPos; pos--) {
      servo.write(pos);
      delay(speedDelay);
    }
  }
}

