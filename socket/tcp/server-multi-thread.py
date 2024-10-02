import socket
import threading
server=socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

port=4321
ip=''
server.bind((ip,port))

server.listen()

def sock_fun(csession,addr):
    print(addr)
    data=csession.recv(1024)
    csession.send(b"Hi I am from server")
    print(data)


while True:
    csession,addr=server.accept()
    t1=threading.Thread(target=sock_fun,args=(csession,addr))
    t1.start()