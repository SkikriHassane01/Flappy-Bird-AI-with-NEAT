#___________Importing Libraries______________#
from utils import settings as cfg
from utils import assets as asset
import pygame
import neat # NEAT algorithm for AI training
import time
import os
import random

class Bird:
    # Attributes
    IMGS = asset.BIRD_IMGS

    # Constructor
    def __init__(self, x, y):
        # Bird's position on screen
        self.x = x 
        self.y = y
        self.tilt = 0 # Current rotation angle (starts flat)
        self.tick_count = 0 # tracks how many frames have passed
        self.vel = 0 # (speed in a specific direction)
        self.height = self.y # reference point that stores the bird's y position at the moments it jumped
        """
        We need to make the bird flap its wings, so we have a cycle of 3 images 
        - Wings Up 
        - Wings Middle
        - Wings Down
        img_count: here we will count how many frames have passed so we can change the image slowly (eg. every 5 frames)
        for example (wings up, wings up .... 5times, wings Middle... 5times , wings down and so on)
        """
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
            if self.tilt < cfg.MAX_ROTATION:
                self.tilt = cfg.MAX_ROTATION
        else:
            if self.tilt > - 90:
                self.tilt -= cfg.ROT_VEL # gradually points down by ROT_VEL degrees

    def draw(self, win):
        self.img_count += 1

        if self.img_count < cfg.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < 2 * cfg.ANIMATION_TIME:
            self.img = self.IMGS[1] 
        elif self.img_count < 3 * cfg.ANIMATION_TIME:
            self.img = self.IMGS[2]
        elif self.img_count < 4 * cfg.ANIMATION_TIME:
            self.img = self.IMGS[1]
        elif self.img_count < 4 * cfg.ANIMATION_TIME + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = cfg.ANIMATION_TIME * 2

        # rotate the bird image around its center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center= self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)               

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.heigh = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(asset.PIPE_IMG, False, True)
        self.PIPE_BOTTOM = asset.PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.heigh = random.randrange(50, 450)
        self.top = self.heigh - self.PIPE_TOP.get_height()
        self.bottom = self.heigh + cfg.GAP

    def move(self):
        self.x -= cfg.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top)) 
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    
    # Pixel perfect collision
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
        
        # endless scrolling effect
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
    
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def draw_window(win, bird, pipes, base):
    win.blit(asset.BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(230,350)
    base = Base(550)
    pipes = [Pipe(600)]

    win = pygame.display.set_mode((cfg.WIN_WIDTH, cfg.WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(cfg.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # bird.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()
            # check for collision
            if pipe.collide(bird):
                pass # handle collision

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            pipes.append(Pipe(550))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 550 or bird.y < 0:
            pass # handle ground or ceiling collision

        base.move()
        draw_window(win, bird, pipes, base)

    pygame.quit()

if __name__ == "__main__":
    main()