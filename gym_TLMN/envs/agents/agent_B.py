from re import T
from ..base.player import Player
import random as rd
import math
import numpy as np
import json
path = "/content/TienLenMienNam/gym_TLMN/"

def create_mind(learned_action):
    use_action = [[] for _ in learned_action]
    for action_id in range(len(learned_action)):
        learned_state = learned_action[action_id]
        for dict_state in learned_state:
            chose = list(dict_state.keys())
            weigh = list(dict_state.values())
            if len(chose) == 0:
                chosen = 0
            else:
                chosen = int(rd.choices(chose,weights=weigh)[0])
            use_action[action_id].append(chosen)
    return use_action

def predict(state,act,use_action):
    new_state = np.array(state) + np.array(use_action[act])
    return new_state

def scoring(state,value):
    list_score = []
    for id_state in range(len(state)):
        name = str(id_state) + "_" + str(state[id_state])
        if name in value.keys():
            score = value[name][0]
            list_score.append(score)
            # print(score,name)
    return min(list_score)





class Agent(Player):
    with open(path + "envs/agents/action.json", 'r') as openfile:
        act_model = json.load(openfile)
    with open(path + "envs/agents/value.json", 'r') as openfile:
        value = json.load(openfile)
    action_model = create_mind(act_model)
    def __init__(self, name):
        super().__init__(name)
        self.pairs = []




    def action(self, dict_input):
        State = self.get_list_state(dict_input)
        list_action = self.get_list_index_action(State)
        print(len(list_action))
        action = rd.choice(list_action)
        min_turn = 12
        for to_act in list_action:
            old_states = [predict(State,to_act,Agent.action_model)]
            mode = "start"
            for turn in range(1,min_turn+1):
                if mode == "end":
                    break
                new_states = []
                for state in old_states:
                    if self.check_victory(state) == 1:
                        mode = "end"
                        break
                    else:
                        try:
                            list_new_action = self.get_list_index_action(state)
                            for act in list_new_action:
                                new_states.append(predict(state,act,Agent.action_model))
                        except:
                            continue
                # old_states = new_states.copy()
                danhsach = min(len(new_states),5)
                old_states = rd.choices(new_states,k=danhsach)
            if turn < min_turn:
                min_turn = turn
                action = to_act
        print("dự kiến thắng sau",min_turn,"turn nữa")
        self.pairs.append([State,action])
        # học thêm về action 
        if self.check_victory(State) != -1:
            try:
                with open(path + "envs/agents/action.json", 'r') as openfile:
                    action_learning = json.load(openfile)
            except:
                action_learning = [[{} for a in range(len(State))] for _ in range(self.amount_action_space)]
            for id_pair in range(len(self.pairs)):
                old_state = self.pairs[id_pair][0]
                old_action = self.pairs[id_pair][1]
                if id_pair != len(self.pairs) -1:
                    new_state = self.pairs[id_pair+1][0]
                else:
                    new_state = State
                act_formula = np.array(new_state) - np.array(old_state)
                for id_state in range(len(act_formula)):
                    name = str(act_formula[id_state])
                    if name not in action_learning[old_action][id_state].keys():
                        action_learning[old_action][id_state][name] = 1
                    else:
                        action_learning[old_action][id_state][name] += 1
            with open(path+'envs/agents/action.json', 'w') as f:
                json.dump(action_learning, f)   
        return action
