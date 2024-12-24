import socket
import os
import threading

PORT = 9966
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(client_socket):
    request_data = client_socket.recv(2048).decode('utf-8')
    print(f"Received request:\n{request_data}\n\n") 
    request_line = request_data.split('\r\n')[0] 
    _, request_path, _ = request_line.split(' ') 
    response = handle_request(request_path, client_socket.getpeername())
    client_socket.sendall(response)
    client_socket.close()


def handle_request(request,client_address):
    file_path_mapping = {
        '/': 'main_en.html',
        '/en': 'main_en.html',
        '/main_en.html': 'main_en.html',
        '/ar': 'main_ar.html',
    }

    content_types = {
        ".html": "text/html",
        ".css": "text/css",
        ".png": "image/png",
        ".jpg": "image/jpeg",
    }

    redirects = {
        '/cr': 'http://cornell.edu',
        '/so': 'http://stackoverflow.com',
        '/rt': 'http://ritaj.birzeit.edu',
    }

    if request in redirects:
        location = redirects[request]
        response = f"HTTP/1.1 307 Temporary Redirect\r\nLocation: {location}\r\n\r\n"
        return response.encode()

    if request in file_path_mapping:
        file_path = file_path_mapping[request]
    else:
        file_path = request[1:]

    if os.path.isfile(file_path):
        _, file_extension = os.path.splitext(file_path)
        content_type = content_types.get(file_extension, "application/octet-stream")
        with open(file_path, 'rb') as file:
            content = file.read()
        return f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode() + content
        
    return f"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n".encode() + get_error_html(client_address)


def get_error_html(client_address):
    with open("error.html", "r") as error_file:
        error_html_content = error_file.read()
    error_html_content = error_html_content.replace("[Client IP and Port]", f"{client_address[0]}:{client_address[1]}")
    
    return error_html_content.encode()


def start():
    server.listen() 
    print(f"Server listening on port {PORT}...")
    print()
    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, ))
        thread.start()

start()
