from ssl import SSLContext
import tornado.ioloop
import tornado.iostream
import tornado.tcpserver

import components.clientModul

class MyTCPServer(tornado.tcpserver.TCPServer):

    async def handle_stream(self, stream, address):
        print("New connection from:", address)  # Выводим информацию о новом подключении

        client = components.clientModul.Client(address, stream)

        await client.run_loop()

def run_server(ip, port):
    server = MyTCPServer()
    server.listen(port, ip)

    print(f"[\033[34m INFO \033[0m]Server started:\n IP:{ip}\n   PORT:{port}")

    tornado.ioloop.IOLoop.current().start()