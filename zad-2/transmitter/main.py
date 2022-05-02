from os.path import getsize
import serial
from time import time, sleep

# nadajnik

SOH = b'0x1'
EOT = b'0x4'
ACK = b'0x6'
NAK = b'0x15'
CAN = b'0x18'
CRC = b'0x43'


serialPort1 = serial.Serial(
        port="COM1", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )  # odbiornik


def handshake_transmitter(transmitter, s):
    while s:
        # mins, secs = divmod(s, 60)
        answer = transmitter.read(4)
        print(answer)
        if answer == NAK:
            return 1
        elif answer == CRC:
            return 2
        sleep(1)
        s -= 1
    return -1


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
                    block.append(0x40)
                    if len(block) == 128:
                        filled = True
            data.append(block)
    return data


def add_properties(block, index, crc):
    if crc:
        checksum = crc_sum(block).to_bytes(2, byteorder='big')
    else:
        checksum = algebraic_sum(block).to_bytes(1, byteorder='big')
    prepared = bytearray(SOH)
    prepared.append(index)
    prepared.append(255 - index)
    prepared.extend(block)
    prepared.extend(checksum)
    return prepared


def send_package(transmitter, package, index):
    answer = b''
    while answer != ACK:
        # transmitter.open()
        transmitter.write(package)
        answer = transmitter.read(4)
<<<<<<< HEAD
        print(str(serialPort1.read()) + "ddd")
=======
        print("sending")
>>>>>>> 8e67110ec6da87fb8e0f84d11c52dd100e6fec3d
        if answer == NAK:  # NAK b'0x15'
            print("Send failed - package index: " + index)
        elif answer == CAN:
            # transmitter.close()
            return


def close_connection(transmitter):
    answer = transmitter.read(4)
    while answer != ACK:
        transmitter.write(EOT)
        answer = transmitter.read(4)
        if answer == CAN:
            # transmitter.close()
            return
    # transmitter.close()


def algebraic_sum(block):
    s = 0
    for byte in block:
        s += byte
    return s % 256


def crc_sum(block):
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


    transmitter = serial.Serial(
        port="COM2", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )

    # type = handshake_transmitter(transmitter, 60)
    is_crc = False
    # if type == 1:
    #     print("Connection established")
    # elif type == 2:
    #     print("Connection established - CRC type")
    #     is_crc = True
    # else:
    #     print("Connection failed!")
    #     transmitter.close()
    #     return

    data = divide_into_blocks()
    for index, block in enumerate(data, 1):
        index = index % 256
        package = add_properties(block, index, is_crc)
        # print(package)
        send_package(transmitter, package, index)


    close_connection(transmitter)
    # transmitter.close()
    # for x in package:
    #     print(x)
    # for el in data:
    #     transmitter.write(el)
    # print(serialPort1.read_all())
    # for x in data:
    #     print(x)
    # for x in data:
    #     print(len(x))


if __name__ == "__main__":
    main()
