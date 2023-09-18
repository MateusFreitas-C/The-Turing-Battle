import pygame
from src.ImageButton import ImageButton
from src.Fighter import Fighter
from src.HealthBar import HealthBar
from src.TextButton import TextButton
from src.label import *
from src.questions import questions
import time

class Game():
    def __init__(self):

        #create the screen
        self.bottom_panel = 150
        self.screen_width = 800
        self.screen_height = 400 + self.bottom_panel
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        #Game variables
        pygame.display.set_caption("The Turing Battle")
        self.game_over = 0

        #Game Images
        self.backgroud_img = pygame.image.load("img/Background/background.png").convert_alpha()
        self.panel_img = pygame.image.load("img/Icons/panel.png").convert_alpha()
        self.victory_img = pygame.image.load("img/Icons/victory.png").convert_alpha()
        self.game_over_img = pygame.image.load("img/Icons/defeat.png").convert_alpha()
        self.restart_img = pygame.image.load("img/Icons/restart.png").convert_alpha()

        #Game caracters
        self.player = Fighter(self.screen, 200, 260, "Turing", 80, 10)
        self.enemy = Fighter(self.screen, 550, 270, "Bandit", 50, 10)


        #Game configs
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.run_game = True

        #Game utils
        self.buttons = pygame.sprite.Group()
        self.player_health_bar = HealthBar(self.screen, 140, 190, self.player.hp, self.player.max_hp)
        self.enemy_health_bar = HealthBar(self.screen, 490, 190, self.enemy.hp, self.enemy.max_hp)
        self.qnum = 1
        self.points = 0
        self.title = Label(self.screen, questions[self.qnum-1][0], 40, self.screen_height - 140, 20, color="white")
        self.restart_button = ImageButton(self.screen, 330, 120, self.restart_img, 120, 30)


    def draw(self):
            #Draw background
        self.screen.blit(self.backgroud_img, (0,0))
        self.screen.blit(self.panel_img, (0,self.screen_height - self.bottom_panel))

            #Draw fighters
        self.player.draw()
        self.enemy.draw()

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
        if self.qnum < len(questions):
            print(self.qnum, len(questions))
            if answered == "right":
                time.sleep(.5)
                self.points += 1
                self.player.attack(self.enemy)

            else:
                self.enemy.attack(self.player)

            self.qnum += 1 # counter for next question in the list
            # Change the text of the question
            self.title.change_text(questions[self.qnum-1][0], color="white")
            # change the question number
            self.show_question() # delete old buttons and show new
                

            # for the last question...
        elif self.qnum == len(questions):
            print(self.qnum, len(questions))
            if answered == "right":
                self.player.attack(self.enemy)
                self.kill()
                time.sleep(.5)
                self.points +=1
            else:
                self.enemy.attack(self.player)
            time.sleep(.5)

    def on_click(self, clicked_answer):
        print("Click on one answer")

            # Verifique se a resposta clicada é igual à resposta correta da pergunta atual
        if clicked_answer == questions[self.qnum-1][2]:
            self.check_score("right")
        else:
            self.check_score()

    def show_question(self):

        # Kills the previous buttons/sprites
        self.kill()
            
        # The 4 position of the buttons
        pos = [self.screen_height-35, self.screen_height - 70, self.screen_height - 70, self.screen_height - 35]
        # randomized, so that the right one is not on top

        # ============== TEXT: question and answers ====================
        self.buttons.add(TextButton(self.screen, (60, pos[0]), questions[self.qnum-1][1][0], 20, "red on yellow",
                hover_colors="blue on orange", style="button1", borderc=(255,255,0),
                command=lambda: self.on_click(questions[self.qnum-1][1][0])))
        self.buttons.add(TextButton(self.screen, (460, pos[1]), questions[self.qnum-1][1][1], 20, "red on yellow",
                hover_colors="blue on orange", style="button1", borderc=(255,255,0),
                command=lambda: self.on_click(questions[self.qnum-1][1][1])))
        self.buttons.add(TextButton(self.screen, (60, pos[2]), questions[self.qnum-1][1][2], 20, "red on yellow",
                hover_colors="blue on orange", style="button1", borderc=(255,255,0),
                command=lambda: self.on_click(questions[self.qnum-1][1][2])))
        self.buttons.add(TextButton(self.screen, (460, pos[3]), questions[self.qnum-1][1][3], 20, "red on yellow",
                hover_colors="blue on orange", style="button1", borderc=(255,255,0),
                command=lambda: self.on_click(questions[self.qnum-1][1][3])))

    def check_game_over(self):
        if self.player.alive == False: 
            self.game_over = -1

        alive_enemy = 0

        if self.enemy.alive == True:
            alive_enemy += 1
            
        if alive_enemy == 0:
            self.game_over = 1

        if self.game_over != 0:

            if self.game_over == 1:
                self.screen.blit(self.victory_img, (250, 50))

            if self.game_over == -1:
                self.screen.blit(self.game_over_img, (290, 50))

            if self.restart_button.draw():
                self.player.reset()
                self.enemy.reset()
                self.points = 0
                self.qnum = 1
                self.game_over = 0

    def run(self):
        self.run_game = True

        while self.run_game:
            self.clock.tick(self.fps)
            self.update()
            self.draw()
            show_labels()
            self.show_question()
            self.check_game_over()
            self.handle_quit()
            pygame.display.update()