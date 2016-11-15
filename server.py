

#SERVER

import socket, time, json, os

os.system("clear")
#host = raw_input("Enter Your IP: ")
host = "127.0.0.1"
#port = input("Enter Port: ")
port = 5000
#worldName = raw_input("Enter Path to Worldfile: ")
worldName = "./Worlds/spawnIsland"


def fromFile(file):
    worldFile = open(file,'r')
    array = json.load(worldFile)
    worldFile.close()
    return array

def sendToAll(addr, data, sock):
    for client in clients:
        if addr != client:
            toSend = {"data": data, "addr": list(addr)}
            sock.sendto(json.dumps(toSend), client) #convert list into a tuple

def Login(addr,sock):
    clients.append(addr)


def Logout(addr):
    del clients[clients.index(addr)]

worldArray = fromFile(worldName)

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(True)

quitting = False
print "Server Started."
while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        print time.ctime(time.time()) + str(addr) + ": :" + str(data)
        if "Quit" in str(data):
            Logout(addr)
        if "Hello!" in str(data):
            Login(addr,s)
        sendToAll(addr,data,s)
    except:
        raise
s.close()
