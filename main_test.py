from copy import deepcopy
import gym
from collections import Counter
import gym_TLMN
import time
from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

env = gym.make('gym_TLMN-v0')

def main():
    env.reset()

    # print([i.name for i in env.players])

    for i in range(500):
        env.render()

        o,a,done,t = env.step(env.turn.action(deepcopy(env.dict_input)))
        if done:
            break

    for i in range(env.players.__len__()):
        env.render()

        o,a,done,t = env.step(env.turn.action(deepcopy(env.dict_input)))
    
    print(env.p_name_victory)
    return env.p_name_victory

count = {}
for van in range(100):
    with suppress_stdout():
        name = main()
    if name in count.keys():
        count[name] += 1
    else:
        count[name] = 1
    print(count)