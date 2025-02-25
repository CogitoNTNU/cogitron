import odrive
from odrive.enums import *
print("Finding ODrive...")
odrv0 = odrive.find_any()

print("Setting parameters...")
odrv0.axis0.motor.config.current_lim = 10  # Set current limit
odrv0.axis0.motor.config.pole_pairs = 7  # Adjust for your motor
odrv0.axis0.encoder.config.cpr = 8192  # Encoder counts per revolution
odrv0.axis1.motor.config.current_lim = 10  # Set current limit
odrv0.axis1.motor.config.pole_pairs = 7  # Adjust for your motor
odrv0.axis1.encoder.config.cpr = 8192  # Encoder counts per revolution


print("Saving configuration...")
odrv0.save_configuration()

print("Rebooting ODrive...")
odrv0.reboot()

print("Reconnecting to ODrive after reboot...")
odrv0 = odrive.find_any()
left_motor = odrv0.axis0
right_motor = odrv0.axis1

print("Starting calibration...")
left_motor.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

print("Waiting for calibration to complete...")
while left_motor.current_state != AXIS_STATE_IDLE:
    pass

print("Calibration complete! Setting to closed-loop control mode...")
left_motor.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

print("Done!")
