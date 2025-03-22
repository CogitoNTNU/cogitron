# import sys
# print(sys.path)

import sys
import os
sys.path.append(os.path.abspath("."))


from lerobot.common.robot_devices.motors.dynamixel import DynamixelMotorsBus

from time import sleep
from numpy import array, int32
import numpy as np

from lerobot.common.robot_devices.motors.dynamixel import TorqueMode

# sudo chmod 666 /dev/ttyACM2 /dev/ttyACM1

leader_port = "/dev/ttyACM1"
follower_port = "/dev/ttyACM0"

leader_arm = DynamixelMotorsBus(
    port=leader_port,
    motors={
        # name: (index, model)
        "shoulder_pan": (1, "xl330-m077"),
        "shoulder_lift": (2, "xl330-m077"),
        "elbow_flex": (3, "xl330-m077"),
        "wrist_flex": (4, "xl330-m077"),
        "wrist_roll": (5, "xl330-m077"),
        "gripper": (6, "xl330-m077"),
    },
)


follower_arm = DynamixelMotorsBus(
    port=follower_port,
    motors={
        # name: (index, model)
        "shoulder_pan": (1, "xl430-w250"),
        "shoulder_lift": (2, "xl430-w250"),
        "elbow_flex": (3, "xl330-m288"),
        "wrist_flex": (4, "xl330-m288"),
        "wrist_roll": (5, "xl330-m288"),
        "gripper": (6, "xl330-m288"),
    },
)

#positions = [array([1842, 2009, 1688, 3435, 2172, 4063], dtype=int32), array([1556, 2008, 1896, 3854, 2133, 4063], dtype=int32), array([1763, 1936, 2273, 4145, 2442, 4563], dtype=int32), array([2445, 1892, 2188, 3229, 2123, 4520], dtype=int32), array([1853, 2654, 2736, 4194, 1718, 4394], dtype=int32), array([1611, 1894, 2148, 3001, 2231, 4396], dtype=int32), array([1597, 1885, 1676, 4602, 1860, 4396], dtype=int32), array([1774, 1887, 2403, 3618, 2428, 4394], dtype=int32), array([1282, 1878, 2069, 3444, 1522, 4391], dtype=int32), array([1794, 2423, 2321, 4266, 2324, 4051], dtype=int32), array([1535, 2044, 1913, 3415, 2374, 4331], dtype=int32)]

#leader_arm.connect()
follower_arm.connect()

def follower_read():
    return follower_arm.read("Present_Position")

def follower_write(position):
    follower_arm.write("Goal_Position", position)

def leader_read():
    return leader_arm.read("Present_Position")

def leader_write(position):
    leader_arm.write("Goal_Position", position)



def follower_relax():
    follower_arm.write("Torque_Enable", TorqueMode.DISABLED.value)

def follower_flex():
    follower_arm.write("Torque_Enable", TorqueMode.ENABLED.value)

recorded_positions = []

def record_position():
    recorded_positions.append(follower_read())

def move(positions):
    follower_flex()

    for position in positions:
        follower_write(position)
        sleep(1)


def interpolate(a, b, x):
    return a*(1-x) + b*(x)



def dance():
    follower_flex()

    positions_min = np.array([983,2069,2376,5036,45, 4108])
    positions_max = np.array([3061,2517,2753,3659,4128,4695])

    t = 0
    delta_t = 0.001

    w = np.array([0.1,0.12,0.14,0.16,0.18,0.2])

    while True:
        t += delta_t

        position = interpolate(positions_min, positions_max, (np.sin(w*t) +1.)/2.)

        follower_write(position.astype(np.int32))


    #positions = [
    #array([2071, 2095, 1756, -530, 1914,   86], dtype=int32),
    #array([1633, 1821, 2504, -521, 1916,  475], dtype=int32),
    #array([1057, 1851, 1906, -522, 1916,  475], dtype=int32),
    #array([2019, 1772, 1779, -522, 1916,  475], dtype=int32),
    #]


def grip_package():
    move([array([2281, 1983, 2795, 3580, 2061,   94], dtype=int32), array([1812, 2172, 1743, 3592, 2007, 1087], dtype=int32), array([1925, 2175, 1735, 3588, 2084,  298], dtype=int32), array([2833, 1805, 2357, 3530, 2247,  227], dtype=int32), array([3011, 2194, 1784, 3641, 2452,  219], dtype=int32), array([2996, 2142, 1693, 3612, 2390, 1018], dtype=int32), array([2240, 2087, 2985, 3728, 1999,  -44], dtype=int32)])

#dance()

def write_stuff(variable, value):
    leader_arm.write(variable, value)