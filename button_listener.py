from hardware import Hardware
from configconn import *
import time, subprocess

dnsmasq = "/etc/dnsmasq.conf"
dhcpcd = "/etc/dhcpcd.conf"
wpa_supplicant = "/etc/wpa_supplicant/wpa_supplicant.conf"
buzzer_pin = 23
red_pin = 22
green_pin = 16
blue_pin = 27
button_pin = 26

hardware = Hardware(
    redpin = red_pin,
    greenpin = green_pin,
    bluepin = blue_pin,
    buttonpin = button_pin,
    buzzerpin = buzzer_pin
)

def switchToAP():
    print("Resetting network configuration")
    hardware.playBuzzer(5, 0.2, 0.2, useLED=True, ledColor=(False, True, False))
    APConfig.copyfile("configurations/dnsmasq.conf", dnsmasq)
    APConfig.copyfile("configurations/dhcpcd.conf", dhcpcd)
    APServices.start()

hardware.setColorRGB(False, True, False)
hardware.buttonListen(target_time=3, callback_func=switchToAP)
hardware.close()

print("Executing system shutdown")
subprocess.run(["sudo", "shutdown", "-h", "now"], shell=False)
