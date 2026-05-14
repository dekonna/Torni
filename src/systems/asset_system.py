import pygame

class AssetManager:

    # =========================================================
    # CACHE
    # =========================================================

    images = {}

    # =========================================================
    # LOAD IMAGE
    # =========================================================

    @classmethod
    def load_image(cls, path):

        # jos kuvaa ei ole vielä ladattu
        if path not in cls.images:

            cls.images[path] = pygame.image.load(path).convert_alpha()

            print(f"Loaded image: {path}")

        return cls.images[path]