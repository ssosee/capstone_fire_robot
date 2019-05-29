# coding: utf-8
import sys
import threading
import keyboard
import time

from socket import *

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QBoxLayout

from PyQt5.QtWidgets import (QApplication, QCheckBox, QFileDialog,  QGridLayout,QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpinBox, QStyle,QToolButton, QVBoxLayout, QWidget)
from PyQt5.QtCore import Qt

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
#flag 변수 선언
pump_flag = 0
pump_flag_80 = 0
pump_flag_60 = 0
pump_flag_50 = 0
pump_flag_off = 0
Forward_flag = 0
Backward_flag = 0
Right_flag = 0
Left_flag = 0
Spin_Left_flag = 0
Spin_Right_flag = 0
Fast_flag = 0
Slow_flag = 0
Servo_up_flag = 0
Servo_down_flag = 0
Servo_left_flag = 0
Servo_right_flag = 0
Servo_center_flag = 0
Stop_flag = 1
Stop_key = 0
mode = 2
sendData = 'nope'
def send(sock):
    global pump_flag
    global pump_flag_80
    global pump_flag_60
    global pump_flag_50
    global pump_flag_off
    global Forward_flag
    global Backward_flag
    global Right_flag
    global Left_flag
    global Spin_Left_flag
    global Spin_Right_flag
    global Fast_flag
    global Slow_flag
    global Servo_up_flag
    global Servo_down_flag
    global Servo_left_flag
    global Servo_right_flag
    global Servo_center_flag
    global Stop_flag
    global Stop_key
    global sendData
    global mode
    while True:
        if mode  == 0:
            if keyboard.is_pressed('w'):
                sendData = 'w'
                Forward_flag = 0
                if keyboard.is_pressed('.'):
                    sendData = '.'
                elif keyboard.is_pressed(','):
                    sendData = ','
            elif keyboard.is_pressed('s'):
                sendData = 's'
                if keyboard.is_pressed('.'):
                    sendData = '.'
                elif keyboard.is_pressed(','):
                    sendData = ','
                Backward_flag = 0
            elif keyboard.is_pressed('a'):
                sendData = 'a'
                if keyboard.is_pressed('.'):
                    sendData = '.'
                elif keyboard.is_pressed(','):
                    sendData = ','
                Left_flag = 0
            elif keyboard.is_pressed('d'):
                sendData = 'd'
                if keyboard.is_pressed('.'):
                    sendData = '.'
                elif keyboard.is_pressed(','):
                    sendData = ','
                Right_flag = 0
            elif keyboard.is_pressed('q'):
                sendData = 'q'
                if keyboard.is_pressed('.'):
                    sendData = '.'
                elif keyboard.is_pressed(','):
                    sendData = ','
                Spin_Left_flag = 0
            elif keyboard.is_pressed('e'):
                sendData = 'e'
                if keyboard.is_pressed('.'):
                    sendData = '.'
                elif keyboard.is_pressed(','):
                    sendData = ','
                Spin_Right_flag = 0
            elif keyboard.is_pressed(80): #80 down
                sendData = '}'
                Servo_down_flag = 0
            elif keyboard.is_pressed(75): #75 left
                sendData = '['
                Servo_left_flag = 0
            elif keyboard.is_pressed('1'):
                sendData = '1'
                pump_flag = 0
            elif keyboard.is_pressed('2'):
                sendData = '2'
                pump_flag_80 = 0
            elif keyboard.is_pressed('3'):
                sendData = '3'
                pump_flag_60 = 0
            elif keyboard.is_pressed('4'):
                sendData = '4'
                pump_flag_50 = 0
            elif keyboard.is_pressed('5'):
                sendData = 'p'
                pump_flag_off = 0
            elif keyboard.is_pressed('r'):
                sendData = '.'
                Fast_flag = 0
                print(Fast_flag)
            elif keyboard.is_pressed('f'):
                sendData = ','
                Slow_flag = 0
                print(Slow_flag)
            elif keyboard.is_pressed(72): #72 up
                sendData = '{'
                Servo_up_flag = 0
                print(Servo_up_flag)
            elif keyboard.is_pressed(77): #77 right
                sendData = ']'
                Servo_right_flag = 0
                print(Servo_right_flag)
            elif keyboard.is_pressed('c'): #77 center
                sendData = 'c'
                Servo_center_flag = 0
                print(Servo_center_flag)
                print("Stop_key",Stop_key)
                print("Stop_flag",Stop_flag)
            else:
                sendData = '/'

        elif mode == 1:
            if Forward_flag == 1:
                sendData = 'w'
                Forward_flag = 0
                if keyboard.is_pressed('.'):
                    sendData = '.'
                elif keyboard.is_pressed(','):
                    sendData = ','
                Stop_flag = 0

            elif Backward_flag == 1:
                sendData = 's'
                if keyboard.is_pressed('.'):
                    sendData = '.'
                elif keyboard.is_pressed(','):
                    sendData = ','
                Backward_flag = 0
                Stop_flag = 0

            elif Left_flag == 1:
                sendData = 'a'
                if keyboard.is_pressed('.'):
                    sendData = '.'
                elif keyboard.is_pressed(','):
                    sendData = ','
                Left_flag = 0
                Stop_flag = 0

            elif Right_flag == 1:
                sendData = 'd'
                if keyboard.is_pressed('.'):
                    sendData = '.'
                elif keyboard.is_pressed(','):
                    sendData = ','
                Right_flag = 0
                Stop_flag = 0

            elif Spin_Left_flag == 1:
                sendData = 'q'
                if keyboard.is_pressed('.'):
                    sendData = '.'
                elif keyboard.is_pressed(','):
                    sendData = ','
                Spin_Left_flag = 0
                Stop_flag = 0

            elif Spin_Right_flag == 1:
                sendData = 'e'
                if keyboard.is_pressed('.'):
                    sendData = '.'
                elif keyboard.is_pressed(','):
                    sendData = ','
                Spin_Right_flag = 0
                Stop_flag = 0

            elif pump_flag == 1:
                sendData = '1'
                Stop_flag = 0
                pump_flag = 0

            elif pump_flag_80 == 1:
                sendData = '2'
                Stop_flag = 0
                pump_flag_80 = 0

            elif pump_flag_60 == 1:
                sendData = '3'
                Stop_flag = 0
                pump_flag_60 = 0

            elif pump_flag_50 == 1:
                sendData = '4'
                Stop_flag = 0
                pump_flag_50 = 0

            elif pump_flag_off == 1:
                sendData = 'p'
                Stop_flag = 0
                pump_flag_off = 0

            elif Fast_flag == 1:
                sendData = '.'
                Stop_flag = 0
                Fast_flag = 0
                print(Fast_flag)

            elif Slow_flag == 1:
                sendData = ','
                Stop_flag = 0
                Slow_flag = 0
                print(Slow_flag)

            elif Servo_up_flag == 1: #72 up
                sendData = '{'
                Stop_flag = 0
                Servo_up_flag = 0
                print(Servo_up_flag)

            elif Servo_down_flag == 1: #80 down
                sendData = '}'
                Stop_flag = 0
                Servo_down_flag = 0
                print(Servo_down_flag)

            elif Servo_left_flag == 1: #75 left
                sendData = '['
                Stop_flag = 0
                Servo_left_flag = 0
                print(Servo_left_flag)

            elif Servo_right_flag == 1: #77 right
                sendData = ']'
                Stop_flag = 0
                Servo_right_flag = 0
                print(Servo_right_flag)

            elif Servo_center_flag == 1: #77 center
                sendData = 'c'
                Servo_center_flag = 0
                Stop_flag = 0
                print(Servo_center_flag)
                print("Stop_key",Stop_key)
                print("Stop_flag",Stop_flag)

            elif Stop_flag == 1:
                sendData = '/'
        '''elif Stop_flag == 0:
            sendData = '/'
        '''
        '''else:
            sendData = '/'
        '''
        '''elif keyboard.is_pressed(chr(32)):
            sendData = '/'
        '''
        time.sleep(0.01)
        # sendData = input()
        sock.send(sendData.encode('utf-8'))

class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, flags=Qt.Widget)
        self.ui = uic.loadUi("test6.ui", self)
        self.ui.show()

        self.form_layout = QBoxLayout(QBoxLayout.TopToBottom, self)
        self.setLayout(self.form_layout)
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("불이야!")
        # QWebEngineView 를 이용하여 웹 페이지를 표출
        web = QWebEngineView()
        web.setUrl(QUrl("http://192.168.137.252:8080/Picam.html"))
        #self.form_layout.addWidget(web)
        self.resize(1218, 704)
        self.form_layout.addWidget(web, alignment=Qt.AlignTop)
        self.form_layout.setContentsMargins(209, 10, 209, 0)
        web.setFixedWidth(800)
        web.setFixedHeight(450)
    # @pyqtSlot()

    def Keyboard_mode(self):
        global mode
        mode = 0

    def Button_mode(self):
        global mode
        mode = 1

    def connect_event(self):
        port = 8070

        clientSock = socket(AF_INET, SOCK_STREAM)
        clientSock.connect(('192.168.137.252', port))

        print('Connected!')
        #self.ui.label.setText("연결된거임 ㅋ\n 아무튼 그런거임")
        sender = threading.Thread(target=send, args=(clientSock,))

        sender.start()

    def Stop_event(self):
        global Stop_flag
        print("Stop")
        print(Stop_flag)
        Stop_flag = 1
        #Stop_key = 1
        print(Stop_flag)

    def pump_on_event(self):
        global pump_flag
        print(pump_flag)
        print("pump on! power 100")
        pump_flag = 1
        Stop_flag = 0
        print(pump_flag)

    def Pump_on_80_event(self):
        global pump_flag_80
        print("pump power 80")
        pump_flag_80 = 1
        Stop_flag = 0

    def Pump_on_60_event(self):
        global pump_flag_60
        print("pump power 60")
        pump_flag_60 = 1
        Stop_flag = 0

    def Pump_on_50_event(self):
        global pump_flag_50
        print("pump power 50")
        pump_flag_50 = 1
        Stop_flag = 0

    def Pump_off_event(self):
        global pump_flag_off
        print("pump off")
        pump_flag_off = 1
        Stop_flag = 0

    def Forward_event(self):
        global Forward_flag
        print("Forward")
        Forward_flag = 1
        Stop_flag = 0
        print(Stop_flag)

    def Backward_event(self):
        global Backward_flag
        print("Backward")
        Backward_flag = 1
        Stop_flag = 0

    def Right_event(self):
        global Right_flag
        print("Right")
        Right_flag = 1
        Stop_flag = 0

    def Left_event(self):
        global Left_flag
        print("Left")
        Left_flag = 1
        Stop_flag = 0

    def Spin_Left(self):
        global Spin_Left_flag
        print("Spin Left")
        Spin_Left_flag = 1
        Stop_flag = 0

    def Spin_Right(self):
        global Spin_Right_flag
        print("Spin Left")
        Spin_Right_flag = 1
        Stop_flag = 0

    def Fast_event(self):
        global Fast_flag
        print("Fast")
        Fast_flag = 1
        Stop_flag = 0

    def Slow_event(self):
        global Slow_flag
        print("Slow")
        Slow_flag = 1
        Stop_flag = 0

    def Servo_up_event(self):
        global Servo_up_flag
        print("servo up")
        Servo_up_flag = 1
        Stop_flag = 0

    def Servo_down_event(self):
        global Servo_down_flag
        print("servo down")
        Servo_down_flag = 1
        Stop_flag = 0

    def Servo_left_event(self):
        global Servo_left_flag
        print("servo left")
        Servo_left_flag = 1
        Stop_flag = 0

    def Servo_right_event(self):
        global Servo_right_flag
        print("servo right")
        Servo_right_flag = 1
        Stop_flag = 0

    def Servo_center(self):
        global Servo_center_flag
        print("servo center")
        Servo_center_flag = 1
        Stop_flag = 0

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
