from seed import start_seed
from peer.peer import Peer
import random
import time

seed_nodes = start_seed.start_seed()

given_node = Peer("0.0.0.0", 7000)
given_node.start()
time.sleep(1)

selected_nodes = random.sample(seed_nodes, (len(seed_nodes)//2 + 1))

for node in selected_nodes:
    given_node.connect_to_seed(node.ip, node.port)
    
