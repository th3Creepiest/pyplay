import os
import sys
import pickle

import neat
import pygame

try:
    from .game_objects import Bird, Pipe, Base, BackGround
    from .constants import WINDOW_WIDTH, WINDOW_HEIGHT, LOCAL_DIR, BEST_PICKLE
except ImportError:
    from game_objects import Bird, Pipe, Base, BackGround
    from constants import WINDOW_WIDTH, WINDOW_HEIGHT, LOCAL_DIR, BEST_PICKLE


FLOOR = 730
DRAW_LINES = False

gen = 0


def eval_genomes(genomes, config):
    """
    runs the simulation of the current population of
    birds and sets their fitness based on the distance they
    reach in the game.
    """
    global gen
    gen += 1

    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    birds = []
    ge = []
    for _, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(genome)

    base = Base(FLOOR)
    pipes = [Pipe(700)]
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(birds) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].img_top.get_width():  # determine whether to use the first or second
                pipe_ind = 1  # pipe on the screen for neural network input

        for x, bird in enumerate(birds):  # give each bird a fitness of 0.1 for each frame it stays alive
            ge[x].fitness += 0.1
            bird.move()

            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                bird.jump()

        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # check for collision
            for bird in birds:
                if pipe.collide(bird):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.x + pipe.img_top.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            # can add this line to give more reward for passing through a pipe (not required)
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe(WINDOW_WIDTH))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        draw_window(win, birds, pipes, base, score, gen, pipe_ind)

        # # break if score gets large enough
        # if score > 20:
        #     with open(BEST_PICKLE, "wb") as f:
        #         pickle.dump(nets[0], f)
        #     break


def draw_window(window, birds, pipes, base, score, generation, pipe_ind):
    """
    draws the windows for the main game loop
    :param window: pygame window surface
    :param birds: a list of Bird objects
    :param pipes: List of pipes
    :param score: score of the game (int)
    :param gen: current generation
    :param pipe_ind: index of closest pipe
    :return: None
    """
    if generation == 0:
        generation = 1

    BackGround().draw(window)

    for pipe in pipes:
        pipe.draw(window)

    base.draw(window)
    for bird in birds:
        # draw lines from bird to pipe
        if DRAW_LINES:
            try:
                pygame.draw.line(window, (255, 0, 0), (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2), (pipes[pipe_ind].x + pipes[pipe_ind].img_top.get_width() / 2, pipes[pipe_ind].height), 5)
                pygame.draw.line(window, (255, 0, 0), (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2), (pipes[pipe_ind].x + pipes[pipe_ind].img_bot.get_width() / 2, pipes[pipe_ind].bottom), 5)
            except IndexError:
                pass

        # draw bird
        bird.draw(window)

    stat_font = pygame.font.SysFont("comicsans", 50)

    # score
    score_label = stat_font.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(score_label, (WINDOW_WIDTH - score_label.get_width() - 15, 10))

    # generations
    score_label = stat_font.render("Gens: " + str(generation - 1), 1, (255, 255, 255))
    window.blit(score_label, (10, 10))

    # alive
    score_label = stat_font.render("Alive: " + str(len(birds)), 1, (255, 255, 255))
    window.blit(score_label, (10, 50))

    pygame.display.update()


def run_neat(
    fitness_func: callable,
    num_generations: int,
    neat_config: str = os.path.join(LOCAL_DIR, "config.txt"),
    save: bool = False,
):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, neat_config)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(fitness_func, num_generations)

    if save:
        with open(BEST_PICKLE, "wb") as f:
            pickle.dump(winner, f)


if __name__ == "__main__":
    pygame.init()
    run_neat(eval_genomes, 50)
    pygame.quit()
