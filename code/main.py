import pygame
from engine import Game
from entities import Duck, Crosshair, Menu

def main():
    game = Game()
    crosshair = Crosshair()
    menu = Menu()
    ducks = [Duck() for _ in range(4)]

    while game.running:
        dt = game.clock.tick(60) / 1000.0
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            if event.type == pygame.KEYDOWN:
                if game.state == "MENU" and event.key == pygame.K_s:
                    game.state = "PLAYING"
                if game.state == "GAMEOVER" and event.key == pygame.K_r:
                    game.restart()
