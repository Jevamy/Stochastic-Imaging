import time
import RPi.GPIO as GPIO
import random

GPIO.setmode(GPIO.BOARD) #tells rpi numbering system being used to reference GPIO pins

pins = [7,11,12,13,15,16,18,19,29,31,32,33,35,36,37,40] #GPIO pins numbers to be used
for each in pins:
    GPIO.setup(each,GPIO.OUT) #set up each pin as output

blinkTime = 0.05 # 0.05 = 20Hz
timeOfRun = 7 # how long setup will run for
numIterations = int(timeOfRun/(2*blinkTime))

def randomFlash():
    
    for numRuns in range(numIterations): # number of images to be captured
            ranOutput = random.randint(0,len(pins)-1)

            GPIO.output(pins[ranOutput],True)
            time.sleep(blinkTime)
            GPIO.output(pins[ranOutput],False)
            time.sleep(blinkTime)

    time.sleep(1)
    
    GPIO.cleanup()

def squareFlash(): #selects LEDS on edge of array
    pinSetup = [7,11,12,13,15,16,18,19,29,31,32,33,35,36,37,40] #refresh pin setup as overwriting is possible
    GPIO.setmode(GPIO.BOARD) #tells rpi numbering system being used to reference GPIO pins    
    squarePins = pinSetup
    
    for eachSQ in squarePins:
        GPIO.setup(eachSQ,GPIO.OUT) #set up each pin as output
        
    for i in (16,18,31,32): # GPIO pins that are unwanted
        while i in squarePins:
            squarePins.remove(i) # removes 4 centre LEDS from iterable list
       
    for numRuns in range(numIterations): # number of images to be captured
        ranOutput = random.randint(0,len(squarePins)-1)

        GPIO.output(squarePins[ranOutput],True)
        time.sleep(blinkTime)
        GPIO.output(squarePins[ranOutput],False)
        time.sleep(blinkTime)

    time.sleep(1)
    
    GPIO.cleanup()
    
def crossFlash():
    pinSetup2 = [7,11,12,13,15,16,18,19,29,31,32,33,35,36,37,40] #refresh pin setup as overwriting is possible   
    GPIO.setmode(GPIO.BOARD) #tells rpi numbering system being used to reference GPIO pins    
    crossPins = pinSetup2
    
    for eachCR in crossPins:
        GPIO.setup(eachCR,GPIO.OUT) #set up each pin as output
        
    for i in (11,12,15,19,29,33,35,37): # GPIO pins that are unwanted
        while i in crossPins:
            crossPins.remove(i) # removes LEDS from iterable list
    
    for numRuns in range(numIterations): # number of images to be captured
            ranOutput = random.randint(0,len(crossPins)-1)

            GPIO.output(crossPins[ranOutput],True)
            time.sleep(blinkTime)
            GPIO.output(crossPins[ranOutput],False)
            time.sleep(blinkTime)

    time.sleep(1)
    
    GPIO.cleanup()
    
#randomfFlash() # call random all LED flash function
#crossFlash() # call cross LED flash function
#squareFlash() # call square LED flash function

def callFunc(shapes):
    if shapes.upper() == 'ALL':
        randomFlash()
        crossFlash()
        squareFlash()
    elif shapes.upper() == 'CROSS':
        crossFlash()
    elif shapes.upper() == 'SQUARE':
        squareFlash()
      
callFunc('ALL')
