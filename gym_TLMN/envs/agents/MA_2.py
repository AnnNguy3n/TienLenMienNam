from re import T
from ..base.player import Player
import random
import math
import json
import numpy as np
import pandas as pd

PATH = 'gym_TLMN/envs/agents/finalized_model.sav'
class Agent(Player):
    def __init__(self, name):
        pd.DataFrame({'state':[], 'Turn_to_win': []}).to_csv('State_tam_2.csv', index = False)
        super().__init__(name)

    def action(self,  state=None):
        t = self.get_list_state(state)
        a = self.get_list_index_action(t)
        number = random.randint(0,len(a)-1)
        try:
            s_a = pd.read_csv('State_tam_2.csv')
        except:
            s_a = [np.nan]
        s_a.loc[len(s_a.index)] =[t, np.nan]
        s_a.to_csv('State_tam_2.csv', index = False)

        if self.check_victory(t) == 1:
            try:
                state_save = pd.read_csv('state.csv')
            except:
                state_save = pd.DataFrame({'state':[], 'Turn_to_win': []})
            s_a = pd.read_csv(f'State_tam_2.csv')
            s_a['Turn_to_win'] = s_a.index
            state_save = pd.concat([state_save, s_a]) 
            state_save.to_csv('state.csv', index = False)   
        
        return a[number]

def prepar_data_train(df_state):
  df_state1 = df_state.copy()
  df_state1["state"] = df_state1["state"].apply(lambda x: x.replace("[" , ","))
  df_state1["state"] = df_state1["state"].apply(lambda x: x.replace("]" , ","))
  df_state1 = df_state1["state"].str.split(pat=',',expand=True)
  df_state1['Turn_to_win'] = df_state['Turn_to_win']
  return df_state1


def turn_win_left(state, PATH):
    """
    requires: 
    - import pickle
    input: state, PATH model
    output: turn to win ( best value: 0 )
    """
    # prepar dataset 
    data = prepar_data_train(state) 
    feature = [107, 108, 44, 45, 110, 50, 109, 43, 48, 39, 49, 47, 46, 42, 40, 41, 34, 36, 38, 28, 51, 37, 54, 32, 31, 30, 35, 23, 52, 27, 10, 24, 20, 19, 115, 26, 14, 33, 22, 16, 18, 12, 29, 13, 17, 15, 11, 21, 8, 53, 25, 7, 9, 2, 114, 6, 4, 5, 1, 3, 113, 70, 66, 62, 112]
    dataset = data[feature]

    loaded_model = pickle.load(open(PATH, 'rb'))
    y_pred = loaded_model.predict(dataset)
    return y_pred