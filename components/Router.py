import components.info
import json
import random

from components.Lobby import Lobby

class Router():
    
    def __init__(self):

        self.__RULES = {
            "GET":{
                "VERSION": self.get_version,
                "PING": self.ping,
                "GETAPI": self.get_api
            },
            "POST":{
                "REG": self.set_client_name,
                "CREATELOBBY": self.create_lobby
            }
        }

        self.using_lobby_code_pull = []
        self.lobby_list = {}
    
    def get_lobby_code(self):

        rand_pool = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        
        while True:

            code = ""
            for i in range(8):
                code += rand_pool[random.randint(0, len(rand_pool) - 1)]
            
            if not code in self.using_lobby_code_pull:
                break
        
        return code
    
    def remove_player(self, player):
        pass

    def remove_lobby(self, code):

        del self.lobby_list[code]

    def update(self, recv, client):

        addr = client.get_addr()

        print(recv)

        try:
            #print(f"[\033[34m INFO \033[0m]Sing message:{addr[0]}:{addr[1]} type:{recv["type"]} name:{recv["name"]} body:{recv["body"]}")

            resp = self.__RULES[recv["type"]][recv["name"]](recv["body"], client)

            resp = json.dumps(resp)

            #print(f"[\033[34m INFO \033[0m]Sing message:{addr[0]}:{addr[1]} type:{recv["type"]} name:{recv["name"]} body:{recv["body"]}")
        except KeyError:

            resp = {
                "code": 404,
                "body": {
                    "aaa": 1
                }
            }

            resp = json.dumps(resp)

            return {
                "id": recv["id"],
                "response": resp
            }

        return {
            "id": recv["id"],
            "response": resp
        }
    
    def get_version(self, arg, client):

        return {
            "code": 200,
            "body": {
                "server": components.info.VERSION_SERVER,
                "api": components.info.VERSION_API
            }
        }
    
    def get_api(self, arg, client):

        return {
            "code": 200,
            "body": "Router"
        }
    
    def set_client_name(self, name, client):

        client.set_nik_name(name)

        return {
            "code": 200,
            "body": {
                "name": name
            }
        }
    
    def ping(self, arg, client):

        return {
            "code": 200,
            "body": "PONG"
        }
    
    def create_lobby(self, arg, client):

        code = self.get_lobby_code()
        self.lobby_list[code] = Lobby(self, code)
        print("aaa")
        self.lobby_list[code].add_player(client)
        self.lobby_list[code].set_host(client)

        return {
            "code": 200,
            "body": "lobby created"
        }
    
    def join_lobby(self, arg, client):
        
        self.lobby_list[arg].add_player(client)