import pandas as pd
import copy

from sim.gauntlets import random_gauntlet_from_hero, semirandom_gauntlet_from_hero, \
                random_gauntlet, semirandom_gauntlet, pvp_gauntlet_from_hero, pvp_gauntlet
from sim.processing import GauntletSim
from sim.heroes import DummyTeam
from sim.models import Faction, Rune, Artifact


def friend_boss_test(hero, pos, rune=None, artifact=None, n_sim=1000):
    gauntlet = random_gauntlet_from_hero(hero, pos, rune=rune, artifact=artifact, length=n_sim)
    friend_boss_gauntlet = [DummyTeam.friend() for i in range(n_sim)]

    sim = GauntletSim(gauntlet, friend_boss_gauntlet, test_team=1, test_pos=pos, n_sim=n_sim)
    sim.process()
    damage = sim.team_damage

    return sim, damage


def main_friend_boss_test(hero, rune=Rune.attack.R2, artifact=Artifact.dragonblood.O6, n_sim=100):
    print(hero.name.value, '\n')
    best_val = 0
    best_pos = None
    for pos in [1, 2, 3, 4, 5, 6]:
        sim, damage = friend_boss_test(hero, pos=pos, rune=rune, artifact=artifact, n_sim=n_sim)
        print('Pos : {}, damage : {}'.format(pos, damage))
        if damage > best_val:
            best_val = damage
            best_pos = pos
    print('Best pos : {}\n'.format(best_pos))
    sim, damage = friend_boss_test(hero, pos=best_pos, rune=rune, artifact=artifact, n_sim=3*n_sim)
    damage_from_self = sim.heroes[0].stats['damage']
    print('Damage : {}'.format(damage))
    print('Damage from self : {}\n'.format(damage_from_self))

    return sim, damage
    

def master_friend_boss_test(heroes, n_sim=100):
    idx = []
    data = []
    for h in heroes:
        sim, damage = main_friend_boss_test(h, n_sim=n_sim)
        damage_from_self = sim.heroes[0].stats['damage']
        damage_by_skill = sim.heroes[0].stats['damage_by_skill']
        idx.append(h.name.value)
        data.append([damage, damage_from_self, damage_by_skill])
    df = pd.DataFrame(data, index=idx, columns=['damage', 'damage_from_self', 'damage_by_source'])
    df.insert(1, 'score', df.damage.apply(lambda x: round((x - df.damage.median()) / 15000)))
    df.to_excel('data/results_friend_boss.xlsx')


def guild_boss_test(hero, pos, rune=None, artifact=None, n_sim=1000):
    n_tanks = 1 if pos > 1 else 0

    gauntlet = semirandom_gauntlet_from_hero(hero, pos, rune=rune, artifact=artifact, n_tanks=n_tanks,
                                        n_healers=1, length=n_sim)
    guild_boss_gauntlet = [DummyTeam.guild() for i in range(n_sim)]
    sim = GauntletSim(gauntlet, guild_boss_gauntlet, test_team=1, test_pos=pos, n_sim=n_sim)
    sim.process()
    damage = sim.team_damage

    return sim, damage


def main_guild_boss_test(hero, rune=None, artifact=None, n_sim=100):
    print(hero.name.value, '\n')
    best_val = 0
    best_pos = None
    for pos in [1, 2, 3, 4, 5, 6]:
        sim, damage = guild_boss_test(hero, pos=pos, rune=rune, artifact=artifact, n_sim=n_sim)
        print('Pos : {}, damage : {}'.format(pos, damage))
        if damage > best_val:
            best_val = damage
            best_pos = pos
    print('Best pos : {}\n'.format(best_pos))
    sim, damage = guild_boss_test(hero, pos=best_pos, rune=rune, artifact=artifact, n_sim=10*n_sim)
    damage_from_self = sim.heroes[0].stats['damage']
    print('Damage : {}'.format(damage))
    print('Damage from self : {}\n'.format(damage_from_self))

    return sim, damage


def master_guild_boss_test(heroes, n_sim=100):
    idx = []
    data = []
    for h in heroes:
        sim, damage = main_guild_boss_test(h, n_sim=n_sim)
        damage_from_self = sim.heroes[0].stats['damage']
        damage_by_skill = sim.heroes[0].stats['damage_by_skill']
        turns_alive = sim.heroes[0].stats['turns_alive']
        idx.append(h.name.value)
        data.append([damage, damage_from_self, turns_alive, damage_by_skill])
    df = pd.DataFrame(data, index=idx, columns=['damage', 'damage_from_self', 'turns_alive', 'damage_by_skill'])
    df.insert(1, 'score', df.damage.apply(lambda x: round((x - df.damage.median()) / 21500)))
    df.to_excel('data/results_guild_boss.xlsx')


def trial_test(hero, pos, rune=None, artifact=None, n_sim=3000, n_tanks=1, n_healers=1, boost=[0.6, 1.2]):
    gauntlet = semirandom_gauntlet_from_hero(hero, pos, rune=rune, artifact=artifact, n_tanks=n_tanks, 
                                        n_healers=n_healers, length=n_sim)
    trial_gauntlet = random_gauntlet(length=n_sim)

    for i in range(n_sim):
        team = trial_gauntlet[i]
        for h in team.heroes:
            bonus = boost[0] + (boost[1] - boost[0]) * i / n_sim
            h.hp *= 1 + bonus
            h.atk *= 1 + bonus
            h.speed -= 65

    sim = GauntletSim(gauntlet, trial_gauntlet, test_team=1, test_pos=pos, n_sim=n_sim)
    sim.process()
    winrate = sim.wins_1 / sim.n_sim

    return sim, winrate


def main_trial_test(hero, rune=None, artifact=None, n_sim=500, verbose=False):
    data = []
    for n_tanks in [0, 1, 2]:
        for n_healers in [0, 1, 2]:
            for pos in [1, 2, 3, 4, 5, 6]:
                sim, winrate = trial_test(hero, pos=pos, rune=rune, artifact=artifact, n_sim=n_sim, 
                                n_tanks=n_tanks, n_healers=n_healers)
                if verbose:
                    print('{} tanks, {} healers, pos {} : {} winrate'
                            .format(n_tanks, n_healers, pos, winrate))
                data.append((winrate, n_tanks, n_healers, pos))
    data = reversed(sorted(data, key=lambda x: x[0]))
    scores, tanks, healers, pos_vals = zip(*data)
    print('\nBest setups :')
    for i in range(3):
        print('{} tanks, {} healers, pos {} : {} winrate'
                .format(tanks[i], healers[i], pos_vals[i], scores[i]))

    sim, winrate = trial_test(hero, pos_vals[0], rune=rune, artifact=artifact, n_tanks=tanks[0], n_healers=healers[0])
    return sim, winrate


def pvp_test(hero, pos, rune=None, artifact=None, n_sim=3000, attack=True):
    print(hero.name.value, '\n')
    gauntlet = pvp_gauntlet_from_hero(hero, pos, rune=rune, artifact=artifact, length=n_sim)
    enemy_gauntlet = pvp_gauntlet(length=n_sim)

    sim = None
    if attack:
        sim = GauntletSim(gauntlet, enemy_gauntlet, test_team=1, test_pos=pos, n_sim=n_sim)
    else:
        sim = GauntletSim(enemy_gauntlet, gauntlet, test_team=2, test_pos=pos, n_sim=n_sim)
    sim.process()
    winrate = sim.wins_1 / sim.n_sim

    return hero, pos, sim, winrate


def uniform_test(hero, pos, rune=None, artifact=None, n_sim=3000, n_tanks=1, n_healers=1):
    gauntlet = semirandom_gauntlet_from_hero(hero, pos, rune=rune, artifact=artifact, n_tanks=n_tanks, 
                                        n_healers=n_healers, length=n_sim)
    enemy_gauntlet = semirandom_gauntlet(n_tanks=1, n_healers=1, length=n_sim, player=True)

    sim = GauntletSim(gauntlet, enemy_gauntlet, test_team=1, test_pos=pos, n_sim=n_sim)
    sim.process()
    winrate = sim.wins_1 / sim.n_sim

    return sim, winrate


def sim_setup(hero, pos=None, encoded_rune=None, n_sim=1000, verbose=True):
    print(hero.name.value, '\n')

    best_pos = pos
    pos_scores = [0] * 6
    if pos is None:
        best_val = -1
        best_pos = -1
        pos_scores = []
        for pos in [1, 2, 3, 4, 5, 6]:
            n_tanks = 0 if pos == 1 else 1
            sim, winrate = uniform_test(hero, pos=pos, n_tanks=n_tanks, n_sim=n_sim)
            del sim
            pos_scores.append(winrate)
            if winrate > best_val:
                best_val = winrate
                best_pos = pos
            if verbose:
                print('Pos {}, {} winrate'.format(pos, winrate))
        if verbose:
            print('Best pos : {}\n'.format(best_pos))
    n_tanks = 0 if best_pos == 1 else 1

    runes = [Rune.accuracy.R2, Rune.armor_break.R2, Rune.attack.R2, Rune.crit_damage.R2, 
            Rune.crit_rate.R2, Rune.evasion.R2, Rune.hp.R2, Rune.skill_damage.R2, 
            Rune.speed.R2, Rune.vitality.R2]
    best_rune = None
    if encoded_rune is not None:
        best_rune = runes[encoded_rune]
    rune_scores = [0] * 10
    if encoded_rune is None:
        best_val = -1
        best_rune = None
        rune_scores = []
        for rune in runes:
            sim, winrate = uniform_test(hero, pos=best_pos, n_tanks=n_tanks, rune=rune, n_sim=n_sim)
            del sim
            rune_scores.append(winrate)
            if winrate > best_val:
                best_val = winrate
                best_rune = rune
            if verbose:
                print('Rune {}, {} winrate'.format(rune.__class__.__name__, winrate))
        if verbose:
            print('Best rune : {}\n'.format(best_rune.__class__.__name__))

    best_val = -1
    best_art = None
    art_scores = []
    neutral_artifacts = [Artifact.dragonblood.O6, Artifact.bone_grip.O6, Artifact.tears_of_the_goddess.O6, Artifact.giant_lizard.O6]
    artifacts = copy.deepcopy(neutral_artifacts)
    if hero.faction == Faction.ALLIANCE:
        artifacts.append(Artifact.knights_vow.O6)
        artifacts.append(Artifact.ancient_vows.O6)
        artifacts.append(Artifact.gospel_song.O6)
    elif hero.faction == Faction.HORDE:
        artifacts.append(Artifact.primeval_soul.O6)
        artifacts.append(Artifact.gun_of_the_disaster.O6)
        artifacts.append(Artifact.blood_medal.O6)
    elif hero.faction == Faction.ELF:
        artifacts.append(Artifact.star_pray.O6)
        artifacts.append(Artifact.fine_snow_dance.O6)
        artifacts.append(Artifact.queens_crown.O6)
    elif hero.faction == Faction.UNDEAD:
        artifacts.append(Artifact.soul_torrent.O6)
        artifacts.append(Artifact.siren_heart.O6)
        artifacts.append(Artifact.cursed_gun.O6)
    elif hero.faction == Faction.HEAVEN:
        artifacts.append(Artifact.light_pace.O6)
        artifacts.append(Artifact.holy_light_justice.O6)
        artifacts.append(Artifact.gift_of_creation.O6)
    elif hero.faction == Faction.HELL:
        artifacts.append(Artifact.eternal_curse.O6)
        artifacts.append(Artifact.hell_disaster.O6)
    for i, artifact in enumerate(artifacts):
        sim, winrate = uniform_test(hero, pos=best_pos, n_tanks=n_tanks, rune=best_rune, artifact=artifact, n_sim=n_sim)
        del sim
        if i < len(neutral_artifacts):
            art_scores.append(winrate)
        else:
            art_scores.append((winrate, artifact.__class__.__name__))
        if winrate > best_val:
            best_val = winrate
            best_art = artifact
        if verbose:
            print('Artifact {}, {} winrate'.format(artifact.__class__.__name__, winrate))
    if verbose:
        print('Best artifact : {}\n'.format(best_art.__class__.__name__))
    for i in range(len(neutral_artifacts) + 3 - len(art_scores)):
        art_scores.append('')

    return hero.name.value, best_pos, best_rune, best_art, best_val, pos_scores, rune_scores, art_scores
