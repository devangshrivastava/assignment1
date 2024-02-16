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
    peer2.connect(seed1.host, seed1.port)
    time.sleep(1)
    peer3.connect(seed1.host, seed1.port)
    time.sleep(1)
    peer4.connect(seed1.host, seed1.port)
    time.sleep(1)
    print(peer3.peers)
    print("done")


except KeyboardInterrupt:
    print("Shutting down...")
    print("Goodbye!")

