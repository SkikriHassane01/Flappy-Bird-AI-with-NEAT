import sys 
import os 

project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(os.path.abspath(project_root))

import pygame
from objects.bird import Bird
from utils import settings as cfg
from utils import assets as asset

pygame.init()
win = pygame.display.set_mode((cfg.WIN_WIDTH, cfg.WIN_HEIGHT))
clock = pygame.time.Clock()

def main():
    bird = Bird(200, 200)
    run = True
    print("Press Space to jump\n close window to stop")

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                    print(f"Jumped! Velocity: {bird.vel}")
        
        bird.move()

        win.blit(asset.BG_IMG, (0,0))
        bird.draw(win)
        pygame.display.update()

        if bird.y > 600:
            print("Bird fell off the screen! Resetting...")
            bird.y = 200
            bird.vel = 0
    pygame.quit()

if __name__ == "__main__":
    main()