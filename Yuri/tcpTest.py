import socket
import sys
import time

hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
host = IPAddr
port = 5065

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET for IPv4, SOCK_STREAM as Stream socket for tcp/ip

address = (host, port)

data = "1,2,3"  #test data

check = 0


sock.connect(address)
print("Connected to address:", socket.gethostbyname(socket.gethostname()) + ":" + str(port))

while True:
    check = int(input()) 
    if check == 0: 
        data = "0,2,3"
        check += 1
    elif check == 1:
        data = "1,2,3"
        check += 1
    elif check == 2:
        data = "2,2,3"
        check += 1
    elif check == 3:
        data = "3,2,3"
        check += 1
    elif check == 4:
        data = "4,2,3"
        check += 1
    elif check == 5:
        data = "5,2,3"
        check += 1
    elif check == 6:
        data = "6,2,3"
        check = 0
    
    
    print(data)
    sock.sendall(data.encode("utf-8")) #tcp can only transfer byte so need to encode
    print(socket.gethostname())
    
    # response = sock.recv(1024).decode("utf-8")
    # print(response)
    # time.sleep(10)

# try:
#     sock.connect(address)
#     print('hi1')
#     print("Connected to address:", socket.gethostbyname(socket.gethostname()) + ":" + str(port))
#     print('hi2')
#     sock.sendall(data.encode("utf-8")) #tcp can only transfer byte so need to encode
#     print('hi3')
#     # response = sock.recv(1024).decode("utf-8")
#     print('hi4')
#     # print(response)

# finally:
#     sock.close()
# except OSError as e:
#     print("Error while connecting :: %s" % e)
    
#     # quit the script if connection fails (e.g. Unity server side quits suddenly)
#     sys.exit()


