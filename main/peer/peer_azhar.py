import socket
import threading
import random
import json
import time

class Peer:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # for binding
        self.connections = [] # list of connected peer sockets
        self.connected_to_count = 0 # keeping track of nodes I am connected to 
        self.connected_seed = [] # connected seed socket
        
    
    def connect_to_seed(self,config_file):
        
        lenght = len(config_file)
        # instaed shuffle the dictonary and keep a count of n/2+1 connection if sussessfull then end the loop
        # otherwise keep trying
        random_seeds = dict(random.sample(config_file.items(),(len//2 +1) ))

        peer_to_connect= set()
        for i in random_seeds.keys():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((random_seeds[i][0],random_seeds[i][1]))
             # request send to seed for connection
            if( s.recv(1024).decode() == "yes"):

                self.connected_seed.append(list(s,random_seeds[i]))
                s.sendall((str(self.host)+"-"+str(self.port)).encode())
                print(f"Connected to {i}")

            received_data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                received_data += chunk

            # extraxt the ip and host of peers
            received_list = json.loads(received_data.decode())

            # adding in the set
            for i in received_list:
                
                peer_to_connect.add(i[1])

            
            
        return self.connected_seed,peer_to_connect
    




    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print( f"Listening for connections on {self.host}:{self.port} ................")
        while True:
            connection, address = self.socket.accept()
            self.connected_from.append(connection)
            print(f"Accepted connection from {address}\n")
            # threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def connect(self,peer_list):
        # randomly connect to 4 peers at most
        # and store the connection socket and their ip and port
        peer_list = random.sample(peer_list, 4)
        for i in peer_list:
            try:
                if(self.connected_to_count < 5): 
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
                    connection = s.connect((i[0],i[1]))
                    self.connected_to.append(connection)
                    print(f"Connected to {i[0]}:{i[1]}")
                else: 
                    print("Max connections reached")
            except Exception as e:
                print("error encounter: ",e)


    def start(self):
        listen_thread = threading.Thread(target=self.listen())
        listen_thread.start()

    



