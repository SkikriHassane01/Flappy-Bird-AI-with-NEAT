import os 
import sys 
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(os.path.abspath(project_root))

import pygame
from objects.bird import Bird
from objects.pipe import Pipe
from utils import settings as cfg
from utils import assets as asset

pygame.init()
win = pygame.display.set_mode((cfg.WIN_WIDTH, cfg.WIN_HEIGHT))
clock = pygame.time.Clock()

def main():
    bird = Bird(230, 350)
    pipes = [Pipe(600)]
    run = True
    score = 0

    print("TEST START: Avoid the pipes!")

    while run:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.move()

        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()
            
            # Test Collision
            if pipe.collide(bird):
                print("CRASH! Collision detected.")
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            print(f"Score: {score}")
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)
        # ------------------

        # Draw
        win.blit(asset.BG_IMG, (0,0))
        for pipe in pipes:
            pipe.draw(win)
        bird.draw(win)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()