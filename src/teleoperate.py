from cogitron.arms import get_follower_arm, get_leader_arm, reboot
import time

robot = get_follower_arm()
teleop_device = get_leader_arm()

reboot(robot.bus.port_handler)
reboot(teleop_device.bus.port_handler)

time.sleep(1)

robot.connect()
teleop_device.connect()

while True:
    observation = robot.get_observation()
    action = teleop_device.get_action()
    robot.send_action(action)