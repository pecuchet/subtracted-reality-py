import config
import cv2
import os
import sys

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
        bg = VideoCamStream(src=bg_file).start()
    else:
        bg_type = 'image'
        background = cv2.imread(bg_file)

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

        foreground = cv2.flip(foreground, 1)

        background = cv2.resize(background, config.SIZE)
        foreground = cv2.resize(foreground, config.SIZE)

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
    if len(sys.argv) > 1:
        config.FILE = sys.argv[0]
    in_window('', os.path.join(config.DIR, config.FILE))

if __name__ == '__main__':
    main()
