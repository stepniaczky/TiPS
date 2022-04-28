import socket
#from huffman import decoding


class SocketController:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port


class Client(SocketController):
    def __init__(self, ip, port):
        super().__init__(ip, port)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.clientSocket.connect((self.ip, self.port))

    def disconnect(self):
        self.clientSocket.close()

    def send(self, file):
        pass


class Server(SocketController):
    clientConnection, clientAddress = None, None
    received_text = ""

    def __init__(self, ip, port):
        super().__init__(ip, port)
        # self.serverSocket = socket.socket(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket = socket.socket()

    def listen(self):
        # self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # czy to potrzebne
        self.serverSocket.bind((self.ip, self.port))
        self.serverSocket.listen()
        (self.clientConnection, self.clientAddress) = self.serverSocket.accept()

    def receive(self):
        while True:
            data = self.clientConnection.recv(1024).decode()
            if data == "END":
                msg = "Odpowiedz serwera:\nTransfer udany, zakanczanie polaczenia!"
                msgBytes = str.encode(msg)
                self.clientConnection.send(msgBytes)
                print("\nConnection closed.\n")
                break
            self.received_text += data
        return self.received_text
        #decoded_text = decoding(self.received_text)
        #return decoded_text


