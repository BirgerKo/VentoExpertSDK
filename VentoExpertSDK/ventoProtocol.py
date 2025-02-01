"""Blauberg protocol Parameters constant library.
Kept in a separate file to have this readable notation.

Packet structure from the Blauberg documentaiton
0xFD | 0xFD | TYPE | SIZE ID | ID | SIZE PWD | PWD | FUNC | DATA | Chksum L | Chksum H |

0xFD - packet beginning character (2 x 1 byte)
TYPE - protocol type (1 byte)
SIZE ID - size of the ID field (1 byte)
ID - device ID (16 bytes)
SIZE PWD - size of the password field (1 byte)
PWD - device password (1-8 bytes)
FUNC - function number (1 byte)
    0x01: R     parameter read.
    0x02: INC   parameter write. The controller does not send any response regarding the status of the given parameters.
    0x03: RW    parameter write with subsequent controller response regarding the status of the given parameters.
    0x04: W     parameter increment with subsequent controller response regarding the status of the given parameters.
    0x05: DEC   parameter decrement with subsequent controller response regarding the status of the given parameters.
    0x06:       controller response to the request (FUNC = 0x01, 0x03, 0x04, 0x05).
DATA - parameter or parameter-value (1-255 bytes)
Chksum L -  low byte of the checksum (1 byte)
Chksum H -  high byte of the checksum (1 byte) . This is calculated as the total of bytes beginning with the TYPE byte
            and ending with the final byte of the DATA block.

For further detrails consult the Blauberg documentation referenced in the readme.md file for the project.
"""

"""Constants determening Read/Write mode for packets to a fan device as well as reponse packet from the device"""

READ = 0x01         # parameter read
WRITE = 0x02        # parameter write. The controller does not send any response regarding the status of the given parameters
WRITEREAD = 0x03    # parameter write with subsequent controller response regarding the status of the given parameters
INCREAD = 0x04      # parameter increment with subsequent controller response regarding the status of the given parameters
DECREAD = 0x05      # parameter decrement with subsequent controller response regarding the status of the given parameters
RESPONSE = 0x06     # controller response to the request (FUNC = 0x01(READ), 0x03(WRITEREAD), 0x04(INCREAD), 0x05(DECREAD))

"""Packet structure constants"""
PACKET_START_CHARACTER = 0xFD   # Packet beginning character. Shall be repeated in 2 following bytes for each packet. 0xFD,0xFD
PROTOCOL_TYPE = 0x02            # protocol type (1 byte). Value = 0x02

"""Packet Parameter values"""
ON_OFF = 0x01                 # R/W/RW          0 — Off,1 — On, 2 – Invert
SPEED = 0x02                  # R/W/RW/INC/DEC  1 – Speed 1, 2 – Speed 2, 3 – Speed 3, 255 – manual speed setting mode (see parameter 68)
BOOST_MODE_STATUS = 0x06      # R               0 – Off,1 – On
TIMER_MODE = 0x07             # R/W/RW/INC/DEC  0 – Off, 1 – Night mode, 2 – "Party" mode
TIMER_COUNTDOWN = 0x0B        # R               Byte 1 – seconds (0…59), Byte 2 – minutes (0…59), Byte 3 – hours (0…23). Countdown for current mode
HUMIDITY_SENSOR = 0x0F        # R/W/RW          0 — Off,1 — On, 2 – Invert
RELAY_SENSOR = 0x14           # R/W/RW          0 — Off,1 — On, 2 – Invert
ZERO_10V_SENSOR = 0x16        # R/W/RW          0 — Off,1 — On, 2 – Invert
HUMIDITY_THRESHOLD_SETPOINT = 0x19      # R/W/RW/INC/DEC    40…80 RH%
CURRENT_RTC_BATTERY_VOLTAGE = 0x24      # R     0…5000 mV
CURRENT_HUMIDITY = 0x25                 # R     0…100 RH%
CURRENT_ZERO_10V_SENSOR_VALUE = 0x2D    # R     0…100 %
CURRENT_REALY_SENSOR_STATE = 0x32       # R     0 – Off,1 – On
SUPPLY_FAN_SPEED1 = 0x3A            # R/W/RW/INC/DEC    Supply fan speed in 1st speed mode 10..255  Available for VENTO Expert A50-1 W V.3.
EXHAUST_FAN_SPEED1 = 0x3B           # R/W/RW/INC/DEC    Exhaust fan speed in 1st speed mode 10..255 Available for VENTO Expert A50-1 W V.3.
SUPPLY_FAN_SPEED2 = 0x3C            # R/W/RW/INC/DEC    Supply fan speed in 2nd speed mode 10..255  Available for VENTO Expert A50-1 W V.3.
EXHAUST_FAN_SPEED2 = 0x3D           # R/W/RW/INC/DEC    Exhaust fan speed in 2nd speed mode 10..255 Available for VENTO Expert A50-1 W V.3.
SUPPLY_FAN_SPEED3 = 0x3E            # R/W/RW/INC/DEC    Supply fan speed in 3rd speed mode 10..255  Available for VENTO Expert A50-1 W V.3.
EXHAUST_FAN_SPEED3 = 0x3F           # R/W/RW/INC/DEC    Exhaust fan speed in 3rd speed mode 10..255 Available for VENTO Expert A50-1 W V.3.
MANUAL_SPEED = 0x44                 # R/W/RW/INC/DEC  0…255
FAN1RPM = 0x4A                      # R               0…5000 rpm
FAN2RPM = 0x4B                      # R               0…5000 rpm
FILTER_REPLACEMENT_TIME = 0x63      # R/W/RW/INC/DEC Filter replacement timer setup 70…365 days Available for VENTO Expert A50-1 W V.3.
FILTER_TIMER = 0x64                 # R               Timer countdown to filter replacement. Byte 1 –minutes(0…59), Byte 2 –hours(0…23), Byte 3 –days(0…181)
RESET_FILTER_TIMER = 0x65           # W               Reset timer countdown to filter replacement, Any byte
BOST_MODE_DEACTIVATION_SETPOINT = 0x66  # R/W/RW/INC/DEC        0…60 minutes
RTC_TIME = 0x6F                     # R/W/RW          Byte 1 – seconds (0…59), Byte 2 – minutes (0…59), Byte 3 – hours (0…23)
RTC_CALENDAR = 0x70                 # R/W/RW          Byte 1 – RTC number (1…31), Byte 2 – RTC day of the week (1…7), Byte 3 – RTC month (1…12),
#                                               Byte 4 - RTC year (0...99)
WEEKLY_SCHEDULE_MODE = 0x72   # R/W/RW          0 — Off,1 — On, 2 – Invert
SCHEDULE_SETUP = 0x77         # Consult Blauberg documentation
SEARCH = 0x7C                 # R               Device search on the local network. ID - Text („0…9“, „A…F“) 16 bytes
DEVICE_PASSWORD = 0x7D        # R/W/RW          Text („0…9“, „a…z“, „A…Z“) 0-8 bytes
MACHINE_HOURS = 0x7E          # R               Byte 1 – minutes (0…59), Byte 2 – hours (0…23), Byte 3 and Byte 4 – days (0…65535)
RESET_ALARMS = 0x80           # W               Any byte
READ_ALARM = 0x83             # R               0 – No, 1 – alarm (highest priority), 2 – warning
CLOUD_OPERATION = 0x85        # R/W/RW          0 — Off,1 — On, 2 – Invert
READ_FIRMWARE_VERSION = 0x86  # R               Byte 1 – firmware version (major), Byte 2 – firmware version (minor),
#                                               Byte 3 – day, Byte 4 – month, Byte 5 and Byte 6 – year
RESTORE_FACTORY_SETTINGS = 0x87   # W           Any byte
FILTER_ALARM = 0x88           # R               Filter replacement indicator. 0 – filter replacement not required, 1 – replace filter
WIFI_OPERATION_MODE = 0x94    # R/W/RW/INC/DEC  1 – Client, 2 – Access Point
WIFI_CLIENT_NAME = 0x95       # R/W/RW          Text
WIFI_PASSWORD = 0x96          # R/W/RW          Text
WIFI_ENCRYPTION = 0x99        # R/W/RW          48 – OPEN, 50 – WPA_PSK, 51 – WPA2_PSK, 52 – WPA_WPA2_PSK
WIFI_CHANNEL = 0x9A           # R/W/RW/INC/DEC  1…13
WIFI_IP_MODE = 0x9B           # R/W/RW          0 – STATIC, 1 – DHCP, 2 – Invert
ASSIGNED_IP_ADDRESS = 0x9C      # R/W/RW        Byte 1 – 0…255, Byte 2 – 0…255, Byte 3 – 0…255, Byte 4 – 0…255
ASSIGNED_IP_SUBNET_MASK = 0x9D  # R/W/RW        Byte 1 – 0…255, Byte 2 – 0…255, Byte 3 – 0…255, Byte 4 – 0…255
ASSIGNED_IP_GATEWAY = 0x9E      # R/W/RW        Byte 1 – 0…255, Byte 2 – 0…255, Byte 3 – 0…255, Byte 4 – 0…255
APPLY_QUIT_SETUP_MODE = 0xA0    # W             Apply new Wi-Fi parameters and quit Setup Mode.      Any byte
DISCARD_QUIT_SETUP_MODE = 0xA2  # W             Discard new Wi-Fi parameters and quit Setup Mode.    Any byte
CURRENT_IP_ADDRESS = 0xA3       # R             Byte 1 – 0…255, Byte 2 – 0…255, Byte 3 – 0…255, Byte 4 – 0…255
VENTILATION_MODE = 0xB7         # R/W/RW/INC/DEC  0 – ventilation, 1 – heat recovery, 2 – supply
ZERO_10V_SENSOR_THRESHOLD = 0xB8  # R/W/RW/INC/DEC  5…100 % 1 byte
UNIT_TYPE = 0xB9                # R             3: Vento Expert A50-1 W V.2, Vento Expert A85-1 W V.2, Vento Expert A100-1 W V.2,
#                                               4: Vento Expert Duo A30-1 W V.2, 5: Vento Expert A30 W V.2
SC_CHANGE_FUNCTION_NUMBER = 0XFC    # Change function (FUNC) number. The following byte must be the new function number ranging from 0x01 to 0x05.
# This Special Command is used to organise several functions with different actions into a single packet.
SC_PARAMETER_NOT_SUPPORTED = 0xFD   # Parameter not supported by the controller. The following byte is the low byte of the non-supported
# parameter. This Special Command is used in controller response (FUNC = 0x06) to a non-supported parameter read or write request.
SC_CHANGE_VALUE_SIZE = 0xFE         # Change a size of the Value for one parameter which follows. The following byte must be the new parameter
#                                     size followed by the low byte of the parameter number, and then – by the Value itself
SC_CHANGE_HIGH_BYTE = 0xFF          # Change the high byte for parameter numbers within a single packet. The following byte must be the new high byte.
NIGHT_MODE_TIMER_SETPOINT = 0x302   # R/W/RW    Byte 1 – minutes (0…59), Byte 2 – hours (0…23)
PARTY_MODE_TIMER_SETPOINT = 0x303   # R/W/RW    Byte 1 – minutes (0…59), Byte 2 – hours (0…23)
HUMIDITY_SETPOINT_STATUS = 0x304    # R         0 – below setpoint, 1 – over setpoint
ZERO_10V_SENSOR_STATUS = 0x305      # R         0 – below setpoint, 1 – over setpoint


"""Constants determening ventilation speed mode for the fan device"""
SPEED_OFF = 0
SPEED_LOW = 1
SPEED_MEDIUM = 2
SPEED_HIGH = 3
SPEED_MANUAL = 255

"""Lists with available parameters for the different ventilators"""
VENTO_EXPERT_A30_W_V2_PARAMETERS = [ON_OFF, SPEED, BOOST_MODE_STATUS, TIMER_MODE, TIMER_COUNTDOWN, HUMIDITY_SENSOR, RELAY_SENSOR, HUMIDITY_THRESHOLD_SETPOINT,
                                    CURRENT_RTC_BATTERY_VOLTAGE, CURRENT_HUMIDITY, CURRENT_REALY_SENSOR_STATE, MANUAL_SPEED,
                                    FAN1RPM, FAN2RPM, FILTER_TIMER, RESET_FILTER_TIMER, BOST_MODE_DEACTIVATION_SETPOINT, RTC_TIME, RTC_CALENDAR,
                                    WEEKLY_SCHEDULE_MODE, SCHEDULE_SETUP, SEARCH, DEVICE_PASSWORD, MACHINE_HOURS, RESET_ALARMS, READ_ALARM, CLOUD_OPERATION,
                                    READ_FIRMWARE_VERSION, RESTORE_FACTORY_SETTINGS, FILTER_ALARM, WIFI_OPERATION_MODE, WIFI_CLIENT_NAME, WIFI_PASSWORD,
                                    WIFI_ENCRYPTION, WIFI_CHANNEL, WIFI_IP_MODE, ASSIGNED_IP_ADDRESS, ASSIGNED_IP_SUBNET_MASK, ASSIGNED_IP_GATEWAY,
                                    APPLY_QUIT_SETUP_MODE, DISCARD_QUIT_SETUP_MODE, CURRENT_IP_ADDRESS, VENTILATION_MODE, UNIT_TYPE,
                                    SC_CHANGE_FUNCTION_NUMBER, SC_PARAMETER_NOT_SUPPORTED, SC_CHANGE_VALUE_SIZE, SC_CHANGE_HIGH_BYTE, NIGHT_MODE_TIMER_SETPOINT,
                                    PARTY_MODE_TIMER_SETPOINT, HUMIDITY_SETPOINT_STATUS]

VENTO_EXPERT_A50_1_W_V2_PARAMETERS = [ON_OFF, SPEED, BOOST_MODE_STATUS, TIMER_MODE, TIMER_COUNTDOWN, HUMIDITY_SENSOR, RELAY_SENSOR, ZERO_10V_SENSOR,
                                      HUMIDITY_THRESHOLD_SETPOINT, CURRENT_RTC_BATTERY_VOLTAGE, CURRENT_HUMIDITY, CURRENT_ZERO_10V_SENSOR_VALUE,
                                      CURRENT_REALY_SENSOR_STATE, MANUAL_SPEED, FAN1RPM, FAN2RPM, FILTER_TIMER, RESET_FILTER_TIMER,
                                      BOST_MODE_DEACTIVATION_SETPOINT, RTC_TIME, RTC_CALENDAR, WEEKLY_SCHEDULE_MODE, SCHEDULE_SETUP, SEARCH, DEVICE_PASSWORD,
                                      MACHINE_HOURS, RESET_ALARMS, READ_ALARM, CLOUD_OPERATION, READ_FIRMWARE_VERSION, RESTORE_FACTORY_SETTINGS,
                                      FILTER_ALARM, WIFI_OPERATION_MODE, WIFI_CLIENT_NAME, WIFI_PASSWORD, WIFI_ENCRYPTION, WIFI_CHANNEL, WIFI_IP_MODE,
                                      ASSIGNED_IP_ADDRESS, ASSIGNED_IP_SUBNET_MASK, ASSIGNED_IP_GATEWAY, APPLY_QUIT_SETUP_MODE, DISCARD_QUIT_SETUP_MODE,
                                      CURRENT_IP_ADDRESS, VENTILATION_MODE, ZERO_10V_SENSOR_THRESHOLD, UNIT_TYPE, SC_CHANGE_FUNCTION_NUMBER,
                                      SC_PARAMETER_NOT_SUPPORTED, SC_CHANGE_VALUE_SIZE, SC_CHANGE_HIGH_BYTE, NIGHT_MODE_TIMER_SETPOINT,
                                      PARTY_MODE_TIMER_SETPOINT, HUMIDITY_SETPOINT_STATUS, ZERO_10V_SENSOR_STATUS]

VENTO_EXPERT_A85_1_W_V2_PARAMETERS = [ON_OFF, SPEED, BOOST_MODE_STATUS, TIMER_MODE, TIMER_COUNTDOWN, HUMIDITY_SENSOR, RELAY_SENSOR, ZERO_10V_SENSOR,
                                      HUMIDITY_THRESHOLD_SETPOINT, CURRENT_RTC_BATTERY_VOLTAGE, CURRENT_HUMIDITY, CURRENT_ZERO_10V_SENSOR_VALUE,
                                      CURRENT_REALY_SENSOR_STATE, MANUAL_SPEED, FAN1RPM, FAN2RPM, FILTER_TIMER, RESET_FILTER_TIMER,
                                      BOST_MODE_DEACTIVATION_SETPOINT, RTC_TIME, RTC_CALENDAR, WEEKLY_SCHEDULE_MODE, SCHEDULE_SETUP,
                                      SEARCH, DEVICE_PASSWORD, MACHINE_HOURS, RESET_ALARMS, READ_ALARM, CLOUD_OPERATION, READ_FIRMWARE_VERSION,
                                      RESTORE_FACTORY_SETTINGS, FILTER_ALARM, WIFI_OPERATION_MODE, WIFI_CLIENT_NAME, WIFI_PASSWORD, WIFI_ENCRYPTION,
                                      WIFI_CHANNEL, WIFI_IP_MODE, ASSIGNED_IP_ADDRESS, ASSIGNED_IP_SUBNET_MASK, ASSIGNED_IP_GATEWAY, APPLY_QUIT_SETUP_MODE,
                                      DISCARD_QUIT_SETUP_MODE, CURRENT_IP_ADDRESS, VENTILATION_MODE, ZERO_10V_SENSOR_THRESHOLD, UNIT_TYPE,
                                      SC_CHANGE_FUNCTION_NUMBER, SC_PARAMETER_NOT_SUPPORTED, SC_CHANGE_VALUE_SIZE, SC_CHANGE_HIGH_BYTE,
                                      NIGHT_MODE_TIMER_SETPOINT, PARTY_MODE_TIMER_SETPOINT, HUMIDITY_SETPOINT_STATUS, ZERO_10V_SENSOR_STATUS]

VENTO_EXPERT_A100_1_W_V2_PARAMETERS = [ON_OFF, SPEED, BOOST_MODE_STATUS, TIMER_MODE, TIMER_COUNTDOWN, HUMIDITY_SENSOR, RELAY_SENSOR, ZERO_10V_SENSOR,
                                       HUMIDITY_THRESHOLD_SETPOINT, CURRENT_RTC_BATTERY_VOLTAGE, CURRENT_HUMIDITY, CURRENT_ZERO_10V_SENSOR_VALUE,
                                       CURRENT_REALY_SENSOR_STATE, MANUAL_SPEED, FAN1RPM, FAN2RPM, FILTER_TIMER, RESET_FILTER_TIMER,
                                       BOST_MODE_DEACTIVATION_SETPOINT, RTC_TIME, RTC_CALENDAR, WEEKLY_SCHEDULE_MODE, SCHEDULE_SETUP, SEARCH, DEVICE_PASSWORD,
                                       MACHINE_HOURS, RESET_ALARMS, READ_ALARM, CLOUD_OPERATION, READ_FIRMWARE_VERSION, RESTORE_FACTORY_SETTINGS,
                                       FILTER_ALARM, WIFI_OPERATION_MODE, WIFI_CLIENT_NAME, WIFI_PASSWORD, WIFI_ENCRYPTION, WIFI_CHANNEL, WIFI_IP_MODE,
                                       ASSIGNED_IP_ADDRESS, ASSIGNED_IP_SUBNET_MASK, ASSIGNED_IP_GATEWAY, APPLY_QUIT_SETUP_MODE, DISCARD_QUIT_SETUP_MODE,
                                       CURRENT_IP_ADDRESS, VENTILATION_MODE, ZERO_10V_SENSOR_THRESHOLD, UNIT_TYPE, SC_CHANGE_FUNCTION_NUMBER,
                                       SC_PARAMETER_NOT_SUPPORTED, SC_CHANGE_VALUE_SIZE, SC_CHANGE_HIGH_BYTE, NIGHT_MODE_TIMER_SETPOINT,
                                       PARTY_MODE_TIMER_SETPOINT, HUMIDITY_SETPOINT_STATUS, ZERO_10V_SENSOR_STATUS]

VENTO_EXPERT_DUO_A30_1_W_V2_PARAMETERS = [ON_OFF, SPEED, BOOST_MODE_STATUS, TIMER_MODE, TIMER_COUNTDOWN, HUMIDITY_SENSOR, RELAY_SENSOR, ZERO_10V_SENSOR,
                                          HUMIDITY_THRESHOLD_SETPOINT, CURRENT_RTC_BATTERY_VOLTAGE, CURRENT_HUMIDITY, CURRENT_ZERO_10V_SENSOR_VALUE,
                                          CURRENT_REALY_SENSOR_STATE, MANUAL_SPEED, FAN1RPM, FAN2RPM, FILTER_TIMER, RESET_FILTER_TIMER,
                                          BOST_MODE_DEACTIVATION_SETPOINT, RTC_TIME, RTC_CALENDAR, WEEKLY_SCHEDULE_MODE, SCHEDULE_SETUP, SEARCH,
                                          DEVICE_PASSWORD, MACHINE_HOURS, RESET_ALARMS, READ_ALARM, CLOUD_OPERATION, READ_FIRMWARE_VERSION,
                                          RESTORE_FACTORY_SETTINGS, FILTER_ALARM, WIFI_OPERATION_MODE, WIFI_CLIENT_NAME, WIFI_PASSWORD, WIFI_ENCRYPTION,
                                          WIFI_CHANNEL, WIFI_IP_MODE, ASSIGNED_IP_ADDRESS, ASSIGNED_IP_SUBNET_MASK, ASSIGNED_IP_GATEWAY, APPLY_QUIT_SETUP_MODE,
                                          DISCARD_QUIT_SETUP_MODE, CURRENT_IP_ADDRESS, VENTILATION_MODE, ZERO_10V_SENSOR_THRESHOLD, UNIT_TYPE,
                                          SC_CHANGE_FUNCTION_NUMBER, SC_PARAMETER_NOT_SUPPORTED, SC_CHANGE_VALUE_SIZE, SC_CHANGE_HIGH_BYTE,
                                          NIGHT_MODE_TIMER_SETPOINT, PARTY_MODE_TIMER_SETPOINT, HUMIDITY_SETPOINT_STATUS, ZERO_10V_SENSOR_STATUS]

VENTO_EXPERT_A50_1_W_V3_PARAMETERS = [ON_OFF, SPEED, BOOST_MODE_STATUS, TIMER_MODE, TIMER_COUNTDOWN, HUMIDITY_SENSOR, RELAY_SENSOR, ZERO_10V_SENSOR,
                                      HUMIDITY_THRESHOLD_SETPOINT, CURRENT_RTC_BATTERY_VOLTAGE, CURRENT_HUMIDITY, CURRENT_ZERO_10V_SENSOR_VALUE,
                                      CURRENT_REALY_SENSOR_STATE, SUPPLY_FAN_SPEED1, EXHAUST_FAN_SPEED1, SUPPLY_FAN_SPEED2, EXHAUST_FAN_SPEED2,
                                      SUPPLY_FAN_SPEED3, EXHAUST_FAN_SPEED3, MANUAL_SPEED, FAN1RPM, FAN2RPM, FILTER_REPLACEMENT_TIME, FILTER_TIMER,
                                      RESET_FILTER_TIMER, BOST_MODE_DEACTIVATION_SETPOINT, RTC_TIME, RTC_CALENDAR, WEEKLY_SCHEDULE_MODE, SCHEDULE_SETUP, SEARCH,
                                      DEVICE_PASSWORD, MACHINE_HOURS, RESET_ALARMS, READ_ALARM, CLOUD_OPERATION, READ_FIRMWARE_VERSION,
                                      RESTORE_FACTORY_SETTINGS, FILTER_ALARM, WIFI_OPERATION_MODE, WIFI_CLIENT_NAME, WIFI_PASSWORD, WIFI_ENCRYPTION,
                                      WIFI_CHANNEL, WIFI_IP_MODE, ASSIGNED_IP_ADDRESS, ASSIGNED_IP_SUBNET_MASK, ASSIGNED_IP_GATEWAY, APPLY_QUIT_SETUP_MODE,
                                      DISCARD_QUIT_SETUP_MODE, CURRENT_IP_ADDRESS, VENTILATION_MODE, ZERO_10V_SENSOR_THRESHOLD, UNIT_TYPE,
                                      SC_CHANGE_FUNCTION_NUMBER, SC_PARAMETER_NOT_SUPPORTED, SC_CHANGE_VALUE_SIZE, SC_CHANGE_HIGH_BYTE,
                                      NIGHT_MODE_TIMER_SETPOINT, PARTY_MODE_TIMER_SETPOINT, HUMIDITY_SETPOINT_STATUS, ZERO_10V_SENSOR_STATUS]
