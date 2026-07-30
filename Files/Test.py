import robotiq_gripper
import time
import math
import rtde_control
from rtde_receive import RTDEReceiveInterface
import threading

ip = "172.31.52.50"

def log_info(gripper):
    print(f"Pos: {str(gripper.get_current_position()): >3}  "
          f"Open: {gripper.is_open(): <2}  "
          f"Closed: {gripper.is_closed(): <2}  ")


print("Creating gripper...")
gripper = robotiq_gripper.RobotiqGripper()
print("Connecting to gripper...")
gripper.connect(ip, 63352)
print("Activating gripper...")
gripper.activate()


print("Testing gripper...")
gripper.move_and_wait_for_pos(255, 255, 100)
log_info(gripper)
force = gripper._get_var('FOR')
print(force)
gripper.move_and_wait_for_pos(0, 255, 100)
log_info(gripper)

def monitor_force():
    round = 0
    try:
        while round <= 100:
            force = gripper._get_var("FOR")
            print(f"Current force: {force}")
            time.sleep(0.01)
            round += 1
    except KeyboardInterrupt:
        print("Stop")

try:
    monitor = threading.Thread(target=monitor_force)
    monitor.start()
    moveing = True
    gripper.move(255,100, 1)
    monitor.join()
    moveing = False
    time.sleep(3)
    gripper.move(0,100,1)
    time.sleep(3)


except KeyboardInterrupt:
    print("Programm ended")
finally:
    gripper.disconnect()
    print("gripper disconnected")
