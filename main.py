import pygame
import neat
import os
from utils import settings as cfg
from utils import assets as asset
from objects.bird import Bird
from objects.pipe import Pipe
from objects.base import Base

def draw_window(win, bird, pipes, base, score):
    win.blit(asset.BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    text = cfg.STATE_FONT.render('Score: ' + str(score), 1, (255,255,255))
    win.blit(text, (cfg.WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((cfg.WIN_WIDTH, cfg.WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0

    run = True
    while run:
        clock.tick(cfg.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.move()
        
        # Pipe management
        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird):
                print("Game Over")
                run = False # Stop game on collision
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
        
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
        
        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730:
            print("Hit Floor")
            run = False

        base.move()
        draw_window(win, bird, pipes, base, score)

    pygame.quit()

if __name__ == "__main__":
    main()