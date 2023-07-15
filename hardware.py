from configparser import ConfigParser
import RPi.GPIO as GPIO
import time, sys

class Hardware:

    def __init__(self, 
            redpin: int, 
            greenpin: int, 
            bluepin: int, 
            buttonpin: int,
            buzzerpin: int,
            isrgbenabled: bool = True,
            isbuzzerenabled: bool = True
        ):
        self.isrgbenabled = isrgbenabled
        self.isbuzzerenabled = isbuzzerenabled
        self.buzzerPin = buzzerpin
        self.redPin = redpin
        self.greenPin = greenpin
        self.bluePin = bluepin
        self.buttonPin = buttonpin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.setupPins()

    def close(self):
        # self.setColorRGB(False, False, False)
        # self.playBuzzerOnly(False)
        GPIO.cleanup()

    def __del__(self):
        # self.setColorRGB(False, False, False)
        # self.playBuzzerOnly(False)
        # GPIO.cleanup()
        pass

    def setupPins(self):
        GPIO.setup(self.buzzerPin, GPIO.OUT)
        GPIO.setup(self.redPin, GPIO.OUT)
        GPIO.setup(self.bluePin, GPIO.OUT)
        GPIO.setup(self.greenPin, GPIO.OUT)
        GPIO.setup(self.buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def buttonListen(self, target_time, callback_func):
        time_flag = False
        button_flag = True
        isRunning = True
        start_time = 0
        counter_start_time = 0
        while isRunning:
            if GPIO.input(self.buttonPin) == GPIO.HIGH:
                if time_flag == True:
                    counter = time.time() - counter_start_time
                    elapsed_time = time.time() - start_time
                    if counter >= 1:
                        sys.stdout.write(".")
                        sys.stdout.flush()
                        counter_start_time = time.time() 
                    if elapsed_time >= target_time:
                        isRunning = False
                if button_flag == True:
                    button_flag = False
                    time_flag = True
                    start_time = time.time()
            else:
                button_flag = True
                start_time = time.time()
                time.sleep(0.1)
        sys.stdout.write("\n")
        sys.stdout.flush()
        callback_func()
        
    def setColorRGB(self, red: bool = False, green: bool = False, blue: bool = False):
        """
        Set the color of the RGB LED. Requires 3 states for red, green, and blue.
        """
        if self.isrgbenabled:
            if red == True:
                GPIO.output(self.redPin, GPIO.HIGH)
            else:
                GPIO.output(self.redPin, GPIO.LOW)
            if green == True:
                GPIO.output(self.greenPin, GPIO.HIGH)
            else:
                GPIO.output(self.greenPin, GPIO.LOW)
            if blue == True:
                GPIO.output(self.bluePin, GPIO.HIGH)
            else:
                GPIO.output(self.bluePin, GPIO.LOW)

    def playBuzzerOnly(self, state):
        if state:
            GPIO.output(self.buzzerPin, GPIO.HIGH)
        else:
            GPIO.output(self.buzzerPin, GPIO.LOW)

    def playBuzzer(
            self, 
            n_times: int, 
            delay1: float, 
            delay2: float, 
            useLED: bool = False, 
            ledColor: tuple = (False, False, False)
        ):
        """
        Play buzzer with an interval. Requires n_times, delay1, and delay2.
        """
        if self.isbuzzerenabled:
            for _ in range(n_times):
                GPIO.output(self.buzzerPin, GPIO.HIGH)
                if useLED:
                    self.setColorRGB(*ledColor)
                time.sleep(delay1)
                GPIO.output(self.buzzerPin, GPIO.LOW)
                if useLED:
                    self.setColorRGB(False, False, False)
                time.sleep(delay2)
