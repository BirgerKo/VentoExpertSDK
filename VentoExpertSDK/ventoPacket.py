# Implements a class for the UDP data packet
from .device import Device
from .mode import Mode

from VentoExpertSDK import ventoProtocol as protocol


class VentoExpertPacket:
    """ building the UDP data packet to/from the device
    Packet: 0xFD 0xFD TYPE SIZE_ID ID SIZE PWD PWD FUNC DATA(parameter or parameter-value) Chksum_L Chksum_H"""

    def __init__(self):
        self._data = None
        self._pos = 0
        self.maxsize = 200

    '''The following method initialize the Blauberg Vento data packet for the search command that can be sent to the fan'''
    def initialize_search_cmd(self):
        """Initialize a search command packet usingf the string "DEFAULT_DEVICEID" as the device ID
        "DEFAULT_DEVICEID" is a special device ID that Blauberg VEnto uses to search for devices on the network.
        The search is done by broadcasting the search command to the network on 255.255.255.255"""
        self.__build_data("DEFAULT_DEVICEID", "")
        self.__add_byte(protocol.READ)
        self.__add_byte(protocol.SEARCH)
        self.__add_checksum()

    def initialize_speed_cmd(self, device: Device, speed: int):
        """Initialize a speed command packet to be sent to a device"""
        self.__build_data(device.device_id, device.password)
        self.__add_byte(protocol.WRITEREAD)
        self.__add_byte(protocol.SPEED)
        self.__add_byte(speed)
        self.__add_checksum()

    def initialize_manualspeed_cmd(self, device: Device, manualspeed: int):
        """Initialize a manual speed command packet to be sent to a device
        The manuals speed is in the interval 0-255
        """
        self.__build_data(device.device_id, device.password)
        self.__add_byte(protocol.WRITEREAD)
        self.__add_byte(protocol.MANUAL_SPEED)
        self.__add_byte(manualspeed)
        self.__add_checksum()

    def initialize_mode_cmd(self, device: Device, mode: Mode):
        """Intialize a mode command packet to be sent to a device"""
        self.__build_data(device.device_id, device.password)
        self.__add_byte(protocol.WRITEREAD)
        self.__add_byte(protocol.VENTILATION_MODE)
        self.__add_byte(mode)
        self.__add_checksum()

    def initialize_on_cmd(self, device: Device):
        """Initialize a ON command packet to be sent to a device"""
        self.__build_data(device.device_id, device.password)
        self.__add_byte(protocol.WRITEREAD)
        self.__add_byte(protocol.ON_OFF)
        self.__add_byte(0x01)
        self.__add_checksum()

    def initialize_off_cmd(self, device: Device):
        """Initialize a Off command packet to be sent to a device"""
        self.__build_data(device.device_id, device.password)
        self.__add_byte(protocol.WRITEREAD)
        self.__add_byte(protocol.ON_OFF)
        self.__add_byte(0x00)
        self.__add_checksum()

    def initialize_status_cmd(self, device: Device):
        """Initialize a status command packet to be sent to a device"""
        self.__build_data(device.device_id, device.password)
        self.__add_byte(protocol.READ)
        self.__add_byte(protocol.ON_OFF)
        self.__add_byte(protocol.VENTILATION_MODE)
        self.__add_byte(protocol.SPEED)
        self.__add_byte(protocol.MANUAL_SPEED)
        self.__add_byte(protocol.FAN1RPM)
        self.__add_byte(protocol.FILTER_ALARM)
        self.__add_byte(protocol.FILTER_TIMER)
        self.__add_byte(protocol.CURRENT_HUMIDITY)
        self.__add_checksum()

    def initialize_reset_filter_alarm_cmd(self, device: Device):
        """Initialize a reset filter alarm command packet to be sent to a
        device"""
        self.__build_data(device.device_id, device.password)
        self.__add_byte(protocol.WRITE)
        self.__add_byte(protocol.RESET_FILTER_TIMER)
        self.__add_checksum()

    def initialize_get_firmware_cmd(self, device: Device):
        """Initialize a get firmware and unit type command packet to be sent to a
        device"""
        self.__build_data(device.device_id, device.password)
        self.__add_byte(protocol.READ)
        self.__add_byte(protocol.READ_FIRMWARE_VERSION)
        self.__add_byte(protocol.UNIT_TYPE)
        self.__add_checksum()

    @property
    def data(self):
        """Return the data for the packet"""
        return self._data[0: self._pos]

    def __add_byte(self, byte: int):
        """Add a byte to the packet"""
        self._data[self._pos] = byte
        self._pos += 1

    def __build_data(self, device_id: str, password: str):
        """Build a packet header with start characters, ID and password"""
        self._data = bytearray(self.maxsize)
        self._pos = 0
        self.__add_byte(protocol.PACKET_START_CHARACTER)
        self.__add_byte(protocol.PACKET_START_CHARACTER)
        self.__add_byte(protocol.PROTOCOL_TYPE)
        self.__add_byte(len(device_id))
        for char in device_id:
            self.__add_byte(ord(char))
        self.__add_byte(len(password))
        for char in password:
            self.__add_byte(ord(char))

    def __add_parameter(self, parameter: int, value):
        self.__add_byte(parameter)
        self.__add_byte(value)

    def __add_checksum(self):
        """Divides the checksum into two sepparate bytes and adds the checksum bytes to the data packet"""
        checksum = self.calc_checksum(self._pos)
        checksumLowByte = (checksum & 0xFF)
        checksumHighByte = (checksum >> 8)
        self.__add_byte(checksumLowByte)
        self.__add_byte(checksumHighByte)

    def calc_checksum(self, size) -> int:
        """Calculates the sum of data in the packet from Type to the final Data bloc and masks it down to two bytes"""
        checksum: int = 0
        for i in range(2, size):
            checksum += self._data[i]
        return (checksum & 0xFFFF)
