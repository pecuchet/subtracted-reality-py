import cv2
import videoStream


class VideoCamStream(videoStream.VideoStream):
    """
    Access a webcam or USB camera through a thread, to reduce I/O latency.
    Based on Adrian Rosebrock's work
    @see http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
    """

    def __init__(self, resolution=None, frame_rate=30, src=0):
        """
        Initialize the video stream + read the first frame.
        :param src: int for camera || string for video file path
        """
        # super().__init__()
        # super(self.__class__, self).__init__()
        # Works on Python 3.2 and lower
        videoStream.VideoStream.__init__(self, resolution)

        self.src = src
        self.stream = cv2.VideoCapture(src)

        # 3, 4 and 5 are resp. the width, height and frame rate constants,
        # that should work in OpenCV 3 and lower
        self.stream.set(3, self.resolution[0])
        self.stream.set(4, self.resolution[1])
        # depends on the camera, seems ignored by iSight
        self.stream.set(5, frame_rate)

        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def update(self):
        """
        Keep looping infinitely until the thread is stopped.
        :return:
        """
        while not self.stopped:
            # read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        """
        Overwrite parent to resize video files (stream.set has no effect on them)
        and to mirror image if constant is set.
        :return:
        """
        if isinstance(self.src, str):
            # todo this seems to be quite heavy
            self.frame = cv2.resize(self.frame, self.resolution)
            # assume video files never have to be mirrored
            return self.frame

        return cv2.flip(self.frame, 1) if self.MIRROR else self.frame
