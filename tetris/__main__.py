import sys
import random
import pygame

try:
    from .game_objects import Piece
    from .constants import (
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        PLAY_WIDTH,
        PLAY_HEIGHT,
        BLOCK_SIZE,
        TOP_LEFT_X,
        TOP_LEFT_Y,
        SHAPES,
        COLORS,
        BLACK,
        WHITE,
        GREY,
        RED,
    )
except ImportError:
    from game_objects import Piece
    from constants import (
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        PLAY_WIDTH,
        PLAY_HEIGHT,
        BLOCK_SIZE,
        TOP_LEFT_X,
        TOP_LEFT_Y,
        SHAPES,
        COLORS,
        BLACK,
        WHITE,
        GREY,
        RED,
    )


def main():
    pygame.display.set_caption("Tetris")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    paused = False
    grid = create_grid()
    current_piece = new_piece()
    next_piece = new_piece()
    fall_time = 0
    fall_speed = 0.5  # Starting speed
    level_time = 0  # Time since last level increase
    score = 0
    level = 1
    high_score = 0
    locked_positions = {}

    # Variables for continuous key movement
    key_left_pressed = False
    key_right_pressed = False
    key_down_pressed = False
    key_repeat_delay = 250  # milliseconds before key repeats
    key_repeat_interval = 100  # milliseconds between repeats
    left_time = 0
    right_time = 0
    down_time = 0

    while run:
        grid = create_grid(locked_positions)
        lines_cleared = clear_rows(grid, locked_positions)

        if lines_cleared > 0:
            score += (lines_cleared * 100) * (lines_cleared)

            if score > high_score:
                high_score = score

            grid = create_grid(locked_positions)

        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()

        # Update key timers
        if key_left_pressed:
            left_time += clock.get_rawtime()
        if key_right_pressed:
            right_time += clock.get_rawtime()
        if key_down_pressed:
            down_time += clock.get_rawtime()

        clock.tick()

        # Process events regardless of pause state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Key press events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        draw_text_middle(screen, "PAUSED", WHITE)
                        pygame.display.update()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_h:
                    if not paused:
                        current_piece.move_left()
                        if not valid_space(current_piece, grid):
                            current_piece.move_right()
                        key_left_pressed = True
                        left_time = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_l:
                    if not paused:
                        current_piece.move_right()
                        if not valid_space(current_piece, grid):
                            current_piece.move_left()
                        key_right_pressed = True
                        right_time = 0
                elif event.key == pygame.K_DOWN:
                    if not paused:
                        current_piece.move_down()
                        if not valid_space(current_piece, grid):
                            current_piece.y -= 1
                        key_down_pressed = True
                        down_time = 0
                elif event.key == pygame.K_UP:
                    if not paused:
                        current_piece.rotate()
                        if not valid_space(current_piece, grid):
                            for _ in range(3):
                                current_piece.rotate()
                elif event.key == pygame.K_SPACE:
                    if not paused:
                        if instant_drop(current_piece, grid):
                            shape = current_piece.get_shape()
                            for i, row in enumerate(shape):
                                for j, cell in enumerate(row):
                                    if cell:
                                        locked_positions[(current_piece.x + j, current_piece.y + i)] = current_piece.color

                            current_piece = next_piece
                            next_piece = new_piece()

                            if not valid_space(current_piece, grid):
                                run = False
                                draw_text_middle(screen, "GAME OVER!", RED)
                                pygame.display.update()
                                pygame.time.delay(1500)

            # Key release events
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_h):
                    key_left_pressed = False
                elif event.key in (pygame.K_RIGHT, pygame.K_l):
                    key_right_pressed = False
                elif event.key == pygame.K_DOWN:
                    key_down_pressed = False

        if paused:
            screen.fill(BLACK)
            draw_grid(screen, grid)
            draw_piece(screen, current_piece)
            draw_next_piece(screen, next_piece)
            draw_score(screen, score, level, high_score)
            draw_text_middle(screen, "PAUSED", WHITE)
            pygame.display.update()
            continue

        # Handle continuous key movement
        if key_left_pressed and left_time > key_repeat_delay:
            left_time = key_repeat_interval
            current_piece.move_left()
            if not valid_space(current_piece, grid):
                current_piece.move_right()

        if key_right_pressed and right_time > key_repeat_delay:
            right_time = key_repeat_interval
            current_piece.move_right()
            if not valid_space(current_piece, grid):
                current_piece.move_left()

        if key_down_pressed and down_time > key_repeat_delay:
            down_time = key_repeat_interval
            current_piece.move_down()
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                # Handle piece landing from fast drop
                shape = current_piece.get_shape()
                for i, row in enumerate(shape):
                    for j, cell in enumerate(row):
                        if cell:
                            locked_positions[(current_piece.x + j, current_piece.y + i)] = current_piece.color

                current_piece = next_piece
                next_piece = new_piece()
                key_down_pressed = False

                if not valid_space(current_piece, grid):
                    run = False
                    show_game_over(screen)

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.move_down()
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                shape = current_piece.get_shape()
                for i, row in enumerate(shape):
                    for j, cell in enumerate(row):
                        if cell:
                            locked_positions[(current_piece.x + j, current_piece.y + i)] = current_piece.color

                current_piece = next_piece
                next_piece = new_piece()
                if not valid_space(current_piece, grid):
                    run = False
                    show_game_over(screen)

        # Increase level and speed every 30 seconds
        if level_time / 1000 > 30:
            level_time = 0
            if fall_speed > 0.15:  # Don't make it too fast
                fall_speed -= 0.05
                level += 1

        screen.fill(BLACK)

        # Draw play area border
        pygame.draw.rect(screen, GREY, (TOP_LEFT_X - 5, TOP_LEFT_Y - 5, PLAY_WIDTH + 10, PLAY_HEIGHT + 10), 5)

        draw_grid(screen, grid)
        draw_piece(screen, current_piece)
        draw_next_piece(screen, next_piece)
        draw_score(screen, score, level, high_score)

        pygame.display.update()


def new_piece():
    shape_index = random.randint(0, len(SHAPES) - 1)
    return Piece(SHAPES[shape_index], COLORS[shape_index])


def create_grid(locked_positions=None):
    if locked_positions is None:
        locked_positions = {}

    grid = [[BLACK for _ in range(10)] for _ in range(20)]

    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]

    return grid


def draw_grid(surface, grid):
    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # Draw grid lines
    for i in range(len(grid) + 1):
        pygame.draw.line(surface, WHITE, (TOP_LEFT_X, TOP_LEFT_Y + i * BLOCK_SIZE), (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + i * BLOCK_SIZE))

    for j in range(len(grid[0]) + 1):
        pygame.draw.line(surface, WHITE, (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y), (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))


def draw_piece(surface, piece):
    shape = piece.get_shape()
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, piece.color, (TOP_LEFT_X + (piece.x + j) * BLOCK_SIZE, TOP_LEFT_Y + (piece.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)


def valid_space(piece, grid):
    shape = piece.get_shape()

    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                x = piece.x + j
                y = piece.y + i
                if x < 0 or x >= 10 or y >= 20 or (y >= 0 and grid[y][x] != BLACK):
                    return False
    return True


def clear_rows(grid, locked):
    cleared = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            cleared += 1

            # Remove the row
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except KeyError:
                    continue

            # Shift every row above down one
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < i:
                    new_key = (x, y + 1)
                    locked[new_key] = locked.pop(key)

    return cleared


def draw_text_middle(surface, text, color):
    FONT_60_CS = pygame.font.SysFont("comicsans", 60, bold=True)
    label = FONT_60_CS.render(text, 1, color)
    surface.blit(label, (SCREEN_WIDTH / 2 - (label.get_width() / 2), SCREEN_HEIGHT / 2 - (label.get_height() / 2)))


def draw_score(surface, score, level, high_score=0):
    FONT_28_CS = pygame.font.SysFont("comicsans", 28)
    label_score = FONT_28_CS.render(f"Score: {score}", 1, WHITE)
    label_level = FONT_28_CS.render(f"Level: {level}", 1, WHITE)
    label_high_score = FONT_28_CS.render(f"High Score: {high_score}", 1, WHITE)

    # Position for score display - left side of the screen
    score_x = 30
    surface.blit(label_score, (score_x, 50))
    surface.blit(label_level, (score_x, 80))
    surface.blit(label_high_score, (score_x, 110))


def draw_next_piece(surface, piece):
    preview_x = SCREEN_WIDTH - 180
    preview_y = 100
    preview_box_size = 150

    # Draw the preview box
    pygame.draw.rect(surface, GREY, (preview_x - 10, preview_y - 10, preview_box_size, preview_box_size), 1)

    # Calculate the size of the piece
    shape = piece.get_shape()
    piece_height = len(shape)
    piece_width = len(shape[0]) if piece_height > 0 else 0

    # Calculate offsets to center the piece in the preview box
    offset_x = (preview_box_size - piece_width * BLOCK_SIZE) // 2
    offset_y = (preview_box_size - piece_height * BLOCK_SIZE) // 2

    # Draw the next piece
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, piece.color, (preview_x + offset_x + j * BLOCK_SIZE, preview_y + offset_y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)


def instant_drop(piece, grid):
    """Move the piece down until it hits something"""
    while valid_space(piece, grid):
        piece.y += 1
    piece.y -= 1  # Move back up one step since we went too far
    return True  # Return True to indicate the piece has landed


def show_game_over(screen: pygame.Surface):
    draw_text_middle(screen, "GAME OVER!", RED)
    pygame.display.update()
    pygame.time.delay(1500)


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
