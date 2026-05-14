import pygame


class BodyPart:

    def __init__(
        self,
        game,
        x,
        y,
        image,
        velocity_x,
        velocity_y
    ):

        self.game = game

        self.image = image

        self.rect = self.image.get_rect(
            center=(x, y)
        )

        self.x = float(x)
        self.y = float(y)

        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

        self.rotation = 0
        self.rotation_speed = 12

        self.timer = 1000

    def update(self):

        self.x += self.velocity_x
        self.y += self.velocity_y

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        self.velocity_x *= 0.92
        self.velocity_y *= 0.92

        # gravity
        self.velocity_y += 0.15

        self.rotation += self.rotation_speed

        if abs(self.velocity_x) < 0.1:
            self.velocity_x = 0

        if abs(self.velocity_y) < 0.1:
            self.velocity_y = 0

        self.timer -= 1

    def draw(self):
        rotated = pygame.transform.rotate(
            self.image,
            self.rotation
        )

        draw_x = (
                self.rect.centerx
                - self.game.camera.camera.x
        )

        draw_y = (
                self.rect.centery
                - self.game.camera.camera.y
        )

        rect = rotated.get_rect(
            center=(draw_x, draw_y)
        )

        self.game.game_surface.blit(
            rotated,
            rect
        )