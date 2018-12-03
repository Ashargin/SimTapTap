import numpy as np
import random as rd
import cProfile

from sim.heroes import Team, Hero
from sim.models import Armor, Helmet, Weapon, Pendant, Rune, Artifact, Familiar
from sim.sim import Sim, Game

heroes = [Hero.aden, Hero.blood_tooth, Hero.centaur, Hero.chessia, Hero.dziewona, Hero.forest_healer, Hero.freya,
          Hero.gerald, Hero.luna, Hero.medusa, Hero.minotaur, Hero.monkey_king, Hero.reaper, Hero.ripper, Hero.rlyeh,
          Hero.saw_machine, Hero.scarlet, Hero.shudde_m_ell, Hero.ultima, Hero.vegvisir, Hero.verthandi, 
          Hero.nameless_king, Hero.mars, Hero.mulan, Hero.vivienne]


def get_random_team():
    team_heroes = []
    for i in range(6):
        team_heroes.append(heroes[rd.randint(0, len(heroes) - 1)]())
    return Team(team_heroes)


attack_team = get_random_team()
defense_team = get_random_team()

game = Game(attack_team, defense_team)
game.process()
print(game.teams())
print(game.log.text)

sim = Sim(attack_team, defense_team)
sim.process()

# profile = cProfile.Profile()
# profile.enable()
# for i in range(20):
#     attack_team = get_random_team()
#     defense_team = get_random_team()
#     sim = Sim(attack_team, defense_team, n_sim=1000)
#     sim.process()
# profile.disable()
# profile.print_stats(sort='tottime')

# todo:
# connect the engine to the server
# add all heroes
# set stats depending on the hero level

# add empty runes/artifacts
# check : can dots crit?
# see which familiar attacks first
# make sure crit_damage > 0, armor_break > 0 (or not? check)
# check every behaviour marked with "check" comments
