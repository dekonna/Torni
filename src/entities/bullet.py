import pygame
import math

class Bullet:

    def __init__(self, x, y, dx, dy, damage=20, speed=10):
        self.rect   = pygame.Rect(x, y, 6, 6)
        self.speed  = speed
        self.damage = damage
        self.alive  = True

        length = math.hypot(dx, dy)
        if length != 0:
            self.dx = dx / length
            self.dy = dy / length
        else:
            self.dx = 0
            self.dy = 0


    def update(self, map_width=4000, map_height=4000):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        if (self.rect.x < 0 or self.rect.x > map_width or
                self.rect.y < 0 or self.rect.y > map_height):
            self.alive = False


    def draw(self, surface, camera):
        rect = camera.apply(self.rect)
        pygame.draw.rect(surface, (255, 255, 0), rect)