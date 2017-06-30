import cv2
import videoStream


class VideoCamStream(videoStream.VideoStream):
    """
    Access a webcam or USB camera through a thread, to reduce I/O latency.
    Based on Adrian Rosebrock's work
    @see http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
    """

    def __init__(self, src=0):
        """
        Initialize the video stream + read the first frame.
        :param src: int for camera || string for video file path
        """
        #super().__init__()
        #super(self.__class__, self).__init__()
        videoStream.VideoStream.__init__(self)
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, 640)
        self.stream.set(4, 480)
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
