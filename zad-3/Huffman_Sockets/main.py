from model import Client, Server
from huffman import Huffman
from subprocess import call
import os


def toBinary(a):
    l, m = [], []
    for i in a:
        l.append(ord(i))
    for i in l:
        m.append(bin(i)[2:])
    return ''.join(m)


def clear():
    # check and make call for specific operating system
    try:
        _ = call('clear' if os.name == 'posix' else 'cls')
    except FileNotFoundError:
        print("\nClear command is available only for os shell/terminal\n")


def validate_int(msg):
    try:
        test = int(input(msg))
        return test
    except ValueError:
        print("Port number must be an integer!")
        return validate_int(msg)


def load(filename):
    dir_path = "data/client"
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    with open(f"{dir_path}/{filename}") as file:
        arr = file.read()
    return arr


def server():
    port = int
    ip = str
    setup_flag = False
    while True:
        command = ""
        try:
            command = input("server>")
        except KeyboardInterrupt:
            print('\n^C', end='')
            quit()
        if command not in ["exit", "clear"]:
            print()
        match command.split():
            case ["setup"]:
                ip = input("ip address: ")
                port = int(input("port: "))
                setup_flag = True
            case ["start"]:
                if setup_flag is True:
                    s = Server(ip, port)
                    s.start()
                else:
                    print("Firstly, configure the socket to listen!")
            case ["exit"]:
                return
            case ["clear"]:
                clear()
            case ["help"]:
                print("setup", "start", "clear",
                      "exit", "help", sep="\n")
            case _:
                print("Unknown command.")
                print("Type 'help' to see available commands.")
        if command not in ["exit", "clear"]:
            print()


def client():
    port = int
    ip = str
    setup_flag = False
    connection_flag = False
    while True:
        command = ""
        try:
            command = input("client>")
        except KeyboardInterrupt:
            print('\n^C', end='')
            quit()
        if command not in ["exit", "clear"]:
            print()
        match command.split():
            case ["setup"]:
                ip = input("server ip address: ")
                port = validate_int("server port: ")
                setup_flag = True
            case ["send", filename]:
                # connecting phase
                if setup_flag is True:
                    s = Client(ip, port)
                    try:
                        s.connect()
                        connection_flag = True
                        print(f"You are connected to the server: ({ip}, {port})")
                    except TimeoutError:
                        print("Timeout error")
                    except ConnectionRefusedError:
                        print("Connection refused error.")

                    # sending data after establishing a connection with the server
                    if connection_flag is True:
                        try:
                            if not filename.__contains__(".txt"):
                                filename = f"{filename}.txt"
                            file = load(filename)
                            h = Huffman(file)
                            encoded = h.encode()
                            _dict = f"{h.sign_freq}"
                            operation_flag = s.send(_dict, encoded)
                            if operation_flag is True:
                                print("File has been successfully received by server.")

                                with open('data/client/test1.txt', "w") as test1:
                                    test1.write(toBinary(file))
                                before = os.path.getsize(f'data/client/test1.txt')

                                with open('data/client/test2.txt', "w") as test2:
                                    test2.write(encoded)
                                after = os.path.getsize('data/client/test2.txt')

                                compression_ratio = round(100 / (before / after), 2)
                                print(f'Size of transmitted file is {compression_ratio}% of the'
                                      f' original ASCII file.')
                                os.remove('data/client/test1.txt')
                                os.remove('data/client/test2.txt')
                            else:
                                print("An error occurred while sending file to the server.")
                        except FileNotFoundError:
                            print(f"File with name '{filename}' does not exist!")

                        # disconnecting phase
                        s.disconnect()
                        print("You are disconnected from the server.")

                else:
                    print("Configure the server socket before establishing a connection.")

            case ["exit"]:
                return
            case ["clear"]:
                clear()
            case ["help"]:
                print("setup", "send <filename>", "clear",
                      "exit", "help", sep="\n")
            case _:
                print("Unknown command.")
                print("Type 'help' to see available commands.")
        if command not in ["exit", "clear"]:
            print()


def main(command):
    if command not in ["server", "client", "exit", "clear"]:
        print()
    match command.split():
        case ["server"]:
            server()
        case ["client"]:
            client()
        case ["exit"]:
            quit()
        case ["clear"]:
            clear()
        case ["help"]:
            print("server", "client", "clear", "exit", "help", sep="\n")
        case _:
            print("Unknown command.")
            print("Type 'help' to see available commands.")
    if command not in ["server", "client", "exit", "clear"]:
        print()


if __name__ == "__main__":
    while True:
        try:
            main(input("$>"))
        except KeyboardInterrupt:
            print('\n^C', end='')
            quit()
