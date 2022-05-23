from ..base.player import Player

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
    
    def action(self, dict_input):
        return []