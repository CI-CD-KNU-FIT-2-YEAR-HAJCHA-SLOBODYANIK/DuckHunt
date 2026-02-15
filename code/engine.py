import pygame

class Score:
    def __init__(self):
        self.points = 0
        self.hits = 0
        self.misses = 0
        self.time_left = 60.0
        self.rounds = 1