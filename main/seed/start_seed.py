import config_file
import seed

active_seed=[]

for i in config_file.seed_info:
    s = seed(i[0],i[1])
    s.start()

    active_seed.append(s)

    
