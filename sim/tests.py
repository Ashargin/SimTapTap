from sim.gauntlets import random_gauntlet_from_hero, semirandom_gauntlet_from_hero, \
                            semirandom_gauntlet_notank_from_hero, random_gauntlet
from sim.sim import GauntletSim
from sim.heroes import DummyTeam


def friend_boss_test(hero, pos, n_sim=1000):
    gauntlet = random_gauntlet_from_hero(hero, pos, length=n_sim)
    friend_boss_gauntlet = [DummyTeam.centaur() for i in range(len(gauntlet))]
    sim = GauntletSim(gauntlet, friend_boss_gauntlet, test_team=1, test_pos=pos, n_sim=n_sim)
    sim.process()
    damage = sim.team_damage

    return sim, damage


def guild_boss_test(hero, pos, n_sim=1000):
    gauntlet = random_gauntlet_from_hero(hero, pos, length=n_sim)
    guild_boss_gauntlet = [DummyTeam.guild_wanderer() for i in range(len(gauntlet))]
    sim = GauntletSim(gauntlet, guild_boss_gauntlet, test_team=1, test_pos=pos, n_sim=n_sim)
    sim.process()
    damage = sim.team_damage

    return sim, damage


def trial_test(hero, pos, n_sim=1000, tank=None, boost=0.1):
    if tank is None:
        tank = pos == 1

    gauntlet = None
    if tank:
        gauntlet = semirandom_gauntlet_notank_from_hero(hero, pos, length=n_sim)
    else:
        gauntlet = semirandom_gauntlet_from_hero(hero, pos, length=n_sim)
    trial_gauntlet = random_gauntlet(length=n_sim)

    for i in range(n_sim):
        team = trial_gauntlet[i]
        for h in team.heroes:
            h.hp *= 1 + boost * (2 * i / n_sim - 1)
            h.atk *= 1 + boost * (2 * i / n_sim - 1)

    sim = GauntletSim(gauntlet, trial_gauntlet, test_team=1, test_pos=pos, n_sim=n_sim)
    sim.process()
    winrate = sim.wins_1 / sim.n_sim

    return sim, winrate
