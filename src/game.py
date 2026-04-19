import pygame
import math
import os
from src import asetukset
from pytmx.util_pygame import load_pygame
from src.UI.menu import Menu
from src.UI.character_creation import CharacterCreation
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.pickup import WeaponPickup
from src.save_manager import SaveManager
from src.systems.weapon_factory import WeaponFactory

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

        # invetory
        self.inventory_open = False

        # Kartta
        self.floor_maps = [
            "Testi_Map.tmx",
            "Testi_Map.tmx",
            "Testi_Map.tmx"
        ]

        self.current_floor = 0
        self.load_map(self.floor_maps[self.current_floor])

        self.messages = []
        self.message_timer = 0

        self.reset_game()

        # pelaaja kamera
        self.camera = Camera(
            self.map.width * self.map.tilewidth,
            self.map.height * self.map.tileheight
        )

    def reset_game(self):
        self.player = Player(
            self,
            self.player_spawn[0],
            self.player_spawn[1]
        )
        self.enemies = [
            Enemy(self, x, y)
            for x, y in self.enemy_spawns
        ]

        bat_weapon = WeaponFactory.create("Bat")
        pistol = WeaponFactory.create("Pistol")
        self.player.inventory.append(pistol)

        self.pickups = [
            WeaponPickup(
                300,
                300,
                bat_weapon,
                bat_weapon.image
            )
        ]

    def run(self):

        print("Game loop started")

        while self.running:

            self.handle_events()

            # GAME
            if self.state == "GAME":

                if not self.inventory_open:
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

            # Sulje peli
            if event.type == pygame.QUIT:
                self.running = False

            # =========================
            # NÄPPÄIMET
            # =========================
            if event.type == pygame.KEYDOWN:

                # Save
                if event.key == pygame.K_F5:
                    SaveManager.save(self)
                    self.add_message("Game Saved")
                    self.menu.refresh()

                # NEXT FLOOR TEST
                elif event.key == pygame.K_F6:
                    self.next_floor()

                # Aseenvaihto
                elif event.key == pygame.K_1:
                    if len(self.player.inventory) > 0:
                        self.player.current_weapon_index = 0

                elif event.key == pygame.K_2:
                    if len(self.player.inventory) > 1:
                        self.player.current_weapon_index = 1

                # Inventory toggle
                elif event.key == pygame.K_i:
                    if self.state == "GAME":
                        self.inventory_open = not self.inventory_open

                # PICK UP
                elif event.key == pygame.K_f:
                    if self.state == "GAME":

                        for pickup in self.pickups[:]:
                            if self.player.rect.colliderect(pickup.rect):
                                self.player.inventory.append(pickup.weapon)
                                self.add_message(f"Picked up {pickup.weapon.name}")
                                self.pickups.remove(pickup)
                                break

                            if self.exit_rect and self.player.rect.colliderect(self.exit_rect):
                                self.next_floor()


                # ESC
                elif event.key == pygame.K_ESCAPE:
                    if self.state == "GAME":
                        self.state = "MENU"

                    elif self.state == "CHARACTER":
                        self.state = "MENU"

                # Restart
                elif event.key == pygame.K_r:
                    if self.state == "GAME_OVER":
                        self.reset_game()
                        self.state = "GAME"

            # =========================
            # MENU
            # =========================
            if self.state == "MENU":

                result = self.menu.handle_event(event)

                if result == "New Game":
                    self.reset_game()
                    self.state = "GAME"

                elif result == "Continue":
                    self.load_game()
                    self.state = "GAME"

                elif result == "Save Game":
                    SaveManager.save(self)
                    self.menu.refresh()

                elif result == "Load Game":
                    self.load_game()
                    self.state = "GAME"

                elif result == "Character":
                    self.state = "CHARACTER"

                elif result == "Quit":
                    self.running = False

            # =========================
            # GAME
            # =========================
            elif self.state == "GAME":

                if not self.inventory_open:

                    # Mouse attack
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.player.attack()

                    # Space attack
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.player.attack()

    def update(self):
        keys = pygame.key.get_pressed()

        if self.state == "GAME":
            # mouse position in pixels on screen
            mouse_x, mouse_y = pygame.mouse.get_pos()

            mouse_x = asetukset.SCREEN_WIDTH//2-mouse_x
            mouse_y = asetukset.SCREEN_HEIGHT//2-mouse_y
            # PLAYER
            self.player.update(mouse_x, mouse_y)

            # cooldownit
            if self.player.damage_cooldown > 0:
                self.player.damage_cooldown -= 1

            if self.player.attack_cooldown > 0:
                self.player.attack_cooldown -= 1

            # =========================
            # 🔹 VIHOLLISET + BULLET HIT
            # =========================
            for enemy in self.enemies[:]:
                enemy.update(self.player)

                for bullet in self.player.bullets[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.hp -= 20
                        bullet.alive = False
                        print("BULLET HIT!", enemy.hp)

                        if enemy.hp <= 0:
                            enemy.alive = False

                        break

                # player vs enemy
                if self.player.rect.colliderect(enemy.rect):
                    if self.player.damage_cooldown == 0:
                        self.player.hp -= 15
                        self.player.damage_cooldown = 60
                        print("HIT!", self.player.hp)

                if not enemy.alive:
                    self.enemies.remove(enemy)
                    print("Enemy died")

            # =========================
            # 🔥 BULLET VS WALLS (ERILLINEN!)
            # =========================
            for bullet in self.player.bullets[:]:
                for rect in self.collision_rects:
                    if bullet.rect.colliderect(rect):
                        bullet.alive = False
                        break

            # 🔹 poista kuolleet bulletit
            self.player.bullets = [b for b in self.player.bullets if b.alive]

            # =========================
            # MUU LOGIIKKA
            # =========================

            if self.message_timer > 0:
                self.message_timer -= 1

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

        mouse_x, mouse_y = pygame.mouse.get_pos()

        pygame.draw.circle(
            self.game_surface,
            (255, 0, 0),
            (int(mouse_x), int(mouse_y)),
            5
        )

        # KARTTA
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

        # PICKUPIT
        for pickup in self.pickups:
            pickup.draw(self.game_surface, self.camera)

        # PICKUP PROMPT
        for pickup in self.pickups:
            if self.player.rect.colliderect(pickup.rect):
                text = self.font.render(
                    f"Press F to pick up {pickup.weapon.name}",
                    True,
                    (255, 255, 255)
                )

                text_rect = text.get_rect(
                    center=(asetukset.RENDER_WIDTH // 2, asetukset.RENDER_HEIGHT - 30)
                )

                self.game_surface.blit(text, text_rect)
                break

        # ENTITYT
        entities = [self.player] + self.enemies
        entities.sort(key=lambda e: e.rect.bottom)

        for entity in entities:
            entity.draw(self.game_surface, self.camera)

        # HP BAR
        pygame.draw.rect(self.game_surface, (255, 0, 0), (10, 10, 200, 20))

        hp_width = 200 * (self.player.hp / 100)
        pygame.draw.rect(self.game_surface, (0, 255, 0), (10, 10, hp_width, 20))

        hp_text = self.font.render(f"HP: {self.player.hp}", True, (255, 255, 255))
        self.game_surface.blit(hp_text, (220, 10))

        self.draw_message_box()

        # SCALE
        scaled_surface = pygame.transform.scale(
            self.game_surface,
            (asetukset.SCREEN_WIDTH, asetukset.SCREEN_HEIGHT)
        )

        scaled_width = asetukset.SCREEN_WIDTH
        scaled_height = int(asetukset.SCREEN_WIDTH * asetukset.RENDER_HEIGHT / asetukset.RENDER_WIDTH)

        scaled_surface = pygame.transform.scale(self.game_surface, (scaled_width, scaled_height))

        offset_y = (asetukset.SCREEN_HEIGHT - scaled_height) // 2

        self.screen.blit(scaled_surface, (0, offset_y))

        if self.inventory_open:
            self.draw_inventory()

    def draw_game_over(self):
        self.screen.fill((0, 0, 0))

        text = self.font_big.render("GAME OVER", True, (255, 0, 0))
        restart = self.font.render("Press R to restart", True, (255, 255, 255))

        text_rect = text.get_rect(center=(asetukset.SCREEN_WIDTH // 2, asetukset.SCREEN_HEIGHT // 2 - 30))
        restart_rect = restart.get_rect(center=(asetukset.SCREEN_WIDTH // 2, asetukset.SCREEN_HEIGHT // 2 + 20))

        self.screen.blit(text, text_rect)
        self.screen.blit(restart, restart_rect)


    def draw_inventory(self):
        overlay = pygame.Surface((500, 400))
        overlay.set_alpha(220)
        overlay.fill((30, 30, 30))

        x = asetukset.SCREEN_WIDTH // 2 - 250
        y = asetukset.SCREEN_HEIGHT // 2 - 200

        self.screen.blit(overlay, (x, y))

        title = self.font_big.render("INVENTORY", True, (255, 255, 255))
        self.screen.blit(title, (x + 120, y + 20))

        for i, weapon in enumerate(self.player.inventory):
            item_text = self.font.render(
                f"{i + 1}. {weapon.name}",
                True,
                (255, 255, 255)
            )
            self.screen.blit(item_text, (x + 40, y + 100 + i * 40))

    def add_message(self, text):
        self.messages.append(text)

        if len(self.messages) > 5:
            self.messages.pop(0)

        self.message_timer = 180

    def draw_message_box(self):

        if not self.messages or self.message_timer <= 0:
            return

        box_width = 500
        box_height = 80

        x = asetukset.RENDER_WIDTH // 2 - box_width // 2
        y = asetukset.RENDER_HEIGHT - 100

        pygame.draw.rect(
            self.game_surface,
            (20, 20, 20),
            (x, y, box_width, box_height)
        )

        pygame.draw.rect(
            self.game_surface,
            (200, 200, 200),
            (x, y, box_width, box_height),
            2
        )

        text = self.font.render(self.messages[-1], True, (255, 255, 255))
        self.game_surface.blit(text, (x + 20, y + 25))

    def apply_save(self, data):

        self.player.hp = data["player"]["hp"]

        self.player.rect.x = data["player"]["x"]
        self.player.rect.y = data["player"]["y"]

        self.player.current_weapon_index = data["player"]["current_weapon_index"]

        self.current_floor = data["floor"]

        # -------------------------
        # LOAD INVENTORY
        # -------------------------
        self.player.inventory = []

        for weapon_name in data["player"].get("inventory", []):
            weapon = WeaponFactory.create(weapon_name)
            self.player.inventory.append(weapon)

        # -------------------------
        # LOAD PICKUPS
        # -------------------------
        self.pickups = []

        for pickup_data in data.get("pickups", []):
            weapon = WeaponFactory.create(pickup_data["weapon"])

            self.pickups.append(
                WeaponPickup(
                    pickup_data["x"],
                    pickup_data["y"],
                    weapon,
                    weapon.image
                )
            )
        # -------------------------
        # LOAD ENEMIES
        # -------------------------
        self.enemies = []

        for enemy_data in data.get("enemies", []):
            enemy = Enemy(
                self,
                enemy_data["x"],
                enemy_data["y"]
            )

            enemy.hp = enemy_data["hp"]

            self.enemies.append(enemy)

        print("Inventory after load:", [w.name for w in self.player.inventory])
        print("Save loaded.")

    def load_game(self):
        save_data = SaveManager.load()

        if save_data:
            self.apply_save(save_data)
            print("Game loaded from Continue")
        else:
            print("No save found")

    def load_map(self, map_name):

        self.collision_rects = []

        base_path = os.path.dirname(os.path.dirname(__file__))
        map_path = os.path.join(base_path, "maps", map_name)

        self.map = load_pygame(map_path)

        self.map_width = self.map.width * self.map.tilewidth
        self.map_height = self.map.height * self.map.tileheight

        self.player_spawn = (100, 100)
        self.exit_rect = None
        self.enemy_spawns = []

        # Käy kaikki object layerit läpi
        for layer in self.map.objectgroups:

            # COLLISIONS layer
            if layer.name == "Collisions":
                for obj in layer:
                    self.collision_rects.append(
                        pygame.Rect(
                            obj.x,
                            obj.y,
                            obj.width,
                            obj.height
                        )
                    )

            # MUUT objectit (spawnit jne.)
            else:
                for obj in layer:

                    if obj.name == "PlayerSpawn":
                        self.player_spawn = (obj.x, obj.y)

                    elif obj.name == "Exit":
                        self.exit_rect = pygame.Rect(
                            obj.x,
                            obj.y,
                            obj.width,
                            obj.height
                        )

                    elif obj.name == "EnemySpawn":
                        self.enemy_spawns.append((obj.x, obj.y))

    def next_floor(self):

        self.current_floor += 1

        if self.current_floor >= len(self.floor_maps):
            print("No more floors!")
            return

        self.load_map(self.floor_maps[self.current_floor])

        self.player.rect.x = self.player_spawn[0]
        self.player.rect.y = self.player_spawn[1]

        self.enemies = [
            Enemy(self, x, y)
            for x, y in self.enemy_spawns
        ]

        print(f"Loaded floor: {self.floor_maps[self.current_floor]}")

