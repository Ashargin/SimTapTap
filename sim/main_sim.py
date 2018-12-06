import numpy as np
import random as rd

from sim.heroes import Team, DummyTeam, Hero
from sim.models import Armor, Helmet, Weapon, Pendant, Rune, Artifact, Familiar
from sim.sim import GameSim, GauntletAttackSim, GauntletDefenseSim, GauntletSim, Game
from sim.tests import friend_boss_test, guild_boss_test, trial_test

heroes = [Hero.abyss_lord, Hero.aden, Hero.blood_tooth, Hero.centaur, Hero.chessia, 
        Hero.dziewona, Hero.freya, Hero.gerald, Hero.grand, Hero.hester, Hero.lexar, Hero.luna, 
        Hero.mars, Hero.martin, Hero.medusa, Hero.megaw, Hero.minotaur, Hero.monkey_king, 
        Hero.mulan, Hero.nameless_king, Hero.orphee, Hero.reaper, Hero.ripper, Hero.rlyeh, 
        Hero.samurai, Hero.saw_machine, Hero.scarlet, Hero.shudde_m_ell, Hero.tesla, 
        Hero.tiger_king, Hero.ultima, Hero.vegvisir, Hero.verthandi, Hero.vivienne, 
        Hero.werewolf, Hero.wolf_rider, Hero.wolnir]

hero = Hero.werewolf
for pos in [1, 2, 3, 4, 5, 6]:
    print(pos)
    sim, damage = guild_boss_test(hero, pos=pos, n_sim=100)
    print(damage)
    sim.print_stats('damage_by_skill')
sim, damage = friend_boss_test(Hero.ripper, pos=3, n_sim=3000)

for pos in [1, 2, 3, 4, 5, 6]:
    if pos == 1:
        sim, winrate = trial_test(hero, pos=pos, n_sim=1000, tank=True)
        print('Pos = {}{} : {}'.format(pos, ' (solo tank)', winrate))
    sim, winrate = trial_test(hero, pos=pos, n_sim=1000, tank=False)
    print('Pos = {}{} : {}'.format(pos, '', winrate))

# todo:
# connect the engine to the server
# add all heroes
# re-check all heroes
# set stats depending on the hero level
# tier list : pvp, trial, expedition, guild boss OK, friend boss OK

# add empty runes/artifacts
# check : can dots crit?
# see which familiar attacks first
# make sure crit_damage > 0, armor_break > 0 (or not? check)
# check every behaviour marked with "check" comments

# for each hero : check skills values and behaviour
#                 write things to be checked
#                 check every action is written
#                 rewrite stats DONE (recheck)
#                 check names conflicts (this_name)
# then :          re-check rune/artifact

# Wolnir : Bone Pact : including self? including skills? even when dodged?
# Abyss Lord : Abyssal Blade : cannot be dodged?
# Aden : Strangle : cannot be dodged?
# Blood Tooth : Power Torture : cannot be dodged?
# Centaur : Dual Throwing Axe : 3-turns dot? (or 2)
# Chessia : Black Hole Generated : 4-turns bleed? 4-turns skill_damage_up?
# Dziewona : Spider Attack : dot only to mages or everyone? can be dodged?      PRIORITY
# Freya : Hollow Descent : energy decreased or drained?
