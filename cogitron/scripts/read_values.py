import sys
import os
from time import sleep
from numpy import array, int32
import numpy as np
sys.path.append(os.path.abspath("."))

from lerobot.common.robot_devices.motors.dynamixel import TorqueMode
from cogitron.arms import follower_arm, leader_arm

leader_arm.connect()
follower_arm.connect()

value_names = [
    "Model_Number",
    "Model_Information",
    "Firmware_Version",
    "ID",
    "Baud_Rate",
    "Return_Delay_Time",
    "Drive_Mode",
    "Operating_Mode",
    "Secondary_ID",
    "Protocol_Type",
    "Homing_Offset",
    "Moving_Threshold",
    "Temperature_Limit",
    "Max_Voltage_Limit",
    "Min_Voltage_Limit",
    "PWM_Limit",
    "Current_Limit",
    "Acceleration_Limit",
    "Velocity_Limit",
    "Max_Position_Limit",
    "Min_Position_Limit",
    "Shutdown",
    "Torque_Enable",
    "LED",
    "Status_Return_Level",
    "Registered_Instruction",
    "Hardware_Error_Status",
    "Velocity_I_Gain",
    "Velocity_P_Gain",
    "Position_D_Gain",
    "Position_I_Gain",
    "Position_P_Gain",
    "Feedforward_2nd_Gain",
    "Feedforward_1st_Gain",
    "Bus_Watchdog",
    "Goal_PWM",
    "Goal_Current",
    "Goal_Velocity",
    "Profile_Acceleration",
    "Profile_Velocity",
    "Goal_Position",
    "Realtime_Tick",
    "Moving",
    "Moving_Status",
    "Present_PWM",
    "Present_Current",
    "Present_Velocity",
    "Present_Position",
    "Velocity_Trajectory",
    "Position_Trajectory",
    "Present_Input_Voltage",
    "Present_Temperature",
]

leader_values = {}
follower_values = {}

values_leader = "cogitron/values_leader.txt"
values_follower = "cogitron/values_follower.txt"

def connect_arms():
    leader_arm.connect()
    follower_arm.connect()

def read_values_leader():
    for key in value_names:
        leader_values[key] =leader_arm.read(key)

def read_values_follower():
    for key in value_names:
        follower_values[key] = follower_arm.read(key)

def save_values_leader():
    with open(values_leader, "w") as f:
        f.write("Leader: \n")
        for key, value in leader_values.items():
            f.write(f"{key}: {value} \n")

def save_values_follower():
    with open(values_follower, "a") as f:
        f.write("Follower: \n")
        for key, value in follower_values.items():
            f.write(f"{key}: {value} \n")

def save_values():
    save_values_leader()
    save_values_follower()

def print_values():
    print("Leader: \n")
    for key, value in leader_values.items():
        print(f"{key}: {value} \n")
    print("Follower: \n")
    for key, value in follower_values.items():
        print(f"{key}: {value} \n")

def load_old_values():
    with open(values_leader, "r") as f:
        for line in f:
            key, value = line.split(": ")
            value = int(value)
            leader_values[key] = value
    with open(values_follower, "r") as f:
        for line in f:
            key, value = line.split(": ")
            value = int(value)
            follower_values[key] = value

def load_saved_values():
    for key in value_names:
        leader_arm.write(key, leader_values[key])
        follower_arm.write(key, follower_values[key])

def write_to_leader(key, value):
    leader_arm.write(key, value)
    leader_values[key] = value
    print(f"Leader {key}: {value} \n")

def write_to_follower(key, value):
    follower_arm.write(key, value)
    follower_values[key] = value
    print(f"Follower {key}: {value} \n")
