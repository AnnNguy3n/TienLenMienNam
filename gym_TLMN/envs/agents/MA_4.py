from re import T
from ..base.player import Player
import random
import math
import json
import numpy as np
import pandas as pd


class Agent(Player):
    def __init__(self, name):
        self.s_a = []
        super().__init__(name)

    def action(self,  state=None):
        t = self.get_list_state(state)
        a = self.get_list_index_action(t)
        number = random.randint(0,len(a)-1)
        self.s_a.append(t)

        if self.check_victory(t) == 1:
            try:
                state_save = pd.read_csv('state.csv')
            except:
                state_save = pd.DataFrame({'state':[], 'Turn_to_win': []})
            s_a = pd.DataFrame({'state':self.s_a})
            s_a = s_a.iloc[::-1].reset_index(drop = True)
            s_a['Turn_to_win'] = s_a.index
            state_save = pd.concat([state_save, s_a]) 
            state_save.to_csv('state.csv', index = False)   
        return a[number]