# 🕹️ Pong Game

import sys
import pygame


TITLE = "Pong"
FPS = 60
BALL_SIZE = 20
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def main():

    # Initialize Pygame
    pygame.init()

    # Screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)

    # Paddle positions
    player_paddle = pygame.Rect(50, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    computer_paddle = pygame.Rect(WINDOW_WIDTH - 50 - PADDLE_WIDTH, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    # Ball position and velocity
    ball = pygame.Rect(WINDOW_WIDTH // 2 - BALL_SIZE // 2, WINDOW_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
    ball_velocity = [5, 5]

    # Clock
    clock = pygame.time.Clock()

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_paddle.top > 0:
            player_paddle.y -= 5
        if keys[pygame.K_DOWN] and player_paddle.bottom < WINDOW_HEIGHT:
            player_paddle.y += 5

        # Computer paddle movement
        if computer_paddle.centery < ball.centery:
            computer_paddle.y += 4
        elif computer_paddle.centery > ball.centery:
            computer_paddle.y -= 4

        # Ball movement
        ball.x += ball_velocity[0]
        ball.y += ball_velocity[1]

        # Ball collision with walls
        if ball.top <= 0 or ball.bottom >= WINDOW_HEIGHT:
            ball_velocity[1] = -ball_velocity[1]

        # Ball collision with paddles
        if ball.colliderect(player_paddle) or ball.colliderect(computer_paddle):
            ball_velocity[0] = -ball_velocity[0]

        # Ball out of bounds
        if ball.left <= 0 or ball.right >= WINDOW_WIDTH:
            ball.x, ball.y = WINDOW_WIDTH // 2 - BALL_SIZE // 2, WINDOW_HEIGHT // 2 - BALL_SIZE // 2

        # Clear screen
        screen.fill(BLACK)

        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, player_paddle)
        pygame.draw.rect(screen, WHITE, computer_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)


if __name__ == "__main__":
    main()
