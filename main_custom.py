import pandas as pd
import click
import multiprocessing as mp

from sim.heroes import Team, DummyTeam, Hero
from sim.models import Armor, Helmet, Weapon, Pendant, Rune, Artifact, Familiar
from sim.processing import GameSim, GauntletAttackSim, GauntletDefenseSim, GauntletSim, Game
from sim.tests import friend_boss_test, main_friend_boss_test, master_friend_boss_test, guild_boss_test, \
                    main_guild_boss_test, master_guild_boss_test, trial_test, main_trial_test, pvp_test, sim_setup

heroes = [Hero.abyss_lord, Hero.aden, Hero.blood_tooth, Hero.centaur, Hero.chessia, Hero.drow,
        Hero.dziewona, Hero.freya, Hero.gerald, Hero.grand, Hero.hester, Hero.lexar, Hero.lindberg,
        Hero.luna, Hero.mars, Hero.martin, Hero.medusa, Hero.megaw, Hero.minotaur, 
        Hero.monkey_king, Hero.mulan, Hero.nameless_king, Hero.orphee, Hero.reaper, Hero.ripper, 
        Hero.rlyeh, Hero.samurai, Hero.saw_machine, Hero.scarlet, Hero.shudde_m_ell, Hero.tesla, 
        Hero.tiger_king, Hero.ultima, Hero.valkyrie, Hero.vegvisir, Hero.verthandi, Hero.vivienne, 
        Hero.werewolf, Hero.wolf_rider, Hero.wolnir, Hero.xexanoth]

team_1 = Team([Hero.abyss_lord(rune=Rune.hp.R2, artifact=Artifact.blood_medal.O6),
                Hero.aden(rune=Rune.evasion.R2, artifact=Artifact.soul_torrent.O6),
                Hero.mulan(rune=Rune.vitality.R2, artifact=Artifact.bone_grip.O6),
                Hero.verthandi(rune=Rune.speed.R2, artifact=Artifact.gift_of_creation.O6),
                Hero.xexanoth(rune=Rune.armor_break.R2, artifact=Artifact.eternal_curse.O6),
                Hero.centaur(rune=Rune.attack.R2, artifact=Artifact.fine_snow_dance.O6)])
print('This is team_1 :\n', team_1.comp())

team_2 = Team([Hero.scarlet(rune=Rune.hp.R2, artifact=Artifact.blood_medal.O6),
                Hero.shudde_m_ell(rune=Rune.evasion.R2, artifact=Artifact.soul_torrent.O6),
                Hero.saw_machine(rune=Rune.vitality.R2, artifact=Artifact.bone_grip.O6),
                Hero.mars(rune=Rune.speed.R2, artifact=Artifact.gift_of_creation.O6),
                Hero.freya(rune=Rune.armor_break.R2, artifact=Artifact.eternal_curse.O6),
                Hero.luna(rune=Rune.attack.R2, artifact=Artifact.fine_snow_dance.O6)])
print('This is team_2 :\n', team_2.comp())

game = Game(team_1, team_2)
game.process()
print('\nThis is a game between the two teams :\n', game.log.text)

sim = GameSim(team_1, team_2, n_sim=1000)
sim.process()
print('\nThis is the results over 1000 games :')
sim.print_winrate()