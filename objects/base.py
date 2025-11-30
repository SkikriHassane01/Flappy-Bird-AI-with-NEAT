"""
Base Class
Attributes:
=====================================================
- VEL: velocity at which the base moves to the left
- WIDTH: width of the base image
- IMG: image of the base
- y: vertical position of the base
- x1: horizontal position of the first base image
- x2: horizontal position of the second base image (for scrolling effect)
Methods:
=====================================================
- move(): updates the positions of the base images to create a scrolling effect
- draw(win): draws the base images on the game window
"""

import pygame
from utils import settings as cfg
from utils import assets as asset

class Base:
    VEL = cfg.VEL
    WIDTH = asset.BASE_IMG.get_width()
    IMG = asset.BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
    
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))