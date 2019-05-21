import random as rd
import numpy as np
import copy
from keras.models import Sequential
from keras.layers import Dense

from sim.heroes import Team, Hero
from sim.processing import Game

heroes = [Hero.__dict__[key] for key in Hero.__dict__ if '__' not in key and 'empty' not in key]
ranks = [32, 23, 18, 20, 7, 5,
         38, 4, 33, 19, 11, 29, 2,
         9, 3, 37, 8, 40, 31,
         13, 21, 17, 41, 24, 27,
         35, 39, 25, 22, 6, 16,
         26, 14, 1, 15, 12, 36,
         34, 28, 30, 10]
n_heroes = len(heroes)


def get_random_team():
    return Team([rd.choice(heroes)() for _ in range(6)])


model = Sequential()
model.add(Dense(32, input_dim=6 * n_heroes, activation='sigmoid'))
model.add(Dense(n_heroes, activation='sigmoid'))
model.compile(loss='mse', optimizer='adam', metrics=['mae'])


def get_next_hero(model, eps, state, actions):
    if rd.random() < eps:
        a = rd.randint(0, n_heroes - 1)
        while a in actions:
            a = rd.randint(0, n_heroes - 1)
    else:
        scores = model.predict(state)[0]
        scores[actions] = 0
        a = np.argmax(scores)

    return a


def train_model(model, n_battles=10000, mode='vs_self', eps=0.5, decay=0.9998):
    scores = []
    for i in range(n_battles):
        actions = []
        op_actions = []
        state = np.zeros((1, 6 * n_heroes))
        op_state = np.zeros((1, 6 * n_heroes))
        eps *= decay
        if i % 100 == 0:
            print("Battle {} of {}".format(i + 1, n_battles))

        for turn in range(6):
            a = get_next_hero(model, eps, state, actions)
            op_a = get_next_hero(model, eps, op_state, op_actions)
            actions.append(a)
            op_actions.append(op_a)

            if turn < 5:
                new_state = copy.copy(state)
                new_state[0][n_heroes * turn + a] = 1
                new_op_state = copy.copy(op_state)
                new_op_state[0][n_heroes * turn + op_a] = 1
                target = np.max(np.delete(model.predict(new_state)[0], actions))
                op_target = np.max(np.delete(model.predict(new_op_state)[0], op_actions))

            else:
                team = Team([heroes[a]() for a in actions])
                if mode == 'vs_self':
                    op_team = Team([heroes[op_a]() for op_a in op_actions])
                elif mode == 'vs_random':
                    op_team = get_random_team()
                else:
                    raise Warning('Unknown training mode')
                game = Game(team, op_team)
                game.process()
                target = (game.winner + 1) / 2
                op_target = 1 - target

            target_vec = model.predict(state)[0]
            target_vec[actions[-1]] = target
            model.fit(state, target_vec.reshape((1, n_heroes)), epochs=1, verbose=0)

            if mode == 'vs_self':
                op_target_vec = model.predict(op_state)[0]
                op_target_vec[op_actions[-1]] = op_target
                model.fit(op_state, op_target_vec.reshape((1, n_heroes)), epochs=1, verbose=0)

            state = new_state
            op_state = new_op_state

        scores.append(sum([ranks[a] for a in actions + op_actions]))

    return scores


def get_prediction(model):
    actions = []
    state = np.zeros((1, 6 * n_heroes))
    for turn in range(6):
        scores = model.predict(state)[0]
        scores[actions] = 0
        a = np.argmax(scores)
        actions.append(a)
        state[0][n_heroes * turn + a] = 1

    return Team([heroes[a]() for a in actions])
