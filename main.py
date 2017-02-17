import cv2
import sys
import config

from render import process

debug = config.DEBUG


def _load_background():
    return cv2.imread(config.DIR + '/assets/test-card_640x480.png')


def _start_camera(cam_type):
    if type == 'pi':
        from videoPiStream import VideoPiStream
        return VideoPiStream(resolution=config.SIZE).start()
    else:
        from videoCamStream import VideoCamStream
        return VideoCamStream(src=0).start()


def on_frame_buffer(cam_type):
    """
    Display real time chroma key on the frame buffer through Pygame.
    :return:
    """
    from render import framebuffer
    global debug

    py_game_inst = framebuffer.PyGameRender(config.SIZE)
    background = _load_background()
    video = _start_camera(cam_type)

    frame_count = 0
    fps = None

    if debug:
        from tests import fps
        fps = fps.FPS().start()

    while True:
        # grab the frame from the threaded video stream
        foreground = video.read()

        # do not continue if no frame from cam yet
        # and prevent too much processing...
        frame_count += 1
        if foreground is None or frame_count % 40 != 0:
            continue
        frame_count = 0

        # do the chroma key
        frames = process.subtract(foreground, background)

        # Output to Pygame (frame buffer)
        stop = py_game_inst.render(cv2.add(frames.bg_mask, frames.fg_mask))

        # update the FPS counter
        if debug:
            fps.update()

        if stop:
            if debug:
                fps.stop()
            break

    # close
    py_game_inst.stop()
    video.stop()
    sys.exit()


def in_window(cam_type):
    """
    Display real time chroma key in a X server window through OpenCV.
    :return:
    """
    global debug

    # cv2.startWindowThread()  # This bugs: glib-gobject-critical ** g_object_unref assertion

    cv2.namedWindow(config.WINDOW_NAME, flags=cv2.WINDOW_AUTOSIZE)
    background = _load_background()
    video = _start_camera(cam_type)

    frame_count = 0
    fps = None

    if debug:
        from tests import fps
        fps = fps.FPS().start()

    # main loop
    while True:
        # grab the frame from the threaded video stream
        foreground = video.read()

        # do not continue if no frame from cam yet
        # and prevent too much processing...
        frame_count += 1
        if foreground is None or frame_count % 40 != 0:
            continue
        frame_count = 0

        # do the chroma key
        frames = process.subtract(foreground, background)

        # CV2 output: composite both streams
        cv2.imshow(config.WINDOW_NAME, cv2.add(frames['bg_mask'], frames['fg_mask']))

        # update the FPS counter
        if debug:
            fps.update()

        # interrupt
        if cv2.waitKey(40) & 0xFF == ord('q'):
            if debug:
                fps.stop()
            break

    video.stop()
    cv2.destroyAllWindows()
    sys.exit()
