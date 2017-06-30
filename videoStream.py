from threading import Thread


class VideoStream:
    """
    Base class for threaded camera frames access.
    Based on Adrian Rosebrock's work.
    @see http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
    """

    def __init__(self):
        self.frame = None
        self.stopped = False

    def start(self):
        """
        Start a thread to read frames from the camera.
        Daemon argument is set to True, forcing the Thread to exit when the program stops.
        :return:
        """
        #Thread(target=self.update, args=(), daemon=True).start()
        # Works on Python 3.2 and lower
        Thread(target=self.update, args=()).start()
        self.daemon = True
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
