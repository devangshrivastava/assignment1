from seed.devang_seed import Seed
from peer.peer import Peer 
import time

try:
    seed1 = Seed("127.0.0.1", 7000)
    seed1.start()
    seed2 = Seed("127.0.0.1", 7001)
    seed2.start()

    peer1 = Peer("127.0.0.1", 8000)
    peer1.start()
    peer2 = Peer("127.0.0.1", 8001)
    peer2.start()
    peer3 = Peer("127.0.0.1", 8002)
    peer3.start()
    peer4 = Peer("127.0.0.1", 8003)
    peer4.start()

    time.sleep(2)
    peer1.connect(seed1.host, seed1.port)
    time.sleep(1)
    # for peer in peer1.peers:
        # peer1.connect(peer[0], peer[1])
    
    peer2.connect(seed1.host, seed1.port)
    time.sleep(1)
    # for peer in peer2.peers:
    #     peer2.connect(peer[0], peer[1])
    
    peer3.connect(seed1.host, seed1.port)
    time.sleep(1)
    # for peer in peer3.peers:
    #     peer3.connect(peer[0], peer[1])
    
    peer4.connect(seed1.host, seed1.port)
    time.sleep(1)
    for peer in peer4.peers:
        peer4.connect(peer[0], peer[1])
    
    seed1.send_data("Hello")
    time.sleep(2)
    peer1.send_data("MESSAGE Hello")

    for conn in peer1.connections:
        print(conn)
    
    



except KeyboardInterrupt:
    print("Shutting down...")
    print("Goodbye!")

