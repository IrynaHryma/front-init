import socket
import json
from datetime import datetime

UDP_IP = '127.0.0.1'
UDP_PORT = 5000

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((UDP_IP, UDP_PORT))
    
    while True:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode()
        if message.lower().strip() == "exit":
            break
        save_message(message)
        response = "Message received and stored."
        server_socket.sendto(response.encode(), addr)

    server_socket.close()

def save_message(message):
    timestamp = str(datetime.now())
    data = {
        "username": "example_username",
        "message": message
    }
    with open("storage/data.json", "a") as json_file:
        json.dump({timestamp: data}, json_file, indent=2)
        json_file.write("\n")

if __name__ == "__main__":
    main()
