import pygame
from game import Game

pygame.init()
game = Game(900,900)
pygame.mixer.music.load("../sounds/music.wav")
pygame.mixer.music.play(-1)
game.run()