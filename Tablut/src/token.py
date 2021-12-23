import pygame

class Token:

    def __init__(self, team, x, y):
        self.team = team
        self.x = x
        self.y = y
        self.surface = pygame.image.load(f"../images/tokens/{team}.png")
        self.surface_hover = pygame.image.load(f"../images/tokens/{team}_hover.png")
        self.is_hover = False

    def get_coord(self):
        '''Renvoie les coordonnées du jeton.'''
        return (self.x, self.y)

    def set_coord(self, coords):
        '''Modifie les coordonnées du jeton.'''
        self.x = coords[0]
        self.y = coords[1]

    def set_hover(self, mouse):
        '''Determine si la souris se situe au dessus du jeton.'''
        if self.get_coord() == mouse:
            self.is_hover = True
        else:
            self.is_hover = False

    def draw(self, window):
        '''Affichage pygame du jeton.'''
        if self.is_hover:
            window.blit(self.surface_hover, (self.x * 100 +6, self.y * 100 +6)) # +1 à cause des lignes de la grille faisant 1 pixel de large.
        else:
            window.blit(self.surface, (self.x * 100 +6, self.y * 100 +6)) # idem