import tornado, json

class Client():
    __update_system = None
    nik_name = "Gost"
    isConect = True

    def __init__(self, addr, socket):
        
        self.__addr = addr
        self.__socket = socket
    
    def set_update_system(self, sys):
        
        self.__update_system = sys
    
    def set_nik_name(self, name):

        self.nik_name = name
    
    def get_addr(self):
        return self.__addr
    
    async def fire_client(self, mess):

        await self.__socket.write((json.dumps(mess) + "\n").encode())
    
    async def run_loop(self):

        while True:
            data = await self.__socket.read_until(b"\n")

            if not data:
                break

            message = json.loads(data.decode().strip())

            resp = await self.__update_system.update(message, self)

            await self.__socket.write((json.dumps(resp) + "\n").encode())
    
    def remove_player(self):

        self.__update_system.remove_player(self)
