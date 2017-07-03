from threading import Thread


class VideoStream:
    """
    Base class for threaded camera frames access.
    Based on Adrian Rosebrock's work.
    @see http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
    """
    MIRROR = True

    def __init__(self, resolution=None):
        self.resolution = resolution if resolution is not None else (640, 480)
        self.frame = None
        self.stopped = False

    def start(self):
        """
        Start a thread to read frames from the camera.
        Daemon argument is set to True, forcing the Thread to exit when the program stops.
        :return:
        """
        # Thread(target=self.update, args=(), daemon=True).start()
        # Works on Python 3.2 and lower
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        return

    def read(self):
        """
        Return the last read frame.
        :return:
        """
        return self.frame

    def stop(self):
        """
        The thread should be stopped.
        :return:
        """
        self.stopped = True
