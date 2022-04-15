# Implements a class for the UDP data packet
from .mode import Mode
from .ventoPacket import VentoExpertPacket
from VentoExpertSDK.source import function
from VentoExpertSDK.source import parameter
from VentoExpertSDK.source import speed
import traceback


class ResponsePacket(VentoExpertPacket):
    # A udp data packet from the device

    parameter_size = {
        # see parmeter.py for documentation to avoid duplicates here
        # see Blauberg doc for packet lenghts documentation
        parameter.ON_OFF: 1,
        parameter.SPEED: 1,
        parameter.BOOST_MODE_STATUS: 1,
        parameter.TIMER_MODE: 1,
        parameter.TIMER_COUNTDOWN: 3,
        parameter.HUMIDITY_SENSOR: 1,
        parameter.RELAY_SENSOR: 1,
        parameter.ZERO_10V_SENSOR: 1,
        parameter.HUMIDITY_THRESHOLD_SETPOINT: 1,
        parameter.CURRENT_RTC_BATTERY_VOLTAGE: 2,
        parameter.CURRENT_HUMIDITY: 1,
        parameter.CURRENT_ZERO_10V_SENSOR_VALUE: 1,
        parameter.CURRENT_REALY_SENSOR_STATE: 1,
        parameter.MANUAL_SPEED: 1,
        parameter.FAN1RPM: 2,
        parameter.FAN2RPM: 2,
        parameter.FILTER_TIMER: 3,
        parameter.RESET_FILTER_TIMER: 1,
        parameter.BOST_MODE_DEACTIVATION_SETPOINT: 1,
        parameter.RTC_TIMER: 3,
        parameter.RTC_CALENDAR: 4,
        parameter.WEEKLY_SCHEDULE_MODE: 1,
        parameter.SCHEDULE_SETUP: 6,
        parameter.SEARCH: 16,
        parameter.DEVICE_PASSWORD: 0,
        parameter.MACHINE_HOURS: 4,
        parameter.RESET_ALARMS: 1,
        parameter.READ_ALARM: 1,
        parameter.CLOUD_OPERATION: 1,
        parameter.READ_FIRMWARE_VERSION: 6,
        parameter.RESTORE_FACTORY_SETTINGS: 1,
        parameter.FILTER_ALARM: 1,
        parameter.WIFI_OPERATION_MODE: 1,
        parameter.WIFI_CLIENT_NAME: 0,
        parameter.WIFI_PASSWORD: 0,
        parameter.WIFI_ENCRYPTION: 1,
        parameter.WIFI_CHANNEL: 1,
        parameter.WIFI_IP_MODE: 1,
        parameter.ASSIGNED_IP_ADDRESS: 4,
        parameter.ASSIGNED_IP_SUBNET_MASK: 4,
        parameter.ASSIGNED_IP_GATEWAY: 4,
        parameter.APPLY_QUIT_SETUP_MODE: 1,
        parameter.DISCARD_QUIT_SETUP_MODE: 1,
        parameter.CURRENT_IP_ADDRESS: 4,
        parameter.VENTILATION_MODE: 1,
        parameter.UNIT_TYPE: 2,
        parameter.SC_CHANGE_FUNCTION_NUMBER: 1,  # Just dummy so all are in the list. Length will vary.
        parameter.SC_PARAMETER_NOT_SUPPORTED: 1,
        parameter.SC_CHANGE_VALUE_SIZE: 1,       # Just dummy so all are in the list. Length will vary.
        parameter.SC_CHANGE_HIGH_BYTE: 1,
        parameter.NIGHT_MODE_TIMER_SETPOINT: 3,
        parameter.PARTY_MODE_TIMER_SETPOINT: 3,
        parameter.HUMIDITY_SETPOINT_STATUS: 1,
        parameter.ZERO_10V_SENSOR_STATUS: 1,
    }

    def __print_data(self, data):
        """Print data in hex - for debugging purpose """
        print(" ".join("{:02x}".format(x) for x in data), " in responsepacket")

    def __init__(self):
        super(ResponsePacket, self).__init__()
        self.device_id = None
        self.device_password = None
        self.is_on = None
        self.speed: Speed = None
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

    def initialize_from_data(self, data) -> bool:
        """Initialize a packet from data revieved from the device
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
            if func != function.RESPONSE:
                # The search command sent out to "DEFAULT_DEVICEID" will be read here as it goes out as a broadcast and is received with type READ.
                # That is not a fault.
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
            if parameters == parameter.SC_CHANGE_VALUE_SIZE:
                # print(f"FE Parameter to be processed: {hex(parameters)}")
                size = self.read_byte()
                parameters = self.read_byte()   # read the extended lenght parameter

            # print(f"Parameter to be processed: {hex(parameters)}")
            match parameters:
                case parameter.ON_OFF:
                    self.is_on = self._data[self._pos] != 0
                case parameter.SPEED:
                    self.speed = self._data[self._pos]
                case parameter.MANUAL_SPEED:
                    self.manualspeed = self._data[self._pos]
                case parameter.FAN1RPM:
                    self.fan1rpm = self._data[self._pos] + (self._data[self._pos + 1] << 8)
                case parameter.FAN2RPM:
                    self.fan2rpm = self._data[self._pos] + (self._data[self._pos + 1] << 8)
                case parameter.CURRENT_HUMIDITY:
                    self.humidity = self._data[self._pos]
                case parameter.VENTILATION_MODE:
                    self.mode = self._data[self._pos]
                case parameter.READ_FIRMWARE_VERSION:
                    major = self._data[self._pos]
                    minor = self._data[self._pos + 1]
                    self.firmware_version = f"{major}.{minor}"
                    day = self._data[self._pos + 2]
                    month = self._data[self._pos + 3]
                    year = self._data[self._pos + 4] + (self._data[self._pos + 5] << 8)
                    self.firmware_date = f"{day}-{month}-{year}"
                case parameter.UNIT_TYPE:
                    self.unit_type = self._data[self._pos]
                case parameter.FILTER_ALARM:
                    self.filter_alarm = self._data[self._pos]
                case parameter.FILTER_TIMER:
                    self.filter_timer_minutes = self._data[self._pos]
                    self.filter_timer_hours = self._data[self._pos + 1]
                    self.filter_timer_days = self._data[self._pos + 2]
                    self.filter_timer = (str(self.filter_timer_days)+" days " +
                                         str(self.filter_timer_hours)+" hours " +
                                         str(self.filter_timer_minutes)+" minutes")
                case parameter.SEARCH:
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
            self.speed = Speed.OFF

        return True
