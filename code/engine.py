import pygame

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
        self.running = True
        self.state = "MENU"

        self.score = Score()
        self.font = pygame.font.SysFont("Verdana", 24, bold=True)

    def restart(self):
        self.score = Score()
        self.state = "PLAYING"