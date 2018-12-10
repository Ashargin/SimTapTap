import random as rd

from sim.heroes import Team, DummyTeam, Hero
from sim.models import Armor, Helmet, Weapon, Pendant, Rune, Artifact, Familiar
from sim.sim import GameSim, GauntletAttackSim, GauntletDefenseSim, GauntletSim, Game
from sim.tests import friend_boss_test, main_friend_boss_test, guild_boss_test, \
                    main_guild_boss_test, trial_test, main_trial_test, pvp_test, sim_setup

heroes = [Hero.abyss_lord, Hero.aden, Hero.blood_tooth, Hero.centaur, Hero.chessia, 
        Hero.dziewona, Hero.freya, Hero.gerald, Hero.grand, Hero.hester, Hero.lexar, Hero.luna, 
        Hero.lindberg, Hero.mars, Hero.martin, Hero.medusa, Hero.megaw, Hero.minotaur, 
        Hero.monkey_king, Hero.mulan, Hero.nameless_king, Hero.orphee, Hero.reaper, Hero.ripper, 
        Hero.rlyeh, Hero.samurai, Hero.saw_machine, Hero.scarlet, Hero.shudde_m_ell, Hero.tesla, 
        Hero.tiger_king, Hero.ultima, Hero.vegvisir, Hero.verthandi, Hero.vivienne, 
        Hero.werewolf, Hero.wolf_rider, Hero.wolnir, Hero.xexanoth]

hero = Hero.abyss_lord
sim_setup(hero)

# todo:
# set prefered settings (rune/artifact)
# tier list : pvp (atk/def), trial, den, expedition, guild boss, friend boss
# friend boss : check level ==> speed (Alo), guild boss : check damage (Alo)
# pvp : set custom gauntlet

# connect the engine to the server
# set stats depending on the hero level
# add empty runes/artifacts

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
# Xexanoth : Weak Point Stealing : on_hit or on_attack?                                             IMPORTANT
