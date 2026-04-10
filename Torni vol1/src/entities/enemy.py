import pygame

class Enemy:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = 1
        self.hp = 50
        self.alive = True

        # sprite sheet
        self.sprite_sheet = pygame.image.load("assets/sprites/monsters/skeleton/skeleton_o1.png").convert_alpha()

        # animaatio framet
        self.frames = []

        # animaatio
        self.frame_index = 0
        self.animation_speed = 0.2

        frame_width = 32
        frame_height = 32

        # jos hahmot ovat pystysuunnassa
        for i in range(4):  # kokeile 4–8 jos ei osu oikein
            frame = self.sprite_sheet.subsurface((0, i * frame_height, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (32, 32))
            self.frames.append(frame)

    def update(self, player):
        # seuraa pelaajaa
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed

        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        if self.rect.y > player.rect.y:
            self.rect.y -= self.speed

        # animaatio pyörii
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

    def draw(self, surface, camera):

        # vihollinen
        rect = camera.apply(self.rect)
        frame = self.frames[int(self.frame_index)]
        frame_rect = frame.get_rect(center=rect.center)
        surface.blit(frame, frame_rect)

        # HP bar tausta
        pygame.draw.rect(surface, (255, 0, 0), (rect.x, rect.y - 10, 30, 5))

        # HP bar vihreä
        hp_width = 30 * (self.hp / 100)
        pygame.draw.rect(surface, (0, 255, 0), (rect.x, rect.y - 10, hp_width, 5))


    def take_damage(self, amount):
        self.hp -= amount
        self.hp = max(0, self.hp)
        print("HIT!", self.hp)

        if self.hp <= 0:
            self.alive = False