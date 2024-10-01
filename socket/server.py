import socket
network_type=socket.SOCK_DGRAM #udp
address_family = socket.AF_INET

server=socket.socket(address_family,network_type)

server.bind(("10.1.1.204",4321))

data=server.recvfrom(1024)
print(data)