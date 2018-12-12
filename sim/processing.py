import numpy as np
import random as rd
import copy
from collections import defaultdict

from sim.utils import format_stats, add_dicts, rescale_dict


class BaseSim:
    def compute_winner(self, winner):
        self.winners.append(winner)
        if winner == 1:
            self.wins_1 += 1
        elif winner == -1:
            self.wins_2 += 1
        else:
            self.ties += 1

    def print_stats(self, stat='damage'):
        print('# {} #\n'.format(stat))
        len_max = max(len(u.str_id) for u in self.heroes + self.pets)
        for u in self.heroes + self.pets:
            print('{}{} : {}'.format(u.str_id, ' ' * (len_max - len(u.str_id)), 
                                                    self.stats[stat][u.str_id]))

    def print_winrate(self):
        print('Attacker winrate : {}%'.format(100 * self.wins_1 / self.n_sim))
        print('Defender winrate : {}%'.format(100 * (self.wins_2 + self.ties) / self.n_sim))
        print('Including wins by tie : {}%'.format(100 * self.ties / self.n_sim))


class GameSim(BaseSim):
    def __init__(self, attack_team, defense_team, n_sim=1000):
        self.attack_team = attack_team
        self.defense_team = defense_team
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
        self.winners = []
        self.wins_1 = 0
        self.wins_2 = 0
        self.ties = 0
        self.n_sim = n_sim

    def process(self):
        units_stats = {unit.str_id: {} for unit in self.heroes + self.pets}
        for i in range(self.n_sim):
            game = Game(self.attack_team, self.defense_team)
            game.process()
            winner = game.winner
            self.compute_winner(winner)

            for unit in game.heroes + game.pets:
                add_dicts(units_stats[unit.str_id], unit.stats)

            del game

        for unit in self.heroes + self.pets:
            rescale_dict(units_stats[unit.str_id], 1 / self.n_sim)
            unit.stats = units_stats[unit.str_id]
        self.stats = {key: {u.str_id: u.stats[key] for u in self.heroes + self.pets}
                                            for key in self.heroes[0].stats.keys()}


class GauntletAttackSim(BaseSim):
    def __init__(self, attack_team, gauntlet, n_sim=1000):
        self.attack_team = attack_team
        self.gauntlet = gauntlet
        for h in self.attack_team.heroes:
            h.str_id = '{}_{}_{}'.format(h.name.value, 1, h.pos + 1)
        self.attack_team.pet.str_id = self.attack_team.pet.name + '_1'
        self.heroes = self.attack_team.heroes
        self.pets = [self.attack_team.pet]
        self.winners = []
        self.wins_1 = 0
        self.wins_2 = 0
        self.ties = 0
        self.n_sim = n_sim

    def process(self):
        units_stats = {unit.str_id: {} for unit in self.heroes + self.pets}
        for i in range(self.n_sim):
            defense_team = self.gauntlet[0]
            game = Game(self.attack_team, defense_team, copy_defense=False)
            game.process()
            winner = game.winner
            self.compute_winner(winner)

            for unit in game.attack_team.heroes + [game.attack_team.pet]:
                add_dicts(units_stats[unit.str_id], unit.stats)

            del game
            del self.gauntlet[0]

        for unit in self.heroes + self.pets:
            rescale_dict(units_stats[unit.str_id], 1 / self.n_sim)
            unit.stats = units_stats[unit.str_id]
        self.stats = {key: {u.str_id: u.stats[key] for u in self.heroes + self.pets}
                                            for key in self.heroes[0].stats.keys()}


class GauntletDefenseSim(BaseSim):
    def __init__(self, gauntlet, defense_team, n_sim=1000):
        self.gauntlet = gauntlet
        self.defense_team = defense_team
        for h in self.defense_team.heroes:
            h.str_id = '{}_{}_{}'.format(h.name.value, 1, h.pos + 1)
        self.defense_team.pet.str_id = self.defense_team.pet.name + '_2'
        self.heroes = self.defense_team.heroes
        self.pets = [self.defense_team.pet]
        self.winners = []
        self.wins_1 = 0
        self.wins_2 = 0
        self.ties = 0
        self.n_sim = n_sim

    def process(self):
        units_stats = {unit.str_id: {} for unit in self.heroes + self.pets}
        for i in range(self.n_sim):
            attack_team = self.gauntlet[0]
            game = Game(attack_team, self.defense_team, copy_attack=False)
            game.process()
            winner = game.winner
            self.compute_winner(winner)

            for unit in game.defense_team.heroes + [game.defense_team.pet]:
                add_dicts(units_stats[unit.str_id], unit.stats)

            del game
            del self.gauntlet[0]

        for unit in self.heroes + self.pets:
            rescale_dict(units_stats[unit.str_id], 1 / self.n_sim)
            unit.stats = units_stats[unit.str_id]
        self.stats = {key: {u.str_id: u.stats[key] for u in self.heroes + self.pets}
                                            for key in self.heroes[0].stats.keys()}


class GauntletSim(BaseSim):
    def __init__(self, attack_gauntlet, defense_gauntlet, test_team=None, 
                                                test_pos=None, n_sim=1000):
        self.attack_gauntlet = attack_gauntlet
        self.defense_gauntlet = defense_gauntlet
        self.heroes = []
        self.test_team = test_team
        self.test_pos = test_pos
        if self.test_team == 1:
            self.heroes = [copy.deepcopy(attack_gauntlet[0].heroes[self.test_pos - 1])]
        elif self.test_team == 2:
            self.heroes = [copy.deepcopy(defense_gauntlet[0].heroes[self.test_pos - 1])]
        for h in self.heroes:
            h.str_id = '{}_{}_{}'.format(h.name.value, self.test_team, self.test_pos)
        self.pets = []
        self.winners = []
        self.wins_1 = 0
        self.wins_2 = 0
        self.ties = 0
        self.n_sim = n_sim

    def process(self):
        units_stats = {unit.str_id: {} for unit in self.heroes}
        team_damage = 0
        for i in range(self.n_sim):
            from pympler.asizeof import asizeof
            attack_team = self.attack_gauntlet[0]
            defense_team = self.defense_gauntlet[0]
            game = Game(attack_team, defense_team, copy_attack=False, copy_defense=False)
            game.process()
            winner = game.winner
            self.compute_winner(winner)

            if self.test_team == 1:
                unit = game.attack_team.heroes[self.test_pos - 1]
                add_dicts(units_stats[unit.str_id], unit.stats)
                team_damage += sum([game.stats['damage'][h.str_id] 
                                    for h in game.attack_team.heroes])
            elif self.test_team == 2:
                unit = game.defense_team.heroes[self.test_pos - 1]
                add_dicts(units_stats[unit.str_id], unit.stats)
                team_damage += sum([game.stats['damage'][h.str_id] 
                                    for h in game.defense_team.heroes])

            del game
            del self.attack_gauntlet[0]
            del self.defense_gauntlet[0]

        for unit in self.heroes:
            rescale_dict(units_stats[unit.str_id], 1 / self.n_sim)
            unit.stats = units_stats[unit.str_id]
            team_damage *= 1 / self.n_sim
            self.team_damage = round(team_damage)
        self.stats = {key: {u.str_id: u.stats[key] for u in self.heroes + self.pets}
                                            for key in self.heroes[0].stats.keys()}


class Game:
    def __init__(self, attack_team, defense_team, verbose_full=False, 
                                    copy_attack=True, copy_defense=True):
        self.actions = []
        self.rounds = []
        self.attack_team = attack_team
        self.defense_team = defense_team
        if copy_attack:
            self.attack_team = copy.deepcopy(self.attack_team)
        if copy_defense:
            self.defense_team = copy.deepcopy(self.defense_team)
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
        for unit in self.heroes + self.pets:
            unit.game = self
            unit.stats = {'damage': 0,
                        'effective_healing': 0,
                        'healing': 0, # healing = effective_healing + overheal
                        'damage_taken': 0,
                        'effective_healing_taken': 0,
                        'healing_taken': 0,
                        'damage_by_skill': defaultdict(int),
                        'damage_by_target': defaultdict(int),
                        'effective_healing_by_skill': defaultdict(int),
                        'effective_healing_by_target': defaultdict(int),
                        'healing_by_skill': defaultdict(int),
                        'healing_by_target': defaultdict(int),
                        'damage_taken_by_skill': defaultdict(int),
                        'damage_taken_by_source': defaultdict(int),
                        'effective_healing_taken_by_skill': defaultdict(int),
                        'effective_healing_taken_by_source': defaultdict(int),
                        'healing_taken_by_skill': defaultdict(int),
                        'healing_taken_by_source': defaultdict(int),
                        'kills': 0,
                        'deaths': 0,
                        'skills': 0,
                        'turns_played': 0,
                        'effective_hard_cc_turns': 0,
                        'effective_hard_cc_turns_taken': 0,
                        'effective_silence_turns': 0,
                        'effective_silence_turns_taken': 0,
                        'turns_alive': 0,
                        'game_length': 0,
                        'hits': 0,
                        'hits_taken': 0,
                        'crits': 0,
                        'crits_taken': 0,
                        'dodges': 0,
                        'dodges_taken': 0,
                        'dots': 0, # including poisons and bleeds
                        'dots_taken': 0,
                        'bleeds': 0,
                        'bleeds_taken': 0,
                        'poisons': 0,
                        'poisons_taken': 0,
                        'silences': 0,
                        'silences_taken': 0,
                        'stuns': 0,
                        'stuns_taken': 0,
                        'petrifies': 0,
                        'petrifies_taken': 0,
                        'freezes': 0,
                        'freezes_taken': 0,
                        'hard_ccs': 0, # stuns, petrifies or freezes
                        'hard_ccs_taken': 0,
                        'attack_ups': 0, # HERE
                        'attack_ups_taken': 0,
                        'attack_downs': 0,
                        'attack_downs_taken': 0,
                        'hp_ups': 0,
                        'hp_ups_taken': 0,
                        'hp_downs': 0,
                        'hp_downs_taken': 0,
                        'crit_rate_ups': 0,
                        'crit_rate_ups_taken': 0,
                        'crit_rate_downs': 0,
                        'crit_rate_downs_taken': 0,
                        'crit_damage_ups': 0,
                        'crit_damage_ups_taken': 0,
                        'crit_damage_downs': 0,
                        'crit_damage_downs_taken': 0,
                        'hit_rate_ups': 0,
                        'hit_rate_ups_taken': 0,
                        'hit_rate_downs': 0,
                        'hit_rate_downs_taken': 0,
                        'dodge_ups': 0,
                        'dodge_ups_taken': 0,
                        'dodge_downs': 0,
                        'dodge_downs_taken': 0,
                        'skill_damage_ups': 0,
                        'skill_damage_ups_taken': 0,
                        'skill_damage_downs': 0,
                        'skill_damage_downs_taken': 0,
                        'control_immune_ups': 0,
                        'control_immune_ups_taken': 0,
                        'control_immune_downs': 0,
                        'control_immune_downs_taken': 0,
                        'armor_break_ups': 0,
                        'armor_break_ups_taken': 0,
                        'armor_break_downs': 0,
                        'armor_break_downs_taken': 0,
                        'armor_ups': 0,
                        'armor_ups_taken': 0,
                        'armor_downs': 0,
                        'armor_downs_taken': 0,
                        'speed_ups': 0,
                        'speed_ups_taken': 0,
                        'speed_downs': 0,
                        'speed_downs_taken': 0,
                        'energy_ups': 0,
                        'energy_ups_taken': 0,
                        'energy_downs': 0,
                        'energy_downs_taken': 0,
                        'damage_reduction_ups': 0,
                        'damage_reduction_ups_taken': 0,
                        'true_damage_ups': 0,
                        'true_damage_ups_taken': 0}
            for stat in ('damage_by_skill', 'damage_by_target', 'effective_healing_by_skill', 
                        'effective_healing_by_target', 'healing_by_skill', 'healing_by_target', 
                        'damage_taken_by_skill', 'damage_taken_by_source', 'effective_healing_taken_by_skill', 
                        'effective_healing_taken_by_source', 'healing_taken_by_skill', 
                        'healing_taken_by_source'):
                unit.stats[stat]['Total'] = 0
        self.prefix = self.teams() + '\n'

    def turn(self):
        round_prefix = '\n### Turn {} ###'.format(self.round)

        # effects
        prefix = '\n# Active effects #'.format(self.round)
        self.actions = []
        effect_ids = [e.id for h in self.heroes for e in h.effects]
        for h in self.heroes:
            if not h.is_dead:
                h.can_attack = True
                for e in [e for e in h.effects if e.percentage]:
                    if e.id in effect_ids:
                        e.tick()
                for e in [e for e in h.effects if not e.percentage]:
                    if e.id in effect_ids:
                        e.tick()
        effects_turn = EffectsTurn(self.actions, prefix=prefix)

        # heroes
        heroes_turns = []
        while any([h.can_attack for h in self.heroes]) and not self.is_finished():
            self.actions = []
            max_speed = max([h.speed for h in self.heroes if h.can_attack])
            fastest_heroes = [h for h in self.heroes
                              if h.speed == max_speed and h.can_attack]
            fastest = fastest_heroes[rd.randint(0, len(fastest_heroes) - 1)]
            prefix = "\n\n# {}'s turn #".format(fastest.str_id)
            fastest.turn()
            heroes_turns.append(HeroTurn(self.actions, prefix=prefix))

        # familiars
        pet_turns = []
        for pet in (self.attack_team.pet, self.defense_team.pet):
            if not self.is_finished():
                self.actions = []
                pet_playing = False
                if pet.energy == 100:
                    pet_playing = True
                    prefix = "\n\n# {}'s turn #".format(pet.str_id)
                pet.turn()
                if pet_playing:
                    pet_turns.append(PetTurn(self.actions, prefix=prefix))

        # effects
        for h in self.heroes:
            if not h.is_dead:
                for e in h.effects:
                    if e.turns == 0:
                        e.kill()

        round_suffix = '\n\n{}\n'.format(self.state())

        round_turns = [effects_turn] + heroes_turns + pet_turns
        round = Round(round_turns, prefix=round_prefix, suffix=round_suffix)
        self.rounds.append(round)

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
        names = [h.str_id if not h.is_dead else 'DEAD' for h in self.heroes]
        hps = [str(round(h.hp)) if not h.is_dead else '' for h in self.heroes]
        energies = [str(int(h.energy) if h.energy == int(h.energy) else h.energy) 
                            if not h.is_dead else '' for h in self.heroes]
        hps_energies = [('{}|{}'.format(hps[i], energies[i])) 
                            if not h.is_dead else ' '
                            for i, h in enumerate(self.heroes)]
        names_len_max_1 = max([len(names[i]) for i in (0, 3, 6, 9)])
        names_len_max_2 = max([len(names[i]) for i in (1, 4, 7, 10)])
        names_len_max_3 = max([len(names[i]) for i in (2, 5, 8, 11)])
        hps_len_max_1 = max([len(hps[i]) for i in (0, 3, 6, 9)])
        hps_len_max_2 = max([len(hps[i]) for i in (1, 4, 7, 10)])
        hps_len_max_3 = max([len(hps[i]) for i in (2, 5, 8, 11)])
        energies_len_max_1 = max([len(energies[i]) for i in (0, 3, 6, 9)])
        energies_len_max_2 = max([len(energies[i]) for i in (1, 4, 7, 10)])
        energies_len_max_3 = max([len(energies[i]) for i in (2, 5, 8, 11)])

        state_str = '# State #'
        state_str += '\nAttack team  : Backline  : '
        state_str += '[{}{}{}{}, {}{}{}{}, {}{}{}{}]' \
            .format(names[3],
                    ' ' * (names_len_max_1 - len(names[3]) + hps_len_max_1 - len(hps[3]) + 1),
                    hps_energies[3],
                    ' ' * (energies_len_max_1 - len(energies[3])),
                    names[4],
                    ' ' * (names_len_max_2 - len(names[4]) + hps_len_max_2 - len(hps[4]) + 1),
                    hps_energies[4],
                    ' ' * (energies_len_max_2 - len(energies[4])),
                    names[5],
                    ' ' * (names_len_max_3 - len(names[5]) + hps_len_max_3 - len(hps[5]) + 1),
                    hps_energies[5],
                    ' ' * (energies_len_max_3 - len(energies[5])))
        state_str += '\n               Frontline : '
        state_str += '[{}{}{}{}, {}{}{}{}, {}{}{}{}]' \
            .format(names[0],
                    ' ' * (names_len_max_1 - len(names[0]) + hps_len_max_1 - len(hps[0]) + 1),
                    hps_energies[0],
                    ' ' * (energies_len_max_1 - len(energies[0])),
                    names[1],
                    ' ' * (names_len_max_2 - len(names[1]) + hps_len_max_2 - len(hps[1]) + 1),
                    hps_energies[1],
                    ' ' * (energies_len_max_2 - len(energies[1])),
                    names[2],
                    ' ' * (names_len_max_3 - len(names[2]) + hps_len_max_3 - len(hps[2]) + 1),
                    hps_energies[2],
                    ' ' * (energies_len_max_3 - len(energies[2])))
        state_str += '\nDefense team : Frontline : '
        state_str += '[{}{}{}{}, {}{}{}{}, {}{}{}{}]' \
            .format(names[6],
                    ' ' * (names_len_max_1 - len(names[6]) + hps_len_max_1 - len(hps[6]) + 1),
                    hps_energies[6],
                    ' ' * (energies_len_max_1 - len(energies[6])),
                    names[7],
                    ' ' * (names_len_max_2 - len(names[7]) + hps_len_max_2 - len(hps[7]) + 1),
                    hps_energies[7],
                    ' ' * (energies_len_max_2 - len(energies[7])),
                    names[8],
                    ' ' * (names_len_max_3 - len(names[8]) + hps_len_max_3 - len(hps[8]) + 1),
                    hps_energies[8],
                    ' ' * (energies_len_max_3 - len(energies[8])))
        state_str += '\n               Backline  : '
        state_str += '[{}{}{}{}, {}{}{}{}, {}{}{}{}]' \
            .format(names[9],
                    ' ' * (names_len_max_1 - len(names[9]) + hps_len_max_1 - len(hps[9]) + 1),
                    hps_energies[9],
                    ' ' * (energies_len_max_1 - len(energies[9])),
                    names[10],
                    ' ' * (names_len_max_2 - len(names[10]) + hps_len_max_2 - len(hps[10]) + 1),
                    hps_energies[10],
                    ' ' * (energies_len_max_2 - len(energies[10])),
                    names[11],
                    ' ' * (names_len_max_3 - len(names[11]) + hps_len_max_3 - len(hps[11]) + 1),
                    hps_energies[11],
                    ' ' * (energies_len_max_3 - len(energies[11])))

        return state_str

    def is_finished(self):
        return True if self.attack_team.is_dead() or self.defense_team.is_dead() or self.round > 15 else False

    def process(self):
        self.round = 1
        while not self.is_finished():
            self.turn()
            self.round += 1
            for unit in self.heroes + self.pets:
                if not unit.is_dead:
                    unit.stats['turns_alive'] += 1
                unit.stats['game_length'] += 1

        self.suffix = '\n### Final state ###\n'
        self.suffix += '\n\n{}'.format(self.state())

        for h in self.heroes:
            h.stats = format_stats(h.stats)
        for pet in self.pets:
            pet.stats = format_stats(pet.stats, pet=True)
        self.stats = {key: {u.str_id: u.stats[key] for u in self.heroes + self.pets}
                                            for key in self.heroes[0].stats.keys()}

        if self.defense_team.is_dead() and self.attack_team.is_dead() or \
                not self.defense_team.is_dead() and not self.attack_team.is_dead():
            self.winner = 0
        elif self.defense_team.is_dead():
            self.winner = 1
        else:
            self.winner = -1

        if self.winner != 0:
            self.suffix += '\n\nWinner : team {}'.format(1 if self.winner == 1 else 2)
        else:
            self.suffix += '\n\nTie'.format(1 if self.winner == 1 else 2)

        self.log = Log(self.rounds, prefix=self.prefix, suffix=self.suffix)

    def print_stats(self, stat='damage'):
        print('# {} #\n'.format(stat))
        len_max = max(len(e.str_id) for e in self.heroes + self.pets)
        for e in self.heroes + self.pets:
            print('{}{} : {}'.format(e.str_id, ' ' * (len_max - len(e.str_id)), 
                                                    self.stats[stat][e.str_id]))


class EmptyGame:
    def __init__(self):
        self.actions = []
        self.verbose_full = False

    def is_finished(self):
        return False


class Log:
    def __init__(self, rounds, prefix='', suffix=''):
        self.rounds = rounds
        self.text = prefix + ''.join([r.text for r in self.rounds]) + suffix


class Round:
    def __init__(self, turns, prefix='', suffix=''):
        self.turns = turns
        self.text = prefix + ''.join([t.text for t in self.turns]) + suffix


class EffectsTurn:
    def __init__(self, actions, prefix=''):
        self.actions = actions
        self.text = prefix + ''.join([a.text for a in self.actions])


class HeroTurn:
    def __init__(self, actions, prefix=''):
        self.actions = actions
        self.text = prefix + ''.join([a.text for a in self.actions])


class PetTurn:
    def __init__(self, actions, prefix=''):
        self.actions = actions
        self.text = prefix + ''.join([a.text for a in self.actions])
