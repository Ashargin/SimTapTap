from heroes import set_team, Scarlet

guild_tech = [[0, 0, 0, 0, 0], 
              [0, 0, 0, 0, 0], 
              [0, 0, 0, 0, 0], 
              [0, 0, 0, 0, 0], 
              [0, 0, 0, 0, 0]]

scarlet = Scarlet()
print("Scarlet's example base hp is set to 10000")
print("Scarlet's hp with equipment, rune and artifact is", scarlet.hp)

set_team([scarlet, Scarlet(), Scarlet(), Scarlet(), Scarlet(), Scarlet()], guild_tech)
print('With 5 other Scarlets and the aura bonus, her hp is now', scarlet.hp)

guild_tech = [[60, 60, 60, 60, 60], 
              [50, 50, 50, 50, 50], 
              [40, 40, 40, 40, 40], 
              [30, 30, 30, 30, 30], 
              [20, 20, 20, 20, 20]]
scarlet = Scarlet()
set_team([scarlet, Scarlet(), Scarlet(), Scarlet(), Scarlet(), Scarlet()], guild_tech)
print('Adding the guild tech (maxed), her hp is', scarlet.hp)
