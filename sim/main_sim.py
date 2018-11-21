import numpy as np

from heroes import Team, Hero
from models import Armor, Helmet, Weapon, Pendant, Rune, Artifact, Familiar
from sim import Sim, Game

team_1 = Team([Hero.gerald() for i in range(6)])
team_2 = Team([Hero.freya() for i in range(6)])

game = Game(team_1, team_2)
game.process()
print(game.log)

sim = Sim(team_1, team_2, n_sim=1000)
sim.process()
sim.print_winrate()

# priority:
# check that atk boosts are multiplicative between skills and additive beneath skills, even for atk_down
# (maybe atk_down is multiplicative between stacks of the same skill?)
# make sure atk > 0 (and crit damage > 0, or > 0.5, and armor break > 0?)

# todo:
# add all heroes

# kind of minor : check every behaviour marked with "check" comments
# minor : store stats during battles, display graphs
