# Client (Line)

import socket
import RPi.GPIO as GPIO
import time
from threading import Thread

HOST = '192.168.137.125'  
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket create
s.connect((HOST,PORT)) # connect socket

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.OUT) #LED
GPIO.setup(3, GPIO.IN) #SENSOR

def line():
    while True:
        sensor_state=GPIO.input(3) 
        atm_data=s.recv(1024) # recieve ATM data (from server)

        if atm_data=='ATM User Detect': 

            if sensor_state==0:
                GPIO.output(2,True) 
                print('Line Motion Detect')
                line_data = 'Line Motion Detect'
                time.sleep(0.5)

            else:
                GPIO.output(2,False)
                print('Line Motion Not Detect')
                line_data = 'Line Motion Not Detect'
                time.sleep(0.5)

            s.send(line_data) # send Line data (to server)

        else:
            continue

    return

if __name__ == "__main__":
    
    th2 = Thread(target=line, args=())
    th2.start() # start PIR Sensor thread