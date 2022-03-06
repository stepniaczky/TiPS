from stream_functions import save, load
from convert import code, decode

H = [[1, 0, 1, 0, 0, 1, 0, 1,      1, 0, 0, 0, 0, 0, 0, 0],    # 165 / 128
     [0, 1, 1, 1, 0, 1, 1, 1,      0, 1, 0, 0, 0, 0, 0, 0],    # 119 / 64
     [0, 0, 0, 1, 1, 1, 1, 0,      0, 0, 1, 0, 0, 0, 0, 0],    # 30 / 32
     [1, 0, 0, 0, 1, 1, 1, 1,      0, 0, 0, 1, 0, 0, 0, 0],    # 143 / 16
     [1, 1, 1, 0, 0, 0, 1, 0,      0, 0, 0, 0, 1, 0, 0, 0],    # 226 / 8
     [1, 1, 1, 1, 0, 0, 0, 1,      0, 0, 0, 0, 0, 1, 0, 0],    # 241 / 4
     [1, 1, 0, 1, 1, 1, 0, 1,      0, 0, 0, 0, 0, 0, 1, 0],    # 221 / 2
     [0, 1, 0, 0, 1, 0, 1, 1,      0, 0, 0, 0, 0, 0, 0, 1]]    # 75 / 1

def menu():
    choice = int
    try:
        choice = int(input("--- MENU ---\n"
                           "1: Zakoduj wiadomosc\n"
                           "2: Odkoduj wiadomosc\n"
                           "3: Zakoncz program\n"
                           "Twoj wybor:  "))
        main(choice)
    except ValueError:
        main(choice)


def main(choice):
    if choice == 1:
        filename = input("Nazwa pliku, ktory chcesz zakodowac: ")
        try:
            message = load(filename)
            encoded = code(message)
            save(f"coded-{filename}", encoded)
        except FileNotFoundError:
            print("Podano bledna nazwe pliku!")

    elif choice == 2:
        filename = input("Nazwa pliku, ktory chcesz odkodowac: ")
        try:
            encoded_message = load(filename)
            decoded = decode(encoded_message)
            save(f"encoded-{filename}", decoded)
        except FileNotFoundError:
            print("Podano bledna nazwe pliku!")

    elif choice == 3:
        return 0

    else:
        print("Wybrano niepoprawna wartosc!")

    print()
    menu()

menu()