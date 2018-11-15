import random as rd
from dataclasses import dataclass

from models import Faction, HeroType, HeroName, Equipment, Armor, Helmet, Weapon, Pendant, Rune, Artifact, Aura, Effect
from settings import guild_tech_maxed, guild_tech_empty


class Team:
    def __init__(self, heroes):   
        self.heroes = heroes
        for i, h in enumerate(self.heroes):
            h.pos = i

        aura = Aura(heroes) # aura
        self.compute_aura(aura)

        for h in self.heroes:
            h.hp_max = h.hp
            h.own_team = self

    def compute_aura(self, aura):
        for h in self.heroes:
            h.atk *= (1 + aura.atk_bonus)
            h.hp *= (1 + aura.hp_bonus)
            h.dodge += aura.dodge
            h.crit_rate += aura.crit_rate
            h.control_immune += aura.control_immune
            h.armor_break *= (1 + aura.armor_break_bonus)

    def next_target(self):
        alive = [h for h in self.heroes if not h.is_dead]

        return alive[0]

    def is_dead(self):
        return True if all([h.is_dead for h in self.heroes]) else False


class Hero:
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

    own_team = None
    op_team = None
    game = None
    pos = None
    is_dead = False
    can_attack = True

    def __init__(self, armor, helmet, weapon, pendant, rune, artifact, guild_tech):
        self.energy = 50
        self.effects = []
        self.compute_items(armor, helmet, weapon, pendant, rune, artifact)
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

    def faction_bonus(self, target):
        faction_bonus = False
        if self.faction == Faction.ALLIANCE and target.faction == Faction.HORDE:
            faction_bonus = True
        elif self.faction == Faction.HORDE and target.faction == Faction.ELF:
            faction_bonus = True
        elif self.faction == Faction.ELF and target.faction == Faction.UNDEAD:
            faction_bonus = True
        elif self.faction == Faction.UNDEAD and target.faction == Faction.ALLIANCE:
            faction_bonus = True
        elif self.faction == Faction.HEAVEN and target.faction == Faction.HELL:
            faction_bonus = True
        elif self.faction == Faction.HELL and target.faction == Faction.HEAVEN:
            faction_bonus = True

        return faction_bonus

    def type_damage(self, target):
        if target.type == HeroType.WARRIOR:
            return self.damage_to_warriors
        elif target.type == HeroType.ASSASSIN:
            return self.damage_to_assassins
        elif target.type == HeroType.WANDERER:
            return self.damage_to_wanderers
        elif target.type == HeroType.CLERIC:
            return self.damage_to_clerics
        elif target.type == HeroType.MAGE:
            return self.damage_to_mages

    def compute_damage(self, target, power, skill=False):
        faction_damage = 0
        if self.faction_bonus(target):
            faction_damage = 0.3

        type_damage = self.type_damage(target)

        crit_damage = 0
        if rd.random() <= self.crit_rate:
            crit_damage = self.crit_damage

        op_armor = target.armor - self.armor_break # check armor break behaviour
        damage_reduction_from_armor = (op_armor + 11) / 91 # check armor behaviour

        skill_damage = 0
        if skill:
            skill_damage = self.skill_damage

        dmg = power * (1 - damage_reduction_from_armor) * (1 + crit_damage) \
                    * (1 + self.true_damage) * (1 - target.damage_reduction) \
                    * (1 + faction_damage) * (1 + type_damage) * (1 + skill_damage)
                    # check faction damage behaviour
                    # check type damage behaviour
                    # check skill damage behaviour

        damage_components = {'Power': power, 
                            'Damage reduction from armor': damage_reduction_from_armor, 
                            'Crit damage': crit_damage, 
                            'True damage': self.true_damage, 
                            'Damage reduction': target.damage_reduction, 
                            'Faction damage': faction_damage, 
                            'Type damage': type_damage, 
                            'Skill damage': skill_damage, 
                            'Total damage': dmg}

        return damage_components

    def compute_dodge(self, target):
        dodged = False
        hit_rate = self.hit_rate
        if self.faction_bonus(target):
            hit_rate += 0.15
        if rd.random() <= target.dodge - hit_rate and not target.is_dead: # check dodge behaviour
            dodged = True

        return dodged

    def turn(self):
        if self.energy == 100:
            self.skill()
        else:
            self.attack()
        self.can_attack = False

    def attack(self, target=None, power=None):
        if target is None:
            target = self.op_team.next_target()
        if power is None:
            power = self.atk

        dodged = self.compute_dodge(target)
        if not dodged:
            self.hit(target, power=power, on_attack=True, on_hit=True, name='attack')

    def skill(self):
        self.energy = 0

    def hit(self, target, power, skill=False, on_attack=False, on_hit=False, name=''):
        if not target.is_dead:
            damage_components = self.compute_damage(target, power, skill=skill)
            dmg = damage_components['Total damage']
            crit = True if damage_components['Crit damage'] > 0 else False
            crit_str = ', crit' if crit else ''

            target.hp -= dmg
            log_text = '\n{} takes {} damage from {} ({}{})' \
                        .format(target.str_id, round(dmg), self.str_id, name, crit_str)
            self.game.log += log_text
            target.has_taken_damage(self)
            if on_attack:
                self.on_attack(target)
            if on_hit:
                target.on_hit(self)

    def poison(self, target, power, turns, skill=False, name=''):
        if not target.is_dead:
            poison = Effect.poison(self, target, power, turns, skill=skill, name=name)
            target.effects.append(poison)
            poison.tick()

    def has_taken_damage(self, attacker):
        if self.hp <= 0:
            self.kill()
            attacker.on_kill(self)
            self.on_death(attacker)

    def kill(self):
        self.is_dead = True
        self.can_attack = False
        self.effects = []
        self.game.log += '\n{} dies'.format(self.str_id)

    def on_attack(self, target):
        self.energy = min(self.energy + 50, 100)

    def on_hit(self, attacker):
        self.energy = min(self.energy + 10, 100)

    def on_kill(self, target):
        pass

    def on_death(self, attacker):
        pass

    def print_stats(self):
        stats = [self.hp, self.atk, self.armor, self.speed, 
                self.armor_break, self.skill_damage, self.hit_rate, self.dodge, 
                self.crit_rate, self.crit_damage - 0.5, self.true_damage, self.damage_reduction, 
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


class EmptyHero(Hero):
    name = HeroName.EMPTY
    faction = Faction.EMPTY
    type = HeroType.EMPTY

    hp = 0
    atk = 0
    armor = 0
    speed = 0
    is_dead = True
    can_attack = False

    def __init__(self):
        pass


class Centaur(Hero):
    name = HeroName.CENTAUR
    faction = Faction.ELF
    type = HeroType.WANDERER

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.queens_crown.O5, 
                    guild_tech=guild_tech_maxed):
        if tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 250108.46 # should depend on the level
        self.atk = 15053.54 # should depend on the level
        self.armor = 10 # should depend on the level
        self.speed = 983 # should depend on the level
        self.crit_rate += 0.4
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech)
        self.atk *= 1.3


class Reaper(Hero):
    name = HeroName.REAPER
    faction = Faction.UNDEAD
    type = HeroType.MAGE

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.soul_torrent.O5, 
                    guild_tech=guild_tech_maxed):
        if tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 201719.98 # should depend on the level
        self.atk = 16276.31 # should depend on the level
        self.armor = 8 # should depend on the level
        self.speed = 984 # should depend on the level
        self.armor_break = 9.6
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech)
        self.hp *= 1.3
        self.atk *= 1.3


class Scarlet(Hero):
    name = HeroName.SCARLET
    faction = Faction.HORDE
    type = HeroType.MAGE

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.primeval_soul.O5, 
                    guild_tech=guild_tech_maxed):
        if tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 177925.38 # should depend on the level
        self.atk = 18157.38 # should depend on the level
        self.armor = 9 # should depend on the level
        self.speed = 984 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech)

    def skill(self):
        name = 'Poison Nova'
        for target in self.op_team.heroes:
            dodged = self.compute_dodge(target)
            if not dodged:
                hit_power = self.atk * 0.42
                poison_power = self.atk * 0.6

                self.hit(target, power=hit_power, skill=True, on_hit=True, name=name) # sequence order?
                self.poison(target, power=poison_power, turns=3, skill=True, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Poison Touch'
        power = self.atk * 0.7
        if self.star >= 7:
            power = self.atk * 0.8
        if rd.random() <= 0.8:
            self.poison(target, power=power, turns=2, name=name)
        super().on_attack(target)

    def on_hit(self, attacker):
        name = 'Corrosive Skin'
        power = self.atk * 0.54
        if self.star >= 9:
            power = self.atk * 0.62
        if rd.random() <= 0.6:
            self.poison(attacker, power=power, turns=3, name=name)
        super().on_hit(attacker)

    def on_death(self, attacker):
        name = 'Malefic'
        power = self.atk * 0.63
        if self.star >= 8:
            power = self.atk * 0.85
        for h in self.op_team.heroes:
            self.poison(h, power=power, turns=3, name=name)
        super().on_death(attacker)


class Stonecutter(Hero):
    name = 'Stonecutter'    
    faction = Faction.ALLIANCE
    type = HeroType.WANDERER

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.empty, helmet=Helmet.empty, weapon=Weapon.empty, pendant=Pendant.empty, 
                    rune=Rune.empty, artifact=Artifact.empty, 
                    guild_tech=guild_tech_empty):
        if tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 162 # should depend on the level
        self.atk = 39 # should depend on the level
        self.armor = 7 # should depend on the level
        self.speed = 118 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech)


@dataclass
class HeroList:
    empty = EmptyHero()
    centaur = Centaur
    reaper = Reaper
    scarlet = Scarlet
    stonecutter = Stonecutter
