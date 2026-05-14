import pygame
import os
import random
import math

from src.save_manager import SaveManager
from src import asetukset


class Menu:

    def __init__(self, screen):

        # =========================
        # SCREEN
        # =========================

        self.screen = screen

        # =========================
        # FONT PATH
        # =========================

        base_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        )

        font_path = os.path.join(
            base_path,
            "assets",
            "menu",
            "fonts",
            "Rajdhani-SemiBold.ttf"
        )

        # =========================
        # FONTS
        # =========================

        self.font_title = pygame.font.Font(
            font_path,
            100
        )

        self.font_item = pygame.font.Font(
            font_path,
            48
        )

        # =========================
        # MENU ITEMS
        # =========================

        self.items = self.build_menu_items()

        self.item_rects = []
        self.selected_index = 0

        # =========================
        # SIGNAL EFFECT TIMER
        # =========================

        self.signal_timer = 0

        # =========================
        # MENU LAYOUT
        # =========================

        self.start_y = 270
        self.spacing = 82

        self.menu_x = 110

        # =========================
        # BACKGROUND IMAGE
        # =========================

        bg_path = os.path.join(
            base_path,
            "assets",
            "menu",
            "backgrounds",
            "main_menu_1.png"
        )

        self.background = pygame.image.load(bg_path).convert()

        # =========================
        # SCALE BACKGROUND
        # =========================

        self.background = pygame.transform.scale(
            self.background,
            (asetukset.SCREEN_WIDTH, asetukset.SCREEN_HEIGHT)
        )

        self.bg_x = 0
        self.bg_y = 0

        # =========================
        # RAIN PARTICLES
        # =========================

        self.rain_drops = []

        for _ in range(320):

            x = random.randint(
                0,
                asetukset.SCREEN_WIDTH
            )

            y = random.randint(
                0,
                asetukset.SCREEN_HEIGHT
            )

            length = random.randint(6, 12)
            speed = random.randint(10, 18)

            self.rain_drops.append([
                x,
                y,
                length,
                speed
            ])

        # =========================
        # LIGHTNING EFFECT
        # =========================

        self.lightning_alpha = 0
        self.lightning_timer = random.randint(500, 1400)

        self.second_flash = False
        self.second_flash_timer = 0

        # =========================
        # FOG MOVEMENT
        # =========================

        self.fog_offset = 0

        # =========================
        # STATIC FOG PATCHES
        # =========================

        self.fog_patches = []

        layers = [

            (760, 820, 900, 120, 22),
            (500, 760, 700, 90, 16),
            (1050, 870, 1100, 150, 26),

        ]

        for x, y, w, h, alpha in layers:

            patch = pygame.Surface((w, h), pygame.SRCALPHA)

            patch.set_alpha(85)

            for _ in range(140):
                ellipse_w = random.randint(220, 850)
                ellipse_h = random.randint(12, 42)

                ellipse_x = random.randint(-120, w - 120)
                ellipse_y = random.randint(0, h - 20)

                pygame.draw.ellipse(
                    patch,
                    (
                        210,
                        220,
                        225,
                        random.randint(1, alpha)
                    ),
                    (
                        ellipse_x,
                        ellipse_y,
                        ellipse_w,
                        ellipse_h
                    )
                )

            self.fog_patches.append(
                (patch, x, y)
            )

    def build_menu_items(self):

        # =========================
        # BASE MENU ITEMS
        # =========================

        items = [
            "New Game"
        ]

        # =========================
        # CONTINUE IF SAVE EXISTS
        # =========================

        if SaveManager.load():
            items.append("Continue")

        # =========================
        # EXTRA MENU ITEMS
        # =========================

        items += [
            "Load Game",
            "Save Game",
            "Character",
            "Options",
            "Quit"
        ]

        return items

    def refresh(self):

        # =========================
        # REFRESH MENU
        # =========================

        self.items = self.build_menu_items()

        if self.selected_index >= len(self.items):
            self.selected_index = 0

    def draw(self):

        # =========================
        # UPDATE SIGNAL TIMER
        # =========================

        self.signal_timer += 1

        # =========================
        # LIGHTNING UPDATE
        # =========================

        self.lightning_timer -= 1

        if self.lightning_timer <= 0:

            # Main flash
            self.lightning_alpha = random.randint(
                45,
                80
            )

            # Enable second flash
            self.second_flash = True

            self.second_flash_timer = random.randint(
                16,
                28
            )

            # Next lightning strike
            self.lightning_timer = random.randint(
                500,
                1400
            )

        # =========================
        # SECOND LIGHTNING FLASH
        # =========================

        if self.second_flash:

            self.second_flash_timer -= 1

            if self.second_flash_timer <= 0:

                self.lightning_alpha = random.randint(
                    35,
                    60
                )

                self.second_flash = False

        # =========================
        # LIGHTNING FADE
        # =========================

        if self.lightning_alpha > 0:

            self.lightning_alpha -= random.randint(
                3,
                7
            )

        # =========================
        # DRAW BACKGROUND
        # =========================

        self.screen.blit(
            self.background,
            (self.bg_x, self.bg_y)
        )

        # =========================
        # DARK OVERLAY
        # =========================

        overlay = pygame.Surface(
            (
                asetukset.SCREEN_WIDTH,
                asetukset.SCREEN_HEIGHT
            )
        )

        overlay.set_alpha(70)
        overlay.fill((0, 0, 0))

        self.screen.blit(overlay, (0, 0))

        # =========================
        # LEFT CINEMATIC GRADIENT
        # =========================

        gradient = pygame.Surface(
            (
                520,
                asetukset.SCREEN_HEIGHT
            ),
            pygame.SRCALPHA
        )

        for x in range(520):

            alpha = max(
                0,
                210 - (x * 0.42)
            )

            pygame.draw.line(
                gradient,
                (0, 0, 0, int(alpha)),
                (x, 0),
                (x, asetukset.SCREEN_HEIGHT)
            )

        self.screen.blit(gradient, (0, 0))

        # =========================
        # TITLE SIGNAL FLICKER
        # =========================

        title_brightness = 225

        if self.signal_timer % 180 < 3:
            title_brightness = 170

        elif self.signal_timer % 240 < 2:
            title_brightness = 200

        # =========================
        # DRAW TITLE
        # =========================

        title = self.font_title.render(
            "TORNI",
            True,
            (
                title_brightness,
                title_brightness,
                title_brightness
            )
        )

        title_rect = title.get_rect(
            topleft=(80, 110)
        )

        self.screen.blit(
            title,
            title_rect
        )

        # =========================
        # MENU ITEMS
        # =========================

        self.item_rects = []

        mouse_pos = pygame.mouse.get_pos()

        hover_found = False

        for i, item in enumerate(self.items):

            y = self.start_y + i * self.spacing

            # =========================
            # MOUSE HOVER
            # =========================

            temp_rect = self.font_item.render(
                item,
                True,
                (255, 255, 255)
            ).get_rect(
                topleft=(
                    self.menu_x,
                    y
                )
            )

            if temp_rect.collidepoint(mouse_pos):

                self.selected_index = i
                hover_found = True

            # =========================
            # SIGNAL FLICKER
            # =========================

            brightness = 0
            x_offset = 0

            if i == self.selected_index:

                x_offset = 4

                if self.signal_timer % 90 < 4:
                    brightness = -35

            # =========================
            # TEXT COLOR
            # =========================

            if i == self.selected_index:

                color = (
                    220 + brightness,
                    220 + brightness,
                    220 + brightness
                )

            else:

                color = (
                    110,
                    110,
                    110
                )

            # =========================
            # DRAW MENU TEXT
            # =========================

            text = self.font_item.render(
                item,
                True,
                color
            )

            rect = text.get_rect(
                topleft=(
                    self.menu_x + x_offset,
                    y
                )
            )

            self.item_rects.append(rect)

            self.screen.blit(
                text,
                rect
            )

        # =========================
        # REMOVE HOVER IF MOUSE AWAY
        # =========================

        if not hover_found:
            self.selected_index = -1

        # =========================
        # SUBTLE SKY LIGHTNING
        # =========================

        if self.lightning_alpha > 0:

            lightning_surface = pygame.Surface(
                (
                    asetukset.SCREEN_WIDTH,
                    asetukset.SCREEN_HEIGHT
                ),
                pygame.SRCALPHA
            )

            # =========================
            # TOP SKY BRIGHTENING
            # =========================

            for y in range(350):

                alpha = int(
                    (1 - y / 350)
                    * self.lightning_alpha
                    * 0.42
                )

                pygame.draw.line(
                    lightning_surface,
                    (
                        190,
                        205,
                        255,
                        alpha
                    ),
                    (0, y),
                    (asetukset.SCREEN_WIDTH, y)
                )

            # =========================
            # VERY SUBTLE GLOBAL LIGHT
            # =========================

            subtle_flash = pygame.Surface(
                (
                    asetukset.SCREEN_WIDTH,
                    asetukset.SCREEN_HEIGHT
                ),
                pygame.SRCALPHA
            )

            subtle_flash.fill(
                (
                    120,
                    135,
                    170,
                    int(self.lightning_alpha * 0.075)
                )
            )

            lightning_surface.blit(
                subtle_flash,
                (0, 0)
            )

            self.screen.blit(
                lightning_surface,
                (0, 0)
            )

        # =========================
        # GROUND FOG
        # =========================

        fog_surface = pygame.Surface(
            (
                asetukset.SCREEN_WIDTH,
                asetukset.SCREEN_HEIGHT
            ),
            pygame.SRCALPHA
        )

        fog_time = pygame.time.get_ticks() * 0.000002

        fog_surface = pygame.Surface(
            (
                asetukset.SCREEN_WIDTH,
                asetukset.SCREEN_HEIGHT
            ),
            pygame.SRCALPHA
        )

        fog_time = pygame.time.get_ticks() * 0.00000035

        for i, (patch, x, y) in enumerate(self.fog_patches):
            drift = math.sin(fog_time + i * 0.7) * 1.2

            fog_surface.blit(
                patch,
                (
                    x - patch.get_width() // 2 + drift,
                    y
                )
            )

        self.screen.blit(fog_surface, (0, 0))

        # =========================
        # DRAW RAIN FOREGROUND
        # =========================

        for rain in self.rain_drops:

            x, y, length, speed = rain

            # Random rain brightness
            rain_shade = random.randint(60, 130)

            pygame.draw.line(
                self.screen,
                (
                    rain_shade,
                    rain_shade,
                    rain_shade
                ),
                (x, y),

                # Wind direction
                (x - 4, y + length),

                1
            )

            # Heavy wind movement
            rain[1] += speed
            rain[0] -= speed * 0.75

            # Reset rain drop
            if rain[1] > asetukset.SCREEN_HEIGHT:

                rain[0] = random.randint(
                    0,
                    asetukset.SCREEN_WIDTH
                )

                rain[1] = random.randint(
                    -200,
                    -20
                )

    def handle_event(self, event):

        # =========================
        # KEYBOARD INPUT
        # =========================

        if event.type == pygame.KEYDOWN:

            # DOWN
            if event.key == pygame.K_DOWN:

                self.selected_index = (
                    self.selected_index + 1
                ) % len(self.items)

            # UP
            elif event.key == pygame.K_UP:

                self.selected_index = (
                    self.selected_index - 1
                ) % len(self.items)

            # ENTER
            elif event.key == pygame.K_RETURN:

                return self.items[
                    self.selected_index
                ]

        # =========================
        # MOUSE INPUT
        # =========================

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            for i, rect in enumerate(
                self.item_rects
            ):

                if rect.collidepoint(mouse_pos):
                    return self.items[i]

        return None