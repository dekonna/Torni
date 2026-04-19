import json

class SaveManager:

    SAVE_FILE = "savegame.json"

    @staticmethod
    def save(game):
        data = {
            "player": {
                "hp": game.player.hp,
                "x": game.player.rect.x,
                "y": game.player.rect.y,
                "current_weapon_index": game.player.current_weapon_index,
                "inventory": [
                    weapon.name for weapon in game.player.inventory
                ]
            },

            "floor": game.current_floor,

            "pickups": [
                {
                    "weapon": pickup.weapon.name,
                    "x": pickup.rect.x,
                    "y": pickup.rect.y
                }
                for pickup in game.pickups
            ],

            "enemies": [
                {
                    "x": enemy.rect.x,
                    "y": enemy.rect.y,
                    "hp": enemy.hp
                }
                for enemy in game.enemies
            ]
        }

        with open(SaveManager.SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)

        print("Game saved.")

    @staticmethod
    def load():
        try:
            with open(SaveManager.SAVE_FILE, "r") as f:
                return json.load(f)

        except FileNotFoundError:
            return None