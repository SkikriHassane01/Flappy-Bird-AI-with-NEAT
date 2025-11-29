#___________Importing Libraries______________#
import pygame
import neat # NEAT algorithm for AI training
import time
import os
import random

#____________Global Constants_______________#
WIN_HEIGHT = 800
WIN_WIDTH = 600
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

class Bird:
    # Attributes
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25 # How much the bird will tilt
    ROT_VEL = 20 # How much we will rotate the bird for each frame
    ANIMATION_TIME = 5

    # Constructor
    def __init__(self, x, y):
        # Bird's position on screen
        self.x = x 
        self.y = y
        self.tilt = 0 # Current rotation angle (starts flat)
        self.tick_count = 0 # tracks how many frames have passed
        self.vel = 0 # (speed in a specific direction)
        self.height = self.y # reference point that stores the bird's y position at the moments it jumped
        self.img_count = 0 
        self.img = self.IMGS[0]

    # Methods
    def jump(self):
        self.vel = -10.5 # moves upward
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # calculate how far the bird moves vertically
        # Equation of motion = Initial motion + gravity effect
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        # terminal velocity check
        if d >= 16:
            d = 16 # to not fall too fast
        if d < 0:
            d -= 2 # make the jump more responsive

        # Move slowly up or down
        self.y = self.y + d

        ### Tilting the bird
        # Tilt the bird upwards when jumping
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > - 90:
                self.tilt -= self.ROT_VEL # gradually points down by ROT_VEL degrees