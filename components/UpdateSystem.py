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
                "GETLOBBYCODE": self.get_lobby_code,
                "GETPLAYERS": self.get_players
            },
            "POST":{
                "UPDATEPLAYER": self.update_player
            }
        }

        self.unit_list = {}

        self.players_unit = {}

        self.status_game = False
    
    def add_player(self, player):

        self.player_list.append(player)
    
    def remove_player(self, player):

        self.player_list.remove(player)
        self.lobby.remove_player(player)
    
    def lobby_decorator(self, func):

        def wraper(*arg):

            if self.status_game:
                res = func(*arg)
            else:
                res = {
                    "code": 401
                }

            return res

        return wraper

    def set_host(self, player):
        self.host_gate_way = HostGateWay(self, player)
        player.set_update_system(self.host_gate_way)

    async def update(self, recv, client):

        addr = client.get_addr()

        print(recv)

        try:

            resp = self.__RULES[recv["type"]][recv["name"]](recv["body"], client)
        
        except None:

            resp = {
                "code": 404
            }

        resp = json.dumps(resp)

        resp2 = {
            "name": recv["name"],
            "response": resp
        }

        resp2 = json.dumps(resp2)

        return {
            "id": recv["id"],
            "response": resp2
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
    
    def get_players(self, arg, client):

        res = []

        for i in self.player_list:

            res.append(i.nik_name)

        return {
            "code": 200,
            "body": res
        }
    
    @lobby_decorator
    def update_player(self, recv, client):

        arg = json.loads(recv)
    
        if arg["id"] in self.players_unit:

            if id(self.players_unit[arg["id"]]["client"]) == id(client):
                self.players_unit[arg["id"]]["body"] = arg["body"]
                print(self.players_unit)
        else:
            self.players_unit[arg["id"]] = {
                "client": client,
                "body": arg["body"]
            }


class HostGateWay():

    def __init__(self, game_core, host):
        
        self.game_core = game_core
        self.host = host

        self.__RULES = {
            "GET":{
                "PING": self.ping,
                "GETAPI": self.get_api,
                "GETLOBBYCODE": self.get_lobby_code,
                "GETPLAYERS": self.game_core.get_players
            },
            "POST":{
                "UPDATEPLAYER": self.game_core.update_player,
                "STARTGAME": self.start_game
            }
        }
    
    def remove_player(self, player):

        self.game_core.lobby.remove_lobby()
    
    async def update(self, recv, client):

        addr = client.get_addr()

        print(recv)

        try:

            resp = self.__RULES[recv["type"]][recv["name"]](recv["body"], client)
        
        except KeyError:

            resp = {
                "code": 404
            }

        resp = json.dumps(resp)

        resp2 = {
            "name": recv["name"],
            "response": resp
        }

        resp2 = json.dumps(resp2)

        return {
            "id": recv["id"],
            "response": resp2
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
    
    def start_game(self, arg, client):

        req = {
            "code": 200,
            "body": "game started"
        }

        resp = json.dumps(resp)

        resp2 = {
            "name": "STARTGAME",
            "response": resp
        }

        resp2 = json.dumps(resp2)

        resp3 = {
            "id": "EventSystem",
            "response": resp2
        }

        self.game_core.fire_clients(resp3)