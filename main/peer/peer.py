import socket
import threading
import time

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_to = []
        self.connections_from = []

    def connect(self, peer_host, peer_port):
        connection = socket.create_connection((peer_host, peer_port))

        self.connected_to.append(connection)
        print(f"Connected to {peer_host}:{peer_port}\n")

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f"Listening for connections on {self.host}:{self.port}\n")
        threading.Thread(target=self.send_heartbeat).start()
        while True:
            connection, address = self.socket.accept()
            self.connections_from.append(connection)
            print(f"Accepted connection from {address}\n")
            threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def send_heartbeat(self):
        while True:
            # Send heartbeat to each connected peer
            for connection in self.connections_from:
                try:
                    m = "Heartbeat from " + str(self.port)
                    connection.sendall(m.encode())
                except socket.error as e:
                    print(f"Failed to send heartbeat to {connection.getpeername()}. Error: {e}")
                    self.connections.remove(connection)
            time.sleep(13)  

    def send_data(self, data):
        for connection in self.connections:
            try:
                connection.sendall(data.encode())
            except socket.error as e:
                print(f"Failed to send data. Error: {e}")
                self.connections.remove(connection)

    def handle_client(self, connection, address):
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                data = data.decode()
                if data.startswith("Heartbeat"): continue 
                print(f"Received data from {address}: {data}")
            except socket.error:
                break

        print(f"Connection from {address} closed.")
        self.connections.remove(connection)
        connection.close()

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

    def close_connections(self):
        for conn in self.connections:
            conn.close()
        self.socket.close()
        self.socket.close()
        print("Connections closed")




    

    