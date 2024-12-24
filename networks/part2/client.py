import socket

PORT = 9955
SERVER = socket.gethostbyname(socket.gethostname())
HEADER = 64
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
DISCONNECT_MSG = "!disconnect!"
VALID_STUDENT_IDS = ["1212028","1210260"]


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive():
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        print(f"[SERVER]: {msg}")


while True:
    user_input = input(f"Enter a student ID (or type {DISCONNECT_MSG} to close): ")
    send(user_input)
    receive()

    if user_input == DISCONNECT_MSG or user_input in VALID_STUDENT_IDS:
        break
