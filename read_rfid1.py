import RPi.GPIO as GPIO
import MFRC522
import signal
from rpi_lcd import LCD
from time import sleep
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

uid = None
prev_uid = None 
continue_reading = True
count = 0
match = False

lcd = LCD()
pin = 25



# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
mfrc522 = MFRC522.MFRC522()
# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips.
# If one is near it will get the UID
#lcd.text('Hello', 1)
countnumber =[]
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = mfrc522.MFRC522_Request(mfrc522.PICC_REQIDL)
    
    # If a card is found
    if status == mfrc522.MI_OK:
        # Get the UID of the card
        (status,uid) = mfrc522.MFRC522_Anticoll()
        

        if len(countnumber) != 0:
            for userId in countnumber:
                if uid==userId:
                    match = True
                   # print("length of countnumber"+ str(len(countnumber)))
                    break

        if match==False:
            countnumber.append(uid)
            print("New card detected! UID of card is {}".format(uid))
            count+=1 
            print('Number of patients is ' + str(count))
            lcd.text('Number of', 1)
            lcd.text('patients is '+ str(count),2)
          #  print("test"+ str(len(countnumber)))
            print countnumber
            sleep(3)
            
             
        else:
            countnumber.remove(uid)
            count-=1
            print('Number of patients is '+ str(count))
            lcd.text('Number of', 1)
            lcd.text('patients is '+ str(count),2)
            print countnumber
           # print("test2"+ str(len(countnumber)))
            if len(countnumber)==0:
                countnumber=[]
            sleep(3)

        if count==1:
            GPIO.setup(18, GPIO.OUT)
            GPIO.output(18,True)
        else:
            GPIO.setup(18, GPIO.OUT)
            GPIO.output(18,False)