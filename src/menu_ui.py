import cv2

class OverlayUI:
    def __init__(self):
        self.zoom_enabled = True
        self.zoom_factor = 2.0
        self.zoom_min, self.zoom_max = 1.2, 5.0

    def toggle_zoom(self):
        self.zoom_enabled = not self.zoom_enabled

    def adjust_zoom(self, delta):
        self.zoom_factor = max(self.zoom_min, min(self.zoom_max, self.zoom_factor + delta))

    def apply(self, frame, pan, tilt, step):
        # Grid
        self.draw_grid(frame)
        # Range Circles
        self.draw_range_circles(frame)
        # Crosshair
        self.draw_crosshair(frame)
        # Zoom PiP
        if self.zoom_enabled:
            frame = self.draw_zoom_pip(frame)
        # HUD text
        hud = f"pan={pan:3d} tilt={tilt:3d} step={step} [WASD/Arrows | SPACE=center | z=zoom | +/- zoom | q=quit]"
        cv2.putText(frame, hud, (12, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)
        return frame

    def draw_crosshair(self, img):
        h, w = img.shape[:2]; cx, cy = w//2, h//2
        cv2.line(img, (cx-30, cy), (cx+30, cy), (255,255,255), 2)
        cv2.line(img, (cx, cy-30), (cx, cy+30), (255,255,255), 2)
        cv2.rectangle(img, (cx-4, cy-4), (cx+4, cy+4), (255,255,255), 1)

    def draw_grid(self, img, spacing=80):
        h, w = img.shape[:2]
        for x in range(0, w, spacing):
            cv2.line(img, (x,0), (x,h), (0,255,0), 1)
        for y in range(0, h, spacing):
            cv2.line(img, (0,y), (w,y), (0,255,0), 1)

    def draw_range_circles(self, img, num_circles=3):
        h, w = img.shape[:2]; cx, cy = w//2, h//2
        max_radius = min(cx,cy)-20
        step = max_radius//num_circles
        for i in range(1,num_circles+1):
            cv2.circle(img,(cx,cy),i*step,(0,255,255),1)

    def draw_zoom_pip(self, img):
        h, w = img.shape[:2]; cx, cy = w//2, h//2
        roi_size = int(220/self.zoom_factor)
        x1, y1 = cx-roi_size//2, cy-roi_size//2
        roi = img[max(0,y1):y1+roi_size, max(0,x1):x1+roi_size]
        if roi.size==0: return img
        pip = cv2.resize(roi,(220,220))
        xR, yT = w-220-12, 12
        img[yT:yT+220, xR:xR+220] = pip
        cv2.rectangle(img,(xR,yT),(xR+220,yT+220),(255,255,255),2)
        return img
