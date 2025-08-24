import odrive

from odrive.enums import (
    AXIS_STATE_IDLE,
    AXIS_STATE_FULL_CALIBRATION_SEQUENCE,
    AXIS_STATE_CLOSED_LOOP_CONTROL,
    INPUT_MODE_TRAP_TRAJ,
    INPUT_MODE_POS_FILTER,
    CONTROL_MODE_VELOCITY_CONTROL
)

from odrive.utils import *
import time
import keyboard
from pynput import keyboard as kb


def configure_motor_and_encoder(axis):
    axis.motor.config.current_lim = 100
    axis.motor.config.pole_pairs = 7
    axis.motor.config.torque_constant = 8.27 / 270
    axis.motor.config.motor_type = 0
    axis.encoder.config.cpr = 8192
    axis.encoder.config.calib_scan_distance = 100


def calibrate_axis(axis):
    axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    while axis.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)


def setup_odrive2():
    odrv = odrive.find_any()
    odrv.clear_errors()

    for axis in [odrv.axis0, odrv.axis1]:
        configure_motor_and_encoder(axis)

    for axis in [odrv.axis0, odrv.axis1]:
        calibrate_axis(axis)

    print("Konfigurasjon og kalibrering fullført. Lagrer konfigurasjon...")

    odrv.save_configuration()
    print("Konfigurasjon lagret.")

    dump_errors(odrv)
    return odrv


def setup_odrive():
    odrv = odrive.find_any()
    odrv.clear_errors()

    for axis in [odrv.axis0, odrv.axis1]:
        configure_motor_and_encoder(axis)

    print("Konfigurasjon fullført. Lagrer konfigurasjon...")
    # odrv.save_configuration()

    print("Venter på at ODrive skal restarte...")
    time.sleep(3)
    odrv = odrive.find_any()

    for axis in [odrv.axis0, odrv.axis1]:
        calibrate_axis(axis)

    print("Kalibrering fullført.")
    dump_errors(odrv)
    return odrv


def control_loop(odrv):
    odrv.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv.axis0.controller.config.input_mode = INPUT_MODE_POS_FILTER
    odrv.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

    odrv.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv.axis1.controller.config.input_mode = INPUT_MODE_POS_FILTER
    odrv.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

    print("Bruk WASD-tastene for å styre. Trykk ESC for å avslutte.")

    velocity = 1  # eller den farten du ønsker
    pressed_keys = set()
    running = True

    def update_velocity():
        if 'w' in pressed_keys and 'a' in pressed_keys:
            odrv.axis0.controller.input_vel = velocity
            odrv.axis1.controller.input_vel = -velocity
        elif 'w' in pressed_keys and 'd' in pressed_keys:
            odrv.axis0.controller.input_vel = velocity
            odrv.axis1.controller.input_vel = -2 * velocity
        elif 's' in pressed_keys and 'a' in pressed_keys:
            odrv.axis0.controller.input_vel = -velocity
            odrv.axis1.controller.input_vel = velocity
        elif 's' in pressed_keys and 'd' in pressed_keys:
            odrv.axis0.controller.input_vel = -velocity
            odrv.axis1.controller.input_vel = 2 * velocity
        elif 'w' in pressed_keys:
            odrv.axis0.controller.input_vel = velocity
            odrv.axis1.controller.input_vel = -velocity
        elif 's' in pressed_keys:
            odrv.axis0.controller.input_vel = -velocity
            odrv.axis1.controller.input_vel = velocity
        elif 'a' in pressed_keys:
            odrv.axis0.controller.input_vel = velocity
            odrv.axis1.controller.input_vel = -velocity
        elif 'd' in pressed_keys:
            odrv.axis0.controller.input_vel = velocity
            odrv.axis1.controller.input_vel = -2 * velocity
        else:
            # Ingen relevante taster trykket: Stopp
            odrv.axis0.controller.input_vel = 0
            odrv.axis1.controller.input_vel = 0

    def on_press(key):
        nonlocal running
        try:
            pressed_keys.add(key.char)
            update_velocity()
        except AttributeError:
            if key == kb.Key.esc:
                print("Avslutter kontroll...")
                running = False

    def on_release(key):
        nonlocal running
        try:
            pressed_keys.discard(key.char)
            update_velocity()
        except AttributeError:
            if key == kb.Key.esc:
                print("Avslutter kontroll...")
                running = False

    listener = kb.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while running:
        time.sleep(0.05)

    listener.stop()


if __name__ == "__main__":
    odrv0 = setup_odrive()
    control_loop(odrv0)

