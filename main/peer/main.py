from seeds.peer.peer import Peer
import signal
import sys
import time

# Create signal handler function
def signal_handler(sig, frame):
    print('Exiting...')
    node1.close_connections()
    node2.close_connections()
    sys.exit(0)

# Register signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Create two peers
try:
    node1 = Peer("0.0.0.0", 8000)
    node1.start()

    node2 = Peer("0.0.0.0", 8001)
    node2.start()

    # Give some time for nodes to start listening
    time.sleep(2)
    node2.connect("127.0.0.1", 8000)
    time.sleep(1)  # Allow connection to establish
    node1.connect("127.0.0.1", 8001)

    input("Press Enter to send data...")
    while True:
        time.sleep(1)
        a = input("Enter node number: ")
        m = input("Enter message: ")
        if a == "1":
            node1.send_data(m)
        elif a == "2":
            node2.send_data(m)
        else:
            print("Invalid input")
            break
        
        b = input("Do you want to continue? (yes/no): ")
        if b == "no":
            break
        elif b == "yes":
            continue
        else:
            print("Invalid input")
            break
        

    node1.close_connections()
    node2.close_connections()






except KeyboardInterrupt:
    print('Interrupted by user. Closing connections...')
    node1.close_connections()
    node2.close_connections()
