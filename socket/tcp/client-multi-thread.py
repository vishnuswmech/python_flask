import socket
import threading
client=socket.socket()
client.connect(("",4321))



def recv(client):
 data = client.recv(1024)
 print(data.decode())
   

def send(client):
 name=input("Enter your name:")
 while True:
  mes=input()
  data=name + ":" + mes
  client.send(data.encode())

send_thread=threading.Thread(target=send,args=(client,))
recv_thread=threading.Thread(target=recv,args=(client,))
send_thread.start()
recv_thread.start()


