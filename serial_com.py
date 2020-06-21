# -*- coding: utf-8 -*-

import serial
import binascii


class SerialPort(object):
    def __init__(self, port, baud):
        self.port = serial.Serial(port, baud)
        self.port.close()
        if not self.port.isOpen():
            self.port.open()

    # Set Port Open
    def port_open(self):
        if not self.port.isOpen():
            self.port.open()

    # Set Port Close
    def port_close(self):
        self.port.close()

    # Set Send Data
    def send_data(self, angle0, angle1, angle2, angle3, speed):
        if self.port.isOpen():
            cmd_ascii = '$A,' + str(angle0) + ',' + str(angle1) + ',' + str(angle2) + ',' + str(angle3) + \
                        ',$B,' + str(speed) + ',$,'
            cmd_hex = binascii.b2a_hex(cmd_ascii) + '0a'
            cmd = cmd_hex.decode('hex')
            self.port.write(cmd)
            return cmd
        else:
            return "Error0."
        # Error0:Serial Port is Close

    # Set Read Data
    def read_data(self):
        if self.port.isOpen():
            raw_data = self.port.readline()
            return raw_data
        else:
            return "Error0."
