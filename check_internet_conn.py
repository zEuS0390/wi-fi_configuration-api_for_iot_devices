from hardware import Hardware
import sys, time, urllib.request

# Connect to a given host.
def connect(host="https://google.com", verbose=False) -> bool:
    try:
        urllib.request.urlopen(host, timeout=20)
        return True
    except Exception as err:
        if verbose:
            sys.stdout.write(str(err)+"\n")
            sys.stdout.flush()
    return False

# Enable performing internet connection checking
def setStatus(status_file, is_active) -> any:
    if isinstance(is_active, bool):
        with open(status_file, "w") as f:
            f.write("1" if is_active else "0")
        return
    raise Exception("setStatus's parameter 'state' requires to be a boolean type")

# Get the status of internet connection checking 
def getStatus(status_file) -> bool:
    is_active = False
    with open(status_file, "r") as f:
        is_active = bool(int(f.readline()))
    return is_active

if __name__=="__main__":

    buzzer_pin = 23
    red_pin = 22
    green_pin = 17
    blue_pin = 27
    button_pin = 24

    hardware = Hardware(
        redpin = red_pin,
        greenpin = green_pin,
        bluepin = blue_pin,
        buttonpin = button_pin,
        buzzerpin = buzzer_pin
    )

    status_file = "check_internet_conn_status.txt"
    setStatus(status_file, True)

    while True:

        is_active = getStatus(status_file)
        
        if is_active:

            connected = connect(host="https://google.com")
            
            if connected:
                hardware.setColorRGB(False, True, False)
            else:
                hardware.setColorRGB(True, False, False)

            sys.stdout.write("-" if not connected else ".")
            sys.stdout.flush()
        else:
            sys.stdout.write("_")
            sys.stdout.flush()

        time.sleep(1)

