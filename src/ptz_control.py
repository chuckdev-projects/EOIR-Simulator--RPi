import time
from adafruit_servokit import ServoKit

class PTZController:
    def __init__(self, address=0x40, pan_ch=0, tilt_ch=1, pan_min=10, pan_max=170, tilt_min=15, tilt_max=165):
        self.kit = ServoKit(channels=16, address=address)
        self.pan_ch, self.tilt_ch = pan_ch, tilt_ch
        self.pan_min, self.pan_max = pan_min, pan_max
        self.tilt_min, self.tilt_max = tilt_min, tilt_max
        self.kit.servo[pan_ch].set_pulse_width_range(500, 2500)
        self.kit.servo[tilt_ch].set_pulse_width_range(500, 2500)

    def move(self, pan_angle, tilt_angle):
        self.kit.servo[self.pan_ch].angle = pan_angle
        self.kit.servo[self.tilt_ch].angle = tilt_angle

    def release(self):
        self.kit.servo[self.pan_ch].angle = None
        self.kit.servo[self.tilt_ch].angle = None
