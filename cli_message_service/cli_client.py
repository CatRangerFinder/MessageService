import socket
#import threading


HEADER = 64
PORT = 5050
SERVER = "192.168.0.10"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
CMD_DISCONNECT_MESSAGE = "!DISCONNECT!"
CMD_SERVER_MSG_ACK = "!Msg received!"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def msg_handler(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    server_msg = client.recv(2048).decode(FORMAT)

    if server_msg == CMD_SERVER_MSG_ACK:
        print("Sent!")



def start():

    msg = str(input("message: "))
    msg_handler(msg)



if __name__ == '__main__':
    start()