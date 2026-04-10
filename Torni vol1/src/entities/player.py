import pygame
import math
from src.entities.bullet import Bullet
from src.systems.weapons import Weapon

class Player:

    def __init__(self, game, x, y):
        self.game = game
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = 4

        self.direction = "down"

        self.hp = 100
        self.damage_cooldown = 0
        self.attack_cooldown = 0

        self.animations = {
            "down": [],
            "up": [],
            "left": [],
            "right": []
        }

        self.frame_index = 0
        self.animation_speed = 0.2

        self.bullets = []
        self.shoot_cooldown = 0
        self.angle = 0

        # ASEET / INVENTAARIO
        self.inventory = []
        self.current_weapon_index = 0

        self.inventory.append(Weapon("Pistol", "ranged", 10, 300, 200))
        self.inventory.append(Weapon("Bat", "melee", 15, 50, 400))

        self.last_attack = 0

        self.ui_font = pygame.font.Font(None, 24)

        # ladataan animaatiot
        for i in range(1, 7):  # koska alkaa 1:stä

            self.animations["down"].append(
                pygame.transform.scale(
                    pygame.image.load(f"assets/sprites/player/Run/Down/Base_run_down_{i}.png").convert_alpha(),
                    (32, 32)
                )
            )

            self.animations["up"].append(
                pygame.transform.scale(
                    pygame.image.load(f"assets/sprites/player/Run/Up/Base_run_up_{i}.png").convert_alpha(),
                    (32, 32)
                )
            )

            self.animations["left"].append(
                pygame.transform.scale(
                    pygame.image.load(f"assets/sprites/player/Run/Left/Base_run_left_{i}.png").convert_alpha(),
                    (32, 32)
                )
            )

            self.animations["right"].append(
                pygame.transform.scale(
                    pygame.image.load(f"assets/sprites/player/Run/Right/Base_run_right_{i}.png").convert_alpha(),
                    (32, 32)
                )
            )

    def update(self, world_x, world_y):

        moving = False
        keys = pygame.key.get_pressed()

        # WASD LIIKE
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.direction = "up"
            moving = True

        if keys[pygame.K_s]:
            self.rect.y += self.speed
            self.direction = "down"
            moving = True

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = "left"
            moving = True

        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = "right"
            moving = True

        # ANIMAATIO
        if moving:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.animations[self.direction]):
                self.frame_index = 0
        else:
            self.frame_index = 0

        # LUODIT
        for bullet in self.bullets:
            bullet.update()
        # poistetaan kuolleet luodit
        self.bullets = [b for b in self.bullets if getattr(b, "alive", True)]

        # COOLDOWN
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # TÄHTÄYS (360)
        dx = world_x - self.rect.centerx
        dy = world_y - self.rect.centery

        keys = pygame.key.get_pressed()

        # HIIRI ENSISIJAINEN
        self.angle = math.atan2(dy, dx)

        # NUOLINÄPPÄIMET vain jos niitä painetaan
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:

            if keys[pygame.K_UP]:
                self.angle = -math.pi / 2
            elif keys[pygame.K_DOWN]:
                self.angle = math.pi / 2
            elif keys[pygame.K_LEFT]:
                self.angle = math.pi
            elif keys[pygame.K_RIGHT]:
                self.angle = 0

    def draw(self, screen, camera):
        # pelaaja
        frame = self.animations[self.direction][int(self.frame_index)]
        screen.blit(frame, camera.apply(self.rect))

        # luodit
        for bullet in self.bullets:
            bullet.draw(screen, camera)

        # tähtäin (vain ranged aseelle)
        weapon = self.inventory[self.current_weapon_index]

        if weapon.weapon_type == "ranged":
            start = camera.apply(self.rect).center

            end = (
                start[0] + math.cos(self.angle) * 200,
                start[1] + math.sin(self.angle) * 200
            )

            pygame.draw.line(screen, (255, 0, 0), start, end, 2)

        # INVENTORY UI
        for i, weapon in enumerate(self.inventory):
            x = 10 + i * 110
            y = 50

            color = (200, 200, 200)

            if i == self.current_weapon_index:
                color = (255, 255, 0)

            pygame.draw.rect(screen, color, (x, y, 100, 40))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, 100, 40), 2)

            text = self.ui_font.render(weapon.name, True, (0, 0, 0))
            screen.blit(text, (x + 10, y + 10))

    def attack(self):
        weapon = self.inventory[self.current_weapon_index]

        print("ASE:", weapon.name, "TYPE:", weapon.weapon_type)

        now = pygame.time.get_ticks()

        if now - self.last_attack < weapon.cooldown:
            return

        self.last_attack = now

        if weapon.weapon_type == "ranged":
            print("AMPUI")
            self.shoot()

        elif weapon.weapon_type == "melee":
            print("LYÖ")
            self.melee_attack()

    def melee_attack(self):
        weapon = self.inventory[self.current_weapon_index]

        for enemy in self.game.enemies:
            dx = enemy.rect.centerx - self.rect.centerx
            dy = enemy.rect.centery - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance < weapon.range:
                enemy.take_damage(weapon.damage)

    def shoot(self):
        if self.shoot_cooldown == 0:
            dx = math.cos(self.angle)
            dy = math.sin(self.angle)

            bullet = Bullet(
                self.rect.centerx,
                self.rect.centery,
                dx,
                dy
            )

            self.bullets.append(bullet)
            self.shoot_cooldown = 15