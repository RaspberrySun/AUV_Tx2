# -*- coding: utf-8 -*-
"""
Author: Bo Sun,https://github.com/RaspberrySun/AUV_Tx2
"""
from serial_com import SerialPort
from auv_ui import ui_auv
import csv
import threading
import cv2
from datetime import datetime
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow

# Create AUV Serial Item
Device = "/tty/THS1"
BaudRate = 19200
auv_serial = SerialPort(Device, BaudRate)


# Set AUV_WS Class SignalSlots
class AUV_WS(QMainWindow, ui_auv):
    def __init__(self, parent=None):
        super(AUV_WS, self).__init__(parent)
        self.setupUi(self)
        self.CreateSignalSlot()

    def CreateSignalSlot(self):
        self.pushButton0.clicked.connect(self.open_pushbtn0)
        self.pushButton1.clicked.connect(self.open_pushbtn1)
        self.pushButton2.clicked.connect(self.open_pushbtn2)
        self.pushButton3.clicked.connect(self.open_pushbtn3)

        self.radioButton.clicked.connect(self.open_radiobtn)
        self.radioButton1.clicked.connect(self.open_radiobtn1)

    def open_pushbtn0(self):
        if not self.pushButton0.isChecked():
            self.pushButton0.setChecked(True)
            self.pushButton0.setText("数据接收")

    def open_pushbtn1(self):
            self.pushButton1.setChecked(True)

    def open_pushbtn2(self):
            self.pushButton2.setChecked(True)

    def open_pushbtn3(self):
        self.pushButton3.setChecked(True)
        self.pushButton0.setChecked(False)
        self.pushButton0.setText("关闭")
        self.stop_all()

    def open_radiobtn(self):
        self.radioButton.setChecked(True)
        self.lineEdit_7.setEnabled(True)
        self.lineEdit_8.setEnabled(True)
        self.lineEdit_9.setEnabled(True)
        self.pushButton1.setChecked(True)

        self.lineEdit_10.setEnabled(False)
        self.lineEdit_11.setEnabled(False)
        self.lineEdit_12.setEnabled(False)
        self.pushButton2.setEnabled(False)

    def open_radiobtn1(self):
        self.radioButton1.setChecked(True)
        self.lineEdit_10.setEnabled(True)
        self.lineEdit_11.setEnabled(True)
        self.lineEdit_12.setEnabled(True)
        self.pushButton2.setEnabled(True)

        self.lineEdit_7.setEnabled(False)
        self.lineEdit_8.setEnabled(False)
        self.lineEdit_9.setEnabled(False)
        self.pushButton1.setEnabled(False)

    def data_read(self):
        try:
            while 1:
                sensor_data_raw = auv_serial.read_data()
                sensor_data = sensor_data_raw.split(',')
                longitude = sensor_data[10][:5]
                latitude = sensor_data[13][:5]
                roll = str(-float(sensor_data[16]))[:5]
                pitch = sensor_data[18][:5]
                yaw = str(-float(sensor_data[20]))[:5]
                depth = sensor_data[22][:5]
                self.lineEdit.setText(longitude)
                self.lineEdit_2.setText(latitude)
                self.lineEdit_3.setText(depth)
                self.lineEdit_4.setText(pitch)
                self.lineEdit_5.setText(roll)
                self.lineEdit_6.setText(yaw)
                time.sleep(0.2)
        except self.pushButton3.isChecked():
            pass

    def manual_control(self):
        angle_ver = self.lineEdit_10.text()
        angle_hor = self.lineEdit_11.text()
        motor_speed = self.lineEdit_12.text()
        auv_serial.send_data(angle_ver, -angle_ver, angle_hor, -angle_hor, motor_speed)

    def stop_all(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.lineEdit_9.clear()
        self.lineEdit_10.clear()
        self.lineEdit_11.clear()
        self.lineEdit_12.clear()
        auv_serial.send_data(45, 45, 45, 45, 10.0)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    auv_ws = AUV_WS()
    auv_ws.show()
    sys.exit(app.exec_())
