import pygame
import random
import math
from engine import Game
from entities import Duck, Menu, VisualDecal, Animation

FLY_PATHS = [f"code/assets/duck_fly_{i}.png" for i in range(1, 7)]
DEAD_PATHS = [f"code/assets/duck_dead_{i}.png" for i in range(1, 3)]
CLOUD_PATH = ["code/assets/cloud.png"]

def main():
    game = Game()
    menu = Menu()
    decals = []
    ducks = [] 
    cloud_timer = 0.0
    
    cloud_fb = Animation(CLOUD_PATH, 0, (120, 120), rotate_deg=90)
    fly_fb, dead_fb = None, None  # Їх присвоюю потім, бо розмір не конст

    while game.running:
        dt = game.clock.tick(60) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        # --- ЛОГІКА ХМАР (Активна завжди) ---
        cloud_timer += dt
        if cloud_timer >= 4.0:
            v_x = random.uniform(60.0, 120.0) 
            decals.append(VisualDecal(-150, random.randint(30, 200), 
                                      v_x, 0, 0, 0, cloud_fb))
            cloud_timer = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            
            if event.type == pygame.KEYDOWN:
                if game.state == "MENU" and event.key == pygame.K_s:
                    game.restart()
                    d = game.get_diff()
                    t_size = (int(60 * d.size_mult), int(60 * d.size_mult))
                    fly_fb = Animation(FLY_PATHS, 0.1, t_size, flip_h=True)
                    dead_fb = Animation(DEAD_PATHS, 0.1, t_size, flip_h=True)
                    ducks = [Duck(d.speed_mult, d.size_mult, fly_fb) for _ in range(d.count)]
                if game.state == "GAMEOVER" and event.key == pygame.K_r:
                    game.restart()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.state == "MENU":
                    if menu.btn_start.collidepoint(mouse_pos):
                        game.restart()
                        d = game.get_diff()
                        t_size = (int(60 * d.size_mult), int(60 * d.size_mult))
                        fly_fb = Animation(FLY_PATHS, 0.2, t_size, flip_h=True)
                        dead_fb = Animation(DEAD_PATHS, 0.2, t_size, flip_h=True)
                        ducks = [Duck(d.speed_mult, d.size_mult, fly_fb) for _ in range(d.count)]
                    elif menu.btn_opts.collidepoint(mouse_pos):
                        game.state = "SETTINGS"
                
                elif game.state == "SETTINGS":
                    for i, r in enumerate(menu.btns_diff):
                        if r.collidepoint(mouse_pos): game.current_diff_idx = i
                    if menu.btn_exit.collidepoint(mouse_pos): game.state = "MENU"
                
                elif game.state == "PLAYING":
                    hit_found = False
                    for duck in ducks:
                        if duck.rect.collidepoint(mouse_pos):

                            h = 370.0 
                            angle = math.radians(random.uniform(55, 75))
                            direction = 1 if random.random() < 0.5 else -1
                            decals.append(VisualDecal(
                                duck.rect.centerx, duck.rect.centery, 
                                h * math.cos(angle) * direction, 
                                -h * math.sin(angle), 
                                800.0, 200.0, dead_fb
                            ))
                            game.score.increment_hit()
                            duck.spawn()

                            hit_found = True
                            break
                    if not hit_found:
                        game.score.increment_miss()

        game.screen.fill((100, 150, 230))

        for d in decals[:]:
            d.update(dt)
            if not d.active:
                decals.remove(d)
            else:
                d.draw(game.screen)

        if game.state == "PLAYING":
            if game.score.update_time(dt):
                game.state = "GAMEOVER"
            
            for duck in ducks:
                duck.move()
                duck.update(dt)

                if (duck.rect.x > 850 or duck.rect.y > 850 or duck.rect.y < menu.panel_height - 50): duck.spawn()
                duck.draw(game.screen)
            
            pygame.draw.circle(game.screen, (255, 0, 0), mouse_pos, 15, 3)
            menu.draw_fancy_ui(game.screen, game.score, game.font)
        
        else:
            menu.draw_overlay(game.screen, game.state, game.font, 
                              game.current_diff_idx, game.levels, game.score)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()