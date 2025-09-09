from picamera2 import Picamera2

class CameraDriver:
    def __init__(self, width=1280, height=720):
        self.picam2 = Picamera2()
        self.config = self.picam2.create_preview_configuration(main={"size": (width, height)})
        self.picam2.configure(self.config)

    def start(self):
        self.picam2.start()

    def get_frame(self):
        return self.picam2.capture_array()

    def stop(self):
        self.picam2.stop()
