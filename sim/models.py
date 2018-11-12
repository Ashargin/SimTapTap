from enum import Enum
from dataclasses import dataclass


## Heroes names, types and factions
class Faction(Enum):
    ALLIANCE = 'ALLIANCE'
    HORDE = 'HORDE'
    ELF = 'ELF'
    UNDEAD = 'UNDEAD'
    HEAVEN = 'HEAVEN'
    HELL = 'HELL'


class HeroType(Enum):
    WARRIOR = 'WARRIOR'
    ASSASSIN = 'ASSASSIN'
    WANDERER = 'WANDERER'
    CLERIC = 'CLERIC'
    MAGE = 'MAGE'


class HeroName(Enum):
    SCARLET = 'Scarlet'


## Equipment
class Equipment:
    def __init__(self, armor, helmet, weapon, pendant):
        self.hp = armor.hp + helmet.hp
        self.atk = weapon.atk + pendant.atk

        hp_bonus = 0
        atk_bonus = 0
        set_counts = {}
        for item in armor, helmet, weapon, pendant:
            if item.set in set_counts:
                set_counts[item.set] += 1
            else:
                set_counts[item.set] = 1
        for set in set_counts:
            if set_counts[set] >= 2:
                hp_bonus += set.hp_bonus_1
            if set_counts[set] >= 3:
                atk_bonus += set.atk_bonus
            if set_counts[set] == 4:
                hp_bonus += set.hp_bonus_2

        self.hp_bonus = hp_bonus
        self.atk_bonus = atk_bonus


@dataclass
class SetEmpty:
    hp_bonus_1 = 0
    atk_bonus = 0
    hp_bonus_2 = 0
@dataclass
class SetG1:
    hp_bonus_1 = 0.01
    atk_bonus = 0.02
    hp_bonus_2 = 0.01
@dataclass
class SetG2:
    hp_bonus_1 = 0.01
    atk_bonus = 0.02
    hp_bonus_2 = 0.01
@dataclass
class SetB1:
    hp_bonus_1 = 0.01
    atk_bonus = 0.02
    hp_bonus_2 = 0.01
@dataclass
class SetB2:
    hp_bonus_1 = 0.01
    atk_bonus = 0.02
    hp_bonus_2 = 0.01
@dataclass
class SetY1:
    hp_bonus_1 = 0.01
    atk_bonus = 0.02
    hp_bonus_2 = 0.01
@dataclass
class SetY2:
    hp_bonus_1 = 0.01
    atk_bonus = 0.02
    hp_bonus_2 = 0.01
@dataclass
class SetY3:
    hp_bonus_1 = 0.01
    atk_bonus = 0.02
    hp_bonus_2 = 0.01
@dataclass
class SetP1:
    hp_bonus_1 = 0.01
    atk_bonus = 0.02
    hp_bonus_2 = 0.01
@dataclass
class SetP2:
    hp_bonus_1 = 0.01
    atk_bonus = 0.02
    hp_bonus_2 = 0.01
@dataclass
class SetP3:
    hp_bonus_1 = 0.01
    atk_bonus = 0.02
    hp_bonus_2 = 0.01
@dataclass
class SetP4:
    hp_bonus_1 = 0.01
    atk_bonus = 0.02
    hp_bonus_2 = 0.01
@dataclass
class SetO1:
    hp_bonus_1 = 0.01
    atk_bonus = 0.02
    hp_bonus_2 = 0.01
@dataclass
class SetO2:
    hp_bonus_1 = 0.01
    atk_bonus = 0.02
    hp_bonus_2 = 0.01
@dataclass
class SetO3:
    hp_bonus_1 = 0.01
    atk_bonus = 0.02
    hp_bonus_2 = 0.01
@dataclass
class SetO4:
    hp_bonus_1 = 0.01
    atk_bonus = 0.02
    hp_bonus_2 = 0.01


@dataclass
class Empty:
    hp = 0
    atk = 0
    set = SetEmpty


@dataclass
class ArmorG1:
    hp = 1000
    set = SetG1
@dataclass
class ArmorG2:
    hp = 1000
    set = SetG2
@dataclass
class ArmorB1:
    hp = 1000
    set = SetB1
@dataclass
class ArmorB2:
    hp = 1000
    set = SetB2
@dataclass
class ArmorY1:
    hp = 1000
    set = SetY1
@dataclass
class ArmorY2:
    hp = 1000
    set = SetY2
@dataclass
class ArmorY3:
    hp = 1000
    set = SetY3
@dataclass
class ArmorP1:
    hp = 1000
    set = SetP1
@dataclass
class ArmorP2:
    hp = 1000
    set = SetP2
@dataclass
class ArmorP3:
    hp = 1000
    set = SetP3
@dataclass
class ArmorP4:
    hp = 1000
    set = SetP4
@dataclass
class ArmorO1:
    hp = 1000
    set = SetO1
@dataclass
class ArmorO2:
    hp = 1000
    set = SetO2
@dataclass
class ArmorO3:
    hp = 1000
    set = SetO3
@dataclass
class ArmorO4:
    hp = 1000
    set = SetO4


@dataclass
class HelmetG1:
    hp = 1000
    set = SetG1
@dataclass
class HelmetG2:
    hp = 1000
    set = SetG2
@dataclass
class HelmetB1:
    hp = 1000
    set = SetB1
@dataclass
class HelmetB2:
    hp = 1000
    set = SetB2
@dataclass
class HelmetY1:
    hp = 1000
    set = SetY1
@dataclass
class HelmetY2:
    hp = 1000
    set = SetY2
@dataclass
class HelmetY3:
    hp = 1000
    set = SetY3
@dataclass
class HelmetP1:
    hp = 1000
    set = SetP1
@dataclass
class HelmetP2:
    hp = 1000
    set = SetP2
@dataclass
class HelmetP3:
    hp = 1000
    set = SetP3
@dataclass
class HelmetP4:
    hp = 1000
    set = SetP4
@dataclass
class HelmetO1:
    hp = 1000
    set = SetO1
@dataclass
class HelmetO2:
    hp = 1000
    set = SetO2
@dataclass
class HelmetO3:
    hp = 1000
    set = SetO3
@dataclass
class HelmetO4:
    hp = 1000
    set = SetO4


@dataclass
class WeaponG1:
    atk = 1000
    set = SetG1
@dataclass
class WeaponG2:
    atk = 1000
    set = SetG2
@dataclass
class WeaponB1:
    atk = 1000
    set = SetB1
@dataclass
class WeaponB2:
    atk = 1000
    set = SetB2
@dataclass
class WeaponY1:
    atk = 1000
    set = SetY1
@dataclass
class WeaponY2:
    atk = 1000
    set = SetY2
@dataclass
class WeaponY3:
    atk = 1000
    set = SetY3
@dataclass
class WeaponP1:
    atk = 1000
    set = SetP1
@dataclass
class WeaponP2:
    atk = 1000
    set = SetP2
@dataclass
class WeaponP3:
    atk = 1000
    set = SetP3
@dataclass
class WeaponP4:
    atk = 1000
    set = SetP4
@dataclass
class WeaponO1:
    atk = 1000
    set = SetO1
@dataclass
class WeaponO2:
    atk = 1000
    set = SetO2
@dataclass
class WeaponO3:
    atk = 1000
    set = SetO3
@dataclass
class WeaponO4:
    atk = 1000
    set = SetO4


@dataclass
class PendantG1:
    atk = 1000
    set = SetG1
@dataclass
class PendantG2:
    atk = 1000
    set = SetG2
@dataclass
class PendantB1:
    atk = 1000
    set = SetB1
@dataclass
class PendantB2:
    atk = 1000
    set = SetB2
@dataclass
class PendantY1:
    atk = 1000
    set = SetY1
@dataclass
class PendantY2:
    atk = 1000
    set = SetY2
@dataclass
class PendantY3:
    atk = 1000
    set = SetY3
@dataclass
class PendantP1:
    atk = 1000
    set = SetP1
@dataclass
class PendantP2:
    atk = 1000
    set = SetP2
@dataclass
class PendantP3:
    atk = 1000
    set = SetP3
@dataclass
class PendantP4:
    atk = 1000
    set = SetP4
@dataclass
class PendantO1:
    atk = 1000
    set = SetO1
@dataclass
class PendantO2:
    atk = 1000
    set = SetO2
@dataclass
class PendantO3:
    atk = 1000
    set = SetO3
@dataclass
class PendantO4:
    atk = 1000
    set = SetO4


@dataclass
class Armor:
    G1 = ArmorG1
    G2 = ArmorG2
    B1 = ArmorB1
    B2 = ArmorB2
    Y1 = ArmorY1
    Y2 = ArmorY2
    Y3 = ArmorY3
    P1 = ArmorP1
    P2 = ArmorP2
    P3 = ArmorP3
    P4 = ArmorP4
    O1 = ArmorO1
    O2 = ArmorO2
    O3 = ArmorO3
    O4 = ArmorO4


@dataclass
class Helmet:
    G1 = HelmetG1
    G2 = HelmetG2
    B1 = HelmetB1
    B2 = HelmetB2
    Y1 = HelmetY1
    Y2 = HelmetY2
    Y3 = HelmetY3
    P1 = HelmetP1
    P2 = HelmetP2
    P3 = HelmetP3
    P4 = HelmetP4
    O1 = HelmetO1
    O2 = HelmetO2
    O3 = HelmetO3
    O4 = HelmetO4


@dataclass
class Weapon:
    G1 = WeaponG1
    G2 = WeaponG2
    B1 = WeaponB1
    B2 = WeaponB2
    Y1 = WeaponY1
    Y2 = WeaponY2
    Y3 = WeaponY3
    P1 = WeaponP1
    P2 = WeaponP2
    P3 = WeaponP3
    P4 = WeaponP4
    O1 = WeaponO1
    O2 = WeaponO2
    O3 = WeaponO3
    O4 = WeaponO4


@dataclass
class Pendant:
    G1 = PendantG1
    G2 = PendantG2
    B1 = PendantB1
    B2 = PendantB2
    Y1 = PendantY1
    Y2 = PendantY2
    Y3 = PendantY3
    P1 = PendantP1
    P2 = PendantP2
    P3 = PendantP3
    P4 = PendantP4
    O1 = PendantO1
    O2 = PendantO2
    O3 = PendantO3
    O4 = PendantO4


## Rune
class BaseRune:
    atk = 0
    hp = 0
    atk_bonus = 0
    hp_bonus = 0


class AttackRuneG1(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneG2(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneB1(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneB2(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneY1(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneY2(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneY3(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneP1(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneP2(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneP3(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneP4(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneO1(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneO2(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneO3(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneO4(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneR1(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneR2(BaseRune):
    atk = 1000
    atk_bonus = 0.15
class AttackRuneG1(BaseRune):
    atk = 1000
    atk_bonus = 0.15


@dataclass
class AttackRune:
    G1 = AttackRuneG1()
    G2 = AttackRuneG2()
    B1 = AttackRuneB1()
    B2 = AttackRuneB2()
    Y1 = AttackRuneY1()
    Y2 = AttackRuneY2()
    Y3 = AttackRuneY3()
    P1 = AttackRuneP1()
    P2 = AttackRuneP2()
    P3 = AttackRuneP3()
    P4 = AttackRuneP4()
    O1 = AttackRuneO1()
    O2 = AttackRuneO2()
    O3 = AttackRuneO3()
    O4 = AttackRuneO4()
    R1 = AttackRuneR1()
    R2 = AttackRuneR2()


@dataclass
class Rune:
    attack = AttackRune


## Artifact
class BaseArtifact:
    atk = 0
    hp = 0
    atk_bonus = 0
    hp_bonus = 0
    damage_to_warriors = 0
    damage_to_assassins = 0
    damage_to_wanderers = 0
    damage_to_clerics = 0
    damage_to_mages = 0


class WarriorArtifactG1(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15
class WarriorArtifactG2(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15
class WarriorArtifactB1(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15
class WarriorArtifactB2(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15
class WarriorArtifactY1(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15
class WarriorArtifactY2(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15
class WarriorArtifactY3(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15
class WarriorArtifactP1(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15
class WarriorArtifactP2(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15
class WarriorArtifactP3(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15
class WarriorArtifactP4(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15
class WarriorArtifactO1(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15
class WarriorArtifactO2(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15
class WarriorArtifactO3(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15
class WarriorArtifactO4(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15
class WarriorArtifactO5(BaseArtifact):
    atk = 1000
    damage_to_warriors = 0.15


class AssassinArtifactG1(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15
class AssassinArtifactG2(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15
class AssassinArtifactB1(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15
class AssassinArtifactB2(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15
class AssassinArtifactY1(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15
class AssassinArtifactY2(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15
class AssassinArtifactY3(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15
class AssassinArtifactP1(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15
class AssassinArtifactP2(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15
class AssassinArtifactP3(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15
class AssassinArtifactP4(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15
class AssassinArtifactO1(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15
class AssassinArtifactO2(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15
class AssassinArtifactO3(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15
class AssassinArtifactO4(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15
class AssassinArtifactO5(BaseArtifact):
    atk = 1000
    damage_to_assassins = 0.15


class WandererArtifactG1(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15
class WandererArtifactG2(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15
class WandererArtifactB1(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15
class WandererArtifactB2(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15
class WandererArtifactY1(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15
class WandererArtifactY2(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15
class WandererArtifactY3(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15
class WandererArtifactP1(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15
class WandererArtifactP2(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15
class WandererArtifactP3(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15
class WandererArtifactP4(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15
class WandererArtifactO1(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15
class WandererArtifactO2(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15
class WandererArtifactO3(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15
class WandererArtifactO4(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15
class WandererArtifactO5(BaseArtifact):
    atk = 1000
    damage_to_wanderers = 0.15


class ClericArtifactG1(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15
class ClericArtifactG2(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15
class ClericArtifactB1(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15
class ClericArtifactB2(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15
class ClericArtifactY1(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15
class ClericArtifactY2(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15
class ClericArtifactY3(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15
class ClericArtifactP1(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15
class ClericArtifactP2(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15
class ClericArtifactP3(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15
class ClericArtifactP4(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15
class ClericArtifactO1(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15
class ClericArtifactO2(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15
class ClericArtifactO3(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15
class ClericArtifactO4(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15
class ClericArtifactO5(BaseArtifact):
    atk = 1000
    damage_to_clerics = 0.15


class MageArtifactG1(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15
class MageArtifactG2(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15
class MageArtifactB1(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15
class MageArtifactB2(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15
class MageArtifactY1(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15
class MageArtifactY2(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15
class MageArtifactY3(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15
class MageArtifactP1(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15
class MageArtifactP2(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15
class MageArtifactP3(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15
class MageArtifactP4(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15
class MageArtifactO1(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15
class MageArtifactO2(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15
class MageArtifactO3(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15
class MageArtifactO4(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15
class MageArtifactO5(BaseArtifact):
    atk = 1000
    damage_to_mages = 0.15


@dataclass
class WarriorArtifact:
    G1 = WarriorArtifactG1()
    G2 = WarriorArtifactG2()
    B1 = WarriorArtifactB1()
    B2 = WarriorArtifactB2()
    Y1 = WarriorArtifactY1()
    Y2 = WarriorArtifactY2()
    Y3 = WarriorArtifactY3()
    P1 = WarriorArtifactP1()
    P2 = WarriorArtifactP2()
    P3 = WarriorArtifactP3()
    P4 = WarriorArtifactP4()
    O1 = WarriorArtifactO1()
    O2 = WarriorArtifactO2()
    O3 = WarriorArtifactO3()
    O4 = WarriorArtifactO4()
    O5 = WarriorArtifactO5()


@dataclass
class AssassinArtifact:
    G1 = AssassinArtifactG1()
    G2 = AssassinArtifactG2()
    B1 = AssassinArtifactB1()
    B2 = AssassinArtifactB2()
    Y1 = AssassinArtifactY1()
    Y2 = AssassinArtifactY2()
    Y3 = AssassinArtifactY3()
    P1 = AssassinArtifactP1()
    P2 = AssassinArtifactP2()
    P3 = AssassinArtifactP3()
    P4 = AssassinArtifactP4()
    O1 = AssassinArtifactO1()
    O2 = AssassinArtifactO2()
    O3 = AssassinArtifactO3()
    O4 = AssassinArtifactO4()
    O5 = AssassinArtifactO5()


@dataclass
class WandererArtifact:
    G1 = WandererArtifactG1()
    G2 = WandererArtifactG2()
    B1 = WandererArtifactB1()
    B2 = WandererArtifactB2()
    Y1 = WandererArtifactY1()
    Y2 = WandererArtifactY2()
    Y3 = WandererArtifactY3()
    P1 = WandererArtifactP1()
    P2 = WandererArtifactP2()
    P3 = WandererArtifactP3()
    P4 = WandererArtifactP4()
    O1 = WandererArtifactO1()
    O2 = WandererArtifactO2()
    O3 = WandererArtifactO3()
    O4 = WandererArtifactO4()
    O5 = WandererArtifactO5()


@dataclass
class ClericArtifact:
    G1 = ClericArtifactG1()
    G2 = ClericArtifactG2()
    B1 = ClericArtifactB1()
    B2 = ClericArtifactB2()
    Y1 = ClericArtifactY1()
    Y2 = ClericArtifactY2()
    Y3 = ClericArtifactY3()
    P1 = ClericArtifactP1()
    P2 = ClericArtifactP2()
    P3 = ClericArtifactP3()
    P4 = ClericArtifactP4()
    O1 = ClericArtifactO1()
    O2 = ClericArtifactO2()
    O3 = ClericArtifactO3()
    O4 = ClericArtifactO4()
    O5 = ClericArtifactO5()


@dataclass
class MageArtifact:
    G1 = MageArtifactG1()
    G2 = MageArtifactG2()
    B1 = MageArtifactB1()
    B2 = MageArtifactB2()
    Y1 = MageArtifactY1()
    Y2 = MageArtifactY2()
    Y3 = MageArtifactY3()
    P1 = MageArtifactP1()
    P2 = MageArtifactP2()
    P3 = MageArtifactP3()
    P4 = MageArtifactP4()
    O1 = MageArtifactO1()
    O2 = MageArtifactO2()
    O3 = MageArtifactO3()
    O4 = MageArtifactO4()
    O5 = MageArtifactO5()


@dataclass
class Artifact:
    warrior = WarriorArtifact
    assassin = AssassinArtifact
    wanderer = WandererArtifact
    cleric = ClericArtifact
    mage = MageArtifact


## Aura
class Aura:
    def __init__(self, heroes):
        alliance_count = len([h for h in heroes if h.faction == Faction.ALLIANCE])
        horde_count = len([h for h in heroes if h.faction == Faction.HORDE])
        elf_count = len([h for h in heroes if h.faction == Faction.ELF])
        undead_count = len([h for h in heroes if h.faction == Faction.UNDEAD])
        heaven_count = len([h for h in heroes if h.faction == Faction.HEAVEN])
        hell_count = len([h for h in heroes if h.faction == Faction.HELL])

        self.atk_bonus = 0
        self.hp_bonus = 0
        self.dodge = 0
        self.crit_rate = 0
        self.armor_break_bonus = 0
        self.control_immune = 0

        if alliance_count == 6:
            self.dodge = 0.05
            self.hp_bonus = 0.2
        elif horde_count == 6:
            self.atk_bonus = 0.15
            self.hp_bonus = 0.2
        elif elf_count == 6:
            self.crit_rate = 0.05
            self.hp_bonus = 0.2
        elif undead_count == 6:
            self.armor_break_bonus = 0.2
            self.hp_bonus = 0.2
        elif heaven_count == 6:
            self.control_immune = 0.3
            self.hp_bonus = 0.2
        elif hell_count == 6:
            self.control_immune = 0.3
            self.hp_bonus = 0.2
        elif min([alliance_count, horde_count, elf_count, undead_count, heaven_count, hell_count]) == 1:
            self.atk_bonus = 0.1
            self.hp_bonus = 0.1
        elif min([heaven_count, hell_count]) == 3:
            self.atk_bonus = 0.135
            self.hp_bonus = 0.16
        elif min([alliance_count, elf_count]) == 3:
            self.atk_bonus = 0.1
            self.hp_bonus = 0.08
        elif min([horde_count, undead_count]) == 3:
            self.atk_bonus = 0.08
            self.hp_bonus = 0.1
        elif min([alliance_count, elf_count, heaven_count]) == 2:
            self.atk_bonus = 0.11
            self.hp_bonus = 0.13
        elif min([horde_count, undead_count, hell_count]) == 2:
            self.atk_bonus = 0.13
            self.hp_bonus = 0.11
