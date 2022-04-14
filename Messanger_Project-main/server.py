import socket
import threading
import os
from os import listdir
from os.path import join, isfile

HOST = '127.0.0.1'
PORT = 50002
BUFFERSIZE =2048
Data = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind(Data)

server.listen()

clients = []
nickNames = []


class udpPORT:
    def __init__(self, available, client_address, sock):
        self.available = available
        self.client_address = client_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class udpPORTS:
    def __init__(self):
        self.portsList = {port: udpPORT(False, None, None) for port in range(55000, 55016)}


    def getAvailablePort(self):
        for elem in self.portsList.items():
            if not elem[1].available and elem[1].client_address is None:
                return elem[0]
        return None


portList = udpPORTS()


def sendFile(sockUDP, filename, client_address):
    with open(filename, "rb") as file:
        dataList = []
        ackList = []
        while True:
            bytes_read = file.read(BUFFERSIZE)
            dataList.append(bytes_read)
            if not bytes_read:
                break

        packetNum =0
        while packetNum < len(dataList)-1:

            sockUDP.sendto(dataList[packetNum], client_address)


            try:
                sockUDP.settimeout(0.1)
                ack , _ = sockUDP.recvfrom(10)
                packetNum+=1


            except:
                print("Tryin again !")


def broadCast(message):

    if bool(nickNames):
        print(len(clients))
        for client in clients:
            client.send(message)


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        client.send("NICK".encode())
        nickName = client.recv(1024)
        print(nickName)
        nickNames.append(nickName.decode())
        clients.append(client)
        print(f"Nickname of the client is : {nickName}")
        broadCast(nickName + " joined to the chat!\n".encode())
        client.send("Connected to the server !\n".encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def handle(client):
    while True:
        # try:
            case1 = False
            case2 = False
            message = client.recv(1024)
            print(message)
            msgstring = str(message)
            msgstring = msgstring.split(" ")
            print(msgstring)
            if len(msgstring) > 1 :
                private = msgstring[2]
                if private[0] == '/':
                    destName = private[1:]
                    if destName == 'download':
                        filename = msgstring[3]
                        destFileName = msgstring[4]
                        destFileName = destFileName[0:-3]
                        files = os.listdir(r'../Messanger_Project')
                        if filename not in files:
                            client.send(f"ERROR : {filename} is not exists !".encode())
                            case2 = True
                        else:
                            port = portList.getAvailablePort()
                            portList.portsList[port].sock.bind((socket.gethostbyname(socket.gethostname()), port))
                            portList.portsList[port].available = True
                            client.sendall(f"/download {socket.gethostbyname(socket.gethostname())} {port} {destFileName} {os.path.getsize(filename)}".encode())
                            msg, client_address = portList.portsList[port].sock.recvfrom(4096)
                            portList.portsList[port].client_address = client_address
                            sendFile_thread = threading.Thread(target=sendFile, args=[portList.portsList[port].sock, filename, client_address])
                            sendFile_thread.start()
                            # sendFile(portList.portsList[port].sock, filename, client_address)
                            case2 = True
                            print(f"[RECIEVED] : {msg}: {client_address}")

                            '''$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'''
                    elif str(destName) not in nickNames:
                        client.send("This user is not online! \n".encode())
                        case1 = True
                    else:
                        index = nickNames.index(str(destName))
                        privateMsg = message.decode()
                        privateMsg = str(privateMsg)
                        privateMsg = privateMsg.split(" ")
                        print(privateMsg)
                        del privateMsg[0:3]
                        privateMsg = " ".join(privateMsg)
                        privateMsg = str(privateMsg)
                        test = f"{nickNames[clients.index(client)]} [PRIVATE] : " + privateMsg
                        dest = clients[index]
                        dest.send(test.encode('utf-8'))
                        client.send((f"Sent to {destName} [PRIVATE]: " + privateMsg).encode())
                        case1 = True
            if message == 'get_users'.encode():
                something = "SERVER MESSAGE ! \n----------- \nOnline members : \n"
                for nick in nickNames:
                    something += nick   + "\n"
                something += "----------- \n"
                client.send(something.encode())
                case2 = True

            if message == 'show_files'.encode():
                path = r'../Messanger_Project'
                filesListstr = "SERVER MESSAGE ! \n----------- \nFiles avaible : \n"
                onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
                files = os.listdir(path)
                for f in files:
                    filesListstr += f"{f} \n"
                filesListstr += "----------- \n"
                client.send(filesListstr.encode())
                case2 = True

            if len(msgstring) > 1 and msgstring[1] == "has":  # discconect
                temp = msgstring[0]
                temp = temp[2:]

                client.close()
                clients.remove(client)
                message += "\n".encode()
                broadCast(message)
                nickNames.remove(temp)
                break

            if case1 == False and case2 == False:
                broadCast(message)



print("Server is running...")
receive()

