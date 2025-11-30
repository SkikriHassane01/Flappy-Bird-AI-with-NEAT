"""
The Bird Class
Attributes:
=====================================================
- IMGS: 3 birds images(wings up, middle, down)
- x: horizontal position of the bird
- y: vertical position of the bird
- tilt: current rotation angle of the bird
- tick_count: counts the number of frames since the last jump => gravity effect
- vel: vertical velocity of the bird (positive is down, negative is up)
- height: the y position of the bird at the moment it jumped => when start falling down, to make the tilt effect
- img_count: counts the number of frames to manage wing flapping animation
- img: current image of the bird to be displayed

Methods:
=====================================================
- jump(): makes the bird jump by setting its vertical velocity to a negative value
- move(): updates the bird's position and tilt based on its velocity and gravity
- draw(win): draws the bird on the game window with the appropriate rotation and animation frame
- get_mask(): returns a mask for the current image of the bird for pixel-perfect collision detection
"""
import pygame 
from utils import settings as cfg
from utils import assets as asset

class Bird:
    IMGS = asset.BIRD_IMGS
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[1]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
    
    def move(self):
        self.tick_count += 1

        # calculate how far the bird moves vertically (Equation of motion)
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16
        if d < 0:
            d -= 2
        
        self.y = self.y + d

        # Tilting the bird
        if d < 0 or self.y < self.height + 50:
            if self.tilt < cfg.MAX_ROTATION:
                self.tilt = cfg.MAX_ROTATION
        else:
            if self.tilt > - 90:
                self.tilt -= cfg.ROT_VEL

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