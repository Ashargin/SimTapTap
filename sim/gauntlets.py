import random as rd
import pickle

from sim.heroes import Team, Hero
from sim.models import Faction

heroes = [Hero.abyss_lord, Hero.aden, Hero.blood_tooth, Hero.centaur, Hero.chessia, 
        Hero.dziewona, Hero.freya, Hero.gerald, Hero.grand, Hero.hester, Hero.lexar, Hero.luna, 
        Hero.mars, Hero.martin, Hero.medusa, Hero.megaw, Hero.minotaur, Hero.monkey_king, 
        Hero.mulan, Hero.nameless_king, Hero.orphee, Hero.reaper, Hero.ripper, Hero.rlyeh, 
        Hero.samurai, Hero.saw_machine, Hero.scarlet, Hero.shudde_m_ell, Hero.tesla, 
        Hero.tiger_king, Hero.ultima, Hero.vegvisir, Hero.verthandi, Hero.vivienne, 
        Hero.werewolf, Hero.wolf_rider, Hero.wolnir]
alliance = [h for h in heroes if h.faction == Faction.ALLIANCE]
horde = [h for h in heroes if h.faction == Faction.HORDE]
elf = [h for h in heroes if h.faction == Faction.ELF]
undead = [h for h in heroes if h.faction == Faction.UNDEAD]
heaven = [h for h in heroes if h.faction == Faction.HEAVEN]
hell = [h for h in heroes if h.faction == Faction.HELL]
tanks = [Hero.abyss_lord, Hero.grand, Hero.lexar, Hero.minotaur, Hero.monkey_king, 
        Hero.rlyeh, Hero.tiger_king, Hero.ultima, Hero.vegvisir, 
        Hero.wolf_rider, Hero.wolnir]
healers = [Hero.megaw, Hero.shudde_m_ell, Hero.verthandi, Hero.vivienne]
others = [h for h in heroes if h not in tanks and h not in healers]


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
        if missing_fac == 0:
            comp.append(rd.choice(horde + elf + undead))
        if missing_fac == 1:
            comp.append(rd.choice(alliance + elf + undead))
        if missing_fac == 2:
            comp.append(rd.choice(alliance + horde + undead))
        if missing_fac == 3:
            comp.append(rd.choice(alliance + horde+ elf))
        comp.append(rd.choice(heaven + hell))
        if enemy:
            comp.append(rd.choice(heroes))
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
        path = path = 'data/semirandom_sample_{}T{}H_enemy.pkl'.format(n_tanks, n_healers)
    with open(path, 'wb') as file:
        pickle.dump(sample, file)


def generate_all_semirandom_samples(n_sample=10000):
    for n_tanks in (0, 1, 2):
        for n_healers in (0, 1, 2):
            generate_semirandom_sample(n_sample=n_sample, n_tanks=n_tanks, n_healers=n_healers)
            generate_semirandom_sample(n_sample=n_sample, n_tanks=n_tanks, n_healers=n_healers, enemy=True)


# def generate_pvp_sample(n_sample=10000, enemy=False):
#     pass


def gauntlet_from_sample(sample, length, from_hero=False, hero=None, pos=None):
    gauntlet = []
    for sub in sample[:length]:
        heroes = []
        if from_hero:
            for h in sub[:pos - 1]:
                heroes.append(h())
            heroes.append(hero())
            for h in sub[pos - 1:]:
                heroes.append(h())
        else:
            for h in sub:
                heroes.append(h())
        team = Team(heroes)
        gauntlet.append(team)

    return gauntlet


def random_gauntlet_from_hero(hero, pos, length=10000):
    sample = None
    with open('data/random_sample.pkl', 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length, from_hero=True, hero=hero, pos=pos)

    return gauntlet


def semirandom_gauntlet_from_hero(hero, pos, length=10000):
    sample = None
    with open('data/semirandom_sample.pkl', 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length, from_hero=True, hero=hero, pos=pos)

    return gauntlet


def semirandom_gauntlet_notank_from_hero(hero, pos, length=10000):
    sample = None
    with open('data/semirandom_sample_notank.pkl', 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length, from_hero=True, hero=hero, pos=pos)

    return gauntlet


def random_gauntlet(length=10000):
    sample = None
    with open('data/random_sample_enemy.pkl', 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length)

    return gauntlet


def semirandom_gauntlet(length=10000):
    sample = None
    with open('data/semirandom_sample_enemy.pkl', 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length)

    return gauntlet


def semirandom_gauntlet_notank(length=10000):
    sample = None
    with open('data/semirandom_sample_notank_enemy.pkl', 'rb') as file:
        sample = pickle.load(file)
    gauntlet = gauntlet_from_sample(sample, length=length)

    return gauntlet
