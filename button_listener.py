import RPi.GPIO as GPIO
from configconn import *
import time, subprocess

dnsmasq = "/etc/dnsmasq.conf"
dhcpcd = "/etc/dhcpcd.conf"
wpa_supplicant = "/etc/wpa_supplicant/wpa_supplicant.conf"

isRunning = True
button_pin = 17
led_pin = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

time_flag = False
button_flag = True
start_time = 0
target_time = 3

def switchToAP():
    APConfig.copyfile("configurations/dnsmasq.conf", dnsmasq)
    APConfig.copyfile("configurations/dhcpcd.conf", dhcpcd)
    APServices.start()

GPIO.output(led_pin, GPIO.HIGH)

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

for _ in range(5):
    time.sleep(0.2)
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(led_pin, GPIO.HIGH)

print("Proper shutdown and resetting network configuration")
switchToAP()

GPIO.output(led_pin, GPIO.LOW)

GPIO.cleanup()

subprocess.run(["sudo", "shutdown", "-h", "now"])
