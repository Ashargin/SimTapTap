import numpy as np
import random as rd
import copy


class Sim:
    def __init__(self, team_1, team_2, n_sim=1000):
        self.team_1 = team_1
        self.team_2 = team_2
        self.wins = 0
        self.n_sim = n_sim

    def process(self):
        for i in range(self.n_sim):
            game = Game(self.team_1, self.team_2)
            game.process()
            winner = game.winner
            if winner == 0:
                self.wins += 1

    def print_winrate(self):
        print('Team 1 winrate : {}%'.format(100 * self.wins / self.n_sim))


class Game:
    def __init__(self, team_1, team_2):
        self.log = ''
        self.team_1 = copy.deepcopy(team_1) # deepcopies?
        self.team_2 = copy.deepcopy(team_2)
        for h in self.team_1.heroes:
            h.op_team = self.team_2
            h.str_id = '{}_{}_{}'.format(h.name.value, 1, h.pos + 1)
        for h in self.team_2.heroes:
            h.op_team = self.team_1
            h.str_id = '{}_{}_{}'.format(h.name.value, 2, h.pos + 1)
        self.heroes = self.team_1.heroes + self.team_2.heroes
        for h in self.heroes:
            h.game = self

    def turn(self):
        self.log += '\n### Turn {} ###'.format(self.round)

        for h in self.heroes:
            if not h.is_dead:
                h.can_attack = True
            for e in h.effects:
                e.tick()

        while any([h.can_attack for h in self.heroes]) and not self.is_finished():
            max_speed = max([h.speed for h in self.heroes if h.can_attack])
            fastest_heroes = [h for h in self.heroes if h.speed == max_speed and h.can_attack]
            fastest = fastest_heroes[rd.randint(0, len(fastest_heroes) - 1)]
            self.log += "\n\n# {}'s turn #".format(fastest.str_id)
            fastest.turn()

        self.log += '\n\n{}\n'.format(self.state())

    def state(self):
        team_1_hps = np.array([[self.team_1.heroes[3].hp, self.team_1.heroes[4].hp, self.team_1.heroes[5].hp], 
                        [self.team_1.heroes[0].hp, self.team_1.heroes[1].hp, self.team_1.heroes[2].hp]]).astype(int)
        team_2_hps = np.array([[self.team_2.heroes[0].hp, self.team_2.heroes[1].hp, self.team_2.heroes[2].hp], 
                        [self.team_2.heroes[3].hp, self.team_2.heroes[4].hp, self.team_2.heroes[5].hp]]).astype(int)
        return '{}\n{}'.format(str(team_1_hps), str(team_2_hps))

    def print_state(self):
        print(np.array([[self.team_1.heroes[3].hp, self.team_1.heroes[4].hp, self.team_1.heroes[5].hp], 
                        [self.team_1.heroes[0].hp, self.team_1.heroes[1].hp, self.team_1.heroes[2].hp]]).astype(int))
        print(np.array([[self.team_2.heroes[0].hp, self.team_2.heroes[1].hp, self.team_2.heroes[2].hp], 
                        [self.team_2.heroes[3].hp, self.team_2.heroes[4].hp, self.team_2.heroes[5].hp]]).astype(int))

    def is_finished(self):
        return True if self.team_1.is_dead() or self.team_2.is_dead() or self.round > 15 else False

    def process(self):
        self.round = 1
        while not self.is_finished():
            self.turn()
            self.round += 1

        self.log += '\n### Final state ###\n'
        self.log += '\n\n{}'.format(self.state())

        if self.team_2.is_dead() and not self.team_1.is_dead():
            self.winner = 0
        else:
            self.winner = 1

        self.log += '\n\nWinner : team {}'.format(self.winner + 1)
