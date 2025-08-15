from cogitron.arms import get_follower_arm, get_leader_arm

robot = get_follower_arm()
teleop_device = get_leader_arm()

robot.connect()
teleop_device.connect()

while True:
    observation = robot.get_observation()
    action = teleop_device.get_action()
    robot.send_action(action)