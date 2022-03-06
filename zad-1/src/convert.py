H = [[1, 0, 1, 0, 0, 1, 0, 1,      1, 0, 0, 0, 0, 0, 0, 0],    # 165 / 128
     [0, 1, 1, 1, 0, 1, 1, 1,      0, 1, 0, 0, 0, 0, 0, 0],    # 119 / 64
     [0, 0, 0, 1, 1, 1, 1, 0,      0, 0, 1, 0, 0, 0, 0, 0],    # 30 / 32
     [1, 0, 0, 0, 1, 1, 1, 1,      0, 0, 0, 1, 0, 0, 0, 0],    # 143 / 16
     [1, 1, 1, 0, 0, 0, 1, 0,      0, 0, 0, 0, 1, 0, 0, 0],    # 226 / 8
     [1, 1, 1, 1, 0, 0, 0, 1,      0, 0, 0, 0, 0, 1, 0, 0],    # 241 / 4
     [1, 1, 0, 1, 1, 1, 0, 1,      0, 0, 0, 0, 0, 0, 1, 0],    # 221 / 2
     [0, 1, 0, 0, 1, 0, 1, 1,      0, 0, 0, 0, 0, 0, 0, 1]]    # 75 / 1

BYTE = 8

def code(message):
    string = ""
    letter_bin = []
    control_bits = []
    for row in message:
        for sign in row:
            letter = ord(sign)  # przekonwertowanie znaku na kod ASCII

            for i in range(BYTE):
                letter_bin.append(letter % 2)  # zamiana kodu ASCII na kod binarny
                letter = int(letter / 2)
                control_bits.append(0)  # wypelnienie tablicy bitow kontrolnych zerami

            for i in range(BYTE):
                for j in range(BYTE):
                    control_bits[i] += letter_bin[j] * H[i][j]  # obliczenie kolejnych bitow kontrolnych
                control_bits[i] %= 2

            for i in range(BYTE):
                string += str(letter_bin[i])
            for i in range(BYTE):
                string += str(control_bits[i])
            string += "\n"

            letter_bin.clear()
            control_bits.clear()
    return string


def decode(encoded_message):
    return 0