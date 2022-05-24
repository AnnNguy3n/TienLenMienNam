from ..base.player import Player
from numpy import e


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
    
    def action(self, dict_input):
        for key in dict_input.keys():
            print(key)
        
        my_cards = dict_input['Turn_player_cards'].copy()
        board = dict_input['Board']


        abc = self.action_space(my_cards, board.turn_cards, board.turn_cards_owner)
        for key in abc.keys():
            print(key)
            print(abc[key])
            xyz = abc[key][0]['list_card']
            for card in xyz:
                print(card.name)
            break
        return []