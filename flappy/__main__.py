import os
import sys
import logging
import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from globals import BLACK, FONT_50, FONT_40, GREEN, GRAY

try:
    from .ai import run_neat, eval_genomes
    from .game_objects import Bird, Pipe, Base, BackGround
    from .constants import WINDOW_WIDTH, WINDOW_HEIGHT
except ImportError:
    from ai import run_neat, eval_genomes
    from game_objects import Bird, Pipe, Base, BackGround
    from constants import WINDOW_WIDTH, WINDOW_HEIGHT


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main():
    logging.info("launching flappy game")
    pygame.display.set_caption("Flappy")
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen = pygame.display.get_surface()
    display_menu(screen)


def display_menu(screen: pygame.Surface):
    logging.info("displaying menu screen")
    clock = pygame.time.Clock()

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_a:
                    run_neat(eval_genomes, 50)
                elif event.key == pygame.K_h:
                    run_human_game(screen)

        screen.fill(BLACK)

        title = FONT_50.render("Flappy", True, GREEN)
        human_text = FONT_40.render("Press H for Human Player", True, GRAY)
        ai_text = FONT_40.render("Press A for AI Player", True, GRAY)

        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        human_rect = human_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        ai_rect = ai_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

        screen.blit(title, title_rect)
        screen.blit(human_text, human_rect)
        screen.blit(ai_text, ai_rect)

        pygame.display.flip()


def run_human_game(screen: pygame.Surface):
    print("run_human_game")
    bird = Bird(230, 350)
    pipes = [Pipe(700)]
    base = Base(730)
    bg = BackGround()
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
                if event.key == pygame.K_SPACE:
                    bird.jump()

        screen.fill((0, 0, 0))

        bg.draw(screen)

        bird.move()
        bird.draw(screen)

        for pipe in pipes:
            pipe.move()
            pipe.draw(screen)

        base.move()
        base.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()
