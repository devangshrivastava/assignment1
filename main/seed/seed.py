
import socket
import threading
import json
import time

lock = threading.Lock()

class Seed:
    def __init__(self,host,port):
        self.ip = host
        self.port = port
        self.connections = []
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle_peer(self,conn,data):
        try:
            
            lock.acquire()
            data_to_send = self.connections
            json_data = json.dumps(data_to_send)
            conn.sendall(json_data.encode())

            self.connections.append(list(conn,data))# increasing the connection list 

            lock.release()
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
        self.soc.bind((self.ip, self.port))
        self.soc.listen()
        print("listening for peers...")
        
        while True:
            
            connection, address = self.soc.accept()

            
            print(f"Accepted connection from {address}")
            connection.sendall("yes".encode())

             
            data = conn.recv(1024).decode()
            data = data.split("-")
            
            threading.Thread(target=self.handle_peer, args=(connection,data)).start() 
            time.sleep(1)
            

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()
    
    def __del__(self):
        self.soc.close()
    
    







