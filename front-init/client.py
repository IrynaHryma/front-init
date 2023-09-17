import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 5000

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = input("--->")
    while message.lower().strip() != "exit":
        client_socket.sendto(message.encode(), (UDP_IP, UDP_PORT))
        message = input("--->")
    
    client_socket.close()

if __name__ == "__main__":
    main()

