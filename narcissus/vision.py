import time

from .util import get_resource_path

try:
    import cv2

    opencv_available = True
except ImportError:
    opencv_available = False
    print("Please install OpenCV to use facial recognition.")

_model = get_resource_path(__file__, "models/opencv/haarcascade_frontalface_alt.xml")


class Vision:
    def __init__(
        self,
        cascade_model: str = _model,
        camera: int = 0,
    ):
        self.face_cascade = cv2.CascadeClassifier(cascade_model)
        self.camera: int = camera

    def recognize(self) -> None:
        if not opencv_available:
            return

        cam = cv2.VideoCapture(self.camera)
        while True:
            # Capture frame-by-frame
            _, frame = cam.read()

            gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(
                gray_image,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE,
            )

            if len(faces) > 0:
                # When everything is done, release the capture
                cam.release()
                cv2.destroyAllWindows()
                return

            time.sleep(0.1)
