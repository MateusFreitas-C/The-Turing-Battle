import pygame

class HealthBar():
    def __init__(self, surface, x, y, hp, max_hp):
        self.surface = surface
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp
        ratio = self.hp / self.max_hp

        pygame.draw.rect(self.surface, (255, 0 ,0), (self.x, self.y, 120, 15))
        pygame.draw.rect(self.surface, (255, 255, 0), (self.x, self.y, 120 * ratio, 15))