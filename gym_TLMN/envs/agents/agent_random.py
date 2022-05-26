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
        # if self.check_victory(t) == -1:
        # print('turn_to_win', turn_to_win(t, PATH))
        turn_win = []
        if self.check_victory(t) == -1:
            list_st = self.list_action_state( a, t)
            for id_a in range(len(a)):
                # print(list_st[id_a])
                turn_win.append(turn_to_win(list_st[id_a], PATH))
        # print(a)
        # print(turn_win)
        if len(turn_win) > 0:
            print(a[turn_win.index(min(turn_win))])
            return a[turn_win.index(min(turn_win))]
        # if self.check_victory(t) == 1:
        #     print(self.name, 'thắng')
        #     self.save_json(self.state_new, self.action_new)
        # elif self.check_victory(t) == 0:
        #     print(self.name, 'Thua')
        #     self.save_json(self.state_new, self.action_new)
        print(t)
        print(action)
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
                if str(action) in data[key_state]:
                    random_weight = random.choices(list(data[key_state][str(action)].keys()), weights = data[key_state][str(action)].values(), k=1)[0]
                    s_n.append(int(random_weight))
                else:
                    s_n.append(t[id_s])
            list_state.append(s_n)
        
        return list_state

def turn_to_win(state, PATH):
    feature = ['107', '110', '45', '108', '46', '43', '44', '109', '36', '48', '51', '42', '39', '31', '47', '24', '38', '29', '35', '28', '49', '30', '40', '32', '33', '27', '6', '17', '41', '34', '50', '37', '25', '9', '54', '22', '14', '10', '5', '8', '26', '19', '18', '115', '23', '16', '15', '13', '11', '21', '20', '12', '52', '1', '4', '7', '2', '53', '114', '3', '58', '113', '61', '77', '60']
    dat = pd.DataFrame([state])
    dat.columns = [str(i) for i in range(1, len(state)+1)]
    dataset = dat[feature]
    loaded_model = pickle.load(open(PATH, 'rb'))
    turn_win = loaded_model.predict(dataset)
    return math.ceil(turn_win[0])