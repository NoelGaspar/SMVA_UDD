"""
SMVA-Server code testing
using socketio. 
https://python-socketio.readthedocs.io/en/latest/
"""
import eventlet
import socket
from datetime import datetime

PORT = 777
BUFF_SIZE = 1024


server_socket = socket.socket()

print("\n Server is listing on port:",PORT,"\n")

server_socket.bind(('',PORT))
server_socket.listen(10)

rcv_filename = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")+".csv"
rcv_file = open(rcv_filename,"a+")
print("\n Copied file will be recived be ",rcv_filename," at server side")

while True:
  myconn,addr_conn = server_socket.accept()
  msg = "\n Hi Client [IP address:"+addr_conn[0]+"]"
  myconn.send(msg.encode())
  print("reciving data")
  RecivedData = myconn.recv(BUFF_SIZE).decode()
  print(RecivedData)
  while RecivedData:
    print("writing data")
    rcv_file.write(RecivedData)
    print("reciving another bounch of data")
    RecivedData = myconn.recv(BUFF_SIZE).decode()
    print(RecivedData)

  rcv_file.close()
  print("\n File has been copied successfully \n")
  
  myconn.close()
  print("\n Server closed the connection \n")

  break

