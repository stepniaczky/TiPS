import serial
from time import time, sleep


# odbiornik

SOH = b'0x1'
EOT = b'0x4'
ACK = b'0x6'
NAK = b'0x15'
CAN = b'0x18'
C = b'0x43'


def handshake_receiver(serialPort1, s):
    while s:
        mins, secs = divmod(s, 60)
        if secs % 10 == 0:
            serialPort1.write(NAK)
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
        received_block = serialPort1.readline()
        print(received_block)
        received_check_sum = int.from_bytes(received_block[-1:],byteorder='big')
        # int.from_bytes(received_block[-2:], byteorder="big")
        if received_check_sum != algebraic_sum(received_block):
            serialPort1.write(NAK)
        else:
            serialPort1.write(ACK)
            received.append(serialPort1.readline())
        if serialPort1.read_all() == b'':
            all_sent = True
    if serialPort1.readline(1) == EOT:
        serialPort1.write(ACK)
    return received


def algebraic_sum(block):
    s = 0
    for byte in block:
        s += byte
    return s % 256


def crc(block):
    poly = 0x1021
    crc = 0xFFFF
    for i in range(len(block)):
        crc ^= block[i] << 8
        for j in range(8):
            if (crc & 0x8000) > 0:
                crc = (crc << 1) ^ poly
            else:
                crc = crc << 1
    return crc & 0xFFFF


def main():
    serialPort1 = serial.Serial(
        port="COM2", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
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
    # for x in received:
    #     print(x)
    with open("output.txt", "w") as txt_file:
        for line in received:
            txt_file.write(" ".join(line) + "\n")

if __name__ == "__main__":
    main()
