from random import random
from re import I
from timeit import repeat
import pygame
import config as cfg
import random
import noise
import animal as a
from game import Game

class Block(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super(Block, self).__init__()
        self.surf = Game.load_img(image_path, 0, (cfg.BLOCK_SIZE, cfg.BLOCK_SIZE))
        self.rect = self.surf.get_rect()

class Chunk(pygame.sprite.Sprite):
    def __init__(self):
        super(Chunk, self).__init__()
        self.surf = pygame.Surface((cfg.CHUNK_SIZE * cfg.BLOCK_SIZE, cfg.CHUNK_SIZE * cfg.BLOCK_SIZE), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()
        Game.all_sprites.add(self)
        self.chunk_data = {}

        for x_pos in range(cfg.CHUNK_SIZE):
            high = 0
            for y_pos in range(cfg.CHUNK_SIZE):
                block_x = x_pos
                block_y = y_pos
                block_type = ''
                height = int(noise.pnoise1(x_pos * 0.05 * random.random(), repeat=9999999) * 4)
                if block_y <= 3 + height:
                    block_type = Block('assets/minecraft/dirt.webp')
                    self.chunk_data[(block_x, block_y)] = block_type
                    high = block_y
                else:
                    if random.randint(1, 5) == 1 and block_x > 0 and (block_x - 1, block_y) not in self.chunk_data:
                        self.chunk_data[(block_x, block_y)] = a.Animal((0, 0))
                        self.chunk_data[(block_x-1, block_y)] = Block('assets/minecraft/sword.png')
                    break

            self.chunk_data[(x_pos, high)] = Block('assets/minecraft/grass.webp')
                    

    def draw(self, pos):
        self.rect.topleft = pos
        self.surf.fill((0, 0, 0, 0))
        for k, v in self.chunk_data.items():
            self.surf.blit(v.surf, (k[0] * cfg.BLOCK_SIZE, cfg.CHUNK_SIZE * cfg.BLOCK_SIZE - k[1] * cfg.BLOCK_SIZE))



class Terrain:
    def __init__(self):
        self.chunks = []
        for i in range(cfg.CHUNKS_ON_SCREEN + 1):
            self.chunks.append([Chunk(), i * cfg.CHUNK_SIZE])
    

    def block(self, pos):
        for chunk in self.chunks:
            if (pos[0] - chunk[1], pos[1]) in chunk[0].chunk_data:
                return chunk[0].chunk_data[(pos[0] - chunk[1], pos[1])]
        return None

    def remove(self, pos):
        for chunk in self.chunks:
            if (pos[0] - chunk[1], pos[1]) in chunk[0].chunk_data:
                chunk[0].chunk_data[(pos[0] - chunk[1], pos[1])].kill()
                del chunk[0].chunk_data[(pos[0] - chunk[1], pos[1])]
        return None



   
    def tick(self):
        # если первый чанк полностью скрылся с экрана
        if self.chunks[0][1] <= -cfg.CHUNK_SIZE:
            self.chunks[0][0].kill()
            self.chunks = self.chunks[1:]
            self.chunks.append([Chunk(), cfg.CHUNKS_ON_SCREEN * cfg.CHUNK_SIZE])

        for chunk in self.chunks:
            chunk[0].draw((chunk[1] * cfg.BLOCK_SIZE, cfg.SCREEN_HEIGHT - cfg.CHUNK_SIZE * cfg.BLOCK_SIZE))
            chunk[1] -= 1
