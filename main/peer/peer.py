import socket
import threading
import time
import os

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_to = []
        self.connected_from = []
        self.seed_socket = []
        self.log_file = f"peer_{port}_log.txt"

    def log_activity(self, activity):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as file:
            file.write(f"[{timestamp}] {activity}\n")

    def connect(self, peer_host, peer_port):
        activity = ""
        if(len(self.connected_to) < 5):    
            connection = socket.create_connection((peer_host, peer_port))
            self.connected_to.append(connection)
            activity = f"Connected to {peer_host}:{peer_port}"
        else: 
            activity = "Max connections reached"

        # print(activity)
        self.log_activity(activity)

    def connect_to_seed(self, seed_host, seed_port):
        connection = socket.create_connection((seed_host, seed_port))
        activity = f"Connected to {seed_host}:{seed_port}"
        self.seed_socket.append(connection)
        self.log_activity(activity)
        # print(activity)
        


    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        activity = f"Listening for connections on {self.host}:{self.port}"
        # print(activity)
        self.log_activity(activity)
        threading.Thread(target=self.send_heartbeat).start()
        while True:
            connection, address = self.socket.accept()
            self.connected_from.append(connection)
            activity = f"Accepted connection from {address}\n"
            self.log_activity(activity)
            threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def send_heartbeat(self):
        while True:
            # Send heartbeat to each connected peer
            for connection in self.connected_to:
                try:
                    m = "Heartbeat from " + str(self.port)
                    connection.sendall(m.encode())
                except socket.error as e:
                    print(f"Failed to send heartbeat to {connection.getpeername()}. Error: {e}")
                    self.connected_to.remove(connection)
            time.sleep(5)  

    def send_data(self, data):
        for connection in self.connected_to:
            try:
                connection.sendall(data.encode())
                activity = f"Sent data to {connection.getpeername()}: {data}"
                # print(activity)
                self.log_activity(activity)
            except socket.error as e:
                print(f"Failed to send data. Error: {e}")
                self.connected_to.remove(connection)

    def handle_client(self, connection, address):
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                data = data.decode()
                if data.startswith("Heartbeat"): continue 
                activity = f"Received data from {address}: {data}"
                # print(activity)
                self.log_activity(activity)
            except socket.error:
                break

        activity = f"Connection from {address} closed."
        # print(activity)
        self.log_activity(activity)
        self.connected_to.remove(connection)
        self.connected_from.remove(connection)
        connection.close()

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

    def close_connections(self):
        for conn in self.connected_to:
            conn.close()
        for conn in self.connected_from:
            conn.close()
        self.socket.close()
        activity = "Connections closed"
        os.remove(self.log_file)
        # print(activity)
        self.log_activity(activity)
        



    

    