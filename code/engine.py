import pygame

# Структура для зберігання параметрів складності
class Difficulty:
    def __init__(self, name, count, speed, size, color):
        self.name = name
        self.count = count  # Цільова кількість качок на екрані
        self.speed_mult = speed
        self.size_mult = size
        self.color = color  # Колір для меню налаштувань

class Score:
    def __init__(self):
        self.points = 0
        self.hits = 0
        self.misses = 0
        self.time_left = 60.0
        self.rounds = 1

    def increment_hit(self):
        self.hits += 1
        self.points += 100

    def increment_miss(self):
        self.misses += 1

    def update_time(self, dt):
        self.time_left -= dt
        return self.time_left <= 0

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 22, bold=True)
        self.running = True
        self.state = "MENU"
        self.score = Score()
        
        self.levels = [
            Difficulty("ЛЕГКИЙ", 6, 0.75, 1.15, (46, 204, 113)),
            Difficulty("СЕРЕДНІЙ", 4, 1.0, 1.0, (241, 196, 15)),
            Difficulty("СКЛАДНИЙ", 4, 1.33, 0.85, (231, 76, 60))
        ]
        self.current_diff_idx = 1

    def restart(self):
        self.score = Score()
        self.state = "PLAYING"

    def get_diff(self):
        return self.levels[self.current_diff_idx] # Повернення активної складності