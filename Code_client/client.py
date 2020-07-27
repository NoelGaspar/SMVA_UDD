"""
SMVA-Server code testing


"""
import socketio
import time

SERVER_IP_ADDR = '192.168.0.9'
sio = socketio.Client()
cnt = 0

def send_data():
  sio.emit('my_message',{'data':cnt})
  while cnt<1000:
    sio.emit('my_message',{'data':cnt})
    cnt+=1


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