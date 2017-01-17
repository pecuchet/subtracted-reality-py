import pygame
import numpy


class PyGameRender:

    def __init__(self, screen_size):
        # os.putenv('SDL_VIDEODRIVER', 'directfb')
        pygame.display.init()

        if screen_size:
            self.screen_size = screen_size
        else:
            self.screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        self.screen = pygame.display.set_mode(self.screen_size, -2147483648)
        self.surface = pygame.Surface(self.screen.get_size())

    def render(self, cv_image):
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
