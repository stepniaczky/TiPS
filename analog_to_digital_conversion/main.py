import keyboard
from models.player import Player
from models.recorder import Recorder


def main():
    sampling = abs(int(input("Frequency of sampling [Hz]: ")))
    quantization = int(input("Level of quantization [8, 16, 32]: "))

    print("Press 'r' to start recording",
          "Press 'm' to stop recording"
          "Press 's' to save recorded audio",
          "Press 'p' to play recorded audio",
          "Press 'z' to play saved audio",
          "Press 'q' to quit the program", sep="\n")

    recorder = Recorder(sampling, quantization)
    player = Player(sampling)

    while True:
        if keyboard.is_pressed('r'):
            while True:
                if keyboard.is_pressed('m'):
                    break
                recorder.record(1)

        if keyboard.is_pressed('s'):
            recorder.save()

        if keyboard.is_pressed('p'):
            player.play_recorded()

        if keyboard.is_pressed('z'):
            player.play_saved()

        if keyboard.is_pressed('q'):
            break


if __name__ == '__main__':
    main()
