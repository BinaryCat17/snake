import pygame
import snake as s
import animal as a
from game import Game


class SnakeGame(Game):
    def init(self):
        self.snake = s.Snake()

    def setup_events(self):
        self.GAME_TICK = pygame.USEREVENT + 1
        pygame.time.set_timer(self.GAME_TICK, 150)
        
        self.SPAWN_ANIMAL = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SPAWN_ANIMAL, 1000)

    def process_event(self, event):
        if event.type == self.GAME_TICK:
            self.snake.tick()
        elif event.type == self.SPAWN_ANIMAL:
            self.all_sprites.add(a.Animal(self.all_sprites))
        return True

    def update(self):
        return self.snake.update()

SnakeGame().run()