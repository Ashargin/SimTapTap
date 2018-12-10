import random as rd

from sim.heroes import Team, DummyTeam, Hero
from sim.models import Armor, Helmet, Weapon, Pendant, Rune, Artifact, Familiar
from sim.sim import GameSim, GauntletAttackSim, GauntletDefenseSim, GauntletSim, Game
from sim.tests import friend_boss_test, main_friend_boss_test, guild_boss_test, trial_test

heroes = [Hero.abyss_lord, Hero.aden, Hero.blood_tooth, Hero.centaur, Hero.chessia, 
        Hero.dziewona, Hero.freya, Hero.gerald, Hero.grand, Hero.hester, Hero.lexar, Hero.luna, 
        Hero.lindberg, Hero.mars, Hero.martin, Hero.medusa, Hero.megaw, Hero.minotaur, 
        Hero.monkey_king, Hero.mulan, Hero.nameless_king, Hero.orphee, Hero.reaper, Hero.ripper, 
        Hero.rlyeh, Hero.samurai, Hero.saw_machine, Hero.scarlet, Hero.shudde_m_ell, Hero.tesla, 
        Hero.tiger_king, Hero.ultima, Hero.vegvisir, Hero.verthandi, Hero.vivienne, 
        Hero.werewolf, Hero.wolf_rider, Hero.wolnir, Hero.xexanoth]

hero = Hero.abyss_lord
main_friend_boss_test(hero)
sim, damage = friend_boss_test(Hero.ripper, pos=3, n_sim=3000)

for pos in [1, 2, 3, 4, 5, 6]:
    if pos == 1:
        sim, winrate = trial_test(hero, pos=pos, n_sim=1000, tank=True)
        print('Pos = {}{} : {}'.format(pos, ' (solo tank)', winrate))
    sim, winrate = trial_test(hero, pos=pos, n_sim=1000, tank=False)
    print('Pos = {}{} : {}'.format(pos, '', winrate))

# todo:
# check questions
# set prefered settings (rune/artifact), set global armor/pet levels
# tier list : pvp, trial, expedition, guild boss OK, friend boss OK

# connect the engine to the server
# set stats depending on the hero level
# add empty runes/artifacts
# make sure crit_damage > 0, armor_break > 0 (or not? check)

# Aden 6* : Strangle : cannot be dodged?
# Dziewona : Spider Attack : dot only to mages or everyone?
# Freya : Hollow Descent : energy decreased or drained?
# Gerald : Wheel Of Torture : dot only to assassins or everyone?
# Lindberg : Cross Shelter : stun_immune?
# Mars : Miracle Of Resurrection : overkill?
# Nameless King : Lightning Storm : additional mark on skill or on first mark triggered?            IMPORTANT
# Scarlet : Poison Nova : poison or dot?
# Tiger King : Tiger Attack : dot or burn?
# Vivienne : Cleric Shine : 2 backline enemies?
# Wolnir : Bone Pact : even when dodged?
# Xexanoth : Weak Point Stealing : on_hit or on_attack?                                             PRIORITY
