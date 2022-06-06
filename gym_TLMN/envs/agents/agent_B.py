from ..base.player import Player
import random as rd
from colorama import Fore, Style
import json
import os
import numpy as np
path = os.path.dirname(os.path.abspath(__file__)) + "/"
def predict(state,act,model,max_limit,min_limit):
   data = model[act]
   act_formula = []
   for use_data in data:
       try:
           choice = rd.choices(list(use_data.keys()),weights=list(use_data.values()))[0]
       except:
           choice = 0
       act_formula.append(choice)
   new_state = np.array(state,dtype=int) + np.array(act_formula,dtype=int)
   new_state = np.maximum(new_state,min_limit)
   new_state = np.minimum(new_state,max_limit)
   return new_state
 
 
 
 
 
class Agent(Player):
   def __init__(self, name):
       super().__init__(name)
       self.states = []
       self.actions = []
       with open(path + 'data.json', 'r') as f:
           self.data = json.load(f)
       with open(path + 'model.json', 'r') as f:
           self.model = json.load(f)
       self.max_limit = np.load(path+"max_limit.npy")
       self.min_limit = np.load(path+"min_limit.npy")
   def greedy_state(self,state):
       list_action = self.get_list_index_action(state)
       list_weight = [self.data[act][0] for act in list_action]
       action = list_action[list_weight.index(max(list_weight))]
       new_state = predict(state,action,self.model,self.max_limit,self.min_limit)
       return new_state
 
   def action(self, dict_input):
       State = self.get_list_state(dict_input)
       list_action = self.get_list_index_action(State)
       action = None
       # min_turn = 20
       for act in list_action:
           old_state = predict(State,act,self.model,self.max_limit,self.min_limit)
           if self.check_victory(old_state) == 1:
               action = act
               print("thắng đến nơi rồi")
               break
       #     for turn in range(1,min_turn+1):
       #         new_state = self.greedy_state(old_state)
       #         if self.check_victory(new_state) == 1 and turn <= min_turn:
       #             min_turn = turn
       #             action = act
       #         old_state = new_state.copy()
       # print("dự kiến thắng sau",min_turn,"turn nữa")
       if action == None:
           list_weight = [self.data[act][0] for act in list_action]
           action = list_action[list_weight.index(max(list_weight))]
       return action
