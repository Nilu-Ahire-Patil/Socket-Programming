import socket
import threading

HEADER = 64 #64 bytes contain metadata of message
PORT = 5050 #port number
SERVER_NAME = socket.gethostname() #server name
SERVER_IP = socket.gethostbyname(SERVER_NAME) #gives server ip address by name
ADDR = (SERVER_IP,PORT) #complete address with port no
FORMAT = 'utf-8' #encoding format
DISCONNECT_MESSAGE = "DISCONNECT" #disconection mge
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #establishing server
server.bind(ADDR) #Binding address of the server

def handle_client(conn,addr): #handling the client
    print(f"[NEW CONNECTION] [{addr}]")

    connected = True #assume first we are connected successfully
    while connected and isConnected(conn,addr):
        msg_length = conn.recv(HEADER).decode(FORMAT) #trying to reciving metadata of message
        if msg_length:#check the msg is not empry
            msg_length = int(msg_length)#geting length of actual message

            msg = conn.recv(msg_length).decode(FORMAT)#tring to recive messaage of desire length
            if msg == DISCONNECT_MESSAGE:#check the msg contain disconnect code
                connected = False
                print(f"[DISCONNECT] [{addr}]")#informing about disconnection
            else:
                print(f"[{addr}]\t: {msg}") #printing the message get from client
            conn.send(f"{len(msg)}".encode(FORMAT))#send conformation of msg recived
    #print(f"[DISCONNECT] [{addr}]")
    conn.close() #closing the connection
    get_active_connection(1)

def get_active_connection(running_thread = 0):
    print(f"[ACTIVE CONNECTIONS] [{threading.active_count() - 1 - running_thread}]")#print total connection count

def isConnected(conn,addr):#continusly checks connection of server and cient
    return True

def start(): #start new connection
    print("[SERVER START]")
    server.listen()#start server
    print(f"[LISTENING] [{SERVER_IP} {SERVER_NAME}]")
    while True:
        conn , addr = server.accept() #getting address of client
        thread = threading.Thread(target=handle_client,args=(conn,addr))# create thread per client
        thread.start()#start communication with client
        get_active_connection()#get connection count

#message area
start()#stert server