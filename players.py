import json
class Players():
    def __init__(self):
        self.players = json.load(
            open('data_players\\players.json', 'r', encoding='utf-8'))

    def get_player(self):
        pass
