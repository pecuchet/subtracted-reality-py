import cv2
import sys
import config

from render import process

debug = config.DEBUG


def on_frame_buffer(cam_type, bg_file):
    """
    Display real time chroma key on the frame buffer through Pygame.
    :return:
    """
    from render import framebuffer
    global debug

    py_game_inst = framebuffer.PyGameRender(config.SIZE)
    background = _load_background(bg_file)
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


def in_window(cam_type, bg_file):
    """
    Display real time chroma key in a X server window through OpenCV.
    :return:
    """
    global debug

    # cv2.startWindowThread()  # This bugs: glib-gobject-critical ** g_object_unref assertion
    cv2.namedWindow(config.WINDOW_NAME, flags=cv2.WINDOW_AUTOSIZE)

    from videoCamStream import VideoCamStream
    
    # init cam
    video = VideoCamStream(src=0).start()

    # get background
    if bg_file.lower().endswith(('.mov', '.mp4')):
        bg_type = 'video'
        bg = VideoCamStream(src=config.DIR + '/assets/sea_4-3.mov').start()
    else:
        bg_type = 'image'
        bg = cv2.imread(config.DIR + '/assets/test-card_640x480.png')

    frame_count = 0
    fps = None

    if debug:
        from tests import fps
        fps = fps.FPS().start()

    # main loop
    while True:
        # ready to read background video?
        if bg_type == 'video' and not bg.stream.isOpened():
            continue

        # grab the frame from the threaded video stream
        foreground = video.read()

        if bg_type == 'video':
            # read background frame
            background = bg.read()
        else:
            background = bg

        # do not continue if no frame from cam yet
        # and prevent too much processing...
        frame_count += 1
        if foreground is None or frame_count % 40 != 0:
            continue
        frame_count = 0

        # if end of background video, loop back
        if bg_type == 'video' and background is None:
            print("The sea ends here\n")
            bg.stream.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        background = cv2.resize(background, config.SIZE)

        # do the chroma key
        frames = process.subtract(foreground, background)

        # CV2 output: composite both streams
        cv2.imshow(config.WINDOW_NAME, cv2.add(frames['bg_mask'], frames['fg_mask']))

        # update the FPS counter
        if debug:
            fps.update()

        # interrupt
        key = cv2.waitKey(40) & 0xFF
        if key in range(ord('a'), ord('z')):
            if key == ord('q'):
                if debug:
                    fps.stop()
                break
            elif key == ord('e'):
                config.COLOUR_IN[0] -= 1
            elif key == ord('r'):
                config.COLOUR_IN[0] += 1
            elif key == ord('t'):
                config.COLOUR_OUT[0] -= 1
            elif key == ord('y'):
                config.COLOUR_OUT[0] += 1
            elif key == ord('d'):
                config.COLOUR_IN[1] -= 1
            elif key == ord('f'):
                config.COLOUR_IN[1] += 1
            elif key == ord('g'):
                config.COLOUR_OUT[1] -= 1
            elif key == ord('h'):
                config.COLOUR_OUT[1] += 1
            elif key == ord('c'):
                config.COLOUR_IN[2] -= 1
            elif key == ord('v'):
                config.COLOUR_IN[2] += 1
            elif key == ord('b'):
                config.COLOUR_OUT[2] -= 1
            elif key == ord('n'):
                config.COLOUR_OUT[2] += 1
            print 'LOWER: %s UPPER: %s' % (config.COLOUR_IN, config.COLOUR_OUT)

    video.stop()
    cv2.destroyAllWindows()
    sys.exit()


def _load_background(file):
    global debug
    if not file and debug:
        return cv2.imread(config.DIR + '/assets/test-card_640x480.png')
    if file.lower().endswith(('.mov', '.mp4')):
        return cv2.VideoCapture(file)
    # let's assume it is an image file
    return cv2.imread(file)


def _start_camera(cam_type):
    if type == 'pi':
        from videoPiStream import VideoPiStream
        return VideoPiStream(resolution=config.SIZE).start()
    else:
        from videoCamStream import VideoCamStream
        return VideoCamStream(src=0).start()

def main():
    #in_window('', config.DIR + '/assets/sea_4-3.mp4')
    in_window('', config.DIR + '/assets/test-card_640x480.png')

if __name__ == '__main__':
    main()
