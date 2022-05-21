from copy import deepcopy
import gym
from collections import Counter
import gym_TLMN
import time


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