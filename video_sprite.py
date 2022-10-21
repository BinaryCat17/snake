import pygame
import moviepy
from game import Game

import moviepy.editor
import moviepy.video.fx.all
import pygame

class VideoSprite(pygame.sprite.Sprite):
    def __init__(self, rect, filename, colorkey = None):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((rect.width, rect.height), pygame.HWSURFACE)
        self.colorkey = colorkey
        self.rect = self.surf.get_rect()
        self.rect.x = rect.x
        self.rect.y = rect.y
        self.video = moviepy.editor.VideoFileClip(filename).resize((self.rect.width, self.rect.height))
        self.current_frame = 0

    def next_frame(self):
        raw_image = self.video.get_frame(self.current_frame)
        self.surf = pygame.image.frombuffer(raw_image, (self.rect.width, self.rect.height), 'RGB').convert()
        if self.colorkey != None:
            self.surf.set_colorkey(self.colorkey)

        self.current_frame += 1 / self.video.fps 
        if(self.current_frame >= self.video.duration):
            self.current_frame = 0
        