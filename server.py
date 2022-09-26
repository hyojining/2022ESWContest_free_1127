# Server (ATM)

import socket
import time
import RPi.GPIO as GPIO
from threading import Thread

HOST = '192.168.137.125' 
PORT = 12345 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket create

#managing error exception
try:
    s.bind((HOST, PORT))
except socket.error:
    print('Bind failed')

s.listen(1)
(conn, addr) = s.accept() # accept connections from client
print('Connected')

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER=23
GPIO_ECHO=24
GPIO_BUZZER=18

GPIO.setup(GPIO_BUZZER,GPIO.OUT)
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

GPIO.output(GPIO_TRIGGER,False)

def measure():
    GPIO.output(GPIO_TRIGGER,True)
	time.sleep(0.00001) # Delay for 10us pulse generation
    GPIO.output(GPIO_TRIGGER,False)
    start = time.time()

    while GPIO.input(GPIO_ECHO)==0: # Echo Pin High
        start = time.time()

    while GPIO.input(GPIO_ECHO)==1: # Echo Pin Low
        stop = time.time()

    elapsed = stop-start
    distance = (elapsed * 34300)/2 # v=34300cm/s

    return distance

def atm():
    while True:
        distance=measure()
        time.sleep(0.5)

        if distance <= 17:
        	print("ATM User Detect")
			atm_data='ATM User Detect'
			time.sleep(0.5)

        else:
        	print("ATM User Not Detect")
			atm_data='ATM User Not Detect'
			time.sleep(0.5)
		
		conn.send(atm_data) # send ATM data (to client)

    return

def buzzer():
    while True:
        line_data=conn.recv(1024) # recieve Line data (from client)

        if line_data == 'Line Motion Detect':
            print('Buzzer On')
            pwm=GPIO.PWM(GPIO_BUZZER, 1.0)
            pwm.start(50.0)
            pwm.ChangeFrequency(330)
            time.sleep(0.3)
            pwm.stop()
            
        else:
            print('Buzzer Off')
            GPIO.output(GPIO_BUZZER, GPIO.LOW)
            time.sleep(0.1)

if __name__ == "__main__":
	th1 = Thread(target=atm, args=())
    th1.start() # start Ultrasonic Sensor thread

    th3 = Thread(target=buzzer, args=())
    th3.start() # start buzzer thread