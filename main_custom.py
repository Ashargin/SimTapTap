from sim.heroes import Team, DummyTeam, Hero
from sim.models import Armor, Helmet, Weapon, Pendant, Rune, Artifact, Familiar
from sim.processing import GameSim, GauntletAttackSim, GauntletDefenseSim, GauntletSim, Game
from sim.tests import friend_boss_test, main_friend_boss_test, master_friend_boss_test, guild_boss_test, \
    main_guild_boss_test, master_guild_boss_test, trial_test, main_trial_test, pvp_test, sim_setup

# List heroes
heroes = [Hero.__dict__[key] for key in Hero.__dict__ if '__' not in key and 'empty' not in key]

# Create teams
team_1 = Team([Hero.phoenix(),
               Hero.valkyrie(),
               Hero.lindberg(),
               Hero.drow(artifact=Artifact.tears_of_the_goddess.O6),
               Hero.mars(artifact=Artifact.tears_of_the_goddess.O6),
               Hero.shudde_m_ell()])
print('This is team_1 :', team_1.comp())

team_2 = Team([Hero.phoenix(),
               Hero.valkyrie(),
               Hero.lindberg(),
               Hero.drow(artifact=Artifact.tears_of_the_goddess.O6),
               Hero.monkey_king(artifact=Artifact.tears_of_the_goddess.O6),
               Hero.shudde_m_ell()])
print('\nThis is team_2 :', team_2.comp())

# Do simulations
sim = GameSim(team_1, team_2, n_sim=3000)
sim.process()
sim.print_winrate()
