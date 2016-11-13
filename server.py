

#SERVER

import socket, time, json, os

os.system("clear")
host = raw_input("Enter Your IP: ")
port = input("Enter Port: ")
worldName = raw_input("Enter Path to Worldfile: ")


def fromFile(file):
    worldFile = open(file,'r')
    array = json.load(worldFile)
    worldFile.close()
    return array

def sendToAll(addr, data, sock):
    for client in clients:
        if addr != client:
            sock.sendto(data, client)

def Login(addr,sock):
    clients.append(addr)
    sock.sendto(addr, json.dumps(clients))


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
            quitting = True
        if "Hello!" in str(data):
            Login(addr,s)
        sendToAll(addr,data,s)
    except:
        raise
s.close()
