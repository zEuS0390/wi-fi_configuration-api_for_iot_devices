from flask_restful import Resource, Api, request
from flask.json import jsonify
from hardware import Hardware
import check_internet_conn
from flask import Flask
from configconn import *
import urllib.request
import time, sys, os, threading

dnsmasq = "/etc/dnsmasq.conf"
dhcpcd = "/etc/dhcpcd.conf"
wpa_supplicant = "/etc/wpa_supplicant/wpa_supplicant.conf"

buzzer_pin = 23
red_pin = 22
green_pin = 17
blue_pin = 27
button_pin = 24

app = Flask(__name__)
api = Api(app)
hardware = Hardware(
    redpin = red_pin,
    greenpin = green_pin,
    bluepin = blue_pin,
    buttonpin = button_pin,
    buzzerpin = buzzer_pin
)

def connect(host="https://google.com"):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

def setWiFiCredentials(ssid, pwd):

    status_file = "check_internet_conn_status.txt"

    check_internet_conn.setStatus(status_file, False)

    hardware.setColorRGB(False, False, True)
    hardware.playBuzzer(1, 0.5, 0.5)

    # Disable access point and enable connection to a Wi-Fi network
    WPASupplicantConfig.setCredentials(
            "configurations/wpa_supplicant.conf", 
            wpa_supplicant, 
            ssid, 
            pwd
    )
    APConfig.copyfile(
            "configurations/dnsmasq.conf.old", 
            dnsmasq
    )
    APConfig.copyfile(
            "configurations/dhcpcd.conf.old", 
            dhcpcd
    )
    APServices.stop()

    retries = 0
    max_retries = 12
    connected = False

    while not connected and retries < max_retries:
        sys.stdout.write(".")
        sys.stdout.flush()
        connected = connect(host="https://google.com")
        retries += 1
        time.sleep(1)

    if connected:
        hardware.setColorRGB(False, True, False)
        hardware.playBuzzer(1, 0.5, 0.5)
        time.sleep(5)
        hardware.setColorRGB(False, True, False)
        check_internet_conn.setStatus(status_file, True)
        os._exit(0)
    else:
        hardware.setColorRGB(False, False, True)
        # Switch back to being an access point
        APConfig.copyfile("configurations/dnsmasq.conf", dnsmasq)
        APConfig.copyfile("configurations/dhcpcd.conf", dhcpcd)
        APServices.start()
        hardware.setColorRGB(True, False, False)
        hardware.playBuzzer(5, 0.05, 0.05)
        time.sleep(5)
        check_internet_conn.setStatus(status_file, True)

class Index(Resource):

    def get(self):
        data = {
                "message": "Success"
        }
        response = jsonify()
        response.status_code = 200
        return response

    def post(self):
        data = {
                "message": "Invalid request format"
        }
        response = jsonify()
        data = request.get_json(force=True)
        if data is not None:
            try:
                ssid = data["ssid"]
                pwd = data["pwd"]
                print("ssid:", ssid)
                print("pwd:", pwd)
                threading.Thread(target=setWiFiCredentials, args=(ssid, pwd)).start()
                response.status_code = 200
            except:
                response.status_code = 400
        else:
            response.status_code = 400
        return response

api.add_resource(Index, "/")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
