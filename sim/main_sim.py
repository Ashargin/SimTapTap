import numpy as np
import random as rd

from sim.heroes import Team, DummyTeam, Hero
from sim.models import Armor, Helmet, Weapon, Pendant, Rune, Artifact, Familiar
from sim.sim import Sim, Game

heroes = [Hero.abyss_lord, Hero.aden, Hero.blood_tooth, Hero.centaur, Hero.chessia, 
        Hero.dziewona, Hero.freya, Hero.gerald, Hero.grand, Hero.hester, Hero.lexar, Hero.luna, 
        Hero.mars, Hero.martin, Hero.medusa, Hero.megaw, Hero.minotaur, Hero.monkey_king, 
        Hero.mulan, Hero.nameless_king, Hero.orphee, Hero.reaper, Hero.ripper, Hero.rlyeh, 
        Hero.samurai, Hero.saw_machine, Hero.scarlet, Hero.shudde_m_ell, Hero.tesla, 
        Hero.tiger_king, Hero.ultima, Hero.vegvisir, Hero.verthandi, Hero.vivienne, 
        Hero.werewolf, Hero.wolf_rider, Hero.wolnir]


def get_random_team():
    team_heroes = []
    for i in range(6):
        team_heroes.append(heroes[rd.randint(0, len(heroes) - 1)]())
    return Team(team_heroes)


attack_team = get_random_team()
defense_team = get_random_team()

game = Game(attack_team, defense_team)
print(game.teams())
game.process()
print(game.log.text)

sim = Sim(attack_team, defense_team)
sim.process()

# todo:
# connect the engine to the server
# add all heroes
# re-check all heroes
# set stats depending on the hero level

# add empty runes/artifacts
# check : can dots crit?
# see which familiar attacks first
# make sure crit_damage > 0, armor_break > 0 (or not? check)
# check every behaviour marked with "check" comments

# for each hero : check skills values and behaviour
#                 write things to be checked
#                 check every action is written
#                 rewrite stats
