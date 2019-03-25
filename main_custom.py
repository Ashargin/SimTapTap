import pandas as pd
import click
import multiprocessing as mp

from sim.heroes import Team, DummyTeam, Hero
from sim.models import Armor, Helmet, Weapon, Pendant, Rune, Artifact, Familiar
from sim.processing import GameSim, GauntletAttackSim, GauntletDefenseSim, GauntletSim, Game
from sim.tests import friend_boss_test, main_friend_boss_test, master_friend_boss_test, guild_boss_test, \
                    main_guild_boss_test, master_guild_boss_test, trial_test, main_trial_test, pvp_test, sim_setup

heroes = [Hero.abyss_lord, Hero.aden, Hero.blood_tooth, Hero.centaur, Hero.chessia, Hero.drow,
        Hero.dziewona, Hero.freya, Hero.gerald, Hero.grand, Hero.hester, Hero.lexar, Hero.luna, 
        Hero.lindberg, Hero.mars, Hero.martin, Hero.medusa, Hero.megaw, Hero.minotaur, 
        Hero.monkey_king, Hero.mulan, Hero.nameless_king, Hero.orphee, Hero.phoenix, Hero.reaper, 
        Hero.ripper, Hero.rlyeh, Hero.samurai, Hero.saw_machine, Hero.scarlet, Hero.shudde_m_ell, 
        Hero.tesla, Hero.tiger_king, Hero.ultima, Hero.valkyrie, Hero.vegvisir, Hero.verthandi, 
        Hero.vivienne, Hero.werewolf, Hero.wolf_rider, Hero.wolnir, Hero.xexanoth]

team_1 = Team([Hero.phoenix(),
                Hero.ripper(),
                Hero.mulan(),
                Hero.rlyeh(),
                Hero.aden(),
                Hero.ultima()])
print('This is team_1 :\n', team_1.comp())

team_2 = Team([Hero.phoenix(),
                Hero.wolf_rider(),
                Hero.dziewona(),
                Hero.chessia(),
                Hero.grand(),
                Hero.tesla()])
print('This is team_2 :\n', team_2.comp())

game = Game(team_1, team_2, verbose_full=True)
game.process()
print(game.log.text)
