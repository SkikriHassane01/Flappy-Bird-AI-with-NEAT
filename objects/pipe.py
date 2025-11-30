"""
Pipe Class

Attributes:
=====================================================
- x: horizontal position of the pipe
- height: height of the pipe
- top: top position of the top pipe
- bottom: bottom position of the bottom pipe
- PIPE_TOP: image of the top pipe (flipped)
- PIPE_BOTTOM: image of the bottom pipe
- passed: boolean to check if the bird has passed the pipe

Methods:
=====================================================
- set_height(): randomly sets the height of the pipe and calculates top and bottom positions
- move(): moves the pipe to the left by a constant velocity
- draw(win): draws the top and bottom pipes on the game window
- collide(bird): checks for pixel-perfect collision between the pipe and the bird
"""

import pygame
import random
from utils import settings as cfg
from utils import assets as asset

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(asset.PIPE_IMG, False, True)
        self.PIPE_BOTTOM = asset.PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + cfg.GAP

    def move(self):
        self.x -= cfg.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top)) 
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False