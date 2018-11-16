import numpy as np

from heroes import Team, Hero
from models import Armor, Helmet, Weapon, Pendant, Rune, Artifact
from sim import Sim, Game

team_1 = Team([Hero.rlyeh() for i in range(6)])
team_2 = Team([Hero.saw_machine() for i in range(6)])

game = Game(team_1, team_2)
game.process()
print(game.log)

sim = Sim(team_1, team_2, n_sim=1000)
sim.process()
sim.print_winrate()

# write hot
# store stats, make graphs
