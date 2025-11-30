import pygame 
import neat 
import os
from utils import settings as cfg
from utils import assets as asset
from objects.bird import Bird
from objects.pipe import Pipe
from objects.base import Base
import pickle

GEN = 0
WINNER_GENOME = None

def eval_genomes(genomes, config):
    """
    - genome: is the bird's DNA, it determines => nodes and weights, and the connections
    - nets: neural networks created from genomes

    ==> this are the steps:
    - Create a neural network for each genome
    - Create a bird for each network
    - run the game loop => let them play
    - assign grades (fitness)
        - bird stays alive for each frame (second)? ==> + 0.1
        - bird passes pipe? ==> + 5
        - bird hits pipe? ==> -1 and remove it
    - when all birds are dead, function ends. neat looks at the fitness scores, kills the bad birds, breeds the good ones, and calls eval_genomes for next gen
    """
    global GEN, WINNER_GENOME
    GEN += 1
    
    # 1. create lists to hold the neural networks(nets), genomes(ge), and birds
    nets = []
    ge = []
    birds = []

    # 2. for each genome, create a neural network and a bird
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((cfg.WIN_WIDTH, cfg.WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0

    run = True
    while run and len(birds) > 0:
        clock.tick(cfg.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        # 3. determine which pipe to look at (0, 1) 
        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_index = 1
        
        # 4. move birds and ai decisions
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1  # each frame alive +0.1 fitness

            # Activate the Neural Network
            # Inputs: Bird Y, Distance to Top Pipe, Distance to Bottom Pipe
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))

            # Decision: jump or not
            if output[0] > 0.5:
                bird.jump()
        
        base.move()

        # 5. pipe management
        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1  # hit pipe -1 fitness
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
        
        if add_pipe:
            score += 1
            for g in ge:
                 g.fitness += 5  # passed pipe +5 fitness
            pipes.append(Pipe(600))
        
            # Stop when score reaches 30
            if score >= 30:
                print(f"Score of 30 reached! Stopping training.")
                WINNER_GENOME = max(ge, key=lambda g: g.fitness)
                run = False
                break
        
        for r in rem:
            pipes.remove(r)
        
        # 6. check for bird hitting the ground
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        # 7. draw everything
        draw_window(win, birds, pipes, base, score, GEN)
    if WINNER_GENOME is not None:
        raise StopIteration

def draw_window(win, birds, pipes, base, score, gen):
    win.blit(asset.BG_IMG, (0, 0))
    for pip in pipes:
        pip.draw(win)
    text = cfg.STATE_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (cfg.WIN_WIDTH - 10 - text.get_width(), 10))

    text = cfg.STATE_FONT.render("Gen: " + str(gen), 1, (255,255,255))
    win.blit(text, (10, 10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)

    pygame.display.update()

def run(config_path):
    global WINNER_GENOME
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # run for 50 generations
    try:
        winner = p.run(eval_genomes, 50)
    except StopIteration:
        winner = WINNER_GENOME
        print("Training stopped early - goal reached!")
    
    # Save the best bird
    if winner:
        with open("best_bird.pkl", "wb") as f:
            pickle.dump((winner, config), f)
        print("Best bird saved to best_bird.pkl")
    
    return winner

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "utils", "config-feedforward.txt")
    run(config_path)