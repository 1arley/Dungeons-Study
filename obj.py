import pygame

pygame.init()

# Classe genérica para qualquer objeto estático ou que se mova em linha reta
class Obj:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.sprite.rect = self.image.get_rect()
        self.sprite.rect.x = x
        self.sprite.rect.y = y

        # Grupo com um único sprite para facilitar colisão
        self.group = pygame.sprite.Group()
        self.group.add(self.sprite)

    def drawing(self, window):
        window.blit(self.sprite.image, self.sprite.rect)


# Texto simplificado (HUD)
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


# Player = aluno correndo lateralmente
class Player(Obj):
    def __init__(self, image_path, x, y):
        super().__init__(image_path, x, y)
        self.vel = 7
        self.pts = 0
        self.vida = 4

    def mover(self, teclas, largura_tela):
        # movimento esquerda/direita com as setas
        if teclas[pygame.K_LEFT]:
            self.sprite.rect.x -= self.vel
        if teclas[pygame.K_RIGHT]:
            self.sprite.rect.x += self.vel

        # limita dentro da tela
        if self.sprite.rect.x < 0:
            self.sprite.rect.x = 0
        if self.sprite.rect.x + self.sprite.rect.width > largura_tela:
            self.sprite.rect.x = largura_tela - self.sprite.rect.width

    def colisao(self, grupo, tipo):
        # tipo indica o que acontece: ganho de ponto ou perda de vida
        hits = pygame.sprite.spritecollide(self.sprite, grupo, True)
        if not hits:
            return

        if tipo == "Code":
            self.pts += 1
        elif tipo in ("Pdf", "Ekans", "Carro"):
            self.vida -= 1
