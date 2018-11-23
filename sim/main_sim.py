import numpy as np

from heroes import Team, Hero
from models import Armor, Helmet, Weapon, Pendant, Rune, Artifact, Familiar
from sim import Sim, Game

team_1 = Team([Hero.monkey_king() for i in range(6)])
team_2 = Team([Hero.reaper() for i in range(6)])

game = Game(team_1, team_2)
game.process()
print(game.log)

sim = Sim(team_1, team_2, n_sim=1000)
sim.process()
sim.print_winrate()

# todo:
# connect the engine to the server
# add all heroes

# set stats depending on the hero level
# make sure crit_damage > 0, armor_break > 0
# check timed_mark behaviour
# check if skill damage affects undirect skill damage
# check if stacks of attack_up from different sources, same skill, are multiplicative
# check if stacks of attack_up from different sources, different skill, are multiplicative
# check every behaviour marked with "check" comments
# store stats during battles, display graphs
