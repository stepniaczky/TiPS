H = [[1, 1, 1, 1, 1, 1, 1, 1,      1, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 1, 0, 1, 0, 1, 0,      0, 1, 0, 0, 0, 0, 0, 0],
     [1, 1, 0, 0, 1, 1, 0, 0,      0, 0, 1, 0, 0, 0, 0, 0],
     [1, 1, 1, 1, 0, 0, 0, 0,      0, 0, 0, 1, 0, 0, 0, 0],
     [1, 0, 0, 0, 1, 0, 0, 0,      0, 0, 0, 0, 1, 0, 0, 0],
     [1, 0, 1, 0, 0, 0, 0, 0,      0, 0, 0, 0, 0, 1, 0, 0],
     [1, 1, 0, 0, 0, 0, 0, 0,      0, 0, 0, 0, 0, 0, 1, 0],
     [1, 0, 0, 0, 0, 0, 0, 1,      0, 0, 0, 0, 0, 0, 0, 1]]

BYTE = 8

def encode(message):
    string = ""
    for line in message:
        for sign in line:
            ascii_bin = []
            control_bits = []
            ascii_ = ord(sign)  # przekonwertowanie znaku na kod ASCII

            for i in range(BYTE):
                ascii_bin.append(0)

            for i in range(1, BYTE + 1):
                ascii_bin[-i] = ascii_ % 2  # zamiana kodu ASCII na kod binarny
                ascii_ = int(ascii_ / 2)
                control_bits.append(0)  # wypelnienie tablicy bitow kontrolnych zerami

            for i in range(BYTE):
                for j in range(BYTE):
                    control_bits[i] += ascii_bin[j] * H[i][j]  # obliczenie kolejnych bitow kontrolnych
                control_bits[i] %= 2

            for i in range(BYTE):
                string += str(ascii_bin[i])
            for i in range(BYTE):
                string += str(control_bits[i])
            string += "\n"
    return string


def decode(encoded_message):
    string = ""
    for row in encoded_message:
        arr = []
        err_arr = []
        err1 = 0
        for sign in range(BYTE * 2):
            arr.append(int(row[sign]))
        for i in range(BYTE):
            err_arr.append(0)
        for i in range(BYTE):
            for j in range(BYTE * 2):
                err_arr[i] += arr[j] * H[i][j]
            err_arr[i] %= 2
            if err_arr[i] == 1:
                err1 = 1  # idk, ale blad pojedynczy znaleziony

        if err1 != 0:
            for i in range(BYTE * 2):
                for j in range(i + 1, BYTE * 2):
                    err2 = 1
                    for k in range(BYTE):
                        if err_arr[k] != H[k][i] ^ H[k][j]:
                            err2 = 0
                            break
                    if err2 == 1:  # idk, ale podwojny blad
                        firstError = i
                        secondError = j
                        if arr[firstError] == 1:
                            arr[firstError] = 0
                        else:
                            arr[firstError] = 1
                        if arr[secondError] == 1:
                            arr[secondError] = 0
                        else:
                            arr[secondError] = 1
                        i = BYTE * 2
                        break

            if err1 == 1:
                for i in range(BYTE * 2):
                    for j in range(BYTE):
                        if H[j][i] != err_arr[j]:
                            break
                        if j == 7:
                            if arr[j] == 1:
                                arr[j] = 0
                            else:
                                arr[j] = 1
                            i = BYTE * 2
        ascii_ = 0
        q = BYTE - 1
        for i in range(BYTE):
            ascii_ += arr[i] * (2 ** q)
            q -= 1
        letter = chr(ascii_)
        string += letter
    return string