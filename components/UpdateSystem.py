import components.info
import json
import random

class GameCore():

    def __init__(self, lobby):
        self.lobby = lobby
        self.player_list = []

        self.host_gate_way = None

        self.__RULES = {
            "GET":{
                "PING": self.ping,
                "GETAPI": self.get_api,
                "GETLOBBYCODE": self.get_lobby_code
            },
            "POST":{

            }
        }
    
    def add_player(self, player):

        self.player_list.append(player)
    
    def remove_player(self, player):

        self.player_list.remove(player)
        self.lobby.remove_player(player)
    
    def set_host(self, player):
        self.host_gate_way = HostGateWay(self, player)
        player.set_update_system(self.host_gate_way)

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
    
    def fire_clients(self, mess):

        for i in self.player_list:

            i.fire_client(mess)
    
    def get_api(self, arg, client):

        return {
            "code": 200,
            "body": "GameCore"
        }
    
    def ping(self, arg, client):

        return {
            "code": 200,
            "body": "PONG"
        }

    def get_lobby_code(self, arg, client):

        return {
            "code": 200,
            "body": self.lobby.lobby_code
        }


class HostGateWay():

    def __init__(self, game_core, host):
        
        self.game_core = game_core
        self.host = host

        self.__RULES = {
            "GET":{
                "PING": self.ping,
                "GETAPI": self.get_api,
                "GETLOBBYCODE": self.get_lobby_code
            },
            "POST":{

            }
        }
    
    def remove_player(self, player):

        self.game_core.lobby.remove_lobby()
    
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
    
    def get_api(self, arg, client):

        return {
            "code": 200,
            "body": "HostGateWay"
        }
    
    def ping(self, arg, client):

        return {
            "code": 200,
            "body": "PONG"
        }
    
    def get_lobby_code(self, arg, client):

        return {
            "code": 200,
            "body": self.game_core.lobby.lobby_code
        }