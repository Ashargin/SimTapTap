import random as rd
import pandas as pd
import numpy as np
import pickle
import math

from sim.heroes import Team, Hero
from sim.models import Familiar, Artifact

# Heroes settings
new_heroes = {'Xexanoth': 0.2,
              'Lindberg': 0.2,
              'Skuld': 0.1}

heroes = [Hero.__dict__[key] for key in Hero.__dict__ if '__' not in key and 'empty' not in key]
tanks = [Hero.abyss_lord, Hero.grand, Hero.lexar, Hero.minotaur, Hero.monkey_king, Hero.mulan,
         Hero.rlyeh, Hero.tiger_king, Hero.ultima, Hero.vegvisir,
         Hero.wolf_rider, Hero.wolnir]
healers = [Hero.drow, Hero.megaw, Hero.phoenix, Hero.shudde_m_ell, Hero.vivienne, Hero.skuld]
others = [h for h in heroes if h not in tanks and h not in healers]

positions = dict(pd.read_excel('data/results_params.xlsx', index_col=0).pos)
pvp_tanks = [h for h in heroes if positions[h.name.value] == 1]
pvp_others = [h for h in heroes if h not in pvp_tanks]
scores = dict(pd.read_excel('data/results_params.xlsx', index_col=0).score)
for new_hero in new_heroes:
    scores[new_hero] = new_heroes[new_hero]
probas = {key: math.exp(6 * scores[key]) for key in scores}
totg_reliance = pd.read_excel('data/results_params.xlsx', index_col=0).totg_reliance
need_totg = list(totg_reliance.sort_values().tail(5).index)
no_totg = list(totg_reliance[totg_reliance == 0].index)


# Generate samples
def generate_random_sample(n_sample=10000, enemy=False):
    # Generate samples
    sample = []
    for _ in range(n_sample):
        n_to_add = 6 if enemy else 5
        comp = np.random.choice(heroes, n_to_add).tolist()
        sample.append(comp)

    # Save
    path = 'data/random_sample.pkl'
    if enemy:
        path = 'data/random_sample_enemy.pkl'
    with open(path, 'wb') as file:
        pickle.dump(sample, file)


def generate_semirandom_sample(n_sample=10000, n_tanks=1, n_healers=1, enemy=False):
    # Generate samples
    sample = []
    for _ in range(n_sample):
        n_to_add = 6 if enemy else 5
        comp = []
        for _ in range(n_tanks):
            comp.append(rd.choice(tanks))
        for _ in range(n_healers):
            comp.append(rd.choice(healers))
        for _ in range(n_to_add - n_tanks - n_healers):
            comp.append(rd.choice(others))

        # Shuffle
        idxs = list(range(n_tanks, n_to_add))
        rd.shuffle(idxs)
        idxs = list(range(n_tanks)) + idxs
        comp = [comp[i] for i in idxs]
        sample.append(comp)

    # Save
    path = 'data/semirandom_sample_{}T{}H.pkl'.format(n_tanks, n_healers)
    if enemy:
        path = 'data/semirandom_sample_{}T{}H_enemy.pkl'.format(n_tanks, n_healers)
    with open(path, 'wb') as file:
        pickle.dump(sample, file)


def generate_pvp_sample(n_sample=20000, n_tanks=0, enemy=False):
    # Generate samples
    sample = []
    for _ in range(n_sample):
        n_to_add = 6 if enemy else 5
        comp = []
        for _ in range(n_tanks):
            new = weighted_choice(pvp_tanks)
            while new in comp:
                new = weighted_choice(pvp_tanks)
            comp.append(new)
        for _ in range(n_to_add - n_tanks):
            new = weighted_choice(pvp_others)
            while new in comp:
                new = weighted_choice(pvp_others)
            comp.append(new)
        sample.append(comp)

    # Save
    path = 'data/pvp_sample_{}T.pkl'.format(n_tanks)
    if enemy:
        path = 'data/pvp_sample_{}T_enemy.pkl'.format(n_tanks)
    with open(path, 'wb') as file:
        pickle.dump(sample, file)


def weighted_choice(sub):
    sub_probas = [probas[h.name.value] for h in sub]
    sub_probas = [p / sum(sub_probas) for p in sub_probas]
    return np.random.choice(sub, p=sub_probas)


def generate_all_samples(n_sample=10000):
    generate_random_sample(n_sample=n_sample)
    generate_random_sample(n_sample=n_sample, enemy=True)
    for n_tanks in (0, 1, 2):
        for n_healers in (0, 1, 2):
            generate_semirandom_sample(n_sample=n_sample, n_tanks=n_tanks, n_healers=n_healers)
            generate_semirandom_sample(n_sample=n_sample, n_tanks=n_tanks, n_healers=n_healers, enemy=True)
    for n_tanks in (0, 1):
        generate_pvp_sample(n_tanks=n_tanks)
    generate_pvp_sample(n_tanks=1, enemy=True)


# Gaunlet from sample
def gauntlet_from_sample(sample, length, from_hero=False, hero=None, pos=None, rune=None, artifact=None,
                         player=True, totg_max=2):
    gauntlet = []
    for sub in sample[:length]:
        totg_left = totg_max
        heroes_left = len(sub)
        team_heroes = []
        if from_hero:
            if artifact is None:
                artifact = None if hero.name.value in no_totg else Artifact.tears_of_the_goddess.O6
            for h in sub[:pos - 1]:
                new_h, totg_left, heroes_left = get_new_hero(h, totg_left=totg_left, heroes_left=heroes_left)
                team_heroes.append(new_h)
            if rune is None and artifact is None:
                team_heroes.append(hero())
            elif rune is None:
                team_heroes.append(hero(artifact=artifact))
            elif artifact is None:
                team_heroes.append(hero(rune=rune))
            else:
                team_heroes.append(hero(rune=rune, artifact=artifact))
            for h in sub[pos - 1:]:
                new_h, totg_left, heroes_left = get_new_hero(h, totg_left=totg_left, heroes_left=heroes_left)
                team_heroes.append(new_h)
        else:
            for h in sub:
                new_h, totg_left, heroes_left = get_new_hero(h, totg_left=totg_left, heroes_left=heroes_left)
                team_heroes.append(new_h)
        if player:
            team = Team(team_heroes, cancel_aura=True)
        else:
            team = Team(team_heroes, pet=Familiar.empty(), cancel_aura=True)
        gauntlet.append(team)

    return gauntlet


def get_new_hero(h, totg_left, heroes_left):
    if h.name.value in need_totg and totg_left > 0 \
            or h.name.value not in no_totg and totg_left >= heroes_left:
        new_h = h(artifact=Artifact.tears_of_the_goddess.O6)
        totg_left -= 1
    else:
        new_h = h()
    heroes_left -= 1

    return new_h, totg_left, heroes_left


def random_gauntlet_from_hero(hero, pos, rune=None, artifact=None, length=10000, player=True):
    with open('data/random_sample.pkl', 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length, from_hero=True, hero=hero,
                                    pos=pos, rune=rune, artifact=artifact, player=player)

    return gauntlet


def semirandom_gauntlet_from_hero(hero, pos, rune=None, artifact=None, n_tanks=1, n_healers=1, length=10000,
                                  player=True):
    with open('data/semirandom_sample_{}T{}H.pkl'.format(n_tanks, n_healers), 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length, from_hero=True, hero=hero,
                                    pos=pos, rune=rune, artifact=artifact, player=player)

    return gauntlet


def pvp_gauntlet_from_hero(hero, pos, rune=None, artifact=None, length=10000, player=True):
    n_tanks = 0 if pos == 1 else 1
    with open('data/pvp_sample_{}T.pkl'.format(n_tanks), 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length, from_hero=True, hero=hero,
                                    pos=pos, rune=rune, artifact=artifact, player=player)

    return gauntlet


def random_gauntlet(length=10000, player=False):
    with open('data/random_sample_enemy.pkl', 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length, player=player)

    return gauntlet


def semirandom_gauntlet(n_tanks=1, n_healers=1, length=10000, player=False):
    with open('data/semirandom_sample_{}T{}H_enemy.pkl'.format(n_tanks, n_healers), 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length, player=player)

    return gauntlet


def pvp_gauntlet(length=10000, player=True):
    with open('data/pvp_sample_1T_enemy.pkl', 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length, player=player)

    return gauntlet
