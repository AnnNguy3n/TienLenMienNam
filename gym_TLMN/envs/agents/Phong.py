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
        dict_card = {}
        for card in dict_input['Turn_player_cards']:
            dict_card[card] = card.score

        dict_card = dict(sorted(dict_card.items(), key = lambda item:item[1]))
        for i in dict_card:
            print(i.name, dict_card[i], 'stt :', i.stt)

        action_space = self.action_space(dict_input['Turn_player_cards'], dict_input['Board'].turn_cards, dict_input['Board'].turn_cards_owner)
        action = action_space[list(action_space.keys())[-1]][0]
        list_card_action = action['list_card']
        len_list_card = len(list_card_action)
        for id in range(len(action_space)):
            if len_list_card < len(action_space[list(action_space.keys())[id]][0]['list_card']):
                action = action_space[list(action_space.keys())[id]][0]
                list_card_action = action['list_card']
                len_list_card = len(list_card_action)
        # if action == action_space[list(action_space.keys())[-1]][0]['list_card']:
        #     action
        for card in list_card_action:
            print(card.name, end= ' ')
        for card in dict_card:
            if len(list_card_action) == 1:
                if list_card_action[0].score == card.score:
                    if list_card_action[0].stt > card.stt:
                        list_card_actionc = [card]
                        break
        # print(list_card_action)
        self.check_vtr(dict_input)
        return list_card_action

    def check_vtr(self, dict_input):
        victory = self.check_victory(self.get_list_state(dict_input))
        if victory == 1:
            print(self.name, 'Thắng')
            pass
        elif victory == 0:
            print(self.name, 'Thua')
            pass