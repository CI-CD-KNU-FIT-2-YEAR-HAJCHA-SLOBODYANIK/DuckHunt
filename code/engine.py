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