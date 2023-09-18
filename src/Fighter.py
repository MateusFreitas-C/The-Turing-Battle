import pygame
import random
from src.DamageText import DamageText

class Fighter:
    def __init__(self, surface, x, y, name, max_hp, strength):
        self.surface = surface
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.alive = True
        self.damage_text_group = pygame.sprite.Group()

        self.animation_list = []
        self.frame_index = 0
        self.action = 0 #0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()

        temp_list = []

        for i in range(8):
            img = pygame.image.load(f"img/{self.name}/Idle/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)

        self.animation_list.append(temp_list)

        temp_list = []

        for i in range(8):
            img = pygame.image.load(f"img/{self.name}/Attack/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)

        self.animation_list.append(temp_list)

        temp_list = []

        for i in range(3):
            img = pygame.image.load(f"img/{self.name}/Hurt/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)

        self.animation_list.append(temp_list)

        temp_list = []

        for i in range(10):
            img = pygame.image.load(f"img/{self.name}/Death/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)

        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def update(self):
        animation_cooldown = 100
        #handle animation
        self.image = self.animation_list[self.action][self.frame_index]

        if(pygame.time.get_ticks() - self.update_time > animation_cooldown):
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
        if(self.frame_index >= len(self.animation_list[self.action])):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()
    
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        #deal damage to enemy
        target.hp -= self.strength
        target.hurt()
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()

        damage_text = DamageText(target.rect.centerx, target.rect.y, str(self.strength), (255, 0 ,0))
        self.damage_text_group.add(damage_text)

        #variables to attack
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.hp = self.max_hp
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()