from ..base.player import Player
import random
from colorama import Fore, Style


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, dict_input):

        state = self.get_list_state(dict_input)

        list_action = self.get_list_index_action(self.get_list_state(dict_input))

        action = random.choice(list_action)
        victory = self.check_victory(self.get_list_state(dict_input))
        if victory == 1:
            print(Fore.LIGHTYELLOW_EX + self.name + ' thắng', end='')
            pass
        elif victory == 0:
            print(Fore.LIGHTYELLOW_EX + self.name + ' thua', end='')
            pass
        return action