# from gym_TLMN.envs.agents import Phong as p1
# from gym_TLMN.envs.agents import Phong_cu as p2
# from gym_TLMN.envs.agents import Phong_cu as p3
# from gym_TLMN.envs.agents import Phong as p4

from gym_TLMN.envs.agents import random as p1
from gym_TLMN.envs.agents import random as p2
from gym_TLMN.envs.agents import random as p3
from gym_TLMN.envs.agents import random as p4

agent1 = p1.Agent('random1')
agent2 = p2.Agent('random2')
agent3 = p3.Agent('random3')
agent4 = p4.Agent('Phong_MA')

list_player = [agent1, agent2, agent3, agent4]