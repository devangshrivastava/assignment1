import config_file
from seed import Seed

active_seed=[]
seed_info = config_file.seed_info

def start_seed():
    for i in seed_info.values():
        print("Starting seed node with :", i, ".....")
        s = Seed(i[0],i[1])
        s.start()

        active_seed.append(s)


if __name__ == '__main__':
    start_seed()