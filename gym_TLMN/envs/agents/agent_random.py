from ..base.player import Player
import random
import math
import json
import numpy as np
from colorama import Fore, Style
#

class Agent(Player):
    def __init__(self, name):
        self.state_new = []
        self.action_new = []
        self.data_json = json.load(open('gym_TLMN/envs/agents/S_A.json'))
        super().__init__(name)

    def action(self,  dict_input):
        t = self.get_list_state(dict_input)
        a = self.get_list_index_action(t)
        action = random.choice(a)
        self.state_new.append(t)
        self.action_new.append(action)
        # if self.check_victory(t) == -1 and len(dict_input['Turn_player_cards']) > 5:
        #     pass
        if self.check_victory(t) == -1:
            
        if self.check_victory(t) == 1:
            print(self.name, 'thắng')
            self.save_json(self.state_new, self.action_new)
        elif self.check_victory(t) == 0:
            print(self.name, 'Thua')
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
            for id_s in range(len(t)):
                if f'{id_s}_{t[id_s]}' in s_a:
                    if action_new[id] in s_a[f'{id_s}_{t[id_s]}']:
                        if t_n[id_s] in s_a[f'{id_s}_{t[id_s]}'][action_new[id]]:
                            s_a[f'{id_s}_{t[id_s]}'][action_new[id]][t_n[id_s]] += 1
                        else:
                            s_a[f'{id_s}_{t[id_s]}'][action_new[id]][t_n[id_s]] = 1
                    else:
                        s_a[f'{id_s}_{t[id_s]}'][action_new[id]] = {t_n[id_s]:1}
                else:
                    s_a[f'{id_s}_{t[id_s]}'] = {action_new[id]:{t_n[id_s]:1}}
        with open('gym_TLMN/envs/agents/S_A.json', 'w') as f:
            json.dump(s_a, f)
            

    def list_action_state(self, a, t):
        # if 
        data = self.data_json
        list_state = []
        for action in a:
            s_n = []
            for id_s in range(len(t)):
                key_state = f'{id_s}_{t[id_s]}'
                if action in data[key_state]:
                    random_weight = random.choices(list(data[key_state][action].keys()), weights = data[key_state][action].values(), k=1)[0]
                    s_n.append(random_weight)
                else:
                    s_n.append(t[id_s])
            list_state.append(s_n)
        
        return list_state