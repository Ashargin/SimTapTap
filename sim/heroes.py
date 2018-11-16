import random as rd
from dataclasses import dataclass

from models import Faction, HeroType, HeroName, Equipment, Armor, Helmet, Weapon, Pendant, Rune, Artifact, Aura, Effect
from settings import guild_tech_maxed, guild_tech_empty
from utils import targets_at_random


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


class BaseHero:
    def __init__(self, armor, helmet, weapon, pendant, rune, artifact, guild_tech):
        self.energy = 50
        self.armor_break = 0
        self.skill_damage = 0
        self.hit_rate = 0
        self.dodge = 0
        self.crit_rate = 0
        self.crit_damage = 0.5
        self.true_damage = 0
        self.damage_reduction = 0
        self.control_immune = 0
        self.damage_to_warriors = 0
        self.damage_to_assassins = 0
        self.damage_to_wanderers = 0
        self.damage_to_clerics = 0
        self.damage_to_mages = 0
        self.damage_to_poisoned = 0
    
        self.own_team = None
        self.op_team = None
        self.game = None
        self.pos = None
        self.is_dead = False
        self.can_attack = True
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

        op_armor = target.armor - self.armor_break # check armor break behaviour
        damage_reduction_from_armor = (op_armor + 11) / 91 # check armor behaviour

        crit_damage = 0
        crit = self.compute_crit(target)
        if crit:
            crit_damage = self.crit_damage

        skill_damage = 0
        if skill:
            skill_damage = self.skill_damage

        poisoned_extra_damage = 0
        if target.is_poisoned():
            poisoned_extra_damage = self.damage_to_poisoned

        dmg = power * (1 - damage_reduction_from_armor) * (1 + crit_damage) \
                    * (1 + self.true_damage) * (1 - target.damage_reduction) \
                    * (1 + faction_damage) * (1 + type_damage) * (1 + skill_damage) \
                    * (1 + poisoned_extra_damage)
                    # check faction damage behaviour
                    # check type damage behaviour
                    # check skill damage behaviour
                    # check extra damage to poisoned behaviour

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

    def compute_dodge(self, target, name=''):
        dodged = False
        hit_rate = self.hit_rate
        if self.faction_bonus(target):
            hit_rate += 0.15
        if rd.random() <= target.dodge - hit_rate and not target.is_dead: # check dodge behaviour
            dodged = True

        if dodged:
            self.game.log += '\n{} dodges {} from {}' \
                        .format(target.str_id, name, self.str_id)

        return dodged

    def compute_crit(self, target):
        crit = False
        if rd.random() <= self.crit_rate and not target.is_dead:
            crit = True

        return crit

    def turn(self):
        if self.energy >= 100 and self.is_silenced():
            for e in [e for e in self.effects if isinstance(e, Effect.silence)]:
                self.game.log += '\n{} is silenced by {} ({}, {} turns left) ' \
                        'and cannot use its skill' \
                        .format(self.str_id, e.holder.str_id, e.name, e.turns)

        if self.energy >= 100 and not self.is_silenced():
            self.skill()
        else:
            self.attack()
        self.can_attack = False

    def attack(self, target=None, power=None):
        if target is None:
            target = self.op_team.next_target()
        if power is None:
            power = self.atk

        dodged = self.compute_dodge(target, name='attack')
        if not dodged:
            self.hit_attack(target, power=power, name='attack')

    def skill(self):
        self.energy = 0

    def hit(self, target, power, skill, active, on_attack, name=''):
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
            if active and crit:
                self.on_crit(target)
            if active: # only triggered by active? dots/counters?
                target.on_hit(self)

    def hit_attack(self, target, power, name='attack'):
        self.hit(target, power, skill=False, active=True, on_attack=True, name=name)

    def hit_skill(self, target, power, name=''):
        self.hit(target, power, skill=True, active=True, on_attack=False, name=name)

    def hit_passive(self, target, power, name=''):
        self.hit(target, power, skill=False, active=False, on_attack=False, name=name)

    def dot(self, target, power, turns, skill=False, name=''):
        if not target.is_dead:
            dot = Effect.dot(self, target, power, turns, skill=skill, name=name)
            target.effects.append(dot)
            dot.tick()

    def try_dot(self, target, power, turns, chance, skill=False, name=''):
        if rd.random() <= chance:
            self.dot(target, power, turns, skill=skill, name=name)

    def hot(self, target, power, turns, name=''):
        if not target.is_dead:
            hot = Effect.hot(self, target, power, turns, name=name)
            target.effects.append(hot)
            hot.tick()

    def try_hot(self, target, power, turns, chance, name=''):
        if rd.random() <= chance:
            self.hot(target, power, turns, name=name)

    def poison(self, target, power, turns, skill=False, name=''):
        if not target.is_dead:
            poison = Effect.poison(self, target, power, turns, skill=skill, name=name)
            target.effects.append(poison)
            poison.tick()

    def try_poison(self, target, power, turns, chance, skill=False, name=''):
        if rd.random() <= chance:
            self.poison(target, power, turns, skill=skill, name=name)

    def silence(self, target, turns, name=''):
        if not target.is_dead:
            silence = Effect.silence(self, target, turns, name=name)
            target.effects.append(silence)
            silence.tick()

    def try_silence(self, target, turns, chance, name=''):
        if rd.random() <= chance and rd.random() >= target.control_immune: # check control immune behaviour
            self.silence(target, turns, name=name)

    def attack_up(self, target, up, turns, name=''):
        if not target.is_dead:
            attack_up = Effect.attack_up(self, target, up, turns, name=name)
            target.effects.append(attack_up)
            attack_up.tick()

    def try_attack_up(self, target, up, turns, chance, name=''):
        if rd.random() <= chance:
            self.attack_up(target, up, turns, name=name)

    def attack_down(self, target, down, turns, name=''):
        if not target.is_dead:
            attack_down = Effect.attack_down(self, target, down, turns, name=name)
            target.effects.append(attack_down)
            attack_down.tick()

    def try_attack_down(self, target, down, turns, chance, name=''):
        if rd.random() <= chance:
            self.attack_down(target, down, turns, name=name)

    def crit_rate_up(self, target, up, turns, name=''):
        if not target.is_dead:
            crit_rate_up = Effect.crit_rate_up(self, target, up, turns, name=name)
            target.effects.append(crit_rate_up)
            crit_rate_up.tick()

    def try_crit_rate_up(self, target, up, turns, chance, name=''):
        if rd.random() <= chance:
            self.crit_rate_up(target, up, turns, name=name)

    def crit_rate_down(self, target, down, turns, name=''):
        if not target.is_dead:
            crit_rate_down = Effect.crit_rate_down(self, target, down, turns, name=name)
            target.effects.append(crit_rate_down)
            crit_rate_down.tick()

    def try_crit_rate_down(self, target, down, turns, chance, name=''):
        if rd.random() <= chance:
            self.crit_rate_down(target, down, turns, name=name)

    def is_poisoned(self):
        return True if any([isinstance(e, Effect.poison) for e in self.effects]) else False

    def is_silenced(self):
        return True if any([isinstance(e, Effect.silence) for e in self.effects]) else False

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
        self.energy = max(min(self.energy + 50, 100), self.energy)

    def on_crit(self, target):
        pass

    def on_hit(self, attacker):
        self.energy = max(min(self.energy + 10, 100), self.energy)

    def on_kill(self, target):
        pass

    def on_death(self, attacker):
        for h in self.own_team.heroes:
            if isinstance(h, Reaper) and not h.is_dead:
                if h.star < 7:
                    h.armor_break += 6
                    h.atk *= 1.15
                else:
                    h.armor_break += 8.4
                    h.atk *= 1.2

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


class EmptyHero(BaseHero):
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


class Centaur(BaseHero):
    name = HeroName.CENTAUR
    faction = Faction.ELF
    type = HeroType.WANDERER

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.queens_crown.O6, 
                    guild_tech=guild_tech_maxed):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 250108.46 # should depend on the level
        self.atk = 15053.54 # should depend on the level
        self.armor = 10 # should depend on the level
        self.speed = 983 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech)

        if self.star < 7:
            self.crit_rate += 0.3
            self.atk *= 1.25
        else:
            self.crit_rate += 0.4
            self.atk *= 1.3

        if self.star < 9:
            self.damage_to_poisoned += 0.5
        else:
            self.damage_to_poisoned += 0.6

    def on_crit(self, target):
        name = 'Toxic Blade'
        power = self.atk * 0.66
        if self.star >= 8:
            power = self.atk * 0.78
        self.poison(target, power=power, turns=2, name=name)

    def skill(self):
        name = 'Dual Throwing Axe'
        targets = targets_at_random(self.op_team, 4)
        for target in targets:
            dodged = self.compute_dodge(target, name=name)
            if not dodged:
                hit_power = self.atk * 0.8
                dot_power = self.atk * 0.3

                self.hit_skill(target, power=hit_power, name=name)
                self.dot(target, power=dot_power, turns=2, skill=True, name=name)

        super().skill()


class Reaper(BaseHero):
    name = HeroName.REAPER
    faction = Faction.UNDEAD
    type = HeroType.MAGE

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.soul_torrent.O6, 
                    guild_tech=guild_tech_maxed):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 201719.98 # should depend on the level
        self.atk = 16276.31 # should depend on the level
        self.armor = 8 # should depend on the level
        self.speed = 984 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech)

        if self.star < 8:
            self.armor_break += 9.6
            self.hp *= 1.25
            self.atk *= 1.25
        else:
            self.armor_break += 9.6
            self.hp *= 1.3
            self.atk *= 1.3

    def skill(self):
        name = 'Fatal Wave'
        for target in self.op_team.heroes:
            dodged = self.compute_dodge(target, name=name)
            if not dodged:
                power = self.atk * 0.84

                self.hit_skill(target, power=power, name=name)

                if target.type == HeroType.WARRIOR:
                    self.try_silence(target, turns=2, chance=0.75, name=name)
        super().skill()

    def on_death(self, attacker):
        name = 'Pit Of Malice'
        power = self.atk * 0.6
        if self.star >= 9:
            power = self.atk * 1.05
        for h in self.op_team.heroes:
            self.hit_passive(h, power=power, name=name)
        super().on_death(attacker)


class Rlyeh(BaseHero):
    name = HeroName.RLYEH
    faction = Faction.HORDE
    type = HeroType.CLERIC

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.primeval_soul.O6, 
                    guild_tech=guild_tech_maxed):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 179242.021 # should depend on the level
        self.atk = 15288.8 # should depend on the level
        self.armor = 10 # should depend on the level
        self.speed = 951 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech)

        if self.star < 9:
            self.atk *= 1.2
            self.hp *= 1.15
        else:
            self.atk *= 1.25
            self.hp *= 1.2

    def skill(self):
        name = 'Nightmare'
        min_enemy_hp = min([h.hp for h in self.op_team.heroes if not h.is_dead])
        enemy_candidates = [h for h in self.op_team.heroes if h.hp == min_enemy_hp]
        min_ally_hp = min([h.hp for h in self.own_team.heroes if not h.is_dead])
        ally_candidates = [h for h in self.own_team.heroes if h.hp == min_ally_hp]
        rd.shuffle(enemy_candidates)
        rd.shuffle(ally_candidates)
        enemy_target = enemy_candidates[0]
        ally_target = ally_candidates[0]
        dodged = self.compute_dodge(enemy_target, name=name)
        if not dodged:
            dmg_power = self.atk * 1.71
            heal_power = self.atk * 4

            self.hit_skill(enemy_target, power=dmg_power, name=name)
            self.hot(ally_target, power=heal_power, turns=1, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Blood Ceremony'
        power = self.atk * 1.1
        if self.star >= 7:
            power = self.atk * 1.5
        min_hp = min([h.hp for h in self.own_team.heroes if not h.is_dead])
        candidates = [h for h in self.own_team.heroes if h.hp == min_hp]
        rd.shuffle(candidates)
        target = candidates[0]
        self.try_hot(target, power=power, turns=1, chance=0.5, name=name)
        super().on_attack(target)

    def on_hit(self, attacker):
        name = 'Deep Sea Sacrifice'
        power = self.atk * 0.5
        if self.star >= 8:
            power = self.atk * 0.65
        self.hot(self, power=power, turns=1, name=name)
        super().on_hit(attacker)


class SawMachine(BaseHero):
    name = HeroName.SAW_MACHINE
    faction = Faction.ALLIANCE
    type = HeroType.MAGE

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.knights_vow.O6, 
                    guild_tech=guild_tech_maxed):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 233932.307 # should depend on the level
        self.atk = 13313.962 # should depend on the level
        self.armor = 13 # should depend on the level
        self.speed = 984 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech)

        if self.star < 8:
            self.hp *= 1.2
            self.skill_damage += 0.75
        else:
            self.hp *= 1.3
            self.skill_damage += 0.95

    def skill(self):
        name = 'Whirlwind Of Death'
        for target in self.op_team.heroes:
            dodged = self.compute_dodge(target, name=name)
            if not dodged:
                power = self.atk * 1.15

                self.hit_skill(target, power=power, name=name)

                if target.type == HeroType.CLERIC:
                    self.try_silence(target, turns=3, chance=0.75, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Interference Mode'
        down = 0.12
        if self.star >= 7:
            down = 0.16
        self.attack_down(target, down=down, turns=3, name=name)

        name = 'Rampage'
        down = 0.1
        up = 0.2
        if self.star >= 9:
            down = 0.15
            up = 0.3
        self.try_crit_rate_down(target, down=down, turns=3, chance=0.8, name=name)
        self.try_attack_up(self, up=up, turns=3, chance=0.8, name=name)
        super().on_attack(target)


class Scarlet(BaseHero):
    name = HeroName.SCARLET
    faction = Faction.HORDE
    type = HeroType.MAGE

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.primeval_soul.O6, 
                    guild_tech=guild_tech_maxed):
        if level < 200 or tier < 6:
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
            dodged = self.compute_dodge(target, name=name)
            if not dodged:
                hit_power = self.atk * 0.42
                poison_power = self.atk * 0.6

                self.hit_skill(target, power=hit_power, name=name) # sequence order? same for all aoe damage
                self.poison(target, power=poison_power, turns=3, skill=True, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Poison Touch'
        power = self.atk * 0.7
        if self.star >= 7:
            power = self.atk * 0.8
        self.try_poison(target, power=power, turns=2, chance=0.8, name=name)
        super().on_attack(target)

    def on_hit(self, attacker):
        name = 'Corrosive Skin'
        power = self.atk * 0.54
        if self.star >= 9:
            power = self.atk * 0.62
        self.try_poison(attacker, power=power, turns=3, chance=0.6, name=name)
        super().on_hit(attacker)

    def on_death(self, attacker):
        name = 'Malefic'
        power = self.atk * 0.63
        if self.star >= 8:
            power = self.atk * 0.85
        for h in self.op_team.heroes:
            self.poison(h, power=power, turns=3, name=name)
        super().on_death(attacker)


@dataclass
class Hero:
    empty = EmptyHero()
    centaur = Centaur
    reaper = Reaper
    rlyeh = Rlyeh
    saw_machine = SawMachine
    scarlet = Scarlet
