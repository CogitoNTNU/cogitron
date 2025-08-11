import subprocess
import dynamixel_sdk as dxl
from lerobot.teleoperators.koch_leader import KochLeaderConfig, KochLeader
from lerobot.robots.koch_follower import KochFollowerConfig, KochFollower
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig
from config import FPS, CAMERA_WIDTH, CAMERA_HEIGHT

PROTOCOL_VERSION = 2.0
TIMEOUT_MS = 1000
ADDRESS_MODEL_NUMBER = 0
COMM_SUCCESS = 0 # Communication Success result value
COMM_TX_FAIL = -1001 # Communication Tx Failed
USB_DECODER_ID = "0000:0000" # Place holder. TODO: Change to actual value of decoder.


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
    

camera_config = {
    "front": OpenCVCameraConfig(index_or_path=0, width=CAMERA_WIDTH, height=CAMERA_HEIGHT, fps=FPS)
}

robot_config = KochFollowerConfig(
    port=follower_port,
    id="follower_arm",
    cameras=camera_config,
)

teleop_config = KochLeaderConfig(
    port=leader_port,
    id="leader_arm",
)


def get_follower_arm():    
    return KochFollower(robot_config)

def get_leader_arm():
    return KochLeaderConfig(teleop_config)