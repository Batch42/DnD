from socket import *
import hashlib
from threading import Thread

password = 'mattisfat'
client = socket(AF_INET, SOCK_DGRAM)
server = socket(AF_INET, SOCK_DGRAM)
addr = None
window_=None

def send(message):
    global client
    global addr
    print(message)
    client.sendto((hashlib.md5((password+message).encode()).hexdigest()+'\n'+message).encode(),addr)
def listen():
    global server
    global window_
    while(True):
        message,addr = server.recvfrom(1024)
        message = message.decode()
        print(message)
        body=''
        code = message.split('\n')[0]
        if len(message.split('\n'))>1:
            for s in message.split('\n')[1:]:
                body+=s+'\n'
            body=body[:-1]
            if hashlib.md5((password+body).encode()).hexdigest() == code:
                window_.recv(body.split('\n'))

def initnet(port,window):
    global window_
    global server
    global addr
    addr = ('138.78.102.89',port)
    window_=window
    server.bind(('', 0))
    greeting='hello\n'+server.getsockname()[0] +'\n'+str(server.getsockname()[1]) +'\n' + window_.name)
    send(greeting)
    t=Thread(target=listen)
    t.start()
    

