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
    def __init__(self):
        self.gold = (255, 215, 0)
        self.dark = (30, 30, 40)

    def draw_fancy_ui(self, screen, score_obj, font):
        pygame.draw.rect(screen, self.dark, (0, 530, 800, 70))
        pygame.draw.line(screen, self.gold, (0, 530), (800, 530), 4)
        time_ratio = max(0, score_obj.time_left / 60.0)
        pygame.draw.rect(screen, (60, 60, 60), (300, 555, 200, 20))
        pygame.draw.rect(screen, (220, 20, 60), (300, 555, int(200 * time_ratio), 20))
        score_txt = font.render(f"SCORE: {score_obj.points:05}", True, self.gold)
        hits_txt = font.render(f"HITS: {score_obj.hits}", True, (255, 255, 255))
        screen.blit(score_txt, (30, 550))
        screen.blit(hits_txt, (650, 550))

    def draw_overlay(self, screen, state, font, score=None):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        if state == "MENU":
            msg = font.render("ELITE DUCK HUNT: PRESS 'S'", True, self.gold)
            screen.blit(msg, (230, 270))
        elif state == "GAMEOVER":
            msg = font.render("HUNT OVER! PRESS 'R' TO RESTART", True, self.gold)
            res = font.render(f"TOTAL HITS: {score.hits}", True, (255, 255, 255))
            screen.blit(msg, (180, 250))
            screen.blit(res, (310, 310))