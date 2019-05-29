import RPi.GPIO as GPIO
from socket import *
import threading
#import keyboard
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Right DC Motor
GPIO_DC1_IN1 = 20 #IN1
GPIO_DC1_IN2 = 21 #IN2
GPIO_DC1_PWM = 16 #PWM
#Left DC Motor
GPIO_DC2_IN1 = 19 #IN1
GPIO_DC2_IN2 = 26 #IN2
GPIO_DC2_PWM = 13 #PWM
#Pump Motor
GPIO_PUMP_ON = 3
GPIO_PUMP_PWM = 2

key = '0'
speed_mode = 0
move_mode = 0
duty_ratio = [25, 50, 75, 100]


def DC_Init():
    global PWM1
    global PWM2
    global PWM_PUMP

    #Right DC Motor Setup
    GPIO.setup(GPIO_DC1_IN1, GPIO.OUT)
    GPIO.setup(GPIO_DC1_IN2, GPIO.OUT)
    GPIO.setup(GPIO_DC1_PWM, GPIO.OUT)
    #Left DC Motor Setup
    GPIO.setup(GPIO_DC2_IN1, GPIO.OUT)
    GPIO.setup(GPIO_DC2_IN2, GPIO.OUT)
    GPIO.setup(GPIO_DC2_PWM, GPIO.OUT)
    #Pump Motor Setup
    GPIO.setup(GPIO_PUMP_ON, GPIO.OUT)
    GPIO.setup(GPIO_PUMP_PWM, GPIO.OUT)

    #Setup PWM
    PWM1 = GPIO.PWM(GPIO_DC1_PWM, 2000)
    PWM2 = GPIO.PWM(GPIO_DC2_PWM, 2000)
    PWM_PUMP = GPIO.PWM(GPIO_PUMP_PWM, 2000)

    #PWM Start!
    PWM1.start(0)
    PWM2.start(0)
    PWM_PUMP.start(0)

def DC_Forward():
    GPIO.output(GPIO_DC1_IN1, True)
    GPIO.output(GPIO_DC1_IN2, False)
    PWM1.ChangeDutyCycle(duty_ratio[speed_mode])

    GPIO.output(GPIO_DC2_IN1, True)
    GPIO.output(GPIO_DC2_IN2, False)
    PWM2.ChangeDutyCycle(duty_ratio[speed_mode])

def DC_Backward():
    GPIO.output(GPIO_DC1_IN1, False)
    GPIO.output(GPIO_DC1_IN2, True)
    PWM1.ChangeDutyCycle(duty_ratio[speed_mode])

    GPIO.output(GPIO_DC2_IN1, False)
    GPIO.output(GPIO_DC2_IN2, True)
    PWM2.ChangeDutyCycle(duty_ratio[speed_mode])

def DC_Right():
    GPIO.output(GPIO_DC1_IN1, True)
    GPIO.output(GPIO_DC1_IN2, False)
    PWM1.ChangeDutyCycle(duty_ratio[speed_mode]/4)

    GPIO.output(GPIO_DC2_IN1, True)
    GPIO.output(GPIO_DC2_IN2, False)
    PWM2.ChangeDutyCycle(duty_ratio[speed_mode])

def DC_Left():
    GPIO.output(GPIO_DC1_IN1, True)
    GPIO.output(GPIO_DC1_IN2, False)
    PWM1.ChangeDutyCycle(duty_ratio[speed_mode])

    GPIO.output(GPIO_DC2_IN1, True)
    GPIO.output(GPIO_DC2_IN2, False)
    PWM2.ChangeDutyCycle(duty_ratio[speed_mode]/4)

def DC_SpinRight():
    GPIO.output(GPIO_DC1_IN1, False)
    GPIO.output(GPIO_DC1_IN2, True)
    PWM1.ChangeDutyCycle(duty_ratio[speed_mode])

    GPIO.output(GPIO_DC2_IN1, True)
    GPIO.output(GPIO_DC2_IN2, False)
    PWM2.ChangeDutyCycle(duty_ratio[speed_mode])

def DC_SpinLeft():
    GPIO.output(GPIO_DC1_IN1, True)
    GPIO.output(GPIO_DC1_IN2, False)
    PWM1.ChangeDutyCycle(duty_ratio[speed_mode])

    GPIO.output(GPIO_DC2_IN1, False)
    GPIO.output(GPIO_DC2_IN2, True)
    PWM2.ChangeDutyCycle(duty_ratio[speed_mode])

def DC_Brake():
    GPIO.output(GPIO_DC1_IN1, False)
    GPIO.output(GPIO_DC1_IN2, False)

    GPIO.output(GPIO_DC2_IN1, False)
    GPIO.output(GPIO_DC2_IN2, False)

def PUMP_On(duty):
    GPIO.output(GPIO_PUMP_ON, True)
    PWM_PUMP.ChangeDutyCycle(duty)

def PUMP_Off():
    GPIO.output(GPIO_PUMP_ON, False)

def Main_mode():
    global speed_mode
    if key == 'w':
        DC_Forward()
    elif key == 's':
        DC_Backward()
    elif key == 'a':
        DC_Left()
    elif key == 'd':
        DC_Right()
    elif key == 'q':
        DC_SpinLeft()
    elif key == 'e':
        DC_SpinRight()
    elif key == '/':
        DC_Brake()
    elif key == '.':
        speed_mode = speed_mode + 1
        if speed_mode > 3:
            speed_mode = 3
        PWM1.ChangeDutyCycle(duty_ratio[speed_mode])
        PWM2.ChangeDutyCycle(duty_ratio[speed_mode])
    elif key == ',':
        speed_mode = speed_mode - 1
        if speed_mode < 0:
            speed_mode = 0
        PWM1.ChangeDutyCycle(duty_ratio[speed_mode])
        PWM2.ChangeDutyCycle(duty_ratio[speed_mode])
    elif key == '1':
        PUMP_On(100)
    elif key == '2':
        PUMP_On(80)
    elif key == '3':
        PUMP_On(60)
    elif key == '4':
        PUMP_On(50)
    elif key == '5':
        PUMP_Off()

def receive(sock):
    global key
    while True:
        recvData = sock.recv(1024)
        print(recvData.decode('utf-8'))
        key = recvData.decode('utf-8')
        Main_mode()

try:
    DC_Init()
    port = 8070

    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('', port))
    serverSock.listen(1)

    print('Port %d waiting...'%port)

    connectionSock, addr = serverSock.accept()

    print(str(addr), 'connected.')

    receiver = threading.Thread(target=receive, args=(connectionSock,))

    receiver.start()
    while True:
        pass


except KeyboardInterrupt:
    print("\nExit\n")
    PWM1.stop()
    GPIO.cleanup()
    socket.close(self)
    sys.exit()
