from ssl import SSLContext
import tornado.ioloop
import tornado.iostream
import tornado.tcpserver

import components.clientModul, components.Router

class CoreTCPServer(tornado.tcpserver.TCPServer):

    __client_list = {}
    __room_list = []

    __router = components.Router.Router()

    async def handle_stream(self, stream, address):

        self.__client_list[f"{str(address[0])}:{str(address[1])}"] = {}

        client = components.clientModul.Client(address, stream)
        client.set_update_system(self.__router)
        
        try:
            await client.run_loop()
        except tornado.iostream.StreamClosedError:
            del self.__client_list[f"{str(address[0])}:{str(address[1])}"]

            client.remove_player()

def run_server(ip, port):
    server = CoreTCPServer()
    server.listen(port, ip)

    print(f"[\033[34m INFO \033[0m]Server started:\n IP:{ip}\n   PORT:{port}")

    tornado.ioloop.IOLoop.current().start()