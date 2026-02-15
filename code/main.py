import pygame
from engine import Game
from entities import Duck, Crosshair, Menu

def main():
    game = Game()
    crosshair = Crosshair()
    menu = Menu()
    ducks = [Duck() for _ in range(4)]
