"""Blauberg protocol Parameters constant library.
Kept in a separate file to have this readable notation. """

PROTOCOL_TYPE = 0x02          # protocol type (1 byte). Value = 0x02
PACKET_START_CHARACTER = 0xFD       # Packet beginning character. Shall be repeated in 2 following bytes for each packet. 0xFD,0xFD


# Parameter values
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
MANUAL_SPEED = 0x44           # R/W/RW/INC/DEC  0…255
FAN1RPM = 0x4A                # R               0…5000 rpm
FAN2RPM = 0x4B                # R               0…5000 rpm
FILTER_TIMER = 0x64           # R               Timer countdown to filter replacement. Byte 1 –minutes(0…59), Byte 2 –hours(0…23), Byte 3 –days(0…181)
RESET_FILTER_TIMER = 0x65     # W               Reset timer countdown to filter replacement, Any byte
BOST_MODE_DEACTIVATION_SETPOINT = 0x66  # R/W/RW/INC/DEC        0…60 minutes
RTC_TIMER = 0x6F              # R/W/RW          Byte 1 – seconds (0…59), Byte 2 – minutes (0…59), Byte 3 – hours (0…23)
RTC_CALENDAR = 0x70           # R/W/RW          Byte 1 – RTC number (1…31), Byte 2 – RTC day of the week (1…7), Byte 3 – RTC month (1…12),
#                                               Byte 4 - RTC year (0...99)
WEEKLY_SCHEDULE_MODE = 0x72   # R/W/RW          0 — Off,1 — On, 2 – Invert
SCHEDULE_SETUP = 0x77         # Consult Blauberg documentation
SEARCH = 0x7C                 # R               Device search on the local network. ID - Text („0…9“, „A…F“)
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
VENTILATION_MODE = 0xB7       # R/W/RW/INC/DEC  0 – ventilation, 1 – heat recovery, 2 – supply
UNIT_TYPE = 0xB9              # R               3: Vento Expert A50-1 W V.2, Vento Expert A85-1 W V.2, Vento Expert A100-1 W V.2,
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
