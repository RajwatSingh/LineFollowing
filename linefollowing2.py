from picarx import Picarx   # PicarX library to interface with the PiCar chassis
from time import sleep       # sleep for adding delays
import random                # random for picking intersection exits

# --- Initialization and Calibration ---
px = Picarx()                              # Create controller instance
px.set_line_reference([1400, 1400, 1400])  # Set the grayscale thresholds for left, center, right sensors

# --- Global State & Parameters ---
current_state = None       # Holds the most recent detected driving state
correction = 10            # Angle (°) to gently correct when off line
px_power = 2               # Motor power for forward movement
px_back = 3                # Motor power for backward movement
offset = 45                # Larger angle (°) for sharper recovery turns
last_state = "stop"        # Last valid non-stop state, used for recovery
intersection_counter = 0   # Frames counted where all sensors see the line
intersection_threshold = 2 # Frames required to confirm an intersection

def outHandle():
    """Recovery handler: if we lose the line, steer back toward where we last were."""
    global last_state, current_state
    if last_state == 'left':
        # If last we were veering left, gently steer left while moving forward
        px.set_dir_servo_angle(-correction)
        px.forward(px_power)
    elif last_state == 'right':
        # If last we were veering right, gently steer right while moving forward
        px.set_dir_servo_angle(correction)
        px.forward(px_power)
    # Short pause to let sensors update
    sleep(0.01)

def get_status(val_list):
    """Return the robot’s next move state based on sensor readings."""
    global intersection_counter
    _state = px.get_line_status(val_list)  # e.g. [1, 0, 1]

    # 1) Intersection: all three sensors detect the line
    if _state == [1, 1, 1]:
        intersection_counter += 1
        return 'intersect'

    # 2) Standard line-following:
    if _state == [0, 1, 0]:
        return 'forward'        # perfectly centered
    elif _state == [1, 1, 0]:
        return 'turn_left'      # left sensor & center see line; need sharper left
    elif _state == [0, 1, 1]:
        return 'turn_right'     # center & right see line; need sharper right
    elif _state[2] == 1:
        return 'right'          # only right sensor sees line; gentle right
    elif _state[0] == 1:
        return 'left'           # only left sensor sees line; gentle left

    # 3) No line detected
    return 'stop'

def adjust_turn_direction(gm_state):
    """Perform steering maneuvers based on the given state."""
    if gm_state == 'left':
        # Gentle left for adjusting to small deviations
        px.set_dir_servo_angle(-correction)
        px.forward(px_power)
    elif gm_state == 'right':
        # Gentle right for adjusting to small deviations
        px.set_dir_servo_angle(correction)
        px.forward(px_power)
    elif gm_state == 'turn_left':
        # Left turn 
        print("Turning left")
        px.set_dir_servo_angle(offset)
        px.backward(px_back)
        sleep(0.4)
        px.set_dir_servo_angle(-offset)
        px.forward(px_power)
        sleep(0.5)
    elif gm_state == 'turn_right':
        # Right turn 
        print("Turn right")
        px.set_dir_servo_angle(-offset)
        px.backward(px_back)
        sleep(0.2)
        px.set_dir_servo_angle(int(0.7 * offset))
        px.forward(px_power)
        sleep(1.2)

    # Small pause to stabilize sensor readings
    sleep(0.01)

def intersection():
    """Choose a direction at an intersection randomly."""
    exit_spoke = random.randint(1, 3)
    print("RANDO:", exit_spoke)
    return 'straight'

# --- Main Loop ---
if __name__ == '__main__':
    try:
        while True:
            # 1) Read sensors and decide state
            gm_val_list = px.get_grayscale_data()
            gm_state = get_status(gm_val_list)
            print(f"gm_val_list: {gm_val_list}, state: {gm_state}")

            # 2) If recovering from a sharp turn, keep going straight until we see a new signal
            if last_state == 'turn_left' and gm_state != 'right':
                px.forward(px_power)
                continue
            elif last_state == 'turn_right' and gm_state != 'left':
                px.forward(px_power)
                continue

            # 3) Update last_state when not stopped
            if gm_state != "stop":
                last_state = gm_state

            # 4) Handle intersection behavior
            if gm_state == 'intersect':
                sleep(0.1)
                px.set_dir_servo_angle(0)     # face forward
                px.backward(px_back)          # back up slightly to show we are at an intersection
                sleep(0.6)
                direction = intersection()     # pick exit
                print("interDir:", direction)
                if direction == 'forward':
                    px.set_dir_servo_angle(0)
                    px.forward(px_power)
                    sleep(2.5) # go forward for a bit
                else:
                    adjust_turn_direction(direction)
                last_state = direction
                continue

            # 5) Execute normal movements
            if gm_state == 'forward':
                px.set_dir_servo_angle(0)
                px.forward(px_power)
            elif gm_state in ('turn_left', 'turn_right', 'left', 'right'):
                adjust_turn_direction(gm_state)
            else:
                # Lost line: try recovery handler
                outHandle()

    finally:
        # On exit (e.g., Ctrl+C), stop all motors cleanly
        px.stop()
        print("stop and exit")
        sleep(0.1)


        #DANISTHEGOAT
