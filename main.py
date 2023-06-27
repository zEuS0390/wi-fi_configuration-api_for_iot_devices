from flask import Flask, render_template, request
from configconn import *

app = Flask(
        "WiFiSetupApp",
        static_url_path="/static",
        static_folder="static",
        template_folder="templates"
)

# Configuration files that will be modified 
dnsmasq = "/etc/dnsmasq.conf"
dhcpcd = "/etc/dhcpcd.conf"
wpa_supplicant = "/etc/wpa_supplicant/wpa_supplicant.conf"

# Home Page
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        ssid = request.form.get("ssid")
        pwd = request.form.get("password")

        WPASupplicantConfig.setCredentials("configurations/wpa_supplicant.conf", wpa_supplicant, ssid, pwd)
        APConfig.copyfile("configurations/dnsmasq.conf.old", dnsmasq)
        APConfig.copyfile("configurations/dhcpcd.conf.old", dhcpcd)
        APServices.stop()

        return render_template("index.html")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
