from peer import Peer
import signal
import sys
import time
import random

# Create signal handler function
def signal_handler(sig, frame):
    print('Exiting...')
    # node1.close_connections()
    # node2.close_connections()
    sys.exit(0)

# Register signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Create two peers
try:

    given_node = Peer("0.0.0.0", 7000)
    given_node.start()
    nodes = []
    for port in range(8000, 8006):
        node = Peer("0.0.0.0", port)
        nodes.append(node)  

    for node in nodes:
        node.start()
    time.sleep(2) # Give some time for nodes to start listening

    selected_nodes = random.sample(nodes, 4)

    for node in selected_nodes:
        node.connect("127.0.0.1",given_node.port)
        time.sleep(1)
        given_node.connect("127.0.0.1",node.port)
        time.sleep(1)

    input("Press Enter to send data...")
    while True:
        time.sleep(1)
        a = input("Enter node number: ")
        m = input("Enter message: ")
        # if a == "1":
        #     node1.send_data(m)
        # elif a == "2":
        #     node2.send_data(m)
        # else:
        #     print("Invalid input")
        #     break
        
        b = input("Do you want to continue? (yes/no): ")
        if b == "no":
            break
        elif b == "yes":
            continue
        else:
            print("Invalid input")
            break
        
    
    for node in nodes:
        node.close_connections()
    given_node.close_connections()
    # node1.close_connections()
    # node2.close_connections()






except KeyboardInterrupt:
    print('Interrupted by user. Closing connections...')
    # node1.close_connections()
    # node2.close_connections()
