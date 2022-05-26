from copy import deepcopy
import gym
import gym_TLMN
import time
from collections import Counter

env = gym.make('gym_TLMN-v0')

def main():
    env.reset()

    # print([i.name for i in env.players])

    for i in range(100):
        env.render()

        o,a,done,t = env.step(env.turn.action(deepcopy(env.dict_input)))
        if done:
            break

    for i in range(env.players.__len__()):
        env.render()

        o,a,done,t = env.step(env.turn.action(deepcopy(env.dict_input)))
    print(env.p_name_victory)
for i in range(1):
    main() 
# while main() != 'Dong':
#     print('Thua')
# for i in range(1):
#     print(i)
#     main()

# end = time.time()
# print(end - start, 'sec')