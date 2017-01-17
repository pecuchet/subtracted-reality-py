import os
import pygame
import time


class PyScope:
    """
    Check installed frame buffer drivers.
    """
    screen = None

    def __init__(self):
        """
        Initializes a new pygame screen using the frame buffer
        Based on "Python GUI in Linux frame buffer"
        http://www.karoltomala.com/blog/?p=679
        """

        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print("I'm running under X display = {0}".format(disp_no))

        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib', 'xvfb', 'x11']
        self.found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                print('Driver: {0} success.'.format(driver))
                pygame.display.init()
            except pygame.error:
                print('Driver: {0} failed.'.format(driver))
                continue
            self.found = True
            break

        if not self.found:
            print('No suitable video driver found!')
        else:
            size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            print("Framebuffer size: %d x %d" % (size[0], size[1]))
            self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
            # Clear the screen to start
            self.screen.fill((0, 0, 0))
            # Initialise font support
            # pygame.font.init()
            # Render the screen
            pygame.display.update()

    def __del__(self):
        """Destructor to make sure pygame shuts down, etc."""

    def test(self):
        # Fill the screen with red (255, 0, 0)
        red = (255, 0, 0)
        self.screen.fill(red)
        # Update the display
        pygame.display.update()


# Create an instance of the PyScope class
scope = PyScope()

if scope.found:
    scope.test()
    time.sleep(10)
