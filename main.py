import config
import cv2
import os
import sys

from render import process

debug = config.DEBUG
bg_type = 'image'

if config.CAMERA == 'pi':
    from videoPiStream import VideoPiStream
else:
    from videoCamStream import VideoCamStream


def on_frame_buffer(bg_file):
    """
    Display real time chroma key on the frame buffer through Pygame.
    :return:
    """
    from render import framebuffer
    global debug

    py_game_inst = framebuffer.PyGameRender(config.SIZE)
    background = _load_background(bg_file)
    video = _start_camera()

    frame_count = 0
    fps = None

    if debug:
        from tests import fps
        fps = fps.FPS(file=os.path.join(config.DIR, config.LOG)).start()

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
        stop = py_game_inst.render(cv2.add(frames['bg_mask'], frames['fg_mask']))

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


def in_window(bg_file):
    """
    Display real time chroma key in a X server window through OpenCV.
    :return:
    """
    global debug, bg_type

    # cv2.startWindowThread()  # This bugs: glib-gobject-critical ** g_object_unref assertion
    cv2.namedWindow(config.WINDOW_NAME, flags=cv2.WINDOW_AUTOSIZE)
    # todo full screen
    # cv2.namedWindow(config.WINDOW_NAME, flags=cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty(config.WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    # init cam
    video = _start_camera()

    # get background
    bg = _load_background(bg_file)

    frame_count = 0
    fps = None

    if debug:
        from tests import fps
        fps = fps.FPS().start()

    # main loop
    while True:
        # prevent too much processing...
        frame_count += 1
        if frame_count % 40 != 0:
            continue
        frame_count = 0

        # background video ready?
        if bg_type == 'video' and not bg.stream.isOpened():
            continue

        # grab the frame from the threaded video stream
        foreground = video.read()

        # do not continue if no frame from cam yet
        if foreground is None:
            continue

        # read background frame
        background = bg.read() if bg_type == 'video' else bg

        # if end of background video, loop back
        # todo use CV_CAP_PROP_FRAME_COUNT & CV_CAP_PROP_POS_FRAMES
        if bg_type == 'video' and background is None:
            print("The sea ends here\n")
            bg.stream.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # let's do this in VideoCamStream since PiCamera has an option for it
        # foreground = cv2.flip(foreground, 1)

        # do this outside the loop (for images)
        # background = cv2.resize(background, config.SIZE)
        # not needed: video is already resized in class
        # foreground = cv2.resize(foreground, config.SIZE)

        if debug:
            cv2.putText(foreground, '         H    S    V', (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, 0, 1)
            cv2.putText(foreground, 'LOWER: %s' % (config.COLOUR_IN), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, 0, 1)
            cv2.putText(foreground, 'UPPER: %s' % (config.COLOUR_OUT), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, 0, 1)

        # do the chroma key
        frames = process.subtract(foreground, background)

        # CV2 output: composite both streams
        cv2.imshow(config.WINDOW_NAME, cv2.add(frames['bg_mask'], frames['fg_mask']))

        # update the FPS counter
        if debug:
            fps.update()

        # interrupt
        key = cv2.waitKey(10) & 0xFF
        if key in range(ord('A'), ord('z')):
            if key == ord('q'):
                if debug:
                    fps.stop()
                break
            elif key == ord('D'):
                debug = not debug
            elif key == ord('e') and 0 < config.COLOUR_IN[0]:
                config.COLOUR_IN[0] -= 1
            elif key == ord('r') and config.COLOUR_IN[0] < config.COLOUR_OUT[0]:
                config.COLOUR_IN[0] += 1
            elif key == ord('t') and config.COLOUR_IN[0] < config.COLOUR_OUT[0]:
                config.COLOUR_OUT[0] -= 1
            elif key == ord('y') and config.COLOUR_OUT[0] < 179:
                config.COLOUR_OUT[0] += 1
            elif key == ord('d') and 0 < config.COLOUR_IN[1]:
                config.COLOUR_IN[1] -= 1
            elif key == ord('f') and config.COLOUR_IN[1] < config.COLOUR_OUT[1]:
                config.COLOUR_IN[1] += 1
            elif key == ord('g') and config.COLOUR_IN[1] < config.COLOUR_OUT[1]:
                config.COLOUR_OUT[1] -= 1
            elif key == ord('h') and config.COLOUR_OUT[1] < 255:
                config.COLOUR_OUT[1] += 1
            elif key == ord('c') and 0 < config.COLOUR_IN[2]:
                config.COLOUR_IN[2] -= 1
            elif key == ord('v') and config.COLOUR_IN[2] < config.COLOUR_OUT[2]:
                config.COLOUR_IN[2] += 1
            elif key == ord('b') and config.COLOUR_IN[2] < config.COLOUR_OUT[2]:
                config.COLOUR_OUT[2] -= 1
            elif key == ord('n') and config.COLOUR_OUT[2] < 255:
                config.COLOUR_OUT[2] += 1
            #if debug:
            #    print 'LOWER: %s UPPER: %s' % (config.COLOUR_IN, config.COLOUR_OUT)

    video.stop()
    cv2.destroyAllWindows()
    sys.exit()


def _load_background(file):
    """
    Decide what to load as background: an image or a video
    :param file:
    :return:
    """
    global debug, bg_type
    if file.lower().endswith(('.mov', '.mp4')):
        bg_type = 'video'
        return VideoCamStream(resolution=config.SIZE, frame_rate=config.FRAMERATE, src=file).start()
    # let's assume it's an image file
    bg_type = 'image'
    bg_img = cv2.imread(file)
    return cv2.resize(bg_img, config.SIZE)


def _start_camera():
    """
    Start PiCamera or web cam based on /config.py params
    :return:
    """
    if config.CAMERA == 'pi':
        return VideoPiStream(resolution=config.SIZE, frame_rate=config.FRAMERATE).start()
    else:
        return VideoCamStream(resolution=config.SIZE, frame_rate=config.FRAMERATE, src=config.CAMERA).start()


def main():
    if len(sys.argv) > 1:
        config.BG_FILE = sys.argv[0]
    in_window(os.path.join(config.DIR, config.BG_FILE))

if __name__ == '__main__':
    main()
