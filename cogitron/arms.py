import subprocess
import dynamixel_sdk as dxl
from lerobot.teleoperators.koch_leader.koch_leader import KochLeader, KochLeaderConfig
from lerobot.robots.koch_follower import KochFollower, KochFollowerConfig
from cogitron import config
from pathlib import Path
from cogitron.query_device import get_device_id
from cogitron.camera import get_camera_config
from cogitron.filecache import filecache

PROTOCOL_VERSION = 2.0
TIMEOUT_MS = 1000
ADDRESS_MODEL_NUMBER = 0
DATA_SIZE_MODEL_NUMBER = 2

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


leader_arm_key = tuple(map(lambda x:model_numbers[x[1]], leader_arm_motors.values()))
follower_arm_key = tuple(map(lambda x:model_numbers[x[1]], follower_arm_motors.values()))

follower_port, leader_port = None, None


def get_port_key(port):
    packet_handler = dxl.PacketHandler(PROTOCOL_VERSION)

    port_handler = dxl.PortHandler(port)
    port_handler.setPacketTimeoutMillis(TIMEOUT_MS)
    port_handler.openPort()
    
    if not port_handler.openPort():
        return None
    
    sync_reader = dxl.GroupSyncRead(port_handler, packet_handler, ADDRESS_MODEL_NUMBER, DATA_SIZE_MODEL_NUMBER)

    key = []
    
    for id in range(1,7):
        sync_reader.addParam(id)
        sync_reader.txRxPacket()
        
        model_number = sync_reader.getData(id, ADDRESS_MODEL_NUMBER, DATA_SIZE_MODEL_NUMBER)
        key.append(model_number)

        sync_reader.removeParam(id)
        
    key = tuple(key)

    return key


def validate_arm_ports(ports):
    follower_port, leader_port = ports
    current_follower_arm_key, current_leader_arm_key = get_port_key(follower_port), get_port_key(leader_port)
    is_valid = (current_follower_arm_key, current_leader_arm_key) == (follower_arm_key, leader_arm_key)
    return is_valid

@filecache(validation_function=validate_arm_ports)
def get_arm_ports():
    possible_arm_paths = Path("/dev").glob("ttyACM*")
    possible_arm_paths = [str(path) for path in possible_arm_paths]
    arm_paths = list(filter(lambda path:get_device_id(path)==config.ROBOT_ARM_USB_ID, possible_arm_paths))

    packet_handler = dxl.PacketHandler(PROTOCOL_VERSION)

    for port in arm_paths:
        port_handler = dxl.PortHandler(port)
        port_handler.setPacketTimeoutMillis(TIMEOUT_MS)
        port_handler.openPort()
        
        if not port_handler.openPort():
            raise OSError(f"Failed to open port '{port}'.")
        
        sync_reader = dxl.GroupSyncRead(port_handler, packet_handler, ADDRESS_MODEL_NUMBER, DATA_SIZE_MODEL_NUMBER)

        key = []
        
        for id in range(1,7):
            sync_reader.addParam(id)
            sync_reader.txRxPacket()
            
            model_number = sync_reader.getData(id, ADDRESS_MODEL_NUMBER, DATA_SIZE_MODEL_NUMBER)
            key.append(model_number)

            sync_reader.removeParam(id)
            
        key = tuple(key)
        
        global follower_port, leader_port

        if key==leader_arm_key:
            leader_port = port
        elif key==follower_arm_key:
            follower_port = port

        port_handler.closePort()
    
    return (follower_port, leader_port)


def get_follower_arm():
    global follower_port, leader_port
    
    if follower_port is None:
        follower_port, leader_port = get_arm_ports()
    
    camera_config = {
        "front": get_camera_config()
    }
    
    robot_config = KochFollowerConfig(
        port=follower_port,
        id="follower_arm",
        cameras=camera_config,
    )
     
    return KochFollower(robot_config)

def get_leader_arm():
    global follower_port, leader_port
    
    if leader_port is None:
        follower_port, leader_port = get_arm_ports()

    teleop_config = KochLeaderConfig(
        port=leader_port,
        id="leader_arm",
    )
    
    return KochLeader(teleop_config)


def reboot(port_handler:dxl.PortHandler):
    packet_handler:dxl.Protocol2PacketHandler = dxl.packet_handler.PacketHandler(PROTOCOL_VERSION)
    
    if(not port_handler.is_open):
        port_handler.openPort()

    for id in range(1,7):
        packet_handler.reboot(port_handler, id)

    port_handler.closePort()
