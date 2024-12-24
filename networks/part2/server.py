import socket
import threading 
import time
import ctypes

PORT = 9955
SERVER = socket.gethostbyname(socket.gethostname())
HEADER = 64
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
DISCONNECT_MSG = "!disconnect!"
VALID_STUDENT_IDS = ["1212028","1210260"]

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn,addr):
    print(f"[NEW CONNECTION]{addr}connected")
    connected=True
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length=int(msg_length)
            msg=conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}]{msg}")
            if msg==DISCONNECT_MSG:   
                connected=False
            elif msg in VALID_STUDENT_IDS:
                print(f"[{addr}] Valid student ID received. Locking screen in 10 seconds.")
                send("Locking screen in 10 seconds.", conn)
                time.sleep(10)
                lock_screen()
            else:
                print(f"[{addr}] Error: Invalid student ID received. No action taken.")
                send("Error: Invalid student ID. No action taken.", conn)
    conn.close()

def send(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def start():
    server.listen()
    while True:
        conn,addr=server.accept()
        thread=threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]{threading.active_count()-1}")

def lock_screen():
    ctypes.windll.user32.LockWorkStation()
    print("Screen locked.")

print("[STARTING]server is starting...")
start()

