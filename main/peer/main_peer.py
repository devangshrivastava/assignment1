from peer import Peer
import time

try:

    given_node = Peer("127.0.0.1", 7000)
    given_node.start()
    nodes = []
    for port in range(8000, 8006):
        node = Peer("127.0.0.1", port)
        nodes.append(node)  

    for node in nodes:
        node.start()
    time.sleep(2) # Give some time for nodes to start listening
    
    
    
    node1 = nodes[0]    
    for node in nodes:
        node.connect(given_node.host, given_node.port)
    

    for conn in given_node.connections:
        print(conn)
    

    input("Press Enter to send data...")
        
    
    for node in nodes:
        node.close_connections()
    given_node.close_connections()
    node1.close_connections()
    # node2.close_connections()
    
    

except KeyboardInterrupt:
    print("Shutting down...")
    for node in nodes:
        node.close_connections()
    given_node.close_connections()
    node1.close_connections()
    # node2.close_connections()/
    print("Goodbye!")