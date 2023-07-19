import pygame, random
from data import *

class Particle(pygame.sprite.Sprite):
    def __init__(self, origin, size=[2, 2], color=(255, 255, 0), velocityRange=0.25, duration=1, destination=None,):
        super().__init__()
        self.image = pygame.Surface(size)
        pygame.Surface.fill(self.image, color)
        self.rect = self.image.get_rect()
        self.pos = [origin[0], origin[1]]
        if destination:
            pass
        else:
            self.velocity = [random.randrange(-1, 2, 2)*random.random()*velocityRange, random.randrange(-1, 2, 2)*random.random()*velocityRange]
        self.startTime = pygame.time.get_ticks()
        self.duration = duration

    def update(self):
        if pygame.time.get_ticks() - self.startTime > self.duration*1000:
            self.kill()
            del self
            return

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.x, self.rect.y = self.pos

    def draw(self):
        gamevars['display'].blit(self.image, (self.rect.x, self.rect.y))