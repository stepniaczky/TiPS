import serial
from time import time, sleep


# odbiornik
#
# SOH = 0x1
# EOT = 0x4
# ACK = 0x6
# NAK = 0x15
# CAN = 0x18
# C = 0x43


def handshake_receiver(serialPort1, s):
    while s:
        mins, secs = divmod(s, 60)
        if secs % 10 == 0:
            serialPort1.write(b'0x15')
        if serialPort1.read():
            return True
        print(serialPort1.readline())
        sleep(1)
        s -= 1
    return False


def receive_blocks(serialPort1):
    received = []
    all_sent = False
    print("check - receive blocks")
    while not all_sent:
        received.append(serialPort1.readline())
        print(serialPort1.readline())
        serialPort1.write(b'0x6')
        if serialPort1.read_all() == b'':
            all_sent = True
    if serialPort1.readline() == b'0x4':
        serialPort1.write(b'0x6')
    return received


def main():
    serialPort1 = serial.Serial(
        port="COM1", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )  # odbiornik

    # serialPort2 = serial.Serial(
    #     port="COM2", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    # )   #nadajnik
    connection = handshake_receiver(serialPort1, 60)
    if connection:
        print("Nawiązano połaczenie i rozpoczęto przesył")
    else:
        print("Nie nawiązano połączenia")
    received = receive_blocks(serialPort1)
    for x in received:
        print(x)


if __name__ == "__main__":
    main()
