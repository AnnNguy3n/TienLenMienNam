from colorama import Fore, Style
import gym
import random
import pandas
from gym_TLMN.envs.base.board import Board
from gym_TLMN.envs.base.card import Card
from gym_TLMN.envs.base.player import Player
from gym_TLMN.envs.agents import agent_interface

def p_rint_horizontal_lines():
    print('----------------------------------------------------------------------------------------------------')
    pass

def p_rint_list_card(list_card: list):
    for i in range(list_card.__len__()):
        print(Fore.LIGHTMAGENTA_EX + str(i), end='. ')
        print(Fore.LIGHTWHITE_EX + list_card[i].name, Fore.LIGHTCYAN_EX + str(list_card[i].stt), end=', ')
        pass
        
    print(Style.RESET_ALL)


class TLMN_Env(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.__full_action = list(pandas.read_csv('gym_TLMN/envs/action_space.csv')['action_code'])
        self.board = Board()
        self.reset()

    def reset(self):
        self.board.reset()
        temp = random.sample([i for i in range(agent_interface.lst.__len__())], k=min(agent_interface.lst.__len__(), 4))
        self.players = [agent_interface.lst[i].Agent(agent_interface.lst_name[i]) for i in temp]
        self.players_cards = {}
        for i in range(temp.__len__()):
            self.players_cards[self.players[i].name] = []
        
        self.turn = random.choice(self.players)
        self.p_name_victory = 'None'

        self.dict_input = {
            'Board': self.board,
            'Player': self.players,
            'Playing_id': [i for i in range(temp.__len__())],
            'Turn_id': self.players.index(self.turn),
            'Turn_player_cards': []
        }

        self.setup_board()

    def setup_board(self):
        hidden_cards = [Card(i) for i in range(52)]
        total_play_cards = self.players.__len__() * 13
        self.admin = Player('ADMIN')
        reset_deal_cards = True
        while reset_deal_cards:
            random.shuffle(hidden_cards)
            i = 0
            for player in self.players:
                temp_list = [hidden_cards[j] for j in range(total_play_cards) if j % self.players.__len__() == i]
                temp_list.sort(key=lambda x:x.stt)

                # Ki???m tra t??? qu?? 2
                check_list = self.admin.list_card_hand(temp_list, '4_of_a_kind')
                if check_list.__len__() != 0 and max(i['hand_score'] for i in check_list) >= 48:
                    print(Fore.LIGHTYELLOW_EX + f'{player.name} c?? t??? qu?? Hai n??n chia l???i b??i', end='')
                    print(Style.RESET_ALL)
                    p_rint_list_card(temp_list)
                    reset_deal_cards = True
                    break

                # Ki???m tra 5 ????i th??ng
                check_list = self.admin.list_card_hand(temp_list, '5_pairs_straight')
                if check_list.__len__() != 0:
                    print(Fore.LIGHTYELLOW_EX + f'{player.name} c?? 5 ????i th??ng n??n chia l???i b??i', end='')
                    print(Style.RESET_ALL)
                    p_rint_list_card(temp_list)
                    reset_deal_cards = True
                    break

                # Ki???m tra s???nh r???ng
                check_list = self.admin.list_card_hand(temp_list, '12_straight')
                if check_list.__len__() != 0:
                    print(Fore.LIGHTYELLOW_EX + f'{player.name} s???nh r???ng n??n chia l???i b??i', end='')
                    print(Style.RESET_ALL)
                    p_rint_list_card(temp_list)
                    reset_deal_cards = True
                    break
                
                self.players_cards[player.name] = temp_list.copy()
                reset_deal_cards = False
                i += 1

        self.board._Board__hidden_cards = hidden_cards[total_play_cards:]
        self.dict_input['Turn_player_cards'] = self.players_cards[self.turn.name]
        # p_rint_horizontal_lines()

    def close(self):
        if self.p_name_victory != 'None':
            return True

        temp_arr = [self.players_cards[player.name].__len__() for player in self.players]
        if min(temp_arr) == 0:
            for player in self.players:
                if self.players_cards[player.name].__len__() == 0:
                    self.p_name_victory = player.name
                    break

            return True
        
        return False

    def render(self, mode="human", close=False):
        p_rint_horizontal_lines()
        p_rint_list_card(self.dict_input['Turn_player_cards'])
        pass

    def step(self, action_player):
        if self.close():
            self.process([])
            return self, None, True, None

        else:
            if type(action_player) == list:
                self.process(action_player)
            
            else:
                if action_player == 0:
                    self.process([])
                else:
                    action_code = self.__full_action[action_player]
                    temp = action_code.split('_')
                    hand_score = int(temp[-1])
                    hand_name = '_'.join(temp[:temp.__len__() - 1])
                    list_action = self.admin.list_card_hand(self.players_cards[self.turn.name], hand_name)
                    check = False
                    for act in list_action:
                        if act['hand_name'] == hand_name and act['hand_score'] == hand_score:
                            self.process(act['list_card'])
                            check = True
                            break

                    if not check:
                        print(Fore.LIGHTRED_EX + 'Index action kh??ng ????ng: ' + str(action_player), end='')
                        print(Style.RESET_ALL)
                        input(Fore.LIGHTYELLOW_EX + 'Action ng?????i ch??i ??ang ch??a ????ng, nh???n ph??m b???t k?? ????? b??? qua d??ng c???nh b??o n??y!'.upper() + Style.RESET_ALL)
                        self.process([])

            done = self.close()
            if done:
                p_rint_horizontal_lines()
                print(Fore.LIGHTYELLOW_EX + 'Ch??c m???ng ' + str(self.p_name_victory)+' l?? ng?????i chi???n th???ng', end='')
                print(Style.RESET_ALL)

                self.board._Board__turn_cards = {'list_card': [], 'hand_name': 'Nothing', 'hand_score': -1}
                self.board._Board__turn_cards_owner = 'None'
                self.dict_input['Playing_id'] = [i for i in range(self.players.__len__())]

            return self, None, done, None

    def process(self, action_player: list):
        check_, score = self.check_action(action_player, self.dict_input['Turn_player_cards'])
        val_list_action = [i.stt for i in action_player]
        
        def _p_rint_list_card_(action_player, check_):
            for i in action_player:
                print(Fore.LIGHTBLUE_EX + i.name, Fore.LIGHTCYAN_EX + str(i.stt), end=', ')
                pass   

            print(Fore.LIGHTGREEN_EX + 'Type: ' + check_, end='')
            print(Style.RESET_ALL)

        if self.board.turn_cards['list_card'].__len__() == 0 or self.board.turn_cards_owner == self.turn.name: # Kh???i ?????u v??ng ch??i m???i
            if check_ == 'Nothing' or check_ == 'Error_input': # Kh??ng ????nh g?? ho???c ?????u v??o l???i
                if check_ == 'Nothing':
                    print(Fore.LIGHTCYAN_EX + self.turn.name + Fore.LIGHTGREEN_EX + ' kh???i ?????u v??ng m???i nh??ng kh??ng ????nh g??', end='')
                    pass
                else:
                    print(Fore.LIGHTCYAN_EX + self.turn.name + Fore.LIGHTYELLOW_EX + ' ????nh b??i l???i n??n m???t quy???n kh???i ?????u v??ng', end='')
                    pass
                
                print(Style.RESET_ALL)
                if check_ == 'Error_input':
                    input(Fore.LIGHTYELLOW_EX + 'Action ng?????i ch??i ??ang ch??a ????ng, nh???n ph??m b???t k?? ????? b??? qua d??ng c???nh b??o n??y!'.upper() + Style.RESET_ALL)
                    pass

                # Thay ?????i th??? tr??n b??n ch??i
                self.board._Board__turn_cards = {'list_card': [], 'hand_name': 'Nothing', 'hand_score': -1}
                self.board._Board__turn_cards_owner = 'None'
            
            else: # ?????u v??o ????ng
                print(Fore.LIGHTCYAN_EX + self.turn.name + Fore.LIGHTGREEN_EX + ' kh???i ?????u v??ng m???i v???i: ', end='')
                _p_rint_list_card_(action_player, check_)

                # C???p nh???t c??c l?? b??i c???a ng?????i v???a ????nh b??i
                self.players_cards[self.turn.name] = [i for i in self.dict_input['Turn_player_cards'] if i.stt not in val_list_action]

                # Th??m v??o list c??c th??? ???? ????nh
                self.players[self.dict_input['Turn_id']]._Player__played_cards += action_player
                self.board._Board__played_cards += action_player

                # Thay ?????i th??? tr??n b??n ch??i
                self.board._Board__turn_cards = {'list_card': action_player.copy(), 'hand_name': check_, 'hand_score': score}
                self.board._Board__turn_cards_owner = self.turn.name

            # Ng?????i ??i ti???p theo
            self.dict_input['Turn_id'] = (self.dict_input['Turn_id'] + 1) % self.players.__len__()
            self.turn = self.players[self.dict_input['Turn_id']]

            # Truy???n c??c l?? b??i c???a ng?????i ti???p theo v??o
            self.dict_input['Turn_player_cards'] = self.players_cards[self.turn.name]

        else: # Kh??ng ph???i kh???i ?????u v??ng m???i
            elimination = None # True: b??? lo???i kh???i v??ng v?? l?? do n??o ????, False: ch???t ???????c n??n kh??ng b??? lo???i kh???i v??ng

            # Kh??ng ????nh g?? ho???c ?????u v??o l???i
            if check_ == 'Nothing' or check_ == 'Error_input':
                if check_ == 'Nothing':
                    print(Fore.LIGHTCYAN_EX + self.turn.name + Fore.LIGHTGREEN_EX + ' kh??ng ch???t g?? n??n b??? lo???i kh???i v??ng', end='')
                    pass
                else:
                    print(Fore.LIGHTCYAN_EX + self.turn.name + Fore.LIGHTYELLOW_EX + ' ????nh b??i l???i n??n b??? lo???i kh???i v??ng', end='')
                    pass
                    
                print(Style.RESET_ALL)
                elimination = True

            # ????nh ????ng, c??ng lo???i v???i b??i hi???n t???i
            elif check_ == self.board.turn_cards['hand_name']:
                if score < self.board.turn_cards['hand_score']:
                    print(Fore.LIGHTCYAN_EX + self.turn.name + Fore.LIGHTYELLOW_EX + ' ????nh b??i th???p h??n n??n b??? lo???i kh???i v??ng: ', end='')
                    _p_rint_list_card_(action_player, check_)
                    input(Fore.LIGHTYELLOW_EX + 'Action ng?????i ch??i ??ang ch??a ????ng, nh???n ph??m b???t k?? ????? b??? qua d??ng c???nh b??o n??y!'.upper() + Style.RESET_ALL)
                    elimination = True
                else:
                    elimination = False

            # ????nh ????ng, kh??c lo???i v???i b??i hi???n t???i
            else:
                # 3 ????i th??ng ch???t ???????c 1 con 2
                if check_ == '3_pairs_straight' and self.board.turn_cards['hand_name'] == 'Single' and self.board.turn_cards['hand_score'] >= 48:
                    elimination = False

                # T??? qu?? ch???t ???????c 1 ho???c ????i 2, 3 ????i th??ng
                elif check_ == '4_of_a_kind':
                    # 1 ho???c ????i 2
                    if self.board.turn_cards['hand_score'] >= 48 and self.board.turn_cards['hand_name'] in ['Single', 'Pair']:
                        elimination = False
                    # 3 ????i th??ng
                    elif self.board.turn_cards['hand_name'] == '3_pairs_straight':
                        elimination = False

                    else:
                        elimination = True

                # 4 ????i th??ng ch???t ???????c 1 ho???c ????i 2, t??? qu??, 3 ????i th??ng
                elif check_ == '4_pairs_straight':
                    # 1 ho???c ????i 2
                    if self.board.turn_cards['hand_score'] >= 48 and self.board.turn_cards['hand_name'] in ['Single', 'Pair']:
                        elimination = False
                    # 3 ????i th??ng
                    elif self.board.turn_cards['hand_name'] == '3_pairs_straight':
                        elimination = False
                    # T??? qu??
                    elif self.board.turn_cards['hand_name'] == '4_of_a_kind':
                        elimination = False

                    else:
                        elimination = True
                else:
                    elimination = True

            if elimination: # B??? lo???i kh???i v??ng ch??i
                if (check_ != 'Nothing') and (check_ != 'Error_input') and check_ != self.board.turn_cards ['hand_name']:
                    print(Fore.LIGHTCYAN_EX + self.turn.name + Fore.LIGHTYELLOW_EX + ' ch???t b??i kh??ng ph?? h???p n??n b??? lo???i kh???i v??ng: ', end='')
                    _p_rint_list_card_(action_player, check_)
                    input(Fore.LIGHTYELLOW_EX + 'Action ng?????i ch??i ??ang ch??a ????ng, nh???n ph??m b???t k?? ????? b??? qua d??ng c???nh b??o n??y!'.upper() + Style.RESET_ALL)
                    pass

                # B??? ng?????i ch??i n??y kh???i v??ng
                indexx = self.dict_input['Playing_id'].index(self.dict_input['Turn_id'])
                self.dict_input['Playing_id'].remove(self.dict_input['Turn_id'])

                # X??c ?????nh ng?????i ??i ti???p theo
                self.dict_input['Turn_id'] = self.dict_input['Playing_id'][indexx % self.dict_input['Playing_id'].__len__()]
                self.turn = self.players[self.dict_input['Turn_id']]

                # Truy???n v??o c??c l?? b??i c???a ng?????i ti???p theo v??o
                self.dict_input['Turn_player_cards'] = self.players_cards[self.turn.name]

                # N???u c??n duy nh???t m???t ng?????i trong Playing_id th?? th??m l???i t???t c??? ng?????i ch??i v??o
                if self.dict_input['Playing_id'].__len__() == 1:
                    self.dict_input['Playing_id'] = [i for i in range(self.players.__len__())]

            else: # Ch???t ???????c b??i tr??n b??n
                print(Fore.LIGHTCYAN_EX + self.turn.name + Fore.LIGHTGREEN_EX + ' ch???t b??i v???i: ', end='')
                _p_rint_list_card_(action_player, check_)

                # C???p nh???t c??c l?? b??i c???a ng?????i v???a ????nh b??i
                self.players_cards[self.turn.name] = [i for i in self.dict_input['Turn_player_cards'] if i.stt not in val_list_action]

                # Th??m v??o list c??c th??? ???? ????nh
                self.players[self.dict_input['Turn_id']]._Player__played_cards += action_player
                self.board._Board__played_cards += action_player

                # Thay ?????i th??? tr??n b??n ch??i
                self.board._Board__turn_cards = {'list_card': action_player.copy(), 'hand_name': check_, 'hand_score': score}
                self.board._Board__turn_cards_owner = self.turn.name

                # N???u b??i v???a ????nh ra li??n quan ?????n c??c l?? '2' ho???c d??y ????i th??ng, t??? qu?? th?? t???t c??? ng?????i ch??i ???????c th??m l???i v??o v??ng
                if score >= 48 or check_ in ['4_of_a_kind', '3_pairs_straight', '4_pairs_straight']:
                    self.dict_input['Playing_id'] = [i for i in range(self.players.__len__())]

                # X??c ?????nh ng?????i ??i ti???p theo
                indexx = self.dict_input['Playing_id'].index(self.dict_input['Turn_id'])
                self.dict_input['Turn_id'] = self.dict_input['Playing_id'][(indexx+1) % self.dict_input['Playing_id'].__len__()]
                self.turn = self.players[self.dict_input['Turn_id']]

                # Truy???n v??o c??c l?? b??i c???a ng?????i ti???p theo v??o
                self.dict_input['Turn_player_cards'] = self.players_cards[self.turn.name]

    def check_action(self, action_player: list, list_card: list):
        len_ = action_player.__len__()
        if len_ == 0:
            return 'Nothing', -1

        v_list = [i.score for i in action_player]
        val_list = [i.stt for i in action_player]

        def _p_rint_list_card(action_player):
            for i in action_player:
                print(Fore.RED + str(i.name) + ', ', end='')
                pass

            print(Style.RESET_ALL)

        # Ki???m tra xem c?? 2 l?? b??i n??o tr??ng hay kh??ng
        temp_list = []
        for i in val_list:
            if i in temp_list:
                print(Fore.LIGHTRED_EX + 'C?? hai th??? b??i tr??ng nhau: ', end='')
                _p_rint_list_card(action_player)
                return 'Error_input', -7
            
            temp_list.append(i)

        # Ki???m tra xem c??c l?? b??i c?? ph???i c???a ng?????i ch??i hi???n t???i kh??ng
        temp_list = [i.stt for i in list_card]
        for i in val_list:
            if i not in temp_list:
                print(Fore.LIGHTRED_EX + 'C?? ??t nh???t 1 th??? b??i kh??ng ph???i c???a ng?????i ch??i hi???n t???i: ', end='')
                _p_rint_list_card(action_player)
                # input(Fore.LIGHTYELLOW_EX + 'Action ng?????i ch??i ??ang ch??a ????ng, nh???n ph??m b???t k?? ????? b??? qua d??ng c???nh b??o n??y!'.upper() + Style.RESET_ALL)
                return 'Error_input', -7

        if len_ == 1:
            return 'Single', action_player[0].stt

        if len_ == 2:
            if self.admin.list_card_hand(action_player, 'Pair').__len__() != 0:
                return 'Pair', max(val_list)

            print(Fore.LIGHTRED_EX + 'D???ng b??i kh??ng ????ng: ', end='')
            _p_rint_list_card(action_player)
            # input(Fore.LIGHTYELLOW_EX + 'Action ng?????i ch??i ??ang ch??a ????ng, nh???n ph??m b???t k?? ????? b??? qua d??ng c???nh b??o n??y!'.upper() + Style.RESET_ALL)
            return 'Error_input', -7

        # Ki???m tra xem c?? ph???i l?? s???nh
        if max(v_list) - min(v_list) == (len_-1) and max(v_list) != 12:
            if self.admin.list_card_hand(action_player, f'{len_}_straight').__len__() != 0:
                return f'{len_}_straight', max(val_list)

        # Ki???m tra xem c?? ph???i b??? ba ho???c t??? qu??
        if max(v_list) == min(v_list):
            return f'{len_}_of_a_kind', max(val_list)

        # Ki???m tra d??y ????i th??ng
        if len_ % 2 == 0 and len_ >= 6:
            if self.admin.list_card_hand(action_player, f'{len_//2}_pairs_straight').__len__() != 0:
                return f'{len_//2}_pairs_straight', max(val_list)

        print(Fore.LIGHTRED_EX + 'D???ng b??i kh??ng ????ng: ', end='')
        _p_rint_list_card(action_player)
        # input(Fore.LIGHTYELLOW_EX + 'Action ng?????i ch??i ??ang ch??a ????ng, nh???n ph??m b???t k?? ????? b??? qua d??ng c???nh b??o n??y!'.upper() + Style.RESET_ALL)
        return 'Error_input', -7