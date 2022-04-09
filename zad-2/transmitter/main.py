import serial
from time import time, sleep


# nadajnik
#
# SOH = 0x1
# EOT = 0x4
# ACK = 0x6
# NAK = 0x15
# CAN = 0x18
# C = 0x43

def handshake_transmitter(serialPort2, s):
    while s:
        mins, secs = divmod(s, 60)
        # timer = '{:02d}:{:02d}'.format(mins, secs)
        # print(timer, end="\r")
        ifNAK = serialPort2.read()
        if ifNAK == b'0x15':
            return True
        sleep(1)
        s -= 1
    return False


def divide_into_blocks(content):
    data = []
    content_b = bytes(content, 'ascii')
    # data.append(content_b[:128])
    # data.append(content_b[128:256])
    # data.append(content_b[256:384])
    index = 0
    byte = 128
    all_filled = False
    while not all_filled:
        if byte == 128:
            data.append(content_b[:byte])
        if byte > 128:
            data.append(data.append(content_b[byte - 128:byte]))

        if len(data[index]) < 128:  #DLACZEGO TU SIE WYPIERDALA
            missing_bytes = 128 - len(data[index])
            data_extended = []

            for i in missing_bytes:
                data_extended.append(" ")

            data.extend(data_extended)
            all_filled = True
        index += 1
        byte += 128
    return data


def main():
    serialPort1 = serial.Serial(
        port="COM2", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )  # odbiornik

    serialPort2 = serial.Serial(
        port="COM3", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )  # nadajnik

    # connetction = handshake_transmitter(serialPort2, 60)
    # if connetction:
    #     print("nawiazano polaczenie rozpoczeto przesyl danych")
    # else:
    #     print("nie nawiazano polaczenia")

    with open("message.txt") as file:
        content = file.readline()
    file.close()

    data = []
    data = divide_into_blocks(content)
    for x in data:
        print(x)


main()
