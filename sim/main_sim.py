import numpy as np

from heroes import Team, HeroList
from models import Armor, Helmet, Weapon, Pendant, Rune, Artifact
from sim import Game

team_1 = Team([HeroList.reaper(), HeroList.reaper(), HeroList.reaper(), 
            HeroList.reaper(), HeroList.reaper(), HeroList.reaper()])
team_2 = Team([HeroList.reaper(), HeroList.reaper(), HeroList.reaper(), 
            HeroList.reaper(), HeroList.reaper(), HeroList.reaper()])

c0 = 0
c1 = 0
for i in range(1000):
    game = Game(team_1, team_2)
    game.process()
    if game.winner == 0:
        c0 += 1
    else :
        c1 += 1
    # print(game.log)
print('Team 1 winrate : {}%'.format(10 * c0))

# for i in range(20):
#     target = team_2.next_target()
#     last_hp = target.hp
#     scarlet_1.turn(team_1, team_2)
#     print('{} was attacked by {} and lost {} hp. She has {} hp left.'
#         .format(target.name.value, scarlet_1.name.value, 
#         round(last_hp - target.hp), 
#         round(target.hp)))
#     print(np.array([[team_1.heroes[0].hp, team_1.heroes[1].hp, team_1.heroes[2].hp], 
#                     [team_1.heroes[3].hp, team_1.heroes[4].hp, team_1.heroes[5].hp]]).astype(int))
#     print(np.array([[team_2.heroes[0].hp, team_2.heroes[1].hp, team_2.heroes[2].hp], 
#                     [team_2.heroes[3].hp, team_2.heroes[4].hp, team_2.heroes[5].hp]]).astype(int))
#     print()
# 
# reaper = HeroList.reaper(armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
#                     rune=Rune.hp.P3, artifact=Artifact.soul_torrent.O5)
# centaur = HeroList.centaur(armor=Armor.empty, helmet=Helmet.empty, weapon=Weapon.empty, pendant=Pendant.empty, 
#                     rune=Rune.crit_damage.O1, artifact=Artifact.empty)
# stonecutter = HeroList.stonecutter()
# 
# team_1 = Team([centaur, HeroList.empty, HeroList.empty, 
#             HeroList.empty, HeroList.empty, HeroList.empty])
# team_2 = Team([stonecutter, HeroList.empty, HeroList.empty, 
#             HeroList.empty, HeroList.empty, HeroList.empty])
# 
# reaper.turn(team_1, team_2)
# print(np.array([[team_1.heroes[0].hp, team_1.heroes[1].hp, team_1.heroes[2].hp], 
#                 [team_1.heroes[3].hp, team_1.heroes[4].hp, team_1.heroes[5].hp]]).astype(int))
# print(np.array([[team_2.heroes[0].hp, team_2.heroes[1].hp, team_2.heroes[2].hp], 
#                 [team_2.heroes[3].hp, team_2.heroes[4].hp, team_2.heroes[5].hp]]).astype(int))
# print()
