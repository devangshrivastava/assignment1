import socket
import threading
import datetime
import time

import hashlib


class Message:
    def __init__(self,message):
        self.message = message
        self.hash = hashlib.sha256(message.encode()).hexdigest()
        self.received_from = []
        self.sent_to = []



class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_count = 0
        self.connections = []
        self.logfile = f"logfile_{self.port}.txt"
        self.peers = []
        self.messages = []

    def connect(self, peer_host, peer_port):
        connection = socket.create_connection((peer_host, peer_port))
        self.connections.append(connection)
        self.log(f"Connected to {peer_host}:{peer_port}")
        data = f"STORE-{self.host}:{self.port}"
        connection.sendall(data.encode())
        threading.Thread(target=self.listen_other, args=(connection,)).start()

    def message_check(self,message):
        hash = hashlib.sha256(message.encode()).hexdigest()
        for msg in self.messages:
            if msg.hash == hash:
                return False
        return True

    def listen_other(self,connection):
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                data = data.decode()
                address = connection.getpeername()
                self.log(f"Received data from :{address}: {data}")
                if data.startswith("PEERS-"):
                    peer_strings = data.split("-")[1:]
                    for peer_string in peer_strings:
                        host, port = peer_string.split(",")
                        self.peers.append((host, int(port)))
                
                if data.startswith("MESSAGE"):
                    b = self.message_check(data)
                    if b:
                        self.send_data(data)
                        time.sleep(1)
                        msg = Message(data)
                        self.messages.append(msg)
                

                    

            except socket.error:
                break
        self.log(f"Connection from closed.")
        connection.close()



    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        self.log(f"Listening for connections on {self.host}:{self.port}")

        while True:
            connection, address = self.socket.accept()
            self.connections.append(connection)
            peer_address = connection.getpeername()
            self.log(f"Accepted connection from {peer_address}")
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


    #shayad kuch nhi karta ye ab
    def handle_client(self, connection, address):
        self.log(f"Connection from {address} opened.")
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                data = data.decode()
                self.log(f"data from :{address}: {data}")
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

# Example usage:
# if __name__ == "__main__":
#     node1 = Peer("0.0.0.0", 8000)
#     node1.start()

#     node2 = Peer("0.0.0.0", 8001)
#     node2.start()

#     # Give some time for nodes to start listening
#     import time
#     time.sleep(2)

#     node2.connect("127.0.0.1", 8000)
#     time.sleep(1)  # Allow connection to establish

#     node2.send_data("Hello from node2!")
    
#     node1.send_data("Hello from node1!")
#     time.sleep(1)  # Allow time for data to be received
