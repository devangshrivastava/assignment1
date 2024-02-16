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
    peer1.connect_seed(seed1.host, seed1.port)
    time.sleep(1)
    # for peer in peer1.peers:
        # peer1.connect(peer[0], peer[1])
    
    peer2.connect_seed(seed1.host, seed1.port)
    time.sleep(1)
    # for peer in peer2.peers:
    #     peer2.connect(peer[0], peer[1])
    
    peer3.connect_seed(seed1.host, seed1.port)
    time.sleep(1)
    # for peer in peer3.peers:
    #     peer3.connect(peer[0], peer[1])
    
    peer4.connect_seed(seed1.host, seed1.port)
    time.sleep(1)
    for peer in peer4.peers:
        peer4.connect(peer[0], peer[1])
    
    seed1.send_data("Hello")
    time.sleep(2)
    peer1.send_data("MESSAGE Hello")
    time.sleep(1)
    for conn in peer4.connections:
        print(conn)
    print(len(peer1.connections))

    for conn in peer4.connected:
        print(conn[0], conn[1], conn[2])
    
    # for conn in peer1.connected:
    #     print(conn[0], conn[1], conn[2])    

    print(len(peer1.messages))
    for msg in peer4.messages:
        print(msg.message)
        print(msg.sent_to)
        print(msg.received_from)

except KeyboardInterrupt:
    print("Shutting down...")
    print("Goodbye!")

