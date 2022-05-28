from ..base.player import Player
import random
from colorama import Fore, Style
import pandas
class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
    def action(self, dict_input):  
        state = self.get_list_state(dict_input)
        list_action = self.get_list_index_action(self.get_list_state(dict_input))
        list_all_actions = list(pandas.read_csv('gym_TLMN/envs/action_space.csv')['action_code'])
        print(list_action, 'action có thể làm')
        if state[114] != 0:
            biggest_single = None
            action = None
            for act in list_action:
                real_act = list_all_actions[act]
                if "Single" in real_act:
                    biggest_single = act
                if "Nothing" not in real_act and "Single" not in real_act:
                    action = act
                    break
            if action == None:
                action = biggest_single
        else:
            smallest_single = None
            action = None
            for act in list_action:
                real_act = list_all_actions[act]
                if "Single" in real_act and smallest_single == None:
                    smallest_single = act
                if "Nothing" not in real_act and "Single" not in real_act:
                    action = act
                    break
            if action == None:
                action = smallest_single
        if action == None:
            print("random ở đây")
            action = random.choice(list_action)
        return action