from copy import deepcopy
import gym
from collections import Counter
import gym_TLMN
import time
import pandas as pd

env = gym.make('gym_TLMN-v0')

def main():
    env.reset()

    print([i.name for i in env.players])

    for i in range(500):
        env.render()

        o,a,done,t = env.step(env.turn.action(deepcopy(env.dict_input)))
        if done:
            break

    for i in range(env.players.__len__()):
        env.render()

        o,a,done,t = env.step(env.turn.action(deepcopy(env.dict_input)))
    
    return env.p_name_victory

start = time.time()

print(Counter(main() for i in range(1)))

end = time.time()
print(end - start, 'sec')






def main(env):

    env.reset() 
    for i in range(500):
        env.render()
        o,a,done,t = env.step(env.turn.action(deepcopy(env.dict_input)))
        if done:
            break
    for i in range(env.players.__len__()):
        env.render()
        o,a,done,t = env.step(env.turn.action(deepcopy(env.dict_input)))

    dict_result = {}
    for p in env.dict_input['Player']:
        dict_result[p.name] = p.amount_cards_remaining
    sort_list = sorted(dict_result.items(), key=lambda x:x[1], reverse= False)
    sort_player = [item[0] for item in sort_list]
    sort_score = [item[1] for item in sort_list]
    return sort_player, sort_score


if __name__ == '__main__':
    env = gym.make('gym_TLMN-v0')
    try:
        result_for_elo = pd.read_csv('data_for_elo.csv')
    except:
        result_for_elo = pd.DataFrame({'player':[], 'score':[]})
    list_player = []
    list_score = []
   
    # for i in range(1, len(env.list_all_game)+1):
    for i in range(1, 10):
        print('Game', i)
        x, y = main(env)
        list_player.append(x)
        list_score.append(y)
    list_player = list(result_for_elo['player']) + list_player
    list_score = list(result_for_elo['score']) + list_score
    result_for_elo_new = pd.DataFrame()
    result_for_elo_new['player'] = list_player
    result_for_elo_new['score'] = list_score
    result_for_elo_new.to_csv('data_for_elo.csv', index= False)
