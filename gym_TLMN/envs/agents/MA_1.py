from re import T
from ..base.player import Player
import random
import math
import json
import numpy as np
import pandas as pd


class Agent(Player):
    def __init__(self, name):
        pd.DataFrame({'state':[], 'action':[], 'list_action': [],'win': []}).to_csv('State_tam_1.csv', index = False)
        super().__init__(name)

    def action(self,  state=None):
        t = self.get_list_state(state)
        a = self.get_list_index_action(t)
        number = random.randint(0,len(a)-1)
        try:
            s_a = pd.read_csv('State_tam_1.csv')
        except:
            s_a = [np.nan, np.nan, np.nan, np.nan]
        s_a.loc[len(s_a.index)] =[t, number, a, np.nan]
        s_a.to_csv('State_tam_1.csv', index = False)

        print(self.check_victory(t))
        if self.check_victory(t) == 1:
            try:
                state_save = pd.read_csv('state.csv')
            except:
                state_save = pd.DataFrame({'state':[], 'action':[], 'list_action': [],'win': []})
            s_a = pd.read_csv(f'State_tam_1.csv').assign(win = 1)
            state_save = pd.concat([state_save, s_a])
            state_save.to_csv('state.csv', index = False)  
        elif self.check_victory(t) == 0:
            try:
                state_save = pd.read_csv('state.csv')
            except:
                state_save = pd.DataFrame({'state':[], 'action':[], 'list_action': [],'win': []})
            s_a = pd.read_csv(f'State_tam_1.csv').assign(win = 0)
            state_save = pd.concat([state_save, s_a]) 
            state_save.to_csv('state.csv', index = False)      
        return a[number]
