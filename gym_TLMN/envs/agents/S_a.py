from ..base.player import Player
import random
import math
import json
import numpy as np
from colorama import Fore, Style
import pandas as pd
import pickle
import xgboost as xgb
import warnings 
warnings.filterwarnings('ignore')
# PATH = 'gym_TLMN/envs/agents/model (1).pkl'
# PATH = 'gym_TLMN/envs/agents/finalized_model1.sav'
PATH = 'gym_TLMN/envs/agents/model (1).pkl'
class Agent(Player):
    def __init__(self, name):
        self.state_new = []
        self.action_new = []
        super().__init__(name)

    def action(self,  dict_input):
        t = self.get_list_state(dict_input)
        a = self.get_list_index_action(t)
        action = random.choice(a)
        self.state_new.append(t)
        self.action_new.append(action)
        if self.check_victory(t) != -1:
            self.save_json(self.state_new, self.action_new)
        return action
    
    def save_json(self, state_new, action_new):
        try:
            s_a = json.load(open('gym_TLMN/envs/agents/S_A.json'))
        except:
            s_a = {} 
        for id in range(len(state_new) - 1):
            t = state_new[id]
            t_n = state_new[id+1]
            # print(action_new[id])
            for id_s in range(len(t)):
                if f'{id_s}_{t[id_s]}' in s_a:
                    # print(f'{id_s}_{t[id_s]}', action_new[id])
                    if str(action_new[id]) in s_a[f'{id_s}_{t[id_s]}']:
                        if str(t_n[id_s]) in s_a[f'{id_s}_{t[id_s]}'][str(action_new[id])]:
                            s_a[f'{id_s}_{t[id_s]}'][str(action_new[id])][str(t_n[id_s])] += 1
                        else:
                            s_a[f'{id_s}_{t[id_s]}'][str(action_new[id])][str(t_n[id_s])] = 1
                    else:
                        t_n_2 = {str(t_n[id_s]):1}
                        s_a[f'{id_s}_{t[id_s]}'][str(action_new[id])] = t_n_2
                else:
                    t_n_3 = {str(t_n[id_s]):1}
                    action_new_2 = {str(action_new[id]) : t_n_3}
                    s_a[f'{id_s}_{t[id_s]}'] = action_new_2
        with open('gym_TLMN/envs/agents/S_A.json', 'w') as f:
            json.dump(s_a, f)
            
    def check_vtr(self, dict_input):
        victory = self.check_victory(self.get_list_state(dict_input))
        if victory == 1:
            print(self.name, 'Thắng')
        elif victory == 0:
            print(self.name, 'Thua')