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
            if event.type == pygame.MOUSEBUTTONDOWN and game.state == "PLAYING":
                hit_found = False
                for duck in ducks:
                    if duck.rect.collidepoint(mouse_pos):
                        game.score.increment_hit()
                        duck.spawn()
                        hit_found = True
                        break
                if not hit_found:
                    game.score.increment_miss()

        game.screen.fill((100, 150, 230))

        if game.state == "MENU":
            menu.draw_overlay(game.screen, "MENU", game.font)
        elif game.state == "PLAYING":
            if game.score.update_time(dt):
                game.state = "GAMEOVER"
            crosshair.update_position(mouse_pos)
            for duck in ducks:
                duck.move()
                if duck.rect.x > 850: duck.spawn()
                game.screen.blit(duck.image, duck.rect)
            pygame.draw.circle(game.screen, (255, 0, 0), mouse_pos, 15, 3)
            menu.draw_fancy_ui(game.screen, game.score, game.font)
        elif game.state == "GAMEOVER":
            menu.draw_overlay(game.screen, "GAMEOVER", game.font, game.score)
