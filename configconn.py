import os, shutil, stat, subprocess

class APConfig:

    @staticmethod
    def copyfile(source, target):
        shutil.copy2(source, target)

    @staticmethod
    def deletefile(source):
        os.remove(source)

class ParseSimpleConfig:
    
    @staticmethod
    def read(filename: str) -> dict:
        cfg = {}
        with open(filename, "r") as file:
            for line in file:
                if line.startswith("#"):
                    continue
                else:
                    key, value = line.strip().split("=", 1)
                    cfg[key] = value
        return cfg
    
    @staticmethod
    def set(filename: str, key: str, value: str) -> None:
        cfg = ParseSimpleConfig.read(filename)
        with open(filename, "w") as file:
            for _key, _value in cfg.items():
                if _key == key:
                    file.write("=".join([key, value])+"\n")
                else:
                    file.write("=".join([_key, _value])+"\n")

class APServices:

    @staticmethod
    def start():
        # sudo systemctl daemon-reload
        # sudo systemctl restart dhcpcd
        # sudo service dnsmasq start
        # sudo service hostapd start
        APServices.restartDHCPCD()
        subprocess.run(["sudo", "service", "dnsmasq", "start"])
        subprocess.run(["sudo", "service", "hostapd", "start"])
        return

    @staticmethod
    def stop():
        # sudo service dnsmasq stop
        # sudo service hostapd stop
        # sudo systemctl daemon-reload
        # sudo systemctl restart dhcpcd
        subprocess.run(["sudo", "service", "dnsmasq", "stop"])
        subprocess.run(["sudo", "service", "hostapd", "stop"])
        APServices.restartDHCPCD()
        return

    @staticmethod
    def restartDHCPCD():
        subprocess.run(["sudo", "systemctl", "daemon-reload"])
        subprocess.run(["sudo", "systemctl", "restart", "dhcpcd"])

class WPASupplicantConfig:

    @staticmethod
    def setCredentials(source, destination, ssid, psk):
        scan_ssid = "scan_ssid=1"
        ssid = "ssid=\""+ssid+"\""
        psk = "psk=\""+psk+"\""
        network = "network={\n "+scan_ssid+"\n "+ssid+"\n "+psk+"\n}\n"

        APConfig.copyfile(source, destination)
        with open(destination, "a") as file:
            file.write(network)

