import serial
from time import time, sleep

# odbiornik

SOH = b'0x1'
EOT = b'0x4'
ACK = b'0x6'
NAK = b'0x15'
CAN = b'0x18'
CRC = b'0x43'  # C


def handshake_receiver(receiver, s, is_crc):
    answer = b''
    while s:
        mins, secs = divmod(s, 60)
        answer = receiver.read(4)
        if is_crc:
            if secs % 10 == 0:
                receiver.write(CRC)
                print("CRC")
        else:
            if secs % 10 == 0:
                receiver.write(NAK)
                print("NAK")
        if answer == SOH:
            return True
        elif answer != b'':
            return True
        print(receiver.read())
        sleep(1)
        s -= 1
    return False


def receive_blocks(receiver, package_size, index, is_crc):
    received = bytearray()
    answer = b''
    while answer != EOT:
        is_okay = True
        received_package = receiver.read(package_size - 1)
        # received_package = receiver.readline(package_size - 1)
        if is_crc:
            checksum_bytes = received_package[-2:]
            received_checksum = int.from_bytes(checksum_bytes, byteorder='big')
        else:
            checksum_bytes = received_package[-1:]
            received_checksum = int.from_bytes(checksum_bytes, byteorder='big')
        received_index = received_package[0]
        received_supplement = received_package[1]
<<<<<<< HEAD
        received_block = received_package[2: 130]
=======
        # print(received_block)
        # print(received_index)
        # print(received_supplement)
        # print(received_package)
>>>>>>> 8e67110ec6da87fb8e0f84d11c52dd100e6fec3d
        if index != received_index or received_supplement != 255 - received_index:
            receiver.write(CAN)
            is_okay = False
            return
        if is_crc:
            checksum = crc(received_block)
        else:
            checksum = algebraic_sum(received_block)
        if checksum != received_checksum:
            receiver.write(NAK)
            is_okay = False
        if is_okay:
            received.extend(received_block)
            receiver.write(ACK)
            answer = receiver.read(3)
            if answer != b'':
                print("ok")
    receiver.write(ACK)
    print(received)
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


def choice():
    print("Use CRC?")
    try:
        answer = input("Y/N --- ")
        if answer in ["yes", "Y", "y", "tak", "Yes", "Tak", "YES", "TAK"]:
            return True
        elif answer in ["no", "N", "n", "nie", "No", "Nie", "NO", "NIE"]:
            return False
        print("Invalid input!")
        return choice()
    except ValueError:
        print("An invalid value has been entered!")


def main():
    receiver = serial.Serial(
        port="COM1", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )  # odbiornik
    # receiver.open()
    is_crc = choice()
    if is_crc:
        package_size = 133
    else:
        package_size = 132
    index = 1
    data = bytearray()
    connection = handshake_receiver(receiver, 60, is_crc)
    if connection:
        print("Connection established")
        le = 5
        # for i in range(le):
        data = receive_blocks(receiver, package_size, index, is_crc)
        print(data)
        # with open("output.txt", "wb") as txt_file:
        #     for line in data:
        #         txt_file.write(line)
    else:
        print("Connection failed!")

    # data = receive_blocks(receiver, package_size, index, is_crc)

    # receiver.close()
    # for x in received:
    #     print(x)
    # with open("output.txt", "w") as txt_file:
    #     for line in received:
    #         txt_file.write(" ".join(line) + "\n")


if __name__ == "__main__":
    main()
