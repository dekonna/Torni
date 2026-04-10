import pygame
import math
import os
from src import asetukset
from pytmx.util_pygame import load_pygame
from src.UI.menu import Menu
from src.UI.character_creation import CharacterCreation
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.bullet import Bullet


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)

    def apply(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + asetukset.RENDER_WIDTH // 2 - target.rect.width // 2
        y = -target.rect.y + asetukset.RENDER_HEIGHT // 2 - target.rect.height // 2

        self.camera = pygame.Rect(x, y, self.camera.width, self.camera.height)

class Game:

    def __init__(self):
        pygame.init()

        self.font = pygame.font.Font(None, 30)
        self.font_big = pygame.font.Font(None, 80)

        # Luo peli-ikkuna
        self.screen = pygame.display.set_mode(
            (asetukset.SCREEN_WIDTH, asetukset.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(asetukset.TITLE)

        # Render surface (pixel scaling)
        self.game_surface = pygame.Surface(
            (asetukset.RENDER_WIDTH, asetukset.RENDER_HEIGHT)
        )

        # FPS kello
        self.clock = pygame.time.Clock()

        # Peli käynnissä
        self.running = True

        # Pelitila
        self.state = "MENU"

        # Menu
        self.menu = Menu(self.screen)
        self.character_creation = CharacterCreation(self.screen)

        # Kartta
        base_path = os.path.dirname(os.path.dirname(__file__))
        map_path = os.path.join(base_path, "maps", "Testi_Map.tmx")

        self.map = load_pygame(map_path)
        self.map_width = self.map.width * self.map.tilewidth
        self.map_height = self.map.height * self.map.tileheight

        self.reset_game()

        # pelaaja kamera
        self.camera = Camera(
            self.map.width * self.map.tilewidth,
            self.map.height * self.map.tileheight
        )

    def reset_game(self):
        self.player = Player(self, 100, 100)
        self.enemies = [Enemy(200, 200)]

    def run(self):

        print("Game loop started")

        while self.running:

            self.handle_events()

            # GAME
            if self.state == "GAME":
                self.update()
                self.draw_game()

            # GAME OVER
            elif self.state == "GAME_OVER":
                self.draw_game_over()

            # MENU
            elif self.state == "MENU":
                self.screen.fill((0, 0, 0))
                self.menu.draw()

            # CHARACTER
            elif self.state == "CHARACTER":
                self.screen.fill((0, 0, 0))
                self.character_creation.draw()

            pygame.display.flip()
            self.clock.tick(asetukset.FPS)

        pygame.quit()

    def handle_events(self):

        for event in pygame.event.get():

            # sulje peli
            if event.type == pygame.QUIT:
                self.running = False

            # aseenvaihto
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    print("Vaihdettiin ase 1")
                    self.player.current_weapon_index = 0

                elif event.key == pygame.K_2:
                    print("Vaihdettiin ase 2")
                    self.player.current_weapon_index = 1

                # ESC toimii kaikkialla
                elif event.key == pygame.K_ESCAPE:
                    if self.state == "GAME":
                        self.state = "MENU"
                    elif self.state == "CHARACTER":
                        self.state = "MENU"

            # MENU
            if self.state == "MENU":
                result = self.menu.handle_event(event)

                if result:
                    if result == "New Game":
                        self.reset_game()
                        self.state = "GAME"

                    elif result == "Character":
                        self.state = "CHARACTER"

                    elif result == "Quit":
                        self.running = False

            # GAME OVER
            elif self.state == "GAME_OVER":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()
                    self.state = "GAME"

            # GAME
            elif self.state == "GAME":

                # 🖱️ hiiri
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.player.attack()

                # ⌨️ SPACE
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player.attack()

    def update(self):
        keys = pygame.key.get_pressed()

        if self.state == "GAME":

            # HIIRI → WORLD
            mouse_x, mouse_y = pygame.mouse.get_pos()
            world_x = mouse_x + self.camera.camera.x
            world_y = mouse_y + self.camera.camera.y

            # PLAYER
            self.player.update(world_x, world_y)

            # cooldownit
            if self.player.damage_cooldown > 0:
                self.player.damage_cooldown -= 1

            if self.player.attack_cooldown > 0:
                self.player.attack_cooldown -= 1

            # viholliset
            for enemy in self.enemies[:]:
                enemy.update(self.player)

                # bullet collision
                for bullet in self.player.bullets[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.hp -= 20
                        bullet.alive = False
                        print("BULLET HIT!", enemy.hp)

                        if enemy.hp <= 0:
                            enemy.alive = False

                        break

                if self.player.rect.colliderect(enemy.rect):
                    if self.player.damage_cooldown == 0:
                        self.player.hp -= 15
                        self.player.damage_cooldown = 60
                        print("HIT!", self.player.hp)

                if not enemy.alive:
                    self.enemies.remove(enemy)
                    print("Enemy died")

            # pelaaja kuolee
            if self.player.hp <= 0:
                print("KUOLEMA TRIGGER")
                self.state = "GAME_OVER"

            # rajat
            self.player.rect.x = max(
                0,
                min(self.player.rect.x, self.map_width - self.player.rect.width)
            )

            self.player.rect.y = max(
                0,
                min(self.player.rect.y, self.map_height - self.player.rect.height)
            )

            # kamera
            self.camera.update(self.player)

    def draw(self):

        if self.state == "MENU":
            self.menu.draw()

        elif self.state == "CHARACTER":
            self.character_creation.draw()

        elif self.state == "GAME":
            self.draw_game()

        elif self.state == "GAME_OVER":
            self.draw_game_over()

    def draw_game(self):
        self.game_surface.fill(asetukset.BACKGROUND_COLOR)

        for layer in self.map.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, surf in layer.tiles():
                    rect = pygame.Rect(
                        x * asetukset.TILE_SIZE,
                        y * asetukset.TILE_SIZE,
                        asetukset.TILE_SIZE,
                        asetukset.TILE_SIZE
                    )

                    self.game_surface.blit(
                        surf,
                        self.camera.apply(rect)
                    )

        # piirtää pelaajan -> kaikki hahmot yhteen listaan
        entities = [self.player] + self.enemies

        # järjestetään Y-koordinaatin mukaan (depth)
        entities.sort(key=lambda e: e.rect.bottom)

        # piirretään oikeassa järjestyksessä
        for entity in entities:
            entity.draw(self.game_surface, self.camera)

            # tausta (punainen)
            pygame.draw.rect(self.game_surface, (255, 0, 0), (10, 10, 200, 20))

            # hp (vihreä)
            hp_width = 200 * (self.player.hp / 100)
            pygame.draw.rect(self.game_surface, (0, 255, 0), (10, 10, hp_width, 20))

        # HP bar teksti
        hp_text = self.font.render(f"HP: {self.player.hp}", True, (255, 255, 255))
        self.game_surface.blit(hp_text, (220, 10))

        # skaalaa ruudulle
        scaled_surface = pygame.transform.scale(
            self.game_surface,
            (asetukset.SCREEN_WIDTH, asetukset.SCREEN_HEIGHT)
        )
        self.screen.blit(scaled_surface, (0, 0))

    def draw_game_over(self):
        self.screen.fill((0, 0, 0))

        text = self.font_big.render("GAME OVER", True, (255, 0, 0))
        restart = self.font.render("Press R to restart", True, (255, 255, 255))

        text_rect = text.get_rect(center=(asetukset.SCREEN_WIDTH // 2, asetukset.SCREEN_HEIGHT // 2 - 30))
        restart_rect = restart.get_rect(center=(asetukset.SCREEN_WIDTH // 2, asetukset.SCREEN_HEIGHT // 2 + 20))

        self.screen.blit(text, text_rect)
        self.screen.blit(restart, restart_rect)


