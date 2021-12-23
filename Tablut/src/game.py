import pygame
from pygame.locals import *
from board import Board

class Game:

    def __init__(self, length, width):
        # Paramètres de la page
        self.window = pygame.display.set_mode((length, width))
        pygame.display.set_caption('Tablut')
        logo = pygame.image.load('../images/titles/logo.png')
        pygame.display.set_icon(logo)

        # Chargement des images
        self.background = pygame.image.load("../images/background.jpg")
        self.title = pygame.image.load("../images/titles/title.png")
        self.subtitle = pygame.image.load("../images/titles/subtitle.png")
        self.move = pygame.image.load("../images/tokens/move.png")
        self.m_victory = pygame.image.load("../images/titles/m_victory.png")
        self.s_victory = pygame.image.load("../images/titles/s_victory.png")

        # Création du plateau
        board_model = [
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [1, 0, 0, 0, 2, 0, 0, 0, 1],
            [1, 1, 2, 2, 3, 2, 2, 1, 1],
            [1, 0, 0, 0, 2, 0, 0, 0, 1],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
        ]
        self.board = Board(board_model)

        # Variables pour la gestion des scènes
        self.status = False

        self.is_on_menu = True
        self.is_on_party = False
        self.is_on_results = False


    def get_mouse_position(self):
        '''Renvoie la case dans laquelle se trouve la souris.'''
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        for x in range(9):
            for y in range(9):
                if x * 100 + 100 >= mouse_x and x * 100 + 100 < mouse_x + 100 and y * 100 + 100 >= mouse_y and y * 100 + 100 < mouse_y + 100:
                    return (x,y)

    def menu(self):
        '''Affichage du menu.'''
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.title, (350,350))
        self.window.blit(self.subtitle, (225,500))

    def party(self, event):
        '''Affichage et gestion de la partie.'''
        if event.type == MOUSEBUTTONDOWN:
            self.status = self.board.update(self.get_mouse_position())
        self.board.display(self.window, self.get_mouse_position())

    def results(self):
        '''Affichage des résultats'''
        self.window.blit(self.background, (0, 0))
        if self.status == "m":
            self.window.blit(self.m_victory, (275, 420))
        if self.status == "s":
            self.window.blit(self.s_victory, (275, 420))

    def run(self):
        lock = True
        while lock:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    lock = False

                if self.is_on_menu: # Gestion du menu
                    self.menu()
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        self.is_on_menu = False
                        self.is_on_party = True

                if self.is_on_party: # Gestion de la partie
                    self.party(event)
                    if self.status == "s" or self.status == "m":
                        self.is_on_results = True
                        self.is_on_party = False
                        self.results()

                if self.is_on_results: # Gestion des résultats
                    self.results()
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        self.__init__(900,900)

            pygame.display.update()

        pygame.quit()