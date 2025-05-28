import cv2
import threading

class LatestFrameCapture:
    def __init__(self, src=0, width=None, height=None):
        self.cap = cv2.VideoCapture(src)
        print("Frame rate: ", self.cap.get(cv2.CAP_PROP_FPS))
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera.")

        if width:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        if height:
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'));

        self.ret = False
        self.frame = None
        self.lock = threading.Lock()
        self.running = True

        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

    def _update(self):
        while self.running:
            ret, frame = self.cap.read()
            with self.lock:
                self.ret = ret
                self.frame = frame

    def read(self):
        with self.lock:
            return self.ret, self.frame.copy() if self.frame is not None else None
            # return self.ret, self.frame        

    def is_opened(self):
        return self.cap.isOpened()

    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()
