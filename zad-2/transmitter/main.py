from os.path import getsize
import serial
from time import time, sleep


# nadajnik

SOH = b'0x1'
EOT = b'0x4'
ACK = b'0x6'
NAK = b'0x15'
CAN = b'0x18'
C = b'0x43'


def handshake_transmitter(serialPort2, s):
    while s:
        mins, secs = divmod(s, 60)
        ifNAK = serialPort2.readline()
        print(serialPort2.readline())
        if ifNAK == NAK:
            return True

        # print(ifNAK)
        sleep(1)
        s -= 1
    return False


def divide_into_blocks():
    data = []
    with open("message.txt", 'rb') as file:
        size = getsize("message.txt")
        blocks_numbers = size // 128 \
            if size % 128 == 0 \
            else (size // 128) + 1

        for block_number in range(blocks_numbers):
            filled = False
            block = bytearray(file.read(128))
            if len(block) < 128:
                while not filled:
                    block.append(0x20)
                    if len(block) == 128:
                        filled = True
            data.append(block)
    return data


def add_properties(blocks):
    index = 0
    while index < len(blocks):
        soh = bytes(0x1)
        blocks[index] += soh
        number = bytes(index + 1)
        blocks[index] += number
        index += 1
    # for bl in blocks:
    #     print(bl)
    #     print("\n")


def send_blocks(serialPort2, blocks, start_with):
    el = start_with
    # print(len(blocks))
    while el < len(blocks):
        serialPort2.write(blocks[el])
        print(el)
        if serialPort2.read(1) == ACK:  # ACK
            el += 1
        elif serialPort2.read(1) == NAK:  # NAK b'0x15'
            send_blocks(serialPort2, blocks, el)

    # print(serialPort1.read_all())
    while serialPort2.readline() != ACK:
        serialPort2.write(EOT)  # EOT
        print("supa")


def main():
    # serialPort1 = serial.Serial(
    #     port="COM1", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    # )  # odbiornik

    serialPort2 = serial.Serial(
        port="COM3", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )  # nadajnik

    connetction = handshake_transmitter(serialPort2, 60)
    if connetction:
        print("nawiazano polaczenie rozpoczeto przesyl danych")
    else:
        print("nie nawiazano polaczenia")

    data = divide_into_blocks()
    # for x in data:
    #     print(x)
    # for x in data:
    #     print(len(x))

    add_properties(data)
    # for x in data:
    #     print(x)
    send_blocks(serialPort2, data, 0)
    # for el in data:
    #     serialPort2.write(el)
    # print(serialPort1.read_all())


if __name__ == "__main__":
    main()
