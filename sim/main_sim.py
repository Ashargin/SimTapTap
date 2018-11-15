import numpy as np

from heroes import Team, HeroList
from models import Armor, Helmet, Weapon, Pendant, Rune, Artifact
from sim import Sim, Game

team_1 = Team([HeroList.centaur(), HeroList.centaur(), HeroList.centaur(), 
            HeroList.centaur(), HeroList.centaur(), HeroList.centaur()])
team_2 = Team([HeroList.centaur(), HeroList.centaur(), HeroList.centaur(), 
            HeroList.centaur(), HeroList.centaur(), HeroList.centaur()])

game = Game(team_1, team_2)
game.process()
print(game.log)

sim = Sim(team_1, team_2, n_sim=1000)
sim.process()
sim.print_winrate()
