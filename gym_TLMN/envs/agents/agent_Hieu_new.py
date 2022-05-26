from ..base.player import Player
import random
from colorama import Fore, Style
import pandas as pd

full_action = list(pd.read_csv('gym_TLMN/envs/action_space.csv')['action_code'])
full_score = list(pd.read_csv('gym_TLMN/envs/action_space.csv')['hand_score'])
full_hand_name = list(pd.read_csv('gym_TLMN/envs/action_space.csv')['hand_name'])

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self, dict_input):
        state = self.get_list_state(dict_input)
        list_action = self.get_list_index_action(self.get_list_state(dict_input))
        print(list_action, 'action có thể làm')
        print('PASS')
        victory = self.check_victory(self.get_list_state(dict_input))
        if victory == 1:
            print(Fore.LIGHTYELLOW_EX + self.name + ' thắng', end='')
            pass
        elif victory == 0:
            print(Fore.LIGHTYELLOW_EX + self.name + ' thua', end='')
            pass
        elif victory == -1:
            print(Fore.LIGHTYELLOW_EX + 'Chưa hết game', end='')
            pass
        
        print(Style.RESET_ALL)
        card_number = state[107:110]
        print(state[110:114], 'tình trạng bỏ vòng')
        if state[114] == 0:     #bđ vòng mới
            print('đầu vòng')
            return self.start_circle(dict_input)
        #đánh nối vòng
        else:
            if len(list_action) > 1:
                return self.continue_turn(dict_input)
            else:
                return list_action[0]

    def continue_turn(self, dict_input):
        state = self.get_list_state(dict_input)
        all_action = self.possible_action(dict_input['Turn_player_cards'])
        action_space = self.action_space(dict_input['Turn_player_cards'], dict_input['Board'].turn_cards, dict_input['Board'].turn_cards_owner)
        dict_action = {}
        dict_action_len = {}
        for key in list(action_space.keys())[:-1]:
            for action in action_space[key]:
                dict_action[tuple(action['list_card'])] = action['hand_name']
                dict_action_len[tuple(action['list_card'])] = len(action['list_card'])
        list_key = list(all_action.keys())
        sort_action_len = sorted(dict_action_len.items(), key=lambda x:x[1], reverse= True)
        for item in sort_action_len:
            if "3_of_a_kind" in  dict_action[item[0]] or 'straight' in  dict_action[item[0]] and 'pairs_straight' not in dict_action[item[0]]:
                return list(item[0])

        for action in list(dict_action.keys())[:-1]:
            action1 = list(action)
            if len(action1) == 1:
                can_return = True
                count_pair = 0
                count_straight = 0
                count_contain = 0
                print(can_return,count_pair,count_straight,count_contain)
                for i in range(2, len(list_key)):
                    for action2 in all_action[list_key[i]]:
                        if self.check_action(action1, action2['list_card']) > 0:
                            print('_straight', action2['hand_name'])
                            if action2['hand_name'] == 'Pair':
                                can_return = False
                                count_pair += 1
                            elif '_straight' in action2['hand_name']:
                                if (action1[0] == action2['list_card'][-1] or action1[0] == action2['list_card'][0]) and len(action2['list_card']) >2:
                                    count_straight += 1
                                    can_return = False
                                if action1[0] in action2['list_card']:
                                    count_contain += 1
                if count_pair == 2 and count_straight > 0:
                    print('TOANG2')
                    return action1
                elif count_pair == 1:
                    print('TOANG3')
                    return action1
                elif count_pair == 0 and count_straight > 2:
                    print('TOANG3')
                    return action1
                elif can_return == True:
                    print('TOANG4')
                    return action1
            elif len(action1) > 1:
                can_return = True
                count_3_kind = 0
                count_straight = 0
                for i in range(3, len(list_key)):
                    for action2 in all_action[list_key[i]]:
                        if self.check_action(action1, action2['list_card']) > 0:
                            if '_straight' in action2['hand_name']:
                                if "3_of_a_kind" in action2['hand_name']:
                                    can_return == False
                                    count_3_kind += 1
                                if (action1[1] == action2['list_card'][0] or action1[0] == action2['list_card'][0]):
                                    count_straight += 1
                                    can_return = False
                if count_3_kind == 1 and count_straight > 0:
                    print('TOANG5')
                    return action1
                elif can_return == True:
                    print('TOANG5.05')
                    return action1
            else:
                print('TOANG5.5')
                # print(action1)
                return action1

        for action in action_space[list(action_space.keys())[-2]]:
            # print(action_space)
            if len(action['list_card']) >= state[106] - 1:
                print('TOANG6')
                return action['list_card']
            if '4_of_a_kind' not in action['hand_name'] and '_pairs_straight' not in action['hand_name']:
                if action['hand_score'] < 45:
                    print('TOANG7')
                    return action['list_card']
        for action in action_space[list(action_space.keys())[-2]]:
            print('TOANG8')
            return action['list_card']  

    def start_circle(self, dict_input):
        state = self.get_list_state(dict_input)
        card_number = state[107:110]
        action_space = self.action_space(dict_input['Turn_player_cards'], dict_input['Board'].turn_cards, dict_input['Board'].turn_cards_owner)

        dict_action = {}
        dict_action_len = {}
        for key in list(action_space.keys())[:-1]:
            for action in action_space[key]:
                dict_action[tuple(action['list_card'])] = action['hand_name']
                dict_action_len[tuple(action['list_card'])] = len(action['list_card'])
        #nếu đối thủ còn ít bài
        sort_action_len = sorted(dict_action_len.items(), key=lambda x:x[1], reverse= True)
        for item in sort_action_len:
            if "3_of_a_kind" in  dict_action[item[0]] or 'straight' in  dict_action[item[0]] and 'pairs_straight' not in dict_action[item[0]]:
                return list(item[0])
        if min(card_number) < 5:
            action_last = {}
            for list_type_action in action_space.values():
                for action in list_type_action:
                    if len(action['list_card']) == state[106]:
                        print('toang106')
                        return action['list_card']
                    else:
                        action_last[tuple(action['list_card'])] = action['hand_score']
            sort_action = sorted(dict_action.items(), key=lambda x:x[1], reverse= False)
            # print(sort_action)
            print('toang00')
            return list(sort_action[0][0])
        #nếu đối thủ còn nhiều bài
        else:

            action_last = {}
            for list_type_action in action_space.values():
                for action in list_type_action:
                    action_last[tuple(action['list_card'])] = action['hand_score']
            #Cóc:
            list_key = list(action_space.keys())[:-1]
            # print(action_space)
            for i in range(len(list_key) -1):
                # print(list_key[i])
                for action1 in action_space[list_key[i]]:
                    check = True
                    for j in range(i+1, len(list_key)):
                        for action2 in action_space[list_key[j]]:
                            if self.check_action(action1['list_card'], action2['list_card']) > 0:
                                check = False
                    if check == True:
                        print('DONE1')
                        if action1['hand_score'] < 45:
                            return action1['list_card']
            #nếu các bộ trên đều liên quan nhau
            for action in action_space[list_key[-1]]:
                if len(action['list_card']) >= state[106] - 1:
                    print('DONE3')
                    return action['list_card']
                if '4_of_a_kind' not in action['hand_name'] and '_pairs_straight' not in action['hand_name']:
                    print('DONE2')
                    return action['list_card']
            for action in action_space[list_key[-1]]:
                return action['list_card']

    def check_action(self, action1, action2):
        same = 0
        for card1 in action1:
            for card2 in action2:
                if card1 == card2:
                    same += 1
        return same
