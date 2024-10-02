import socket

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("10.1.1.127",2345))
client.send(b"hi from client")
client.recv(1024)