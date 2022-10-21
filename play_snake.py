import pygame
import snake as s
import animal as a
import config as cfg
import random
import util as u
from game import Game

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

class SnakeGame(Game):
    def init(self):
        self.snake = s.Snake((cfg.BLOCK_SIZE, cfg.BLOCK_SIZE))
        self.last_keys = []

    def setup_events(self):
        self.GAME_TICK = pygame.USEREVENT + 1
        pygame.time.set_timer(self.GAME_TICK, cfg.TICK_RATE)
        
        self.SPAWN_ANIMAL = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SPAWN_ANIMAL, 1000)

    def process_event(self, event):
        if event.type == self.GAME_TICK:
            self.snake.tick(self.move_dir())
        elif event.type == self.SPAWN_ANIMAL:
            animal = a.Animal((0, 0))
            self.random_animal_position(animal)
            while pygame.sprite.spritecollideany(animal, self.all_sprites):
                self.random_animal_position(animal)
            self.all_sprites.add(animal)
        return True

    def random_animal_position(self, animal):
        animal.rect.center = u.roundup(random.randint(Game.game_field.left + cfg.BLOCK_SIZE, Game.game_field.width - cfg.BLOCK_SIZE), cfg.BLOCK_SIZE), \
                    u.roundup(random.randint(Game.game_field.top + cfg.BLOCK_SIZE, Game.game_field.height - cfg.BLOCK_SIZE), cfg.BLOCK_SIZE)



    def move_dir(self):
        if len(self.last_keys) == 0:
            return None
        elif self.last_keys[K_UP]:
            if(self.snake.head.last_dir == K_DOWN):
                return None
            return K_UP
        elif self.last_keys[K_DOWN]:
            if(self.snake.head.last_dir == K_UP):
                return None
            return K_DOWN
        elif self.last_keys[K_LEFT]:
            if(self.snake.head.last_dir == K_RIGHT):
                return None
            return K_LEFT
        elif self.last_keys[K_RIGHT]:
            if(self.snake.head.last_dir == K_LEFT):
                return None
            return K_RIGHT

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if (pressed_keys[K_UP] or pressed_keys[K_DOWN] or pressed_keys[K_LEFT] or pressed_keys[K_RIGHT]):
            self.last_keys = pressed_keys
        return self.snake.update()


SnakeGame().run()