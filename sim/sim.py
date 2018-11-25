import numpy as np
import random as rd
import copy


class Sim:
    def __init__(self, attack_team, defense_team, n_sim=1000):
        self.attack_team = attack_team
        self.defense_team = defense_team
        self.wins_1 = 0
        self.wins_2 = 0
        self.ties = 0
        self.n_sim = n_sim

    def process(self):
        for i in range(self.n_sim):
            game = Game(self.attack_team, self.defense_team)
            game.process()
            winner = game.winner
            if winner == 1:
                self.wins_1 += 1
            elif winner == -1:
                self.wins_2 += 1
            else:
                self.ties += 1

    def print_winrate(self):
        print('Attacker winrate : {}%'.format(100 * self.wins_1 / self.n_sim))
        print('Defender winrate : {}%'.format(100 * (self.wins_2 + self.ties) / self.n_sim))
        print('Including wins by tie : {}%'.format(100 * self.ties / self.n_sim))


class Game:
    def __init__(self, attack_team, defense_team, verbose_full=False):
        self.log = ''
        self.attack_team = copy.deepcopy(attack_team)
        self.defense_team = copy.deepcopy(defense_team)
        self.verbose_full = verbose_full
        for h in self.attack_team.heroes:
            h.op_team = self.defense_team
            h.str_id = '{}_{}_{}'.format(h.name.value, 1, h.pos + 1)
        for h in self.defense_team.heroes:
            h.op_team = self.attack_team
            h.str_id = '{}_{}_{}'.format(h.name.value, 2, h.pos + 1)
        self.attack_team.pet.op_team = self.defense_team
        self.attack_team.pet.str_id = self.attack_team.pet.name + '_1'
        self.defense_team.pet.op_team = self.attack_team
        self.defense_team.pet.str_id = self.defense_team.pet.name + '_2'
        self.heroes = self.attack_team.heroes + self.defense_team.heroes
        self.pets = [self.attack_team.pet, self.defense_team.pet]
        for h in self.heroes:
            h.game = self
        self.attack_team.pet.game = self
        self.defense_team.pet.game = self

        self.log += self.teams() + '\n'

    def turn(self):
        self.log += '\n### Turn {} ###'.format(self.round)

        # effects
        self.log += '\n# Active effects #'.format(self.round)
        for h in self.heroes:
            if not h.is_dead:
                h.can_attack = True
                for e in h.effects:
                    e.tick()

        # heroes
        while any([h.can_attack for h in self.heroes]) and not self.is_finished():
            max_speed = max([h.speed for h in self.heroes if h.can_attack])
            fastest_heroes = [h for h in self.heroes 
                            if h.speed == max_speed and h.can_attack]
            fastest = fastest_heroes[rd.randint(0, len(fastest_heroes) - 1)]
            self.log += "\n\n# {}'s turn #".format(fastest.str_id)
            fastest.turn()

        # familiars
        first_pet = None
        second_pet = None
        if self.pets[0].level == self.pets[1].level:
            choice = rd.randint(0, 1)
            first_pet = self.pets[choice]
            second_pet = self.pets[1 - choice]
        elif self.pets[0].level > self.pets[1].level:
            first_pet = self.pets[0]
            second_pet = self.pets[1]
        else:
            first_pet = self.pets[1]
            second_pet = self.pets[0]
        for pet in (first_pet, second_pet):
            if not self.is_finished():
                if pet.energy == 100:
                    self.log += "\n\n# {}'s turn #".format(pet.str_id)
                pet.turn()

        # effects
        for h in self.heroes:
            if not h.is_dead:
                for e in h.effects:
                    if e.turns == 0:
                        e.kill()

        self.log += '\n\n{}\n'.format(self.state())

    def teams(self):
        teams_str = '### Teams ###'
        len_max_1 = max([len(self.heroes[i].str_id) for i in (0, 3, 6, 9)])
        len_max_2 = max([len(self.heroes[i].str_id) for i in (1, 4, 7, 10)])
        len_max_3 = max([len(self.heroes[i].str_id) for i in (2, 5, 8, 11)])
        teams_str += '\nAttack team  : Backline  : '
        teams_str += '[{}{}, {}{}, {}{}]' \
            .format(self.attack_team.heroes[3].str_id, 
                    ' ' * (len_max_1 - len(self.attack_team.heroes[3].str_id)), 
                    self.attack_team.heroes[4].str_id, 
                    ' ' * (len_max_2 - len(self.attack_team.heroes[4].str_id)), 
                    self.attack_team.heroes[5].str_id, 
                    ' ' * (len_max_3 - len(self.attack_team.heroes[5].str_id)))
        teams_str += '\n               Frontline : '
        teams_str += '[{}{}, {}{}, {}{}]' \
            .format(self.attack_team.heroes[0].str_id, 
                    ' ' * (len_max_1 - len(self.attack_team.heroes[0].str_id)), 
                    self.attack_team.heroes[1].str_id, 
                    ' ' * (len_max_2 - len(self.attack_team.heroes[1].str_id)), 
                    self.attack_team.heroes[2].str_id, 
                    ' ' * (len_max_3 - len(self.attack_team.heroes[2].str_id)))
        teams_str += '\nDefense team : Frontline : '
        teams_str += '[{}{}, {}{}, {}{}]' \
            .format(self.defense_team.heroes[0].str_id, 
                    ' ' * (len_max_1 - len(self.defense_team.heroes[0].str_id)), 
                    self.defense_team.heroes[1].str_id, 
                    ' ' * (len_max_2 - len(self.defense_team.heroes[1].str_id)), 
                    self.defense_team.heroes[2].str_id, 
                    ' ' * (len_max_3 - len(self.defense_team.heroes[2].str_id)))
        teams_str += '\n               Backline  : '
        teams_str += '[{}{}, {}{}, {}{}]' \
            .format(self.defense_team.heroes[3].str_id, 
                    ' ' * (len_max_1 - len(self.defense_team.heroes[3].str_id)), 
                    self.defense_team.heroes[4].str_id, 
                    ' ' * (len_max_2 - len(self.defense_team.heroes[4].str_id)), 
                    self.defense_team.heroes[5].str_id, 
                    ' ' * (len_max_3 - len(self.defense_team.heroes[5].str_id)))
        return teams_str

    def state(self):
        attack_team_hps = np.array([[self.attack_team.heroes[3].hp, 
                                    self.attack_team.heroes[4].hp, 
                                    self.attack_team.heroes[5].hp], 
                                    [self.attack_team.heroes[0].hp, 
                                    self.attack_team.heroes[1].hp, 
                                    self.attack_team.heroes[2].hp]]).astype(int)
        defense_team_hps = np.array([[self.defense_team.heroes[0].hp, 
                                    self.defense_team.heroes[1].hp, 
                                    self.defense_team.heroes[2].hp], 
                                    [self.defense_team.heroes[3].hp, 
                                    self.defense_team.heroes[4].hp, 
                                    self.defense_team.heroes[5].hp]]).astype(int)
        return '{}\n{}'.format(str(attack_team_hps), str(defense_team_hps))

    def is_finished(self):
        return True if self.attack_team.is_dead() or self.defense_team.is_dead() or self.round > 15 else False

    def process(self):
        self.round = 1
        while not self.is_finished():
            self.turn()
            self.round += 1

        self.log += '\n### Final state ###\n'
        self.log += '\n\n{}'.format(self.state())

        if self.defense_team.is_dead() and self.attack_team.is_dead() or \
                        not self.defense_team.is_dead() and not self.attack_team.is_dead():
            self.winner = 0
        elif self.defense_team.is_dead():
            self.winner = 1
        else:
            self.winner = -1

        if self.winner != 0:
            self.log += '\n\nWinner : team {}'.format(1 if self.winner == 1 else 2)
        else:
            self.log += '\n\nTie'.format(1 if self.winner == 1 else 2)


class EmptyGame:
    def __init__(self):
        self.log = ''
        self.verbose_full = False
