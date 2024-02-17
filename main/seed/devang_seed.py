import socket
import threading
import datetime

class Seed:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_count = 0
        self.connections = []
        self.logfile = f"logfile_{self.port}.txt"
        self.connected_peers = [["PEERS"]]

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        self.log(f"Listening for connections on {self.host}:{self.port}")

        while True:
            connection, address = self.socket.accept()
            self.connections.append(connection)

            self.log(f"Accepted connection from {address}")
            threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def send_data(self, data):
        for connection in self.connections:
            try:
                connection.sendall(data.encode())
                peer_address = connection.getpeername()
                self.log(f"Sent data to {peer_address}: {data}")
            except socket.error as e:
                self.log(f"Failed to send data. Error: {e}")
                self.connections.remove(connection)
    
    def send_list(self, connection):
        data_list = self.connected_peers
        encoded_data = "-".join(",".join(map(str, sublist)) for sublist in data_list)
        try:
            connection.sendall(encoded_data.encode())
            peer_address = connection.getpeername()
            self.log(f"Sent data list to {peer_address}: {data_list}")
        except socket.error as e:
            self.log(f"Failed to send data list. Error: {e}")
            self.connections.remove(connection)


    def handle_client(self, connection, address):
        self.log(f"Connection from {address} opened.")
        self.send_list(connection)
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                data = data.decode()
                if data.startswith("STORE-"):
                    host_port_str = data.split("-")[1]  
                    host, port = host_port_str.split(":") 
                    self.connected_peers.append([host, port])
                self.log(f"data from :{address}: {data}")
                if data.startswith("REMOVE-"):
                    host_port_str = data.split("-")[1]  
                    host, port = host_port_str.split(":")
                    try:
                        self.connected_peers.remove([host,port])
                        self.log(f"data from :{address}: {data}")
                        print(self.connected_peers)
                        self.log(f"new peer list :{str(self.connected_peers)}")
                    except Exception as e: 
                        pass
            except socket.error:
                break

        self.log(f"Connection from {address} closed.")
        self.connections.remove(connection)
        connection.close()

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        with open(self.logfile, "a") as f:
            f.write(log_message)


