from configconn import *
import getpass

if __name__=="__main__":

    # Configuration files that will be modified 
    dnsmasq = "/etc/dnsmasq.conf"
    dhcpcd = "/etc/dhcpcd.conf"
    wpa_supplicant = "/etc/wpa_supplicant/wpa_supplicant.conf"

    print("Network Connection Options:\n\tWIFI\n\tAP\n")
    select = input("Select Network Connection: ")

    if select == "WIFI":

        print("Setup Wi-Fi Connection")
        ssid = input("ssid: ")
        pwd = getpass.getpass("wpa_passphrase: ")

        WPASupplicantConfig.setCredentials("configurations/wpa_supplicant.conf", wpa_supplicant, ssid, pwd)
        print("Successfully saved SSID and WPA_Passphrase.")

        APConfig.copyfile("configurations/dnsmasq.conf.old", dnsmasq)
        APConfig.copyfile("configurations/dhcpcd.conf.old", dhcpcd)

        APServices.stop()

        print("Switch to Wi-Fi Connection")

    else:

        APConfig.copyfile("configurations/dnsmasq.conf", dnsmasq)
        APConfig.copyfile("configurations/dhcpcd.conf", dhcpcd)

        APServices.start()

        print("Switch to being an Access Point")



