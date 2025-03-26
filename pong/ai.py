import os
import sys
import time
import pickle

import neat
import pygame

try:
    from logic import Game
    from game import draw_game, draw_net, draw_scores, draw_hits
    from constants import SCREEN_WIDTH, SCREEN_HEIGHT
except ImportError:
    from .logic import Game
    from .game import draw_game, draw_net, draw_scores, draw_hits
    from .constants import SCREEN_WIDTH, SCREEN_HEIGHT

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from globals import BLACK

BEST_PICKLE = "pong/best.pickle"
CHECKPOINT_DIR = "pong/checkpoints/"
DRAW_TRAINING = False


class PongAi:

    def __init__(self, window: pygame.Surface, width: int, height: int):
        self.genome1: neat.genome.DefaultGenome
        self.genome2: neat.genome.DefaultGenome
        self.game = Game(width, height)
        self.window = window

    def test_ai(self, net: neat.nn.FeedForwardNetwork):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)
            self.game.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        break

            output = net.activate((self.game.paddleR.y, abs(self.game.paddleR.x - self.game.ball.x), self.game.ball.y))
            decision = output.index(max(output))

            if decision == 1:  # AI moves up
                self.game.move_right_paddle_up()
            elif decision == 2:  # AI moves down
                self.game.move_right_paddle_down()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_left_paddle_up()
            elif keys[pygame.K_s]:
                self.game.move_left_paddle_down()

            self.window.fill(BLACK)
            draw_scores(self.window, self.game)
            draw_net(self.window, self.game)
            draw_hits(self.window, self.game)
            draw_game(self.window, self.game)
            pygame.display.flip()

    def train_ai(self, genome1: neat.genome.DefaultGenome, genome2: neat.genome.DefaultGenome, neat_config: neat.Config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, neat_config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, neat_config)
        self.genome1 = genome1
        self.genome2 = genome2
        start_time = time.time()
        run = True
        max_hits = 50

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        break

            self.game.update()
            self._move_ai_paddles(net1, net2)

            if DRAW_TRAINING:
                self.window.fill(BLACK)
                draw_scores(self.window, self.game)
                draw_net(self.window, self.game)
                draw_hits(self.window, self.game)
                draw_game(self.window, self.game)
                pygame.display.flip()

            duration = time.time() - start_time
            if self.game.score_left == 1 or self.game.score_right == 1 or self.game.hits_left >= max_hits:
                self._calculate_fitness(duration)
                break

    def _calculate_fitness(self, duration: float):
        self.genome1.fitness += self.game.hits_left + duration
        self.genome2.fitness += self.game.hits_right + duration

    def _move_ai_paddles(self, net1: neat.nn.FeedForwardNetwork, net2: neat.nn.FeedForwardNetwork):
        players = [(self.genome1, net1, self.game.paddleL, True), (self.genome2, net2, self.game.paddleR, False)]

        for genome, net, paddle, left in players:
            output = net.activate((paddle.y, abs(paddle.x - self.game.ball.x), self.game.ball.y))
            decision = output.index(max(output))

            valid = True
            if decision == 0:  # Don't move
                genome.fitness -= 0.01  # we want to discourage this
            elif decision == 1:  # Move up
                if left:
                    valid = self.game.move_left_paddle_up()
                else:
                    valid = self.game.move_right_paddle_up()
            else:  # Move down
                if left:
                    valid = self.game.move_left_paddle_down()
                else:
                    valid = self.game.move_right_paddle_down()

            if not valid:  # If the movement makes the paddle go off the screen punish the AI
                genome.fitness -= 1


def eval_genomes(genomes: list[tuple[int, neat.genome.DefaultGenome]], neat_config: neat.Config):
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    for i, (_, genome1) in enumerate(genomes):
        print(f"Progress: {round(i / len(genomes) * 100)}%", end="\r", flush=True)
        genome1.fitness = 0
        for _, genome2 in genomes[min(i + 1, len(genomes) - 1) :]:
            genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
            pong = PongAi(win, SCREEN_WIDTH, SCREEN_HEIGHT)
            pong.train_ai(genome1, genome2, neat_config)


def run_neat(num_generations: int, neat_config: neat.Config, checkpoint_dir=CHECKPOINT_DIR, checkpoint: str | None = None):
    if checkpoint:
        p = neat.Checkpointer.restore_checkpoint(os.path.join(checkpoint_dir, checkpoint))
    else:
        p = neat.Population(neat_config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1, filename_prefix=f"{CHECKPOINT_DIR}neat-checkpoint-"))
    winner = p.run(eval_genomes, num_generations)

    with open(BEST_PICKLE, "wb") as f:
        pickle.dump(winner, f)


def test_best_network(neat_config: neat.Config):
    with open(BEST_PICKLE, "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, neat_config)
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pong = PongAi(win, SCREEN_WIDTH, SCREEN_HEIGHT)
    pong.test_ai(winner_net)


if __name__ == "__main__":

    if not os.path.isdir(CHECKPOINT_DIR):
        os.makedirs(CHECKPOINT_DIR)

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    checkpoints = os.listdir(CHECKPOINT_DIR)
    last_checkpoint = max(checkpoints, key=lambda x: int(x.split("-")[-1]))
    print(last_checkpoint)

    pygame.display.set_caption("Ai Pong")

    run_neat(5, config, checkpoint=last_checkpoint)
    test_best_network(config)

    pygame.quit()
