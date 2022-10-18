import random
import pygame
import util as u
import config as cfg
from game import Game


class Animal(pygame.sprite.Sprite):
    animals = u.list_files('assets/animals')

    def __init__(self, sprites) -> None:
        super(Animal, self).__init__()
        self.img = random.choice(Animal.animals)

        self.surf = pygame.image.load(self.img)
        self.surf = pygame.transform.scale(self.surf, (cfg.BLOCK_SIZE, cfg.BLOCK_SIZE))
        self.surf.set_colorkey((0, 0, 0))

        self.random_position()
        while pygame.sprite.spritecollideany(self, sprites):
            self.random_position()

    def random_position(self):
        self.rect = self.surf.get_rect(
            center=(u.roundup(random.randint(Game.game_field.left + cfg.BLOCK_SIZE, Game.game_field.width - cfg.BLOCK_SIZE), cfg.BLOCK_SIZE),
                    u.roundup(random.randint(Game.game_field.top + cfg.BLOCK_SIZE, Game.game_field.height - cfg.BLOCK_SIZE), cfg.BLOCK_SIZE))

        )

    def update(self):
        pass
