"""
SMVA-Server code testing
https://python-socketio.readthedocs.io/en/latest/

"""
import socketio
import time

SERVER_IP_ADDR = '192.168.0.8'
sio = socketio.Client()

def send_data():
  cnt = 0
  sio.emit('my_message',{'data':cnt})
  while True:
    while cnt<10:
      sio.emit('my_message',{'data':cnt})
      cnt+=1
    cnt=0	    
    sio.sleep(5)


@sio.event
def connect():
    print('connection established')
    sio.start_background_task(send_data)

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://'+SERVER_IP_ADDR+':5000')
#sio.wait()
