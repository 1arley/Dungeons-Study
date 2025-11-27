import pygame
import random

pygame.init()

# Classe genérica para qualquer objeto de jogo (fundo, obstáculos, itens)
class Obj:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.sprite.rect = self.image.get_rect()
        self.sprite.rect.x = x
        self.sprite.rect.y = y

        # grupo com 1 sprite, para facilitar usar .group nas colisões
        self.group = pygame.sprite.Group()
        self.group.add(self.sprite)

        # suporte a animação por spritesheet
        self.sheet = None
        self.frames = []
        self.current_frame = 0
        self.anim_timer = 0

    def drawing(self, window):
        window.blit(self.sprite.image, self.sprite.rect)

    def anima(self, prefix, colunas, linhas):
        """
        prefix: nome base do arquivo de spritesheet, sem número
        colunas, linhas: quantidade de frames na sheet
        Ex.: "boneco" -> assets/boneco.png
        """
        # Só carrega spritesheet e corta frames na primeira chamada
        if self.sheet is None:
            path = f"assets/{prefix}.png"
            self.sheet = pygame.image.load(path).convert_alpha()
            sheet_rect = self.sheet.get_rect()
            frame_width = sheet_rect.width // colunas
            frame_height = sheet_rect.height // linhas

            for linha in range(linhas):
                for coluna in range(colunas):
                    frame_surf = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                    frame_surf.blit(
                        self.sheet,
                        (0, 0),
                        (coluna * frame_width, linha * frame_height, frame_width, frame_height)
                    )
                    self.frames.append(frame_surf)

        # Avança frames devagar para ficar visível
        self.anim_timer += 1
        if self.anim_timer >= 5:
            self.anim_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.sprite.image = self.frames[self.current_frame]


# Classe do texto na tela (pontuação, vidas)
class Texto:
    def __init__(self, size, text, color=(255, 255, 255)):
        self.font = pygame.font.SysFont("Arial", size, True, False)
        self.text = text
        self.color = color
        self.render = self.font.render(self.text, True, self.color)

    def update_texto(self, new_text):
        self.text = new_text
        self.render = self.font.render(self.text, True, self.color)

    def draw(self, window, x, y):
        window.blit(self.render, (x, y))


# Classe do aluno (jogador) correndo pelo campus
class Player(Obj):
    def __init__(self, image_path, x, y):
        super().__init__(image_path, x, y)
        # Player usa o mesmo esquema de sprite do Obj, mas com lógica própria
        self.vel = 7
        self.pts = 0
        self.vida = 4

    def mover(self, teclas, largura_tela):
        # Movimento lateral (esquerda/direita) para desviar dos obstáculos
        if teclas[pygame.K_LEFT]:
            self.sprite.rect.x -= self.vel
        if teclas[pygame.K_RIGHT]:
            self.sprite.rect.x += self.vel

        # Mantém o aluno dentro da tela
        if self.sprite.rect.x < 0:
            self.sprite.rect.x = 0
        if self.sprite.rect.x + self.sprite.rect.width > largura_tela:
            self.sprite.rect.x = largura_tela - self.sprite.rect.width

    def colisao(self, grupo, tipo):
        """
        tipo:
          - "Code": item bom -> aumenta pontos
          - "Pdf": penalidade
          - "Ekans" ou "Carro": obstáculos que tiram vida
        """
        hits = pygame.sprite.spritecollide(self.sprite, grupo, True)
        if not hits:
            return

        if tipo == "Code":
            # Pegou código / crédito
            self.pts += 1
        elif tipo == "Pdf":
            # Burocracia / trabalho atrasado
            self.vida -= 1
        elif tipo in ("Ekans", "Carro"):
            # Obstáculos fortes
            self.vida -= 1
        # Se quiser efeitos diferentes por tipo, basta ajustar aqui
