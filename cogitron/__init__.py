from cogitron import arms
from cogitron.arms import leader_arm, follower_arm


config_leader = {
    "Velocity_I_Gain":1000,
    "Velocity_P_Gain":100,
    "Position_P_Gain":640,
    "Position_D_Gain":4000,
    "Position_I_Gain":0,
}

config_follower = {
    "Velocity_I_Gain":1000,
    "Velocity_P_Gain":100,
    "Position_P_Gain":640,
    "Position_D_Gain":4000,
    "Position_I_Gain":0,
}

def initialize_arms():
    try:
        for key, value in config_leader.items():
            leader_arm.write(key, value)
        for key, value in config_follower.items():
            follower_arm.write(key, value)
    except Exception as e:
        print("Error while initializing arms")
