from models import Faction, HeroType, HeroName, Equipment, Armor, Helmet, Weapon, Pendant, Rune, Artifact, Aura


def set_team(heroes, guild_tech):
    warriors = [h for h in heroes if h.type == HeroType.WARRIOR] # guild tech
    assassins = [h for h in heroes if h.type == HeroType.ASSASSIN]
    wanderers = [h for h in heroes if h.type == HeroType.WANDERER]
    clerics = [h for h in heroes if h.type == HeroType.CLERIC]
    mages = [h for h in heroes if h.type == HeroType.MAGE]
    for h in warriors:
        h.hp *= (1 + guild_tech[0][0] / 200)
        h.atk *= (1 + guild_tech[1][0] / 200)
        h.crit_rate += guild_tech[2][0] / 200
        h.dodge += guild_tech[3][0] / 200
        h.skill_damage += guild_tech[4][0] / 100
    for h in assassins:
        h.hp *= (1 + guild_tech[0][1] / 200)
        h.atk *= (1 + guild_tech[1][1] / 200)
        h.crit_rate += guild_tech[2][1] / 200
        h.armor_break += guild_tech[3][1] * 0.15
        h.skill_damage += guild_tech[4][1] / 100
    for h in wanderers:
        h.hp *= (1 + guild_tech[0][2] / 200)
        h.atk *= (1 + guild_tech[1][2] / 200)
        h.dodge += guild_tech[2][2] / 200
        h.hit_rate += guild_tech[3][2] / 200
        h.skill_damage += guild_tech[4][2] / 100
    for h in clerics:
        h.hp *= (1 + guild_tech[0][3] / 200)
        h.dodge += guild_tech[1][3] / 200
        h.crit_rate += guild_tech[2][3] / 200
        h.speed += guild_tech[3][3] * 2
        h.skill_damage += guild_tech[4][3] / 100
    for h in mages:
        h.hp *= (1 + guild_tech[0][4] / 200)
        h.atk *= (1 + guild_tech[1][4] / 200)
        h.crit_rate += guild_tech[2][4] / 200
        h.hit_rate += guild_tech[3][4] / 200
        h.skill_damage += guild_tech[4][4] / 100

    aura = Aura(heroes) # aura
    for h in heroes:
        h.atk *= (1 + aura.atk_bonus)
        h.hp *= (1 + aura.hp_bonus)
        h.dodge += aura.dodge
        h.crit_rate += aura.crit_rate
        h.armor_break *= (1 + aura.armor_break_bonus)
        h.control_immune += aura.control_immune


class Hero:
    dodge = 0
    hit_rate = 0
    skill_damage = 0
    crit_rate = 0
    armor_break = 0
    control_immune = 0
    damage_to_warriors = 0
    damage_to_assassins = 0
    damage_to_wanderers = 0
    damage_to_clerics = 0
    damage_to_mages = 0

    def __init__(self, armor, helmet, weapon, pendant, rune, artifact):
        equipment = Equipment(armor, helmet, weapon, pendant) # equipment
        self.hp += equipment.hp
        self.atk += equipment.atk
        self.hp += rune.hp # rune
        self.atk += rune.atk
        self.hp += artifact.hp # artifact
        self.atk += artifact.atk
        self.hp *= (1 + equipment.hp_bonus)
        self.atk *= (1 + equipment.atk_bonus)
        self.hp *= (1 + rune.hp_bonus)
        self.atk *= (1 + rune.atk_bonus)
        self.hp *= (1 + artifact.hp_bonus)
        self.atk *= (1 + artifact.atk_bonus)
        self.damage_to_warriors += artifact.damage_to_warriors
        self.damage_to_assassins += artifact.damage_to_assassins
        self.damage_to_wanderers += artifact.damage_to_wanderers
        self.damage_to_clerics += artifact.damage_to_clerics
        self.damage_to_mages += artifact.damage_to_mages

    def on_death(self, attacker, allies, enemies):
        pass

    def on_kill(self, target, allies, enemies):
        pass

    def on_hit(self, attacker, allies, enemies):
        pass

    def on_attack(self, target, allies, enemies):
        pass


class Scarlet(Hero): # heroes are assumed to be at least 6-star and tier 6 for now
    name = HeroName.SCARLET
    faction = Faction.HORDE
    type = HeroType.MAGE

    def __init__(self, star=9, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.wanderer.O5):
        self.hp = 10000 # should depend on the level
        self.atk = 1000 # should depend on the level
        self.armor = 10 # should depend on the level
        self.speed = 100 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact)

    def on_death(self, attacker, allies, enemies):
        atk_perc = 0
        if star >= 8:
            atk_perc = 0.85
        else:
            atk_perc = 0.63

        # implement scarlet's on-death effect
        pass

    def on_hit(self, attacker, allies, enemies):
        # implement scarlet's on-hit effect
        pass
