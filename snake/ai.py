import random
from collections import deque

import torch
from torch import nn
from torch import optim

try:
    from .game_logic import Grid, Game, Coord
except ImportError:
    from game_logic import Grid, Game, Coord


class SnakeNN(nn.Module):

    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        super(SnakeNN, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


class SnakeAI:

    def __init__(self, game_grid: Grid):
        self.grid = game_grid
        self.game = Game(game_grid)
        self.memory = deque(maxlen=1000)
        self.batch_size = 64
        self.gamma = 0.9  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.state_size = 8  # food direction and danger of self collision in all 4 directions
        self.action_size = 4  # up, down, left, right
        self.model = SnakeNN(self.state_size, 24, self.action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    def get_state(self):
        head = self.game.snake.positions[0]

        # Distance to food
        food_direction = [
            1 if self.game.food.y < head.y else 0,  # food up
            1 if self.game.food.y > head.y else 0,  # food down
            1 if self.game.food.x < head.x else 0,  # food left
            1 if self.game.food.x > head.x else 0,  # food right
        ]

        # Danger of collision
        danger = [
            Coord(head.x, head.y - 1) in self.game.snake.positions[1:],  # up
            Coord(head.x, head.y + 1) in self.game.snake.positions[1:],  # down
            Coord(head.x - 1, head.y) in self.game.snake.positions[1:],  # left
            Coord(head.x + 1, head.y) in self.game.snake.positions[1:],  # right
        ]

        state = food_direction + danger
        return torch.FloatTensor(state)

    def get_action(self, state):

        if random.random() <= self.epsilon:
            return random.randint(0, 3)

        with torch.no_grad():
            q_values = self.model(state)
            return torch.argmax(q_values).item()

    def train(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        states = torch.stack([x[0] for x in batch])
        actions = torch.tensor([x[1] for x in batch])
        rewards = torch.tensor([x[2] for x in batch], dtype=torch.float32)
        next_states = torch.stack([x[3] for x in batch])
        is_terminal = torch.tensor([x[4] for x in batch], dtype=torch.float32)

        current_q = self.model(states).gather(1, actions.unsqueeze(1))
        next_q = self.model(next_states).max(1)[0].detach()
        target_q = rewards + (1 - is_terminal) * self.gamma * next_q

        loss = self.criterion(current_q.squeeze(), target_q)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update(self):
        state = self.get_state()
        action = self.get_action(state)
        old_score = self.game.score

        self.game.snake.change_direction(int(action))
        self.game.update()

        reward = 0
        if self.game.game_over:
            reward = -100
        elif self.game.score > old_score:
            reward = 10

        next_state = self.get_state()
        self.train(state, action, reward, next_state, self.game.game_over)

        if self.game.game_over:
            self.game.start_new_game()
