Peer-to-Peer Messaging System
Group : Devang Srivastava (B21CS024), Azhar khan (B21CS087)

This project implements a simple peer-to-peer messaging system using Python. It consists of two main components:

    Seed nodes: Serve as central points for initial peer discovery and provide stability to the network.
    Peer nodes: Communicate with each other to exchange messages.

Key features:

    Seed nodes can be configured in a separate file for easy scaling.
    Random peer selection adds dynamism to the network connections.
    Messages are secured using hash-based duplication checks.
    Seed nodes are informed about removed peers to maintain network consistency.

Running the system:

    Clone this repository.
    Ensure you have Python and its dependencies installed (socket, threading, datetime, hashlib).
    Place the seed node information in a file named config_file.py with the following format:


    seed_info = {
        "seed_1": ("127.0.0.1", 12345),
        "seed_2": ("127.0.0.1", 54321),
        "seed_name": ("host_ip", "host_port)
    }

Use code with caution.

    Run main.py to start the seed nodes and peer nodes.

    Observe the output messages to understand the connections, message flow, and network dynamics.

    The output Log files with the name Log_{port}.txt will be displaying the specified detail.

    The Log file contains the network flow witht he specified data time stamps.

    Use Ctrl+C to gracefully shut down the system.

Understanding the code:

    seed.py: Defines the Seed class responsible for starting and managing seed nodes.
    peer.py: Defines the Peer class responsible for starting and managing peer nodes, handling connections, and message exchange.
    main.py: The main entry point, starting seed and peer nodes, sending messages, and demonstrating functionalities.

Further development:

    Implement more complex message types (e.g., group messages, private messages).
    Enhance fault tolerance and network resilience.
    Integrate security measures like encryption and authentication.
    Explore message routing algorithms for efficient message delivery.

This project provides a basic framework for peer-to-peer messaging. Feel free to explore and expand upon it to build more advanced and robust communication systems!