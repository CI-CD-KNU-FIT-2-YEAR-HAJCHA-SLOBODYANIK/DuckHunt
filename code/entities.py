import pygame
import random
import math

# Анімація-гіф. Схоже на фліпбук
class Animation:
    def __init__(self, paths, frame_time, target_size, flip_h=False, rotate_deg=0):
        self.frames = []
        for p in paths:
            img = pygame.image.load(p).convert_alpha()
            
            if flip_h: img = pygame.transform.flip(img, True, False)
            if rotate_deg != 0: img = pygame.transform.rotate(img, rotate_deg)

            img = pygame.transform.scale(img, target_size)
            
            self.frames.append(img)
            
        self.frame_time = frame_time
        self.index = 0

    def get_sprite(self, time):
        if self.frame_time <= 0: 
            return self.frames[0]
        
        index = int(time / self.frame_time) % len(self.frames)
        return self.frames[index]

# Візуальна декаль. Просто візуальний ефект із деякою логікою руху. Розраховано на прямолінійний рух або на падіння/зліт.
class VisualDecal:
    def __init__(self, x, y, impulse_x, impulse_y, weight, resistance, animation):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(impulse_x, impulse_y)
        self.weight = weight  # Позитивна вага дає прискорення вниз
        self.resistance = resistance  # Віднімає (НЕ МНОЖИТЬ) ШВИДКІСТЬ не змінюючи НАПРЯМОК
        self.animation = animation
        self.active = True # Статус активності
        
        self.time = 0

        fw, fh = self.animation.frames[0].get_size()
        self.diag = math.sqrt(fw**2 + fh**2)

    def update(self, dt):
        if not self.active: return
        
        self.pos += self.velocity * dt
        self.time += dt

        speed = self.velocity.length()
        if speed > 0:
            reduction = self.resistance * dt
            new_speed = speed - reduction
            if new_speed > 0:
                self.velocity.scale_to_length(new_speed)
            else:
                self.velocity.update(0, 0)

        self.velocity.y += self.weight * dt
        
        if (self.pos.x < -self.diag or self.pos.x > 800 + self.diag or  # Якщо вікно не 800 на 600, то змінювати тут обов'язково!!!
            self.pos.y < -self.diag or self.pos.y > 600 + self.diag):
            self.active = False

    def draw(self, screen):
        sprite = self.animation.get_sprite(self.time)
        
        angle = math.degrees(math.atan2(-self.velocity.y, self.velocity.x)) - 90
        sprite = pygame.transform.rotate(sprite, angle)

        screen.blit(sprite, sprite.get_rect(center=self.pos))


class Crosshair:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 30, 30)

    def update_position(self, pos):
        self.rect.center = pos


class Duck:
    def __init__(self, speed_mult, size_mult, animation):
        self.time = 0
        self.speed_mult = speed_mult
        self.animation = animation # Посилання на фліпбук
        self.rect = pygame.Rect(0, 0, int(60 * size_mult), int(45 * size_mult))  # Типово хітбокс 60 на 45
        self.spawn()

    def spawn(self):
        self.time = 0
        self.rect.x = random.randint(-150, -60)
        self.rect.y = random.randint(50, 400)
        self.velocity = [random.randint(5, 8) * self.speed_mult, random.uniform(-1, 1)]  # Зменшив на 1 діапазон швидкості Х
    
    def move(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def update(self, dt):
        self.time += dt

    def draw(self, screen):
        sprite = self.animation.get_sprite(self.time)
        screen.blit(sprite, sprite.get_rect(center=self.rect.center))


class Menu:
    def __init__(self):
        self.gray = (80, 80, 80)
        self.gold = (255, 215, 0)
        self.dark = (30, 30, 40)
        self.white = (255, 255, 255)

        self.btn_start = pygame.Rect(310, 185, 180, 50)
        self.btn_opts = pygame.Rect(310, 305, 180, 50)

        self.btns_diff = [pygame.Rect(100, 300, 180, 50), pygame.Rect(310, 300, 180, 50), 
                          pygame.Rect(520, 300, 180, 50)]
        self.btn_exit = pygame.Rect(310, 450, 180, 50)

        self.panel_height = 70 # Редагувати тільки тут
    def draw_fancy_ui(self, screen, score_obj, font):
        y_pos = screen.get_height() - self.panel_height
        # Нижня панель
        pygame.draw.rect(screen, self.dark, (0, y_pos, screen.get_width(), self.panel_height))
        pygame.draw.line(screen, self.gold, (0, y_pos), (screen.get_width(), y_pos), 4)
        
        # Смужка часу
        time_ratio = max(0, score_obj.time_left / 60.0)
        pygame.draw.rect(screen, (60, 60, 60), (300, 555, 200, 20))
        # Текст
        pygame.draw.rect(screen, (220, 20, 60), (300, 555, int(200 * time_ratio), 20))
        
        score_txt = font.render(f"SCORE: {score_obj.points:05}", True, self.gold)
        hits_txt = font.render(f"HITS: {score_obj.hits}", True, self.white)
        screen.blit(score_txt, (30, 550))
        screen.blit(hits_txt, (650, 550))

    def draw_overlay(self, screen, state, font, current_idx, levels, score=None):
        if state == "MENU":
            self.draw_main(screen, font, current_idx, levels)
        elif state == "GAMEOVER":
            self.draw_end(screen, font, score)
        elif state == "SETTINGS":
            self.draw_settings(screen, font, current_idx, levels)

    def draw_main(self, screen, font, current_idx, levels):
        screen.fill((20, 20, 30))

        for btn, txt in [(self.btn_start, "START"), (self.btn_opts, "SETTINGS")]:
            pygame.draw.rect(screen, self.gold, btn, 2)
            t = font.render(txt, True, self.gold)
            screen.blit(t, t.get_rect(center=btn.center))

        diff_name = levels[current_idx].name
        diff_txt = font.render(f"Рівень складності - {diff_name}", True, self.white)
        screen.blit(diff_txt, (240, 260))

    def draw_end(self, screen, font, score=None):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        msg = font.render("HUNT OVER! PRESS 'R' TO RESTART", True, self.gold)
        res = font.render(f"TOTAL HITS: {score.hits}", True, self.white)
        screen.blit(msg, (180, 250))
        screen.blit(res, (310, 310))
    
    def draw_settings(self, screen, font, current_idx, levels):
        screen.fill((20, 20, 30))
    
        for i, rect in enumerate(self.btns_diff):
            level = levels[i]
            color = level.color if i == current_idx else self.gray
        
            pygame.draw.rect(screen, color, rect, 2)
        
            txt = font.render(level.name, True, color)
            screen.blit(txt, txt.get_rect(center=rect.center))
    
        pygame.draw.rect(screen, self.gold, self.btn_exit, 1)
        exit_txt = font.render("ВИХІД", True, self.gold)
        screen.blit(exit_txt, exit_txt.get_rect(center=self.btn_exit.center))