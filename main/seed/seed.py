import config_file
import socket
import threading
import json

class Seed:
    def __init__(self,IP,PORT):
        self.IP = IP
        self.PORT = PORT
        self.connections = []
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle_client(self,conn,addr):
        try:
            
            data_to_send = self.connections

            # Serialize the list to JSON
            json_data = json.dumps(data_to_send)

            # Send the JSON data
            conn.sendall(json_data.encode())

        except Exception as e:
            print("error sending the list")

    # -- helper Code --------------------------------
    # received_data = b""
    #     while True:
    #         chunk = client_socket.recv(4096)
    #         if not chunk:
    #             break
    #         received_data += chunk

    #     # Deserialize the received JSON data
    #     received_list = json.loads(received_data.decode())
        
        


    def listen(self):
        self.soc.bind(self.IP, self.PORT)
        self.soc.listen()
        print("listening for peers...")

        while True:
            
            connection, address = self.soc.accept()
            
            print(f"Accepted connection from {address}")
            
            threading.Thread(target=self.handle_client, args=(connection, address)).start()
            self.connections.append(connection)

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()
    
    
    







