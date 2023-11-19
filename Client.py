import socket

HEADER = 64 # 64 bytes contain metadata of message
FORMAT = 'utf-8' #encoding format
DISCONNECT_MESSAGE = "DISCONNECT" #disconection msg
SERVER_IP = "127.0.1.1" #server ip input("Enter Server IP")
PORT = 5050 #port number int(input("Enter Port"))
ADDR = (SERVER_IP,PORT) #complete address with port no
MSG_RETRY_COUNT = 5 #in case of failure sending msg again and again
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #establishing client
client.connect(ADDR) #connecting to server

def send(msg): #ending msg to server
    fail_to_send = True
    while( fail_to_send and MSG_RETRY_COUNT > 0 and isConnected()):
        message = msg.encode(FORMAT) #encoding the message
        msg_length = str(len(message)) #geting msg length
        msg_length += ' ' * (HEADER - len(msg_length))#padding eith space to create 64 byte msg
        msg_length = msg_length.encode(FORMAT) #encoding lengthof message
        client.send(msg_length)#send metadta of msg
        client.send(message)#sending msg
        if(client.recv(2048).decode(FORMAT) == str(len(message))):#get reply of how much data recived
            fail_to_send = False
            print("[SENT]")
        MSG_RETRY_COUNT -= 1
    if(MSG_RETRY_COUNT == 0):
        print("[FAILURE] [Fail To Send Message]")

def isConnected():#continusly checks connection of server and cient
    return True

def start():
    print(f"[Send '{DISCONNECT_MESSAGE}' for disconnect]")
    while True:
        MESSAGE = input(">>> ")
        send(MESSAGE)
        if(MESSAGE == DISCONNECT_MESSAGE):
            break

#message area
start()#start client