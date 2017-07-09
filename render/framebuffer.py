import cv2
import pygame
import numpy


class PyGameRender:

    def __init__(self, resolution=None):
        # os.putenv('SDL_VIDEODRIVER', 'directfb')
        pygame.display.init()

        if resolution:
            self.screen_size = resolution
        else:
            self.screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        # see https://www.pygame.org/docs/ref/display.html
        # opengl, fullscreen ... options
        self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN | pygame.HWSURFACE, 0) #  -2147483648
        self.surface = pygame.Surface(self.screen.get_size())

    def render(self, cv_image):
        # todo can this be somewhere else?
        # todo do we really need all conversions BGR > HSV > BGR > RGB ...
        # todo probably better to convert config HSV colours to RGB
        # @see https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        image = numpy.rot90(cv_image)

        # frame = pygame.surfarray.make_surface(frame)
        pygame.surfarray.blit_array(self.surface, image)
        self.screen.blit(self.surface, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return True

        return False

    def stop(self):
        pygame.quit()
