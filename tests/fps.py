import datetime
import logging


class FPS:
    """
    Adrian Rosebrock's class to echo frame rate to the console.
    @see http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
    """
    def __init__(self, file=None):
        if file:
            logging.basicConfig(filename=file, level=logging.DEBUG, format='%(asctime)s %(message)s')
            logging.info('*-'*20)
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self.log_to_file = file
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # start the timer
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()
        msg_time = "[INFO] elapsed time: {:.2f}".format(self.elapsed())
        msg_fps = "[INFO] approx. FPS: {:.2f}".format(self.fps())
        if self.log_to_file:
            logging.info(msg_time)
            logging.info(msg_fps)
            logging.info('*-' * 20)
        else:
            print(msg_time)
            print(msg_fps)

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()
