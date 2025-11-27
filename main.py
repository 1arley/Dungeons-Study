import pygame
from menu import Menu, Gameover, Vitoria
from game import Game


class Main:
    def __init__(self, sizex, sizey, title):
        pygame.init()

        # Sem áudio (para evitar erro de dispositivo)
        # pygame.mixer.init()
        # pygame.mixer.music.load("assets/Sons/musica.mp3")
        # pygame.mixer.music.play(-1)

        self.window = pygame.display.set_mode((sizex, sizey))
        pygame.display.set_caption(title)

        self.sizex = sizex
        self.sizey = sizey

        self.menu = Menu("assets/tela inicio.png")
        self.game = Game()
        self.gameover = Gameover("assets/game_over.png")
        self.winner = Vitoria("assets/win.png")

        self.loop = True
        self.fps = pygame.time.Clock()

    def draw(self):
        if not self.menu.change_scene:
            self.menu.draw(self.window)
        elif not self.game.change_scene:
            # movimento contínuo do aluno
            teclas = pygame.key.get_pressed()
            self.game.player.mover(teclas, self.sizex)

            self.game.update()
            self.game.draw(self.window)
        elif self.game.scene_type == "gameover" and not self.gameover.change_scene:
            self.gameover.draw(self.window)
        elif self.game.scene_type == "win" and not self.winner.change_scene:
            self.winner.draw(self.window)
        else:
            # reset geral e volta para o menu
            self.menu.change_scene = False
            self.game.change_scene = False
            self.gameover.change_scene = False
            self.winner.change_scene = False
            self.game.player.vida = 4
            self.game.player.pts = 0
            self.game.scene_type = None

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop = False
            if not self.menu.change_scene:
                self.menu.events(event)
            elif not self.game.change_scene:
                # movimento é contínuo em draw(); aqui não precisa de nada
                pass
            elif not self.winner.change_scene:
                self.winner.events(event)
            else:
                self.gameover.events(event)

    def update(self):
        while self.loop:
            self.fps.tick(30)
            self.draw()
            self.events()
            pygame.display.update()


if __name__ == "__main__":
    game = Main(360, 640, "Race for Approval")
    game.update()
