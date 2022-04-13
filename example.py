# Create a file called ".deviceid" in the current folder.
# This file should contain the device id.
# You can see the device id in the respective mobile phone apps for the relvant supplier of the fans. Blauberg, Vents, Duka.

import sys
import time

from VentoExpertSDK.ventoClient import VentoClient, Device, Mode
# from VentoExpertSDK.device import Device, Mode


def onchange(device: Device):
    # Callback function when device changes
    print(
        f"ip: {device.ip_address}"
        f" speed: {device.speed},"
        f" manualspeed: {device.manualspeed},"
        f" fan1rpm: {device.fan1rpm},"
        # f" fan2rpm: {device.fan2rpm},"
        f" mode: {device.mode},"
        f" humidity: {device.humidity},"
        f" filter alarm: {device.filter_alarm},"
        f" filter timer; {device.filter_timer} minutes"
    )


def newdevice_callback(deviceid: str):
    print("New device id: " + deviceid)


def main():
    # Main example
    fanClient: VentoClient = VentoClient()
    fanClient.search_devices(newdevice_callback)
    # print("\n Number of clients", fanClient.get_device_count())
    time.sleep(5)

    # read the device id from file
    with open(".deviceid.txt", "r") as file:
        device_id = file.readline().replace("\n", "")
        print(f"Device Id read from file: {device_id}")
    # initialize the VentoClient and add the device
    mydevice: Device = fanClient.validate_device(device_id, ip_address="192.168.29.255")
    if mydevice is None:
        print("Device does not respond")
    else:
        mydevice = fanClient.add_device(device_id, ip_address=mydevice.ip_address, onchange=onchange)
        
        print("Device added")
        print(f"Firmware version: {mydevice.firmware_version}")
        print(f"Firmware date: {mydevice.firmware_date}")
        print(f"Unit type: {mydevice.unit_type}")
        while True:
            print(
                "Press one key and enter. "
                "1-3 for speed, 0=off, 9=on,b,n,m for mode,"
                " f for reset filter alarm, q for quit"
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

    print("Closing")
    fanClient.close()
    print("Done")

    exit(0)


main()
