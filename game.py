from obj import Obj, Player, Texto
import random

class Game:
    def __init__(self):
        # fundo rolando
        self.bg = Obj("assets/background.jpg", 0, 0)
        self.bg2 = Obj("assets/background.jpg", 0, -640)

        # obstáculos e itens
        self.ekans = Obj("assets/ekans1.png", random.randrange(150, 330), -50)
        self.code = Obj("assets/code.png", random.randrange(0, 330), -50)
        self.pdf = Obj("assets/pdf.png", random.randrange(0, 330), -50)
        self.carro = Obj("assets/carro.png", random.randrange(0, 130), -50)

        # aluno (player)
        self.player = Player("assets/boneco1.png", 150, 570)

        # controle de cena
        self.change_scene = False
        self.scene_type = None  # "gameover" ou "win"

        # HUD
        self.score = Texto(30, "0")
        self.vidas = Texto(30, "4")

    def draw(self, window):
        # fundo
        self.bg.drawing(window)
        self.bg2.drawing(window)
        # objetos
        self.ekans.drawing(window)
        self.code.drawing(window)
        self.pdf.drawing(window)
        self.carro.drawing(window)
        self.player.drawing(window)
        # HUD
        self.score.draw(window, 150, 20)
        self.vidas.draw(window, 20, 20)

    def update(self):
        self.move_bg()
        self.move_ekans()
        self.move_code()
        self.move_pdf()
        self.move_carro()

        # colisões
        self.player.colisao(self.ekans.group, "Ekans")
        self.player.colisao(self.carro.group, "Carro")
        self.player.colisao(self.pdf.group, "Pdf")
        self.player.colisao(self.code.group, "Code")

        # atualiza textos do HUD
        self.score.update_texto(str(self.player.pts))
        self.vidas.update_texto(str(self.player.vida))

        # verifica fim de jogo
        self.game_over()
        self.winner()

    def move_bg(self):
        self.bg.sprite.rect.y += 2
        self.bg2.sprite.rect.y += 2

        if self.bg.sprite.rect.y >= 640:
            self.bg.sprite.rect.y = 0
        if self.bg2.sprite.rect.y >= 0:
            self.bg2.sprite.rect.y = -640

    def move_ekans(self):
        self.ekans.sprite.rect.y += 10
        if self.ekans.sprite.rect.y >= 700:
            self.ekans.sprite.kill()
            self.ekans = Obj("assets/ekans1.png", random.randrange(150, 330), -50)

    def move_code(self):
        self.code.sprite.rect.y += 8
        if self.code.sprite.rect.y >= 700:
            self.code.sprite.kill()
            self.code = Obj("assets/code.png", random.randrange(0, 330), -50)

    def move_pdf(self):
        self.pdf.sprite.rect.y += 8
        if self.pdf.sprite.rect.y >= 700:
            self.pdf.sprite.kill()
            self.pdf = Obj("assets/pdf.png", random.randrange(0, 330), -50)

    def move_carro(self):
        self.carro.sprite.rect.y += 13
        if self.carro.sprite.rect.y >= 700:
            self.carro.sprite.kill()
            self.carro = Obj("assets/carro.png", random.randrange(0, 130), -50)

    def game_over(self):
        if self.player.vida <= 0:
            self.change_scene = True
            self.scene_type = "gameover"

    def winner(self):
        # vitória simples: 10 pontos (10 "codes" coletados)
        if self.player.pts >= 10:
            self.change_scene = True
            self.scene_type = "win"
