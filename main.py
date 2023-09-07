from typing import Any
import pygame
import random
from custom_button import Custom_Button
import time
from label import *
import pygame.gfxdraw

pygame.init()

clock = pygame.time.Clock()
fps = 60

#Game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("The Turing Battle")

#Define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 10
clicked = False
game_over = 0

questions = [
    ["Quem é conhecido como o 'pai da computação' e projetou a Máquina Analítica?", ["Alan Turing", "Charles Babbage", "John von Neumann", "Ada Lovelace"], "Charles Babbage"],
    ["Qual foi a contribuição mais significativa de Alan Turing para a computação?", ["Primeiro computador eletrônico", "Primeiro sistema operacional", "Teoria da Computabilidade", "Invenção do mouse"], "Teoria da Computabilidade"],
    ["Qual foi o primeiro sistema de programação de computador?", ["Fortran", "Cobol", "Machine Language", "Assembly Language"], "Machine Language"],
    ["Quem desenvolveu o primeiro compilador de alta linguagem, Fortran?", ["Alan Turing", "Grace Hopper", "John von Neumann", "Charles Babbage"], "Grace Hopper"],
    ["Quem escreveu o primeiro algoritmo destinado a ser processado por uma máquina?", ["Alan Turing", "Charles Babbage", "John von Neumann", "Ada Lovelace"], "Ada Lovelace"],
    ["Qual desses foi usado para quebrar o código Enigma durante a Segunda Guerra Mundial?", ["Colossus", "UNIVAC", "IBM 5100", "Apple I"], "Colossus"],
    ["Quem inventou o primeiro mouse e o dispositivo de apontamento para computadores?", ["Alan Turing", "Charles Babbage", "Douglas Engelbart", "John von Neumann"], "Douglas Engelbart"],
    ["Qual linguagem de programação foi desenvolvida por Dennis Ritchie na década de 1970?", ["Fortran", "Cobol", "C", "Pascal"], "C"],
    ["Qual foi o primeiro sistema operacional amplamente utilizado?", ["UNIX", "Windows", "Linux", "MS-DOS"], "UNIX"],
]


#Font
font = pygame.font.SysFont("Times New Roman", 26)

red = (255, 0 ,0)
green = (0, 255, 0)

#Load imagems
#Backgroud images

backgroud_img = pygame.image.load("img/Background/background.png").convert_alpha()
panel_img = pygame.image.load("img/Icons/panel.png").convert_alpha()
potion_img = pygame.image.load("img/Icons/potion.png").convert_alpha()
sword_img = pygame.image.load("img/Icons/sword.png").convert_alpha()
victory_img = pygame.image.load("img/Icons/victory.png").convert_alpha()
game_over_img = pygame.image.load("img/Icons/defeat.png").convert_alpha()
restart_img = pygame.image.load("img/Icons/restart.png").convert_alpha()



#Draw Text

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

#function for drawing backgroud

def Draw_Bg ():
    screen.blit(backgroud_img, (0,0))

def Draw_panel():
    screen.blit(panel_img, (0,screen_height - bottom_panel))



#Class

class Fighter:
    def __init__(self, x, y, name, max_hp, strength):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.alive = True

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
        screen.blit(self.image, self.rect)

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
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        target.hurt()
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()

        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)

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
    
class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp
        ratio = self.hp / self.max_hp

        pygame.draw.rect(screen, red, (self.x, self.y, 120, 15))
        pygame.draw.rect(screen, green, (self.x, self.y, 120 * ratio, 15))

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)

        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        #Delete the text
        self.counter += 1
        if self.counter > 30:
            self.kill()

buttons = pygame.sprite.Group()
class Button(pygame.sprite.Sprite):
    ''' A button treated like a Sprite... and killed too '''
    
    def __init__(self, position, text, size,
        colors="white on blue",
        hover_colors="red on green",
        style="button1",
        borderc=(255,255,255),
        command=lambda: print("No command activated for this button")):

        # the hover_colors attribute needs to be fixed
        super().__init__()
        global num

        self.text = text
        self.command = command
        # --- colors ---
        self.colors = colors
        self.original_colors = colors
        self.fg, self.bg = self.colors.split(" on ")
        # hover_colors
        if hover_colors == "red on green":
            self.hover_colors = f"{self.bg} on {self.fg}"
        else:
            self.hover_colors = hover_colors
        # styles can be button1 or button2 (more simple this one)
        self.style = style
        self.borderc = borderc # for the style2
        # font
        self.font = pygame.font.SysFont("Arial", size)
        self.render(self.text)
        self.x, self.y, self.w , self.h = self.text_render.get_rect()
        self.x, self.y = position
        self.rect = pygame.Rect(self.x, self.y, 200, self.h)
        self.position = position
        self.pressed = 1
        # the groups with all the buttons
        buttons.add(self)

    def render(self, text):
        # we have a surface
        self.text_render = self.font.render(text, 1, self.fg)
        # memorize the surface in the image attributes
        self.image = self.text_render

    def update(self):
        self.fg, self.bg = self.colors.split(" on ")
        if self.style == "button1":
            self.draw_button1()
        elif self.style == "button2":
            self.draw_button2()
        if self.command != None:
            self.hover()
            self.click()

    def draw_button1(self):
        ''' draws 4 lines around the button and the background '''
        # horizontal up
        lcolor = (150, 150, 150)
        lcolor2 = (50, 50, 50)
        pygame.draw.line(screen, lcolor, self.position,
            (self.x + self.w , self.y), 5)
        pygame.draw.line(screen, lcolor, (self.x, self.y - 2),
            (self.x, self.y + self.h), 5)
        # horizontal down
        pygame.draw.line(screen, lcolor2, (self.x, self.y + self.h),
            (self.x + self.w , self.y + self.h), 5)
        pygame.draw.line(screen, lcolor2, (self.x + self.w , self.y + self.h),
            [self.x + self.w , self.y], 5)
        # background of the button
        pygame.draw.rect(screen, self.bg, self.rect)  

    def draw_button2(self):
        ''' a linear border '''
        # the width is set to 500 to have the same size not depending on the text size
        pygame.draw.rect(screen, self.bg, (self.x - 50, self.y, 350 , self.h))
        pygame.gfxdraw.rectangle(screen, (self.x - 50, self.y, 350 , self.h), self.borderc)

    def check_collision(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # you can change the colors when the pointer is on the button if you want
            self.colors = self.hover_colors
            # pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            self.colors = self.original_colors
            # pygame.mouse.set_cursor(*pygame.cursors.arrow)


    def hover(self):
        ''' checks if the mouse is over the button and changes the color if it is true '''

        self.check_collision()

    def click(self):
        ''' checks if you click on the button and makes the call to the action just one time'''
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                print("The answer is:'" + self.text + "'")
                self.command()
                self.pressed = 0

            if pygame.mouse.get_pressed() == (0,0,0):
                self.pressed = 1



# ACTION FOR BUTTON CLICK ================

def on_click(clicked_answer):
    print("Click on one answer")

    # Verifique se a resposta clicada é igual à resposta correta da pergunta atual
    if clicked_answer == questions[qnum-1][2]:
        check_score("right")
    else:
        check_score()

def check_score(answered="wrong"):
    ''' here we check if the answer is right '''
    global qnum, points
    
    # until there are questions (before last)
    if qnum < len(questions):
        print(qnum, len(questions))
        if answered == "right":
            time.sleep(.1) # to avoid adding more point when pressing too much
            points += 1
            knight.attack(bandit1)
            # Show the score text
        else:
            bandit1.attack(knight)
        qnum += 1 # counter for next question in the list
        # Change the text of the question
        title.change_text(questions[qnum-1][0], color="white")
        # change the question number
        show_question(qnum) # delete old buttons and show new
        

    # for the last question...
    elif qnum == len(questions):
        print(qnum, len(questions))
        if answered == "right":
            knight.attack(bandit1)
            kill()
            time.sleep(.1)
            points +=1
        else:
            bandit1.attack(knight)
    time.sleep(.5)

def show_question(qnum):
    ''' put your buttons here '''

    # Kills the previous buttons/sprites
    kill()

    
    # The 4 position of the buttons
    pos = [screen_height-35, screen_height - 70, screen_height - 70, screen_height - 35]
    # randomized, so that the right one is not on top

    # ============== TEXT: question and answers ====================
    Button((60, pos[0]), questions[qnum-1][1][0], 20, "red on yellow",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=lambda: on_click(questions[qnum-1][1][0]))
    Button((460, pos[1]), questions[qnum-1][1][1], 20, "red on yellow",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=lambda: on_click(questions[qnum-1][1][1]))
    Button((60, pos[2]), questions[qnum-1][1][2], 20, "red on yellow",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=lambda: on_click(questions[qnum-1][1][2]))
    Button((460, pos[3]), questions[qnum-1][1][3], 20, "red on yellow",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=lambda: on_click(questions[qnum-1][1][3]))


def kill():
    for _ in buttons:
        _.kill()

points = 0
qnum = 1
title = Label(screen, questions[qnum-1][0], 40, screen_height - 140, 20, color="white")
restart_button = Custom_Button(screen, 330, 120, restart_img, 120, 30)

damage_text_group = pygame.sprite.Group()

knight = Fighter(200, 260, "Knight", 80, 10)
bandit1 = Fighter(550, 270, "Bandit", 50, 10)

bandit_list = []
bandit_list.append(bandit1)

knight_health_bar = HealthBar(140, 190, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(490, 190, bandit1.hp, bandit1.max_hp)

run = True
bool_question = True
while run:
    
    clock.tick(fps)

    #Drawning session
    Draw_Bg()
    Draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)

    knight.update()
    knight.draw()

    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

    damage_text_group.update()
    damage_text_group.draw(screen)
    buttons.update() #                     update buttons
    buttons.draw(screen)
    show_labels()

    if(bool_question):
        show_question(qnum)
    #control player actions
    #reset action variables
    attack = False
    target = None

    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()

    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            pygame.mouse.set_visible(False)
            screen.blit(sword_img, pos)

    if game_over == 0:
        #player action
        if knight.alive == False: 
            game_over = -1
    

        #reset if all fighters attack
        if current_fighter > total_fighters:
            current_fighter = 1

    #check if all bandits are dead
    alive_bandits = 0

    for bandit in bandit_list:
        if bandit.alive == True:
            alive_bandits += 1
    
    if alive_bandits == 0:
        game_over = 1
    
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))

        if game_over == -1:
            screen.blit(game_over_img, (290, 50))

        if restart_button.draw():
            bool_question = False
            knight.reset()
            bandit1.reset()
            game_over = 0
            points = 0
            qnum = 1
            game_over = 0

    #Loop to run de game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()