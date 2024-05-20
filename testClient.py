import socket, json

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.connect(("127.0.0.1", 8888))
print("connected")

while True:

    rec = {}

    rec["type"] = input("type")
    rec["name"] = input("name")
    #rec["body"] = input("body")
    rec["body"] = {}

    rec = json.dumps(rec) + "\n"

    soc.sendall(rec.encode())

    res = soc.recv(1024).decode()

    print(json.loads(res))