from socket import *
HOST=''
PORT=8090
sockobj=socket(AF_INET,SOCK_STREAM)
sockobj.bind((HOST,PORT))
sockobj.listen(5)


while True:
    connection,adress=sockobj.accept()
    print('Connected to:',adress)
    while True:
        data=connection.recv(1024)
        if not data: break
        connection.send(b'Echo '+data)

    connection.close()
