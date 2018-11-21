import numpy as np

from heroes import Team, Hero
from models import Armor, Helmet, Weapon, Pendant, Rune, Artifact, Familiar
from sim import Sim, Game

team_1 = Team([Hero.luna() for i in range(6)])
team_2 = Team([Hero.centaur() for i in range(6)])

game = Game(team_1, team_2)
game.process()
print(game.log)

sim = Sim(team_1, team_2, n_sim=1000)
sim.process()
sim.print_winrate()

# todo:
# get real heroes stats (compare on different accounts with different familiar stats) Saw done
# add all heroes

# kind of minor : check every behaviour marked with "check" comments
# minor : store stats during battles, display graphs

centaur-centaur 50.5/0.7/48.8
centaur-saw 93/0.5/6.5
centaur-reaper 0/42.4/57.6
centaur-rlyeh 88.5/0/11.5
centaur-scarlet 12/41.8/46.2

saw-saw 46/9.7/44.3
saw-reaper 13.6/34.8/51.6
saw-rlyeh 100/0/0
saw-scarlet 100/0/0

reaper-reaper 0/99.7/0.3
reaper-rlyeh 99.9/0/0.1
reaper-scarlet 81.4/18.6/0

rlyeh-rlyeh 0/100/0
rlyeh-scarlet 0/0/100

scarlet-scarlet 10.6/79.3/10.1
