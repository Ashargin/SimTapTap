from heroes import Team, Scarlet

scarlet_1 = Scarlet()
team_1 = Team([scarlet_1, Scarlet(), Scarlet(), Scarlet(), Scarlet(), Scarlet()])

scarlet_2 = Scarlet()
team_2 = Team([scarlet_2, Scarlet(), Scarlet(), Scarlet(), Scarlet(), Scarlet()])

for i in range(20):
    target = team_2.next_target()
    last_hp = target.hp
    scarlet_1.turn(team_1, team_2)
    print('{} was attacked by {} and lost {} hp. She has {} hp left.'
        .format(target.name.value, scarlet_1.name.value, 
        round(last_hp - target.hp), 
        round(target.hp)))
