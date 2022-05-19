from ..base.player import Player
import random
from colorama import Fore, Style
import json
import numpy as np

# print(card.card_type)  # đang bị lỗi
class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
    def action(self, dict_input):
        # print(self.list_card)
        dict_card = {}
        for card in dict_input['Turn_player_cards']:
            dict_card[f'{card.name}'] = card.score
        dict_card = dict(sorted(dict_card.items(), key = lambda item:item[1]))
        for i in dict_card:
            print(i, dict_card[i])
        # action_space = self.action_space(dict_input['Turn_player_cards'], dict_input['Board'].turn_cards, dict_input['Board'].turn_cards_owner)

        state = dict_input
        t = self.get_list_state(state)
        a = self.get_list_index_action(t)
        action = random.choice(a)
        return action

def convert_to_dict(card):
    return {
        f'{card.name}': card.score,
    }