import socket

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(("0.0.0.0",2345))

server.listen()

info,addr=server.accept()

data=info.recv(1024)
print(data)

info.send(b"hi i m server")