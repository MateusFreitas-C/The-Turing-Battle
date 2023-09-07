import pygame
from src.Game import Game

pygame.init()

if __name__ == "__main__":
    game = Game()
    game.run()

pygame.quit()