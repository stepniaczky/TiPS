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
    string = ''
    for line in content:
        string += line

    content_b = bytes(string, 'ascii')
    # data.append(content_b[:128])
    # data.append(content_b[128:256])
    # data.append(content_b[256:384])
    index = 0
    byte = 128
    all_filled = False
    while not all_filled:
        if byte == 128:
            data.append(content_b[:byte])
        elif byte > 128:
            data.append(content_b[byte - 128:byte])

        if len(data[index]) == 0:
            all_filled = True

        if len(data[index]) < 128:  #DLACZEGO TU SIE WYPIERDALA

            missing_bytes = 128 - len(data[index])
            data_extended = b''
            for i in range(missing_bytes):
                data_extended += b' '

            data[index] += data_extended
            all_filled = True


        # print(data[index])
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
        content = file.readlines()

    data = divide_into_blocks(content)
    for x in data:
        print(x)
    #
    # for x in data:
    #     print(len(x))


if __name__ == "__main__":
    main()
