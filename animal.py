import random
import pygame
import config as cfg
import util as u
from game import Game


class Animal(pygame.sprite.Sprite):
    animals = u.list_files('assets/animals')

    def __init__(self, pos) -> None:
        super(Animal, self).__init__()
        self.img = random.choice(Animal.animals)
        self.surf = Game.load_img(self.img, 0, (cfg.BLOCK_SIZE, cfg.BLOCK_SIZE))
        self.rect = self.surf.get_rect(center=pos)

    def update(self):
        pass
