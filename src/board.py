import pygame
from move import Move
from token import Token

class Board:

    def __init__(self, board_model):

        # Remplissage de la grille de jeu
        self.board = [[] ,[] ,[] ,[] ,[] ,[] ,[] ,[] ,[]]
        for i in range(9):
            for j in range(9):
                model = board_model[i][j]
                if model == 0:
                    self.board[i].append(None)
                if model == 1:
                    self.board[i].append(Token("muscovit", i, j))
                if model == 2:
                    self.board[i].append(Token("swedish", i, j))
                if model == 3:
                    self.board[i].append(Token("king", i, j))

        self.background = pygame.image.load("../images/background.jpg") # Fond du plateau de jeu

        # Variables nécessaires à la gestion de la grille
        self.is_muscovit_turn = True
        self.current_token = None
        self.has_king_escape = False

    def get_moves(self, token):
        '''Renvoie tous les déplacements possibles du jeton token sous forme de liste de tuple.'''
        coords = token.get_coord()

        x = coords[0]
        y = coords[1]
        while x > 0: # Test gauche
            x -= 1
            if self.board[x][y] == None:
                self.board[x][y] = Move(x,y)
            else:
                break

        x = coords[0]
        y = coords[1]
        while x < 8: # Test droite
            x += 1
            if self.board[x][y] == None:
                self.board[x][y] = Move(x,y)
            else:
                break

        x = coords[0]
        y = coords[1]
        while y > 0:  # Test haut
            y -= 1
            if self.board[x][y] == None:
                self.board[x][y] = Move(x,y)
            else:
                break

        x = coords[0]
        y = coords[1]
        while y < 8:  # Test bas
            y += 1
            if self.board[x][y] == None:
                self.board[x][y] = Move(x,y)
            else:
                break

    def move(self, actual, goal):
        '''Bouge un pion des coordonnées actual aux coordonées goal'''
        if goal != (4,4):
            obj = self.board[actual[0]][actual[1]]
            self.board[actual[0]][actual[1]] = None
            obj.set_coord(goal)
            obj.is_hover = False
            self.board[goal[0]][goal[1]] = obj
            self.is_muscovit_turn = not self.is_muscovit_turn
            return True
        return False

    def update_token(self, token):
        '''Calcule les conséquences après le mouvement d'un pion.'''
        coords = token.get_coord()

        if token.team == "muscovit":
            opponents = ["swedish", "king"]
        else:
            opponents = ["muscovit"]

        if token.team == "muscovit":
            allies = ["muscovit"]
        else:
            allies = ["swedish", "king"]

        # Test gauche
        x = coords[0]
        y = coords[1]
        if x-2 >= 0:
            if isinstance(self.board[x-1][y], Token) and self.board[x-1][y].team in opponents:
                if isinstance(self.board[x-2][y], Token) and self.board[x-2][y].team in allies:
                    self.board[x - 1][y] = None

        # Test droite
        x = coords[0]
        y = coords[1]
        if x + 2 <= 8:
            if isinstance(self.board[x + 1][y], Token) and self.board[x + 1][y].team in opponents:
                if isinstance(self.board[x + 2][y], Token) and self.board[x + 2][y].team in allies:
                    self.board[x + 1][y] = None

        # Test haut
        x = coords[0]
        y = coords[1]
        if y - 2 >= 0:
            if isinstance(self.board[x][y - 1], Token) and self.board[x][y - 1].team in opponents:
                if isinstance(self.board[x][y - 2], Token) and self.board[x][y - 2].team in allies:
                    self.board[x][y-1] = None

        # Test bas
        x = coords[0]
        y = coords[1]
        if y + 2 <= 8:
            if isinstance(self.board[x][y + 1], Token) and self.board[x][y + 1].team in opponents:
                if isinstance(self.board[x][y + 2], Token) and self.board[x][y + 2].team in allies:
                    self.board[x][y+1] = None

        if token.team == "king" and (0 in coords or 8 in coords):
            return True
        return False

    def check_victory(self, has_king_escape):
        '''Vérifie si une condition de victoire est remplie.'''
        m = False
        k = False
        for line in self.board:
            for token in line:
                if isinstance(token, Token):
                    if token.team == "muscovit":
                        m = True
                    if token.team == "king":
                        k = True
        if not m or self.has_king_escape:
            return 's'
        if not k:
            return "m"
        else:
            return False

    def update(self, mouse):
        '''Update de la grille.'''
        cliked = self.board[mouse[0]][mouse[1]]

        if isinstance(cliked, Move):
            is_moving = self.move(self.current_token.get_coord(), mouse)

            for line in range(9):
                for column in range(9):
                    if isinstance(self.board[line][column], Move):
                        self.board[line][column] = None

            if is_moving:
                self.has_king_escape = self.update_token(self.board[mouse[0]][mouse[1]])

        elif isinstance(cliked, Token):
            if (cliked.team == "muscovit" and self.is_muscovit_turn) or (cliked.team != "muscovit" and not self.is_muscovit_turn):
                self.current_token = cliked
                for line in range(9):
                    for column in range(9):
                        if isinstance(self.board[line][column], Move):
                            self.board[line][column] = None
                self.get_moves(self.current_token)

        else:
            self.current_token = None
            for line in range(9):
                for column in range(9):
                    if isinstance(self.board[line][column], Move):
                        self.board[line][column] = None

        status = self.check_victory(self.has_king_escape)
        return status

    def display(self, window, mouse):
        '''Affichage du plateau de jeu.'''
        # Affichage de la grille
        window.blit(self.background, (0, 0))
        for i in range(1, 9):
            pygame.draw.rect(window, (0, 0, 0), (i * 100, 0, 2, 900))
        for i in range(1, 9):
            pygame.draw.rect(window, (0, 0, 0), (0, i * 100, 900, 2))

        # Affichage du plateau
        for line in self.board:
            for token in line:
                if token != None:
                    if isinstance(token, Token):
                        if (token.team == "muscovit" and self.is_muscovit_turn) or (token.team != "muscovit" and not self.is_muscovit_turn):
                            token.set_hover(mouse)
                    token.draw(window)