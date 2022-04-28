import os
from model import Client, SocketController, Server
#from huffman import *


def validate_int(msg):
    try:
        test = int(input(msg))
        return test
    except ValueError:
        return validate_int(msg)


def save(filename, msg):
    with open(f"data/{filename}", "w") as file:
        file.write(msg)


def load(filename):
    with open(f"data/{filename}") as file:
        arr = file.readlines()
    return arr


def server():
    port = int
    ip = str
    s = None
    setup_flag = False
    connection_flag = False
    clientConnection, clientAddress = None, None
    received_text = None
    while True:
        command = input("server>")
        if command not in "exit" "clear":
            print()
        match command.split():
            case ["setup"]:
                port = int(input("port: "))
                ip = input("ip address: ")
                setup_flag = True
            case ["listen"]:  # dodac jakis czas po ktorym nastepuje przerwanie nasluchiwania
                s = Server(ip, port)
                s.listen()
                received_text = s.receive()
                # moze jeszcze wyswietle ten tekst na konsoli
                filename = input("Type the file name to save the received text: ")
                if filename.__contains__(".txt"):
                    save(f"data/{filename}", received_text)
                else:
                    save(f"data/{filename}.txt", received_text)
            case ["exit"]:
                return
            case ["clear"]:
                os.system("cls")
            case ["help"]:
                print("setup", "connect", "disconnect", "send <filename>",
                      "clear", "exit", "help", sep="\n")
            case _:
                print("Unknown command.")
                print("Type 'help' to see available commands.")
        if command not in "exit" "clear":
            print()


def client():
    port = int
    ip = str
    s = None
    setup_flag = False
    connection_flag = False
    while True:
        command = input("client>")
        if command not in "exit" "clear":
            print()
        match command.split():
            case ["setup"]:  # albo connection setup
                ip = input("ip address: ")
                port = validate_int("port: ")
                setup_flag = True
            case ["connect"]:
                if setup_flag is True:
                    s = Client(ip, port)
                    try:
                        s.connect()
                    except TimeoutError:
                        print("Timeout error")
                    except ConnectionRefusedError:
                        print("Connection refused error")
                else:
                    print("Setup your connection before establishing a connection.")
            case ["disconnect"]:
                if connection_flag is True:
                    s.disconnect()
                else:
                    print("You are not connected to any server.")
            case ["send", filename]:
                file = load(filename)
                s.send(file)
            case ["exit"]:
                return
            case ["clear"]:
                os.system("cls")
            case ["help"]:
                print("setup", "connect", "disconnect", "send <filename>",
                      "clear", "exit", "help", sep="\n")
            case _:
                print("Unknown command.")
                print("Type 'help' to see available commands.")
        if command not in "exit" "clear":
            print()


def main(command):
    if command not in "server" "client" "exit" "clear":
        print()
    match command.split():
        case ["server"]:
            server()
        case ["client"]:
            client()
        case ["exit"]:
            quit()
        case ["clear"]:
            os.system("cls")
        case ["help"]:
            print("server", "client", "clear", "exit", "help", sep="\n")
        case _:
            print("Unknown command.")
            print("Type 'help' to see available commands.")
    if command not in "server" "client" "exit" "clear":
        print()


if __name__ == "__main__":
    while True:
        main(input("$>"))
