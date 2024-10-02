import socket
import threading
server=socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

port=4321
ip=''
server.bind((ip,port))

server.listen()

def recv_fun(csession,addr):
  while True:
    data=csession.recv(1024)
    client_name=addr[0]
    global client_data
    client_data=data.decode()
    #message="Hi I am from server"
    #final_message=client_name + " : " + message
    #csession.send(final_message.encode())
    print(client_data)


while True:
    csession,addr=server.accept()
    t1=threading.Thread(target=recv_fun,args=(csession,addr))
    t1.start()
