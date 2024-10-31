// definitions for injector motor
#define directionPin 2
#define pulsePin 3
#define limitSwitch 4
#define loadSwitch 5
#define dumpSwitch 6

// definitions for syringe rotation motor
#define directionPinMotor2 7 // Define direction pin for motor 2
#define pulsePinMotor2 8     // Define pulse pin for motor 2
#define buttonPin 9  

// initialize variables for injector system
int x = 0;
int load = 0;
int release = 300;
int loadtime = 1;
bool limitSwitchPresses = false;

// initialize variables for rotation system
int stepsFor60Degrees = 100; // Set based on your motor's specifications
bool rotationButtonPressed = false;


void setML(int mL) {
  if (mL == 10) {
    load = 700;  // Set load to 700
  } else if (mL == 20) {
    load = 1300; // Set load to 1300
  } else if (mL == 30) {
    load = 2300; // Set load to 2300
  } else {
    load = 4300; // Default value
  }
}

void setup() {
  Serial.begin(9600); // Initialize serial communication

  // Configure pin modes for injector
  pinMode(limitSwitch, INPUT_PULLUP);
  pinMode(pulsePin, OUTPUT);
  pinMode(directionPin, OUTPUT);
  pinMode(loadSwitch, INPUT_PULLUP);
  pinMode(dumpSwitch, INPUT_PULLUP);
  
  // configure pin modes for syringe rotator
  pinMode(directionPinMotor2, OUTPUT);
  pinMode(pulsePinMotor2, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP); // Assuming a pull-up resistor

  // Set the load variable
  setML(10);
  
  Serial.println("Setup complete. Ready to operate.");
}

void loop() {

  // If the limit switch is not pressed, keep moving the motor
  if (digitalRead(limitSwitch) == LOW) {
    digitalWrite(directionPin, HIGH); // Set the direction
    digitalWrite(pulsePin, HIGH); // Send a pulse to the motor
    delay(loadtime);
    digitalWrite(pulsePin, LOW); // Stop the pulse
    delay(loadtime);
    x++; // Increment position variable
  } else {
    // Optionally, stop the motor or set direction to LOW
    digitalWrite(directionPin, LOW); // Change direction if needed
    Serial.println("Limit switch pressed. Motor stopped.");
  }


  // Check if the button is pressed
  if (digitalRead(buttonPin) == LOW) {
    rotationButtonPressed = true; // Button press detected
  }

  // If the button was pressed, rotate the motor
  if (rotationButtonPressed) {
    rotationButtonPressed = false; // Reset button state after detecting

    // Rotate motor by 60 degrees
    digitalWrite(directionPinMotor2, HIGH); // Set direction
    for (int i = 0; i < stepsFor60Degrees; i++) {
      digitalWrite(pulsePinMotor2, HIGH);
      delayMicroseconds(500); // Adjust pulse speed as necessary
      digitalWrite(pulsePinMotor2, LOW);
      delayMicroseconds(500);
    }

    Serial.println("Motor rotated 60 degrees.");
  }

  // Add a small delay to avoid overwhelming the serial output
  delay(100); // Adjust as necessary
}


