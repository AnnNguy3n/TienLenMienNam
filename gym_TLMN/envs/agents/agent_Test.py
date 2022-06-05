from ..base.player import Player

class Agent(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.history = []
    
    def action(self, dict_input):
        self.history.append(self.history.__len__())
        print(self.history)
        return []