import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.connect(("127.0.0.1", 8888))

while True:

    rec = input() + "\n"

    soc.sendall(rec.encode())

    print(soc.recv(1024).decode())