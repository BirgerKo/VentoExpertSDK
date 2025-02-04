''' Backend for managing Blauber Vento fans on the local network
    I uses the VentoExpert SDK to communicate with the fans
    It can search for fans on the network and display their data and will keep a persistent list of discovered fans
    It can also send commands to the fans to change their speed, mode, etc.
    It will be used by the VentoManagerFront.py to display the data and send commands to the fans'''

from flask import Flask, jsonify, request
from VentoExpertSDK.ventoClient import VentoClient, Device
import time

app = Flask(__name__)

# In-memory storage for fans
listOfFans = []

# Initialize VentoClient
fanClient = VentoClient()


@app.route('/test', methods=['GET'])
def test():
    return jsonify({'Testing': 'Text reurned via the API'}), 404


@app.route('/scan', methods=['GET'])
def scan_fans():
    def newdevice_callback(deviceid: str, ip_addr: str):
        duplicateDevice = False
        dataPair = (deviceid, ip_addr)
        if not listOfFans:
            listOfFans.append(dataPair)
        else:
            for i in range(0, len(listOfFans)):
                # deviceToCompare = deviceAdressList[i]
                if listOfFans[i][0] == deviceid:
                    duplicateDevice = True
                    print("Duplicate found ", i, deviceid)
                    continue
            if not duplicateDevice:
                listOfFans.append(dataPair)

    print("Discovering devices on the network")
    fanClient.search_devices(newdevice_callback)
    time.sleep(4)  # Give fans time to respond to the search command
    return jsonify(listOfFans)


@app.route('/fans', methods=['GET'])
def get_fans():
    if listOfFans == {}:
        return jsonify({'error': 'Fan not found'}), 404
    return jsonify(listOfFans)


@app.route('/fans/<device_id>/commands', methods=['GET'])
def get_fan_commands(device_id):
    if device_id not in listOfFans:
        return jsonify({'error': 'Fan not found'}), 404

    # Assuming the SDK provides a method to get available commands
    commands = fanClient.get_device_commands(device_id)
    return jsonify(commands)


@app.route('/fans/<device_id>/speed', methods=['POST'])
def set_fan_speed(device_id):
    if device_id not in listOfFans:
        return jsonify({'error': 'Fan not found'}), 404

    speed = request.json.get('speed')
    if speed is None:
        return jsonify({'error': 'Speed not provided'}), 400

    fanClient.set_device_speed(device_id, speed)
    return jsonify({'status': 'success'})


@app.route('/fans/<device_id>/clock', methods=['POST'])
def set_real_time_clock(device_id):
    if device_id not in listOfFans:
        return jsonify({'error': 'Fan not found'}), 404

    clock_time = request.json.get('clock_time')
    if clock_time is None:
        return jsonify({'error': 'Clock time not provided'}), 400

    fanClient.set_device_clock(device_id, clock_time)
    return jsonify({'status': 'success'})


@app.route('/fans/<device_id>/filter', methods=['POST'])
def reset_filter_timer(device_id):
    if device_id not in listOfFans:
        return jsonify({'error': 'Fan not found'}), 404

    fanClient.reset_device_filter_timer(device_id)
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)
