import random as rd
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

benchmark = Team([Hero.wolf_rider(), Hero.shudde_m_ell(), Hero.valkyrie(), Hero.drow(), Hero.lindberg(), Hero.freya()])
# random = Team([rd.choice(heroes)() for i in range(6)])
team1 = Team([Hero.xexanoth(), Hero.verthandi(), Hero.chessia(), Hero.mars(), Hero.lindberg(), Hero.freya()])
# team2 = Team([Hero.xexanoth(), Hero.chessia(), Hero.chessia(), Hero.mars(), Hero.mars(), Hero.lindberg()])
# team3 = Team([Hero.verthandi(), Hero.mars(), Hero.mars(), Hero.lindberg(), Hero.lindberg(), Hero.lindberg()])


@click.group()
def cli():
    pass


@click.command(name='sim-params')
@click.option('--time', default=4.0)
@click.option('--cores', default=7)
@click.option('--async/--no-async', default=True)
@click.option('--pos/--no-pos', default=True)
@click.option('--rune/--no-rune', default=True)
def sim_params_cmd(time, cores, async, pos, rune):
    redo_pos = pos # variable name
    redo_rune = rune # variable name

    n_sim = max(10 * (round(267 * time) // 10), 10)
    print('Simulating batches of {} games\n'.format(n_sim))

    positions = dict(pd.read_excel('data/results_params.xlsx').pos)
    runes = dict(pd.read_excel('data/results_params.xlsx').rune)
    rune_encoder = {'AccuracyRuneR2': 0, 'ArmorBreakRuneR2': 1, 'AttackRuneR2': 2, 
                    'CritDamageRuneR2': 3, 'CritRateRuneR2': 4, 'EvasionRuneR2': 5, 
                    'HpRuneR2': 6, 'SkillDamageRuneR2': 7, 'SpeedRuneR2': 8, 'VitalityRuneR2': 9}
    encoded_runes = {key: rune_encoder[runes[key]] for key in runes}

    if redo_pos:
        positions = {key: None for key in positions}
    if redo_rune:
        encoded_runes = {key: None for key in encoded_runes}

    results = None
    if async:
        pool = mp.Pool(processes=cores)
        results = [pool.apply_async(sim_setup, args=(h, positions[h.name.value], 
                    encoded_runes[h.name.value], n_sim, False)) for h in heroes]
        results = [p.get() for p in results]
    else:
        results = [sim_setup(h, positions[h.name.value], encoded_runes[h.name.value], n_sim) for h in heroes]
    idx = []
    data = []
    for res in results:
        name, this_pos, this_rune, this_art, this_second_art, score, pos_scores, rune_scores, art_scores = res
        totg_score = art_scores[2]
        other_art_scores = art_scores[:2] + [art_scores[3]] + [0 if x == '' else x[0] for x in art_scores[4:]]
        totg_reliance = max(totg_score - max(other_art_scores), 0)
        totg_reliance = round(100 * totg_reliance, 1)
        idx.append(name)
        data.append([this_pos, this_rune.__class__.__name__, this_art.__class__.__name__, this_second_art.__class__.__name__, score] + 
                    pos_scores + rune_scores + art_scores + [totg_reliance])
    df = pd.DataFrame(data, index=idx, columns=['pos', 'rune', 'artifact', 'second_artifact', 'score', '1', '2', '3', '4', '5', '6', 'accuracy', 'armor_break', 'attack', 'crit_damage', 'crit_rate', 'evasion', 'hp', 'skill_damage', 'speed', 'vitality', 'dragonblood', 'bone_grip', 'tears_of_the_goddess', 'giant_lizard', 'extra_1', 'extra_2', 'extra_3', 'totg_reliance'])
    df.to_excel(r'data/results_params.xlsx')


@click.command(name='sim-pvp')
@click.option('--sims', default=3000)
@click.option('--cores', default=7)
@click.option('--attack/--defense', default=True)
@click.option('--async/--no-async', default=True)
def sim_pvp_cmd(sims, cores, attack, async):
    n_sims = sims # variable name
    print('Simulating batches of {} games\n'.format(n_sims))

    positions = dict(pd.read_excel('data/results_params.xlsx').pos)
    positions = {key: [positions[key]] for key in positions}
    runes = {key: [None] for key in positions}
    artifacts = {key: [None] for key in positions}
    results = None
    if async:
        pool = mp.Pool(processes=cores)
        results = [pool.apply_async(pvp_test, args=(h, pos, runes[h.name.value][i], 
                                artifacts[h.name.value][i], n_sims, attack)) 
                                for h in heroes for i, pos in enumerate(positions[h.name.value])]
        results = [p.get() for p in results]
    else:
        results = [pvp_test(h, pos, rune=runes[h.name.value][i], artifact=artifacts[h.name.value][i], 
                n_sim=n_sim, attack=attack) for h in heroes for i, pos in enumerate(positions[h.name.value])]
    idx = []
    data = []
    for res in results:
        h, pos, sim, winrate = res
        name = h.name.value
        rune = h().rune.__class__.__name__
        artifact = h().artifact.__class__.__name__
        stats = sim.heroes[0].stats
        idx.append(name)
        data.append([pos, rune, artifact, winrate, stats['damage'], stats['effective_healing'], 
                    stats['skills'], stats['hard_ccs'], stats['silences'], 
                    stats['effective_hard_cc_turns_taken'] + stats['effective_silence_turns_taken'], 
                    stats['dodges'], stats['kills'], stats['deaths'], stats['turns_alive']])
    df = pd.DataFrame(data, index=idx, columns=['pos', 'rune', 'artifact', 'winrate', 'damage', 
                'effective_healing', 'skills', 'hard_ccs', 'silences', 
                'turns_denied_hard_cc_or_silence', 'dodges', 
                'kills', 'deaths', 'turns_alive'])
    df.insert(1, 'score', df.winrate.apply(lambda x: round((x - df.winrate.median()) * 800)))
    if attack:
        df.to_excel(r'data/results_pvp_attack.xlsx')
    else:
        df.score = df.score.apply(lambda x: -x)
        df.to_excel(r'data/results_pvp_defense.xlsx')


cli.add_command(sim_pvp_cmd)
cli.add_command(sim_params_cmd)
if __name__ == '__main__':
    cli()

# todo:
# set prefered settings (rune/artifact)
# tier list : pvp (atk/def), trial, den, expedition, guild boss, friend boss

# connect the engine to the server
# set stats depending on the hero level
# add empty runes/artifacts

# Freya : Hollow Descent : energy decreased or drained?
# Mars : Miracle Of Resurrection : overkill?
# Nameless King : Lightning Storm : additional mark on skill or on first mark triggered?            IMPORTANT
# Vivienne : Cleric Shine : 2 backline enemies?
# Wolnir : Bone Pact : even when dodged?
# Xexanoth : Weak Point Stealing : before or after on_attack?                                       PRIORITY
