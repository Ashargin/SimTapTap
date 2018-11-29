import random as rd


def targets_at_random(heroes, n):
    alive = [h for h in heroes if not h.is_dead]
    targets = alive
    if len(alive) > n:
        idxs = list(range(len(alive)))
        rd.shuffle(idxs)
        targets = [alive[i] for i in idxs[:n]]

    return targets


def format_stats(stats, pet=False):
    for stat in ('damage_by_skill', 'damage_by_target', 'damage_taken_by_skill',
                'damage_taken_by_source','healing_by_skill', 'healing_by_target', 
                'healing_taken_by_skill', 'healing_taken_by_source'):
        data = stats[stat]
        data['Total'] = sum(data[key] for key in data.keys())
        stats[stat] = {key: round(data[key]) for key in data}
    stats['damage'] = stats['damage_by_skill']['Total']
    stats['healing'] = stats['healing_by_skill']['Total']
    stats['damage_taken'] = stats['damage_taken_by_skill']['Total']
    stats['healing_taken'] = stats['healing_taken_by_skill']['Total']

    return stats
