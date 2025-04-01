import arms
from lerobot.common.robot_devices.motors.dynamixel import DynamixelMotorsBus
from arms import leader_arm, follower_arm

# region v1
# value_names = [
#     "Model_Number",
#     "Model_Information",
#     "Firmware_Version",
#     "ID",
#     "Baud_Rate",
#     "Return_Delay_Time",
#     "Drive_Mode",
#     "Operating_Mode",
#     "Secondary_ID",
#     "Protocol_Type",
#     "Homing_Offset",
#     "Moving_Threshold",
#     "Temperature_Limit",
#     "Max_Voltage_Limit",
#     "Min_Voltage_Limit",
#     "PWM_Limit",
#     "Current_Limit",
#     "Acceleration_Limit",
#     "Velocity_Limit",
#     "Max_Position_Limit",
#     "Min_Position_Limit",
#     "Shutdown",
#     "Torque_Enable",
#     "LED",
#     "Status_Return_Level",
#     "Registered_Instruction",
#     "Hardware_Error_Status",
#     "Velocity_I_Gain",
#     "Velocity_P_Gain",
#     "Position_D_Gain",
#     "Position_I_Gain",
#     "Position_P_Gain",
#     "Feedforward_2nd_Gain",
#     "Feedforward_1st_Gain",
#     "Bus_Watchdog",
#     "Goal_PWM",
#     "Goal_Current",
#     "Goal_Velocity",
#     "Profile_Acceleration",
#     "Profile_Velocity",
#     "Goal_Position",
#     "Realtime_Tick",
#     "Moving",
#     "Moving_Status",
#     "Present_PWM",
#     "Present_Current",
#     "Present_Velocity",
#     "Present_Position",
#     "Velocity_Trajectory",
#     "Position_Trajectory",
#     "Present_Input_Voltage",
#     "Present_Temperature",
# ]

# leader_values = {}
# follower_values = {}

# def read_values_leder():
#     for key in value_names:
#         leader_values[key] =leader_arm.read(key)

# def read_values_follower():
#     for key in value_names:
#         follower_values[key] = follower_arm.read(key)

# def save_values_leader():
#     with open("values_leader.txt", "w") as f:
#         f.write("Leader: \n")
#         for key, value in leader_values.items():
#             f.write(f"{key}: {value} \n")
#         f.close()

# def save_values_follower():
#     with open("values_follower.txt", "a") as f:
#         f.write("Follower: \n")
#         for key, value in follower_values.items():
#             f.write(f"{key}: {value} \n")
#         f.close()

# def save_values():
#     save_values_leader()
#     save_values_follower()

# def print_values():
#     print("Leader: \n")
#     for key, value in leader_values.items():
#         print(f"{key}: {value} \n")
#     print("Follower: \n")
#     for key, value in follower_values.items():
#         print(f"{key}: {value} \n")
#
# def load_old_values():
#     with open("values_leader.txt", "r") as f:
#         for line in f:
#             key, value = line.split(": ")
#             value = int(value)
#             leader_values[key] = value
#         f.close()
#     with open("values_follower.txt", "r") as f:
#         for line in f:
#             key, value = line.split(": ")
#             value = int(value)
#             follower_values[key] = value
#         f.close()
# endregion

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