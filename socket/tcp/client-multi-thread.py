import socket
client=socket.socket()
client.connect(("3.239.63.156",4321))
client.send(b"Hi I am from client b")
client.recv(1024)