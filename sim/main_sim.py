import numpy as np

from heroes import Team, Hero
from models import Armor, Helmet, Weapon, Pendant, Rune, Artifact, Familiar
from sim import Sim, Game

team_1 = Team([Hero.centaur() for i in range(6)])
team_2 = Team([Hero.verthandi() for i in range(6)])

game = Game(team_1, team_2)
game.process()
print(game.log)

sim = Sim(team_1, team_2, n_sim=1000)
sim.process()
sim.print_winrate()

# todo:
# add familiar stats (familiar_stats = [26672, 1705] # add this)
# get real heroes stats (compare on different accounts with different familiar stats)
# add all heroes

# kind of minor : check every behaviour marked with "check" comments
# minor : store stats during battles, display graphs
