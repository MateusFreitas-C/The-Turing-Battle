from typing import Any
import pygame
from DamageText import DamageText
from ImageButton import ImageButton
from TextButton import TextButton
from HealthBar import HealthBar
from Fighter import Fighter
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

red = (255, 0 ,0)

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


buttons = pygame.sprite.Group()

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
    buttons.add(TextButton(screen, (60, pos[0]), questions[qnum-1][1][0], 20, "red on yellow",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=lambda: on_click(questions[qnum-1][1][0])))
    buttons.add(TextButton(screen, (460, pos[1]), questions[qnum-1][1][1], 20, "red on yellow",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=lambda: on_click(questions[qnum-1][1][1])))
    buttons.add(TextButton(screen, (60, pos[2]), questions[qnum-1][1][2], 20, "red on yellow",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=lambda: on_click(questions[qnum-1][1][2])))
    buttons.add(TextButton(screen, (460, pos[3]), questions[qnum-1][1][3], 20, "red on yellow",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=lambda: on_click(questions[qnum-1][1][3])))
    

def kill():
    for _ in buttons:
        _.kill()

points = 0
qnum = 1
title = Label(screen, questions[qnum-1][0], 40, screen_height - 140, 20, color="white")
restart_button = ImageButton(screen, 330, 120, restart_img, 120, 30)

knight = Fighter(screen, 200, 260, "Knight", 80, 10)
bandit1 = Fighter(screen, 550, 270, "Bandit", 50, 10)

bandit_list = []
bandit_list.append(bandit1)

knight_health_bar = HealthBar(screen, 140, 190, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(screen, 490, 190, bandit1.hp, bandit1.max_hp)

run = True
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

    knight.damage_text_group.update()
    bandit.damage_text_group.update()
    knight.damage_text_group.draw(screen)
    bandit.damage_text_group.draw(screen)

    buttons.update() #                     update buttons
    buttons.draw(screen)

    show_labels()

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