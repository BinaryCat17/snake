import pygame
from animal import Animal
import config as cfg
from game import Game

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

def blit_body_transparent(dst, src):
        w, h = src.get_size()
        for x in range(w):
            for y in range(h):
                (r1, g1, b1, a1) = src.get_at((x, y))
                (r2, g2, b2, a2) = dst.get_at((x, y))

                if (r2 or g2 or b2):
                    new_alpha = 200 * a1 // 256
                    a = 0.8
                    def w (v1, v2):
                        return int((1 - a) * v1 + a * v2)
                    dst.set_at((x, y), pygame.Color(w(r1, r2), w(g1, g2), w(b1, b2), new_alpha))
                else:
                        dst.set_at((x, y), pygame.Color(r1, g1, b1, a1))

class SnakeBlock(pygame.sprite.Sprite):
    def __init__(self, animal_img, pos, dir):
        super(SnakeBlock, self).__init__()
        self.animal_img = animal_img
        self.last_dir = dir

        self.surf = pygame.Surface((cfg.BLOCK_SIZE, cfg.BLOCK_SIZE), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center = pos)
        self.rotateAnimal(pos, dir)
    
    def clean(self):
        self.surf.fill((0, 0, 0, 0))


    def move(self, dir):

        if dir is None:
            dir = self.last_dir

        if dir == K_UP:
            return self.rect.move(0, -cfg.BLOCK_SIZE)
        elif dir == K_DOWN:
            return self.rect.move(0, cfg.BLOCK_SIZE)
        elif dir == K_LEFT:
            return self.rect.move(-cfg.BLOCK_SIZE, 0)
        elif dir == K_RIGHT:
            return self.rect.move(cfg.BLOCK_SIZE, 0)

    def rotateAnimal(self, pos, dir):
        if dir is None:
            dir = self.last_dir

        self.rect = self.surf.get_rect(center = pos)

        if dir == K_UP:
            rot = 180
        elif dir == K_DOWN:
            rot = 0
        elif dir == K_LEFT:
            rot = -90
        elif dir == K_RIGHT:
            rot = 90

        animal = Game.load_img(self.animal_img, rot, (cfg.BLOCK_SIZE, cfg.BLOCK_SIZE))
        self.surf.blit(animal, (0, 0))
        
        self.last_dir = dir
    
    
    def rotateBody(self, fromDir, toDir, tail = False):
        rot = 0
        img = ''

        if fromDir != toDir:
            img = 'assets/snake/angle.png'
            if fromDir == K_UP and toDir == K_LEFT:
                rot = -90
            elif fromDir == K_UP and toDir == K_RIGHT:
                rot = 0
            elif fromDir == K_DOWN and toDir == K_RIGHT:
                rot = 90
            elif fromDir == K_DOWN and toDir == K_LEFT:
                rot = 180
            elif fromDir == K_RIGHT and toDir == K_UP:
                rot = 180
            elif fromDir == K_RIGHT and toDir == K_DOWN:
                rot = -90
            elif fromDir == K_LEFT and toDir == K_UP:
                rot = 90
            elif fromDir == K_LEFT and toDir == K_DOWN:
                rot = 0
           
        else:
            if tail:
                img = 'assets/snake/tail.png'
                if toDir == K_DOWN:
                    rot = 0
                elif toDir == K_RIGHT:
                    rot = 90
                elif toDir == K_UP:
                    rot = 180
                elif toDir == K_LEFT:
                    rot = -90
            else:
                img = 'assets/snake/body.png'
                if toDir == K_UP or toDir == K_DOWN:
                    rot = 90
                else:
                    rot = 0

           
        body = Game.load_img(img, rot)
        blit_body_transparent(self.surf, body)
        w, h = self.surf.get_size()
 

class Snake():
    def __init__(self) -> None:
        self.isAlive = False
        self.last_keys = []

        self.head = SnakeBlock('assets/snake/head.png', (cfg.BLOCK_SIZE, cfg.BLOCK_SIZE), K_DOWN)
        self.tail = [self.head]

        Game.all_sprites.add(self.tail)
        self.isAlive = True

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if (pressed_keys[K_UP] or pressed_keys[K_DOWN] or pressed_keys[K_LEFT] or pressed_keys[K_RIGHT]):
            self.last_keys = pressed_keys
        return self.isAlive
    
    def move_dir(self):
        if len(self.last_keys) == 0:
            return None
        elif self.last_keys[K_UP]:
            if(self.head.last_dir == K_DOWN):
                return None
            return K_UP
        elif self.last_keys[K_DOWN]:
            if(self.head.last_dir == K_UP):
                return None
            return K_DOWN
        elif self.last_keys[K_LEFT]:
            if(self.head.last_dir == K_RIGHT):
                return None
            return K_LEFT
        elif self.last_keys[K_RIGHT]:
            if(self.head.last_dir == K_LEFT):
                return None
            return K_RIGHT

    def tick(self):
        if Game.out_of_field(self.tail[0].rect):
            self.isAlive = False

        next_dir = self.move_dir()

        next_pos = self.head.move(next_dir)

        blocks = [s for s in Game.all_sprites if type(s) == SnakeBlock and s != self.head]
        block = next_pos.collidelist(blocks)

        if(block != -1):
            self.isAlive = False
            return

        animals = [s for s in Game.all_sprites if type(s) == Animal]
        animal = next_pos.collidelist(animals)

        if animal != -1:
            animal = animals[animal]
            animal.kill()
            
            self.tail.append(SnakeBlock(animal.img, self.head.rect.center, next_dir))
            Game.all_sprites.add(self.tail[-1])

        for i in range(len(self.tail) - 1, 0, -1):
                self.tail[i].clean()
                self.tail[i].rect = self.tail[i - 1].rect
                self.tail[i].rotateAnimal(self.tail[i - 1].rect.center, self.tail[i - 1].last_dir)
 
        self.head.clean()
        self.head.rotateAnimal(next_pos.center, next_dir)

        for i in range(len(self.tail) - 1, 0, -1):
            self.tail[i].rotateBody(self.tail[i].last_dir, self.tail[i - 1].last_dir)

        if(len(self.tail) > 1):
            self.tail[-1].rotateBody(self.tail[-2].last_dir, self.tail[-2].last_dir, True)

