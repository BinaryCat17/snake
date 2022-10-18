import pygame
import config as cfg

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
    
class Game:
    game_field = pygame.rect.Rect(0, 0, cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
    all_sprites = pygame.sprite.Group()
    all_images = {}

    def out_of_field(rect, field = game_field):
        return rect.left < field.left or rect.right > field.width or rect.top < field.top or rect.bottom > field.height

    def return_to_field(rect, field = game_field):
        if rect.left < field.left:
            rect.left = field.left
        if rect.right > field.width:
            rect.right = field.width
        if rect.top <= field.top:
            rect.top = field.top
        if rect.bottom >= field.height:
            rect.bottom = field.height

    def load_img(img, rot, size = (cfg.BLOCK_SIZE, cfg.BLOCK_SIZE)):
        if (img not in Game.all_images):
            Game.all_images[img] = pygame.image.load(img).convert_alpha()
            Game.all_images[img] = pygame.transform.scale(Game.all_images[img], size)

        return pygame.transform.rotate(Game.all_images[img], rot)
    

    def init(self):    
        pass

    def setup_events(self):
        pass

    def process_event(self, _):
        return True

    def update(self):
        return True
    
    def shutdwon(self):
        pass

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode([cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT])
    
        time = pygame.time.Clock()

        self.init()
        self.setup_events()
    
        running = True
        while running:
            time.tick(cfg.FPS)
    
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
    
                elif event.type == QUIT:
                    running = False
                
                else:
                    running = self.process_event(event)

            if not running:
                break

            for entity in Game.all_sprites:
                entity.update()
                    
            screen.fill(cfg.BACKGROUND_COLOR)

            running = self.update()

            for entity in Game.all_sprites:
                screen.blit(entity.surf, entity.rect)

            pygame.display.flip()
        
        pygame.quit()


