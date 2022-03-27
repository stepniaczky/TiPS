import unittest
from random import randint

from convert import encode, decode
from stream_functions import save, load

from convert import nrColumns


class MyTestCase(unittest.TestCase):
    def test_main(self):
        string = "totalnie losowy tekst do zakodowania i odkodowania!"
        encoded = encode(string)
        save("test.txt", encoded)
        encoded_file = load("test.txt")

        with_single_err = self.singleErr(encoded_file)
        with_double_err = self.doubleErr(encoded_file)

        save("test1.txt", with_single_err)
        save("test2.txt", with_double_err)

        encoded1 = load("test1.txt")
        encoded2 = load("test2.txt")

        decoded = decode(encoded1)
        decoded2 = decode(encoded2)

        self.assertEqual(string, decoded)
        self.assertEqual(string, decoded2)

    def singleErr(self, encoded_file):
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

    def doubleErr(self, encoded_file):
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


if __name__ == '__main__':
    unittest.main()
