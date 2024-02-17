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
        self.seed = []
        self.connections = []
        self.connected = [] #port, host, socket
        self.logfile = f"logfile_{self.port}.txt"
        self.peers = set()
        self.messages = []
        self.messages_to_send=[]
        self.inital_peer_count=0

    def connect(self, peer_host, peer_port):
        if self.inital_peer_count < 4:
            connection = socket.create_connection((peer_host, peer_port))
            self.connected.append([peer_port, peer_host, connection])
            self.inital_peer_count+=1
            self.log(f"Connected to {peer_host}:{peer_port}")
            data = f"STORE-{self.host}:{self.port}"
            connection.sendall(data.encode())
            threading.Thread(target=self.listen_other, args=(connection,)).start()

    def connect_seed(self, peer_host, peer_port):
        connection = socket.create_connection((peer_host, peer_port))
        self.seed.append(connection)
        
        self.log(f"Connected to {peer_host}:{peer_port}")
        data = f"STORE-{self.host}:{self.port}"
        connection.sendall(data.encode())
        threading.Thread(target=self.listen_other, args=(connection,)).start()

    def message_check(self,message):
        hash = hashlib.sha256(message.encode()).hexdigest()
        for msg in self.messages:
            if msg.hash == hash: return True
        return False

    def heartbeat(self,connection):
        counter = 0
        port = 123456
        addr ="123456"
        for conn in self.connected:
            if(conn[2] == connection):
                addr = conn[1]
                port = conn[0]
                break
        
        while counter < 3 and connection not in self.seed:
            if port !=123456: self.log(f"Sending heartbeat to {port}")
            time.sleep(13)
            try:
                data = "HEARTBEAT"
                connection.sendall(data.encode())
                counter = 0
            except Exception as e:
                counter += 1
        
        # self.log(f"Connection from {port} closed.")  

        if port !=123456:
            
            self.log(f"3 calls completed. {port} is unfortunately dead :( ")
            try:
                self.connected.remove([port,addr,connection])
            except Exception as e:
                pass
            for conn in self.seed:
                self.send_seed_to_remove_peer(addr,port,conn)

            connection.close()

    def listen_other(self,connection):
        threading.Thread(target=self.heartbeat, args=(connection,)).start()
        
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
                        self.peers.add((host, int(port)))        
                elif data.startswith("MESSAGE"):
                    b = self.message_check(data)
                    if not b:
                        msg = Message(data)
                        for conn in self.connected:
                            if(conn[2] == connection):
                                msg.received_from.append([conn[0], conn[1]])
                                break      
                        self.messages.append(msg)
                        # self.send_data(data) # devang 
                        self.messages_to_send.append(msg)
                        
                if data.startswith("STORE"):
                    host_port_str = data.split("-")[1]  
                    host, port = host_port_str.split(":") 
                    self.connected.append([int(port), host, connection])
                if data.startswith("HEARTBEAT"):
                    
                    continue

            except socket.error:
                break
        
        port = 123456
        for conn in self.connected:
            if(conn[2] == connection):
                port = conn[0]
                break
        # if(port != 123456):
            # self.connected.remove([port, connection.getpeername()[0], connection])
        self.log(f"listening to  {port} closed.")
        connection.close()

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        self.log(f"Listening for connections on {self.host}:{self.port}")
        while True:
            try:
                connection, address = self.socket.accept()
            except socket.error as e:
                self.log(f"Failed to accept connection. Error: {e}")
                break
            # self.connections.append(connection)
            peer_address = connection.getpeername()
            self.log(f"Accepted connection from {peer_address}")
            threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def send_data(self, data):
        msg = None
        if(data.startswith("MESSAGE")):
            for m in self.messages:
                if m.message == data:
                    msg = m
                    break
            
        for conn in self.connected:
            connection = conn[2]
            
            if msg is not None and [conn[0], conn[1]] not in msg.received_from :
                msg.sent_to.append([conn[0], conn[1]]) #port, host,
            # elif msg != None and conn[0] == msg.received_from[0][0]: continue
                try:
                    connection.sendall(data.encode())
                    peer_address = connection.getpeername()
                    self.log(f"Sent data to {peer_address}: {data}")
                except socket.error as e:
                    self.log(f"Failed to send data. Error: {e}")
                    try:
                        self.connected.remove(conn)
                    except Exception as e:
                        pass

    
    def handle_client(self, connection, address):
        threading.Thread(target=self.heartbeat, args=(connection,)).start()
        threading.Thread(target=self.gossip, args=()).start()
        self.log(f"Connection from {address} opened.")
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                data = data.decode()
                port = 123456
                for conn in self.connected:
                    if(conn[2] == connection):
                        port = conn[0]
                        break
                self.log(f"Received data from :{port}: {data}")
                if data.startswith("STORE"):
                    host_port_str = data.split("-")[1]  
                    host, port = host_port_str.split(":") 
                    self.connected.append([int(port), host, connection])
                elif data.startswith("MESSAGE"):
                    b = self.message_check(data)
                    if not b: #if not exist then false
                        msg = Message(data)
                        for conn in self.connected:
                            if(conn[2] == connection):
                                msg.received_from.append([conn[0], conn[1]])
                                break        
                        self.messages.append(msg)
                        # self.send_data(data) # devang
                        self.messages_to_send.append(msg)
                        time.sleep(1)
                elif data.startswith("HEARTBEAT"):
                    continue
                if port != 123456: address = port
                self.log(f"data from :{address}: {data}")
            except socket.error:
                break

        self.log(f"Task over {address} closed.")
        # self.connections.remove(connection)
        connection.close()

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

    def send_seed_to_remove_peer(self,peer_host,peer_port,connection):
        data = "REMOVE-" + str(peer_host) + ":" + str(peer_port)
        connection.sendall(data.encode())

    def gossip(self): # put this in thread of handel client
        

        for i in range(10):
            

            data = "MESSAGE-"+str(i)+"-From-"+str(self.host)+":"+str(self.port)

            msg=Message(data)
            msg.received_from.append([self.host,self.port])
            self.messages.append(msg)
            
            self.messages_to_send.append(msg)
            
            for messy in self.messages_to_send:
                self.send_data(messy.message)

            self.messages_to_send=[] # empty the list

            time.sleep(5)

            

        
    def close_socket(self):
        try:
            for conn in self.connected:
                conn[2].close()
            
            for conn in self.seed:
                conn.close() 
            
            self.socket.close()
            
            print("Peer closed successfully")
        
        except socket.error as e:
            print(f"Error closing the Peer: {e}")

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        with open(self.logfile, "a") as f:
            f.write(log_message)

