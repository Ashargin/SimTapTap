import random as rd
import pandas as pd
import click

from sim.heroes import Team, DummyTeam, Hero
from sim.models import Armor, Helmet, Weapon, Pendant, Rune, Artifact, Familiar
from sim.processing import GameSim, GauntletAttackSim, GauntletDefenseSim, GauntletSim, Game
from sim.tests import friend_boss_test, main_friend_boss_test, guild_boss_test, \
                    main_guild_boss_test, trial_test, main_trial_test, pvp_test, sim_setup
from sim.gauntlets import generate_all_samples

heroes = [Hero.abyss_lord, Hero.aden, Hero.blood_tooth, Hero.centaur, Hero.chessia, 
        Hero.dziewona, Hero.freya, Hero.gerald, Hero.grand, Hero.hester, Hero.lexar, Hero.lindberg,
        Hero.luna, Hero.mars, Hero.martin, Hero.medusa, Hero.megaw, Hero.minotaur, 
        Hero.monkey_king, Hero.mulan, Hero.nameless_king, Hero.orphee, Hero.reaper, Hero.ripper, 
        Hero.rlyeh, Hero.samurai, Hero.saw_machine, Hero.scarlet, Hero.shudde_m_ell, Hero.tesla, 
        Hero.tiger_king, Hero.ultima, Hero.vegvisir, Hero.verthandi, Hero.vivienne, 
        Hero.werewolf, Hero.wolf_rider, Hero.wolnir, Hero.xexanoth]

@click.group()
def cli():
    pass

@click.command(name='sim-params')
@click.option('--time', default=4.0)
def sim_params_cmd(time):
    n_sim = max(10 * (round(267 * time) // 10), 10)
    print('Simulating batches of {} games\n'.format(n_sim))
    print('Generating random gauntlets for simulations\n')
    generate_all_samples()

    idx = []
    data = []
    for hero in heroes:
        this_pos, this_rune, this_art, score, pos_scores, rune_scores, art_scores = sim_setup(hero, n_sim=n_sim)
        idx.append(hero.name.value)
        data.append([this_pos] + [this_rune.__class__.__name__] +
                    [this_art.__class__.__name__] + [score] + pos_scores + rune_scores + art_scores)
        df = pd.DataFrame(data, index=idx, columns=['pos', 'rune', 'artifact', 'score', '1', '2', '3', '4', '5', '6', 'accuracy', 'armor_break', 'attack', 'crit_damage', 'crit_rate', 'evasion', 'hp', 'skill_damage', 'speed', 'vitality', 'dragonblood', 'eye_of_heaven', 'scorching_sun', 'wind_walker', 'extra_1', 'extra_2', 'extra_3'])
        df.to_excel(r'data/results.xlsx')

cli.add_command(sim_params_cmd)
if __name__ == '__main__':
    cli()

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
