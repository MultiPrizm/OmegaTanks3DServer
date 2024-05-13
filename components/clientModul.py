import tornado

class Client():
    __update_system = None

    def __init__(self, addr, socket):
        
        self.__addr = addr
        self.__socket = socket
    
    def set_update_system(self, sys):
        
        self.__update_system = sys
    
    async def run_loop(self):

        a = "200"

        while True:
            try:
                data = await self.__socket.read_until(b"\n")  # Читаем данные из потока до символа конца строки
                if not data:
                    print("Connection closed by:", self.__addr)  # Если данные пустые, значит соединение закрыто
                    break
                message = data.decode().strip()  # Декодируем данные и убираем символы перевода строки и пробелы
                print(f"Received message from {self.__addr}: {message}")  # Выводим полученное сообщение в консоль

                if message == "1":
                    await self.__socket.write(a.encode())
                else:
                    a = message
                    await self.__socket.write("200".encode())
                
            except tornado.iostream.StreamClosedError:
                print("Connection closed by:", self.__addr)  # Если возникает ошибка закрытия потока, выводим информацию
                break