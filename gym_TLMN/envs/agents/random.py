from ..base.player import Player
import random
import math
import json
import numpy as np
from colorama import Fore, Style

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self,  dict_input):
        state = dict_input
        t = self.get_list_state(state)
        a = self.get_list_index_action(t)
        action = random.choice(a)
        return action
