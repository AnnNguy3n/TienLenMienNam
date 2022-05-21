from colorama import Fore, Style
from gym_TLMN.envs.base.card import Card
import pandas


class Player:
    def __init__(self, name: str):
        self.__name = name
        self.__full_action = list(pandas.read_csv('gym_TLMN/envs/action_space.csv')['action_code'])
        self.__amount_action_space = self.__full_action.__len__()
        self.reset()

    def reset(self):
        self.__played_cards = []

    @property
    def amount_action_space(self):
        return self.__amount_action_space

    @property
    def name(self):
        return self.__name

    @property
    def played_cards(self):
        return self.__played_cards.copy()

    @property
    def amount_cards_remaining(self):
        return 13 - self.__played_cards.__len__()

    def get_list_index_action(self, state: list):
        list_all_action_code = self.__full_action.copy()
        if self.check_victory(state) == -1:
            action_space = self.get_action_space_from_list_state(state)
            list_action = []
            for key in action_space:
                list_action += action_space[key]
            
            list_action_code = []
            for action in list_action:
                hand_name = action['hand_name']
                hand_score = action['hand_score']
                list_action_code.append(f'{hand_name}_{hand_score}')

            return [list_all_action_code.index(action_code) for action_code in list_action_code]
        
        return [0]

    def check_victory(self, state: list):
        temp = state[106:110]
        if min(temp) == 0:
            if temp[0] == 0:
                return 1

            return 0

        return -1

    def get_action_space_from_list_state(self, state: list):
        my_list_card = [Card(i) for i in range(52) if state[54:106][i] == 1]
        turn_card_owner = state[114]
        _temp_ = [f'{k}_of_a_kind' for k in [3,4]]\
                + [f'{k}_pairs_straight' for k in [3,4]]\
                + [f'{k}_straight' for k in range(3,12)]\
                + ['Single', 'Pair', 'Nothing']

        hand_name = _temp_[state[52]]
        hand_score = state[53]

        if turn_card_owner == 0 or hand_name == 'Nothing':
            return self.action_space(
                my_list_card,
                {'list_card': [], 'hand_name': 'Nothing', 'hand_score': -1},
                self.name
            )

        return self.action_space(
            my_list_card,
            {'list_card': [], 'hand_name': hand_name, 'hand_score': hand_score},
            'NotMe132465'
        )

    def action_space(self, list_card: list, board_turn_cards: dict, board_turn_cards_owner: str):
        possible_action = self.possible_action(list_card)
        action_space = {}

        if board_turn_cards['hand_name'] == 'Nothing' or board_turn_cards_owner == self.name:
            return possible_action
        
        list_hand_name = []
        if board_turn_cards['hand_name'] in ['Single', 'Pair', '3_of_a_kind']\
                                            + [f'{k}_straight' for k in range(3,12)]:
            if board_turn_cards['hand_score'] <= 47:
                list_hand_name += [board_turn_cards['hand_name']]
            else:
                if board_turn_cards['hand_name'] == 'Single':
                    list_hand_name += ['Single', '4_of_a_kind']\
                                    + [f'{k}_pairs_straight' for k in [3,4]]
                elif board_turn_cards['hand_name'] == 'Pair':
                    list_hand_name += ['Pair', '4_of_a_kind', '4_pairs_straight']
                else:
                    pass
            
            list_hand_name.append('Nothing')
            list_keys = list(possible_action.keys())
            for hand_name in list_hand_name:
                if hand_name in list_keys:
                    if hand_name == board_turn_cards['hand_name']:
                        temp_list = [action for action in possible_action[hand_name] if action['hand_score'] > board_turn_cards['hand_score']]
                        if temp_list.__len__() > 0:
                            action_space[hand_name] = temp_list.copy()
                    else:
                        action_space[hand_name] = possible_action[hand_name].copy()

            return action_space
        
        if board_turn_cards['hand_name'] == '3_pairs_straight':
            list_hand_name += [f'{k}_pairs_straight' for k in [3,4]] + ['4_of_a_kind']
        elif board_turn_cards['hand_name'] == '4_of_a_kind':
            list_hand_name += ['4_of_a_kind', '4_pairs_straight']
        elif board_turn_cards['hand_name'] == '4_pairs_straight':
            list_hand_name += ['4_pairs_straight']
        else:
            pass
        
        list_hand_name.append('Nothing')
        list_keys = list(possible_action.keys())
        for hand_name in list_hand_name:
            if hand_name in list_keys:
                if hand_name == board_turn_cards['hand_name']:
                    temp_list = [action for action in possible_action[hand_name] if action['hand_score'] > board_turn_cards['hand_score']]
                    if temp_list.__len__() > 0:
                        action_space[hand_name] = temp_list.copy()
                else:
                    action_space[hand_name] = possible_action[hand_name].copy()

        return action_space

    def possible_action(self, list_card: list):
        possible_action = {}
        list_hand_name = [f'{k}_of_a_kind' for k in [3,4]]\
                        + [f'{k}_pairs_straight' for k in [3,4]]\
                        + [f'{k}_straight' for k in range(3,12)]\
                        + ['Single', 'Pair', 'Nothing']

        for hand_name in list_hand_name:
            list_action = self.list_card_hand(list_card, hand_name)
            if list_action.__len__() != 0:
                possible_action[hand_name] = list_action.copy()
            
        return possible_action

    def get_list_state(self, dict_input: dict):
        # Các lá bài đã đánh trên bàn 0 51
        list_played_card = [card.stt for card in dict_input['Board'].played_cards]
        temp_1 = [1 if i in list_played_card else 0 for i in range(52)]

        # Bộ hiện tại cần chặn 52 53
        _temp_ = [f'{k}_of_a_kind' for k in [3,4]]\
                + [f'{k}_pairs_straight' for k in [3,4]]\
                + [f'{k}_straight' for k in range(3,12)]\
                + ['Single', 'Pair', 'Nothing']

        hand_name_index = _temp_.index(dict_input['Board'].turn_cards['hand_name'])
        hand_name_score = dict_input['Board'].turn_cards['hand_score']

        # Các lá bài của bản thân 54 105
        turn_player_cards = [card.stt for card in dict_input['Turn_player_cards']]
        temp_3 = [1 if i in turn_player_cards else 0 for i in range(52)]

        # Số lá bài còn lại của các người chơi theo góc nhìn agent 106 109
        temp_4_ = [13 for i in range(4)]
        for i in range(dict_input['Player'].__len__()):
            temp_4_[i] = dict_input['Player'][i].amount_cards_remaining

        list_player_name = [p.name for p in dict_input['Player']]
        my_id = list_player_name.index(self.name)
        temp_4 = temp_4_[my_id:] + temp_4_[:my_id]

        # Tình trạng bỏ vòng 110 113
        temp_5_ = [0 for i in range(4)]
        for i in dict_input['Playing_id']:
            temp_5_[i] = 1

        temp_5 = temp_5_[my_id:] + temp_5_[:my_id]

        # Chủ nhân của bài trên bàn, 0 nếu là mình 114
        temp_6 = -1
        try:
            temp_6 = list_player_name.index(dict_input['Board'].turn_cards_owner)
        except:
            temp_6 = -1

        if temp_6 != -1:
            if my_id <= temp_6:
                temp_6 -= my_id
            else:
                temp_6 = (4-my_id) + temp_6

        return temp_1 + [hand_name_index, hand_name_score] + temp_3 + temp_4 + temp_5 + [temp_6]

    def list_card_hand(self, _list_card: list, hand_name: str):
        list_return = []
        list_card = _list_card.copy()
        list_card.sort(key=lambda x:x.stt)

        if hand_name == 'Nothing':
            list_return.append({
                'list_card': [],
                'hand_name': 'Nothing',
                'hand_score': -1
            })

        elif hand_name == 'Single':
            list_return += [{
                'list_card': [card],
                'hand_name': 'Single',
                'hand_score': card.stt
            } for card in list_card]

        elif hand_name == 'Pair' or hand_name.endswith('_of_a_kind'):
            n = None
            if hand_name == 'Pair':
                n = 2
            else:
                n = int(hand_name.split('_of_a_kind')[0])

            for i in range(13):
                temp_list = [card for card in list_card if card.score == i]
                if temp_list.__len__() >= n:
                    _temp_list_ = temp_list[:n-1]
                    for j in range(n-1, temp_list.__len__()):
                        list_return.append({
                            'list_card': _temp_list_ + [temp_list[j]],
                            'hand_name': 'Pair' if n == 2 else f'{n}_of_a_kind',
                            'hand_score': temp_list[j].stt
                        })

        elif hand_name.endswith('_pairs_straight'):
            n = int(hand_name.split('_pairs_straight')[0])
            list_score = []
            _list_score_ = []

            for i in range(12):
                temp_list = [card for card in list_card if card.score == i]
                if temp_list.__len__() >= 2:
                    list_score.append(i)
                    _list_score_.append(temp_list)

            list_straight_arr = list_straight_subsequence(list_score, n)
            if list_straight_arr.__len__() > 0:
                for straight_arr in list_straight_arr:
                    index_arr = [list_score.index(i) for i in straight_arr]
                    list_max_pair = []
                    max_score_cards = _list_score_[index_arr[n-1]]
                    temp_list = [max_score_cards[0]]
                    for i in range(1, max_score_cards.__len__()):
                        list_max_pair.append(temp_list + [max_score_cards[i]])
                    
                    temp_list = []
                    for i in index_arr[:n-1]:
                        temp_list += _list_score_[i][:2]

                    for pair in list_max_pair:
                        list_return.append({
                            'list_card': temp_list + pair,
                            'hand_name': f'{n}_pairs_straight',
                            'hand_score': pair[1].stt
                        })

        elif hand_name.endswith('_straight'):
            n = int(hand_name.split('_straight')[0])
            list_score = []
            _list_score_ = []

            for i in range(12):
                temp_list = [card for card in list_card if card.score == i]
                if temp_list.__len__() >= 1:
                    list_score.append(i)
                    _list_score_.append(temp_list)

            list_straight_arr = list_straight_subsequence(list_score, n)
            if list_straight_arr.__len__() > 0:
                for straight_arr in list_straight_arr:
                    index_arr = [list_score.index(i) for i in straight_arr]
                    max_score_cards = _list_score_[index_arr[n-1]]
                    temp_list = []
                    for i in index_arr[:n-1]:
                        temp_list.append(_list_score_[i][0])

                    for card in max_score_cards:
                        list_return.append({
                            'list_card': temp_list + [card],
                            'hand_name': f'{n}_straight',
                            'hand_score': card.stt
                        })

        return list_return

def list_straight_subsequence(list_int: list, k: int):
    n = list_int.__len__()
    if k <= 2 or n < k:
        return []
        
    list_return = []
    for i in range(0, n-k+1):
        sub_list = list_int[i:i+k]
        if max(sub_list) - min(sub_list) == k-1:
            list_return.append(sub_list)

    return list_return