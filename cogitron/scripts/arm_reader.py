import arms
from lerobot.common.robot_devices.motors.dynamixel import DynamixelMotorsBus
from arms import leader_arm, follower_arm

class ArmReader:
    def __init__(self, name: str, arm: DynamixelMotorsBus):
        self.name = name
        self.arm = arm

        keys = self.arm.motors.keys()
        self.value_names = keys

        self.arm_values: dict[str, tuple[int, ...]] = {}

    def read_values(self):
        for key in self.value_names:
            self.arm_values[key] = self.arm.read(key)

    def get_values(self):
        return self.arm_values
    
    def load_values(self):
        filename = "values_" + self.name + ".txt"
        with open(filename, "r") as f:
            for line in f:
                if ": " not in line:
                    continue
                key, values_str = line.split(": ")
                key = key.strip()
                values = values_str.strip().split(",")  # Split by space and remove the newline
                # self.arm_values[key] = tuple(int(value) for value in values if value)  # Convert values to int
                self.arm_values[key] = tuple(int(values[0], values[1]))  # if values is tuple of int and str, see arms.py
    
    def save_values(self):
        filename = "values_" + self.name + ".txt"
        with open(filename, "w") as f:
            f.write(f"{self.name}: \n")
            for key, values in self.arm_values.items():
                f.write(f"{key}: {','.join(map(str, values))}\n")
    
    def print_values(self):
        print(f"{self.name} \n")
        for key, item in self.arm_values.item():
            print(f"{key}: {item} \n")

leader_reader = ArmReader("Leader", leader_arm)
follower_reader = ArmReader("Leader", follower_arm)

leader_reader.read_values()
leader_reader.print_values()
# leader_reader.save_values()