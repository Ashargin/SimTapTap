import random as rd


def targets_at_random(team, n):
    alive = [h for h in team.heroes if not h.is_dead]
    targets = alive
    if len(alive) > n:
        idxs = list(range(len(alive)))
        rd.shuffle(idxs)
        targets = [alive[i] for i in idxs[:n]]

    return targets
