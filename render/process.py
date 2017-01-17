import cv2
import numpy
import config


def subtract(foreground, background):
    """
    OpenCV processing
    :param foreground:
    :param background:
    :return:
    """

    # convert the image into the HSV
    hsv = cv2.cvtColor(foreground, cv2.COLOR_BGR2HSV)
    # calculate the background mask
    image_mask = cv2.inRange(hsv, numpy.array(config.COLOUR_IN), numpy.array(config.COLOUR_OUT))
    # apply background mask on background to obscure the keyed color
    bg_mask = cv2.bitwise_and(background, background, mask=image_mask)
    # extract the foreground image from the camera feed
    fg_mask = cv2.bitwise_and(foreground, foreground, mask=cv2.bitwise_not(image_mask))

    return {
        bg_mask: bg_mask,
        fg_mask: fg_mask
    }


def mirror(frame):
    return cv2.flip(frame, 1)
