import pygame

from src import asetukset

from src.UI.menu import Menu
from src.UI.character_creation import CharacterCreation

from src.entities.player import Player
from src.entities.enemies.skeleton import Skeleton
from src.entities.enemies.zombie_basic import ZombieBase
from src.entities.pickup import WeaponPickup

from src.save_manager import SaveManager

from src.systems.weapon_factory import WeaponFactory
from src.systems.camera import Camera
from src.systems.world_logic import WorldSystem
from src.systems.ui_system import UISystem
from src.systems.render_system import RenderSystem
from src.systems.input_system import InputSystem
from src.systems.update_system import UpdateSystem

# =========================================================
# GAME CLASS
# =========================================================

class Game:

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self):

        pygame.init()

        self.asetukset = asetukset

        self.font = pygame.font.Font(None, 30)
        self.font_big = pygame.font.Font(None, 80)

        # =================================================
        # DISPLAY
        # =================================================

        self.screen = pygame.display.set_mode(
            (asetukset.SCREEN_WIDTH, asetukset.SCREEN_HEIGHT)
        )

        pygame.display.set_caption(asetukset.TITLE)

        # =================================================
        # GAME SURFACE
        # =================================================

        self.game_surface = pygame.Surface(
            (asetukset.RENDER_WIDTH, asetukset.RENDER_HEIGHT)
        )

        # =================================================
        # CLOCK
        # =================================================

        self.clock = pygame.time.Clock()

        # =================================================
        # GAME STATE
        # =================================================

        self.running = True
        self.state = "MENU"

        # =================================================
        # UI
        # =================================================

        self.menu = Menu(self.screen)

        self.character_creation = CharacterCreation(
            self.screen
        )

        self.inventory_open = False

        self.debug_mode = False

        # =================================================
        # MAPS
        # =================================================

        self.floor_maps = [
            "Testi_Map.tmx",
            "Testi_Map.tmx",
            "Testi_Map.tmx"
        ]

        self.current_floor = 0

        WorldSystem.load_map(
            self,
            self.floor_maps[self.current_floor]
        )

        # =================================================
        # MESSAGE SYSTEM
        # =================================================

        self.messages = []
        self.message_timer = 0

        # =================================================
        # GAME RESET
        # =================================================

        self.reset_game()

        # =================================================
        # CAMERA
        # =================================================

        self.camera = Camera(
            self.map.width * self.map.tilewidth,
            self.map.height * self.map.tileheight
        )

    # =====================================================
    # RESET GAME
    # =====================================================

    def reset_game(self):

        # =================================================
        # PLAYER
        # =================================================

        self.player = Player(
            self,
            self.player_spawn[0],
            self.player_spawn[1]
        )

        # =================================================
        # ENEMIES
        # =================================================

        self.enemies = []

        for x, y in self.enemy_spawns:

            self.enemies.append(
                Skeleton(self, x, y)
            )

            self.enemies.append(
                ZombieBase(self, x + 80, y)
            )

        # =================================================
        # WEAPONS
        # =================================================

        bat_weapon = WeaponFactory.create("Bat")
        pistol = WeaponFactory.create("Pistol")

        # =================================================
        # PICKUPS
        # =================================================

        self.pickups = [
            WeaponPickup(300, 300, bat_weapon, bat_weapon.image),
            WeaponPickup(400, 300, pistol, None),
        ]

        # =================================================
        # BODY PARTS
        # =================================================

        self.body_parts = []

        self.blood_particles = []

        self.blood_decals = []

    # =====================================================
    # GAME LOOP
    # =====================================================

    def run(self):

        print("Game loop started")

        while self.running:

            self.handle_events()

            # =================================================
            # GAME
            # =================================================

            if self.state == "GAME":

                if not self.inventory_open:
                    self.update()

                self.draw_game()

            # =================================================
            # GAME OVER
            # =================================================

            elif self.state == "GAME_OVER":

                UISystem.draw_game_over(self)

            # =================================================
            # MENU
            # =================================================

            elif self.state == "MENU":

                self.screen.fill((0, 0, 0))
                self.menu.draw()

            # =================================================
            # CHARACTER CREATION
            # =================================================

            elif self.state == "CHARACTER":

                self.screen.fill((0, 0, 0))
                self.character_creation.draw()

            pygame.display.flip()

            self.clock.tick(asetukset.FPS)

        pygame.quit()

    # =====================================================
    # EVENT HANDLING
    # =====================================================

    def handle_events(self):

        for event in pygame.event.get():

            # =================================================
            # QUIT
            # =================================================

            if event.type == pygame.QUIT:
                self.running = False

            # =================================================
            # GLOBAL INPUT
            # =================================================

            InputSystem.handle_global_input(
                self,
                event
            )

            # =================================================
            # MENU INPUT
            # =================================================

            if self.state == "MENU":

                InputSystem.handle_menu_input(
                    self,
                    event
                )

            # =================================================
            # GAME INPUT
            # =================================================

            elif self.state == "GAME":

                InputSystem.handle_game_input(
                    self,
                    event
                )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self):

        if self.state == "GAME":

            # =================================================
            # UPDATE PIPELINE
            # =================================================

            UpdateSystem.update(self)

    # =====================================================
    # GAME RENDERING
    # =====================================================

    def draw_game(self):

        # =================================================
        # BACKGROUND
        # =================================================

        self.game_surface.fill(
            asetukset.BACKGROUND_COLOR
        )

        # =================================================
        # RENDER PIPELINE
        # =================================================

        RenderSystem.draw(self)

        # =================================================
        # UI PIPELINE
        # =================================================

        UISystem.draw(self)

    # =====================================================
    # MESSAGE SYSTEM
    # =====================================================

    def add_message(self, text):

        self.messages.append(text)

        if len(self.messages) > asetukset.MAX_MESSAGES:
            self.messages.pop(0)

        self.message_timer = asetukset.MESSAGE_DURATION

    # =====================================================
    # APPLY SAVE DATA
    # =====================================================

    def apply_save(self, data):

        # =================================================
        # PLAYER DATA
        # =================================================

        self.player.hp = data["player"]["hp"]

        self.player.rect.x = data["player"]["x"]
        self.player.rect.y = data["player"]["y"]

        self.player.current_weapon_index = (
            data["player"]["current_weapon_index"]
        )

        # =================================================
        # FLOOR
        # =================================================

        self.current_floor = data["floor"]

        # =================================================
        # LOAD INVENTORY
        # =================================================

        self.player.inventory = []

        for weapon_name in data["player"].get(
            "inventory",
            []
        ):

            weapon = WeaponFactory.create(weapon_name)

            self.player.inventory.append(weapon)

        # =================================================
        # LOAD PICKUPS
        # =================================================

        self.pickups = []

        for pickup_data in data.get("pickups", []):

            weapon = WeaponFactory.create(
                pickup_data["weapon"]
            )

            self.pickups.append(

                WeaponPickup(
                    pickup_data["x"],
                    pickup_data["y"],
                    weapon,
                    weapon.image
                )
            )

        # =================================================
        # LOAD ENEMIES
        # =================================================

        self.enemies = []

        for enemy_data in data.get("enemies", []):

            enemy = Skeleton(
                self,
                enemy_data["x"],
                enemy_data["y"]
            )

            enemy.hp = enemy_data["hp"]

            self.enemies.append(enemy)

        print(
            "Inventory after load:",
            [w.name for w in self.player.inventory]
        )

        print("Save loaded.")

    # =====================================================
    # LOAD GAME
    # =====================================================

    def load_game(self):

        save_data = SaveManager.load()

        if save_data:

            self.apply_save(save_data)

            print("Game loaded from Continue")

        else:

            print("No save found")