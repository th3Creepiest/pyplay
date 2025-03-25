# 🕹️ Pong Game Objects

from dataclasses import dataclass


@dataclass
class Game:
    WINNING_SCORE = 3
    GAME_OVER = False

    def __init__(self, width: int, height: int):
        self.game_area = GameArea(width, height)
        self.score_left = 0
        self.score_right = 0
        self.hits_left = 0
        self.hits_right = 0

        paddle_width = self.game_area.width * 0.018
        paddle_height = self.game_area.height * 0.18
        ball_radius = self.game_area.width * 0.012

        self.paddleL = Paddle(
            x=self.game_area.width * 0.05,
            y=self.game_area.height // 2 - paddle_height // 2,
            width=paddle_width,
            height=paddle_height,
        )

        self.paddleR = Paddle(
            x=self.game_area.width - paddle_width - self.game_area.width * 0.05,
            y=self.game_area.height // 2 - paddle_height // 2,
            width=paddle_width,
            height=paddle_height,
        )

        self.ball = Ball(
            x=(self.game_area.width // 2),
            y=(self.game_area.height // 2),
            radius=ball_radius,
        )

    def update(self):
        self.ball.move()
        self.handle_collisions()
        self.check_goal()
        self.check_game_over()

    def reset(self):
        self.reset_ball()
        self.reset_paddles()
        self.GAME_OVER = False
        self.score_left = 0
        self.score_right = 0
        self.hits_left = 0
        self.hits_right = 0

    def move_right_paddle_up(self):
        if self.paddleR.y - self.paddleR.VELOCITY >= 0:
            self.paddleR.move_up()

    def move_right_paddle_down(self):
        if self.paddleR.y + self.paddleR.VELOCITY <= self.game_area.height - self.paddleR.height:
            self.paddleR.move_down()

    def move_left_paddle_up(self):
        if self.paddleL.y - self.paddleL.VELOCITY >= 0:
            self.paddleL.move_up()

    def move_left_paddle_down(self):
        if self.paddleL.y + self.paddleL.VELOCITY <= self.game_area.height - self.paddleL.height:
            self.paddleL.move_down()

    def check_goal(self):
        if self.ball.x < 0:
            self.score_right += 1
            self.reset_ball()
        elif self.ball.x > self.game_area.width:
            self.score_left += 1
            self.reset_ball()

    def reset_ball(self):
        self.ball.x = self.game_area.width // 2
        self.ball.y = self.game_area.height // 2
        self.ball.y_velocity = 0
        self.ball.x_velocity *= -1

    def reset_paddles(self):
        self.paddleL.x = self.game_area.width * 0.05
        self.paddleL.y = self.game_area.height // 2 - self.paddleL.height // 2
        self.paddleR.x = self.game_area.width - self.paddleR.width - self.game_area.width * 0.05
        self.paddleR.y = self.game_area.height // 2 - self.paddleR.height // 2

    def check_game_over(self):
        if self.score_left >= self.WINNING_SCORE or self.score_right >= self.WINNING_SCORE:
            self.GAME_OVER = True

    def handle_collisions(self):

        if self.ball.y + self.ball.radius >= self.game_area.height:
            self.ball.y_velocity *= -1

        if self.ball.y - self.ball.radius <= 0:
            self.ball.y_velocity *= -1

        if self.ball.x_velocity < 0:
            if self.ball.y >= self.paddleL.y and self.ball.y <= self.paddleL.y + self.paddleL.height:
                if self.ball.x - self.ball.radius <= self.paddleL.x + self.paddleL.width:
                    self.ball.x_velocity *= -1
                    self.hits_left += 1

                    # Adjust ball velocity based on paddle position
                    middle_y = self.paddleL.y + self.paddleL.height / 2
                    y_difference = middle_y - self.ball.y
                    reduction_factor = (self.paddleL.height / 2) / self.ball.MAX_VELOCITY
                    self.ball.y_velocity = (y_difference / reduction_factor) * -1

        if self.ball.x_velocity > 0:
            if self.ball.y >= self.paddleR.y and self.ball.y <= self.paddleR.y + self.paddleR.height:
                if self.ball.x + self.ball.radius >= self.paddleR.x:
                    self.ball.x_velocity *= -1
                    self.hits_right += 1

                    # Adjust ball velocity based on paddle position
                    middle_y = self.paddleR.y + self.paddleR.height / 2
                    y_difference = middle_y - self.ball.y
                    reduction_factor = (self.paddleR.height / 2) / self.ball.MAX_VELOCITY
                    self.ball.y_velocity = (y_difference / reduction_factor) * -1


@dataclass
class GameArea:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height


@dataclass
class Paddle:
    VELOCITY = 5

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def move_up(self):
        self.y -= self.VELOCITY

    def move_down(self):
        self.y += self.VELOCITY


@dataclass
class Ball:
    MAX_VELOCITY = 5

    def __init__(self, x: int, y: int, radius: int):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
