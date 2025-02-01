# This program can view trhe data from the Blauberg Vento compatible fans on the networ. Blauberg, Vents, Duka.
import sys
import time
from VentoExpertSDK.ventoClient import VentoClient, Device, Mode

deviceAdressList = []


def onchange(device: Device):
    # Callback function when device changes
    print("Device changed\n"
          f"ip: {device.ip_address}\n"
          f" unit type: {device.unit_type}\n"
          f" speed: {device.speed}\n"
          f" manualspeed: {device.manualspeed}\n"
          f" fan1rpm: {device.fan1rpm}\n"
          # f" fan2rpm: {device.fan2rpm},"
          f" mode: {device.mode}\n"
          f" humidity: {device.humidity}\n"
          f" filter alarm: {device.filter_alarm}\n"
          f" time to filter maintenance: {device.filter_timer}\n"
          f" firmware version: {device.firmware_version},"
          f" firmware date: {device.firmware_date},\n"
          f" device ID: {device.device_id}\n"
          )


def newdevice_callback(deviceid: str, ip_addr: str):
    duplicateDevice = False
    dataPair = (deviceid, ip_addr)
    if not deviceAdressList:
        deviceAdressList.append(dataPair)
    else:
        for i in range(0, len(deviceAdressList)):
            # deviceToCompare = deviceAdressList[i]
            if deviceAdressList[i][0] == deviceid:
                duplicateDevice = True
                print("Duplicate found ", i, deviceid)
                continue

        if not duplicateDevice:
            deviceAdressList.append(dataPair)


def showDiscoveredFans():
    print("Press number keys to selct fan device :")
    for i in range(0, len(deviceAdressList)):
        print(i+1, " :  Device = ", deviceAdressList[i][0], ", IP = ", deviceAdressList[i][1])


def shutdown(fanClient=None):
    if fanClient is not None:
        print("Closing")
        fanClient.close()
    print("Done")

    exit(0)


def main():
    # Main
    fanClient: VentoClient = VentoClient()
    fanClient.search_devices(newdevice_callback)
    time.sleep(3)       # Give fans time to respond to the search command

    showDiscoveredFans()

    while True:
        print(
            "Press one key and enter.\n"
            "1-6 to select cooresonding device above\n"
            "q = quit selection process\n"
        )
        char = sys.stdin.read(2)[0]
        if char == "q":
            shutdown()
            break
        if char >= "1" and char <= "6":
            device_id = deviceAdressList[int(char)-1][0]
            ip_address = deviceAdressList[int(char)-1][1]
            break

    # initialize the VentoClient and add the device(s)
    # validate_device(self, device_id: str, password: str = None, ip_address: str = "<broadcast>") -> Device:
    mydevice: Device = fanClient.validate_device(device_id, ip_address=ip_address)
    if mydevice is None:
        print("Device does not respond")
    else:
        mydevice = fanClient.add_device(device_id, ip_address=mydevice.ip_address, onchange=onchange)

        print("Device added")
        print(f"Firmware version: {mydevice.firmware_version}")
        print(f"Firmware date: {mydevice.firmware_date}")
        print(f"Unit type: {mydevice.unit_type}")
        print(f"Number of devices: {fanClient.get_device_count()}\n")
        while True:
            print(
                "Press one key and enter.\n"
                "1-3 for speed, 0=off 9=on\n"
                "b,n,m for mode\n"
                "f for reset filter alarm\n"
                "q for quit\n"
            )
            char = sys.stdin.read(2)[0]
            if char == "q":
                break
            if char >= "0" and char <= "3":
                fanClient.set_speed(mydevice, ord(char) - ord("0"))
            if char >= "4" and char <= "8":
                manualspeed = ((ord(char) - ord("4")) * 50) + 50
                fanClient.set_manual_speed(mydevice, manualspeed)
            if char == "9":
                fanClient.turn_on(mydevice)
            if char == "b":
                fanClient.set_mode(mydevice, Mode.ONEWAY)
            if char == "n":
                fanClient.set_mode(mydevice, Mode.TWOWAY)
            if char == "m":
                fanClient.set_mode(mydevice, Mode.IN)
            if char == "f":
                fanClient.reset_filter_alarm(mydevice)
    shutdown(fanClient)


main()
