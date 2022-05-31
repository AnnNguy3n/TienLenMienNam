# from gym_TLMN.envs.agents import S_a as p1
# from gym_TLMN.envs.agents import S_a as p2
# from gym_TLMN.envs.agents import S_a as p3
# from gym_TLMN.envs.agents import S_a as p4

# agent1 = p1.Agent('1')
# agent2 = p2.Agent('2')
# agent3 = p3.Agent('3')
# agent4 = p4.Agent('4')

from gym_TLMN.envs.agents import agent_random as p1
from gym_TLMN.envs.agents import random as p2
from gym_TLMN.envs.agents import random as p3
from gym_TLMN.envs.agents import random as p4

agent1 = p1.Agent('Phong')
agent2 = p2.Agent('Hiếu')
agent3 = p3.Agent('random1')
agent4 = p4.Agent('random2')

list_player = [agent1, agent2, agent3, agent4]