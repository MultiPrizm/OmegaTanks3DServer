from components.UpdateSystem import GameCore
import json
import asyncio

class Lobby():

    def __init__(self, router, lobby_code):
        
        self.router = router
        self.lobby_code = lobby_code

        self.player_list = []

        self.rules = {
            "max_player": 6,
            "ban_list": []
        }

        self.game_core = GameCore(self)
    
    def add_player(self, player):

        self.player_list.append(player)
        player.set_update_system(self.game_core)
        self.game_core.add_player(player)
    
    def remove_player(self, player):

        self.player_list.remove(player)
    
    def remove_lobby(self):

        pass

    def set_host(self, player):
        self.player_list.append(player)
        player.set_update_system(self.game_core)
        self.game_core.add_player(player)

        self.game_core.set_host(player)