import random as rd
import pandas as pd
import click
import multiprocessing as mp

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

# benchmark = Team([Hero.ultima(), Hero.scarlet(), Hero.monkey_king(), Hero.nameless_king(), Hero.reaper(), Hero.luna()])
# team1 = Team([Hero.monkey_king(), Hero.verthandi(), Hero.mars(), Hero.nameless_king(), Hero.chessia(), Hero.freya()])
# team2 = Team([Hero.ultima(), Hero.scarlet(), Hero.shudde_m_ell(), Hero.chessia(), Hero.luna(), Hero.mars()])
# team3 = Team([Hero.ultima(), Hero.verthandi(), Hero.saw_machine(), Hero.vegvisir(), Hero.luna(), Hero.mars()])
# team4 = Team([Hero.ultima(), Hero.verthandi(), Hero.martin(), Hero.vegvisir(), Hero.luna(), Hero.mars()])
# team5 = Team([Hero.monkey_king(), Hero.scarlet(), Hero.shudde_m_ell(), Hero.aden(), Hero.lexar(), Hero.freya()])

@click.group()
def cli():
    pass

@click.command(name='sim-params')
@click.option('--time', default=4.0)
@click.option('--cores', default=5)
@click.option('--async/--no-async', default=True)
def sim_params_cmd(time, cores, async):
    n_sim = max(10 * (round(267 * time) // 10), 10)
    print('Simulating batches of {} games\n'.format(n_sim))
    print('Generating random gauntlets for simulations\n')
    generate_all_samples()

    results = None
    if async:
        pool = mp.Pool(processes=cores)
        results = [pool.apply_async(sim_setup, args=(h, n_sim, False)) for h in heroes]
        results = [p.get() for p in results]
    else:
        results = [sim_setup(h, n_sim) for h in heroes]
    idx = []
    data = []
    for res in results:
        name, this_pos, this_rune, this_art, score, pos_scores, rune_scores, art_scores = res
        idx.append(name)
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
