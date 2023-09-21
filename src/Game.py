import pygame
from src.ImageButton import ImageButton
from src.Fighter import Fighter
from src.HealthBar import HealthBar
from src.TextButton import TextButton
from src.label import *
from src.questions import *
import time
import random

class Game():
    def __init__(self):

        #create the screen
        self.bottom_panel = 150
        self.screen_width = 800
        self.screen_height = 533 + self.bottom_panel
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        #Game variables
        pygame.display.set_caption("The Turing Battle")
        self.game_over = 0

        random.shuffle(easy_questions)
        random.shuffle(medium_questions)
        random.shuffle(hard_questions)

        self.questions = easy_questions

        #Game Images
        self.backgroud_img = pygame.image.load("img/Background/background2.jpeg").convert_alpha()
        self.panel_img = pygame.image.load("img/Icons/panel2.png").convert_alpha()
        self.victory_img = pygame.image.load("img/Icons/victory.png").convert_alpha()
        self.game_over_img = pygame.image.load("img/Icons/defeat.png").convert_alpha()
        self.restart_img = pygame.image.load("img/Icons/restart.png").convert_alpha()
        self.next_img = pygame.image.load("img/Icons/next.png").convert_alpha()

        #Game caracters
        self.player = Fighter(self.screen, 220, 300, "Turing", 10, 10)
        self.enemies = [
            Fighter(self.screen, 550, 320, "Robot1", 10, 4),
            Fighter(self.screen, 550, 320, "Robot2", 20, 8),
            Fighter(self.screen, 550, 320, "Robot3", 30, 10)
        ]

        self.current_enemy = 0
        self.enemy = self.enemies[self.current_enemy]

        #Game configs
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.run_game = True

        #Game utils
        self.buttons = pygame.sprite.Group()
        self.player_health_bar = HealthBar(self.screen, 90, 40, self.player.hp, self.player.max_hp)
        self.enemy_health_bar = HealthBar(self.screen, 90, 130, self.enemy.hp, self.enemy.max_hp)
        self.qnum = 1
        self.title = Label(self.screen, self.questions[self.qnum-1][0], 40, self.screen_height - 140, 20, color=(17, 42, 70))
        self.restart_button = ImageButton(self.screen, 330, 120, self.restart_img, 120, 30)
        self.next_button = ImageButton(self.screen, 330, 120, self.next_img, 120, 30)


    def draw(self):
            #Draw background
        self.screen.blit(self.backgroud_img, (0,0))
        self.screen.blit(self.panel_img, (0,self.screen_height - self.bottom_panel))

            #Draw fighters
        self.player.draw()
        self.enemy.draw()

            #Draw Icon
        self.player.draw_icon(40, 40)
        self.enemy.draw_icon(40, 140)    

            #Draw health bar
        self.player_health_bar.draw(self.player.hp)
        self.enemy_health_bar.draw(self.enemy.hp)

            #Draw damage text
        self.player.damage_text_group.draw(self.screen)
        self.enemy.damage_text_group.draw(self.screen)

            #Draw buttons
        self.buttons.draw(self.screen)

    def handle_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run_game = False

    def update(self):
        self.player.update()
        self.enemy.update()
        self.player.damage_text_group.update()
        self.enemy.damage_text_group.update()
        self.buttons.update()
        
    def kill(self):
        for _ in self.buttons:
            _.kill()

    def check_score(self, answered="wrong"):
        if self.qnum < len(self.questions):
            print(self.qnum, len(self.questions))
            if answered == "right":
                time.sleep(.2)
                self.player.attack(self.enemy)
                time.sleep(.2)

            else:
                time.sleep(.2)
                self.enemy.attack(self.player)

            self.qnum += 1 # counter for next question in the list
            self.check_level()
            # change the question number
            time.sleep(.2)
            self.show_question() # delete old buttons and show new
                

            # for the last question...
        elif self.qnum == len(self.questions):
            print(self.qnum, len(self.questions))
            if answered == "right":
                
                self.player.attack(self.enemy)
                time.sleep(.2)
                self.kill()
            else:
                self.enemy.attack(self.player)
            time.sleep(.2)

    def on_click(self, clicked_answer):
        print("Click on one answer")

            # Verifique se a resposta clicada é igual à resposta correta da pergunta atual
        if clicked_answer == self.questions[self.qnum-1][2]:
            self.check_score("right")
        else:
            self.check_score()

    def show_question(self):

        # Kills the previous buttons/sprites
        self.kill()
        self.title.change_text(self.questions[self.qnum-1][0], color=(17, 42, 70))
        # The 4 position of the buttons
        pos = [self.screen_height-35, self.screen_height - 80, self.screen_height - 80, self.screen_height - 35]

        self.buttons.add(TextButton(self.screen, (60, pos[0]), self.questions[self.qnum-1][1][0], 20, "red on yellow",
                hover_colors="blue on orange", style="button2", borderc=(255,255,0),
                command=lambda: self.on_click(self.questions[self.qnum-1][1][0])))
        self.buttons.add(TextButton(self.screen, (460, pos[1]), self.questions[self.qnum-1][1][1], 20, "red on yellow",
                hover_colors="blue on orange", style="button2", borderc=(255,255,0),
                command=lambda: self.on_click(self.questions[self.qnum-1][1][1])))
        self.buttons.add(TextButton(self.screen, (60, pos[2]), self.questions[self.qnum-1][1][2], 20, "red on yellow",
                hover_colors="blue on orange", style="button2", borderc=(255,255,0),
                command=lambda: self.on_click(self.questions[self.qnum-1][1][2])))
        self.buttons.add(TextButton(self.screen, (460, pos[3]), self.questions[self.qnum-1][1][3], 20, "red on yellow",
                hover_colors="blue on orange", style="button2", borderc=(255,255,0),
                command=lambda: self.on_click(self.questions[self.qnum-1][1][3])))        

    def check_game_over(self):
        if self.player.alive == False: 
            self.game_over = -1

        alive_enemy = 0

        if self.enemy.alive == True:
            alive_enemy += 1

        else:
            if self.current_enemy < len(self.enemies) - 1:
            # Avance para o próximo inimigo
                if self.next_button.draw():
                    self.current_enemy += 1
                    self.qnum = 1
                    self.player.reset()
                    self.enemy = self.enemies[self.current_enemy]
            
            else:
                self.game_over = 1

        if self.game_over != 0:

            if self.game_over == 1:
                self.screen.blit(self.victory_img, (250, 50))

            if self.game_over == -1:
                self.screen.blit(self.game_over_img, (290, 50))

            if self.restart_button.draw():
                self.current_enemy = 0
                self.enemy = self.enemies[self.current_enemy]
                self.player.reset()
                self.enemy.reset()
                self.qnum = 1
                self.game_over = 0
                

    def check_level(self):
        if self.current_enemy == 0:
            self.questions = easy_questions
        
        elif self.current_enemy == 1:
            self.questions = medium_questions
        
        elif self.current_enemy == 2:
            self.questions = hard_questions

    def run(self):
        self.run_game = True

        while self.run_game:
            self.clock.tick(self.fps)
            self.update()
            self.draw()
            show_labels()
            self.show_question()
            self.check_level()
            self.check_game_over()
            self.handle_quit()
            pygame.display.update()