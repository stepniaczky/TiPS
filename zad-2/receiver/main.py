import serial
from time import time, sleep

#odbiornik
#
# SOH = 0x1
# EOT = 0x4
# ACK = 0x6
# NAK = 0x15
# CAN = 0x18
# C = 0x43

def handshake_receiver(serialPort1, s):
    # send = 1
    start = time()
    while s:
        mins, secs = divmod(s, 60)
        # timer = '{:02d}:{:02d}'.format(mins, secs)
        # print(timer, end="\r")
        # print(secs)
        if secs % 10 == 0:
            serialPort1.write(b'0x15')
            # print(send)
            # send += 1

        # if time() - start % 10 == 0:
        # if time() - start == 60:

        if serialPort1.read():
            return True
        sleep(1)
        s -= 1
    return False

def main():
    serialPort1 = serial.Serial(
        port="COM2", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )   #odbiornik

    serialPort2 = serial.Serial(
        port="COM3", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )   #nadajnik
    connection = handshake_receiver(serialPort1, 60)
    if connection:
        print("Nawiązano połaczenie i rozpoczęto przesył")
    else:
        print("Nie nawiązano połączenia")


main()