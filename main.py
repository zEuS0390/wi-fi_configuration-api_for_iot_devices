from flask_restful import Resource, Api, request
from flask.json import jsonify
from flask import Flask
from configconn import *
import os, threading

app = Flask(__name__)
api = Api(app)

dnsmasq = "/etc/dnsmasq.conf"
dhcpcd = "/etc/dhcpcd.conf"
wpa_supplicant = "/etc/wpa_supplicant/wpa_supplicant.conf"

def setWiFiCredentials(ssid, pwd):
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
    os._exit(0)

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
            ssid = data["ssid"]
            pwd = data["pwd"]
            print("ssid:", ssid)
            print("pwd:", pwd)
            threading.Thread(target=setWiFiCredentials, args=(ssid, pwd)).start()
            response.status_code = 200
        else:
            response.status_code = 400
        return response

api.add_resource(Index, "/")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
