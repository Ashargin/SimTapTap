import pandas as pd
import click
import multiprocessing as mp

from sim.heroes import Hero
from sim.gauntlets import generate_all_samples
from sim.tests import pvp_test, sim_setup

heroes = [Hero.__dict__[key] for key in Hero.__dict__ if '__' not in key and 'empty' not in key]


@click.group()
def cli():
    pass


@click.command(name='sim-params')
@click.option('--time', default=4.0)
@click.option('--cores', default=7)
@click.option('--test-speed/--no-test-speed', default=False)
@click.option('--async/--no-async', default=True)
@click.option('--pos/--no-pos', default=True)
@click.option('--rune/--no-rune', default=True)
def sim_params_cmd(time, cores, test_speed, async, pos, rune):
    redo_pos = pos  # variable name
    redo_rune = rune  # variable name

    n_sim = max(10 * (round(267 * time) // 10), 10)
    print('Simulating batches of {} games\n'.format(n_sim))

    positions = dict(pd.read_excel('data/results_params.xlsx').pos)
    runes = dict(pd.read_excel('data/results_params.xlsx').rune)
    rune_encoder = {'AccuracyRuneR2': 0, 'ArmorBreakRuneR2': 1, 'AttackRuneR2': 2,
                    'CritDamageRuneR2': 3, 'CritRateRuneR2': 4, 'EvasionRuneR2': 5,
                    'HpRuneR2': 6, 'SkillDamageRuneR2': 7, 'SpeedRuneR2': 8, 'VitalityRuneR2': 9,
                    'StormAttackRuneR2': 10}
    encoded_runes = {key: rune_encoder[runes[key]] for key in runes}

    if redo_pos:
        positions = {key: None for key in positions}
    if redo_rune and not test_speed:
        encoded_runes = {key: None for key in encoded_runes}

    generate_all_samples()

    if async:
        pool = mp.Pool(processes=cores)
        results = [pool.apply_async(sim_setup, args=(h, positions[h.name.value], encoded_runes[h.name.value],
                                                     n_sim, test_speed, False)) for h in heroes]
        results = [p.get() for p in results]
    else:
        results = [sim_setup(h, positions[h.name.value], encoded_runes[h.name.value], n_sim, test_speed)
                   for h in heroes]
    idx = []
    data = []
    for res in results:
        name, this_pos, this_rune, this_art, this_second_art, score, pos_scores, rune_scores, art_scores = res
        totg_score = art_scores[1]
        other_art_scores = art_scores[:1] + art_scores[2:3] + [0 if x == '' else x[0] for x in art_scores[3:]]
        totg_reliance = max(totg_score - max(other_art_scores), 0)
        totg_reliance = round(100 * totg_reliance, 1)
        idx.append(name)
        data.append([this_pos, this_rune.__name__, this_art.__name__, this_second_art.__name__, score] +
                    pos_scores + rune_scores + art_scores + [totg_reliance])
    df = pd.DataFrame(data, index=idx,
                      columns=['pos', 'rune', 'artifact', 'second_artifact', 'score', '1', '2', '3', '4', '5', '6',
                               'accuracy', 'armor_break', 'attack', 'crit_damage', 'crit_rate', 'evasion', 'hp',
                               'skill_damage', 'speed', 'vitality', 'storm_attack', 'dragonblood',
                               'tears_of_the_goddess', 'scorching_sun', 'extra_1', 'extra_2', 'extra_3',
                               'totg_reliance'])

    diffs_cols = ['pos', 'rune', 'artifact', 'second_artifact']
    diffs = df[diffs_cols] != pd.read_excel(r'data/results_params.xlsx')[diffs_cols]
    for c in diffs_cols:
        print('{}: \t{}/{} new'.format(c, diffs[c].sum(), diffs.shape[0]))

    df.to_excel(r'data/results_params.xlsx')


@click.command(name='sim-pvp')
@click.option('--sims', default=3000)
@click.option('--cores', default=7)
@click.option('--attack/--defense', default=True)
@click.option('--async/--no-async', default=True)
def sim_pvp_cmd(sims, cores, attack, async):
    n_sim = sims  # variable name
    print('Simulating batches of {} games\n'.format(n_sim))

    positions = dict(pd.read_excel('data/results_params.xlsx').pos)
    positions = {key: [positions[key]] for key in positions}
    runes = {key: [None] for key in positions}
    artifacts = {key: [None] for key in positions}

    generate_all_samples()

    if async:
        pool = mp.Pool(processes=cores)
        results = [pool.apply_async(pvp_test, args=(h, pos, runes[h.name.value][i],
                                                    artifacts[h.name.value][i], n_sim, attack))
                   for h in heroes for i, pos in enumerate(positions[h.name.value])]
        results = [p.get() for p in results]
    else:
        results = [pvp_test(h, pos, rune=runes[h.name.value][i], artifact=artifacts[h.name.value][i],
                            n_sim=n_sim, attack=attack) for h in heroes for i, pos in
                   enumerate(positions[h.name.value])]
    idx = []
    data = []
    for res in results:
        h, pos, sim, winrate = res
        name = h.name.value
        stats = sim.heroes[0].stats
        idx.append(name)
        data.append([winrate, stats['damage'], stats['effective_healing'],
                     stats['skills'], stats['hard_ccs'], stats['silences'],
                     stats['effective_hard_cc_turns_taken'] + stats['effective_silence_turns_taken'],
                     stats['dodges'], stats['kills'], stats['deaths'], stats['turns_alive']])
    df = pd.DataFrame(data, index=idx, columns=['winrate', 'damage',
                                                'effective_healing', 'skills', 'hard_ccs', 'silences',
                                                'turns_denied_hard_cc_or_silence', 'dodges',
                                                'kills', 'deaths', 'turns_alive'])
    df.insert(0, 'score', df.winrate.apply(lambda x: round((x - df.winrate.median()) * 800)))
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
# CHECK : energy on attack/skill : all targets?
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
