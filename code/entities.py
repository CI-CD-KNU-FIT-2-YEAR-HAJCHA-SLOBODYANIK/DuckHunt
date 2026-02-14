import pygame
import random

class Duck:
    def __init__(self):
        self.image = pygame.Surface((60, 45))
        self.image.fill((255, 215, 0)) 
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        self.rect.x = random.randint(-150, -60)
        self.rect.y = random.randint(50, 400)
        self.velocity = [random.randint(4, 9), random.uniform(-1, 1)]

    def move(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

class Crosshair:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 30, 30)

    def update_position(self, pos):
        self.rect.center = pos

class Menu:
    def draw(self, screen, game_state, score, font):
        if game_state == "MENU":
            text = font.render("DUCK HUNT: PRESS 'S' TO START", True, (0, 0, 0))
            screen.blit(text, (220, 280))
        elif game_state == "GAMEOVER":
            text = font.render(f"GAME OVER! HITS: {score.hits} - PRESS 'R' TO RESTART", True, (200, 0, 0))
            screen.blit(text, (180, 280))