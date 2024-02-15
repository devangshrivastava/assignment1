from seed import start_seed


seed_nodes = start_seed.start_seed()
for node in seed_nodes:
    print(node.soc)

