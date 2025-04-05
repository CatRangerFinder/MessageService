import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
CMD_DISCONNECT_MESSAGE = "!DISCONNECT!"
CMD_SERVER_ACK = "!Msg received!"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


# Handle client process
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == CMD_DISCONNECT_MESSAGE:
                connected = False

            print(f"[MESSAGE] Address= {addr} Msg= '{msg}' ")
            conn.send(CMD_SERVER_ACK.encode(FORMAT))

    conn.close()
    print(f"[DISCONNECTED] Address= {addr}")


# Server startup process
def startup():
    print(f"[STARTING] Server starting... \n[INFO] Local_IP= {SERVER} \n[INFO] Port= {PORT}")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print()


if __name__ == '__main__':
    startup()