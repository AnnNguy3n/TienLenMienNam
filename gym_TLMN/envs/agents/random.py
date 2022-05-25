from ..base.player import Player
import random
import math
import json
import numpy as np
from colorama import Fore, Style
import pandas as pd

PATH = 'gym_TLMN/envs/agents/finalized_model.sav'
class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self,  dict_input):
        t = self.get_list_state(dict_input)
        a = self.get_list_index_action(t)
        action = random.choice(a)
        self.check_vtr(dict_input)

        print(turn_win_left(t, PATH))
        return action
    
    def check_vtr(self, dict_input):
        victory = self.check_victory(self.get_list_state(dict_input))
        if victory == 1:
            print(self.name, 'Thắng')
            pass
        elif victory == 0:
            print(self.name, 'Thua')
            pass

def turn_win_left(state, PATH):
    """
    requires: 
    - import pickle
    input: state, PATH model
    output: turn to win ( best value: 0 )
    """
    # prepar dataset 
    data = pd.DataFrame([state])
    print('data ', data)
    feature = [107, 108, 44, 45, 110, 50, 109, 43, 48, 39, 49, 47, 46, 42, 40, 41, 34, 36, 38, 28, 51, 37, 54, 32, 31, 30, 35, 23, 52, 27, 10, 24, 20, 19, 115, 26, 14, 33, 22, 16, 18, 12, 29, 13, 17, 15, 11, 21, 8, 53, 25, 7, 9, 2, 114, 6, 4, 5, 1, 3, 113, 70, 66, 62, 112]
    dataset = data[feature]

    loaded_model = pickle.load(open(PATH, 'rb'))
    y_pred = loaded_model.predict(dataset)
    return y_pred