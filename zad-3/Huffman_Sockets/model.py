from socket import AF_INET, SOCK_DGRAM, socket
#from huffman import decoding


class SocketSide:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.s = socket(AF_INET, SOCK_DGRAM)


class Client(SocketSide):
    def __init__(self, ip, port):
        super().__init__(ip, port)

    def connect(self):
        self.s.connect((self.ip, self.port))

    def disconnect(self):
        self.s.close()

    def send(self, file):
        # server = ('192.168.0.104', 4000)
        self.s.send(file.encode('utf-8'))
        self.s.send('END'.encode('utf-8'))
        received_from_server = self.s.recv(1024).decode('utf-8')
        return True if received_from_server == 'END' else False


class Server(SocketSide):
    clientConnection, clientAddress = None, None
    received_text = ""

    def __init__(self, ip, port):
        super().__init__(ip, port)
        # self.serverSocket = socket.socket(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket = socket()

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


