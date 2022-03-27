import os
import unittest
from random import randint

from convert import encode, decode, nrColumns
from stream_functions import save, load


def singleErr(encoded_file):
    string = ''
    for line in encoded_file:
        R = []
        for sign in line:
            R.append(sign)

        nr = randint(0, nrColumns - 1)
        R[nr] = int(not R[nr])
        for i in range(len(R)):
            string += str(R[i])
    return string


def doubleErr(encoded_file):
    string = ''
    for line in encoded_file:
        R = []
        for sign in line:
            R.append(sign)

        nr = randint(0, nrColumns - 1)
        nr2 = nr
        while nr2 == nr:
            nr2 = randint(0, nrColumns - 1)

        R[nr] = int(not R[nr])
        R[nr2] = int(not R[nr2])
        for i in range(len(R)):
            string += str(R[i])
    return string


class MyTestCase(unittest.TestCase):
    def test_main(self):
        string = "totalnie losowy tekst do zakodowania i odkodowania!"
        encoded = encode(string)
        save("test.txt", encoded)
        encoded_file = load("test.txt")

        with_single_err = singleErr(encoded_file)  # wprowadzenie pojedynczego bledu do kazdej linii
        with_double_err = doubleErr(encoded_file)  # wprowadzenie podwojnego bledu do kazdej linii

        save("test.txt", with_single_err)
        save("test2.txt", with_double_err)

        encoded = load("test.txt")
        encoded2 = load("test2.txt")

        decoded = decode(encoded)
        decoded2 = decode(encoded2)

        self.assertEqual(string, decoded)  # sprawdzenie korekcji pojedynczego bledu dla kazdej linii
        self.assertEqual(string, decoded2)  # sprawdzenie korekcji podwojnego bledu dla kazdej linii

        os.remove("stream-files/test.txt")
        os.remove("stream-files/test2.txt")


if __name__ == '__main__':
    unittest.main()
