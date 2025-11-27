from obj import Obj, Player, Texto
import random

class Game:

    def __init__(self):
        # Fundo: corredor/campus rolando para baixo (efeito de corrida)
        self.bg = Obj("assets/background.jpg", 0, 0)
        self.bg2 = Obj("assets/background.jpg", 0, -640)

        # Obstáculos e itens no tema Pegai Run:
        # ekans  -> distração/obstáculo (ex: colega atrapalhando, cone, etc.)
        # code   -> código/projeto correto (ganha pontos)
        # pdf    -> trabalho/prova atrasada (tira vida)
        # carro  -> trânsito/obstáculo forte (tira mais vida)
        # player -> aluno correndo para entregar o trabalho / pegar aprovação
        self.ekans = Obj("assets/ekans1.png", random.randrange(150, 330), -50)
        self.code = Obj("assets/code.png", random.randrange(0, 330), -50)
        self.pdf = Obj("assets/pdf.png", random.randrange(0, 330), -50)
        self.carro = Obj("assets/carro.png", random.randrange(0, 130), -50)
        self.player = Player("assets/boneco1.png", 150, 570)

        # Controle de mudança de cena (win / gameover)
        self.change_scene = False
        self.scene_type = None

        # HUD: créditos (pontos) e “vidas” do aluno
        self.score = Texto(120, "0")
        self.vidas = Texto(60, "4")

    def draw(self, window):
        # Desenha fundo em loop
        self.bg.drawing(window)
        self.bg2.drawing(window)

        # Desenha objetos do jogo
        self.ekans.drawing(window)
        self.code.drawing(window)
        self.pdf.drawing(window)
        self.carro.drawing(window)
        self.player.drawing(window)

        # Desenha HUD (pontuação e vidas)
        self.score.draw(window, 150, 50)
        self.vidas.draw(window, 50, 50)

    def update(self):
        # Animações simples (spritesheet do aluno e do obstáculo)
        self.ekans.anima("ekans", 8, 4)
        self.player.anima("boneco", 8, 4)

        # Movimento do cenário e dos objetos
        self.move_bg()
        self.move_ekans()
        self.move_code()
        self.move_pdf()
        self.move_carro()

        # Verifica colisões do aluno com cada tipo de objeto
        # A lógica de ganho/perda de pontos/vida fica dentro de Player.colisao
        self.player.colisao(self.ekans.group, "Ekans")   # obstáculo
        self.player.colisao(self.carro.group, "Carro")   # obstáculo forte
        self.player.colisao(self.pdf.group, "Pdf")       # penalidade
        self.player.colisao(self.code.group, "Code")     # recompensa

        # Condições de fim de jogo
        self.game_over()
        self.winner()

        # Atualiza textos do HUD com os valores atuais do player
        self.score.update_texto(str(self.player.pts))
        self.vidas.update_texto(str(self.player.vida))

    def move_bg(self):
        # Faz o fundo “rolar” para dar sensação de movimento do aluno
        self.bg.sprite.rect[1] += 2
        self.bg2.sprite.rect[1] += 2

        if self.bg.sprite.rect[1] >= 640:
            self.bg.sprite.rect[1] = 0

        if self.bg2.sprite.rect[1] >= 0:
            self.bg2.sprite.rect[1] = -640

    def move_ekans(self):
        # Obstáculo vindo de cima (ex: colega/distração)
        self.ekans.sprite.rect[1] += 10

        if self.ekans.sprite.rect[1] >= 700:
            self.ekans.sprite.kill()
            self.ekans = Obj("assets/ekans1.png", random.randrange(150, 330), -50)

    def move_code(self):
        # Item positivo: “código certo / crédito”
        self.code.sprite.rect[1] += 8

        if self.code.sprite.rect[1] >= 700:
            self.code.sprite.kill()
            self.code = Obj("assets/code.png", random.randrange(0, 330), -50)

    def move_pdf(self):
        # Penalidade: “trabalho/prova atrasada”
        self.pdf.sprite.rect[1] += 8

        if self.pdf.sprite.rect[1] >= 700:
            self.pdf.sprite.kill()
            self.pdf = Obj("assets/pdf.png", random.randrange(0, 330), -50)

    def move_carro(self):
        # Obstáculo forte: “carro no campus / trânsito”
        self.carro.sprite.rect[1] += 13

        if self.carro.sprite.rect[1] >= 700:
            self.carro.sprite.kill()
            self.carro = Obj("assets/carro.png", random.randrange(0, 130), -50)

    def game_over(self):
        # Quando o aluno perde todas as vidas → tela de reprovação
        if self.player.vida <= 0:
            self.change_scene = True
            self.scene_type = "gameover"

    def winner(self):
        # Condição de vitória: acumulou créditos suficientes (ajuste o valor se quiser)
        if self.player.pts >= 10:
            self.change_scene = True
            self.scene_type = "win"
