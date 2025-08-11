from lerobot.teleoperators.koch_leader import KochLeaderConfig, KochLeader
from lerobot.robots.koch_follower import KochFollowerConfig, KochFollower
from cogitron.arms import get_leader_port, get_follower_port

leader_port, follower_port = get_leader_port(), get_follower_port()


robot_config = KochFollowerConfig(
    port=follower_port,
    id="follower_arm",
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
    action = teleop_device.get_action()
    robot.send_action(action)