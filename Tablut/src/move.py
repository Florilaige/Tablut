import pygame

class Move:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.surface = pygame.image.load("../images/tokens/move.png")

    def get_coord(self):
        '''Renvoie les coordonnées du mouvement possible.'''
        return (self.x, self.y)

    def set_coord(self, coords):
        '''Affiche les coordonnées du mouvement possible.'''
        self.x = coords[0]
        self.y = coords[1]

    def draw(self, window):
        '''Affichage pygame du mouvement possible'''
        if self.get_coord() != (4,4):
            window.blit(self.surface, (self.x * 100 + 31, self.y * 100 + 31)) # +1 à cause des lignes de la grille faisant 1 pixel de large.