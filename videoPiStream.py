import videoStream
from picamera.array import PiRGBArray
from picamera import PiCamera


class VideoPiStream(videoStream.VideoStream):
    """
    Access Raspberry Pi camera through a thread to reduce I/O latency.
    Based on Adrian Rosebrock's work
    @see http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/

    PiCamera default settings:
        camera.sharpness = 0
        camera.contrast = 0
        camera.brightness = 50
        camera.saturation = 0
        camera.ISO = 0
        camera.video_stabilization = False
        camera.exposure_compensation = 0
        camera.exposure_mode = 'auto'
        camera.meter_mode = 'average'
        camera.awb_mode = 'auto'
        camera.image_effect = 'none'
        camera.color_effects = None
        camera.rotation = 0
        camera.hflip = False
        camera.vflip = False
        camera.crop = (0.0, 0.0, 1.0, 1.0)
    """

    def __init__(self, resolution=(640, 480), framerate=25):
        """
        Initialize the camera and stream
        :param resolution:
        :param framerate:
        """
        self.camera = PiCamera()
        # self.camera.hflip = True
        # self.camera.vflip = True
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
        self.frame = None
        self.stopped = False

    def update(self):
        """
        Keep looping infinitely until the thread is stopped.
        :return:
        """
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return
