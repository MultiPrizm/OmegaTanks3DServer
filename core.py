from ssl import SSLContext
import tornado.ioloop
import tornado.iostream
import tornado.tcpserver

class MyTCPServer(tornado.tcpserver.TCPServer):

    async def handle_stream(self, stream, address):
        print("New connection from:", address)  # Выводим информацию о новом подключении

        a = "200"
        while True:
            try:
                data = await stream.read_until(b"\n")  # Читаем данные из потока до символа конца строки
                if not data:
                    print("Connection closed by:", address)  # Если данные пустые, значит соединение закрыто
                    break
                message = data.decode().strip()  # Декодируем данные и убираем символы перевода строки и пробелы
                print(f"Received message from {address}: {message}")  # Выводим полученное сообщение в консоль

                if message == "1":
                    await stream.write(a.encode())
                else:
                    a = message
                    await stream.write("200".encode())
                
            except tornado.iostream.StreamClosedError:
                print("Connection closed by:", address)  # Если возникает ошибка закрытия потока, выводим информацию
                break

def run_server(ip, port):
    server = MyTCPServer()
    server.listen(port, ip)

    print(f"[\033[34m INFO \033[0m]Server started:\n IP:{ip}\n   PORT:{port}")

    tornado.ioloop.IOLoop.current().start()