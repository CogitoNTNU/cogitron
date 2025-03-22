import arms
from arms import leader_arm, follower_arm

value_names = [
    "Model_Number",
    "Model_Information",
    "Firmware_Version",
    "ID",
    "Baud_Rate",
    "Return_Delay_Time",
    "Drive_Mode",
    "Operating_Mode",
    "Secondary_ID",
    "Protocol_Type",
    "Homing_Offset",
    "Moving_Threshold",
    "Temperature_Limit",
    "Max_Voltage_Limit",
    "Min_Voltage_Limit",
    "PWM_Limit",
    "Current_Limit",
    "Acceleration_Limit",
    "Velocity_Limit",
    "Max_Position_Limit",
    "Min_Position_Limit",
    "Shutdown",
    "Torque_Enable",
    "LED",
    "Status_Return_Level",
    "Registered_Instruction",
    "Hardware_Error_Status",
    "Velocity_I_Gain",
    "Velocity_P_Gain",
    "Position_D_Gain",
    "Position_I_Gain",
    "Position_P_Gain",
    "Feedforward_2nd_Gain",
    "Feedforward_1st_Gain",
    "Bus_Watchdog",
    "Goal_PWM",
    "Goal_Current",
    "Goal_Velocity",
    "Profile_Acceleration",
    "Profile_Velocity",
    "Goal_Position",
    "Realtime_Tick",
    "Moving",
    "Moving_Status",
    "Present_PWM",
    "Present_Current",
    "Present_Velocity",
    "Present_Position",
    "Velocity_Trajectory",
    "Position_Trajectory",
    "Present_Input_Voltage",
    "Present_Temperature",
]

leader_values = {}
follower_values = {}

def read_values_leder():
    for key in value_names:
        leader_values[key] =leader_arm.read(key)

def read_values_follower():
    for key in value_names:
        follower_values[key] = follower_arm.read(key)

def save_values_leader():
    with open("values_leader.txt", "w") as f:
        f.write("Leader: \n")
        for key, value in leader_values.items():
            f.write(f"{key}: {value} \n")
        f.close()

def save_values_follower():
    with open("values_follower.txt", "a") as f:
        f.write("Follower: \n")
        for key, value in follower_values.items():
            f.write(f"{key}: {value} \n")
        f.close()

def save_values():
    save_values_leader()
    save_values_follower()

def print_values():
    print("Leader: \n")
    for key, value in leader_values.items():
        print(f"{key}: {value} \n")
    print("Follower: \n")
    for key, value in follower_values.items():
        print(f"{key}: {value} \n")

def load_old_values():
    with open("values_leader.txt", "r") as f:
        for line in f:
            key, value = line.split(": ")
            value = int(value)
            leader_values[key] = value
        f.close()
    with open("values_follower.txt", "r") as f:
        for line in f:
            key, value = line.split(": ")
            value = int(value)
            follower_values[key] = value
        f.close()