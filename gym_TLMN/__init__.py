from gym.envs.registration import register

register(
    id = 'gym_TLMN-v0',    
    entry_point = 'gym_TLMN.envs:TLMN_Env',
)