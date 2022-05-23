from ..base.player import Player
import random
from colorama import Fore, Style
import json
import numpy as np

# print(card.card_type)  # đang bị lỗi
class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
    def action(self, dict_input):
        t = self.get_list_state(dict_input)

        #Tạo một list các lá bài ở trong tay
        dict_card = {}
        for card in dict_input['Turn_player_cards']:
            dict_card[card] = card.score
        dict_card = dict(sorted(dict_card.items(), key = lambda item:item[1]))

        list_sc_dict = list(dict_card.values())
        list_sc = list_sc_single(list_sc_dict)
        # for i in dict_card:
        #     print(i.name, dict_card[i], 'stt :', i.stt)
        # print('Bài lẻ', list_sc)
        
        #Nếu khởi đầu vòng mới có nhiều lá bài lẻ thì đánh lá nhỏ nhất
        action_space = self.action_space(dict_input['Turn_player_cards'], dict_input['Board'].turn_cards, dict_input['Board'].turn_cards_owner)

        #Đánh bộ có nhiều quân nhất ở trên tay(bộ có thể đánh)
        action = action_space[list(action_space.keys())[-1]][0]
        list_card_action = action['list_card']
        len_list_card = len(list_card_action)
        for id in range(len(action_space)):
            if len_list_card < len(action_space[list(action_space.keys())[id]][0]['list_card']):
                if check_bai_le(list(dict_card.values()), list_card_action):
                    action = action_space[list(action_space.keys())[id]][0]
                    list_card_action = action['list_card']
                    len_list_card = len(list_card_action)
        if t[114] == 0:
            # print(Fore.LIGHTYELLOW_EX + 'Phong khởi đầu vòng mới')
            if len(list_sc) > 2:
                for card in dict_card:
                    if card.score in list_sc:
                        return [card]

        #Nếu chặt một lá thì đánh lá bài có giá trị thấp nhất
        for card in dict_card:
            if len(list_card_action) == 1:
                if card.score in list_sc:
                    if list_card_action[0].score <= card.score:
                        if card.stt >= list_card_action[0].stt:
                            # print(('Danh quan le thap nhat'))
                            list_card_action = [card]

        #Check Victory
        # print([i.score for i in list_card_action])
        # print(list(dict_card.values()))
        # print(check_bai_le(list(dict_card.values()), list_card_action))
        self.check_vtr(dict_input)
        return list_card_action

    def check_vtr(self, dict_input):
        victory = self.check_victory(self.get_list_state(dict_input))
        if victory == 1:
            print(self.name, 'Thắng')
        elif victory == 0:
            print(self.name, 'Thua')
            # raise ValueError('thua roif')
    
def check_bai_le(list_sc_dict, list_card_action):
    so_quan_le_cu =len(list_sc_single(list_sc_dict))
    for i in list_card_action:
        list_sc_dict.remove(i.score)
    so_quan_le_moi = len(list_sc_single(list_sc_dict))
    return False if so_quan_le_moi > so_quan_le_cu else True
        

def list_sc_single(list_sc_dict):
    list_sc = list(set(list_sc_dict) - set(x for x in list_sc_dict if list_sc_dict.count(x) > 1))
    list_sc_copy = list_sc.copy()
    
    #tìm bài lẻ ở trên bàn
    if 12 in list_sc_copy:
        list_sc_copy.remove(12)
    list_doi = set(x for x in list_sc_dict if list_sc_dict.count(x) == 2)
    for score in list_sc_copy:
        if (score+1 in list_sc_dict) and (score+2 in list_sc_dict):
            list_sc.remove(score)
        elif (score+1 in list_sc_dict) and (score-1 in list_sc_dict):
            list_sc.remove(score)
        elif (score-1 in list_sc_dict) and (score-2 in list_sc_dict):
            list_sc.remove(score)

    for score in set(list_sc_dict):
        if (score+1 in list_sc_dict) and (score+2 in list_sc_dict):
            if score in list_doi: list_sc.append(score)
        elif (score+1 in list_sc_dict) and (score-1 in list_sc_dict):
            if score in list_doi: list_sc.append(score)
        elif (score-1 in list_sc_dict) and (score-2 in list_sc_dict):
            if score in list_doi: list_sc.append(score)
    # in các lá bài trên tay là danh sách điểm của các bài lẻ
    list_sc = sorted(list_sc)
    return list_sc