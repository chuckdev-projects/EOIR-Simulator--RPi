#!/usr/bin/env python3
import time
import cv2
import numpy as np
from adafruit_servokit import ServoKit
from picamera2 import Picamera2

# ====== PTZ CONFIG ======
I2C_ADDRESS  = 0x40          # Detected by i2cdetect -y 1
PAN_CH, TILT_CH = 0, 1       # Channels used by the onboard PTZ controller
PAN_CENTER, TILT_CENTER = 90, 90
PAN_MIN, PAN_MAX   = 10, 170
TILT_MIN, TILT_MAX = 15, 165
DEFAULT_STEP = 2

# Adjust if your servos need different pulse ranges
PULSE_MIN_US = 500
PULSE_MAX_US = 2500

# ====== VIDEO & OVERLAYS ======
PREVIEW_SIZE = (1280, 720)   # (width, height). Drop to (960, 540) if you need more FPS.
HUD_COLOR = (255, 255, 255)  # white

# Crosshair
CROSSHAIR_LEN = 30
CROSSHAIR_THK = 2

# Grid
GRID_SPACING = 80            # pixels between grid lines
GRID_COLOR   = (0, 255, 0)   # green
GRID_THK     = 1

# Range circles
RANGE_CIRCLES = 3
RANGE_COLOR   = (0, 255, 255)  # yellow
RANGE_THK     = 1

# Zoom PiP
ZOOM_ENABLED_DEFAULT = True
ZOOM_FACTOR_DEFAULT  = 2.0     # 1.0 ~ off; >1 magnifies center ROI
ZOOM_FACTOR_MIN, ZOOM_FACTOR_MAX = 1.2, 5.0
PIP_BOX_SIZE = 220
PIP_MARGIN   = 12
PIP_BORDER_COLOR = (255, 255, 255)
PIP_BORDER_THK   = 2

# Keys (OpenCV arrow key codes)
ARROW_LEFT, ARROW_UP, ARROW_RIGHT, ARROW_DOWN = 81, 82, 83, 84

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

# ---------- Overlay helpers ----------
def draw_crosshair(img):
    h, w = img.shape[:2]
    cx, cy = w // 2, h // 2
    # Horizontal
    cv2.line(img, (cx - CROSSHAIR_LEN, cy), (cx + CROSSHAIR_LEN, cy), HUD_COLOR, CROSSHAIR_THK, cv2.LINE_AA)
    # Vertical
    cv2.line(img, (cx, cy - CROSSHAIR_LEN), (cx, cy + CROSSHAIR_LEN), HUD_COLOR, CROSSHAIR_THK, cv2.LINE_AA)
    # Center box
    cv2.rectangle(img, (cx - 4, cy - 4), (cx + 4, cy + 4), HUD_COLOR, 1)

def draw_grid(img, spacing=GRID_SPACING, color=GRID_COLOR, thickness=GRID_THK):
    h, w = img.shape[:2]
    # Vertical lines
    for x in range(0, w, spacing):
        cv2.line(img, (x, 0), (x, h), color, thickness)
    # Horizontal lines
    for y in range(0, h, spacing):
        cv2.line(img, (0, y), (w, y), color, thickness)

def draw_range_circles(img, num_circles=RANGE_CIRCLES, color=RANGE_COLOR, thickness=RANGE_THK):
    h, w = img.shape[:2]
    cx, cy = w // 2, h // 2
    max_radius = min(cx, cy) - 20  # margin from edges
    if num_circles < 1 or max_radius <= 0:
        return
    step = max(10, max_radius // num_circles)
    for i in range(1, num_circles + 1):
        cv2.circle(img, (cx, cy), i * step, color, thickness)

def draw_zoom_pip(img, zoom_factor):
    if zoom_factor < 1.2:
        return img  # effectively off

    h, w = img.shape[:2]
    cx, cy = w // 2, h // 2

    # Compute source ROI size so that resizing -> PIP_BOX_SIZE
    roi_size = int(PIP_BOX_SIZE / zoom_factor)
    roi_size = max(20, min(roi_size, min(w, h) - 2))
    half = roi_size // 2

    x1 = clamp(cx - half, 0, w - roi_size)
    y1 = clamp(cy - half, 0, h - roi_size)
    x2, y2 = x1 + roi_size, y1 + roi_size

    roi = img[y1:y2, x1:x2]
    if roi.size == 0:
        return img

    pip = cv2.resize(roi, (PIP_BOX_SIZE, PIP_BOX_SIZE), interpolation=cv2.INTER_CUBIC)

    # Top-right position with margin
    xR = w - PIP_MARGIN - PIP_BOX_SIZE
    yT = PIP_MARGIN

    # Label background & text
    cv2.rectangle(img, (xR - 2, yT - 22), (xR + PIP_BOX_SIZE + 2, yT - 2), PIP_BORDER_COLOR, cv2.FILLED)
    label = f"ZOOM {zoom_factor:.1f}x"
    cv2.putText(img, label, (xR + 8, yT - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)

    # Insert PiP & border
    img[yT:yT + PIP_BOX_SIZE, xR:xR + PIP_BOX_SIZE] = pip
    cv2.rectangle(img, (xR, yT), (xR + PIP_BOX_SIZE, yT + PIP_BOX_SIZE), PIP_BORDER_COLOR, PIP_BORDER_THK)
    return img

def init_ptz():
    kit = ServoKit(channels=16, address=I2C_ADDRESS)
    kit.servo[PAN_CH].set_pulse_width_range(PULSE_MIN_US, PULSE_MAX_US)
    kit.servo[TILT_CH].set_pulse_width_range(PULSE_MIN_US, PULSE_MAX_US)
    return kit

def main():
    # --- Init PTZ ---
    kit = init_ptz()
    pan, tilt, step = PAN_CENTER, TILT_CENTER, DEFAULT_STEP
    kit.servo[PAN_CH].angle = pan
    kit.servo[TILT_CH].angle = tilt
    time.sleep(0.2)

    # --- Init camera ---
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": PREVIEW_SIZE})
    picam2.configure(config)
    picam2.start()

    win = "EO/IR PTZ Viewer"
    cv2.namedWindow(win, cv2.WINDOW_AUTOSIZE)

    zoom_enabled = ZOOM_ENABLED_DEFAULT
    zoom_factor = ZOOM_FACTOR_DEFAULT

    try:
        while True:
            frame = picam2.capture_array()

            # Overlays
            draw_grid(frame)
            draw_range_circles(frame)
            draw_crosshair(frame)
            if zoom_enabled:
                frame = draw_zoom_pip(frame, zoom_factor)

            hud = f"pan={pan:3d}  tilt={tilt:3d}  step={step}  [Arrows/WASD | SPACE=center | [ ]=step | z=zoom | +/-=zoom | q=quit]"
            cv2.putText(frame, hud, (12, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, HUD_COLOR, 2, cv2.LINE_AA)

            cv2.imshow(win, frame)
            k = cv2.waitKey(1) & 0xFF

            if k == ord('q'):
                break
            elif k in (ARROW_LEFT, ord('a')):
                pan = clamp(pan - step, PAN_MIN, PAN_MAX); kit.servo[PAN_CH].angle = pan
            elif k in (ARROW_RIGHT, ord('d')):
                pan = clamp(pan + step, PAN_MIN, PAN_MAX); kit.servo[PAN_CH].angle = pan
            elif k in (ARROW_UP, ord('w')):
                tilt = clamp(tilt - step, TILT_MIN, TILT_MAX); kit.servo[TILT_CH].angle = tilt
            elif k in (ARROW_DOWN, ord('s')):
                tilt = clamp(tilt + step, TILT_MIN, TILT_MAX); kit.servo[TILT_CH].angle = tilt
            elif k == ord(' '):
                pan, tilt = PAN_CENTER, TILT_CENTER
                kit.servo[PAN_CH].angle = pan; kit.servo[TILT_CH].angle = tilt
            elif k == ord('['):
                step = clamp(step - 1, 1, 45)
            elif k == ord(']'):
                step = clamp(step + 1, 1, 45)
            elif k in (ord('z'), ord('Z')):
                zoom_enabled = not zoom_enabled
            elif k in (ord('+'), ord('=')):   # '=' shares key with '+'
                zoom_factor = clamp(zoom_factor + 0.1, ZOOM_FACTOR_MIN, ZOOM_FACTOR_MAX)
            elif k in (ord('-'), ord('_')):
                zoom_factor = clamp(zoom_factor - 0.1, ZOOM_FACTOR_MIN, ZOOM_FACTOR_MAX)

    finally:
        cv2.destroyAllWindows()
        picam2.stop()
        # Optionally relax servos when exiting:
        # kit.servo[PAN_CH].angle = None
        # kit.servo[TILT_CH].angle = None

if __name__ == "__main__":
    main()

