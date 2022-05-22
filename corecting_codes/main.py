from stream_functions import save, load
from convert import encode, decode


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
            encoded = encode(message)
            save(f"encoded-{filename}", encoded)
            print(f"Pomyslnie zapisano zakodowana wiadomosc do pliku: encoded-{filename}")
        except FileNotFoundError:
            print("Podano bledna nazwe pliku!")

    elif choice == 2:
        filename = input("Nazwa pliku, ktory chcesz odkodowac: ")
        try:
            encoded_message = load(filename)
            decoded = decode(encoded_message)
            save(f"decoded-{filename[8:]}", decoded)
            print(f"Pomyslnie zapisano odkodowana wiadomosc do pliku: decoded-{filename[8:]}")
        except FileNotFoundError:
            print("Podano bledna nazwe pliku!")

    elif choice == 3:
        return 0

    else:
        print("Wpisano niepoprawna wartosc!")

    print()
    menu()


# application start
if __name__ == '__main__':
    menu()
