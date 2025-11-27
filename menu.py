import pygame
from obj import Obj

pygame.init()

class Menu:
    def __init__(self, image_path):
        self.bg = Obj(image_path, 0, 0)
        self.change_scene = False  # vira True quando jogador aperta uma tecla

    def draw(self, window):
        self.bg.drawing(window)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            # qualquer tecla inicia o jogo
            self.change_scene = True


class Gameover:
    def __init__(self, image_path):
        self.bg = Obj(image_path, 0, 0)
        self.change_scene = False  # volta para o menu ao apertar uma tecla

    def draw(self, window):
        self.bg.drawing(window)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            self.change_scene = True


class Vitoria:
    def __init__(self, image_path):
        self.bg = Obj(image_path, 0, 0)
        self.change_scene = False

    def draw(self, window):
        self.bg.drawing(window)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            self.change_scene = True
