import random as rd
from dataclasses import dataclass

from models import Faction, HeroType, HeroName, Equipment, Armor, Helmet, Weapon, Pendant, Rune, Artifact, Aura, Effect
from settings import guild_tech_maxed, guild_tech_empty, default_familiar_stats, default_familiar
from utils import targets_at_random


## Team
class Team:
    def __init__(self, heroes, pet=default_familiar):
        if len(heroes) != 6:
            raise Warning('Teams must contain 6 heroes')

        self.heroes = heroes
        self.pet = pet
        for i, h in enumerate(self.heroes):
            h.pos = i

        aura = Aura(heroes) # aura
        self.compute_aura(aura)

        self.compute_pet(pet) # familiar

        for h in self.heroes:
            if isinstance(h, Vegvisir):
                hp_up = 0.4
                crit_damage_up = 0.2
                crit_rate_up = 0.2
                if h.star >= 8: ### add value
                    hp_up = 0.6
                    crit_damage_up = 0.3
                    crit_rate_up = 0.3
                if h.pos <= 2:
                    h.hp *= 1 + hp_up
                else:
                    h.crit_damage += crit_damage_up
                    h.crit_rate += crit_rate_up # check crit rate up behavious (frontline)

        for h in self.heroes:
            h.hp_max = h.hp
            h.own_team = self
        self.pet.own_team = self

    def compute_aura(self, aura):
        for h in self.heroes:
            h.atk *= (1 + aura.atk_bonus)
            h.hp *= (1 + aura.hp_bonus)
            h.dodge += aura.dodge
            h.crit_rate += aura.crit_rate
            h.control_immune += aura.control_immune
            h.armor_break *= (1 + aura.armor_break_bonus)

    def compute_pet(self, pet):
        for h in self.heroes:
            h.crit_rate += pet.crit_rate
            h.crit_damage += pet.crit_damage
            h.skill_damage += pet.skill_damage
            h.hit_rate += pet.hit_rate
            h.true_damage += pet.true_damage
            h.dodge += pet.dodge
            h.speed += pet.speed

    def next_target(self):
        alive = [h for h in self.heroes if not h.is_dead]

        return alive[0]

    def get_backline(self):
        if all([h.is_dead for h in self.heroes[3:]]):
            return self.heroes[:3]
        return self.heroes[3:]

    def get_frontline(self):
        if all([h.is_dead for h in self.heroes[:3]]):
            return self.heroes[3:]
        return self.heroes[:3]

    def is_dead(self):
        return True if all([h.is_dead for h in self.heroes]) else False


## Heroes
class BaseHero:
    def __init__(self, armor, helmet, weapon, pendant, rune, artifact, guild_tech, familiar_stats):
        self.energy = 50
        self.armor_break = 0
        self.skill_damage = 0
        self.hit_rate = 0
        self.dodge = 0
        self.crit_rate = 0
        self.crit_damage = 0
        self.true_damage = 0
        self.damage_reduction = 0
        self.control_immune = 0
        self.damage_to_warriors_base = 0
        self.damage_to_assassins_base = 0
        self.damage_to_wanderers_base = 0
        self.damage_to_clerics_base = 0
        self.damage_to_mages_base = 0
        self.damage_to_warriors = 0
        self.damage_to_assassins = 0
        self.damage_to_wanderers = 0
        self.damage_to_clerics = 0
        self.damage_to_mages = 0
        self.damage_to_poisoned = 0
        self.damage_to_bleeding = 0
        self.damage_to_stunned = 0

        self.own_team = None
        self.op_team = None
        self.game = None
        self.pos = None
        self.is_dead = False
        self.can_attack = True
        self.effects = []

        self.has_dropped_below_60 = False
        self.has_dropped_below_30 = False

        self.compute_familiar_stats(familiar_stats)
        self.compute_items(armor, helmet, weapon, pendant, rune, artifact)
        self.compute_guild_tech(guild_tech)

    def compute_familiar_stats(self, familiar_stats):
        self.hp += familiar_stats[0]
        self.atk += familiar_stats[1]

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
        self.damage_to_warriors_base += artifact.damage_to_warriors
        self.damage_to_assassins_base += artifact.damage_to_assassins
        self.damage_to_wanderers_base += artifact.damage_to_wanderers
        self.damage_to_clerics_base += artifact.damage_to_clerics
        self.damage_to_mages_base += artifact.damage_to_mages
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
            return self.damage_to_warriors_base, self.damage_to_warriors
        elif target.type == HeroType.ASSASSIN:
            return self.damage_to_assassins_base, self.damage_to_assassins
        elif target.type == HeroType.WANDERER:
            return self.damage_to_wanderers_base, self.damage_to_wanderers
        elif target.type == HeroType.CLERIC:
            return self.damage_to_clerics_base, self.damage_to_clerics
        elif target.type == HeroType.MAGE:
            return self.damage_to_mages_base, self.damage_to_mages

    def compute_damage(self, target, power, skill=False):
        faction_damage = 0
        if self.faction_bonus(target):
            faction_damage = 0.3

        type_damage_base, type_damage = self.type_damage(target)

        op_armor = target.armor - self.armor_break
        damage_reduction_from_armor = op_armor * 0.00992543 + 0.20597124 # check armor behaviour

        crit_damage = 0
        crit = self.compute_crit(target)
        if crit:
            crit_damage = self.crit_damage + 0.5

        if skill:
            power += self.skill_damage * self.atk

        poisoned_extra_damage = 0
        if target.is_poisoned():
            poisoned_extra_damage = self.damage_to_poisoned
        bleeding_extra_damage = 0
        if target.is_bleeding():
            bleeding_extra_damage = self.damage_to_bleeding
        stunned_extra_damage = 0
        if target.is_stunned():
            stunned_extra_damage = self.damage_to_stunned

        dmg = power * (1 - damage_reduction_from_armor) * (1 + crit_damage) \
                    * (1 + self.true_damage) * (1 - target.damage_reduction) \
                    * (1 + faction_damage) * (1 + type_damage_base) \
                    * (1 + poisoned_extra_damage) * (1 + bleeding_extra_damage) \
                    * (1 + stunned_extra_damage) * (1 + type_damage)
                    # check faction damage behaviour
                    # check type damage behaviour
                    # check skill damage behaviour
                    # check extra damage to poisoned/bleeding/stunned behaviour

        damage_components = {'Power': power, 
                            'Damage reduction from armor': damage_reduction_from_armor, 
                            'Crit damage': crit_damage, 
                            'True damage': self.true_damage, 
                            'Damage reduction': target.damage_reduction, 
                            'Faction damage': faction_damage, 
                            'Type damage': type_damage, 
                            'Skill damage': self.skill_damage, 
                            'Poisoned extra damage': poisoned_extra_damage, 
                            'Bleeding extra damage': bleeding_extra_damage, 
                            'Stunned extra damage': stunned_extra_damage, 
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

    def targets_hit(self, targets, name=''):
        targets_hit = []
        for target in targets:
            if not target.is_dead:
                dodged = self.compute_dodge(target, name=name)
                if not dodged:
                    targets_hit.append(target)

        return targets_hit

    def compute_crit(self, target):
        crit = False
        if rd.random() <= self.crit_rate and not target.is_dead:
            crit = True

        return crit

    def turn(self):
        if self.is_stunned() or self.is_petrified() or self.is_frozen():
            for e in [e for e in self.effects if isinstance(e, Effect.stun)]:
                self.game.log += '\n{} is stunned by {} ({}, {} turns left) ' \
                        'and cannot play' \
                        .format(self.str_id, e.source.str_id, e.name, e.turns)
            for e in [e for e in self.effects if isinstance(e, Effect.petrify)]:
                self.game.log += '\n{} is petrified by {} ({}, {} turns left) ' \
                        'and cannot play' \
                        .format(self.str_id, e.source.str_id, e.name, e.turns)
            for e in [e for e in self.effects if isinstance(e, Effect.freeze)]:
                self.game.log += '\n{} is frozen by {} ({}, {} turns left) ' \
                        'and cannot play' \
                        .format(self.str_id, e.source.str_id, e.name, e.turns)
        else:
            if self.energy >= 100 and self.is_silenced():
                for e in [e for e in self.effects if isinstance(e, Effect.silence)]:
                    self.game.log += '\n{} is silenced by {} ({}, {} turns left) ' \
                            'and cannot use its skill' \
                            .format(self.str_id, e.source.str_id, e.name, e.turns)
    
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
        self.own_team.pet.energy = max(min(self.own_team.pet.energy + 12.5, 100), self.energy)

    def update_state(self, target, on_attack, active, crit):
        target.has_taken_damage(self)
        if on_attack:
            self.on_attack(target)
        if active and crit:
            self.on_crit(target)
        if active: # only triggered by active? dots/counters?
            target.on_hit(self)

    def hit(self, target, power, skill, active, on_attack, multi, update=True, name=''):
        if not multi:
            if not target.is_dead:
                damage_components = self.compute_damage(target, power, skill=skill)
                dmg = damage_components['Total damage']
                crit = True if damage_components['Crit damage'] > 0 else False
                crit_str = ', crit' if crit else ''
    
                target.hp -= dmg
                log_text = '\n{} takes {} damage from {} ({}{})' \
                            .format(target.str_id, round(dmg), self.str_id, name, crit_str)
                self.game.log += log_text
    
                if update:
                    self.update_state(target, on_attack, active, crit)

                return [crit]

        else:
            crits = []
            for i, t in enumerate(target):
                p = power[i]
                crit = self.hit(t, p, skill, active, on_attack, 
                        multi=False, update=False, name=name)[0]
                crits.append(crit)
            for i, t in enumerate(target):
                if not t.is_dead:
                    crit = crits[i]
                    self.update_state(t, on_attack, active, crit)

            return crits


    def hit_attack(self, target, power, multi=False, name='attack'):
        crits = self.hit(target, power, skill=False, active=True, 
                        on_attack=True, multi=multi, name=name)

        return crits

    def hit_skill(self, target, power, multi=False, name=''):
        crits = self.hit(target, power, skill=True, active=True, 
                        on_attack=False, multi=multi, name=name)

        return crits

    def hit_passive(self, target, power, multi=False, name=''):
        crits = self.hit(target, power, skill=False, active=False, 
                        on_attack=False, multi=multi, name=name)

        return crits

    def try_hit_passive(self, target, power, chance, multi=False, name=''):
        if rd.random() <= chance:
            self.hit_passive(target, power, multi=multi, name=name)
            return True

    def dot(self, target, power, turns, skill=False, name=''):
        if not target.is_dead:
            dot = Effect.dot(self, target, power, turns, skill=skill, name=name)
            target.effects.append(dot)
            dot.tick()

    def try_dot(self, target, power, turns, chance, skill=False, name=''):
        if rd.random() <= chance:
            self.dot(target, power, turns, skill=skill, name=name)
            return True

    def heal(self, target, power, turns, name=''):
        if not target.is_dead:
            heal = Effect.heal(self, target, power, turns, name=name)
            target.effects.append(heal)
            heal.tick()

    def try_heal(self, target, power, turns, chance, name=''):
        if rd.random() <= chance:
            self.heal(target, power, turns, name=name)
            return True

    def poison(self, target, power, turns, skill=False, name=''):
        if not target.is_dead:
            poison = Effect.poison(self, target, power, turns, skill=skill, name=name)
            target.effects.append(poison)
            poison.tick()

    def try_poison(self, target, power, turns, chance, skill=False, name=''):
        if rd.random() <= chance:
            self.poison(target, power, turns, skill=skill, name=name)
            return True

    def bleed(self, target, power, turns, skill=False, name=''):
        if not target.is_dead:
            bleed = Effect.bleed(self, target, power, turns, skill=skill, name=name)
            target.effects.append(bleed)
            bleed.tick()

    def try_bleed(self, target, power, turns, chance, skill=False, name=''):
        if rd.random() <= chance:
            self.bleed(target, power, turns, skill=skill, name=name)
            return True

    def timed_mark(self, target, power, turns, skill=False, name=''):
        if not target.is_dead:
            timed_mark = Effect.timed_mark(self, target, power, turns, skill=skill, name=name)
            target.effects.append(timed_mark)
            timed_mark.tick()

    def silence(self, target, turns, name=''):
        if not target.is_dead:
            silence = Effect.silence(self, target, turns, name=name)
            target.effects.append(silence)
            silence.tick()

    def try_silence(self, target, turns, chance, name=''):
        if rd.random() <= chance and rd.random() >= target.control_immune: # check control immune behaviour
            self.silence(target, turns, name=name)
            return True

    def stun(self, target, turns, name=''):
        if not target.is_dead:
            stun = Effect.stun(self, target, turns, name=name)
            target.effects.append(stun)
            stun.tick()

    def try_stun(self, target, turns, chance, name=''):
        if rd.random() <= chance and rd.random() >= target.control_immune: # check control immune behaviour
            self.stun(target, turns, name=name)
            return True

    def petrify(self, target, turns, name=''):
        if not target.is_dead:
            petrify = Effect.petrify(self, target, turns, name=name)
            target.effects.append(petrify)
            petrify.tick()

    def try_petrify(self, target, turns, chance, name=''):
        if rd.random() <= chance and rd.random() >= target.control_immune: # check control immune behaviour
            self.petrify(target, turns, name=name)
            return True

    def freeze(self, target, turns, name=''):
        if not target.is_dead:
            freeze = Effect.freeze(self, target, turns, name=name)
            target.effects.append(freeze)
            freeze.tick()

    def try_freeze(self, target, turns, chance, name=''):
        if rd.random() <= chance and rd.random() >= target.control_immune: # check control immune behaviour
            self.freeze(target, turns, name=name)
            return True

    def attack_up(self, target, up, turns, name=''):
        if not target.is_dead:
            attack_up = Effect.attack_up(self, target, up, turns, name=name)
            target.effects.append(attack_up)
            attack_up.tick()

    def try_attack_up(self, target, up, turns, chance, name=''):
        if rd.random() <= chance:
            self.attack_up(target, up, turns, name=name)
            return True

    def attack_down(self, target, down, turns, name=''):
        if not target.is_dead:
            attack_down = Effect.attack_down(self, target, down, turns, name=name)
            target.effects.append(attack_down)
            attack_down.tick()

    def try_attack_down(self, target, down, turns, chance, name=''):
        if rd.random() <= chance:
            self.attack_down(target, down, turns, name=name)
            return True

    def crit_rate_up(self, target, up, turns, name=''):
        if not target.is_dead:
            crit_rate_up = Effect.crit_rate_up(self, target, up, turns, name=name)
            target.effects.append(crit_rate_up)
            crit_rate_up.tick()

    def try_crit_rate_up(self, target, up, turns, chance, name=''):
        if rd.random() <= chance:
            self.crit_rate_up(target, up, turns, name=name)
            return True

    def crit_rate_down(self, target, down, turns, name=''):
        if not target.is_dead:
            crit_rate_down = Effect.crit_rate_down(self, target, down, turns, name=name)
            target.effects.append(crit_rate_down)
            crit_rate_down.tick()

    def try_crit_rate_down(self, target, down, turns, chance, name=''):
        if rd.random() <= chance:
            self.crit_rate_down(target, down, turns, name=name)
            return True

    def crit_damage_up(self, target, up, turns, name=''):
        if not target.is_dead:
            crit_damage_up = Effect.crit_damage_up(self, target, up, turns, name=name)
            target.effects.append(crit_damage_up)
            crit_damage_up.tick()

    def try_crit_damage_up(self, target, up, turns, chance, name=''):
        if rd.random() <= chance:
            self.crit_damage_up(target, up, turns, name=name)
            return True

    def crit_damage_down(self, target, down, turns, name=''):
        if not target.is_dead:
            crit_damage_down = Effect.crit_damage_down(self, target, down, turns, name=name)
            target.effects.append(crit_damage_down)
            crit_damage_down.tick()

    def try_crit_damage_down(self, target, down, turns, chance, name=''):
        if rd.random() <= chance:
            self.crit_damage_down(target, down, turns, name=name)
            return True

    def armor_break_up(self, target, up, turns, name=''):
        if not target.is_dead:
            armor_break_up = Effect.armor_break_up(self, target, up, turns, name=name)
            target.effects.append(armor_break_up)
            armor_break_up.tick()

    def try_armor_break_up(self, target, up, turns, chance, name=''):
        if rd.random() <= chance:
            self.armor_break_up(target, up, turns, name=name)
            return True

    def armor_break_down(self, target, down, turns, name=''):
        if not target.is_dead:
            armor_break_down = Effect.armor_break_down(self, target, down, turns, name=name)
            target.effects.append(armor_break_down)
            armor_break_down.tick()

    def try_armor_break_down(self, target, down, turns, chance, name=''):
        if rd.random() <= chance:
            self.armor_break_down(target, down, turns, name=name)
            return True

    def armor_up(self, target, up, turns, name=''):
        if not target.is_dead:
            armor_up = Effect.armor_up(self, target, up, turns, name=name)
            target.effects.append(armor_up)
            armor_up.tick()

    def armor_down(self, target, down, turns, name=''):
        if not target.is_dead:
            armor_down = Effect.armor_down(self, target, down, turns, name=name)
            target.effects.append(armor_down)
            armor_down.tick()

    def speed_up(self, target, up, turns, name=''):
        if not target.is_dead:
            speed_up = Effect.speed_up(self, target, up, turns, name=name)
            target.effects.append(speed_up)
            speed_up.tick()

    def speed_down(self, target, down, turns, name=''):
        if not target.is_dead:
            speed_down = Effect.speed_down(self, target, down, turns, name=name)
            target.effects.append(speed_down)
            speed_down.tick()

    def energy_up(self, target, up, name=''):
        target.energy = max(min(target.energy + up, 100), self.energy)
        self.game.log += "\n{}'s energy is increased by {} by {} ({})" \
                            .format(target.str_id, up, self.str_id, name)

    def energy_down(self, target, down, name=''):
        target.energy = max(target.energy - down, 0)
        self.game.log += "\n{}'s energy is reduced by {} by {} ({})" \
                            .format(target.str_id, down, self.str_id, name)

    def is_poisoned(self):
        return True if any([isinstance(e, Effect.poison) for e in self.effects]) else False

    def is_bleeding(self):
        return True if any([isinstance(e, Effect.bleed) for e in self.effects]) else False

    def is_silenced(self):
        return True if any([isinstance(e, Effect.silence) for e in self.effects]) else False

    def is_stunned(self):
        return True if any([isinstance(e, Effect.stun) for e in self.effects]) else False

    def is_petrified(self):
        return True if any([isinstance(e, Effect.petrify) for e in self.effects]) else False

    def is_frozen(self):
        return True if any([isinstance(e, Effect.freeze) for e in self.effects]) else False

    def has_taken_damage(self, attacker):
        for h in self.op_team.heroes:
            if isinstance(h, Aden) and not h.is_dead:
                name = 'Bloodstain'
                up = 0.08
                if h.star >= 7:
                    up = 0.1
                if self.hp <= 0.6 * self.hp_max and not self.has_dropped_below_60:
                    h.attack_up(h, up=up, turns=None, name=name)
                if self.hp <= 0.3 * self.hp_max and not self.has_dropped_below_30:
                    h.attack_up(h, up=up, turns=None, name=name)

        if self.hp <= 0.6 * self.hp_max:
            self.has_dropped_below_60 = True
        if self.hp <= 0.3 * self.hp_max:
            self.has_dropped_below_30 = True

        if self.hp <= 0:
            if isinstance(self, MonkeyKing):
                if self.has_revived:
                    self.kill()
            else:
                self.kill()

            if attacker is not None:
                attacker.on_kill(self)
            self.on_death(attacker)

    def kill(self):
        self.is_dead = True
        self.can_attack = False
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
        for h in self.op_team.heroes:
            if isinstance(h, Aden) and not h.is_dead:
                name = 'Blood Temple'
                power = h.atk * 0.8
                if h.star >= 9:
                    power = h.atk
                if attacker is not None:
                    if attacker.str_id == h.str_id:
                        power *= 2
                h.heal(h, power=power, turns=1, name=name)

        for h in self.op_team.heroes:
            if isinstance(h, BloodTooth) and not h.is_dead:
                name = 'Executioner'
                up = 0.2
                if h.star >= 8: ### add value
                    up = 0.3
                h.attack_up(h, up=up, turns=None, name=name)

        for h in self.op_team.heroes:
            if isinstance(h, Luna) and not h.is_dead:
                name = 'Blood Moon Sacrifice'
                crit_damage_up = 0.15
                attack_up = 0.12
                if h.star >= 8:
                    crit_damage_up = 0.20
                    attack_up = 0.15
                h.crit_damage_up(h, up=crit_damage_up, turns=None, name=name)
                h.attack_up(h, up=attack_up, turns=None, name=name)

        for h in self.own_team.heroes:
            if isinstance(h, Reaper) and not h.is_dead:
                name = 'Sadism'
                armor_break_up = 6
                attack_up = 0.15
                if h.star >= 7:
                    armor_break_up = 8.4
                    attack_up = 0.2
                h.armor_break_up(h, up=armor_break_up, turns=None, name=name)
                h.attack_up(h, up=attack_up, turns=None, name=name)

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


class Aden(BaseHero):
    name = HeroName.ADEN
    faction = Faction.UNDEAD
    type = HeroType.ASSASSIN

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.soul_torrent.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 0.0 # should depend on the level
        self.atk = 0.0 # should depend on the level
        self.armor = 0 # should depend on the level
        self.speed = 0 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        if self.star < 8:
            self.hit_rate += 0.2
            self.armor_break += 6.4
            self.damage_to_bleeding += 0.4
        else:
            self.hit_rate += 0.25
            self.armor_break += 9.6
            self.damage_to_bleeding += 0.5

    def skill(self):
        name = 'Strangle'
        targets_hit = targets_at_random(self.op_team.heroes, 3)

        hit_power = [self.atk * 1.48] * len(targets_hit)
        bleed_power = self.atk * 0.46
        heal_power = self.atk
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in targets_hit:
            self.bleed(target, power=bleed_power, turns=3, skill=True, name=name)
        if targets_hit:
            self.heal(self, power=heal_power, turns=1, name=name)
        super().skill()


class BloodTooth(BaseHero):
    name = HeroName.BLOOD_TOOTH
    faction = Faction.HORDE
    type = HeroType.ASSASSIN

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.primeval_soul.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 0.0 # should depend on the level
        self.atk = 0.0 # should depend on the level
        self.armor = 0 # should depend on the level
        self.speed = 0 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        if self.star < 7:
            self.atk *= 1.25
            self.crit_rate += 0.3
            self.hp *= 1.15
        else:
            self.atk *= 1.35 ### add value
            self.crit_rate += 0.3
            self.hp *= 1.2

    def attack(self):
        name = 'attack'
        power = self.atk * 1.1
        if self.star >= 9: ### add value
            power = self.atk * 1.3
        min_enemy_hp = min([h.hp for h in self.op_team.heroes if not h.is_dead])
        candidates = [h for h in self.op_team.heroes if h.hp == min_enemy_hp]
        rd.shuffle(candidates)
        target = candidates[0]
        super().attack(target=target, power=power)

    def skill(self):
        name = 'Power Torture'
        targets = targets_at_random(self.op_team.get_backline(), 2)
        targets_hit = self.targets_hit(targets, name=name)

        hit_power = [self.atk * 1.76] * len(targets_hit)
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in targets_hit: # check skill drain behaviour
            self.attack_down(target, down=0.22, turns=2, name=name)
            self.attack_up(self, up=0.22, turns=2, name=name)
        super().skill()


class Centaur(BaseHero):
    name = HeroName.CENTAUR
    faction = Faction.ELF
    type = HeroType.WANDERER

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.queens_crown.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 224121.1 # should depend on the level
        self.atk = 13402.1 # should depend on the level
        self.armor = 10 # should depend on the level
        self.speed = 983 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

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
        super().on_crit(target)

    def skill(self):
        name = 'Dual Throwing Axe'
        targets = targets_at_random(self.op_team.heroes, 4)
        targets_hit = self.targets_hit(targets, name=name)

        hit_power = [self.atk * 0.8] * len(targets_hit)
        dot_power = self.atk * 0.3
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in targets_hit:
            self.dot(target, power=dot_power, turns=2, skill=True, name=name)
        super().skill()


class Dziewona(BaseHero):
    name = HeroName.DZIEWONA
    faction = Faction.UNDEAD
    type = HeroType.ASSASSIN

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.soul_torrent.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 168584.5 # should depend on the level
        self.atk = 13496.1 # should depend on the level
        self.armor = 9 # should depend on the level
        self.speed = 1008 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        self.has_triggered = False

        if self.star < 7:
            self.armor_break += 10.8
            self.atk *= 1.22
        else:
            self.armor_break += 12
            self.atk *= 1.25

    def attack(self):
        target = self.op_team.next_target()
        power = self.atk

        dodged = self.compute_dodge(target, name='attack')
        if not dodged:
            self.hit_attack(target, power=power, name='attack')
        else:
            name = 'Cobweb Trap'
            power = self.atk * 1.4
            if self.star >= 8:
                power = self.atk * 2.8
            self.hit_passive(target, power=power, name=name)

    def skill(self):
        name = 'Spider Attack'
        targets_hit = targets_at_random(self.op_team.heroes, 4)

        power = [self.atk * 1.25] * len(targets_hit)
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            if target.type == HeroType.MAGE:
                self.try_stun(target, turns=2, chance=0.8, name=name)
        super().skill()

    def has_taken_damage(self, attacker):
        if self.hp <= self.hp_max * 0.5 and not self.has_triggered:
            name = 'Crouch Ambush'
            up = 0.25
            if self.star >= 9:
                up = 0.35
            self.attack_up(self, up=up, turns=3, name=name)
            self.has_triggered = True
        super().has_taken_damage(attacker)


class ForestHealer(BaseHero):
    name = HeroName.FOREST_HEALER
    faction = Faction.ELF
    type = HeroType.CLERIC

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.queens_crown.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 191062.2 # should depend on the level
        self.atk = 11944.0 # should depend on the level
        self.armor = 10 # should depend on the level
        self.speed = 973 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        if self.star < 8:
            self.hp *= 1.3
        else:
            self.hp *= 1.4

    def skill(self):
        name = "Nature's Hymn"
        targets_hit = self.targets_hit(self.op_team.get_backline(), name=name)

        hit_power = [self.atk * 0.89] * len(targets_hit)
        heal_power = self.atk * 1.85
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        if targets_hit:
            for target in self.own_team.heroes:
                self.heal(target, power=heal_power, turns=1, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Healing Heart'
        power = self.atk * 0.64
        if self.star >= 7:
            power = self.atk * 0.81
        for target in self.own_team.get_frontline():
            self.heal(target, power=power, turns=1, name=name)
        super().on_attack(target)

    def on_death(self, attacker):
        name = 'Meaning Of Life'
        power = self.atk * 1.2
        crit_rate_up = 0.11
        if self.star >= 9:
            power = self.atk * 1.6
            crit_rate_up = 0.135
        for target in self.own_team.heroes:
            self.heal(target, power=power, turns=1, name=name)
        for target in self.own_team.heroes:
            self.crit_rate_up(target, up=crit_rate_up, turns=3, name=name)
        super().on_death(attacker)


class Freya(BaseHero):
    name = HeroName.FREYA
    faction = Faction.HELL
    type = HeroType.MAGE

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.eternal_curse.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 155323.2 # should depend on the level
        self.atk = 14530.4 # should depend on the level
        self.armor = 9 # should depend on the level
        self.speed = 971 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        if self.star < 8:
            self.skill_damage += 0.875
            self.hp *= 1.35
            self.speed += 50
        else:
            self.skill_damage += 1.0
            self.hp *= 1.4
            self.speed += 60

    def skill(self):
        name = 'Hollow Descent'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        power = [self.atk * 0.54] * len(targets_hit)
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            landed = self.try_petrify(target, turns=2, chance=0.2, name=name)
            if landed:
                name = 'Expand'
                up = 0.35
                if self.star >= 9:
                    up = 0.5
                self.attack_up(self, up=up, turns=4, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Soul Sever'
        chance = 0.45
        if self.star >= 7:
            chance = 0.55
        landed = self.try_petrify(target, turns=1, chance=chance, name=name)
        if landed:
            name = 'Expand'
            up = 0.35
            if self.star >= 9:
                up = 0.5
            self.attack_up(self, up=up, turns=4, name=name)
        super().on_attack(target)


class Gerald(BaseHero):
    name = HeroName.GERALD
    faction = Faction.UNDEAD
    type = HeroType.WANDERER

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.soul_torrent.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 238557.7 # should depend on the level
        self.atk = 12320.2 # should depend on the level
        self.armor = 13 # should depend on the level
        self.speed = 983 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        if self.star < 8:
            self.damage_to_stunned += 0.75
        else:
            self.damage_to_stunned += 0.95

        if self.star < 9:
            self.armor_break += 9.6
            self.atk *= 1.3
        else:
            self.armor_break += 12
            self.atk *= 1.35

    def skill(self):
        name = 'Wheel Of Torture'
        targets = targets_at_random(self.op_team.heroes, 4)
        targets_hit = self.targets_hit(targets, name=name)

        power = [self.atk * 0.98] * len(targets_hit)
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            if target.type == HeroType.ASSASSIN:
                self.try_stun(target, turns=2, chance=0.8, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Chain Of Fool'
        chance = 0.5
        turns = 1
        if self.star >= 7:
            chance = 0.48
            turns = 2
        self.try_stun(target, turns=turns, chance=chance, name=name)
        super().on_attack(target)


class Luna(BaseHero):
    name = HeroName.LUNA
    faction = Faction.ELF
    type = HeroType.WANDERER

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.queens_crown.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 208931.4 # should depend on the level
        self.atk = 12837.8 # should depend on the level
        self.armor = 10 # should depend on the level
        self.speed = 1017 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        if self.star < 7:
            self.crit_rate += 0.3
            self.crit_damage += 0.9
        else:
            self.crit_rate += 0.3
            self.crit_damage += 0.3
            self.atk *= 1.3

    def attack(self):
        name = 'attack'
        targets = targets_at_random(self.op_team.heroes, 3)
        targets_hit = self.targets_hit(targets, name=name)
        power = [self.atk * 0.7] * len(targets_hit)
        if self.star >= 9:
            power = [self.atk * 0.85] * len(targets_hit)

        self.hit(targets_hit, power, skill=False, active=True, 
                    on_attack=False, multi=True, name=name)
        if targets_hit:
            self.on_attack(targets_hit[0])

    def skill(self):
        name = 'Shooting Star'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        power = [self.atk * 0.85] * len(targets_hit)
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            self.try_silence(target, turns=2, chance=0.5, name=name)
        super().skill()


class Medusa(BaseHero):
    name = HeroName.MEDUSA
    faction = Faction.HORDE
    type = HeroType.WANDERER

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.primeval_soul.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 200043.7 # should depend on the level
        self.atk = 12790.5 # should depend on the level
        self.armor = 10 # should depend on the level
        self.speed = 991 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        if self.star < 8:
            self.atk *= 1.4
        else:
            self.atk *= 1.5

    def skill(self):
        name = 'Viper Arrow'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        power = [self.atk * 1.02] * len(targets_hit)
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            down = 0.24
            self.crit_rate_down(target, down=down, turns=3, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Snake Locks'
        down = 0.15
        up = 0.15
        if self.star >= 7:
            down = 0.20
            up = 0.20
        self.crit_rate_down(target, down=down, turns=4, name=name)
        self.crit_rate_up(self, up=up, turns=4, name=name)
        super().on_attack(target)

    def on_hit(self, attacker):
        name = 'Counter'
        power = self.atk * 0.48
        turns = 2
        if self.star >= 9:
            power = self.atk * 0.72
            turns = 1
        self.bleed(attacker, power=power, turns=turns, name=name)
        super().on_hit(attacker)


class Minotaur(BaseHero):
    name = HeroName.MINOTAUR
    faction = Faction.HORDE
    type = HeroType.WARRIOR

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.primeval_soul.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 0.0 # should depend on the level
        self.atk = 0.0 # should depend on the level
        self.armor = 0 # should depend on the level
        self.speed = 0 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        if self.star < 7:
            self.atk *= 1.2
            self.armor += 23
        else:
            self.atk *= 1.25
            self.armor += 25

        if self.star < 8:
            self.damage_to_warriors += 0.45
        else:
            self.damage_to_warriors += 0.6


    def skill(self):
        name = 'Fury Swipes'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        power = [self.atk * 0.9] * len(targets_hit)
        for i, h in enumerate(targets_hit):
            if h.type == HeroType.WARRIOR:
                power[i] += self.atk * 1.2
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        super().skill()

    def on_hit(self, attacker):
        name = 'Rebirth'
        power = self.atk * 0.32
        if self.star >= 9:
            power = self.atk * 0.4 ### add value
        self.heal(self, power=power, turns=1, name=name)
        super().on_hit(attacker)


class MonkeyKing(BaseHero):
    name = HeroName.MONKEY_KING
    faction = Faction.HELL
    type = HeroType.WARRIOR

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.eternal_curse.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 0.0 # should depend on the level
        self.atk = 0.0 # should depend on the level
        self.armor = 0 # should depend on the level
        self.speed = 0 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        self.has_revived = False

    def skill(self):
        name = 'Boundless Strike'
        targets_hit = self.targets_hit(self.op_team.get_backline(), name=name)

        hit_power = [self.atk * 1.08] * len(targets_hit)
        mark_power = self.atk * 2.64
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in targets_hit:
            self.timed_mark(target, power=mark_power, turns=2, skill=True, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Cudgel Mastery'
        chance = 0.3
        power = self.atk * 0.9
        if self.star >= 7:
            chance = 0.35
            power = self.atk * 1.2
        self.try_petrify(target, turns=1, chance=chance, name=name)
        self.timed_mark(target, power=power, turns=2, name=name)

    def on_hit(self, attacker):
        name = 'Fight Against Buddha'
        power = self.atk * 1.5
        if self.star >= 8:
            power = self.atk * 1.85 ### add value
        self.try_hit_passive(attacker, power=power, chance=0.7, name=name)
        super().on_hit(attacker)


    def on_death(self, attacker):
        if not self.has_revived:
            name = 'Buddha Rebirth'
            power = self.hp_max * 0.9 - self.hp
            if self.star >= 9:
                power = self.hp_max - self.hp
            self.heal(self, power=power, turns=1, name=name)
            self.has_revived = True
        super().on_death(attacker)


class Reaper(BaseHero):
    name = HeroName.REAPER
    faction = Faction.UNDEAD
    type = HeroType.MAGE

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.soul_torrent.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 175732.3 # should depend on the level
        self.atk = 14624.2 # should depend on the level
        self.armor = 8 # should depend on the level
        self.speed = 984 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

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
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        power = [self.atk * 0.84] * len(targets_hit)
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            if target.type == HeroType.WARRIOR:
                self.try_silence(target, turns=2, chance=0.75, name=name)
        super().skill()

    def on_death(self, attacker):
        name = 'Pit Of Malice'
        power = self.atk * 0.6
        if self.star >= 9:
            power = self.atk * 1.05
        power = [power] * 6
        self.hit_passive(self.op_team.heroes, power=power, multi=True, name=name)
        super().on_death(attacker)


class Ripper(BaseHero):
    name = HeroName.RIPPER
    faction = Faction.UNDEAD
    type = HeroType.ASSASSIN

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.soul_torrent.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 0.0 # should depend on the level
        self.atk = 0.0 # should depend on the level
        self.armor = 0 # should depend on the level
        self.speed = 0 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        self.has_triggered = False

        if self.star < 7:
            self.armor_break += 9.6
            self.atk *= 1.3
        else: ### add value
            self.armor_break += 12
            self.atk *= 1.4

    def skill(self):
        name = 'Venom Wind'
        targets = targets_at_random(self.op_team.get_backline(), 2)
        targets_hit = self.targets_hit(targets, name=name)

        hit_power = [self.atk * 1.1] * len(targets_hit)
        dot_power = self.atk * 0.45
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in targets_hit:
            self.dot(target, power=dot_power, turns=5, name=name)
        for target in targets_hit:
            self.try_stun(target, turns=2, chance=0.45, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Poison Dagger'
        power = self.atk * 0.38
        if self.star >= 8: ### add value
            power = self.atk * 0.5
        self.poison(target, power=power, turns=6, name=name)
        super().on_attack(target)

    def has_taken_damage(self, attacker):
        if self.hp <= self.hp_max * 0.5 and not self.has_triggered:
            name = 'Poison Nova'
            power = self.atk * 0.4
            if self.star >= 9:
                power = self.atk * 0.6 ### add value
            targets = targets_at_random(self.op_team.get_backline(), 2)
            for target in targets:
                self.poison(target, power=power, turns=5, name=name)
            self.has_triggered = True
        super().has_taken_damage(attacker)


class Rlyeh(BaseHero):
    name = HeroName.RLYEH
    faction = Faction.HORDE
    type = HeroType.CLERIC

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.primeval_soul.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 153254.1 # should depend on the level
        self.atk = 13636.6 # should depend on the level
        self.armor = 10 # should depend on the level
        self.speed = 951 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

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
            self.heal(ally_target, power=heal_power, turns=1, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Blood Ceremony'
        power = self.atk * 1.1
        if self.star >= 7:
            power = self.atk * 1.5
        if any([not h.is_dead for h in self.own_team.heroes]):
            min_hp = min([h.hp for h in self.own_team.heroes if not h.is_dead])
            candidates = [h for h in self.own_team.heroes if h.hp == min_hp]
            rd.shuffle(candidates)
            target = candidates[0]
            self.try_heal(target, power=power, turns=1, chance=0.5, name=name)
            super().on_attack(target)

    def on_hit(self, attacker):
        name = 'Deep Sea Sacrifice'
        power = self.atk * 0.5
        if self.star >= 8:
            power = self.atk * 0.65
        self.heal(self, power=power, turns=1, name=name)
        super().on_hit(attacker)


class SawMachine(BaseHero):
    name = HeroName.SAW_MACHINE
    faction = Faction.ALLIANCE
    type = HeroType.MAGE

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.knights_vow.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 207944.3 # should depend on the level
        self.atk = 11661.9 # should depend on the level
        self.armor = 13 # should depend on the level
        self.speed = 984 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        if self.star < 8:
            self.hp *= 1.2
            self.skill_damage += 0.75
        else:
            self.hp *= 1.3
            self.skill_damage += 0.95

    def skill(self):
        name = 'Whirlwind Of Death'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        power = [self.atk * 1.15] * len(targets_hit)
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
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
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 151937.2 # should depend on the level
        self.atk = 16505.5 # should depend on the level
        self.armor = 9 # should depend on the level
        self.speed = 984 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

    def skill(self):
        name = 'Poison Nova'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)
        hit_power = [self.atk * 0.42] * len(targets_hit)
        poison_power = self.atk * 0.6
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name) # sequence order? same for all aoe damage
        for target in targets_hit:
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


class ShuddeMell(BaseHero):
    name = HeroName.SHUDDE_M_ELL
    faction = Faction.UNDEAD
    type = HeroType.CLERIC

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.soul_torrent.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 0.0 # should depend on the level
        self.atk = 0.0 # should depend on the level
        self.armor = 0 # should depend on the level
        self.speed = 0 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        if self.star < 7:
            self.hp *= 1.22
            self.atk *= 1.15
        else:
            self.hp *= 1.3 ### add value
            self.atk *= 1.2

    def attack(self):
        name = 'attack'
        targets = targets_at_random(self.op_team.heroes, 3)
        targets_hit = self.targets_hit(targets, name=name)
        power = [self.atk * 0.7] * len(targets_hit)
        if self.star >= 8:
            power = [self.atk * 0.85] * len(targets_hit) ### add value

        self.hit(targets_hit, power, skill=False, active=True, 
                    on_attack=False, multi=True, name=name)
        for target in targets_hit: # check skill behaviour (multi silence?)
            name = 'Dominoll'
            self.try_silence(target, turns=2, chance=0.4, name=name)
        if targets_hit:
            self.on_attack(targets_hit[0])

    def skill(self):
        name = 'Tentacle Attack'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)
        hit_power = [self.atk * 0.8] * len(targets_hit)
        heal_power = self.atk * 1.2
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        if targets_hit:
            heal_targets = targets_at_random(self.own_team.heroes, 4)
            for target in heal_targets:
                self.heal(target, power=heal_power, turns=4, name=name)
        super().skill()

    def on_hit(self, attacker):
        name = 'Creation'
        chance = 0.4
        if self.star >= 9: ### add value
            chance = 0.5
        if rd.random() <= chance:
            self.energy_up(self, up=30, name=name)
        super().on_hit(attacker)


class Ultima(BaseHero):
    name = HeroName.ULTIMA
    faction = Faction.ALLIANCE
    type = HeroType.CLERIC

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.knights_vow.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 0.0 # should depend on the level
        self.atk = 0.0 # should depend on the level
        self.armor = 0 # should depend on the level
        self.speed = 0 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        self.has_triggered = False

        if self.star < 7:
            self.hp *= 1.3
            self.speed += 30
        else:
            self.hp *= 1.4 ### add value
            self.speed += 40

    def attack(self):
        name = 'attack'
        targets = targets_at_random(self.op_team.heroes, 3)
        targets_hit = self.targets_hit(targets, name=name)
        power = [self.atk * 0.7] * len(targets_hit)
        if self.star >= 8:
            power = [self.atk * 0.85] * len(targets_hit) ### add value

        self.hit(targets_hit, power, skill=False, active=True, 
                    on_attack=False, multi=True, name=name)
        if targets_hit:
            self.on_attack(targets_hit[0])

    def skill(self):
        name = 'Stellar Detonation'
        targets_hit = self.targets_hit(self.op_team.get_backline(), name=name)

        hit_power = [self.atk * 1.08] * len(targets_hit)
        speed_up = 30
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        if targets_hit:
            for target in self.own_team.get_backline():
                self.speed_up(target, up=speed_up, turns=2, name=name)
        super().skill()

    def has_taken_damage(self, attacker):
        if self.hp <= self.hp_max * 0.5 and not self.has_triggered:
            name = 'Celestial Opposition'
            atk_up = 0.22
            armor_down = 7
            if self.star >= 9:
                atk_up = 0.25 ### add value
                armor_down = 9
            for target in self.own_team.heroes:
                self.attack_up(target, up=atk_up, turns=3, name=name)
            for target in self.op_team.heroes:
                self.armor_down(target, down=armor_down, turns=3, name=name)
            self.has_triggered = True
        super().has_taken_damage(attacker)


class Vegvisir(BaseHero):
    name = HeroName.VEGVISIR
    faction = Faction.ELF
    type = HeroType.WARRIOR

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.queens_crown.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 0.0 # should depend on the level
        self.atk = 0.0 # should depend on the level
        self.armor = 0 # should depend on the level
        self.speed = 0 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        self.has_triggered = False

    def skill(self):
        name = 'Bipolar Reversal'
        targets_hit = targets_at_random(self.op_team.heroes, 3)
        hit_power = [self.atk * 1.58] * len(targets_hit)
        crits = self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for i, target in enumerate(targets_hit):
            if crits[i]:
                self.try_freeze(target, turns=2, chance=0.36, name=name)
        super().skill()

    def on_hit(self, attacker):
        name = 'Glacier Echo'
        crit_rate_up = 0.07
        heal_power = self.atk * 0.3
        if self.star >= 7: ### add value
            crit_rate_up = 0.1
            heal_power = self.atk * 0.4
        self.crit_rate_up(self, up=crit_rate_up, turns=3, name=name)
        self.heal(self, power=heal_power, turns=1, name=name)
        super().on_hit(attacker)

    def has_taken_damage(self, attacker):
        if self.hp <= self.hp_max * 0.5 and not self.has_triggered:
            name = 'Willpower Awakening'
            atk_up = 0.6
            crit_rate_up = 0.3
            heal_power = self.atk * 2.4
            if self.star >= 9: ### add value
                atk_up = 0.6
                crit_rate_up = 0.3
                heal_power = self.atk * 2.4
            self.attack_up(self, up=atk_up, turns=3, name=name)
            self.crit_rate_up(self, up=crit_rate_up, turns=3, name=name)
            self.heal(self, power=heal_power, turns=3, name=name)
            self.has_triggered = True
        super().has_taken_damage(attacker)


class Verthandi(BaseHero):
    name = HeroName.VERTHANDI
    faction = Faction.HEAVEN
    type = HeroType.CLERIC

    def __init__(self, star=9, tier=6, level=200, 
                    armor=Armor.O2, helmet=Helmet.O2, weapon=Weapon.O2, pendant=Pendant.O2, 
                    rune=Rune.attack.R2, artifact=Artifact.gift_of_creation.O6, 
                    guild_tech=guild_tech_maxed, 
                    familiar_stats=default_familiar_stats):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 0.0 # should depend on the level
        self.atk = 0.0 # should depend on the level
        self.armor = 0 # should depend on the level
        self.speed = 0 # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                            rune=rune, artifact=artifact, guild_tech=guild_tech, 
                            familiar_stats=familiar_stats)

        if self.star < 8:
            self.true_damage += 0.48
            self.atk *= 1.4
        else:
            self.true_damage += 0.54
            self.atk *= 1.45

    def skill(self):
        name = 'Goddess Benison'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)
        hit_power = [self.atk * 0.69] * len(targets_hit)
        heal_power = self.atk * 1.3
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        if targets_hit:
            for target in self.own_team.heroes:
                self.heal(target, power=heal_power, turns=1, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Hallowed Pray'
        power = self.atk * 0.7
        if self.star >= 7:
            power = self.atk * 1.15
        self.heal(self, power=power, turns=1, name=name)
        super().on_attack(target)

    def on_hit(self, attacker):
        name = 'Inviolability'
        power = self.atk * 1.8
        if self.star >= 9:
            power = self.atk * 2.1
        self.try_hit_passive(attacker, power=power, chance=0.35, name=name)
        super().on_hit(attacker)


@dataclass
class Hero:
    empty = EmptyHero
    aden = Aden
    blood_tooth = BloodTooth
    centaur = Centaur
    dziewona = Dziewona
    forest_healer = ForestHealer
    freya = Freya
    gerald = Gerald
    luna = Luna
    medusa = Medusa
    minotaur = Minotaur
    monkey_king = MonkeyKing
    reaper = Reaper
    ripper = Ripper
    rlyeh = Rlyeh
    saw_machine = SawMachine
    scarlet = Scarlet
    shudde_m_ell = ShuddeMell
    ultima = Ultima
    vegvisir = Vegvisir
    verthandi = Verthandi


hero_from_request = {
                    'EMPTY': Hero.empty, 
                    'ADEN': Hero.aden, # add stats
                    'BLOOD_TOOTH': Hero.blood_tooth, # add stats, add 9* skill values
                    'CENTAUR': Hero.centaur, 
                    'DZIEWONA': Hero.dziewona, 
                    'FOREST_HEALER': Hero.forest_healer, 
                    'FREYA': Hero.freya, 
                    'GERALD': Hero.gerald, 
                    'LUNA': Hero.luna, 
                    'MEDUSA': Hero.medusa, 
                    'MINOTAUR': Hero.minotaur, # add stats, add 9* skill values
                    'MONKEY_KING': Hero.monkey_king, # add stats, add 9* skill values
                    'REAPER': Hero.reaper, 
                    'RIPPER': Hero.ripper, # add stats, add 9* skill values
                    'RLYEH': Hero.rlyeh, 
                    'SAW_MACHINE': Hero.saw_machine, 
                    'SCARLET': Hero.scarlet, 
                    'SHUDDE_M_ELL': Hero.shudde_m_ell, # add stats, add 9* skill values
                    'ULTIMA': Hero.ultima, # add stats, add 9* skill values
                    'VEGVISIR': Hero.vegvisir, # add stats, add 9* skill values
                    'VERTHANDI': Hero.verthandi # add stats
                    }
