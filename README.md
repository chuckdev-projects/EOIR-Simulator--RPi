# EO/IR Simulator – Raspberry Pi (MX-15 HDI Familiarization)

# Overview
This project simulates an **EO/IR gimbal camera system** (similar to MX-15) using:
- **Raspberry Pi 4** + Camera Module 2 (IMX219)
- **ArduCam PTZ pan/tilt platform**
- **Servo control over I²C**
- **Python (Picamera2 + OpenCV + Adafruit ServoKit)**

Features:
- Live video feed with overlays
- Keyboard-controlled pan/tilt (arrow keys or WASD)
- On-screen HUD:
  - Crosshair
  - Grid overlay
  - Range circles
  - Picture-in-picture (PiP) zoom box
- Modular code (`src/` folder) for clean separation of **camera driver, PTZ control, UI overlays, and main app**.

# Project Structure
EOIR-Simulator--RPi/
│
├── src/
│ ├── camera_driver.py # Handles PiCamera2 video feed
│ ├── ptz_control.py # Controls servos via I²C
│ ├── menu_ui.py # Overlays: HUD, crosshair, grid, range circles, zoom PiP
│ └── eo_ir_ptz_viewer.py # Main entry point (demo app)
│
├── docs/ # (optional) Screenshots, diagrams
└── README.md


---

#  Hardware Requirements
- Raspberry Pi 4 (or 3B+)
- Raspberry Pi Camera Module 2 (IMX219) or NoIR version
- ArduCam PTZ pan/tilt kit (with onboard I²C controller at address `0x40`)
- MicroSD card (32GB+) with Raspberry Pi OS (Bookworm)
- HDMI display, USB keyboard, mouse (for setup)

---

# Software Requirements
Install dependencies:
```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-opencv python3-pip rpicam-apps
pip3 install --break-system-packages adafruit-blinka adafruit-circuitpython-servokit

# Enable I2C
sudo raspi-config
# Interface Options → I2C → Enable → Finish

# Verify PTZ Board on I2C bus:
sudo i2cdetect -y 1
# Should show "40"

# Running the simulator
python3 eo_ir_ptz_viewer.py

# Controls
Controls
Arrows / W, A, S, D → Pan/Tilt
Space → Center gimbal
[ / ] → Step size down/up
Z → Toggle zoom PiP
/ - → Adjust zoom level
Q → Quit


# Future Improvements
Add menu navigation system (MX-15 style overlays).
Simulated IR mode (grayscale/contrast LUT).
Recording modes (still capture / video with PTZ metadata).
Remote client/server control (Pi Zero 2W as “payload”, Pi 4 as “operator”).

# Credits
ArduCam PTZ Kit
Raspberry Pi Foundation
Adafruit ServoKit
OpenCV & Picamera2 for image processing.
