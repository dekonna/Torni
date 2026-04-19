import pygame
import math
from src.entities.bullet import Bullet

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

    def update(self, mouse_x, mouse_y):

        moving = False
        keys = pygame.key.get_pressed()

        # WASD LIIKE
        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= self.speed
            self.direction = "up"

        if keys[pygame.K_s]:
            dy += self.speed
            self.direction = "down"

        if keys[pygame.K_a]:
            dx -= self.speed
            self.direction = "left"

        if keys[pygame.K_d]:
            dx += self.speed
            self.direction = "right"

        # 🔹 X-suunnassa
        self.rect.x += dx

        for rect in self.game.collision_rects:
            if self.rect.colliderect(rect):
                if dx > 0:
                    self.rect.right = rect.left
                elif dx < 0:
                    self.rect.left = rect.right

        # 🔹 Y-suunnassa
        self.rect.y += dy

        for rect in self.game.collision_rects:
            if self.rect.colliderect(rect):
                if dy > 0:
                    self.rect.bottom = rect.top
                elif dy < 0:
                    self.rect.top = rect.bottom

        # ANIMAATIO
        moving = dx != 0 or dy != 0

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

        self.angle = math.atan2(mouse_y, mouse_x) + math.pi

        keys = pygame.key.get_pressed()


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
        if self.inventory:
            weapon = self.inventory[self.current_weapon_index]

            if weapon.weapon_type == "ranged":
                start = camera.apply(self.rect).center

                end = (
                    start[0] + math.cos(self.angle) * 200,
                    start[1] + math.sin(self.angle) * 200
                )

                pygame.draw.line(screen, (255, 0, 0), start, end, 2)

        # ASE KÄDESSÄ
        if self.inventory:

            weapon = self.inventory[self.current_weapon_index]

            if weapon.image:
                weapon_distance = weapon.weapon_distance

                hand_offset_x = weapon.hand_offset_x
                hand_offset_y = weapon.hand_offset_y

                weapon_x = (
                        self.rect.centerx
                        + hand_offset_x
                        + math.cos(self.angle) * weapon_distance
                )

                weapon_y = (
                        self.rect.centery
                        + hand_offset_y
                        + math.sin(self.angle) * weapon_distance
                )

                rotated_weapon = pygame.transform.rotate(
                    weapon.image,
                    -math.degrees(self.angle) + weapon.rotation_offset
                )

                weapon_rect = rotated_weapon.get_rect(
                    center=camera.apply(
                        pygame.Rect(weapon_x, weapon_y, 0, 0)
                    ).center
                )

                screen.blit(rotated_weapon, weapon_rect)

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

        if not self.inventory:
            return

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