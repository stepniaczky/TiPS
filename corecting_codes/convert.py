from operator import xor

# H [10, 18]
H = [[1, 1, 1, 1, 1, 1, 0, 1,       1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 0, 0, 1, 1, 0, 0,       0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 1, 0, 1, 0, 1, 0,       0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 1, 0, 0, 1, 1,       0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 1, 1, 0, 1, 1,       0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
     [1, 0, 0, 1, 0, 1, 1, 1,       0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
     [0, 0, 1, 0, 1, 1, 0, 1,       0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
     [1, 1, 0, 0, 1, 0, 0, 1,       0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
     [1, 1, 0, 0, 0, 0, 1, 1,       0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
     [1, 1, 0, 0, 1, 0, 1, 0,       0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]


nrRows = 10
nrColumns = 18
asciiColumns = 8
controlColumns = 10


def encode(message):
    encoded_msg = ""  # T
    for line in message:
        for sign in line:
            ascii_bin = []  # kod ASCII binarnie
            control_bits = []  # bity parzystosci
            ascii_ = ord(sign)  # przekonwertowanie znaku na kod ASCII

            for i in range(asciiColumns):
                ascii_bin.append(0)

            for i in range(controlColumns):
                control_bits.append(0)

            for i in range(1, asciiColumns + 1):
                ascii_bin[-i] = ascii_ % 2  # zamiana kodu ASCII na kod binarny
                ascii_ = int(ascii_ / 2)

            for i in range(controlColumns):
                for j in range(asciiColumns):
                    control_bits[i] -= ascii_bin[j] * H[i][j]  # obliczenie kolejnych bitow kontrolnych
                control_bits[i] %= 2                           # c[0] = -h[0][0] * a[0] - ... - h[0][m] * a[m]

            for i in range(asciiColumns):
                encoded_msg += str(ascii_bin[i])
            for i in range(controlColumns):
                encoded_msg += str(control_bits[i])
            encoded_msg += "\n"

    return encoded_msg  # T = [a1, ..., am, c1, ..., cn] wektor nadawanej wiadomosci


def decode(encoded_message):
    string = ""
    for row in encoded_message:
        R = []  # R = T + E
        HR = []  # HR = HT + HE
        HE = []
        singleErr = False
        found = False

        for sign in range(nrColumns):
            R.append(int(row[sign]))  # R = T + E / wektor odebranej wiadomosci

        for i in range(nrRows):
            HR.append(0)
            HE.append(0)

        for i in range(nrRows):
            for j in range(nrColumns):
                HR[i] += R[j] * H[i][j]  # HR = HT + HE
            HE[i] = HR[i] % 2  # HR - HT = HE
            if HE[i] == 1:  # jezeli HE != 0 -> znaleziono blad
                singleErr = True

        if singleErr:
            for i in range(nrColumns):
                if found:
                    break

                for j in range(i + 1, nrColumns):
                    doubleErr = True
                    for k in range(nrRows):  # jezeli bledow jest wiecej niz 1 to HE przyjmie postac sumy
                        if HE[k] != xor(H[k][i], H[k][j]):  # to HE przyjmie postac sumy 2 kolumn macierzy H
                            doubleErr = False  # kolumny macierzy H wskazuja kolumny z bledem w macierzy R
                            break  # jezeli rozni sie choc jedna komorka, przestan sprawdzac kolumny

                    if doubleErr:
                        R[i] = int(not R[i])  # zamiana blednych bitow
                        R[j] = int(not R[j])
                        found = True  # jezeli znalazlo blad, moze przestac szukac
                        break

            if not found:
                for i in range(nrColumns):
                    for j in range(nrRows):

                        if HE[j] != H[j][i]:  # jezeli HE != H dla pojedynczego wyrazu,
                            break             # przestan sprawdzac kolumne
                        if j == nrRows - 1:  # jezeli H = HE to w tej kolumnie jest blad
                            R[i] = int(not R[i])  # zamiana blednego bitu

        ascii_ = 0
        q = asciiColumns - 1
        while q >= 0:  # konwersja z systemu binarnego na dziesietny
            ascii_ += R[-q - 1 - controlColumns] * (2 ** q)
            q -= 1

        letter = chr(int(ascii_))  # zamianu kodu ASCII na odpowiadajacy znak
        string += letter

    return string
