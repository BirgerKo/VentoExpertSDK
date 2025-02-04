# Implements a class for the UDP data packet
from .mode import Mode
from .ventoPacket import VentoExpertPacket
from VentoExpertSDK import ventoProtocol as protocol
import traceback


class ResponsePacket(VentoExpertPacket):
    # A UDP data packet from the device

    parameter_size = {
        # see ventoProtocol.py for documentation to avoid duplicates here
        # see Blauberg doc for packet lenghts and other detailed documentation
        protocol.ON_OFF: 1,
        protocol.SPEED: 1,
        protocol.BOOST_MODE_STATUS: 1,
        protocol.TIMER_MODE: 1,
        protocol.TIMER_COUNTDOWN: 3,
        protocol.HUMIDITY_SENSOR: 1,
        protocol.RELAY_SENSOR: 1,
        protocol.ZERO_10V_SENSOR: 1,
        protocol.HUMIDITY_THRESHOLD_SETPOINT: 1,
        protocol.CURRENT_RTC_BATTERY_VOLTAGE: 2,
        protocol.CURRENT_HUMIDITY: 1,
        protocol.CURRENT_ZERO_10V_SENSOR_VALUE: 1,
        protocol.CURRENT_REALY_SENSOR_STATE: 1,
        protocol.SUPPLY_FAN_SPEED1: 1,
        protocol.EXHAUST_FAN_SPEED1: 1,
        protocol.SUPPLY_FAN_SPEED2: 1,
        protocol.EXHAUST_FAN_SPEED2: 1,
        protocol.SUPPLY_FAN_SPEED3: 1,
        protocol.EXHAUST_FAN_SPEED3: 1,
        protocol.MANUAL_SPEED: 1,
        protocol.FAN1RPM: 2,
        protocol.FAN2RPM: 2,
        protocol.FILTER_REPLACEMENT_TIME: 2,
        protocol.FILTER_TIMER: 3,
        protocol.RESET_FILTER_TIMER: 1,
        protocol.BOST_MODE_DEACTIVATION_SETPOINT: 1,
        protocol.RTC_TIME: 3,
        protocol.RTC_CALENDAR: 4,
        protocol.WEEKLY_SCHEDULE_MODE: 1,
        protocol.SCHEDULE_SETUP: 6,
        protocol.SEARCH: 16,
        protocol.DEVICE_PASSWORD: 0,
        protocol.MACHINE_HOURS: 4,
        protocol.RESET_ALARMS: 1,
        protocol.READ_ALARM: 1,
        protocol.CLOUD_OPERATION: 1,
        protocol.READ_FIRMWARE_VERSION: 6,
        protocol.RESTORE_FACTORY_SETTINGS: 1,
        protocol.FILTER_ALARM: 1,
        protocol.WIFI_OPERATION_MODE: 1,
        protocol.WIFI_CLIENT_NAME: 0,
        protocol.WIFI_PASSWORD: 0,
        protocol.WIFI_ENCRYPTION: 1,
        protocol.WIFI_CHANNEL: 1,
        protocol.WIFI_IP_MODE: 1,
        protocol.ASSIGNED_IP_ADDRESS: 4,
        protocol.ASSIGNED_IP_SUBNET_MASK: 4,
        protocol.ASSIGNED_IP_GATEWAY: 4,
        protocol.APPLY_QUIT_SETUP_MODE: 1,
        protocol.DISCARD_QUIT_SETUP_MODE: 1,
        protocol.CURRENT_IP_ADDRESS: 4,
        protocol.VENTILATION_MODE: 1,
        protocol.UNIT_TYPE: 2,
        protocol.SC_CHANGE_FUNCTION_NUMBER: 1,  # Just dummy so all are in the list. Length will vary.
        protocol.SC_PARAMETER_NOT_SUPPORTED: 1,
        protocol.SC_CHANGE_VALUE_SIZE: 1,       # Just dummy so all are in the list. Length will vary.
        protocol.SC_CHANGE_HIGH_BYTE: 1,
        protocol.NIGHT_MODE_TIMER_SETPOINT: 3,
        protocol.PARTY_MODE_TIMER_SETPOINT: 3,
        protocol.HUMIDITY_SETPOINT_STATUS: 1,
        protocol.ZERO_10V_SENSOR_STATUS: 1,
    }

    def __print_data(self, data):
        """Print data in hex - for debugging purpose """
        print(" ".join("{:02x}".format(x) for x in data), " in responsepacket")

    def __init__(self):
        super(ResponsePacket, self).__init__()
        self.device_id = None
        self.device_password = None
        self.is_on = None
        self.speed = None
        self.boostModeStatus = None
        self.timerMode = None
        self.timerCountdown = None
        self.humiditySensor = None
        self.relaySensor = None
        self.voltSensorMode = None
        self.humidityThreshholdSetpoint = None
        self.rtcBatteryVolt = None
        self.humidity = None            # Current humidity
        self.manualspeed = None
        self.fan1rpm = None
        self.fan2rpm = None
        self.mode: Mode = None
        self.filter_alarm = None
        self.filter_timer_minutes = None    # interg representation
        self.filter_timer_hours = None      # interg representation
        self.filter_timer_days = None       # interg representation
        self.filter_timer = None            # String with all parameters
        self.search_device_id = None
        self.firmware_version = None
        self.firmware_date = None
        self.unit_type = None
        self.fan_rtc_date = None
        self.fan_rtc_time = None

    def initialize_from_data(self, data) -> bool:
        """Initialize a packet from data received from the device
        Returns False if the data is invalid
        """
        try:
            self._data = data
            # print(f"Initialize. Data: {self.__print_data(data)}")
            size = len(data)
            if size < 4 or not self.is_header_ok():
                return False
            checksum = self.calc_checksum(size - 2)
            datachecksum = self._data[size - 2] + (self._data[size - 1] << 8)
            if checksum != datachecksum:
                return False
            self.device_id = self.read_string()
            self.device_password = self.read_string()
            func = self.read_byte()
            if func != protocol.RESPONSE:
                # The search command sent out to "DEFAULT_DEVICEID" will be read here as it goes out as a broadcast and is received with type READ.
                # That is not a fault. "DEFAULT_DEVICEID" is a special device ID that Blauberg VEnto uses to search for devices on the network.
                return False
            return self.read_parameters()
        except Exception:
            print("EXCEPTION in init data")
            traceback.print_exc()
            return False

    def is_header_ok(self):
        if self.read_byte() != 0xFD or self.read_byte() != 0xFD:
            return False
        return self.read_byte() == 0x02

    def read_byte(self) -> int:
        byte = self._data[self._pos]
        self._pos = self._pos + 1
        return byte

    def read_string(self) -> str:
        strlen = self.read_byte()
        txt = ""
        for i in range(self._pos, self._pos + strlen):
            txt += chr(self._data[i])
        self._pos += strlen
        return txt

    def read_parameters(self) -> bool:
        # print(f"Read param. Data: {self.__print_data(self._data)}")
        length_data = len(self._data)
        while self._pos < (length_data - 3):
            size = 1        # parameter size always one if it's not an extended parameter
            parameters = self.read_byte()

            # Special handling of parameters that has more than one byte package
            if parameters == protocol.SC_CHANGE_VALUE_SIZE:
                # print(f"FE Parameter to be processed: {hex(parameters)}")
                size = self.read_byte()
                parameters = self.read_byte()   # read the extended lenght parameter

            # print(f"Parameter to be processed: {hex(parameters)}")
            ''' The cases are not in alphabetical order, but the same oreder as in the Blauberg Vento protocol desription
            for parameteres to make it easier to find the parameter in the list '''
            match parameters:
                case protocol.ON_OFF:
                    self.is_on = self._data[self._pos] != 0
                case protocol.SPEED:
                    self.speed = self._data[self._pos]
                case protocol.CURRENT_RTC_BATTERY_VOLTAGE:
                    self.rtcBatteryVoltage = self._data[self._pos]
                case protocol.CURRENT_HUMIDITY:
                    self.humidity = self._data[self._pos]
                case protocol.MANUAL_SPEED:
                    self.manualspeed = self._data[self._pos]
                case protocol.FAN1RPM:
                    self.fan1rpm = self._data[self._pos] + (self._data[self._pos + 1] << 8)
                case protocol.FAN2RPM:
                    self.fan2rpm = self._data[self._pos] + (self._data[self._pos + 1] << 8)
                case protocol.VENTILATION_MODE:
                    self.mode = self._data[self._pos]
                case protocol.READ_FIRMWARE_VERSION:
                    major = self._data[self._pos]
                    minor = self._data[self._pos + 1]
                    self.firmware_version = f"{major}.{minor}"
                    day = self._data[self._pos + 2]
                    month = self._data[self._pos + 3]
                    year = self._data[self._pos + 4] + (self._data[self._pos + 5] << 8)
                    self.firmware_date = f"{day}-{month}-{year}"
                case protocol.UNIT_TYPE:
                    self.unit_type = self._data[self._pos]
                case protocol.FILTER_ALARM:
                    self.filter_alarm = self._data[self._pos]
                case protocol.FILTER_TIMER:
                    self.filter_timer_minutes = self._data[self._pos]
                    self.filter_timer_hours = self._data[self._pos + 1]
                    self.filter_timer_days = self._data[self._pos + 2]
                    self.filter_timer = (str(self.filter_timer_days)+" days " +
                                         str(self.filter_timer_hours)+" hours " +
                                         str(self.filter_timer_minutes)+" minutes")
                case protocol.SEARCH:
                    self.search_device_id = ""
                    for i in range(self._pos, self._pos + 16):
                        self.search_device_id += chr(self._data[i])
                case _:
                    if parameters not in self.parameter_size:
                        print(f"UNEXPECTE PARAMETER : {hex(parameters)}")
                        return False
                    size = self.parameter_size[parameters]

            self._pos += size
        if self.is_on is not None and not self.is_on:
            self.speed = protocol.SPEED_OFF

        return True
