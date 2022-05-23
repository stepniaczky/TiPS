from socket import AF_INET, SOCK_DGRAM, socket
from os import mkdir, path
from datetime import datetime
from huffman import Huffman
import ast


def chunk_data(file):
    chunks = [file[i:i + 128] for i in range(0, len(file), 128)]
    return chunks


def save_and_log(client_ip_address, received_dict, received_data):
    if not path.exists("data"):
        mkdir("data")
    if not path.exists("data/server"):
        mkdir("data/server")

    current_time = datetime.now()
    file_time = current_time.strftime("%d-%m-%Y-%H-%M-%S")
    log_time = current_time.strftime("%d-%m-%Y %H:%M:%S")

    dir_path = f"data/server/{client_ip_address}"
    if not path.exists(dir_path):
        mkdir(dir_path)

    _dict = ""
    for chunk in received_dict:
        _dict += chunk
    _dict = ast.literal_eval(_dict)

    data = ""
    for row in received_data:
        data += row

    h = Huffman(data, _dict)
    decoded = h.decode()

    with open(f"{dir_path}/{file_time}.txt", "w") as file:
        file.write(decoded)
    print(f"{log_time}  Data from {client_ip_address} has been "
          f"successfully received and written to the file")


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

    def send(self, _dict, file):
        _dict = chunk_data(_dict)
        for d in _dict:
            self.s.send(d.encode('utf-8'))
        self.s.send('DICT'.encode('utf-8'))

        file = chunk_data(file)
        for chunk in file:
            self.s.send(chunk.encode('utf-8'))
        self.s.send('END'.encode('utf-8'))

        received_from_server = self.s.recv(1024).decode('utf-8')
        return True if received_from_server == 'END' else False


class Server(SocketSide):

    def __init__(self, ip, port):
        super().__init__(ip, port)

    def start(self):
        received_dict = ""
        received_data = ""
        self.s.bind((self.ip, self.port))

        try:
            while True:
                (client_data, client_address) = self.s.recvfrom(1024)
                client_data = client_data.decode('utf-8')
                if client_data == "DICT":
                    received_dict = received_data
                    received_data = ""

                if client_data == "END":
                    self.s.sendto(client_data.encode('utf-8'), client_address)
                    save_and_log(client_address[0], received_dict, received_data)
                    received_data = ""

                if client_data not in ["DICT", "END"]:
                    received_data += client_data
        except KeyboardInterrupt:
            self.s.close()
            return
