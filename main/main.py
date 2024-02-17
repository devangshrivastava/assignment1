from seed.devang_seed import Seed
from peer.peer import Peer 
import time
import random

from seed import config_file

seed_info = config_file.seed_info

try:

    seed_list=[]
    
    for i in seed_info.values():
        print("Starting seed node with :", i, ".....")
        s = Seed(i[0],i[1])
        s.start()

        seed_list.append(s)

    time.sleep(1)
    
    peer_list = []
    for i in range(8000,8008):
        peer = Peer("127.0.0.1",i)
        peer.start()
  
        sampled_list = random.sample(seed_list, (len(seed_list)//2 + 1))

        for i in sampled_list:
            peer.connect_seed(i.host, i.port)
            # time.sleep(1)

        time.sleep(1)
        sample_peer=[]
        
        if( len(peer.peers)>=4):
            sample_peer = random.sample(list(peer.peers),4)

        else:
            sample_peer = random.sample(list(peer.peers),len(peer.peers))

        for p in sample_peer:
            
            peer.connect(p[0], p[1])

        peer_list.append(peer)

        time.sleep(1)
        

    time.sleep(13)
    peer_list[0].close_socket()
    print("Peer 1 closed")

    
    seed_list[0].send_data("Hello")
    time.sleep(2)
    peer_list[0].send_data("MESSAGE Hello")
    time.sleep(1)
    
    for conn in peer_list[3].connections:
        print(conn)
    print(len(peer_list[0].connections))

    for conn in peer_list[3].connected:
        print(conn[0], conn[1], conn[2])
    

    print(len(peer_list[0].messages))
    for msg in peer_list[3].messages:
        print(msg.message)
        print(msg.sent_to)
        print(msg.received_from)

except KeyboardInterrupt:
    print("Shutting down...")
    print("Goodbye!")

