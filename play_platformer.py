import pygame
from animal import Animal
from config import BLOCK_SIZE
import snake as s
import terrain as t
import config as cfg
import animal as a
import util as u
import random
from game import Game
from video_sprite import VideoSprite

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT
)

class PlatformerGame(Game):
    def init(self):
        pygame.mixer.init()
        pygame.mixer.music.load('assets/phonk.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self.haha = [
            pygame.mixer.Sound('assets/haha1.mp3'),
            pygame.mixer.Sound('assets/haha2.mp3'),
            pygame.mixer.Sound('assets/haha3.mp3'),
            pygame.mixer.Sound('assets/haha4.mp3'),
        ] 

        self.snake_pos = [7, 10]
        self.snakeKilled = False
        self.snake = s.Snake((BLOCK_SIZE * self.snake_pos[0] + BLOCK_SIZE / 2 + BLOCK_SIZE, cfg.SCREEN_HEIGHT - BLOCK_SIZE * self.snake_pos[1] + BLOCK_SIZE / 2), K_RIGHT, platformer=True)
        self.fall_animals = pygame.sprite.Group()
        self.terrain = t.Terrain()
        self.livsi_pos = 0
        self.video = VideoSprite(pygame.Rect(0, 0, cfg.BLOCK_SIZE, cfg.BLOCK_SIZE * 3), 'assets/livsi.mp4', colorkey=(0,0,0))
        Game.all_sprites.add(self.video)
        self.video_end = VideoSprite(pygame.Rect(0, 0, cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT), 'assets/end.mp4')
        self.video_finish = VideoSprite(pygame.Rect(0, 0, cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT), 'assets/livsi.mp4')

    def setup_events(self):
        self.GAME_TICK = pygame.USEREVENT + 1
        pygame.time.set_timer(self.GAME_TICK, cfg.TICK_RATE)

        self.VIDEO_TICK = pygame.USEREVENT + 2
        pygame.time.set_timer(self.VIDEO_TICK, int(1000 / 30))

        self.SPAWN_ANIMAL = pygame.USEREVENT + 3
        pygame.time.set_timer(self.SPAWN_ANIMAL, 3000)
        
    def random_animal_position(self, animal):
        width = random.randint(self.snake.head.rect.centerx - (len(self.snake.tail) - 1) * BLOCK_SIZE, self.snake.head.rect.centerx)
        height = cfg.BLOCK_SIZE
        animal.rect.center = (u.roundup(width, cfg.BLOCK_SIZE) - cfg.BLOCK_SIZE / 2, u.roundup(height, cfg.BLOCK_SIZE))

    def process_event(self, event):
        if event.type == self.GAME_TICK:
            if(self.snakeKilled or not self.snake.isAlive):
                return True

            down_block = self.terrain.block((self.snake_pos[0], self.snake_pos[1] - 1))
            old_pos = self.snake_pos[1]
            if(down_block == None):
                self.snake_pos[1] -= 1
            
            next_block = self.terrain.block((self.snake_pos[0] + 1, self.snake_pos[1]))
            while(next_block != None):
                self.snake_pos[1] += 1
                next_block = self.terrain.block((self.snake_pos[0] + 1, self.snake_pos[1]))
            
            dif = self.snake_pos[1] - old_pos
            if (dif > 0):
                if(self.pressed_keys[K_UP]):
                    for _ in range(dif):
                        self.snake.tick(K_UP, offset=(0, 0))
                else:
                    self.snakeKilled = True
                    pygame.mixer.music.load('assets/kill.mp3')
                    pygame.mixer.music.play(-1)
                    Game.all_sprites.add(self.video_end)

            if (dif < 0):
                for _ in range(abs(dif)):
                    self.snake.tick(K_DOWN, offset=(0, 0))

            down_block = self.terrain.block((self.snake_pos[0], self.snake_pos[1] - 1))

            if(type(down_block) == Animal and self.pressed_keys[K_DOWN]):
                self.snake.eat(down_block, K_DOWN)
                self.haha[random.randint(0, 3)].play(1, 1000)
                self.terrain.remove((self.snake_pos[0], self.snake_pos[1] - 1))
                self.snake.tick(K_DOWN, offset=(0, 0))
                self.snake_pos[1] -= 1
                next_block = self.terrain.block((self.snake_pos[0] + 1, self.snake_pos[1]))
                if(next_block != None):
                    pygame.mixer.music.load('assets/kill.mp3')
                    pygame.mixer.music.play(-1)
                    self.snakeKilled = True

                self.snake.tick(K_RIGHT, offset=(0, 0))
                self.snake_pos[0] += 1
            else:
                self.snake.tick(K_RIGHT, offset=(-BLOCK_SIZE, 0))
                self.terrain.tick()
            
            if self.pressed_keys[K_LEFT]:
                if self.livsi_pos < len(self.snake.tail) - 1:
                    self.livsi_pos += 1

            if self.pressed_keys[K_RIGHT]:
                if self.livsi_pos > 0:
                    self.livsi_pos -= 1
            
            for animal in self.fall_animals:
                animal.rect.centery += cfg.BLOCK_SIZE
                if(animal.rect.centery > cfg.SCREEN_HEIGHT):
                    animal.kill()
                else:
                    if(self.video.rect.colliderect(animal.rect)):
                        self.haha[random.randint(0, 3)].play(1, 1000)
                        self.snake.eat(animal, K_RIGHT)
                        self.snake.tick(K_RIGHT, offset=(0, 0))
                        self.snake_pos[0] += 1
                        break
            
            self.video.rect.bottomleft = (self.snake.tail[self.livsi_pos].rect.topleft[0], self.snake.tail[self.livsi_pos].rect.topleft[1])
        elif event.type == self.VIDEO_TICK:
            self.video.next_frame()
            if not self.snake.isAlive:
                Game.all_sprites.add(self.video_finish)
                self.video_finish.next_frame()
                return True
            if self.snakeKilled:
                self.video_end.next_frame()
                return True
        elif event.type == self.SPAWN_ANIMAL:
            if(self.snakeKilled or not self.snake.isAlive):
                return True
            animal = a.Animal((0, 0))
            self.random_animal_position(animal)
            self.all_sprites.add(animal)
            self.fall_animals.add(animal)

        return True

    def update(self):
        if not self.snakeKilled:
            if not self.snake.isAlive:
                self.video_finish.update()
                return True

            self.video.update()
            self.pressed_keys = pygame.key.get_pressed()
            return self.snake.update()
        else:
            self.video_end.update()
            return True

PlatformerGame().run()