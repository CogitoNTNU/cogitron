import sys
import os
from time import sleep
from numpy import array, int32
import numpy as np
import subprocess
sys.path.append(os.path.abspath("."))

from lerobot.common.robot_devices.motors.dynamixel import DynamixelMotorsBus
from lerobot.common.robot_devices.motors.dynamixel import TorqueMode
from lerobot.common.robot_devices.robots.manipulator import ManipulatorRobotConfig
from lerobot.common.robot_devices.robots.manipulator import ManipulatorRobot

import dynamixel_sdk as dxl



leader_arm_motors = {
    # name: (index, model)
    "shoulder_pan": (1, "xl330-m077"),
    "shoulder_lift": (2, "xl330-m077"),
    "elbow_flex": (3, "xl330-m077"),
    "wrist_flex": (4, "xl330-m077"),
    "wrist_roll": (5, "xl330-m077"),
    "gripper": (6, "xl330-m077"),
}

follower_arm_motors = {
    # name: (index, model)
    "shoulder_pan": (1, "xl430-w250"),
    "shoulder_lift": (2, "xl430-w250"),
    "elbow_flex": (3, "xl330-m288"),
    "wrist_flex": (4, "xl330-m288"),
    "wrist_roll": (5, "xl330-m288"),
    "gripper": (6, "xl330-m288"),
}


model_numbers = {
    "xl330-m077":1_190,
    "xl430-w250":1_060,
    "xl330-m288":1_200,
}


leader_arm_key = tuple(map(lambda x:model_numbers[x[1]], leader_arm_motors))
follower_arm_key = tuple(map(lambda x:model_numbers[x[1]], leader_arm_motors))


PROTOCOL_VERSION = 2.0
TIMEOUT_MS = 1000
ADDRESS_MODEL_NUMBER = 0
COMM_SUCCESS = 0 # Communication Success result value
COMM_TX_FAIL = -1001 # Communication Tx Failed
USB_DECODER_ID = "0000:0000" # Place holder. TODO: Change to actual value of decoder.



usb_device_ports = subprocess.run(f"lsusb | grep {USB_DECODER_ID} | sed -r 's/Bus (.*) Device (.*): .*$/\/dev\/bus\/usb\/\1\/\2/'", shell=True, capture_output=True).stdout.decode().split("\n")


packet_handler = dxl.PacketHandler(PROTOCOL_VERSION)

for port in usb_device_ports:
    port_handler = dxl.PortHandler(port)
    port_handler.setPacketTimeoutMillis(TIMEOUT_MS)

    if not port_handler.openPort():
        raise OSError(f"Failed to open port '{port}'.")
    
    key = []
    
    for id in range(1,7):
        model_number = dxl.read4ByteTxRx(port_handler, PROTOCOL_VERSION, id, ADDRESS_MODEL_NUMBER)
        
        if dxl.getLastTxRxResult(port_handler, PROTOCOL_VERSION) != COMM_SUCCESS:
            dxl.printTxRxResult(PROTOCOL_VERSION, dxl.getLastTxRxResult(port_handler, PROTOCOL_VERSION))
            raise
        elif dxl.getLastRxPacketError(port_handler, PROTOCOL_VERSION) != 0:
            dxl.printRxPacketError(PROTOCOL_VERSION, dxl.getLastRxPacketError(port_handler, PROTOCOL_VERSION))
            raise
        
        key.append(model_number)
        
    key = tuple(key)
    
    
    if key==leader_arm_key:
        leader_port = port
    elif key==follower_arm_key:
        follower_port = port

    port_handler.closePort()




leader_arm = DynamixelMotorsBus(
    port=leader_port,
    motors=leader_arm_motors,
)

follower_arm = DynamixelMotorsBus(
    port=follower_port,
    motors=follower_arm_motors,
)


robot_config = ManipulatorRobotConfig(
    robot_type="koch",
    leader_arms={"main": leader_arm},
    follower_arms={"main": follower_arm},
    cameras={},  # We don't use any camera for now
)


robot = ManipulatorRobot(robot_config)

