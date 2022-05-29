import logging
from models.player import Player
from models.recorder import Recorder
from time import sleep


def int_choice(msg, cond=None):
    while True:
        try:
            n = int(input(msg))
            if cond is not None:
                if n not in cond:
                    raise ValueError
            return n
        except ValueError:
            print("Try again!")


def main():
    sampling = abs(int_choice("Frequency of sampling [Hz]: "))
    quantization = int_choice("Level of quantization [8, 16, 32]: ", [8, 16, 32])
    print()

    menu = ["Type 'r' to start recording", "Type 's' to save recorded audio",
            "Type 'p' to play recorded audio", "Type 'z' to play saved audio",
            "Type 'q' to quit the program", "Type 'h' to display all options"]

    for line in menu:
        print(line)

    recorder = Recorder(sampling, quantization)
    player = Player(sampling)
    logging.basicConfig(format='%(asctime)s : %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
    msg = ''

    while True:
        opt = input("\nOption: ")
        match opt:
            case 'r':
                recorder.clear_recorded_audio()
                time = int_choice("Set recording time [s]: ")
                logging.info("Recording is starting in: ")
                sleep(0.1)
                i = 3
                while i > 0:
                    print(f"{i}...")
                    sleep(1)
                    i -= 1
                recorder.record(time)
                logging.info("Recording is stopped.")

            case 's':
                msg = recorder.save("audio.wav")

            case 'p':
                msg = player.play_recorded(recorder.rec_audio)

            case 'z':
                msg = player.play_saved("audio.wav")

            case 'q':
                logging.info("Exiting the program.")
                break

            case 'h':
                for line in menu:
                    print(line)

            case _:
                logging.info("Unknown option.")

        if opt in ['s', 'p', 'z']:
            logging.info(msg)
        sleep(0.1)


if __name__ == '__main__':
    main()
