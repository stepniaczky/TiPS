def main():
    sampling = abs(int(input("Frequency of sampling [Hz]: ")))
    quantization = int(input("Level of quantization [8, 16, 32]: "))

    print("--- PROGRAM OPTIONS ---"
          "Press 'r' to start recording"
          "Press 'm' to stop recording"
          "Press 's' to save recorded audio"
          "Press 'p' to play recorded audio"
          "Press 'z' to play saved audio")


if __name__ == '__main__':
    main()
