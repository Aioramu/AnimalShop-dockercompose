import sys
from socket import *
sHOST='localhost'
sPORT=8090
message=[b'Hello']
sockobj=socket(AF_INET,SOCK_STREAM)
sockobj.connect((sHOST,sPORT))
for line in message:
    sockobj.send(line)
    data=sockobj.recv(1024)
    print('Client recived:',data)
sockobj.close()
