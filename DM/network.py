from socket import *
import hashlib
from threading import Thread
from collections import defaultdict as dd

password = 'mattisfat'
client = socket(AF_INET, SOCK_DGRAM)
server = socket(AF_INET, SOCK_DGRAM)
window_=None
fromlist = dd()
tolist = dd()

def send(message,name=None):
    global client
    global tolist
    if name == None:
        for key in tolist:
            print(key)
            client.sendto((hashlib.md5((password+message).encode()).hexdigest()+'\n'+message).encode(),tolist[key])
    else:
        client.sendto((hashlib.md5((password+message).encode()).hexdigest()+'\n'+message).encode(),tolist[name])
    
def listen():
    global server
    global window_
    global tolist
    global fromlist
    while(True):
        message,addr = server.recvfrom(1024)
        message = message.decode()
        body=''
        code = message.split('\n')[0]
        if len(message.split('\n'))>1:
            for s in message.split('\n')[1:]:
                body+=s+'\n'
            body=body[:-1]
            print(hashlib.md5((password+body).encode()).hexdigest() == code)
            print(password+body)
            print(code)
            if hashlib.md5((password+body).encode()).hexdigest() == code:
                body = body.split('\n')
                if body[0] == 'hello':
                    #new connections are established through:
                    #hello\nip\nport\nname
                    tolist[body[3]]=(addr[0],int(body[2]))
                    fromlist[addr]=body[3]
                    window_.recv(['load'],body[3])
                else:
                    window_.recv(body,fromlist[addr])

def initnet(window):
    global window_
    global server
    window_=window
    server.bind(('', 0))
    t=Thread(target=listen)
    t.start()
    return server.getsockname()[1]

