# Basic PTZ (Pan-Tilt-Zoom) control demo
# Simulates PTZ commands with keyboard input

import time

def move_camera(direction):
    print(f"[PTZ] Moving {direction}")
    time.sleep(0.5)

if __name__ == "__main__":
    print("PTZ Control Demo (q to quit)")
    while True:
        cmd = input("Direction (up/down/left/right/zoom): ").strip().lower()
        if cmd == "q":
            break
        elif cmd in ["up", "down", "left", "right", "zoom"]:
            move_camera(cmd)
        else:
            print("Invalid command")
