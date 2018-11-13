import random as rd

from models import Faction, HeroType, HeroName, Equipment, Armor, Helmet, Weapon, Pendant, Rune, Artifact, Aura
from settings import guild_tech_maxed


class Team:
    def __init__(self, heroes):   
        self.heroes = heroes
        for i, h in enumerate(self.heroes):
            h.pos = i

        aura = Aura(heroes) # aura
        compute_aura(aura)

    def compute_aura(self, aura):
        for h in self.heroes:
            h.pos = i

            h.atk *= (1 + aura.atk_bonus)
            h.hp *= (1 + aura.hp_bonus)
            h.dodge += aura.dodge
            h.crit_rate += aura.crit_rate
            h.control_immune += aura.control_immune
            h.armor_break *= (1 + aura.armor_break_bonus)

    def next_target(self):
        alive = [h for h in self.heroes if not h.is_dead]

        return alive[0]

class Hero:
    energy = 50
    armor_break = 0
    skill_damage = 0
    hit_rate = 0
    dodge = 0
    crit_rate = 0
    crit_damage = 0.5
    true_damage = 0
    damage_reduction = 0
    control_immune = 0
    damage_to_warriors = 0
    damage_to_assassins = 0
    damage_to_wanderers = 0
    damage_to_clerics = 0
    damage_to_mages = 0

    pos = None
    is_dead = False
    can_attack = True
    effects = []

    def __init__(self, armor, helmet, weapon, pendant, rune, artifact):
        self.compute_items(armor, helmet, weapon, pendant, rune, artifact)
        guild_tech = guild_tech_maxed # change this later
        self.compute_guild_tech(guild_tech)

    def compute_items(self, armor, helmet, weapon, pendant, rune, artifact):
        equipment = Equipment(armor, helmet, weapon, pendant) # equipment
        self.atk += equipment.atk
        self.hp += equipment.hp
        self.atk += rune.atk # rune
        self.hp += rune.hp
        self.armor_break += rune.armor_break
        self.skill_damage += rune.skill_damage
        self.hit_rate += rune.hit_rate
        self.dodge += rune.dodge
        self.crit_rate += rune.crit_rate
        self.crit_damage += rune.crit_damage
        self.energy += artifact.energy # artifact
        self.atk += artifact.atk
        self.hp += artifact.hp
        self.speed += artifact.speed
        self.hit_rate += artifact.hit_rate
        self.true_damage += artifact.true_damage
        self.damage_reduction += artifact.damage_reduction
        self.damage_to_warriors += artifact.damage_to_warriors
        self.damage_to_assassins += artifact.damage_to_assassins
        self.damage_to_wanderers += artifact.damage_to_wanderers
        self.damage_to_clerics += artifact.damage_to_clerics
        self.damage_to_mages += artifact.damage_to_mages
        if self.faction == Faction.ALLIANCE:
            self.skill_damage += artifact.skill_damage_if_alliance
        if self.faction == Faction.UNDEAD:
            self.skill_damage += artifact.skill_damage_if_undead
        if self.faction == Faction.HELL:
            self.skill_damage += artifact.skill_damage_if_hell
        if self.faction == Faction.HORDE:
            self.crit_rate += artifact.crit_rate_if_horde
        if self.faction == Faction.ELF:
            self.crit_rate += artifact.crit_rate_if_elf
        if self.faction == Faction.HEAVEN:
            self.true_damage += artifact.true_damage_if_heaven
        self.atk *= (1 + equipment.atk_bonus)
        self.hp *= (1 + equipment.hp_bonus)
        self.atk *= (1 + rune.atk_bonus)
        self.hp *= (1 + rune.hp_bonus)
        self.atk *= (1 + artifact.atk_bonus)
        self.hp *= (1 + artifact.hp_bonus)

    def compute_guild_tech(self, guild_tech):
        if self.type == HeroType.WARRIOR:
            self.hp *= (1 + guild_tech[0][0] / 200)
            self.atk *= (1 + guild_tech[1][0] / 200)
            self.crit_rate += guild_tech[2][0] / 200
            self.dodge += guild_tech[3][0] / 200
            self.skill_damage += guild_tech[4][0] / 100
        elif self.type == HeroType.ASSASSIN:
            self.hp *= (1 + guild_tech[0][1] / 200)
            self.atk *= (1 + guild_tech[1][1] / 200)
            self.crit_rate += guild_tech[2][1] / 200
            self.armor_break += guild_tech[3][1] * 0.15
            self.skill_damage += guild_tech[4][1] / 100
        elif self.type == HeroType.WANDERER:
            self.hp *= (1 + guild_tech[0][2] / 200)
            self.atk *= (1 + guild_tech[1][2] / 200)
            self.dodge += guild_tech[2][2] / 200
            self.hit_rate += guild_tech[3][2] / 200
            self.skill_damage += guild_tech[4][2] / 100
        elif self.type == HeroType.CLERIC:
            self.hp *= (1 + guild_tech[0][3] / 200)
            self.dodge += guild_tech[1][3] / 200
            self.crit_rate += guild_tech[2][3] / 200
            self.speed += guild_tech[3][3] * 2
            self.skill_damage += guild_tech[4][3] / 100
        elif self.type == HeroType.MAGE:
            self.hp *= (1 + guild_tech[0][4] / 200)
            self.atk *= (1 + guild_tech[1][4] / 200)
            self.crit_rate += guild_tech[2][4] / 200
            self.hit_rate += guild_tech[3][4] / 200
            self.skill_damage += guild_tech[4][4] / 100

    def turn(self, own_team, op_team):
        if energy >= 100:
            self.skill(own_team, op_team)
        else:
            self.attack(own_team, op_team)

    def attack(self, own_team, op_team, target=None, power=None):
        if target is None:
            target = op_team.next_target()
        if power is None:
            power = self.atk

        dodged = False
        if rd.random() <= target.dodge - self.hit_rate: # compute dodge/hit rate
            dodged = True
        if not dodged:
            crit_damage = 0
            if rd.random() <= self.crit_rate:
                crit_damage = self.crit_damage
            
            op_armor = target.armor - self.armor_break
            damage_reduction_from_armor = 0.011 * op_armor + 0.12
            dmg = power * (1 - damage_reduction_from_armor) * (1 + crit_damage) 
                        * (1 + self.true_damage) * (1 - target.damage_reduction)

            target.hp -= dmg
            target.has_taken_damage(self, op_team, own_team)
            self.on_attack(target, own_team, op_team)
            target.on_hit(self, op_team, own_team)

    def skill(self, own_team, op_team):
        self.energy = 0

    def has_taken_damage(self, attacker, own_team, op_team):
        if self.hp <= 0:
            self.is_dead = True
            self.kill()
            attacker.on_kill(self, op_team, own_team)
            self.on_death(attacker, own_team, op_team)

    def kill(self):
        self.can_attack = False
        self.effects = []

    def on_attack(self, target, own_team, op_team):
        self.energy += 50

    def on_hit(self, attacker, own_team, op_team):
        self.energy += 10

    def on_kill(self, target, own_team, op_team):
        pass

    def on_death(self, attacker, own_team, op_team):
        pass

    def print_stats(self):
        stats = [self.hp, self.atk, self.armor, self.speed, 
                self.armor_break, self.skill_damage, self.hit_rate, self.dodge, 
                self.crit_rate, self.crit_damage, self.true_damage, self.damage_reduction, 
                self.control_immune, self.damage_to_warriors, 
                self.damage_to_assassins, self.damage_to_wanderers, 
                self.damage_to_clerics, self.damage_to_mages]
        stats_names = ['Hp', 'Atk', 'Armor', 'Speed', 
                    'Armor break', 'Skill damage', 'Hit rate', 'Dodge', 
                    'Crit rate', 'Crit damage', 'True damage', 'Damage reduction', 
                    'Control immune', 'Damage to warriors', 
                    'Damage to assassins', 'Damage to wanderers', 
                    'Damage to clerics', 'Damage to mages']
        for stat, name in zip(stats, stats_names):
            print('{}\t{}'.format(name, stat))


class Scarlet(Hero):
    name = HeroName.SCARLET
    faction = Faction.HORDE
    type = HeroType.MAGE

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.primeval_soul.O5):
        if tier < 6:
            raise NotImplementedError

        self.hp = 177925.38 # should depend on the level
        self.atk = 18157.38 # should depend on the level
        self.armor = 9 # should depend on the level
        self.speed = 984 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact)

    def on_attack(self, target, own_team, op_team):
        super().on_attack(target, own_team, op_team)

    def on_death(self, attacker, own_team, op_team):
        atk_perc = 0
        if star >= 8:
            atk_perc = 0.85
        else:
            atk_perc = 0.63

        # implement scarlet's on-death effect
        pass

    def on_hit(self, attacker, own_team, op_team):
        # implement scarlet's on-hit effect
        pass
