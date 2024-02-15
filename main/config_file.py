import argparse

seed_info={"seed_1":('127.0.0.1',6000),"seed_2":('127.0.0.1',6001),"seed_3":('127.0.0.1',6002),"seed_4":('127.0.0.1',6003)}

count=len(seed_info)

# def main():
    
#     global seed_info,count
    
#     parser = argparse.ArgumentParser(description="Simple Argument Parser Example")

    
#     parser.add_argument('-ip', '--host_ip', type=str, help='IP to bind the seed')
#     parser.add_argument('-port', '--port', type=int, help='Port number to bind upon')
#     parser.add_argument('-remove', '--remove', type=str, help='seed to remove from the list , mention the seed name to remove')
#     args = parser.parse_args()
    
#     IP = args.host_ip
#     PORT = args.port
#     remove = args.remove

#     print("before:",seed_info)
    
    
#     if not remove:
#         count+=1

#         seed_info["seed_"+str(count)] = tuple((IP,PORT))

#     if remove:
#         try:
#             seed_info= seed_info.pop(remove)

#         except KeyError as e:
#             print("key dsnt exists:", e)
#     print("after: ",seed_info)

# if __name__ == "__main__":

#     main()