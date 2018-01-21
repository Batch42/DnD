import network

window = None

def load(file):
    data = open(file).read()
    if file[-3:]=='map':
        i=0
        for line in data.split('\n'):
            j=0
            for c in line.split(','):
                network.send('MapCell\n'+str(j)+'\n'+str(i)+'\n'+c)
                j+=1
            i+=1
    elif file[-3:]=='ent':
        for line in data.split('\n'):
            network.send('Entity\n'+line.replace(',','\n'))
    else:
        print('Include a valid file extension')

def run():
    global window

    print(window.port)
    
    while True:
        command = input('>').split(" ")
        if command[0] == 'load':
            if len(command)>1:
                try:
                    load(command[1])
                except Exception as ex:
                    print('Load failed: '+str(ex))
            else:
                print('Enter a file name')
        
