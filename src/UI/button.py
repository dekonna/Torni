import pygame


class Button:

    def __init__(self, text, center):

        self.text = text
        self.font = pygame.font.SysFont(None, 50)

        self.image = self.font.render(text, True, (255,0,0))
        self.rect = self.image.get_rect(center=center)


    def draw(self, screen):
        screen.blit(self.image, self.rect)