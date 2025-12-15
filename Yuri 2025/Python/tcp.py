import socket
import sys
import json


class TCP():
    #hostname=socket.gethostname()
    #IPAddr=socket.gethostbyname(hostname)
    host = 
    port = 5065
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET for IPv4, SOCK_STREAM as Stream socket for tcp/ip
    address = (host, port)
    def __init__(self):
        self.sock.connect(self.address)
        print("Connected to address:", self.host + ":" + str(self.port))
    
    def neutral(self):
        self.sock.sendall("Neutral".encode("utf-8"))
    
    def interested(self):
        self.sock.sendall("Interested".encode("utf-8"))

    def cry(self):
        self.sock.sendall("Sad".encode("utf-8"))

    def blush(self):
        self.sock.sendall("Sensitive".encode("utf-8"))

    def surprised(self):
        self.sock.sendall("Surprised".encode("utf-8"))
    
    def bad(self):
        self.sock.sendall("Bad".encode("utf-8"))

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

    def send_to_Unity(self, emotion, mp3path):
        payload = {
        "type": "tts",
        "emotion": emotion,
        "mp3path": mp3path
        }

        message = json.dumps(payload) + "\n" 
        self.sock.sendall(message.encode("utf-8"))
