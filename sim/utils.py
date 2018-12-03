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
    for stat in ('damage_by_skill', 'damage_by_target', 'damage_taken_by_skill', 'damage_taken_by_source', 
                'effective_healing_by_skill', 'effective_healing_by_target', 
                'effective_healing_taken_by_skill', 'effective_healing_taken_by_source', 
                'healing_by_skill', 'healing_by_target', 'healing_taken_by_skill', 
                'healing_taken_by_source'):
        data = stats[stat]
        data['Total'] = sum(data[key] for key in data.keys())
        stats[stat] = {key: round(data[key]) for key in data}
    stats['damage'] = stats['damage_by_skill']['Total']
    stats['healing'] = stats['healing_by_skill']['Total']
    stats['effective_healing'] = stats['effective_healing_by_skill']['Total']
    stats['damage_taken'] = stats['damage_taken_by_skill']['Total']
    stats['effective_healing_taken'] = stats['effective_healing_taken_by_skill']['Total']
    stats['healing_taken'] = stats['healing_taken_by_skill']['Total']

    return stats


def add_dicts(dict_1, dict_2): # dict_1 will be modified, dict_2 won't
    for key in dict_2:
        if key in dict_1:
            if isinstance(dict_2[key], int):
                dict_1[key] += dict_2[key]
            else:
                dict_1[key] = add_dicts(dict_1[key], dict_2[key])
        else:
            dict_1[key] = dict_2[key]     

    return dict_1


def rescale_dict(mydict, scale): # modifies mydict
    for key in mydict:
        if isinstance(mydict[key], int):
            mydict[key] = round(mydict[key] * scale, 2)
            if key in ('damage', 'effective_healing', 'healing', 'damage_taken', 
                                    'effective_healing_taken', 'healing_taken'):
                mydict[key] = round(mydict[key])
        else:
            new_val = rescale_dict(mydict[key], scale)
            new_val = {k: round(new_val[k]) for k in new_val}
            mydict[key] = new_val

    return mydict
