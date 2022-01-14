from numpy.random.mtrand import gamma, rand
import torch
import random
import numpy as np
from collections import deque
from level import Level
from main import Game
from player import *
from model import Linear_QNet, QTrainer
from helper import plot

max_memory = 100_000
batch_size = 1000
learning_rate = 0.001

class Agent:
    def __init__(self):
        self.number_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=max_memory)
        self.model = Linear_QNet(10, 256, 3)
        self.trainer = QTrainer(self.model, lr=learning_rate, gamma=self.gamma)

    def get_state(self, game):
        player = game.level.player.sprite
        down = player.rect.y + 30
        left = player.rect.x - 30
        right = player.rect.x + 30

        direction_left = player.direction == Direction.Left
        direction_right = player.direction == Direction.Right
        direction_jump = player.direction == Direction.Jump

        state = [
            (direction_left and game.level.check_death(down) == False) or
            (direction_right and game.level.check_death(down) == False),

            (direction_left and game.out_of_bounds(left) == False) or
            (direction_right and game.out_of_bounds(left) == False),

            (direction_left and game.out_of_bounds(right) == False) or
            (direction_right and game.out_of_bounds(right) == False),

            direction_left,
            direction_right,
            direction_jump,

            player.rect.y < game.level.closest_tile().y,
            player.rect.y > game.level.closest_tile().y,
            player.rect.x < game.level.closest_tile().x,
            player.rect.x > game.level.closest_tile().x,
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > batch_size:
            mini_sample = random.sample(self.memory, batch_size)
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.number_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Game()
    while True:
        state_old = agent.get_state(game)

        final_move = agent.get_action(state_old)

        reward, done, score = game.runGame(final_move)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.level.reset()
            agent.number_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game:', agent.number_games, 'Score:', score, 'Record:', record)

            # plot_scores.append(score)
            # total_score += score
            # mean_score = total_score / agent.number_games
            # plot_mean_scores.append(mean_score)
            # plot(plot_scores, plot_mean_scores)
            


if __name__ == '__main__':
    train()