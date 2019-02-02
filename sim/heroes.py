import random as rd
from dataclasses import dataclass
import copy

from sim.models import Faction, HeroType, HeroName, Equipment, Armor, Helmet, Weapon, Pendant, Rune, Artifact, Aura, Familiar, Effect, Action
from sim.settings import guild_tech_maxed, guild_tech_empty, default_familiar_stats, default_familiar
from sim.processing import EmptyGame
from sim.utils import targets_at_random


## Heroes
class BaseHero:
    def __init__(self, armor, helmet, weapon, pendant, rune, artifact, guild_tech, 
                                                            familiar_stats, player):
        if not player:
            armor = Armor.empty
            helmet = Helmet.empty
            weapon = Weapon.empty
            pendant = Pendant.empty
            rune = Rune.empty
            artifact = Artifact.empty
            guild_tech = guild_tech_empty
            familiar_stats = [0, 0]

        self.energy = 50
        self.atk_bonus = 0
        self.hp_bonus = 0
        self.armor_break = 0
        self.skill_damage = 0
        self.hit_rate = 0
        self.dodge = 0
        self.crit_rate = 0
        self.crit_damage = 0
        self.true_damage = 0
        self.damage_reduction = 0
        self.control_immune = 0
        self.silence_immune = 0
        self.stun_immune = 0
        self.damage_to_warriors = 0
        self.damage_to_assassins = 0
        self.damage_to_wanderers = 0
        self.damage_to_clerics = 0
        self.damage_to_mages = 0
        self.damage_to_poisoned = 0
        self.damage_to_bleeding = 0
        self.damage_to_stunned = 0
        self.damage_to_petrified = 0
        self.healing_bonus = 0

        self.own_team = None
        self.op_team = None
        self.game = EmptyGame()
        self.pos = None
        self.str_id = self.name.value
        self.is_dead = False
        self.can_attack = True
        self.effects = []

        self.chest = armor.__class__.__name__
        self.helmet = helmet.__class__.__name__
        self.weapon = weapon.__class__.__name__
        self.pendant = pendant.__class__.__name__
        self.rune = rune
        self.artifact = artifact

        self.has_dropped_below_60 = False
        self.has_dropped_below_30 = False

        self.compute_familiar_stats(familiar_stats)
        self.compute_items(armor, helmet, weapon, pendant, rune, artifact)
        self.compute_guild_tech(guild_tech)

    def compute_familiar_stats(self, familiar_stats):
        self.hp += familiar_stats[0]
        self.atk += familiar_stats[1]

    def compute_items(self, armor, helmet, weapon, pendant, rune, artifact):
        equipment = Equipment(armor, helmet, weapon, pendant)  # equipment
        self.atk += equipment.atk
        self.hp += equipment.hp
        self.atk += rune.atk  # rune
        self.hp += rune.hp
        self.speed += rune.speed
        self.armor_break += rune.armor_break
        self.skill_damage += rune.skill_damage
        self.hit_rate += rune.hit_rate
        self.dodge += rune.dodge
        self.crit_rate += rune.crit_rate
        self.crit_damage += rune.crit_damage
        self.energy += artifact.energy  # artifact
        self.atk += artifact.atk
        self.hp += artifact.hp
        self.speed += artifact.speed
        self.hit_rate += artifact.hit_rate
        self.crit_rate += artifact.crit_rate
        self.crit_damage += artifact.crit_damage
        self.true_damage += artifact.true_damage
        self.damage_reduction += artifact.damage_reduction
        self.damage_to_warriors += artifact.damage_to_warriors
        self.damage_to_assassins += artifact.damage_to_assassins
        self.damage_to_wanderers += artifact.damage_to_wanderers
        self.damage_to_clerics += artifact.damage_to_clerics
        self.damage_to_mages += artifact.damage_to_mages
        if self.faction == Faction.ALLIANCE:
            self.skill_damage += artifact.skill_damage_if_alliance
            self.crit_rate += artifact.crit_rate_if_alliance
        if self.faction == Faction.HORDE:
            self.skill_damage += artifact.skill_damage_if_horde
            self.crit_rate += artifact.crit_rate_if_horde
        if self.faction == Faction.ELF:
            self.skill_damage += artifact.skill_damage_if_elf
            self.crit_rate += artifact.crit_rate_if_elf
        if self.faction == Faction.UNDEAD:
            self.skill_damage += artifact.skill_damage_if_undead
            self.crit_rate += artifact.crit_rate_if_undead
        if self.faction == Faction.HEAVEN:
            self.skill_damage += artifact.skill_damage_if_heaven
            self.crit_rate += artifact.crit_rate_if_heaven
            self.true_damage += artifact.true_damage_if_heaven
        if self.faction == Faction.HELL:
            self.skill_damage += artifact.skill_damage_if_hell
            self.crit_rate += artifact.crit_rate_if_hell
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
        return 0

    def compute_damage(self, target, power, skill=False, active=False):
        faction_damage = 0
        if self.faction_bonus(target):
            faction_damage = 0.3

        type_damage = self.type_damage(target)

        op_armor = target.armor - self.armor_break
        damage_reduction_from_armor = op_armor * 0.00992543 + 0.20597124

        crit_damage = 0
        if active:
            crit = self.compute_crit(target)
            if crit:
                crit_damage = self.crit_damage + 0.5

        skill_damage = 0
        if skill:
            skill_damage += self.skill_damage

        poisoned_extra_damage = 0
        if target.is_poisoned():
            poisoned_extra_damage = self.damage_to_poisoned
        bleeding_extra_damage = 0
        if target.is_bleeding():
            bleeding_extra_damage = self.damage_to_bleeding
        stunned_extra_damage = 0
        if target.is_stunned():
            stunned_extra_damage = self.damage_to_stunned
        petrified_extra_damage = 0
        if target.is_petrified():
            petrified_extra_damage = self.damage_to_petrified

        dmg = (power + skill_damage * self.atk) * (1 - damage_reduction_from_armor) \
              * (1 + crit_damage) * (1 + faction_damage) \
              * (1 + self.true_damage) * (1 - target.damage_reduction) \
              * (1 + type_damage) \
              * (1 + poisoned_extra_damage) * (1 + bleeding_extra_damage) \
              * (1 + stunned_extra_damage) * (1 + petrified_extra_damage)

        damage_components = {'Power': power,
                             'Skill damage': skill_damage,
                             'Damage reduction from armor': damage_reduction_from_armor,
                             'Crit damage': crit_damage,
                             'True damage': self.true_damage,
                             'Damage reduction': target.damage_reduction,
                             'Faction damage': faction_damage,
                             'Type damage': type_damage,
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
        if rd.random() <= target.dodge - hit_rate and not target.is_dead:
            dodged = True

        if dodged:
            action = Action.dodge(self, target, name)
            action.text = '\n{} dodges {} from {}' \
                .format(target.str_id, name, self.str_id)
            self.game.actions.append(action)

            target.stats['dodges'] += 1
            self.stats['dodges_taken'] += 1

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
                action = Action.is_stunned(e.source, self, e.turns, e.name)
                action.text = '\n{} is stunned by {} ({}, {} turns left) ' \
                                 'and cannot play' \
                    .format(self.str_id, e.source.str_id, e.name, e.turns)
                self.game.actions.append(action)
            for e in [e for e in self.effects if isinstance(e, Effect.petrify)]:
                action = Action.is_petrified(e.source, self, e.turns, e.name)
                action.text = '\n{} is petrified by {} ({}, {} turns left) ' \
                                 'and cannot play' \
                    .format(self.str_id, e.source.str_id, e.name, e.turns)
                self.game.actions.append(action)
            for e in [e for e in self.effects if isinstance(e, Effect.freeze)]:
                action = Action.is_frozen(e.source, self, e.turns, e.name)
                action.text = '\n{} is frozen by {} ({}, {} turns left) ' \
                                 'and cannot play' \
                    .format(self.str_id, e.source.str_id, e.name, e.turns)
                self.game.actions.append(action)
            hard_ccs = [e for e in self.effects if isinstance(e, Effect.stun) 
                                                or isinstance(e, Effect.petrify)
                                                or isinstance(e, Effect.freeze)]
            source = hard_ccs[0].source
            source.stats['effective_hard_cc_turns'] += 1
            self.stats['effective_hard_cc_turns_taken'] += 1

        else:
            if self.energy >= 100 and self.is_silenced():
                for e in [e for e in self.effects if isinstance(e, Effect.silence)]:
                    action = Action.is_silenced(e.source, self, e.turns, e.name)
                    action.text = '\n{} is silenced by {} ({}, {} turns left) ' \
                                     'and cannot use its skill' \
                        .format(self.str_id, e.source.str_id, e.name, e.turns)
                    self.game.actions.append(action)
                silences = [e for e in self.effects if isinstance(e, Effect.silence)]
                source = silences[0].source
                source.stats['effective_silence_turns'] += 1
                self.stats['effective_silence_turns_taken'] += 1

            if self.energy >= 100 and not self.is_silenced():
                self.skill()
            else:
                self.attack()
            self.stats['turns_played'] += 1

            for h in self.own_team.heroes:
                if isinstance(h, Wolnir) and h.str_id != self.str_id:
                    this_name = 'Bone Pact'
                    this_power = 0.3
                    if h.star >= 8:
                        this_power = 0.375
                    h.heal(h, power=this_power, turns=1, name=this_name)

        self.can_attack = False

    def attack(self, target=None, power=None, name='attack'):
        if target is None:
            target = self.op_team.next_target()
        if power is None:
            power = self.atk

        dodged = self.compute_dodge(target, name=name)
        if not dodged:
            self.hit_attack(target, power=power, name=name)

        return dodged

    def skill(self):
        self.energy = 0

        for h in self.game.heroes:
            if isinstance(h, Chessia) and not h.is_dead:
                name = 'Dark Storage'
                h.energy_up(h, up=12.5, name=name, passive=True)

        self.own_team.pet.energy = max(min(self.own_team.pet.energy + 12.5, 100), self.energy)

        self.stats['skills'] += 1

    def update_state(self, target, on_attack, active, crit, energy_on_hit=False):
        target.has_taken_damage(self)
        if energy_on_hit:
            if not isinstance(target, Chessia):
                target.energy = max(min(target.energy + 10, 100), target.energy)
        if crit:
            self.on_crit(target)
        if active:
            target.on_hit(self)
        if on_attack:
            self.on_attack(target)

    def hit(self, target, power, skill, active, on_attack, multi, 
                        multi_attack=False, update=True, name=''):
        if not multi:
            if not target.is_dead:
                damage_components = self.compute_damage(target, power, skill=skill, active=active)
                dmg = damage_components['Total damage']
                crit = True if damage_components['Crit damage'] > 0 else False
                crit_str = ', crit' if crit else ''

                target.hp -= dmg
                action = Action.hit(self, target, damage_components, name)
                action.text = '\n{} takes {} damage from {} ({}{})' \
                    .format(target.str_id, round(dmg), self.str_id, name, crit_str)
                self.game.actions.append(action)

                self.stats['damage_by_skill'][name] += dmg
                self.stats['damage_by_target'][target.str_id] += dmg
                target.stats['damage_taken_by_skill'][name] += dmg
                target.stats['damage_taken_by_source'][self.str_id] += dmg

                if update:
                    self.update_state(target, on_attack, active, crit, energy_on_hit=True)

                return [crit]
            return [False]

        else:
            crits = []
            for i, t in enumerate(target):
                p = power[i]
                crit = self.hit(t, p, skill, active, on_attack,
                                multi=False, update=False, name=name)[0]
                crits.append(crit)
            targets_not_dead = [tar for tar in target if not tar.is_dead]
            for i, t in enumerate(targets_not_dead):
                energy_on_hit = i == 0
                crit = crits[i]
                this_on_attack = on_attack and ((not multi_attack) or i == 0)
                self.update_state(t, this_on_attack, active, crit, energy_on_hit=energy_on_hit)

            return crits

    def hit_attack(self, target, power, multi=False, name='attack'):
        crits = self.hit(target, power, skill=False, active=True,
                        on_attack=True, multi=multi, multi_attack=multi, name=name)

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

    def hit_ally(self, target, power, name=''):
        if not target.is_dead:
            target.hp -= power
            damage_components = {'Power': power,
                                'Skill damage': 0,
                                'Damage reduction from armor': 0,
                                'Crit damage': 0,
                                'True damage': 0,
                                'Damage reduction': 0,
                                'Faction damage': 0,
                                'Base type damage': 0,
                                'Extra type damage': 0,
                                'Poisoned extra damage': 0,
                                'Bleeding extra damage': 0,
                                'Stunned extra damage': 0,
                                'Total damage': power}
            action = Action.hit(self, target, damage_components, name)
            action.text = '\n{} takes {} damage from {} ({})' \
                .format(target.str_id, round(power), self.str_id, name)
            self.game.actions.append(action)

            self.stats['healing_by_skill'][name] -= power
            self.stats['healing_by_target'][target.str_id] -= power
            target.stats['healing_taken_by_skill'][name] -= power
            target.stats['healing_taken_by_source'][self.str_id] -= power
            self.stats['effective_healing_by_skill'][name] -= power
            self.stats['effective_healing_by_target'][target.str_id] -= power
            target.stats['effective_healing_taken_by_skill'][name] -= power
            target.stats['effective_healing_taken_by_source'][self.str_id] -= power

            self.update_state(target, on_attack=False, active=False, 
                                        crit=False, energy_on_hit=False)

    def dot(self, target, power, turns, name=''):
        if not target.is_dead:
            dot = Effect.dot(self, target, power, turns, name=name)
            target.effects.append(dot)
            dot.tick()

            self.stats['dots'] += 1
            target.stats['dots_taken'] += 1

    def try_dot(self, target, power, turns, chance, name=''):
        if rd.random() <= chance:
            self.dot(target, power, turns, name=name)
            return True

    def heal(self, target, power, turns, name='', override=False):
        if not target.is_dead and (not self.game.is_finished() or override):
            power *= 1 + self.healing_bonus
            heal = Effect.heal(self, target, power, turns, name=name)
            target.effects.append(heal)
            heal.tick()

    def try_heal(self, target, power, turns, chance, name=''):
        if rd.random() <= chance:
            self.heal(target, power, turns, name=name)
            return True

    def poison(self, target, power, turns, name=''):
        if not target.is_dead:
            poison = Effect.poison(self, target, power, turns, name=name)
            target.effects.append(poison)
            poison.tick()

            self.stats['poisons'] += 1
            target.stats['poisons_taken'] += 1
            self.stats['dots'] += 1
            target.stats['dots_taken'] += 1

    def try_poison(self, target, power, turns, chance, name=''):
        if rd.random() <= chance:
            self.poison(target, power, turns, name=name)
            return True

    def bleed(self, target, power, turns, name=''):
        if not target.is_dead:
            bleed = Effect.bleed(self, target, power, turns, name=name)
            target.effects.append(bleed)
            bleed.tick()

            self.stats['bleeds'] += 1
            target.stats['bleeds_taken'] += 1
            self.stats['dots'] += 1
            target.stats['dots_taken'] += 1

    def try_bleed(self, target, power, turns, chance, name=''):
        if rd.random() <= chance:
            self.bleed(target, power, turns, name=name)
            return True

    def timed_mark(self, target, power, turns, name=''):
        if not target.is_dead:
            timed_mark = Effect.timed_mark(self, target, power, turns, name=name)
            target.effects.append(timed_mark)
            timed_mark.tick()

    def crit_mark(self, target, power, second_hit=False, name=''):
        if not target.is_dead:
            crit_mark = Effect.crit_mark(self, target, power, second_hit=second_hit, name=name)
            target.effects.append(crit_mark)
            crit_mark.tick()

    def silence(self, target, turns, name=''):
        if not target.is_dead and rd.random() >= target.silence_immune and rd.random() >= target.control_immune:
            silence = Effect.silence(self, target, turns, name=name)
            target.effects.append(silence)
            silence.tick()

            self.stats['silences'] += 1
            target.stats['silences_taken'] += 1

            return True

    def try_silence(self, target, turns, chance, name=''):
        if rd.random() <= chance:
            hit = self.silence(target, turns, name=name)
            return hit

    def stun(self, target, turns, name=''):
        if not target.is_dead and rd.random() >= target.stun_immune and rd.random() >= target.control_immune:
            stun = Effect.stun(self, target, turns, name=name)
            target.effects.append(stun)
            stun.tick()

            self.stats['stuns'] += 1
            target.stats['stuns_taken'] += 1
            self.stats['hard_ccs'] += 1
            target.stats['hard_ccs_taken'] += 1

            return True

    def try_stun(self, target, turns, chance, name=''):
        if rd.random() <= chance:
            hit = self.stun(target, turns, name=name)
            return hit

    def petrify(self, target, turns, name=''):
        if not target.is_dead and rd.random() >= target.control_immune:
            petrify = Effect.petrify(self, target, turns, name=name)
            target.effects.append(petrify)
            petrify.tick()

            self.stats['petrifies'] += 1
            target.stats['petrifies_taken'] += 1
            self.stats['hard_ccs'] += 1
            target.stats['hard_ccs_taken'] += 1

            return True

    def try_petrify(self, target, turns, chance, name=''):
        if rd.random() <= chance:
            hit = self.petrify(target, turns, name=name)
            return hit

    def freeze(self, target, turns, name=''):
        if not target.is_dead and rd.random() >= target.control_immune:
            freeze = Effect.freeze(self, target, turns, name=name)
            target.effects.append(freeze)
            freeze.tick()

            self.stats['freezes'] += 1
            target.stats['freezes_taken'] += 1
            self.stats['hard_ccs'] += 1
            target.stats['hard_ccs_taken'] += 1

            return True

    def try_freeze(self, target, turns, chance, name=''):
        if rd.random() <= chance:
            hit = self.freeze(target, turns, name=name)
            return hit

    def cleanse(self, target, name):
        for e in [e for e in target.effects if isinstance(e, Effect.stun)
                                        or isinstance(e, Effect.petrify)
                                        or isinstance(e, Effect.freeze)
                                        or isinstance(e, Effect.silence)]:
            e.kill()
        action = Action.cleanse(self, target, name)
        action.text = "\n{}'s controls are removed by {} ({})" \
            .format(target.str_id, self.str_id, name)
        self.game.actions.append(action)

    def attack_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            attack_up = Effect.attack_up(self, target, up, turns, name=name, passive=passive)
            target.effects.append(attack_up)
            attack_up.tick()

            if not passive:
                self.stats['attack_ups'] += 1
                target.stats['attack_ups_taken'] += 1

    def try_attack_up(self, target, up, turns, chance, name='', passive=False):
        if rd.random() <= chance:
            self.attack_up(target, up, turns, name=name, passive=passive)
            return True

    def attack_down(self, target, down, turns, name='', passive=False):
        if not target.is_dead:
            attack_down = Effect.attack_down(self, target, down, turns,
                                             name=name, passive=passive)
            target.effects.append(attack_down)
            attack_down.tick()

            if not passive:
                self.stats['attack_downs'] += 1
                target.stats['attack_downs_taken'] += 1

    def try_attack_down(self, target, down, turns, chance, name='', passive=False):
        if rd.random() <= chance:
            self.attack_down(target, down, turns, name=name, passive=passive)
            return True

    def hp_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            hp_up = Effect.hp_up(self, target, up, turns, name=name, passive=passive)
            target.effects.append(hp_up)
            hp_up.tick()

            if not passive:
                self.stats['hp_ups'] += 1
                target.stats['hp_ups_taken'] += 1

    def hp_down(self, target, down, turns, name='', passive=False):
        if not target.is_dead:
            hp_down = Effect.hp_down(self, target, down, turns, name=name, passive=passive)
            target.effects.append(hp_down)
            hp_down.tick()

            if not passive:
                self.stats['hp_downs'] += 1
                target.stats['hp_downs_taken'] += 1

    def crit_rate_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            crit_rate_up = Effect.crit_rate_up(self, target, up, turns,
                                               name=name, passive=passive)
            target.effects.append(crit_rate_up)
            crit_rate_up.tick()

            if not passive:
                self.stats['crit_rate_ups'] += 1
                target.stats['crit_rate_ups_taken'] += 1

    def try_crit_rate_up(self, target, up, turns, chance, name='', passive=False):
        if rd.random() <= chance:
            self.crit_rate_up(target, up, turns, name=name, passive=passive)
            return True

    def crit_rate_down(self, target, down, turns, name='', passive=False):
        if not target.is_dead:
            crit_rate_down = Effect.crit_rate_down(self, target, down, turns,
                                                   name=name, passive=passive)
            target.effects.append(crit_rate_down)
            crit_rate_down.tick()

            if not passive:
                self.stats['crit_rate_downs'] += 1
                target.stats['crit_rate_downs_taken'] += 1

    def try_crit_rate_down(self, target, down, turns, chance, name='', passive=False):
        if rd.random() <= chance:
            self.crit_rate_down(target, down, turns, name=name, passive=passive)
            return True

    def crit_damage_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            crit_damage_up = Effect.crit_damage_up(self, target, up, turns,
                                                   name=name, passive=passive)
            target.effects.append(crit_damage_up)
            crit_damage_up.tick()

            if not passive:
                self.stats['crit_damage_ups'] += 1
                target.stats['crit_damage_ups_taken'] += 1

    def try_crit_damage_up(self, target, up, turns, chance, name='', passive=False):
        if rd.random() <= chance:
            self.crit_damage_up(target, up, turns, name=name, passive=passive)
            return True

    def crit_damage_down(self, target, down, turns, name='', passive=False):
        if not target.is_dead:
            crit_damage_down = Effect.crit_damage_down(self, target, down, turns,
                                                       name=name, passive=passive)
            target.effects.append(crit_damage_down)
            crit_damage_down.tick()

            if not passive:
                self.stats['crit_damage_downs'] += 1
                target.stats['crit_damage_downs_taken'] += 1

    def try_crit_damage_down(self, target, down, turns, chance, name='', passive=False):
        if rd.random() <= chance:
            self.crit_damage_down(target, down, turns, name=name, passive=passive)
            return True

    def hit_rate_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            hit_rate_up = Effect.hit_rate_up(self, target, up, turns, name=name, passive=passive)
            target.effects.append(hit_rate_up)
            hit_rate_up.tick()

            if not passive:
                self.stats['hit_rate_ups'] += 1
                target.stats['hit_rate_ups_taken'] += 1

    def hit_rate_down(self, target, down, turns, name='', passive=False):
        if not target.is_dead:
            hit_rate_down = Effect.hit_rate_down(self, target, down, turns,
                                                 name=name, passive=passive)
            target.effects.append(hit_rate_down)
            hit_rate_down.tick()

            if not passive:
                self.stats['hit_rate_downs'] += 1
                target.stats['hit_rate_downs_taken'] += 1

    def dodge_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            dodge_up = Effect.dodge_up(self, target, up, turns, name=name, passive=passive)
            target.effects.append(dodge_up)
            dodge_up.tick()

            if not passive:
                self.stats['dodge_ups'] += 1
                target.stats['dodge_ups_taken'] += 1

    def dodge_down(self, target, down, turns, name='', passive=False):
        if not target.is_dead:
            dodge_down = Effect.dodge_down(self, target, down, turns, name=name, passive=passive)
            target.effects.append(dodge_down)
            dodge_down.tick()

            if not passive:
                self.stats['dodge_downs'] += 1
                target.stats['dodge_downs_taken'] += 1

    def skill_damage_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            skill_damage_up = Effect.skill_damage_up(self, target, up, turns,
                                                     name=name, passive=passive)
            target.effects.append(skill_damage_up)
            skill_damage_up.tick()

            if not passive:
                self.stats['skill_damage_ups'] += 1
                target.stats['skill_damage_ups_taken'] += 1

    def skill_damage_down(self, target, down, turns, name='', passive=False):
        if not target.is_dead:
            skill_damage_down = Effect.skill_damage_down(self, target, down, turns,
                                                         name=name, passive=passive)
            target.effects.append(skill_damage_down)
            skill_damage_down.tick()

            if not passive:
                self.stats['skill_damage_downs'] += 1
                target.stats['skill_damage_downs_taken'] += 1

    def control_immune_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            control_immune_up = Effect.control_immune_up(self, target, up, turns,
                                                         name=name, passive=passive)
            target.effects.append(control_immune_up)
            control_immune_up.tick()

            if not passive:
                self.stats['control_immune_ups'] += 1
                target.stats['control_immune_ups_taken'] += 1

    def control_immune_down(self, target, down, turns, name='', passive=False):
        if not target.is_dead:
            control_immune_down = Effect.control_immune_down(self, target, down, turns,
                                                             name=name, passive=passive)
            target.effects.append(control_immune_down)
            control_immune_down.tick()

            if not passive:
                self.stats['control_immune_downs'] += 1
                target.stats['control_immune_downs_taken'] += 1

    def silence_immune_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            silence_immune_up = Effect.silence_immune_up(self, target, up, turns,
                                                         name=name, passive=passive)
            target.effects.append(silence_immune_up)
            silence_immune_up.tick()

    def stun_immune_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            stun_immune_up = Effect.stun_immune_up(self, target, up, turns,
                                                         name=name, passive=passive)
            target.effects.append(stun_immune_up)
            stun_immune_up.tick()

    def damage_reduction_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            damage_reduction_up = Effect.damage_reduction_up(self, target, up, turns,
                                                             name=name, passive=passive)
            target.effects.append(damage_reduction_up)
            damage_reduction_up.tick()

            if not passive:
                self.stats['damage_reduction_ups'] += 1
                target.stats['damage_reduction_ups_taken'] += 1

    def true_damage_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            true_damage_up = Effect.true_damage_up(self, target, up, turns,
                                                   name=name, passive=passive)
            target.effects.append(true_damage_up)
            true_damage_up.tick()

            if not passive:
                self.stats['true_damage_ups'] += 1
                target.stats['true_damage_ups_taken'] += 1

    def armor_break_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            armor_break_up = Effect.armor_break_up(self, target, up, turns,
                                                   name=name, passive=passive)
            target.effects.append(armor_break_up)
            armor_break_up.tick()

            if not passive:
                self.stats['armor_break_ups'] += 1
                target.stats['armor_break_ups_taken'] += 1

    def try_armor_break_up(self, target, up, turns, chance, name='', passive=False):
        if rd.random() <= chance:
            self.armor_break_up(target, up, turns, name=name, passive=passive)
            return True

    def armor_break_down(self, target, down, turns, name='', passive=False):
        if not target.is_dead:
            armor_break_down = Effect.armor_break_down(self, target, down, turns,
                                                       name=name, passive=passive)
            target.effects.append(armor_break_down)
            armor_break_down.tick()

            if not passive:
                self.stats['armor_break_downs'] += 1
                target.stats['armor_break_downs_taken'] += 1

    def try_armor_break_down(self, target, down, turns, chance, name='', passive=False):
        if rd.random() <= chance:
            self.armor_break_down(target, down, turns, name=name, passive=passive)
            return True

    def armor_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            armor_up = Effect.armor_up(self, target, up, turns, name=name, passive=passive)
            target.effects.append(armor_up)
            armor_up.tick()

            if not passive:
                self.stats['armor_ups'] += 1
                target.stats['armor_ups_taken'] += 1

    def armor_down(self, target, down, turns, name='', passive=False):
        if not target.is_dead:
            armor_down = Effect.armor_down(self, target, down, turns, name=name, passive=passive)
            target.effects.append(armor_down)
            armor_down.tick()

            if not passive:
                self.stats['armor_downs'] += 1
                target.stats['armor_downs_taken'] += 1

    def speed_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            speed_up = Effect.speed_up(self, target, up, turns, name=name, passive=passive)
            target.effects.append(speed_up)
            speed_up.tick()

            if not passive:
                self.stats['speed_ups'] += 1
                target.stats['speed_ups_taken'] += 1

    def speed_down(self, target, down, turns, name='', passive=False):
        if not target.is_dead:
            speed_down = Effect.speed_down(self, target, down, turns, name=name, passive=passive)
            target.effects.append(speed_down)
            speed_down.tick()

            if not passive:
                self.stats['speed_downs'] += 1
                target.stats['speed_downs_taken'] += 1

    def energy_up(self, target, up, name='', passive=False, override=False):
        if not target.is_dead and (not self.game.is_finished() or override):
            target.energy = max(min(target.energy + up, 100), self.energy)
            action = Action.energy_up(self, target, up, passive, name)
            action.text = "\n{}'s energy is increased by {} by {} ({})" \
                .format(target.str_id, up, self.str_id, name)
            self.game.actions.append(action)

            if not passive:
                self.stats['energy_ups'] += 1
                target.stats['energy_ups_taken'] += 1

    def energy_down(self, target, down, name='', passive=False):
        if not target.is_dead:
            target.energy = max(target.energy - down, 0)
            action = Action.energy_down(self, target, down, passive, name)
            action.text = "\n{}'s energy is reduced by {} by {} ({})" \
                .format(target.str_id, down, self.str_id, name)
            self.game.actions.append(action)

            if not passive:
                self.stats['energy_downs'] += 1
                target.stats['energy_downs_taken'] += 1

    def damage_to_bleeding_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            damage_to_bleeding = Effect.damage_to_bleeding(self, target, up, turns,
                                                           name=name, passive=passive)
            target.effects.append(damage_to_bleeding)
            damage_to_bleeding.tick()

    def damage_to_poisoned_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            damage_to_poisoned = Effect.damage_to_poisoned(self, target, up, turns,
                                                           name=name, passive=passive)
            target.effects.append(damage_to_poisoned)
            damage_to_poisoned.tick()

    def damage_to_stunned_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            damage_to_stunned = Effect.damage_to_stunned(self, target, up, turns,
                                                         name=name, passive=passive)
            target.effects.append(damage_to_stunned)
            damage_to_stunned.tick()

    def damage_to_petrified_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            damage_to_petrified = Effect.damage_to_petrified(self, target, up, turns,
                                                         name=name, passive=passive)
            target.effects.append(damage_to_petrified)
            damage_to_petrified.tick()

    def damage_to_warriors_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            damage_to_warriors = Effect.damage_to_warriors(self, target, up, turns,
                                                           name=name, passive=passive)
            target.effects.append(damage_to_warriors)
            damage_to_warriors.tick()

    def healing_up(self, target, up, turns, name='', passive=False):
        if not target.is_dead and not self.game.is_finished():
            healing_up = Effect.healing_up(self, target, up, turns,
                                        name=name, passive=passive)
            target.effects.append(healing_up)
            healing_up.tick()

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
            self.kill()

            if isinstance(attacker, BaseHero):
                attacker.on_kill(self)
            self.on_death(attacker)

    def kill(self):
        self.is_dead = True
        self.can_attack = False
        action = Action.die(self)
        action.text = '\n{} dies'.format(self.str_id)
        self.game.actions.append(action)

    def has_been_healed(self, source):
        pass

    def on_attack(self, target):
        if not isinstance(self, Chessia):
            self.energy = max(min(self.energy + 50, 100), self.energy)

    def on_crit(self, target):
        for e in [e for e in target.effects if isinstance(e, Effect.crit_mark)]:
            e.trigger()

        for h in self.own_team.heroes:
            if isinstance(h, TigerKing):
                name = 'Sqalid Fever'
                heal_power = 0.45
                if h.star >= 8:
                    heal_power = 0.9
                h.heal(h, power=heal_power, turns=1, name=name)

        self.stats['crits'] += 1
        target.stats['crits_taken'] += 1

    def on_hit(self, attacker):
        attacker.stats['hits'] += 1
        self.stats['hits_taken'] += 1

    def on_kill(self, target):
        self.stats['kills'] += 1

    def on_death(self, attacker):
        for h in self.op_team.heroes:
            if isinstance(h, Aden) and not h.is_dead:
                name = 'Blood Temple'
                power = 0.8
                if h.star >= 9:
                    power = 1.0
                if attacker is not None:
                    if attacker.str_id == h.str_id:
                        power *= 2
                h.heal(h, power=power, turns=1, name=name, override=True)

        for h in self.op_team.heroes:
            if isinstance(h, BloodTooth) and not h.is_dead:
                name = 'Executioner'
                up = 0.2
                if h.star >= 8:
                    up = 0.3
                h.attack_up(h, up=up, turns=None, name=name)

        for h in self.op_team.heroes:
            if isinstance(h, Lindberg) and not h.is_dead:
                name = 'Bloodthirsty Ointment'
                energy_up = 100
                h.energy_up(h, up=energy_up, name=name, override=True)

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
            if isinstance(h, Martin) and not h.is_dead:
                name = 'One On One'
                attack_up = 0.13
                skill_damage_up = 0.125
                if h.star >= 7:
                    attack_up = 0.15
                    skill_damage_up = 0.175
                h.attack_up(h, up=attack_up, turns=None, name=name)
                h.skill_damage_up(h, up=skill_damage_up, turns=None, name=name)

        for h in self.op_team.heroes:
            if isinstance(h, Martin) and not h.is_dead:
                name = 'Slide Tackle'
                crit_rate_up = 0.14
                crit_damage_up = 0.08
                if h.star >= 8:
                    crit_rate_up = 0.18
                    crit_damage_up = 0.11
                h.crit_rate_up(h, up=crit_rate_up, turns=None, name=name)
                h.crit_damage_up(h, up=crit_damage_up, turns=None, name=name)

        for h in self.op_team.heroes:
            if isinstance(h, Orphee) and not h.is_dead:
                name = 'Pity'
                power = 1.4
                if h.star >= 9:
                    power = 1.8
                h.heal(h, power=power, turns=1, name=name, override=True)

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

        for h in self.game.heroes:
            if isinstance(h, Valkyrie) and not h.is_dead:
                name = 'Spiritual Guide'
                power = 2.0
                speed_up = 8
                skill_damage_up = 0.3
                if h.star >= 9:
                    power = 3.0
                    speed_up = 10
                    skill_damage_up = 0.4
                min_ally_hp = min([h2.hp for h2 in h.own_team.heroes if not h2.is_dead])
                candidates = [h2 for h2 in h.own_team.heroes if h2.hp == min_ally_hp]
                rd.shuffle(candidates)
                target = candidates[0]
                h.heal(target, power=power, turns=1, name=name)
                h.speed_up(h, up=speed_up, turns=None, name=name)
                h.skill_damage_up(h, up=skill_damage_up, turns=None, name=name)

        for h in self.game.heroes:
            if isinstance(h, Xexanoth) and not h.is_dead:
                name = 'Death Focus'
                armor_break_up = 1
                h.armor_break_up(h, up=armor_break_up, turns=None, name=name)

        self.stats['deaths'] += 1

    def print_stats(self):
        stats = [self.hp, self.atk, self.armor, self.speed,
                 self.armor_break, self.skill_damage, self.hit_rate, self.dodge,
                 self.crit_rate, self.crit_damage, self.true_damage, self.damage_reduction,
                 self.control_immune]
        stats_names = ['Hp', 'Atk', 'Armor', 'Speed',
                       'Armor break', 'Skill damage', 'Hit rate', 'Dodge',
                       'Crit rate', 'Crit damage', 'True damage', 'Damage reduction',
                       'Control immune']
        for stat, name in zip(stats, stats_names):
            print('{}\t{}'.format(name, stat))


class EmptyHero(BaseHero):
    name = HeroName.EMPTY
    faction = Faction.EMPTY
    type = HeroType.EMPTY

    is_dead = True
    can_attack = False

    def __init__(self):
        self.hp = 0
        self.atk = 0
        self.armor = 0
        self.speed = 0
        self.energy = 0
        self.dodge = 0
        self.crit_rate = 0
        self.control_immune = 0
        self.armor_break = 0
        self.crit_damage = 0
        self.skill_damage = 0
        self.hit_rate = 0
        self.true_damage = 0
        self.damage_reduction = 0
        self.damage_to_warriors = 0
        self.damage_to_assassins = 0
        self.damage_to_wanderers = 0
        self.damage_to_clerics = 0
        self.damage_to_mages = 0
        self.effects = []
        self.str_id = self.name.value


class AbyssLord(BaseHero):
    name = HeroName.ABYSS_LORD
    faction = Faction.HORDE
    type = HeroType.WARRIOR

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.evasion.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 398425.7
        self.atk = 15909.0
        self.armor = 12
        self.speed = 1160
        if self.star == 9:
            self.hp = 200000.0  # should depend on the level
            self.atk = 14000.0  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        self.has_triggered = False

        name = 'Abyssal Protection'
        armor_up = 10
        hp_up = 0.3
        if self.star >= 8:
            armor_up = 12
            hp_up = 0.4
        self.armor_up(self, up=armor_up, turns=None,
                      name=name, passive=True)
        self.hp_up(self, up=hp_up, turns=None,
                       name=name, passive=True)

    def skill(self):
        name = 'Abyssal Blade'
        target = self.op_team.next_target()
        dmg_power = self.atk * 2.8
        heal_power = 2.1
        if self.star >= 10:
            dmg_power = self.atk * 3.2
            heal_power = 3

        self.hit_skill(target, power=dmg_power, name=name)
        self.heal(self, power=heal_power, turns=1, name=name)
        if self.star >= 10:
            attack_up = 0.5
            self.attack_up(self, up=attack_up, turns=2, name=name)
        super().skill()

    def on_hit(self, attacker):
        name = 'Pitch-Black Curse'
        down = 0.15
        if self.star >= 7:
            down = 0.18
        self.crit_rate_down(attacker, down=down, turns=3, name=name)
        super().on_hit(attacker)

    def has_taken_damage(self, attacker):
        if self.hp <= self.hp_max * 0.3 and not self.has_triggered:
            self.has_triggered = True
            name = 'Rebirth'
            up = 30
            if self.star >= 9:
                up = 36
            self.armor_up(self, up=up, turns=3, name=name)
        super().has_taken_damage(attacker)


class Aden(BaseHero):
    name = HeroName.ADEN
    faction = Faction.UNDEAD
    type = HeroType.ASSASSIN

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.attack.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 330768.0
        self.atk = 25174.0
        self.armor = 9
        self.speed = 1178
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Blood Craving'
        hit_rate_up = 0.2
        armor_break_up = 6.4
        damage_to_bleeding_up = 0.4
        if self.star >= 8:
            hit_rate_up = 0.25
            armor_break_up = 9.6
            damage_to_bleeding_up = 0.5
        self.hit_rate_up(self, up=hit_rate_up, turns=None,
                         name=name, passive=True)
        self.armor_break_up(self, up=armor_break_up, turns=None,
                            name=name, passive=True)
        self.damage_to_bleeding_up(self, up=damage_to_bleeding_up, turns=None,
                                   name=name, passive=True)

    def skill(self):
        name = 'Strangle'
        targets = targets_at_random(self.op_team.heroes, 3)
        targets_hit = self.targets_hit(targets, name=name)

        hit_power = [self.atk * 1.48] * len(targets_hit)
        bleed_power = 0.46
        heal_power = 1.0
        if self.star >= 10:
            hit_power = [self.atk * 1.8] * len(targets_hit)
            for i, h in enumerate(targets_hit):
                if h.type == HeroType.WANDERER:
                    hit_power[i] += self.atk * 0.6
            bleed_power = 0.7
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in targets_hit:
            self.bleed(target, power=bleed_power, turns=3, name=name)
        if targets_hit:
            self.heal(self, power=heal_power, turns=1, name=name)
        super().skill()


class BloodTooth(BaseHero):
    name = HeroName.BLOOD_TOOTH
    faction = Faction.HORDE
    type = HeroType.ASSASSIN

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.attack.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 284265.0
        self.atk = 27039.3
        self.armor = 9
        self.speed = 1176
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Rabid'
        attack_up = 0.25
        crit_rate_up = 0.3
        hp_up = 0.15
        if self.star >= 7:
            attack_up = 0.35
            crit_rate_up = 0.3
            hp_up = 0.2
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)
        self.crit_rate_up(self, up=crit_rate_up, turns=None,
                          name=name, passive=True)
        self.hp_up(self, up=hp_up, turns=None,
                   name=name, passive=True)

    def attack(self):
        name = 'attack'
        power = self.atk * 1.1
        if self.star >= 9:
            power = self.atk * 1.3
        min_enemy_hp = min([h.hp for h in self.op_team.heroes if not h.is_dead])
        candidates = [h for h in self.op_team.heroes if h.hp == min_enemy_hp]
        rd.shuffle(candidates)
        target = candidates[0]
        super().attack(target=target, power=power, name=name)

    def skill(self):
        name = 'Power Torture'
        targets = targets_at_random(self.op_team.get_backline(), 2)
        targets_hit = None
        if self.star >= 10:
            targets_hit = targets
        else:
            targets_hit = self.targets_hit(targets, name=name)

        hit_power = [self.atk * 1.76] * len(targets_hit)
        turns = 2
        if self.star >= 10:
            hit_power = [self.atk * 1.9] * len(targets_hit)
            turns = 3
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        if self.star >= 10 and targets_hit:
            heal_power = 1.0
            self.heal(self, power=heal_power, turns=turns, name=name)
        for target in targets_hit:
            drain = 0.22
            if self.star >= 10:
                drain = 0.3
            self.attack_down(target, down=drain, turns=turns, name=name)
            self.attack_up(self, up=drain, turns=turns, name=name)
        super().skill()


class Centaur(BaseHero):
    name = HeroName.CENTAUR
    faction = Faction.ELF
    type = HeroType.WANDERER

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.armor_break.R2, artifact=Artifact.tears_of_the_goddess.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 388869.0
        self.atk = 23251.5
        self.armor = 10
        self.speed = 1148
        if self.star == 9:
            self.hp = 224121.1  # should depend on the level
            self.atk = 13402.1  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 983  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = "Earth's Power"
        crit_rate_up = 0.3
        attack_up = 0.25
        if self.star >= 7:
            crit_rate_up = 0.4
            attack_up = 0.3
        self.crit_rate_up(self, up=crit_rate_up, turns=None,
                          name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)

        name = 'Majestic Countenance'
        damage_to_poisoned_up = 0.5
        if self.star >= 9:
            damage_to_poisoned_up = 0.6
        self.damage_to_poisoned_up(self, up=damage_to_poisoned_up, turns=None,
                                   name=name, passive=True)

    def on_crit(self, target):
        name = 'Toxic Blade'
        power = 0.66
        if self.star >= 8:
            power = 0.78
        self.poison(target, power=power, turns=2, name=name)
        super().on_crit(target)

    def skill(self):
        name = 'Dual Throwing Axe'
        targets = targets_at_random(self.op_team.heroes, 4)
        targets_hit = self.targets_hit(targets, name=name)

        hit_power = [self.atk * 0.8] * len(targets_hit)
        dot_power = 0.3
        if self.star >= 10:
            hit_power = [self.atk] * len(targets_hit)
            dot_power = 0.5
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in targets_hit:
            self.poison(target, power=dot_power, turns=3, name=name)
        if self.star >= 10:
            for target in targets_hit:
                speed_down = 30
                self.speed_down(target, down=speed_down, turns=3, name=name)
        super().skill()


class Chessia(BaseHero):
    name = HeroName.CHESSIA
    faction = Faction.HELL
    type = HeroType.WANDERER

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.armor_break.R2, artifact=Artifact.tears_of_the_goddess.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 358449.0
        self.atk = 25057.7
        self.armor = 10
        self.speed = 1161
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Shadow Queen'
        skill_damage_up = 0.5
        attack_up = 0.25
        silence_immune_up = 0.4
        if self.star >= 7:
            skill_damage_up = 0.625
            attack_up = 0.3
            silence_immune_up = 0.5
        self.skill_damage_up(self, up=skill_damage_up, turns=None,
                             name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)
        self.silence_immune_up(self, up=silence_immune_up, turns=None,
                               name=name, passive=True)

    def skill(self):
        name = 'Black Hole Generated'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        power = [self.atk * 1.24] * len(targets_hit)
        if self.star >= 10:
            power = [self.atk * 1.4] * len(targets_hit)
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            bleed_power = 0.49
            turns = 3
            if self.star >= 10:
                bleed_power = 0.5
                turns = 4
            if target.type == HeroType.WANDERER:
                bleed_power *= 2
            self.bleed(target, power=bleed_power, turns=turns, name=name)
        if self.star >= 10 and targets_hit:
            skill_damage_up = 0.15
            self.skill_damage_up(self, up=skill_damage_up, turns=4, name=name)

        name = 'Shadow Blessing'
        up = 2.0
        if self.star >= 9:
            up = 2.5
        self.skill_damage_up(self, up=up, turns=None, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Dark Storage'
        up = 0.12
        if self.star >= 8:
            up = 0.15
        self.attack_up(self, up=up, turns=3, name=name)
        super().on_attack(target)


class Drow(BaseHero):
    name = HeroName.DROW
    faction = Faction.ELF
    type = HeroType.CLERIC

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.speed.R2, artifact=Artifact.queens_crown.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 326223.2
        self.atk = 26922.3
        self.armor = 9
        self.speed = 1149
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        self.has_triggered = False

        name = 'Embrace The Darkness'
        attack_up = 0.15
        hp_up = 0.2
        crit_rate_up = 0.2
        if self.star >= 7:
            attack_up = 0.3
            hp_up = 0.25
            crit_rate_up = 0.35
        self.attack_up(self, up=attack_up, turns=None,
                            name=name, passive=True)
        self.hp_up(self, up=hp_up, turns=None,
                       name=name, passive=True)
        self.crit_rate_up(self, up=crit_rate_up, turns=None,
                       name=name, passive=True)

    def skill(self):
        name = 'Heart-Taking Thorn'
        targets = targets_at_random(self.op_team.heroes, 4)
        targets_hit = self.targets_hit(targets, name=name)
        hit_power = [self.atk * 1.42] * len(targets_hit)
        heal_power = 0.6
        if self.star >= 10:
            hit_power = [self.atk * 1.82] * len(targets_hit)
            heal_power = 0.75
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in self.own_team.heroes:
            self.heal(target, power=heal_power, turns=6, name=name)
        if self.star >= 10:
            for target in targets_hit:
                if target.type == HeroType.CLERIC:
                    self.try_stun(target, turns=2, chance=0.8, name=name)
                    dot_power = 0.5
                    self.bleed(target, power=dot_power, turns=2, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Living Sacrifice'
        power = 0.6
        attack_up = 0.2
        if self.star >= 8:
            power = 0.75
            attack_up = 0.3
        if not self.game.is_finished():
            self.heal(self, power=power, turns=3, name=name)
        self.attack_up(self, up=attack_up, turns=3, name=name)
        super().on_attack(target)

    def has_taken_damage(self, attacker):
        if self.hp <= self.hp_max * 0.5 and not self.has_triggered:
            self.has_triggered = True
            name = "Evil Goddess's Blessing"
            chance = 0.75
            crit_damage_up = 0.4
            if self.star >= 9:
                chance = 1.0
                crit_damage_up = 0.6
            if rd.random() <= chance:
                for target in self.op_team.heroes:
                    self.silence(target, turns=1, name=name)
            self.crit_damage_up(self, up=crit_damage_up, turns=6, name=name)
        super().has_taken_damage(attacker)


class Dziewona(BaseHero):
    name = HeroName.DZIEWONA
    faction = Faction.UNDEAD
    type = HeroType.ASSASSIN

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.armor_break.R2, artifact=Artifact.tears_of_the_goddess.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 292482.0
        self.atk = 23426.4
        self.armor = 9
        self.speed = 1173
        if self.star == 9:
            self.hp = 168584.5  # should depend on the level
            self.atk = 13496.1  # should depend on the level
            self.armor = 9  # should depend on the level
            self.speed = 1008  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        self.has_triggered = False

        name = 'Stiff Chin'
        armor_break_up = 10.8
        attack_up = 0.22
        if self.star >= 7:
            armor_break_up = 12
            attack_up = 0.25
        self.armor_break_up(self, up=armor_break_up, turns=None,
                            name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)

    def attack(self):
        target = self.op_team.next_target()
        dodged = super().attack(target=target)

        if dodged:
            name = 'Cobweb Trap'
            power = self.atk * 1.4
            if self.star >= 8:
                power = self.atk * 2.8
            self.hit_passive(target, power=power, name=name)

    def skill(self):
        name = 'Spider Attack'
        targets_hit = targets_at_random(self.op_team.heroes, 4)

        power = [self.atk * 1.25] * len(targets_hit)
        if self.star >= 10:
            power = [self.atk * 1.6] * len(targets_hit)
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            if target.type == HeroType.MAGE:
                self.try_stun(target, turns=2, chance=0.8, name=name)
                if self.star >= 10:
                    dot_power = 0.8
                    self.poison(target, power=dot_power, turns=2, name=name)
        super().skill()

    def has_taken_damage(self, attacker):
        if self.hp <= self.hp_max * 0.5 and not self.has_triggered:
            self.has_triggered = True
            name = 'Crouch Ambush'
            up = 0.25
            if self.star >= 9:
                up = 0.35
            self.attack_up(self, up=up, turns=3, name=name)
        super().has_taken_damage(attacker)


class ForestHealer(BaseHero):
    name = HeroName.FOREST_HEALER
    faction = Faction.ELF
    type = HeroType.CLERIC

    def __init__(self, star=9, tier=6, level=200,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.attack.R2, artifact=Artifact.queens_crown.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 191062.2  # should depend on the level
        self.atk = 11944.0  # should depend on the level
        self.armor = 10  # should depend on the level
        self.speed = 973  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Longevity'
        hp_up = 0.3
        if self.star >= 8:
            hp_up = 0.4
        self.hp_up(self, up=hp_up, turns=None,
                   name=name, passive=True)

    def skill(self):
        name = "Nature's Hymn"
        targets_hit = self.targets_hit(self.op_team.get_backline(), name=name)

        hit_power = [self.atk * 0.89] * len(targets_hit)
        heal_power = 1.85
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        if targets_hit:
            for target in self.own_team.heroes:
                self.heal(target, power=heal_power, turns=1, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Healing Heart'
        power = 0.64
        if self.star >= 7:
            power = 0.81
        for target in self.own_team.get_frontline():
            self.heal(target, power=power, turns=1, name=name)
        super().on_attack(target)

    def on_death(self, attacker):
        name = 'Meaning Of Life'
        power = 1.2
        crit_rate_up = 0.11
        if self.star >= 9:
            power = 1.6
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

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.speed.R2, artifact=Artifact.hell_disaster.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 269521.4
        self.atk = 25233.0
        self.armor = 9
        self.speed = 1136
        if self.star == 9:
            self.hp = 155323.2  # should depend on the level
            self.atk = 14530.4  # should depend on the level
            self.armor = 9  # should depend on the level
            self.speed = 971  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Demonisation'
        skill_damage_up = 0.875
        hp_up = 0.35
        speed_up = 50
        if self.star >= 8:
            skill_damage_up = 1.0
            hp_up = 0.4
            speed_up = 60
        self.skill_damage_up(self, up=skill_damage_up, turns=None,
                             name=name, passive=True)
        self.hp_up(self, up=hp_up, turns=None,
                   name=name, passive=True)
        self.speed_up(self, up=speed_up, turns=None,
                      name=name, passive=True)

    def skill(self):
        name = 'Hollow Descent'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        power = [self.atk * 0.54] * len(targets_hit)
        chance = 0.2
        if self.star >= 10:
            power = [self.atk * 0.75] * len(targets_hit)
            chance = 0.3
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            landed = self.try_petrify(target, turns=2, chance=chance, name=name)

            if landed:
                this_name = 'Expand'
                up = 0.35
                if self.star >= 9:
                    up = 0.5
                self.attack_up(self, up=up, turns=4, name=this_name)

        super().skill()

        if self.star >= 10:
            for target in targets_hit:
                drain = 10
                if rd.random() <= 0.3:
                    self.energy_down(target, down=drain, name=name)
                    self.energy_up(self, up=drain, name=name)

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

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.speed.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 413927.0
        self.atk = 21386.7
        self.armor = 13
        self.speed = 1148
        if self.star == 9:
            self.hp = 238557.7  # should depend on the level
            self.atk = 12320.2  # should depend on the level
            self.armor = 13  # should depend on the level
            self.speed = 983  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Faith Ruin'
        damage_to_stunned = 0.75
        if self.star >= 8:
            damage_to_stunned = 0.95
        self.damage_to_stunned_up(self, up=damage_to_stunned, turns=None,
                                  name=name, passive=True)

        name = 'Berserker'
        armor_break_up = 9.6
        attack_up = 0.3
        if self.star >= 9:
            armor_break_up = 12
            attack_up = 0.35
        self.armor_break_up(self, up=armor_break_up, turns=None,
                            name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)

    def skill(self):
        name = 'Wheel Of Torture'
        targets = targets_at_random(self.op_team.heroes, 4)
        targets_hit = self.targets_hit(targets, name=name)

        power = [self.atk * 0.98] * len(targets_hit)
        if self.star >= 10:
            power = [self.atk * 1.2] * len(targets_hit)
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            if target.type == HeroType.ASSASSIN:
                self.try_stun(target, turns=2, chance=0.8, name=name)
                if self.star >= 10:
                    dot_power = 0.4
                    self.poison(target, power=dot_power, turns=3, name=name)
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


class Grand(BaseHero):
    name = HeroName.GRAND
    faction = Faction.ELF
    type = HeroType.WARRIOR

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.evasion.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 427621.5
        self.atk = 17365.0
        self.armor = 12
        self.speed = 1166
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Living Armor'
        hp_up = 0.32
        damage_reduction_up = 0.2
        if self.star >= 8:
            hp_up = 0.44
            damage_reduction_up = 0.26
        self.hp_up(self, up=hp_up, turns=None,
                            name=name, passive=True)
        self.damage_reduction_up(self, up=damage_reduction_up, turns=None,
                       name=name, passive=True)

    def skill(self):
        name = 'Leech Seed'
        targets_hit = self.targets_hit(self.op_team.get_frontline(), name=name)
        min_ally_hp = min([h.hp for h in self.own_team.heroes if not h.is_dead])
        candidates = [h for h in self.own_team.heroes if h.hp == min_ally_hp]
        rd.shuffle(candidates)
        ally_target = candidates[0]

        hit_power = [self.atk * 1.24] * len(targets_hit)
        if self.star >= 10:
            hit_power = [self.atk * 1.8] * len(targets_hit)
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in targets_hit:
            self.armor_down(target, down=7, turns=2, name=name)
            self.armor_up(self, up=7, turns=2, name=name)

        if self.star >= 10 and targets_hit:
            heal_power = 1.5
            self.heal(ally_target, power=heal_power, turns=2, name=name)
        super().skill()

    def on_hit(self, attacker):
        name = "Nature's Power"
        power = self.atk * 1.5
        if self.star >= 9:
            power = self.atk * 2
        self.try_hit_passive(attacker, power=power, chance=0.4, name=name)

        name = 'Eye Of The Jungle'
        down = 0.15
        if self.star >= 7:
            down = 0.24
        self.crit_rate_down(attacker, down=down, turns=2, name=name)
        super().on_hit(attacker)


class Hester(BaseHero):
    name = HeroName.HESTER
    faction = Faction.UNDEAD
    type = HeroType.CLERIC

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.speed.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 304894.0
        self.atk = 26864.1
        self.armor = 8
        self.speed = 1138
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Wish Of Cinderella'
        hit_rate_up = 0.35
        attack_up = 0.35
        if self.star >= 8:
            hit_rate_up = 0.45
            attack_up = 0.45
        self.hit_rate_up(self, up=hit_rate_up, turns=None,
                            name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)

        self.has_triggered = False

    def skill(self):
        name = 'Soul Pulse'
        targets_hit = self.targets_hit(self.op_team.get_backline(), name=name)

        power = [self.atk * 1.63] * len(targets_hit)
        if self.star >= 10:
            power = [self.atk * 2] * len(targets_hit)
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            self.try_petrify(target, turns=2, chance=0.36, name=name)

        if self.star >= 10 and targets_hit:
            up = 0.25
            for target in self.own_team.heroes:
                self.skill_damage_up(target, up=up, turns=3, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Weak Tone'
        down = 0.24
        if self.star >= 7:
            down = 0.3
        self.dodge_down(target, down=down, turns=3, name=name)
        super().on_attack(target)

    def has_taken_damage(self, attacker):
        if self.hp <= self.hp_max * 0.5 and not self.has_triggered:
            self.has_triggered = True
            name = 'Dream Withered'
            up = 0.8
            if self.star >= 9:
                up = 1.0
            self.attack_up(self, up=up, turns=3, name=name)
        super().has_taken_damage(attacker)


class Lexar(BaseHero):
    name = HeroName.LEXAR
    faction = Faction.HORDE
    type = HeroType.WARRIOR

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.armor_break.R2, artifact=Artifact.blood_medal.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 477272.0
        self.atk = 22727.0
        self.armor = 12
        self.speed = 1166
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        self.has_triggered = False

    def skill(self):
        name = 'Blood Axe'
        targets_hit = self.op_team.get_frontline()

        dmg_power = [self.atk * 2.5] * len(targets_hit)
        if self.star >= 10:
            dmg_power = [self.atk * 3] * len(targets_hit)
        self_dmg_power = self.hp * 0.2
        self.hit_skill(targets_hit, power=dmg_power, multi=True, name=name)
        if targets_hit:
            self.hit_ally(self, power=self_dmg_power, name=name)
            if self.star >= 10:
                up = 0.1
                self.attack_up(self, up=up, turns=3, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'War Roar'
        power = 0.8
        if self.star >= 7:
            power = 1.0
        self.heal(self, power=power, turns=1, name=name)
        super().on_attack(target)

    def has_taken_damage(self, attacker):
        name = 'War Frenzy'
        for e in [e for e in self.effects if e.name == 'War Frenzy']:
            e.kill()
        perc = 1 - self.hp / self.hp_max
        attack_up = 1.5
        healing_up = 1.2
        if self.star >= 8:
            attack_up = 2.0
            healing_up = 1.5
        self.attack_up(self, up=attack_up*perc, turns=None, name=name)
        self.healing_up(self, up=healing_up*perc, turns=None, name=name)

        if self.hp <= self.hp_max * 0.5 and not self.has_triggered:
            self.has_triggered = True
            name = 'God Of War'
            crit_rate_up = 0.4
            crit_damage_up = 0.6
            if self.star >= 9:
                crit_rate_up = 0.5
                crit_damage_up = 0.75
            self.crit_rate_up(self, up=crit_rate_up, turns=3, name=name)
            self.crit_damage_up(self, up=crit_damage_up, turns=3, name=name)
            self.cleanse(self, name=name)
        super().has_taken_damage(attacker)

    def has_been_healed(self, source):
        name = 'War Frenzy'
        for e in [e for e in self.effects if e.name == 'War Frenzy']:
            e.kill()
        perc = 1 - self.hp / self.hp_max
        attack_up = 1.5
        healing_up = 1.2
        if self.star >= 8:
            attack_up = 2.0
            healing_up = 1.5
        self.attack_up(self, up=attack_up*perc, turns=None, name=name)
        self.healing_up(self, up=healing_up*perc, turns=None, name=name)
        super().has_been_healed(source)


class Lindberg(BaseHero):
    name = HeroName.LINDBERG
    faction = Faction.HEAVEN
    type = HeroType.ASSASSIN

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.speed.R2, artifact=Artifact.light_pace.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 479836.0
        self.atk = 26223.2
        self.armor = 11
        self.speed = 1177
        if self.star == 9:
            self.hp = 200000.0  # should depend on the level
            self.atk = 14000.0  # should depend on the level
            self.armor = 12  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, rune=rune, artifact=artifact,
                         guild_tech=guild_tech, familiar_stats=familiar_stats, player=player)

        name = 'Cross Shelter'
        speed_up = 35
        attack_up = 0.2
        stun_immune_up = 1.0
        if self.star >= 7:
            speed_up = 40
            attack_up = 0.25
            stun_immune_up = 1.0
        self.speed_up(self, up=speed_up, turns=None,
                          name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                            name=name, passive=True)
        self.stun_immune_up(self, up=stun_immune_up, turns=None,
                            name=name, passive=True)

    def attack(self):
        name = 'attack'
        power = self.atk * 1.2
        if self.star >= 8:
            power = self.atk * 1.4
        min_enemy_hp = min([h.hp for h in self.op_team.heroes if not h.is_dead])
        candidates = [h for h in self.op_team.heroes if h.hp == min_enemy_hp]
        rd.shuffle(candidates)
        target = candidates[0]
        super().attack(target=target, power=power, name=name)

    def skill(self):
        name = 'Throat Blade'
        targets = targets_at_random(self.op_team.get_backline(), 2)
        targets_hit = self.targets_hit(targets, name=name)

        hit_power = [self.atk * 1.8] * len(targets_hit)
        for i, h in enumerate(targets_hit):
            if h.type == HeroType.WANDERER:
                hit_power[i] += self.atk * 0.5
        if self.star >= 10:
            hit_power = [self.atk * 2.3] * len(targets_hit)
            for i, h in enumerate(targets_hit):
                if h.type == HeroType.WANDERER:
                    hit_power[i] += self.atk * 0.7
                if h.hp <= h.hp_max * 0.5:
                    hit_power[i] += self.atk * 1.8
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in targets_hit:
            self.stun(target, turns=2, name=name)
        super().skill()

    def has_taken_damage(self, attacker):
        name = 'Blood Purification'
        for e in [e for e in self.effects if e.name == 'Blood Purification']:
            e.kill()
        perc = 1 - self.hp / self.hp_max
        crit_rate_up = 0.8
        crit_damage_up = 1.5
        if self.star >= 9:
            crit_rate_up = 1.0
            crit_damage_up = 2.0
        self.crit_rate_up(self, up=crit_rate_up*perc, turns=None, name=name)
        self.crit_damage_up(self, up=crit_damage_up*perc, turns=None, name=name)
        super().has_taken_damage(attacker)

    def has_been_healed(self, source):
        name = 'Blood Purification'
        for e in [e for e in self.effects if e.name == 'Blood Purification']:
            e.kill()
        perc = 1 - self.hp / self.hp_max
        crit_rate_up = 0.8
        crit_damage_up = 1.5
        if self.star >= 9:
            crit_rate_up = 1.0
            crit_damage_up = 2.0
        self.crit_rate_up(self, up=crit_rate_up*perc, turns=None, name=name)
        self.crit_damage_up(self, up=crit_damage_up*perc, turns=None, name=name)
        super().has_been_healed(source)


class Luna(BaseHero):
    name = HeroName.LUNA
    faction = Faction.ELF
    type = HeroType.WANDERER

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.speed.R2, artifact=Artifact.tears_of_the_goddess.O6, # because people do it
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 400232.0
        self.atk = 19987.7
        self.armor = 10
        self.speed = 1179
        if self.star == 9:
            self.hp = 208931.4  # should depend on the level
            self.atk = 12837.8  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 1017  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Full Moon Blessing'
        crit_rate_up = 0.3
        crit_damage_up = 0.9
        attack_up = None
        if self.star >= 7:
            crit_rate_up = 0.3
            crit_damage_up = 0.3
            attack_up = 0.3
        self.crit_rate_up(self, up=crit_rate_up, turns=None,
                          name=name, passive=True)
        self.crit_damage_up(self, up=crit_damage_up, turns=None,
                            name=name, passive=True)
        if attack_up is not None:
            self.attack_up(self, up=attack_up, turns=None,
                           name=name, passive=True)

    def attack(self):
        name = 'attack'
        targets = targets_at_random(self.op_team.heroes, 3)
        targets_hit = self.targets_hit(targets, name=name)
        power = [self.atk * 0.7] * len(targets_hit)
        if self.star >= 9:
            power = [self.atk * 0.85] * len(targets_hit)

        self.hit_attack(targets_hit, power, multi=True, name=name)

    def skill(self):
        name = 'Shooting Star'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        power = [self.atk * 0.85] * len(targets_hit)
        if self.star >= 10:
            power = [self.atk * 1.45] * len(targets_hit)
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            self.try_silence(target, turns=2, chance=0.5, name=name)
        if self.star >= 10 and targets_hit:
            up = 0.8
            self.damage_reduction_up(self, up=up, turns=2, name=name)
        super().skill()


class Mars(BaseHero):
    name = HeroName.MARS
    faction = Faction.HEAVEN
    type = HeroType.WANDERER

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.speed.R2, artifact=Artifact.light_pace.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 364684.0
        self.atk = 24066.9
        self.armor = 10
        self.speed = 1156
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                rune=rune, artifact=artifact, guild_tech=guild_tech, familiar_stats=familiar_stats, player=player)

        self.has_revived = False

        name = 'Fury Brand'
        true_damage_up = 0.3
        attack_up = 0.25
        speed_up = 20
        if self.star >= 7:
            true_damage_up = 0.6
            attack_up = 0.3
            speed_up = 40
        self.true_damage_up(self, up=true_damage_up, turns=None,
                   name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                            name=name, passive=True)
        self.speed_up(self, up=speed_up, turns=None,
                            name=name, passive=True)

    def skill(self):
        name = 'Eye Of Thunderstorm'
        n_targets = 3
        if self.star >= 10:
            n_targets = 4
        targets_hit = targets_at_random(self.op_team.heroes, n_targets)

        power = [self.atk * 1.48] * len(targets_hit)
        if self.star >= 10:
            power = [self.atk * 1.7] * len(targets_hit)
        if self.hp <= 0.2 * self.hp_max:
            power = [p + self.atk * 2.0 for p in power]
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        if self.star >= 10:
            for target in targets_hit:
                self.try_stun(target, turns=2, chance=0.6, name=name)

        name = 'Militant'
        up = 0.2
        self.true_damage_up(self, up=up, turns=None, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Militant'
        up = 0.25
        if self.star >= 8:
            up = 0.30
        self.skill_damage_up(self, up=up, turns=None, name=name)
        super().on_attack(target)

    def has_taken_damage(self, attacker):
        if self.hp <= 0 and not self.has_revived:
            self.has_revived = True
            name = 'Miracle Of Resurrection'
            heal_power = (self.hp_max * 0.12 - self.hp) / self.atk
            energy_up = 80
            damage_reduction_up = 0.8
            if self.star >= 9:
                heal_power = (self.hp_max * 0.15 - self.hp) / self.atk
                energy_up = 100
                damage_reduction_up = 0.8
            self.heal(self, power=heal_power, turns=1, name=name)
            self.energy_up(self, up=energy_up, name=name)
            self.damage_reduction_up(self, up=damage_reduction_up, turns=1, name=name)
        super().has_taken_damage(attacker)


class Martin(BaseHero):
    name = HeroName.MARTIN
    faction = Faction.ALLIANCE
    type = HeroType.MAGE

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.armor_break.R2, artifact=Artifact.gospel_song.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 350290.7
        self.atk = 22319.2
        self.armor = 11
        self.speed = 1137
        if self.star == 9:
            self.hp = 200000.0  # should depend on the level
            self.atk = 14000.0  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Ace'
        hp_up = 0.35
        attack_up = 0.15
        skill_damage_up = 0.25
        if self.star >= 9:
            hp_up = 0.4
            attack_up = 0.2
            skill_damage_up = 0.375
        self.hp_up(self, up=hp_up, turns=None,
                   name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                            name=name, passive=True)
        self.skill_damage_up(self, up=skill_damage_up, turns=None,
                            name=name, passive=True)

    def skill(self):
        name = 'Hand Of God'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        power = [self.atk * 0.94] * len(targets_hit)
        if self.star >= 10:
            power = [self.atk * 1.7] * len(targets_hit)
        self.hit_skill(targets_hit, power=power, multi=True, name=name)

        if self.star < 10:
            dot_power = 0.36
            for target in targets_hit:
                self.dot(target, power=dot_power, turns=3, name=name)
        elif targets_hit:
            crit_rate_up = 0.15
            crit_damage_up = 0.5
            self.crit_rate_up(self, up=crit_rate_up, turns=3, name=name)
            self.crit_damage_up(self, up=crit_damage_up, turns=3, name=name)
        super().skill()


class Medusa(BaseHero):
    name = HeroName.MEDUSA
    faction = Faction.HORDE
    type = HeroType.WANDERER

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.vitality.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 347085.0
        self.atk = 22202.7
        self.armor = 10
        self.speed = 1156
        if self.star == 9:
            self.hp = 200043.7  # should depend on the level
            self.atk = 12790.5  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 991  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Eyes Of Chaos'
        attack_up = 0.4
        if self.star >= 8:
            attack_up = 0.5
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)

        name = 'The Curse Of The Goddess'
        damage_to_petrified_up = 0.5
        if self.star >= 9:
            damage_to_petrified_up = 0.6
        self.damage_to_petrified_up(self, up=damage_to_petrified_up, turns=None,
                                   name=name, passive=True)

    def attack(self):
        name = 'attack'
        attack_power = self.atk * 0.75
        n_targets = 2
        if self.star >= 7:
            n_targets = 3
        targets = targets_at_random(self.op_team.heroes, n_targets)
        targets_hit = self.targets_hit(targets, name=name)
        power = [attack_power] * len(targets_hit)

        self.hit_attack(targets_hit, power, multi=True, name=name)
        name = 'The Curse Of The Goddess'
        chance = 0.15
        if self.star >= 9:
            chance = 0.2
        for target in targets_hit:
            self.try_petrify(target, turns=2, chance=chance, name=name)

    def skill(self):
        name = 'Viper Arrow'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        power = [self.atk * 1.02] * len(targets_hit)
        dot_power = self.atk * 0.1
        if self.star >= 10:
            power = [self.atk * 1.4] * len(targets_hit)
            dot_power = 0.15
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            self.bleed(target, power=dot_power, turns=3, name=name)
            self.poison(target, power=dot_power, turns=3, name=name)
        super().skill()


class Megaw(BaseHero):
    name = HeroName.MEGAW
    faction = Faction.ELF
    type = HeroType.CLERIC

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.evasion.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 256759.0
        self.atk = 20104.3
        self.armor = 9
        self.speed = 1113
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        self.has_triggered = False

        name = 'Inner Strength'
        attack_up = 0.3
        crit_rate_up = 0.3
        if self.star >= 7:
            attack_up = 0.4
            crit_rate_up = 0.3
        self.attack_up(self, up=attack_up, turns=None,
                      name=name, passive=True)
        self.crit_rate_up(self, up=crit_rate_up, turns=None,
                       name=name, passive=True)

    def skill(self):
        name = 'Sacred Heal'
        targets_hit = self.op_team.heroes

        hit_power = [self.atk * 0.54] * len(targets_hit)
        heal_power = 0.62
        if self.star >= 10:
            hit_power = [self.atk * 0.8] * len(targets_hit)
            heal_power = 0.8
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        if targets_hit:
            for target in self.own_team.heroes:
                self.heal(target, power=heal_power, turns=3, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Forest Scholar'
        skill_damage_up = 0.24
        if self.star >= 8:
            skill_damage_up = 0.3
        self.skill_damage_up(self, up=skill_damage_up, turns=None, name=name)
        super().on_attack(target)

    def has_taken_damage(self, attacker):
        if self.hp <= self.hp_max * 0.5 and not self.has_triggered:
            self.has_triggered = True
            name = 'Forbidden Tome'
            power = 0.56
            if self.star >= 9:
                power = 0.72
            for target in self.op_team.heroes:
                self.crit_mark(target, power=power, name=name)
        super().has_taken_damage(attacker)


class Minotaur(BaseHero):
    name = HeroName.MINOTAUR
    faction = Faction.HORDE
    type = HeroType.WARRIOR

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.evasion.R2, artifact=Artifact.blood_medal.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 386829.0
        self.atk = 18939.2
        self.armor = 12
        self.speed = 1161
        if self.star == 9:
            self.hp = 222945.4  # should depend on the level
            self.atk = 10909.4  # should depend on the level
            self.armor = 12  # should depend on the level
            self.speed = 996  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Ancestor Totem'
        armor_up = 23
        attack_up = 0.2
        if self.star >= 7:
            armor_up = 25
            attack_up = 0.25
        self.armor_up(self, up=armor_up, turns=None,
                      name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)

        name = 'Warrior Killer'
        damage_to_warriors = 0.45
        if self.star >= 8:
            damage_to_warriors = 0.6
        self.damage_to_warriors_up(self, up=damage_to_warriors, turns=None,
                                   name=name, passive=True)

    def skill(self):
        name = 'Fury Swipes'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        power = [self.atk * 0.9] * len(targets_hit)
        for i, h in enumerate(targets_hit):
            if h.type == HeroType.WARRIOR:
                power[i] += self.atk * 1.2
        if self.star >= 10:
            power = [self.atk * 1.2] * len(targets_hit)
            for i, h in enumerate(targets_hit):
                if h.type == HeroType.WARRIOR:
                    power[i] += self.atk * 1.8
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        if self.star >= 10 and targets_hit:
            up = 0.12
            self.damage_reduction_up(self, up=up, turns=3, name=name)
        super().skill()

    def on_hit(self, attacker):
        name = 'Rebirth'
        power = 0.32
        if self.star >= 9:
            power = 0.4
        self.heal(self, power=power, turns=1, name=name)
        super().on_hit(attacker)


class MonkeyKing(BaseHero):
    name = HeroName.MONKEY_KING
    faction = Faction.HELL
    type = HeroType.WARRIOR

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.armor_break.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 443123.0
        self.atk = 25407.0
        self.armor = 12
        self.speed = 1169
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        self.has_revived = False

    def skill(self):
        name = 'Boundless Strike'
        targets_hit = self.targets_hit(self.op_team.get_backline(), name=name)

        hit_power = [self.atk * 1.08] * len(targets_hit)
        mark_power = 2.64
        if self.star >= 10:
            hit_power = [self.atk * 1.2] * len(targets_hit)
            mark_power = 2.8
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in targets_hit:
            self.timed_mark(target, power=mark_power, turns=2, name=name)
        if self.star >= 10 and targets_hit:
            up = 0.1
            self.damage_reduction_up(self, up=up, turns=2, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Cudgel Mastery'
        chance = 0.3
        power = 0.9
        if self.star >= 7:
            chance = 0.35
            power = 1.2
        self.try_petrify(target, turns=1, chance=chance, name=name)
        self.timed_mark(target, power=power, turns=2, name=name)
        super().on_attack(target)

    def on_hit(self, attacker):
        name = 'Fight Against Buddha'
        power = self.atk * 1.5
        chance = 0.7
        if self.star >= 8:
            power = self.atk * 1.85
            chance = 0.85
        self.try_hit_passive(attacker, power=power, chance=chance, name=name)
        super().on_hit(attacker)

    def has_taken_damage(self, attacker):
        if self.hp <= 0 and not self.has_revived:
            self.has_revived = True
            name = 'Buddha Rebirth'
            power = self.hp_max * 0.9 / self.atk
            if self.star >= 9:
                power = self.hp_max / self.atk
            self.heal(self, power=power, turns=1, name=name)
        super().has_taken_damage(attacker)


class Mulan(BaseHero):
    name = HeroName.MULAN
    faction = Faction.ALLIANCE
    type = HeroType.WANDERER

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.evasion.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 328495.7
        self.atk = 24242.0
        self.armor = 12
        self.speed = 1148
        if self.star == 9:
            self.hp = 189322.1  # should depend on the level
            self.atk = 13966.2  # should depend on the level
            self.armor = 12  # should depend on the level
            self.speed = 983  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Tailwind'
        hp_up = 0.15
        dodge_up = 0.2
        speed_up = 50
        if self.star >= 7:
            hp_up = 0.15
            dodge_up = 0.2
            speed_up = 60
        self.hp_up(self, up=hp_up, turns=None,
                            name=name, passive=True)
        self.dodge_up(self, up=dodge_up, turns=None,
                   name=name, passive=True)
        self.speed_up(self, up=speed_up, turns=None,
                       name=name, passive=True)

    def skill(self):
        name = 'Gale Cut'
        targets = None
        if self.star >= 10:
            targets = targets_at_random(self.op_team.heroes, 4)
        else:
            targets = self.op_team.get_frontline()
        targets_hit = self.targets_hit(targets, name=name)

        hit_power = [self.atk * 1.33] * len(targets_hit)
        up = 0.4
        turns = 2
        if self.star >= 10:
            hit_power = [self.atk * 1.8] * len(targets_hit)
            up = 0.6
            turns = 3
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        if targets_hit:
            self.attack_up(self, up=up, turns=turns, name=name)
        if self.star < 10:
            bleed_power = 0.39
            for target in targets_hit:
                if target.type == HeroType.MAGE:
                    self.bleed(target, power=bleed_power, turns=2, name=name)
        super().skill()

    def attack(self):
        name = 'attack'
        targets = self.op_team.get_frontline()
        targets_hit = self.targets_hit(targets, name=name)
        power = [self.atk * 0.65] * len(targets_hit)
        if self.star >= 9:
            power = [self.atk * 0.72] * len(targets_hit)

        self.hit_attack(targets_hit, power, multi=True, name=name)

    def on_attack(self, target):
        name = 'Illusion'
        attack_up = 0.13
        dodge_up = 0.05
        if self.star >= 8:
            attack_up = 0.16
            dodge_up = 0.06
        self.attack_up(self, up=attack_up, turns=2, name=name)
        self.dodge_up(self, up=dodge_up, turns=2, name=name)
        super().on_attack(target)


class NamelessKing(BaseHero):
    name = HeroName.NAMELESS_KING
    faction = Faction.HEAVEN
    type = HeroType.WARRIOR

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.armor_break.R2, artifact=Artifact.holy_light_justice.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 479836.2
        self.atk = 24358.0
        self.armor = 12
        self.speed = 1171
        if self.star == 9:
            self.hp = 276554.0  # should depend on the level
            self.atk = 14012.8  # should depend on the level
            self.armor = 12  # should depend on the level
            self.speed = 1006  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, 
                rune=rune, artifact=artifact, guild_tech=guild_tech, familiar_stats=familiar_stats, player=player)

        name = 'Heir Of Sunlight'
        hp_up = 0.25
        true_damage_up = 0.3
        crit_rate_up = 0.22
        if self.star >= 7:
            hp_up = 0.3
            true_damage_up = 0.36
            crit_rate_up = 0.24
        self.hp_up(self, up=hp_up, turns=None,
                            name=name, passive=True)
        self.true_damage_up(self, up=true_damage_up, turns=None,
                   name=name, passive=True)
        self.crit_rate_up(self, up=crit_rate_up, turns=None,
                       name=name, passive=True)

    def skill(self):
        name = 'Lightning Storm'
        targets_hit = None
        if self.star >= 10:
            targets_hit = self.op_team.heroes
        else:
            targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        hit_power = [self.atk * 0.84] * len(targets_hit)
        mark_power = 1.2
        if self.star >= 10:
            hit_power = [self.atk * 1.1] * len(targets_hit)
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in targets_hit:
            second_hit = False
            if self.star >= 10:
                second_hit = True
            self.crit_mark(target, power=mark_power, second_hit=second_hit, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Sign Of Sun'
        up = 0.08
        power = 0.53
        if self.star >= 8:
            up = 0.12
            power = 0.6
        self.crit_rate_up(self, up=up, turns=3, name=name)
        self.crit_mark(target, power=power, name=name)
        super().on_attack(target)

    def on_hit(self, attacker):
        name = 'Dragon Sphere'
        up = 0.1
        power = 0.53
        if self.star >= 9:
            up = 0.15
            power = 0.56
        self.crit_damage_up(self, up=up, turns=3, name=name)
        self.crit_mark(attacker, power=power, name=name)
        super().on_hit(attacker)


class Orphee(BaseHero):
    name = HeroName.ORPHEE
    faction = Faction.ELF
    type = HeroType.MAGE

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.vitality.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 220395.3
        self.atk = 31934
        self.armor = 9
        self.speed = 1131
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Highest Answer'
        hp_up = 0.3
        crit_rate_up = 0.35
        if self.star >= 8:
            hp_up = 0.3
            crit_rate_up = 0.45
        self.hp_up(self, up=hp_up, turns=None,
                            name=name, passive=True)
        self.crit_rate_up(self, up=crit_rate_up, turns=None,
                       name=name, passive=True)

    def skill(self):
        name = 'Starstorm'
        targets_hit = self.targets_hit(self.op_team.get_backline(), name=name)

        power = [self.atk * 1.78] * len(targets_hit)
        stun_chance = 0.72
        if self.star >= 10:
            power = [self.atk * 2] * len(targets_hit)
            stun_chance = 0.4
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            if target.type == HeroType.WARRIOR:
                self.try_stun(target, turns=2, chance=stun_chance, name=name)
            elif target.type == HeroType.ASSASSIN and self.star >= 10:
                self.try_silence(target, turns=2, chance=0.4, name=name)
        super().skill()

    def on_attack(self, target):
        name = "Nature's Attendants"
        down = 5.1
        if self.star >= 7:
            down = 7.5
        self.armor_break_down(target, down=down, turns=3, name=name)
        super().on_attack(target)


class Reaper(BaseHero):
    name = HeroName.REAPER
    faction = Faction.UNDEAD
    type = HeroType.MAGE

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.attack.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 304894.6
        self.atk = 25407.6
        self.armor = 8
        self.speed = 1149
        if self.star == 9:
            self.hp = 175732.3  # should depend on the level
            self.atk = 14624.2  # should depend on the level
            self.armor = 8  # should depend on the level
            self.speed = 984  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Necromancy'
        armor_break_up = 9.6
        hp_up = 0.25
        attack_up = 0.25
        if self.star >= 8:
            armor_break_up = 9.6
            hp_up = 0.3
            attack_up = 0.3
        self.armor_break_up(self, up=armor_break_up, turns=None,
                            name=name, passive=True)
        self.hp_up(self, up=hp_up, turns=None,
                   name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)

    def skill(self):
        name = 'Fatal Wave'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        power = [self.atk * 0.84] * len(targets_hit)
        chance = 0.75
        if self.star >= 10:
            power = [self.atk * 1.8] * len(targets_hit)
            chance = 1.0
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            if target.type == HeroType.WARRIOR:
                self.try_silence(target, turns=2, chance=chance, name=name)
        if self.star >= 10 and targets_hit:
            up = 0.2
            self.attack_up(self, up=up, turns=2, name=name)
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

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.speed.R2, artifact=Artifact.tears_of_the_goddess.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 298368.0
        self.atk = 23309.6
        self.armor = 9
        self.speed = 1177
        if self.star == 9:
            self.hp = 179870.0  # should depend on the level
            self.atk = 15141.9  # should depend on the level
            self.armor = 9  # should depend on the level
            self.speed = 1012  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        self.has_triggered = False

        name = 'Killer In Mist'
        armor_break_up = 9.6
        attack_up = 0.3
        if self.star >= 7:
            armor_break_up = 12
            attack_up = 0.35
        self.armor_break_up(self, up=armor_break_up, turns=None,
                            name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)

    def skill(self):
        name = 'Venom Wind'
        targets = targets_at_random(self.op_team.get_backline(), 2)
        targets_hit = None
        if self.star >= 10:
            targets_hit = targets
        else:
            targets_hit = self.targets_hit(targets, name=name)

        hit_power = [self.atk * 1.1] * len(targets_hit)
        dot_power = 0.45
        if self.star >= 10:
            hit_power = [self.atk * 1.5] * len(targets_hit)
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in targets_hit:
            self.dot(target, power=dot_power, turns=5, name=name)
        for target in targets_hit:
            self.try_stun(target, turns=2, chance=0.45, name=name)
        if self.star >= 10 and targets_hit:
            up = 0.4
            self.damage_reduction_up(self, up=up, turns=2, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Poison Dagger'
        power = 0.38
        if self.star >= 8:
            power = 0.48
        self.poison(target, power=power, turns=6, name=name)
        super().on_attack(target)

    def has_taken_damage(self, attacker):
        if self.hp <= self.hp_max * 0.5 and not self.has_triggered:
            self.has_triggered = True
            name = 'Poison Nova'
            power = 0.4
            if self.star >= 9:
                power = 0.5
            targets = targets_at_random(self.op_team.get_backline(), 2)
            for target in targets:
                self.poison(target, power=power, turns=5, name=name)
        super().has_taken_damage(attacker)


class Rlyeh(BaseHero):
    name = HeroName.RLYEH
    faction = Faction.HORDE
    type = HeroType.CLERIC

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.evasion.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 265908.3
        self.atk = 23659.2
        self.armor = 10
        self.speed = 1116
        if self.star == 9:
            self.hp = 153254.1  # should depend on the level
            self.atk = 13636.6  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 951  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = "Old Gods' Protection"
        attack_up = 0.2
        hp_up = 0.15
        if self.star >= 9:
            attack_up = 0.25
            hp_up = 0.2
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)
        self.hp_up(self, up=hp_up, turns=None,
                   name=name, passive=True)

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
            heal_power = 4
            if self.star >= 10:
                dmg_power = self.atk * 1.7

            self.hit_skill(enemy_target, power=dmg_power, name=name)
            self.heal(ally_target, power=heal_power, turns=1, name=name)
            if self.star >= 10:
                up = 0.2
                self.damage_reduction_up(self, up=up, turns=3, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Blood Ceremony'
        power = 1.1
        if self.star >= 7:
            power = 1.5
        if any([not h.is_dead for h in self.own_team.heroes]):
            min_hp = min([h.hp for h in self.own_team.heroes if not h.is_dead])
            candidates = [h for h in self.own_team.heroes if h.hp == min_hp]
            rd.shuffle(candidates)
            target = candidates[0]
            self.try_heal(target, power=power, turns=1, chance=0.5, name=name)
        super().on_attack(target)

    def on_hit(self, attacker):
        name = 'Deep Sea Sacrifice'
        power = 0.5
        if self.star >= 8:
            power = 0.65
        self.heal(self, power=power, turns=1, name=name)
        super().on_hit(attacker)


class Samurai(BaseHero):
    name = HeroName.SAMURAI
    faction = Faction.ALLIANCE
    type = HeroType.ASSASSIN

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.evasion.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 306060.0
        self.atk = 20745.7
        self.armor = 12
        self.speed = 1174
        if self.star == 9:
            self.hp = 200000.0  # should depend on the level
            self.atk = 14000.0  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = "Mind's eye"
        dodge_up = 0.25
        attack_up = 0.3
        if self.star >= 8:
            dodge_up = 0.25
            attack_up = 0.4
        self.dodge_up(self, up=dodge_up, turns=None,
                   name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)

    def attack(self):
        name = 'attack'
        power = self.atk
        if self.star >= 9:
            power = self.atk * 1.2
        min_enemy_hp = min([h.hp for h in self.op_team.heroes if not h.is_dead])
        candidates = [h for h in self.op_team.heroes if h.hp == min_enemy_hp]
        rd.shuffle(candidates)
        target = candidates[0]
        super().attack(target=target, power=power, name=name)

    def skill(self):
        name = 'Kifuu'
        targets = targets_at_random(self.op_team.get_backline(), 2)
        targets_hit = None
        if self.star >= 10:
            targets_hit = self.targets_hit(targets, name=name)
        else:
            targets_hit = targets

        hit_power = [self.atk * 1.52] * len(targets_hit)
        dot_power = 0.86
        turns = 2
        if self.star >= 10:
            hit_power = [self.atk * 1.8] * len(targets_hit)
            dot_power = 1.0
            turns = 3
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in targets_hit:
            self.dot(target, power=dot_power, turns=turns, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Flash'
        power = 0.3
        if self.star >= 7:
            power = 0.38
        self.bleed(target, power=power, turns=2, name=name)
        super().on_attack(target)


class SawMachine(BaseHero):
    name = HeroName.SAW_MACHINE
    faction = Faction.ALLIANCE
    type = HeroType.MAGE

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.speed.R2, artifact=Artifact.tears_of_the_goddess.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 360780.0
        self.atk = 20279.0
        self.armor = 13
        self.speed = 1149
        if star == 9:
            self.hp = 207944.3  # should depend on the level
            self.atk = 11661.9  # should depend on the level
            self.armor = 13  # should depend on the level
            self.speed = 984  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Destruction Mode'
        hp_up = 0.2
        skill_damage_up = 0.75
        if self.star >= 8:
            hp_up = 0.3
            skill_damage_up = 0.95
        self.hp_up(self, up=hp_up, turns=None,
                   name=name, passive=True)
        self.skill_damage_up(self, up=skill_damage_up, turns=None,
                             name=name, passive=True)

    def skill(self):
        name = 'Whirlwind Of Death'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        power = [self.atk * 1.15] * len(targets_hit)
        chance = 0.75
        if self.star >= 10:
            power = [self.atk * 1.3] * len(targets_hit)
            for i, h in enumerate(targets_hit):
                if h.type == HeroType.CLERIC:
                    power[i] += self.atk * 0.8
            chance = 1.0
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            if target.type == HeroType.CLERIC:
                self.try_silence(target, turns=3, chance=chance, name=name)
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
            up = 0.25
        self.try_crit_rate_down(target, down=down, turns=3, chance=0.8, name=name)
        self.try_attack_up(self, up=up, turns=3, chance=0.8, name=name)
        super().on_attack(target)


class Scarlet(BaseHero):
    name = HeroName.SCARLET
    faction = Faction.HORDE
    type = HeroType.MAGE

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.attack.R2, artifact=Artifact.tears_of_the_goddess.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 263636.0
        self.atk = 28671
        self.armor = 9
        self.speed = 1149
        if self.star == 9:
            self.hp = 151937.2  # should depend on the level
            self.atk = 16505.5  # should depend on the level
            self.armor = 9  # should depend on the level
            self.speed = 984  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

    def skill(self):
        name = 'Poison Nova'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)
        hit_power = [self.atk * 0.42] * len(targets_hit)
        dot_power = 0.6
        if self.star >= 10:
            hit_power = [self.atk * 0.6] * len(targets_hit)
            dot_power = 0.9
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in targets_hit:
            if self.star >= 10:
                self.poison(target, power=dot_power, turns=3, name=name)
            else:
                self.dot(target, power=dot_power, turns=3, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Poison Touch'
        power = 0.7
        if self.star >= 7:
            power = 0.8
        self.try_poison(target, power=power, turns=2, chance=0.8, name=name)
        super().on_attack(target)

    def on_hit(self, attacker):
        name = 'Corrosive Skin'
        power = 0.54
        if self.star >= 9:
            power = 0.62
        self.try_poison(attacker, power=power, turns=3, chance=0.6, name=name)
        super().on_hit(attacker)

    def on_death(self, attacker):
        name = 'Malefic'
        power = 0.63
        if self.star >= 8:
            power = 0.85
        for h in self.op_team.heroes:
            self.poison(h, power=power, turns=3, name=name)
        super().on_death(attacker)


class ShuddeMell(BaseHero):
    name = HeroName.SHUDDE_M_ELL
    faction = Faction.UNDEAD
    type = HeroType.CLERIC

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.attack.R2, artifact=Artifact.siren_heart.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 338052.8
        self.atk = 24358.3
        self.armor = 11
        self.speed = 1148
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Psychic Blast'
        hp_up = 0.22
        attack_up = 0.15
        if self.star >= 7:
            hp_up = 0.25
            attack_up = 0.2
        self.hp_up(self, up=hp_up, turns=None,
                   name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)

    def attack(self):
        name = 'attack'
        attack_power = self.atk * 0.7
        n_targets = 3
        chance = 0.4
        if self.star >= 8:
            n_targets = 4
            chance = 0.5
        targets = targets_at_random(self.op_team.heroes, n_targets)
        targets_hit = self.targets_hit(targets, name=name)
        power = [attack_power] * len(targets_hit)

        self.hit_attack(targets_hit, power, multi=True, name=name)
        for target in targets_hit:
            name = 'Dominoll'
            self.try_silence(target, turns=2, chance=chance, name=name)

    def skill(self):
        name = 'Tentacle Attack'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)
        hit_power = [self.atk * 0.8] * len(targets_hit)
        heal_power = 1.2
        if self.star >= 10:
            hit_power = [self.atk] * len(targets_hit)
            heal_power = 1.0
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        if targets_hit:
            heal_targets = None
            if self.star >= 10:
                heal_targets = self.own_team.heroes
            else:
                heal_targets = targets_at_random(self.own_team.heroes, 4)
            for target in heal_targets:
                self.heal(target, power=heal_power, turns=4, name=name)
        super().skill()

    def on_hit(self, attacker):
        name = 'Creation'
        chance = 0.4
        up = 30
        if self.star >= 9:
            chance = 0.6
            up = 40
        if rd.random() <= chance:
            self.energy_up(self, up=up, name=name)
        super().on_hit(attacker)


class Tesla(BaseHero):
    name = HeroName.TESLA
    faction = Faction.ALLIANCE
    type = HeroType.MAGE

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.speed.R2, artifact=Artifact.ancient_vows.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 260663.7
        self.atk = 25407.2
        self.armor = 11
        self.speed = 1147
        if self.star == 9:
            self.hp = 200000.0  # should depend on the level
            self.atk = 14000.0  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Static Intensify'
        attack_up = 0.2
        hp_up = 0.3
        if self.star >= 7:
            attack_up = 0.25
            hp_up = 0.35
        self.attack_up(self, up=attack_up, turns=None,
                   name=name, passive=True)
        self.hp_up(self, up=hp_up, turns=None,
                       name=name, passive=True)

    def skill(self):
        name = 'Plasma Field'
        targets = targets_at_random(self.op_team.heroes, 4)
        targets_hit = self.targets_hit(targets, name=name)

        power = [self.atk * 1.2] * len(targets_hit)
        chance = 0.3
        if self.star >= 10:
            power = [self.atk * 1.4] * len(targets_hit)
            chance = 0.5
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            self.try_stun(target, turns=2, chance=chance, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Flux'
        chance = 0.27
        if self.star >= 9:
            chance = 0.4
        self.try_stun(target, turns=2, chance=chance, name=name)
        super().on_attack(target)

    def on_death(self, attacker):
        name = 'Static Storm'
        chance = 0.34
        if self.star >= 8:
            chance = 0.43
        for target in self.op_team.get_backline():
            self.try_stun(target, turns=2, chance=chance, name=name)
        super().on_death(attacker)


class TigerKing(BaseHero):
    name = HeroName.TIGER_KING
    faction = Faction.ELF
    type = HeroType.WARRIOR

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.evasion.R2, artifact=Artifact.star_pray.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 452155.7
        self.atk = 15093.0
        self.armor = 12
        self.speed = 1165
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'King Of Beasts'
        hp_up = 0.3
        armor_up = 11
        if self.star >= 7:
            hp_up = 0.4
            armor_up = 14
        self.hp_up(self, up=hp_up, turns=None,
                   name=name, passive=True)
        self.armor_up(self, up=armor_up, turns=None,
                       name=name, passive=True)

    def skill(self):
        name = 'Tiger Attack'
        targets_hit = self.targets_hit(self.op_team.heroes, name=name)

        power = [self.atk * 0.87] * len(targets_hit)
        dot_power = 0.4
        if self.star >= 10:
            power = [self.atk * 1.6] * len(targets_hit)
            dot_power = 0.8
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            self.dot(target, power=dot_power, turns=3, name=name)
        if self.star >= 10 and targets_hit:
            attack_up = 0.1
            crit_rate_up = 0.1
            self.attack_up(self, up=attack_up, turns=3, name=name)
            self.crit_rate_up(self, up=crit_rate_up, turns=3, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Shield Breaker'
        down = 3.9
        dot_power = 0.26
        if self.star >= 9:
            down = 4.5
            dot_power = 0.32
        self.armor_break_down(target, down=down, turns=6, name=name)
        self.dot(target, power=dot_power, turns=6, name=name)
        super().on_attack(target)


class Ultima(BaseHero):
    name = HeroName.ULTIMA
    faction = Faction.ALLIANCE
    type = HeroType.CLERIC

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.evasion.R2, artifact=Artifact.ancient_vows.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 364975.7
        self.atk = 22144.0
        self.armor = 12
        self.speed = 1116
        if self.star == 9:
            self.hp = 210342.6  # should depend on the level
            self.atk = 12743.7  # should depend on the level
            self.armor = 12  # should depend on the level
            self.speed = 951  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        self.has_triggered = False

        name = 'Essential Dignity'
        hp_up = 0.3
        speed_up = 30
        if self.star >= 7:
            hp_up = 0.4
            speed_up = 50
        self.hp_up(self, up=hp_up, turns=None,
                   name=name, passive=True)
        self.speed_up(self, up=speed_up, turns=None,
                      name=name, passive=True)

    def attack(self):
        name = 'attack'
        targets = targets_at_random(self.op_team.heroes, 3)
        targets_hit = self.targets_hit(targets, name=name)
        power = [self.atk * 0.7] * len(targets_hit)
        if self.star >= 8:
            power = [self.atk * 0.8] * len(targets_hit)

        self.hit_attack(targets_hit, power, multi=True, name=name)

    def skill(self):
        name = 'Stellar Detonation'
        targets_hit = self.targets_hit(self.op_team.get_backline(), name=name)

        speed_up = 30
        hit_power = [self.atk * 1.08] * len(targets_hit)
        if self.star >= 10:
            hit_power = [self.atk * 1.2] * len(targets_hit)
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        if targets_hit:
            for target in self.own_team.get_backline():
                self.speed_up(target, up=speed_up, turns=2, name=name)
                if self.star >= 10:
                    attack_up = 0.2
                    self.attack_up(target, up=attack_up, turns=2, name=name)
        super().skill()

    def has_taken_damage(self, attacker):
        if self.hp <= self.hp_max * 0.5 and not self.has_triggered:
            self.has_triggered = True
            name = 'Celestial Opposition'
            attack_up = 0.22
            armor_down = 7
            if self.star >= 9:
                attack_up = 0.29
                armor_down = 9
            for target in self.own_team.heroes:
                self.attack_up(target, up=attack_up, turns=3, name=name)
            for target in self.op_team.heroes:
                self.armor_down(target, down=armor_down, turns=3, name=name)
        super().has_taken_damage(attacker)


class Valkyrie(BaseHero):
    name = HeroName.VALKYRIE
    faction = Faction.ALLIANCE
    type = HeroType.WARRIOR

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.attack.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 477680.0
        self.atk = 23310.0
        self.armor = 12
        self.speed = 1159
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Galloping Battlefield'
        hp_up = 0.15
        armor_up = 6
        attack_up = 0.15
        if self.star >= 7:
            hp_up = 0.3
            armor_up = 7
            attack_up = 0.3
        self.hp_up(self, up=hp_up, turns=None,
                            name=name, passive=True)
        self.armor_up(self, up=armor_up, turns=None,
                       name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)

    def attack(self):
        name = 'attack'
        power = self.atk * 1.3
        if self.star >= 8:
            power = self.atk * 1.5
        super().attack(power=power, name=name)

    def skill(self):
        name = 'Gungnir'
        targets_hit = self.op_team.heroes
        hit_power = [self.atk * 1.2] * len(targets_hit)
        dot_power = 0.3
        if self.star >= 10:
            hit_power = [self.atk * 1.4] * len(targets_hit)
            dot_power = 0.5
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for target in targets_hit:
            self.dot(target, power=dot_power, turns=5, name=name)
            if self.star >= 10:
                if not target.is_dead:
                    for e in target.effects:
                        if e.name == 'Gungnir' and e.source.str_id == self.str_id \
                                            and isinstance(e, Effect.attack_down):
                            e.kill()
                self.attack_down(target, down=0.2, turns=3, name=name)
            
        super().skill()

    def on_attack(self, target):
        name = 'Ruens Magic'
        drain = 0.15
        if self.star >= 8:
            drain = 0.2
        self.skill_damage_down(target, down=drain, turns=None, name=name)
        self.skill_damage_up(self, up=drain, turns=None, name=name)
        super().on_attack(target)


class Vegvisir(BaseHero):
    name = HeroName.VEGVISIR
    faction = Faction.ELF
    type = HeroType.WARRIOR

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.evasion.R2, artifact=Artifact.star_pray.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 410372.0
        self.atk = 16491.0
        self.armor = 12
        self.speed = 1167
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        self.has_triggered = False

    def skill(self):
        name = 'Bipolar Reversal'
        n_targets = 3
        chance = 0.36
        if self.star >= 10:
            n_targets = 4
            chance = 0.48
        targets_hit = targets_at_random(self.op_team.heroes, n_targets)
        hit_power = [self.atk * 1.58] * len(targets_hit)
        crits = self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        for i, target in enumerate(targets_hit):
            if crits[i]:
                self.try_freeze(target, turns=2, chance=chance, name=name)
        super().skill()

    def on_hit(self, attacker):
        name = 'Glacier Echo'
        crit_rate_up = 0.07
        heal_power = 0.3
        if self.star >= 7:
            crit_rate_up = 0.1
            heal_power = 0.4
        self.crit_rate_up(self, up=crit_rate_up, turns=3, name=name)
        self.heal(self, power=heal_power, turns=1, name=name)
        super().on_hit(attacker)

    def has_taken_damage(self, attacker):
        if self.hp <= self.hp_max * 0.5 and not self.has_triggered:
            self.has_triggered = True
            name = 'Willpower Awakening'
            atk_up = 0.6
            crit_rate_up = 0.3
            heal_power = 2.4
            if self.star >= 9:
                atk_up = 0.8
                crit_rate_up = 0.4
                heal_power = 4
            self.attack_up(self, up=atk_up, turns=3, name=name)
            self.crit_rate_up(self, up=crit_rate_up, turns=3, name=name)
            self.heal(self, power=heal_power, turns=3, name=name)
        super().has_taken_damage(attacker)


class Verthandi(BaseHero):
    name = HeroName.VERTHANDI
    faction = Faction.HEAVEN
    type = HeroType.CLERIC

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.speed.R2, artifact=Artifact.gift_of_creation.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 418472.0
        self.atk = 22960.0
        self.armor = 12
        self.speed = 1138
        if self.star == 9:
            self.hp = 241190.8  # should depend on the level
            self.atk = 13213.7  # should depend on the level
            self.armor = 12  # should depend on the level
            self.speed = 973  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant, rune=rune, artifact=artifact,
                         guild_tech=guild_tech, familiar_stats=familiar_stats, player=player)

        name = 'Fate Drama'
        true_damage_up = 0.48
        attack_up = 0.4
        if self.star >= 8:
            true_damage_up = 0.54
            attack_up = 0.45
        self.true_damage_up(self, up=true_damage_up, turns=None,
                            name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)

    def skill(self):
        name = 'Goddess Benison'
        targets_hit = None
        if self.star >= 10:
            targets_hit = self.op_team.heroes
        else:
            targets_hit = self.targets_hit(self.op_team.heroes, name=name)
        hit_power = [self.atk * 0.69] * len(targets_hit)
        heal_power = 1.3
        if self.star >= 10:
            hit_power = [self.atk * 1.2] * len(targets_hit)
            heal_power = 1.5
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        if targets_hit:
            for target in self.own_team.heroes:
                self.heal(target, power=heal_power, turns=1, name=name)
            if self.star >= 10:
                for target in self.own_team.heroes:
                    up = 0.2
                    self.true_damage_up(target, up=up, turns=3, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Hallowed Pray'
        power = 0.7
        if self.star >= 7:
            power = 1.15
        self.heal(self, power=power, turns=1, name=name)
        super().on_attack(target)

    def on_hit(self, attacker):
        name = 'Inviolability'
        power = self.atk * 1.8
        if self.star >= 9:
            power = self.atk * 2.1
        self.try_hit_passive(attacker, power=power, chance=0.35, name=name)
        super().on_hit(attacker)


class Vivienne(BaseHero):
    name = HeroName.VIVIENNE
    faction = Faction.ALLIANCE
    type = HeroType.CLERIC

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.accuracy.R2, artifact=Artifact.gospel_song.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 327505.2
        self.atk = 21561.6
        self.armor = 12
        self.speed = 1116
        if self.star == 9:
            self.hp = 166421.3  # should depend on the level
            self.atk = 12696.7  # should depend on the level
            self.armor = 12  # should depend on the level
            self.speed = 948  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        self.has_triggered = False

        name = 'Innocent Heart'
        hp_up = 0.3
        attack_up = 0.2
        if self.star >= 8:
            hp_up = 0.35
            attack_up = 0.25
        self.hp_up(self, up=hp_up, turns=None,
                            name=name, passive=True)
        self.attack_up(self, up=attack_up, turns=None,
                       name=name, passive=True)

    def attack(self):
        power = self.atk * 0.4
        if self.star >= 7:
            power = self.atk * 0.5
        super().attack(power=power)

    def skill(self):
        name = 'Cleric Shine'
        targets = targets_at_random(self.op_team.get_backline(), 2)
        targets_hit = self.targets_hit(targets, name=name)
        hit_power = [self.atk * 0.88] * len(targets_hit)
        heal_power = 0.8
        if self.star >= 10:
            heal_power = 1.1
        self.hit_skill(targets_hit, power=hit_power, multi=True, name=name)
        if targets_hit:
            for target in self.own_team.heroes:
                self.heal(target, power=heal_power, turns=3, name=name)
            if self.star >= 10 and rd.random() <= 0.5:
                this_heal_power = 1.0
                for target in self.own_team.heroes:
                    self.heal(target, power=this_heal_power, turns=1, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Largesse'
        power = 0.35
        if self.star >= 7:
            power = 0.5
        if not self.game.is_finished():
            target = targets_at_random(self.own_team.heroes, 1)[0]
            self.heal(target, power=power, turns=3, name=name)
        super().on_attack(target)

    def has_taken_damage(self, attacker):
        if self.hp <= self.hp_max * 0.3 and not self.has_triggered:
            self.has_triggered = True
            name = 'Brave Song'
            power = 0.95
            if self.star >= 9:
                power = 1.35
            for target in self.own_team.heroes:
                self.heal(target, power=power, turns=1, name=name)
        super().has_taken_damage(attacker)


class Werewolf(BaseHero):
    name = HeroName.WEREWOLF
    faction = Faction.ELF
    type = HeroType.ASSASSIN

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.speed.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 307167.0
        self.atk = 22202.4
        self.armor = 10
        self.speed = 1174
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'War Wolf Roar'
        attack_up = 0.2
        hit_rate_up = 0.15
        if self.star >= 8:
            attack_up = 0.25
            hit_rate_up = 0.2
        self.attack_up(self, up=attack_up, turns=None,
                            name=name, passive=True)
        self.hit_rate_up(self, up=hit_rate_up, turns=None,
                       name=name, passive=True)

    def attack(self):
        name = 'attack'
        power = self.atk * 1.1
        if self.star >= 9:
            power = self.atk * 1.5
        target = targets_at_random(self.op_team.get_backline(), 1)[0]
        super().attack(target=target, power=power, name=name)

    def skill(self):
        name = 'Cutting Wolf Claw'
        min_enemy_hp = min([h.hp for h in self.op_team.heroes if not h.is_dead])
        enemy_candidates = [h for h in self.op_team.heroes if h.hp == min_enemy_hp]
        rd.shuffle(enemy_candidates)
        target = enemy_candidates[0]
        dodged = self.compute_dodge(target, name=name)
        if not dodged:
            dmg_power = self.atk * 2.16
            dot_power = 0.83
            if self.star >= 10:
                dmg_power = self.atk * 2.4
                dot_power = 1.0
            self.hit_skill(target, power=dmg_power, name=name)
            if target.type == HeroType.MAGE:
                self.dot(target, power=dot_power, turns=2, name=name)
        super().skill()

    def on_attack(self, target):
        name = 'Fighting Spirit'
        skill_damage_up = 0.3
        drain = 40
        if self.star >= 7:
            skill_damage_up = 0.4
            drain = 50
        self.energy_down(target, down=drain, name=name)
        self.energy_up(self, up=drain, name=name)
        self.skill_damage_up(self, up=skill_damage_up, turns=None, name=name)
        super().on_attack(target)


class WolfRider(BaseHero):
    name = HeroName.WOLF_RIDER
    faction = Faction.HORDE
    type = HeroType.WARRIOR

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.evasion.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 265034.3
        self.atk = 25407
        self.armor = 10
        self.speed = 1167
        if self.star == 9:
            self.hp = 200000.0  # should depend on the level
            self.atk = 14000.0  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        self.has_triggered = False

        name = 'War Wolf Roar'
        armor_up = 10
        hp_up = 0.3
        if self.star >= 7:
            armor_up = 12
            hp_up = 0.4
        self.armor_up(self, up=armor_up, turns=None,
                            name=name, passive=True)
        self.hp_up(self, up=hp_up, turns=None,
                       name=name, passive=True)

    def skill(self):
        name = 'Wolf Claw Sunder'
        targets_hit = self.targets_hit(self.op_team.get_backline(), name=name)

        power = [self.atk * 1.08] * len(targets_hit)
        chance = 0.34
        if self.star >= 10:
            power = [self.atk * 1.5] * len(targets_hit)
            chance = 0.48
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        for target in targets_hit:
            self.try_stun(target, turns=2, chance=chance, name=name)
        super().skill()

    def on_death(self, attacker):
        for h in self.own_team.heroes:
            for e in [e for e in h.effects if e.name == 'Attack Command' and e.source.str_id == self.str_id]:
                e.kill()
        super().on_death(attacker)

    def has_taken_damage(self, attacker):
        if self.hp <= self.hp_max * 0.5 and not self.has_triggered:
            self.has_triggered = True
            name = 'Bloody Ascent'
            up = 0.35
            if self.star >= 9:
                up = 0.45
            self.damage_reduction_up(self, up=up, turns=3, name=name)
        super().has_taken_damage(attacker)


class Wolnir(BaseHero):
    name = HeroName.WOLNIR
    faction = Faction.UNDEAD
    type = HeroType.WARRIOR

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.evasion.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 480069.9
        self.atk = 16899.0
        self.armor = 9
        self.speed = 1165
        if self.star == 9:
            self.hp = 200000.0  # should depend on the level
            self.atk = 14000.0  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Desperate Struggle'
        hp_up = 0.3
        hit_rate_up = 0.2
        if self.star >= 7:
            hp_up = 0.4
            hit_rate_up = 0.2
        self.hp_up(self, up=hp_up, turns=None,
                            name=name, passive=True)
        self.hit_rate_up(self, up=hit_rate_up, turns=None,
                       name=name, passive=True)

    def skill(self):
        name = 'Power Of Hades'
        targets_hit = self.targets_hit(self.op_team.get_backline(), name=name)

        power = [self.atk * 1.14] * len(targets_hit)
        heal_power = 0.95
        if self.star >= 10:
            power = [self.atk * 1.6] * len(targets_hit)
            heal_power = 2.0
        self.hit_skill(targets_hit, power=power, multi=True, name=name)
        if self.star >= 10:
            for target in targets_hit:
                self.try_freeze(target, turns=2, chance=0.3, name=name)
        if targets_hit:
            self.heal(self, power=heal_power, turns=1, name=name)
        super().skill() 

    def on_attack(self, target):
        name = 'Bloodthirst'
        power = 0.36
        if self.star >= 9:
            power = 0.48
        self.heal(self, power=power, turns=1, name=name)
        super().on_attack(target)


class Xexanoth(BaseHero):
    name = HeroName.XEXANOTH
    faction = Faction.HELL
    type = HeroType.ASSASSIN

    def __init__(self, star=10, tier=6, level=250,
                 armor=Armor.O3, helmet=Helmet.O3, weapon=Weapon.O3, pendant=Pendant.O3,
                 rune=Rune.speed.R2, artifact=Artifact.bone_grip.O6,
                 guild_tech=guild_tech_maxed,
                 familiar_stats=default_familiar_stats, player=True):
        if level < 200 or tier < 6:
            raise NotImplementedError

        self.star = star
        self.tier = tier
        self.level = level
        self.hp = 443123.1
        self.atk = 26223.0
        self.armor = 11
        self.speed = 1177
        if self.star == 9:
            self.hp = 200000  # should depend on the level
            self.atk = 14000  # should depend on the level
            self.armor = 10  # should depend on the level
            self.speed = 985  # should depend on the level
        super().__init__(armor=armor, helmet=helmet, weapon=weapon, pendant=pendant,
                         rune=rune, artifact=artifact, guild_tech=guild_tech,
                         familiar_stats=familiar_stats, player=player)

        name = 'Rebellion'
        silence_immune_up = 1.0
        self.silence_immune_up(self, up=silence_immune_up, turns=None,
                               name=name, passive=True)

        name = 'Weak Point Stealing'
        speed_up = 35
        if self.star >= 8:
            speed_up = 40
        self.speed_up(self, up=speed_up, turns=None,
                            name=name, passive=True)

        name = 'Death Focus'
        hp_up = 0.25
        skill_damage_up = 0.4
        if self.star >= 9:
            hp_up = 0.3
            skill_damage_up = 0.5
        self.hp_up(self, up=hp_up, turns=None,
                            name=name, passive=True)
        self.skill_damage_up(self, up=skill_damage_up, turns=None,
                            name=name, passive=True)

    def attack(self):
        name = 'attack'
        attack_power = self.atk * 0.9
        if self.star >= 7:
            attack_power = self.atk * 1.1
        targets = targets_at_random(self.op_team.heroes, 2)
        targets_hit = self.targets_hit(targets, name=name)
        power = [attack_power] * len(targets_hit)

        self.hit_attack(targets_hit, power, multi=True, name=name)
        for target in targets_hit:
            name = 'Rebellion'
            self.try_silence(target, turns=2, chance=0.6, name=name)

    def skill(self):
        name = 'Betrayal Provocation'
        target = targets_at_random(self.op_team.get_frontline(), 1)[0]
        dodged = self.compute_dodge(target, name=name)
        if not dodged:
            dmg_power = self.atk * 2.5
            armor_down = 5
            if self.star >= 10:
                dmg_power = self.atk * 3
                extra_power = min(target.hp_max * 0.25, self.atk * 4)
                dmg_power += extra_power
                armor_down = 7
            self.hit_skill(target, power=dmg_power, name=name)
            self.armor_down(target, down=armor_down, turns=2, name=name)
        super().skill()

    def on_hit(self, attacker):
        name = 'Weak Point Stealing'
        drain = 8
        if self.star >= 8:
            drain = 10
        self.energy_down(attacker, down=drain, name=name)
        self.energy_up(self, up=drain, name=name)
        super().on_hit(attacker)


@dataclass
class Hero:
    empty = EmptyHero
    abyss_lord = AbyssLord
    aden = Aden
    blood_tooth = BloodTooth
    centaur = Centaur
    chessia = Chessia
    drow = Drow
    dziewona = Dziewona
    forest_healer = ForestHealer
    freya = Freya
    gerald = Gerald
    grand = Grand
    hester = Hester
    lexar = Lexar
    lindberg = Lindberg
    luna = Luna
    mars = Mars
    martin = Martin
    medusa = Medusa
    megaw = Megaw
    minotaur = Minotaur
    monkey_king = MonkeyKing
    mulan = Mulan
    nameless_king = NamelessKing
    orphee = Orphee
    reaper = Reaper
    ripper = Ripper
    rlyeh = Rlyeh
    samurai = Samurai
    saw_machine = SawMachine
    scarlet = Scarlet
    shudde_m_ell = ShuddeMell
    tesla = Tesla
    tiger_king = TigerKing
    ultima = Ultima
    valkyrie = Valkyrie
    vegvisir = Vegvisir
    verthandi = Verthandi
    vivienne = Vivienne
    werewolf = Werewolf
    wolf_rider = WolfRider
    wolnir = Wolnir
    xexanoth = Xexanoth


hero_from_request = {
    'EMPTY': Hero.empty,
    'ABYSS_LORD': Hero.abyss_lord,
    'ADEN': Hero.aden,
    'BLOOD_TOOTH': Hero.blood_tooth,
    'CENTAUR': Hero.centaur,
    'CHESSIA': Hero.chessia,
    'DROW': Hero.drow,
    'DZIEWONA': Hero.dziewona,
    'FOREST_HEALER': Hero.forest_healer,
    'FREYA': Hero.freya,
    'GERALD': Hero.gerald,
    'GRAND': Hero.grand,
    'HESTER': Hero.hester,
    'LEXAR': Hero.lexar,
    'LINDBERG': Hero.lindberg,
    'LUNA': Hero.luna,
    'MARS': Hero.mars,
    'MARTIN': Hero.martin,
    'MEDUSA': Hero.medusa,
    'MEGAW': Hero.megaw,
    'MINOTAUR': Hero.minotaur,
    'MONKEY_KING': Hero.monkey_king,
    'MULAN': Hero.mulan,
    'NAMELESS_KING': Hero.nameless_king,
    'ORPHEE': Hero.orphee,
    'REAPER': Hero.reaper,
    'RIPPER': Hero.ripper,
    'RLYEH': Hero.rlyeh,
    'SAMURAI': Hero.samurai,
    'SAW_MACHINE': Hero.saw_machine,
    'SCARLET': Hero.scarlet,
    'SHUDDE_M_ELL': Hero.shudde_m_ell,
    'TESLA': Hero.tesla,
    'TIGER_KING': Hero.tiger_king,
    'ULTIMA': Hero.ultima,
    'VALKYRIE': Hero.valkyrie,
    'VEGVISIR': Hero.vegvisir,
    'VERTHANDI': Hero.verthandi,
    'VIVIENNE': Hero.vivienne,
    'WEREWOLF': Hero.werewolf,
    'WOLF_RIDER': Hero.wolf_rider,
    'WOLNIR': Hero.wolnir,
    'XEXANOTH': Hero.xexanoth
}


## Team
class Team:
    def __init__(self, heroes, pet=default_familiar, cancel_aura=False):
        if len(heroes) != 6:
            raise Warning('Teams must contain 6 heroes')

        self.heroes = heroes
        self.pet = copy.copy(pet)
        for i, h in enumerate(self.heroes):
            h.pos = i

        if not cancel_aura:
            self.aura = Aura(heroes)  # aura
            self.compute_aura()

        self.compute_pet(pet)  # familiar

        for h in self.heroes:
            if isinstance(h, Vegvisir):
                name = 'Eternal North'
                hp_up = 0.4
                crit_damage_up = 0.2
                crit_rate_up = 0.2
                if h.star >= 8:
                    hp_up = 0.6
                    crit_damage_up = 0.3
                    crit_rate_up = 0.3
                if h.pos <= 2:
                    h.hp_up(h, up=hp_up, turns=None,
                            name=name, passive=True)
                else:
                    h.crit_damage_up(h, up=crit_damage_up, turns=None,
                                     name=name, passive=True)
                    h.crit_rate_up(h, up=crit_rate_up, turns=None,
                                   name=name, passive=True)

        for h in self.heroes:
            if isinstance(h, WolfRider):
                name = 'Attack Command'
                up = 0.2
                if h.star >= 8:
                    up = 0.3
                for h2 in self.heroes:
                    h.damage_to_stunned_up(h2, up=up, turns=None,
                                        name=name, passive=True)

        for h in self.heroes:
            h.hp_max = h.hp
            h.own_team = self
        self.pet.own_team = self

    def compute_aura(self):
        for h in self.heroes:
            h.atk *= (1 + self.aura.atk_bonus)
            h.hp *= (1 + self.aura.hp_bonus)
            h.dodge += self.aura.dodge
            h.crit_rate += self.aura.crit_rate
            h.control_immune += self.aura.control_immune
            h.armor_break += self.aura.armor_break

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

    def comp(self):
        teams_str = ''
        len_max_1 = max([len(self.heroes[i].str_id) for i in (0, 3)])
        len_max_2 = max([len(self.heroes[i].str_id) for i in (1, 4)])
        len_max_3 = max([len(self.heroes[i].str_id) for i in (2, 5)])
        teams_str += '\nBackline  : '
        teams_str += '[{}{}, {}{}, {}{}]' \
            .format(self.heroes[3].str_id,
                    ' ' * (len_max_1 - len(self.heroes[3].str_id)),
                    self.heroes[4].str_id,
                    ' ' * (len_max_2 - len(self.heroes[4].str_id)),
                    self.heroes[5].str_id,
                    ' ' * (len_max_3 - len(self.heroes[5].str_id)))
        teams_str += '\nFrontline : '
        teams_str += '[{}{}, {}{}, {}{}]' \
            .format(self.heroes[0].str_id,
                    ' ' * (len_max_1 - len(self.heroes[0].str_id)),
                    self.heroes[1].str_id,
                    ' ' * (len_max_2 - len(self.heroes[1].str_id)),
                    self.heroes[2].str_id,
                    ' ' * (len_max_3 - len(self.heroes[2].str_id)))

        return teams_str


def make_boss_heroes(heroes, neutral=True, multiplier=0.0, speed=0):
    for h in heroes:
        h.hp *= 100
        h.atk *= multiplier
        h.speed += speed
        if neutral:
            h.faction = Faction.EMPTY
            h.type = HeroType.EMPTY


def dummy_friend(neutral=True):
    heroes = []
    for i in range(1, 7):
        if i == 2:
            heroes.append(Hero.centaur(star=6, player=False))
        else:
            heroes.append(Hero.empty())
    make_boss_heroes(heroes, neutral=neutral, multiplier=0.01, speed=-150)

    return Team(heroes, pet=Familiar.empty)


def dummy_guild(neutral=True):
    heroes = []
    for i in range(1, 7):
        if i in (2, 4, 6):
            heroes.append(Hero.martin(star=6, player=False))
        else:
            heroes.append(Hero.empty())
    make_boss_heroes(heroes, neutral=neutral, multiplier=5, speed=450)

    return Team(heroes, pet=Familiar.empty)


@dataclass
class DummyTeam:
    friend = dummy_friend
    guild = dummy_guild
