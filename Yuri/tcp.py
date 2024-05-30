import socket
import sys


class TCP():
    hostname=socket.gethostname()
    IPAddr=socket.gethostbyname(hostname)
    host = IPAddr
    port = 5065
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET for IPv4, SOCK_STREAM as Stream socket for tcp/ip
    address = (host, port)
    def __init__(self):
        self.sock.connect(self.address)
        print("Connected to address:", socket.gethostbyname(socket.gethostname()) + ":" + str(self.port))
    
    def neutral(self):
        self.sock.sendall("0".encode("utf-8"))
    
    def interested(self):
        self.sock.sendall("1".encode("utf-8"))

    def cry(self):
        self.sock.sendall("3".encode("utf-8"))

    def blush(self):
        self.sock.sendall("4".encode("utf-8"))

    def surprised(self):
        self.sock.sendall("5".encode("utf-8"))
    
    def bad(self):
        self.sock.sendall("6".encode("utf-8"))

    def emotion(self, emotion):
        match emotion:
            case "Neutral":
                self.neutral()
            case "Interested":
                self.interested()
            case "Sad":
                self.cry()
            case "Sensitive":
                self.blush()
            case "Surprised":
                self.surprised()
            case "Bad":
                self.bad()
