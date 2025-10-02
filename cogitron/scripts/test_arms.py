import sys
import time
from lerobot.robots.koch_follower import KochFollowerConfig, KochFollower
from lerobot.teleoperators.koch_leader import KochLeaderConfig, KochLeader

try:
    port = sys.argv[1] # First terminal argument,
except IndexError:
    print("""No port specified. Input the port as the The port as the \n
          first input argument. It is often either port /dev/ttyACM0 or /dev/ttyACM1.
          You can find the ports using the command 'lerobot-find-port' if lerobot is 
          installed through pip""")

def test_follower():
    robot_config = KochFollowerConfig(
        port=port,
        id="follower_arm",
    )

    robot = KochFollower(robot_config)
    robot.connect()

def test_leader():
    teleoperator_config = KochLeaderConfig(
        port=port,
        id="leader_arm"
    )

    teleoperator = KochLeader(teleoperator_config)
    teleoperator.connect()


if __name__ == '__main__':
    test_follower()
    test_leader()
