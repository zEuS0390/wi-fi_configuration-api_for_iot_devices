import RPi.GPIO as GPIO
from configconn import *
import time

dnsmasq = "/etc/dnsmasq.conf"
dhcpcd = "/etc/dhcpcd.conf"
wpa_supplicant = "/etc/wpa_supplicant/wpa_supplicant.conf"

isRunning = True
button_pin = 17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

time_flag = False
button_flag = True
start_time = 0
target_time = 3

def switchToAP():
    APConfig.copyfile("configurations/dnsmasq.conf", dnsmasq)
    APConfig.copyfile("configurations/dhcpcd.conf", dhcpcd)
    APServices.start()

while isRunning:

    if GPIO.input(button_pin) == GPIO.HIGH:

        if time_flag == True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= target_time:
                isRunning = False

        if button_flag == True:
            button_flag = False
            time_flag = True
            start_time = time.time()

    else:
        button_flag = True
        time.sleep(0.1)

print("Proper shutdown and resetting network configuration")
switchToAP()

GPIO.cleanup()
