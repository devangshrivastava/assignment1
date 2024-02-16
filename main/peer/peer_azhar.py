data = "STORE-1234:45789"
host_port_str = data.split("-")[1]  
host, port = host_port_str.split(":") 
print(host, port)