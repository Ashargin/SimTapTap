import random as rd
import pandas as pd
import numpy as np
import pickle
import math

from sim.heroes import Team, Hero
from sim.models import Faction, Familiar, Artifact

heroes = [Hero.abyss_lord, Hero.aden, Hero.blood_tooth, Hero.centaur, Hero.chessia, Hero.drow,
        Hero.dziewona, Hero.freya, Hero.gerald, Hero.grand, Hero.hester, Hero.lexar, Hero.luna, 
        Hero.lindberg, Hero.mars, Hero.martin, Hero.medusa, Hero.megaw, Hero.minotaur, 
        Hero.monkey_king, Hero.mulan, Hero.nameless_king, Hero.orphee, Hero.reaper, Hero.ripper, 
        Hero.rlyeh, Hero.samurai, Hero.saw_machine, Hero.scarlet, Hero.shudde_m_ell, Hero.tesla, 
        Hero.tiger_king, Hero.ultima, Hero.valkyrie, Hero.vegvisir, Hero.verthandi, Hero.vivienne, 
        Hero.werewolf, Hero.wolf_rider, Hero.wolnir, Hero.xexanoth]
alliance = [h for h in heroes if h.faction == Faction.ALLIANCE]
horde = [h for h in heroes if h.faction == Faction.HORDE]
elf = [h for h in heroes if h.faction == Faction.ELF]
undead = [h for h in heroes if h.faction == Faction.UNDEAD]
heaven = [h for h in heroes if h.faction == Faction.HEAVEN]
hell = [h for h in heroes if h.faction == Faction.HELL]
tanks = [Hero.abyss_lord, Hero.grand, Hero.lexar, Hero.minotaur, Hero.monkey_king, Hero.mulan,
        Hero.rlyeh, Hero.tiger_king, Hero.ultima, Hero.vegvisir, 
        Hero.wolf_rider, Hero.wolnir]
healers = [Hero.drow, Hero.megaw, Hero.shudde_m_ell, Hero.vivienne]
others = [h for h in heroes if h not in tanks and h not in healers]
pvp_tanks = [Hero.abyss_lord, Hero.grand, Hero.luna, Hero.minotaur, Hero.monkey_king, Hero.mulan, 
            Hero.rlyeh, Hero.tiger_king, Hero.ultima, Hero.vegvisir, 
            Hero.verthandi, Hero.wolf_rider, Hero.wolnir, Hero.xexanoth]
pvp_others = [h for h in heroes if h not in pvp_tanks]

scores = dict(pd.read_excel('data/results_params.xlsx').score)
probas = {key: math.exp(6 * scores[key]) for key in scores}
artifacts = {'Luna': Artifact.queens_crown.O6,
            'Chessia': Artifact.eternal_curse.O6,
            'Scarlet': Artifact.bone_grip.O6,
            'Centaur': Artifact.fine_snow_dance.O6,
            'Saw_Machine': Artifact.ancient_vows.O6,
            'Ripper': Artifact.siren_heart.O6,
            'Dziewona': Artifact.bone_grip.O6}


def generate_random_sample(n_sample=10000, enemy=False):
    sample = []
    for i in range(n_sample):
        comp = []
        missing_fac = rd.randint(0, 3)
        if missing_fac != 0:
            comp.append(rd.choice(alliance))
        if missing_fac != 1:
            comp.append(rd.choice(horde))
        if missing_fac != 2:
            comp.append(rd.choice(elf))
        if missing_fac != 3:
            comp.append(rd.choice(undead))
        append_duplicate_fac(comp, heroes)
        comp.append(rd.choice(heaven + hell))
        if enemy:
            append_new_fac(comp, heroes)
        rd.shuffle(comp)
        sample.append(comp)

    path = 'data/random_sample.pkl'
    if enemy:
        path = 'data/random_sample_enemy.pkl'
    with open(path, 'wb') as file:
        pickle.dump(sample, file)


def append_duplicate_fac(comp, sub):
    candidates = [h for h in sub if h not in heaven + hell and
                        any(h.faction == h2.faction for h2 in comp)]
    comp.append(rd.choice(candidates))


def append_new_fac(comp, sub):
    candidates = [h for h in sub if h not in heaven + hell and
                        all(h.faction != h2.faction for h2 in comp)]
    comp.append(rd.choice(candidates))


def generate_semirandom_sample(n_sample=10000, n_tanks=1, n_healers=1, enemy=False):
    sample = []
    while len(sample) < n_sample:
        given_up = False
        comp_tanks = []
        comp_healers = []
        if n_tanks >= 1:
            comp_tanks.append(rd.choice(tanks))
            if n_tanks == 2:
                comp_tanks.append(rd.choice([h for h in tanks if h not in heaven + hell]))
        if n_healers >= 1:
            if n_tanks >= 1:
                if comp_tanks[0] in heaven + hell:
                    comp_healers.append(rd.choice([h for h in healers if h not in heaven + hell]))
                else:
                    comp_healers.append(rd.choice(healers))
            else:
                comp_healers.append(rd.choice(healers))
            if n_healers == 2:
                comp_healers.append(rd.choice([h for h in healers if h not in heaven + hell]))

        comp = comp_tanks + comp_healers
        has_hh = False
        if n_tanks >= 1:
            if comp_tanks[0] in heaven + hell:
                has_hh = True
        if n_healers >= 1:
            if comp_healers[0] in heaven + hell:
                has_hh = True

        if n_tanks + n_healers >= 1:
            if has_hh:
                if n_tanks + n_healers <= 2:
                    if n_tanks + n_healers == 1:
                        comp.append(rd.choice([h for h in others if h not in heaven + hell]))
                    append_duplicate_fac(comp, others)
                    for i in range(2):
                        append_new_fac(comp, others)
                elif n_tanks + n_healers == 3:
                    if len(set([h.faction for h in comp])) == 3:
                        append_duplicate_fac(comp, others)
                    else:
                        append_new_fac(comp, others)
                    append_new_fac(comp, others)
                elif n_tanks + n_healers == 4:
                    if len(set([h.faction for h in comp])) == 4:
                        append_duplicate_fac(comp, others)
                    elif len(set([h.faction for h in comp])) == 3:
                        append_new_fac(comp, others)
                    else:
                        given_up = True

            else:
                comp.append(rd.choice([h for h in others if h in heaven + hell]))
                if n_tanks + n_healers == 1:
                    append_duplicate_fac(comp, others)
                    for i in range(2):
                        append_new_fac(comp, others)
                elif n_tanks + n_healers == 2:
                    if len(set([h.faction for h in comp])) == 3:
                        append_duplicate_fac(comp, others)
                    else:
                        append_new_fac(comp, others)
                    append_new_fac(comp, others)
                elif n_tanks + n_healers == 3:
                    if len(set([h.faction for h in comp])) == 4:
                        append_duplicate_fac(comp, others)
                    elif len(set([h.faction for h in comp])) == 3:
                        append_new_fac(comp, others)
                    else:
                        given_up = True
                else:
                    if len(set([h.faction for h in comp])) != 4:
                        given_up = True

        else:
            comp.append(rd.choice([h for h in others if h in heaven + hell]))
            comp.append(rd.choice([h for h in others if h not in heaven + hell]))
            append_duplicate_fac(comp, others)
            for i in range(2):
                append_new_fac(comp, others)

        if not given_up:
            if enemy:
                append_new_fac(comp, others)

            idxs = list(range(n_tanks, 5))
            if enemy:
                idxs = list(range(n_tanks, 6))
            rd.shuffle(idxs)
            idxs = list(range(n_tanks)) + idxs
            comp = [comp[i] for i in idxs]
            sample.append(comp)

    path = 'data/semirandom_sample_{}T{}H.pkl'.format(n_tanks, n_healers)
    if enemy:
        path = 'data/semirandom_sample_{}T{}H_enemy.pkl'.format(n_tanks, n_healers)
    with open(path, 'wb') as file:
        pickle.dump(sample, file)


def generate_pvp_sample(n_sample=20000, pos=None, enemy=False):
    sample = []
    for i in range(n_sample):
        comp = []
        if pos != 1 or enemy:
            new = weighted_choice(pvp_tanks)
            comp.append(new)
        for i in range(2, 7):
            if pos != i or enemy:
                new = weighted_choice(pvp_others)
                while new in comp:
                    new = weighted_choice(pvp_others)
                comp.append(new)
        sample.append(comp)

    path = 'data/pvp_sample_{}.pkl'.format(pos)
    if enemy:
        path = 'data/pvp_sample_enemy.pkl'
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
    for pos in range(1, 7):
        generate_pvp_sample(pos=pos)
    generate_pvp_sample(enemy=True)


def gauntlet_from_sample(sample, length, from_hero=False, hero=None, pos=None, rune=None, artifact=None, player=True, reroll_tears=True):
    gauntlet = []
    for sub in sample[:length]:
        heroes = []
        if from_hero:
            for h in sub[:pos - 1]:
                heroes.append(get_new_hero(h, reroll_tears=reroll_tears))
            if rune is None and artifact is None:
                heroes.append(hero())
            elif rune is None:
                heroes.append(hero(artifact=artifact))
            elif artifact is None:
                heroes.append(hero(rune=rune))
            else:
                heroes.append(hero(rune=rune, artifact=artifact))
            for h in sub[pos - 1:]:
                heroes.append(get_new_hero(h, reroll_tears=reroll_tears))
        else:
            for h in sub:
                heroes.append(get_new_hero(h, reroll_tears=reroll_tears))
        team = None
        if player:
            team = Team(heroes, cancel_aura=True)
        else:
            team = Team(heroes, pet=Familiar.empty, cancel_aura=True)
        gauntlet.append(team)

    return gauntlet


tear_skip_idx = 0
def get_new_hero(h, reroll_tears=True):
    global tear_skip_idx
    new_hero = h()
    if new_hero.artifact == Artifact.tears_of_the_goddess.O6 and reroll_tears:
        if tear_skip_idx % 2 != 0:
            new_hero = h(artifact=artifacts[h.name.value])
        tear_skip_idx += 1
    return new_hero


def random_gauntlet_from_hero(hero, pos, rune=None, artifact=None, length=10000, player=True):
    sample = None
    with open('data/random_sample.pkl', 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length, from_hero=True, hero=hero, 
                                    pos=pos, rune=rune, artifact=artifact, player=player)

    return gauntlet


def semirandom_gauntlet_from_hero(hero, pos, rune=None, artifact=None, n_tanks=1, n_healers=1, length=10000, player=True):
    sample = None
    with open('data/semirandom_sample_{}T{}H.pkl'.format(n_tanks, n_healers), 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length, from_hero=True, hero=hero, 
                                    pos=pos, rune=rune, artifact=artifact, player=player)

    return gauntlet


def pvp_gauntlet_from_hero(hero, pos, rune=None, artifact=None, length=10000, player=True):
    sample = None
    with open('data/pvp_sample_{}.pkl'.format(pos), 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length, from_hero=True, hero=hero, 
                                    pos=pos, rune=rune, artifact=artifact, player=player)

    return gauntlet


def random_gauntlet(length=10000, player=False):
    sample = None
    with open('data/random_sample_enemy.pkl', 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length, player=player)

    return gauntlet


def semirandom_gauntlet(n_tanks=1, n_healers=1, length=10000, player=False):
    sample = None
    with open('data/semirandom_sample_{}T{}H_enemy.pkl'.format(n_tanks, n_healers), 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length, player=player)

    return gauntlet


def pvp_gauntlet(length=10000, player=True):
    sample = None
    with open('data/pvp_sample_enemy.pkl', 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length, player=player)

    return gauntlet
