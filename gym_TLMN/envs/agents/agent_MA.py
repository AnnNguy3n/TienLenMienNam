from ..base.player import Player
import random
from colorama import Fore, Style
import json
import numpy as np

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
    def action(self, dict_input):
        state = dict_input
        lst_state = self.get_list_state(state)
        actions = self.get_list_index_action(lst_state)

        # Tạo một list các lá bài ở trong tay
        dict_card = {}
        for card in dict_input['Turn_player_cards']:
            dict_card[card] = card.score


        # tạo action space
        action_space = self.action_space(dict_input['Turn_player_cards'], dict_input['Board'].turn_cards,
                                         dict_input['Board'].turn_cards_owner)
        # print('action space ', action_space)

        lst_len_card = []
        for action_name in action_space.keys():
            # neu the la single danh luon
            if action_name == 'Single':
                return action_space[action_name][0]['list_card']

            # cai nao la bo danh luon
            number_card_return = len(action_space[action_name][0]['list_card'])
            lst_len_card.append(number_card_return)
            # print('number card return ', number_card_return)

            if number_card_return == 2:
                return action_space[action_name][0]['list_card']

            if number_card_return == 3:
                return action_space[action_name][0]['list_card']


        # max_card = max(lst_len_card)
        # for action_name in action_space.keys():
        #     number_card_return = len(action_space[action_name][0]['list_card'])
        #     if number_card_return == max_card:
        #         return action_space[action_name][0]['list_card']

            # cai nao la
        action = random.choice(actions)
        return action

