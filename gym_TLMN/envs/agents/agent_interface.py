from gym_TLMN.envs.agents import agent_B as p1
from gym_TLMN.envs.agents import agent_Hieu_new as p2
from gym_TLMN.envs.agents import agent_MA as p3
from gym_TLMN.envs.agents import agent_NA_ifelse as p4
from gym_TLMN.envs.agents import agent_random as p5
from gym_TLMN.envs.agents import agent_random_system as p6
from gym_TLMN.envs.agents import Phong_cu as p7

agent1 = p1.Agent('NA_RL')
agent2 = p2.Agent('Hieu')
agent3 = p3.Agent('M_Anh')
agent4 = p4.Agent('NA_ifelse')
agent5 = p5.Agent('PhongMinhAnh')
agent6 = p6.Agent('random')
agent7 = p7.Agent('Phongcu')

list_player = [agent1, agent2, agent3, agent4, agent5, agent6, agent7]

#####