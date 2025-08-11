from lerobot.teleoperators.koch_leader import KochLeaderConfig, KochLeader
from lerobot.robots.koch_follower import KochFollowerConfig, KochFollower
from cogitron.arms import get_leader_port, get_follower_port
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig

leader_port, follower_port = get_leader_port(), get_follower_port()

camera_config = {
    "front": OpenCVCameraConfig(index_or_path=0, width=1280, height=720, fps=60)
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



robot = KochFollower(robot_config)
teleop_device = KochLeaderConfig(teleop_config)
robot.connect()
teleop_device.connect()

while True:
    observation = robot.get_observation()
    action = teleop_device.get_action()
    robot.send_action(action)