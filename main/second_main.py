from seed.devang_seed import Seed
from peer.peer import Peer 
import time
import random

seed1 = Seed("127.0.0.1", 7000)
seed1.start()
seed2 = Seed("127.0.0.1", 7001) 

peer1 = Peer("127.0.0.1", 8000)
peer1.start()

peer2 = Peer("127.0.0.1", 8001)
peer2.start()

peer3 = Peer("127.0.0.1", 8002)
peer3.start()

peer4 = Peer("127.0.0.1", 8003)
peer4.start()

peer5 = Peer("127.0.0.1", 8004)
peer5.start()

time.sleep(2)

peer1.connect_seed(seed1.host, seed1.port)
time.sleep(1)
# for peer in peer1.peers:
#     peer1.connect(peer[0], peer[1])
peer2.connect_seed(seed1.host, seed1.port)
time.sleep(1)

peer3.connect_seed(seed1.host, seed1.port)
time.sleep(1)

peer4.connect_seed(seed1.host, seed1.port)
time.sleep(1)
for peer in peer4.peers:
    peer4.connect(peer[0], peer[1])
time.sleep(1)

peer5.connect_seed(seed1.host, seed1.port)
time.sleep(1)
for peer in peer5.peers:
    peer5.connect(peer[0], peer[1])
time.sleep(1)

for peer in peer1.peers:
    print(peer)
for peer in peer1.connected:
    print(peer[0], peer[1], peer[2])


print("Peer 1")

for peer in peer4.connected:
    print(peer[0], peer[1], peer[2])


time.sleep(40)
peer1.close_socket()
print("Peer 1 closed")
