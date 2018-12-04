from enum import Enum
from dataclasses import dataclass

from sim.utils import targets_at_random


## Heroes names, types and factions
class Faction(Enum):
    EMPTY = 'EMPTY'
    ALLIANCE = 'ALLIANCE'
    HORDE = 'HORDE'
    ELF = 'ELF'
    UNDEAD = 'UNDEAD'
    HEAVEN = 'HEAVEN'
    HELL = 'HELL'


class HeroType(Enum):
    EMPTY = 'EMPTY'
    WARRIOR = 'WARRIOR'
    ASSASSIN = 'ASSASSIN'
    WANDERER = 'WANDERER'
    CLERIC = 'CLERIC'
    MAGE = 'MAGE'


class HeroName(Enum):
    EMPTY = 'Empty_Hero'

    SIR_CONRAD = 'Sir_Conrad'
    LONE_HERO = 'Lone_Hero'
    OLIVIA = 'Olivia'
    KING_LIONHEART = 'King_Lionheart'
    TESLA = 'Tesla'
    MULAN = 'Mulan'
    SAW_MACHINE = 'Saw_Machine'
    ULTIMA = 'Ultima'
    VIVIENNE = 'Vivienne'
    MARTIN = 'Martin'
    SAMURAI = 'Samurai'

    KHALIL = 'Khalil'
    RLYEH = 'Rlyeh'
    WOLF_RIDER = 'Wolf_Rider'
    ABYSS_LORD = 'Abyss_Lord'
    MEDUSA = 'Medusa'
    EAGLE_EYE_SHAMAN = 'Eagle-eye_Shaman'
    SWORD_MASTER = 'Sword_Master'
    SCARLET = 'Scarlet'
    MINOTAUR = 'Minotaur'
    BLOOD_TOOTH = 'Blood_Tooth'
    LEXAR = 'Lexar'

    MEGAW = 'Megaw'
    WEREWOLF = 'Werewolf'
    CENTAUR = 'Centaur'
    TIGER_KING = 'Tiger_King'
    DEMON_FIGHTER = 'Demon_Fighter'
    GRAND = 'Grand'
    FOREST_HEALER = 'Forest_Healer'
    ORPHEE = 'Orphee'
    LUNA = 'Luna'
    VEGVISIR = 'Vegvisir'

    FORREN = 'Forren'
    PUPPET_MAID = 'Puppet_Maid'
    EXDEATH = 'Exdeath'
    HESTER = 'Hester'
    DZIEWONA = 'Dziewona'
    WOLNIR = 'Wolnir'
    CURSED_ONE = 'Cursed_One'
    GERALD = 'Gerald'
    REAPER = 'Reaper'
    RIPPER = 'Ripper'
    ADEN = 'Aden'
    SHUDDE_M_ELL = "Shudde_M'ell"

    HEAVEN_JUDGE = 'Heaven_Judge'
    NAMELESS_KING = 'Nameless_King'
    VERTHANDI = 'Verthandi'
    MARS = 'Mars'

    DARK_JUDGE = 'Dark_Judge'
    FREYA = 'Freya'
    MONKEY_KING = 'Monkey_King'
    CHESSIA = 'Chessia'


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
    hp_bonus_1 = 0
    atk_bonus = 0
    hp_bonus_2 = 0


@dataclass
class SetG2:
    hp_bonus_1 = 0
    atk_bonus = 0
    hp_bonus_2 = 0


@dataclass
class SetB1:
    hp_bonus_1 = 0
    atk_bonus = 0
    hp_bonus_2 = 0


@dataclass
class SetB2:
    hp_bonus_1 = 0
    atk_bonus = 0
    hp_bonus_2 = 0


@dataclass
class SetY1:
    hp_bonus_1 = 0
    atk_bonus = 0
    hp_bonus_2 = 0


@dataclass
class SetY2:
    hp_bonus_1 = 0
    atk_bonus = 0
    hp_bonus_2 = 0


@dataclass
class SetY3:
    hp_bonus_1 = 0.02
    atk_bonus = 0.03
    hp_bonus_2 = 0.01


@dataclass
class SetP1:
    hp_bonus_1 = 0.04
    atk_bonus = 0.05
    hp_bonus_2 = 0.02


@dataclass
class SetP2:
    hp_bonus_1 = 0.05
    atk_bonus = 0.07
    hp_bonus_2 = 0.04


@dataclass
class SetP3:
    hp_bonus_1 = 0.07
    atk_bonus = 0.09
    hp_bonus_2 = 0.04


@dataclass
class SetP4:
    hp_bonus_1 = 0.08
    atk_bonus = 0.11
    hp_bonus_2 = 0.05


@dataclass
class SetO1:
    hp_bonus_1 = 0.1
    atk_bonus = 0.13
    hp_bonus_2 = 0.05


@dataclass
class SetO2:
    hp_bonus_1 = 0.11
    atk_bonus = 0.15
    hp_bonus_2 = 0.06


@dataclass
class SetO3:
    hp_bonus_1 = 0.12
    atk_bonus = 0.17
    hp_bonus_2 = 0.07


@dataclass
class SetO4:
    hp_bonus_1 = 0.14
    atk_bonus = 0.19
    hp_bonus_2 = 0.07


@dataclass
class EmptyItem:
    hp = 0
    atk = 0
    set = SetEmpty


@dataclass
class ArmorG1:
    hp = 141
    set = SetG1


@dataclass
class ArmorG2:
    hp = 169
    set = SetG2


@dataclass
class ArmorB1:
    hp = 337
    set = SetB1


@dataclass
class ArmorB2:
    hp = 434
    set = SetB2


@dataclass
class ArmorY1:
    hp = 970
    set = SetY1


@dataclass
class ArmorY2:
    hp = 1255
    set = SetY2


@dataclass
class ArmorY3:
    hp = 1541
    set = SetY3


@dataclass
class ArmorP1:
    hp = 2645
    set = SetP1


@dataclass
class ArmorP2:
    hp = 3207
    set = SetP2


@dataclass
class ArmorP3:
    hp = 3770
    set = SetP3


@dataclass
class ArmorP4:
    hp = 4333
    set = SetP4


@dataclass
class ArmorO1:
    hp = 6401
    set = SetO1


@dataclass
class ArmorO2:
    hp = 7811
    set = SetO2


@dataclass
class ArmorO3:
    hp = 9222
    set = SetO3


@dataclass
class ArmorO4:
    hp = 10632
    set = SetO4


@dataclass
class HelmetG1:
    hp = 94
    set = SetG1


@dataclass
class HelmetG2:
    hp = 113
    set = SetG2


@dataclass
class HelmetB1:
    hp = 223
    set = SetB1


@dataclass
class HelmetB2:
    hp = 289
    set = SetB2


@dataclass
class HelmetY1:
    hp = 647
    set = SetY1


@dataclass
class HelmetY2:
    hp = 837
    set = SetY2


@dataclass
class HelmetY3:
    hp = 1027
    set = SetY3


@dataclass
class HelmetP1:
    hp = 1763
    set = SetP1


@dataclass
class HelmetP2:
    hp = 2183
    set = SetP2


@dataclass
class HelmetP3:
    hp = 2513
    set = SetP3


@dataclass
class HelmetP4:
    hp = 2889
    set = SetP4


@dataclass
class HelmetO1:
    hp = 4267
    set = SetO1


@dataclass
class HelmetO2:
    hp = 5207
    set = SetO2


@dataclass
class HelmetO3:
    hp = 6148
    set = SetO3


@dataclass
class HelmetO4:
    hp = 7088
    set = SetO4


@dataclass
class WeaponG1:
    atk = 32
    set = SetG1


@dataclass
class WeaponG2:
    atk = 38
    set = SetG2


@dataclass
class WeaponB1:
    atk = 66
    set = SetB1


@dataclass
class WeaponB2:
    atk = 85
    set = SetB2


@dataclass
class WeaponY1:
    atk = 168
    set = SetY1


@dataclass
class WeaponY2:
    atk = 218
    set = SetY2


@dataclass
class WeaponY3:
    atk = 256
    set = SetY3


@dataclass
class WeaponP1:
    atk = 414
    set = SetP1


@dataclass
class WeaponP2:
    atk = 502
    set = SetP2


@dataclass
class WeaponP3:
    atk = 590
    set = SetP3


@dataclass
class WeaponP4:
    atk = 678
    set = SetP4


@dataclass
class WeaponO1:
    atk = 914
    set = SetO1


@dataclass
class WeaponO2:
    atk = 1116
    set = SetO2


@dataclass
class WeaponO3:
    atk = 1317
    set = SetO3


@dataclass
class WeaponO4:
    atk = 1519
    set = SetO4


@dataclass
class PendantG1:
    atk = 21
    set = SetG1


@dataclass
class PendantG2:
    atk = 25
    set = SetG2


@dataclass
class PendantB1:
    atk = 44
    set = SetB1


@dataclass
class PendantB2:
    atk = 57
    set = SetB2


@dataclass
class PendantY1:
    atk = 112
    set = SetY1


@dataclass
class PendantY2:
    atk = 145
    set = SetY2


@dataclass
class PendantY3:
    atk = 178
    set = SetY3


@dataclass
class PendantP1:
    atk = 276
    set = SetP1


@dataclass
class PendantP2:
    atk = 335
    set = SetP2


@dataclass
class PendantP3:
    atk = 393
    set = SetP3


@dataclass
class PendantP4:
    atk = 452
    set = SetP4


@dataclass
class PendantO1:
    atk = 610
    set = SetO1


@dataclass
class PendantO2:
    atk = 744
    set = SetO2


@dataclass
class PendantO3:
    atk = 878
    set = SetO3


@dataclass
class PendantO4:
    atk = 1013
    set = SetO4


@dataclass
class Armor:
    empty = EmptyItem
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


armor_from_request = {
    'EMPTY': Armor.empty,
    'GREEN1': Armor.G1,
    'GREEN2': Armor.G2,
    'BLUE1': Armor.B1,
    'BLUE2': Armor.B2,
    'YELLOW1': Armor.Y1,
    'YELLOW2': Armor.Y2,
    'YELLOW3': Armor.Y3,
    'PURPLE1': Armor.P1,
    'PURPLE2': Armor.P2,
    'PURPLE3': Armor.P3,
    'PURPLE4': Armor.P4,
    'ORANGE1': Armor.O1,
    'ORANGE2': Armor.O2,
    'ORANGE3': Armor.O3,
    'ORANGE4': Armor.O4
}


@dataclass
class Helmet:
    empty = EmptyItem
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


helmet_from_request = {
    'EMPTY': Helmet.empty,
    'GREEN1': Helmet.G1,
    'GREEN2': Helmet.G2,
    'BLUE1': Helmet.B1,
    'BLUE2': Helmet.B2,
    'YELLOW1': Helmet.Y1,
    'YELLOW2': Helmet.Y2,
    'YELLOW3': Helmet.Y3,
    'PURPLE1': Helmet.P1,
    'PURPLE2': Helmet.P2,
    'PURPLE3': Helmet.P3,
    'PURPLE4': Helmet.P4,
    'ORANGE1': Helmet.O1,
    'ORANGE2': Helmet.O2,
    'ORANGE3': Helmet.O3,
    'ORANGE4': Helmet.O4
}


@dataclass
class Weapon:
    empty = EmptyItem
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


weapon_from_request = {
    'EMPTY': Weapon.empty,
    'GREEN1': Weapon.G1,
    'GREEN2': Weapon.G2,
    'BLUE1': Weapon.B1,
    'BLUE2': Weapon.B2,
    'YELLOW1': Weapon.Y1,
    'YELLOW2': Weapon.Y2,
    'YELLOW3': Weapon.Y3,
    'PURPLE1': Weapon.P1,
    'PURPLE2': Weapon.P2,
    'PURPLE3': Weapon.P3,
    'PURPLE4': Weapon.P4,
    'ORANGE1': Weapon.O1,
    'ORANGE2': Weapon.O2,
    'ORANGE3': Weapon.O3,
    'ORANGE4': Weapon.O4
}


@dataclass
class Pendant:
    empty = EmptyItem
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


pendant_from_request = {
    'EMPTY': Pendant.empty,
    'GREEN1': Pendant.G1,
    'GREEN2': Pendant.G2,
    'BLUE1': Pendant.B1,
    'BLUE2': Pendant.B2,
    'YELLOW1': Pendant.Y1,
    'YELLOW2': Pendant.Y2,
    'YELLOW3': Pendant.Y3,
    'PURPLE1': Pendant.P1,
    'PURPLE2': Pendant.P2,
    'PURPLE3': Pendant.P3,
    'PURPLE4': Pendant.P4,
    'ORANGE1': Pendant.O1,
    'ORANGE2': Pendant.O2,
    'ORANGE3': Pendant.O3,
    'ORANGE4': Pendant.O4
}


## Rune
class BaseRune:
    atk = 0
    hp = 0
    atk_bonus = 0
    hp_bonus = 0
    armor_break = 0
    skill_damage = 0
    hit_rate = 0
    dodge = 0
    crit_rate = 0
    crit_damage = 0


class EmptyRune(BaseRune):
    pass


class AccuracyRuneB1(BaseRune):
    atk = 0
    atk_bonus = 0
    hit_rate = 0


class AccuracyRuneB2(BaseRune):
    atk = 0
    atk_bonus = 0
    hit_rate = 0


class AccuracyRuneG1(BaseRune):
    atk = 50
    atk_bonus = 0
    hit_rate = 0.02


class AccuracyRuneG2(BaseRune):
    atk = 70
    atk_bonus = 0
    hit_rate = 0.03


class AccuracyRuneY1(BaseRune):
    atk = 125
    atk_bonus = 0
    hit_rate = 0.05


class AccuracyRuneY2(BaseRune):
    atk = 155
    atk_bonus = 0
    hit_rate = 0.06


class AccuracyRuneY3(BaseRune):
    atk = 185
    atk_bonus = 0
    hit_rate = 0.07


class AccuracyRuneP1(BaseRune):
    atk = 0
    atk_bonus = 0
    hit_rate = 0


class AccuracyRuneP2(BaseRune):
    atk = 0
    atk_bonus = 0
    hit_rate = 0


class AccuracyRuneP3(BaseRune):
    atk = 0
    atk_bonus = 0
    hit_rate = 0


class AccuracyRuneO1(BaseRune):
    atk = 0
    atk_bonus = 0
    hit_rate = 0


class AccuracyRuneO2(BaseRune):
    atk = 420
    atk_bonus = 0
    hit_rate = 0.14


class AccuracyRuneO3(BaseRune):
    atk = 0
    atk_bonus = 0
    hit_rate = 0


class AccuracyRuneO4(BaseRune):
    atk = 0
    atk_bonus = 0
    hit_rate = 0


class AccuracyRuneR1(BaseRune):
    atk = 0
    atk_bonus = 0
    hit_rate = 0


class AccuracyRuneR2(BaseRune):
    atk = 620
    atk_bonus = 0.09
    hit_rate = 0.19


class CritRateRuneB1(BaseRune):
    hp = 0
    hp_bonus = 0
    crit_rate = 0


class CritRateRuneB2(BaseRune):
    hp = 0
    hp_bonus = 0
    crit_rate = 0


class CritRateRuneG1(BaseRune):
    hp = 300
    hp_bonus = 0
    crit_rate = 0.02


class CritRateRuneG2(BaseRune):
    hp = 600
    hp_bonus = 0
    crit_rate = 0.03


class CritRateRuneY1(BaseRune):
    hp = 920
    hp_bonus = 0
    crit_rate = 0.05


class CritRateRuneY2(BaseRune):
    hp = 1200
    hp_bonus = 0
    crit_rate = 0.06


class CritRateRuneY3(BaseRune):
    hp = 1480
    hp_bonus = 0
    crit_rate = 0.07


class CritRateRuneP1(BaseRune):
    hp = 0
    hp_bonus = 0
    crit_rate = 0


class CritRateRuneP2(BaseRune):
    hp = 0
    hp_bonus = 0
    crit_rate = 0


class CritRateRuneP3(BaseRune):
    hp = 2280
    hp_bonus = 0
    crit_rate = 0.11


class CritRateRuneO1(BaseRune):
    hp = 0
    hp_bonus = 0
    crit_rate = 0


class CritRateRuneO2(BaseRune):
    hp = 3460
    hp_bonus = 0
    crit_rate = 0.14


class CritRateRuneO3(BaseRune):
    hp = 0
    hp_bonus = 0
    crit_rate = 0


class CritRateRuneO4(BaseRune):
    hp = 0
    hp_bonus = 0
    crit_rate = 0


class CritRateRuneR1(BaseRune):
    hp = 0
    hp_bonus = 0
    crit_rate = 0


class CritRateRuneR2(BaseRune):
    hp = 0
    hp_bonus = 0.13
    crit_rate = 0.19


class AttackRuneB1(BaseRune):
    atk = 55
    atk_bonus = 0


class AttackRuneB2(BaseRune):
    atk = 72
    atk_bonus = 0


class AttackRuneG1(BaseRune):
    atk = 110
    atk_bonus = 0


class AttackRuneG2(BaseRune):
    atk = 150
    atk_bonus = 0


class AttackRuneY1(BaseRune):
    atk = 210
    atk_bonus = 0.04


class AttackRuneY2(BaseRune):
    atk = 270
    atk_bonus = 0.05


class AttackRuneY3(BaseRune):
    atk = 330
    atk_bonus = 0.06


class AttackRuneP1(BaseRune):
    atk = 0
    atk_bonus = 0


class AttackRuneP2(BaseRune):
    atk = 0
    atk_bonus = 0


class AttackRuneP3(BaseRune):
    atk = 0
    atk_bonus = 0


class AttackRuneO1(BaseRune):
    atk = 640
    atk_bonus = 0.135


class AttackRuneO2(BaseRune):
    atk = 0
    atk_bonus = 0


class AttackRuneO3(BaseRune):
    atk = 800
    atk_bonus = 0.165


class AttackRuneO4(BaseRune):
    atk = 0
    atk_bonus = 0


class AttackRuneR1(BaseRune):
    atk = 0
    atk_bonus = 0


class AttackRuneR2(BaseRune):
    atk = 1200
    atk_bonus = 0.22


class EvasionRuneB1(BaseRune):
    hp = 0
    hp_bonus = 0
    dodge = 0


class EvasionRuneB2(BaseRune):
    hp = 0
    hp_bonus = 0
    dodge = 0


class EvasionRuneG1(BaseRune):
    hp = 0
    hp_bonus = 0
    dodge = 0


class EvasionRuneG2(BaseRune):
    hp = 0
    hp_bonus = 0
    dodge = 0


class EvasionRuneY1(BaseRune):
    hp = 920
    hp_bonus = 0
    dodge = 0.035


class EvasionRuneY2(BaseRune):
    hp = 1200
    hp_bonus = 0
    dodge = 0.045


class EvasionRuneY3(BaseRune):
    hp = 0
    hp_bonus = 0
    dodge = 0


class EvasionRuneP1(BaseRune):
    hp = 0
    hp_bonus = 0
    dodge = 0


class EvasionRuneP2(BaseRune):
    hp = 0
    hp_bonus = 0
    dodge = 0


class EvasionRuneP3(BaseRune):
    hp = 0
    hp_bonus = 0
    dodge = 0


class EvasionRuneO1(BaseRune):
    hp = 0
    hp_bonus = 0
    dodge = 0


class EvasionRuneO2(BaseRune):
    hp = 0
    hp_bonus = 0
    dodge = 0


class EvasionRuneO3(BaseRune):
    hp = 0
    hp_bonus = 0
    dodge = 0


class EvasionRuneO4(BaseRune):
    hp = 0
    hp_bonus = 0
    dodge = 0


class EvasionRuneR1(BaseRune):
    hp = 0
    hp_bonus = 0
    dodge = 0


class EvasionRuneR2(BaseRune):
    hp = 0
    hp_bonus = 0.12
    dodge = 0.16


class ArmorBreakRuneB1(BaseRune):
    atk = 0
    atk_bonus = 0
    armor_break = 0


class ArmorBreakRuneB2(BaseRune):
    atk = 0
    atk_bonus = 0
    armor_break = 0


class ArmorBreakRuneG1(BaseRune):
    atk = 0
    atk_bonus = 0
    armor_break = 0


class ArmorBreakRuneG2(BaseRune):
    atk = 0
    atk_bonus = 0
    armor_break = 0


class ArmorBreakRuneY1(BaseRune):
    atk = 125
    atk_bonus = 0
    armor_break = 2


class ArmorBreakRuneY2(BaseRune):
    atk = 155
    atk_bonus = 0
    armor_break = 3


class ArmorBreakRuneY3(BaseRune):
    atk = 185
    atk_bonus = 0
    armor_break = 4


class ArmorBreakRuneP1(BaseRune):
    atk = 0
    atk_bonus = 0
    armor_break = 0


class ArmorBreakRuneP2(BaseRune):
    atk = 0
    atk_bonus = 0
    armor_break = 0


class ArmorBreakRuneP3(BaseRune):
    atk = 0
    atk_bonus = 0
    armor_break = 0


class ArmorBreakRuneO1(BaseRune):
    atk = 0
    atk_bonus = 0
    armor_break = 0


class ArmorBreakRuneO2(BaseRune):
    atk = 0
    atk_bonus = 0
    armor_break = 0


class ArmorBreakRuneO3(BaseRune):
    atk = 0
    atk_bonus = 0
    armor_break = 0


class ArmorBreakRuneO4(BaseRune):
    atk = 0
    atk_bonus = 0
    armor_break = 0


class ArmorBreakRuneR1(BaseRune):
    atk = 0
    atk_bonus = 0
    armor_break = 0


class ArmorBreakRuneR2(BaseRune):
    atk = 620
    atk_bonus = 0.09
    armor_break = 13


class SkillDamageRuneB1(BaseRune):
    skill_damage = 0
    hit_rate = 0


class SkillDamageRuneB2(BaseRune):
    skill_damage = 0
    hit_rate = 0


class SkillDamageRuneG1(BaseRune):
    skill_damage = 0
    hit_rate = 0


class SkillDamageRuneG2(BaseRune):
    skill_damage = 0
    hit_rate = 0


class SkillDamageRuneY1(BaseRune):
    skill_damage = 0
    hit_rate = 0


class SkillDamageRuneY2(BaseRune):
    skill_damage = 0
    hit_rate = 0


class SkillDamageRuneY3(BaseRune):
    skill_damage = 0
    hit_rate = 0


class SkillDamageRuneP1(BaseRune):
    skill_damage = 0
    hit_rate = 0


class SkillDamageRuneP2(BaseRune):
    skill_damage = 0
    hit_rate = 0


class SkillDamageRuneP3(BaseRune):
    skill_damage = 0.14
    hit_rate = 0.05


class SkillDamageRuneO1(BaseRune):
    skill_damage = 0
    hit_rate = 0


class SkillDamageRuneO2(BaseRune):
    skill_damage = 0
    hit_rate = 0


class SkillDamageRuneO3(BaseRune):
    skill_damage = 0
    hit_rate = 0


class SkillDamageRuneO4(BaseRune):
    skill_damage = 0
    hit_rate = 0


class SkillDamageRuneR1(BaseRune):
    skill_damage = 0
    hit_rate = 0


class SkillDamageRuneR2(BaseRune):
    skill_damage = 0.26
    hit_rate = 0.13


class CritDamageRuneB1(BaseRune):
    crit_rate = 0
    crit_damage = 0


class CritDamageRuneB2(BaseRune):
    crit_rate = 0
    crit_damage = 0


class CritDamageRuneG1(BaseRune):
    crit_rate = 0
    crit_damage = 0


class CritDamageRuneG2(BaseRune):
    crit_rate = 0
    crit_damage = 0


class CritDamageRuneY1(BaseRune):
    crit_rate = 0
    crit_damage = 0


class CritDamageRuneY2(BaseRune):
    crit_rate = 0
    crit_damage = 0


class CritDamageRuneY3(BaseRune):
    crit_rate = 0
    crit_damage = 0


class CritDamageRuneP1(BaseRune):
    crit_rate = 0
    crit_damage = 0


class CritDamageRuneP2(BaseRune):
    crit_rate = 0
    crit_damage = 0


class CritDamageRuneP3(BaseRune):
    crit_rate = 0
    crit_damage = 0


class CritDamageRuneO1(BaseRune):
    crit_rate = 0.07
    crit_damage = 0.24


class CritDamageRuneO2(BaseRune):
    crit_rate = 0
    crit_damage = 0


class CritDamageRuneO3(BaseRune):
    crit_rate = 0
    crit_damage = 0


class CritDamageRuneO4(BaseRune):
    crit_rate = 0
    crit_damage = 0


class CritDamageRuneR1(BaseRune):
    crit_rate = 0
    crit_damage = 0


class CritDamageRuneR2(BaseRune):
    crit_rate = 0.13
    crit_damage = 0.44


class HpRuneB1(BaseRune):
    hp = 450
    atk_bonus = 0
    hp_bonus = 0


class HpRuneB2(BaseRune):
    hp = 582
    atk_bonus = 0
    hp_bonus = 0


class HpRuneG1(BaseRune):
    hp = 880
    atk_bonus = 0
    hp_bonus = 0


class HpRuneG2(BaseRune):
    hp = 1120
    atk_bonus = 0
    hp_bonus = 0


class HpRuneY1(BaseRune):
    hp = 1480
    atk_bonus = 0
    hp_bonus = 0.07


class HpRuneY2(BaseRune):
    hp = 1960
    atk_bonus = 0
    hp_bonus = 0.08


class HpRuneY3(BaseRune):
    hp = 2440
    atk_bonus = 0
    hp_bonus = 0.09


class HpRuneP1(BaseRune):
    hp = 0
    atk_bonus = 0
    hp_bonus = 0


class HpRuneP2(BaseRune):
    hp = 0
    atk_bonus = 0
    hp_bonus = 0


class HpRuneP3(BaseRune):
    hp = 4120
    atk_bonus = 0
    hp_bonus = 0.15


class HpRuneO1(BaseRune):
    hp = 0
    atk_bonus = 0
    hp_bonus = 0


class HpRuneO2(BaseRune):
    hp = 0
    atk_bonus = 0
    hp_bonus = 0


class HpRuneO3(BaseRune):
    hp = 6120
    atk_bonus = 0
    hp_bonus = 0.22


class HpRuneO4(BaseRune):
    hp = 0
    atk_bonus = 0
    hp_bonus = 0


class HpRuneR1(BaseRune):
    hp = 0
    atk_bonus = 0
    hp_bonus = 0


class HpRuneR2(BaseRune):
    hp = 8960
    atk_bonus = 0.06
    hp_bonus = 0.25


@dataclass
class AccuracyRune:
    B1 = AccuracyRuneB1()
    B2 = AccuracyRuneB2()
    G1 = AccuracyRuneG1()
    G2 = AccuracyRuneG2()
    Y1 = AccuracyRuneY1()
    Y2 = AccuracyRuneY2()
    Y3 = AccuracyRuneY3()
    P1 = AccuracyRuneP1()
    P2 = AccuracyRuneP2()
    P3 = AccuracyRuneP3()
    O1 = AccuracyRuneO1()
    O2 = AccuracyRuneO2()
    O3 = AccuracyRuneO3()
    O4 = AccuracyRuneO4()
    R1 = AccuracyRuneR1()
    R2 = AccuracyRuneR2()


accuracy_rune_from_request = {
    'BLUE1': AccuracyRune.B1,
    'BLUE2': AccuracyRune.B2,
    'GREEN1': AccuracyRune.G1,
    'GREEN2': AccuracyRune.G2,
    'YELLOW1': AccuracyRune.Y1,
    'YELLOW2': AccuracyRune.Y2,
    'YELLOW3': AccuracyRune.Y3,
    'PURPLE1': AccuracyRune.P1,
    'PURPLE2': AccuracyRune.P2,
    'PURPLE3': AccuracyRune.P3,
    'ORANGE1': AccuracyRune.O1,
    'ORANGE2': AccuracyRune.O2,
    'ORANGE3': AccuracyRune.O3,
    'ORANGE4': AccuracyRune.O4,
    'RED1': AccuracyRune.R1,
    'RED2': AccuracyRune.R2
}


@dataclass
class CritRateRune:
    B1 = CritRateRuneB1()
    B2 = CritRateRuneB2()
    G1 = CritRateRuneG1()
    G2 = CritRateRuneG2()
    Y1 = CritRateRuneY1()
    Y2 = CritRateRuneY2()
    Y3 = CritRateRuneY3()
    P1 = CritRateRuneP1()
    P2 = CritRateRuneP2()
    P3 = CritRateRuneP3()
    O1 = CritRateRuneO1()
    O2 = CritRateRuneO2()
    O3 = CritRateRuneO3()
    O4 = CritRateRuneO4()
    R1 = CritRateRuneR1()
    R2 = CritRateRuneR2()


crit_rate_rune_from_request = {
    'BLUE1': CritRateRune.B1,
    'BLUE2': CritRateRune.B2,
    'GREEN1': CritRateRune.G1,
    'GREEN2': CritRateRune.G2,
    'YELLOW1': CritRateRune.Y1,
    'YELLOW2': CritRateRune.Y2,
    'YELLOW3': CritRateRune.Y3,
    'PURPLE1': CritRateRune.P1,
    'PURPLE2': CritRateRune.P2,
    'PURPLE3': CritRateRune.P3,
    'ORANGE1': CritRateRune.O1,
    'ORANGE2': CritRateRune.O2,
    'ORANGE3': CritRateRune.O3,
    'ORANGE4': CritRateRune.O4,
    'RED1': CritRateRune.R1,
    'RED2': CritRateRune.R2
}


@dataclass
class AttackRune:
    B1 = AttackRuneB1()
    B2 = AttackRuneB2()
    G1 = AttackRuneG1()
    G2 = AttackRuneG2()
    Y1 = AttackRuneY1()
    Y2 = AttackRuneY2()
    Y3 = AttackRuneY3()
    P1 = AttackRuneP1()
    P2 = AttackRuneP2()
    P3 = AttackRuneP3()
    O1 = AttackRuneO1()
    O2 = AttackRuneO2()
    O3 = AttackRuneO3()
    O4 = AttackRuneO4()
    R1 = AttackRuneR1()
    R2 = AttackRuneR2()


attack_rune_from_request = {
    'BLUE1': AttackRune.B1,
    'BLUE2': AttackRune.B2,
    'GREEN1': AttackRune.G1,
    'GREEN2': AttackRune.G2,
    'YELLOW1': AttackRune.Y1,
    'YELLOW2': AttackRune.Y2,
    'YELLOW3': AttackRune.Y3,
    'PURPLE1': AttackRune.P1,
    'PURPLE2': AttackRune.P2,
    'PURPLE3': AttackRune.P3,
    'ORANGE1': AttackRune.O1,
    'ORANGE2': AttackRune.O2,
    'ORANGE3': AttackRune.O3,
    'ORANGE4': AttackRune.O4,
    'RED1': AttackRune.R1,
    'RED2': AttackRune.R2
}


@dataclass
class EvasionRune:
    B1 = EvasionRuneB1()
    B2 = EvasionRuneB2()
    G1 = EvasionRuneG1()
    G2 = EvasionRuneG2()
    Y1 = EvasionRuneY1()
    Y2 = EvasionRuneY2()
    Y3 = EvasionRuneY3()
    P1 = EvasionRuneP1()
    P2 = EvasionRuneP2()
    P3 = EvasionRuneP3()
    O1 = EvasionRuneO1()
    O2 = EvasionRuneO2()
    O3 = EvasionRuneO3()
    O4 = EvasionRuneO4()
    R1 = EvasionRuneR1()
    R2 = EvasionRuneR2()


evasion_rune_from_request = {
    'BLUE1': EvasionRune.B1,
    'BLUE2': EvasionRune.B2,
    'GREEN1': EvasionRune.G1,
    'GREEN2': EvasionRune.G2,
    'YELLOW1': EvasionRune.Y1,
    'YELLOW2': EvasionRune.Y2,
    'YELLOW3': EvasionRune.Y3,
    'PURPLE1': EvasionRune.P1,
    'PURPLE2': EvasionRune.P2,
    'PURPLE3': EvasionRune.P3,
    'ORANGE1': EvasionRune.O1,
    'ORANGE2': EvasionRune.O2,
    'ORANGE3': EvasionRune.O3,
    'ORANGE4': EvasionRune.O4,
    'RED1': EvasionRune.R1,
    'RED2': EvasionRune.R2
}


@dataclass
class ArmorBreakRune:
    B1 = ArmorBreakRuneB1()
    B2 = ArmorBreakRuneB2()
    G1 = ArmorBreakRuneG1()
    G2 = ArmorBreakRuneG2()
    Y1 = ArmorBreakRuneY1()
    Y2 = ArmorBreakRuneY2()
    Y3 = ArmorBreakRuneY3()
    P1 = ArmorBreakRuneP1()
    P2 = ArmorBreakRuneP2()
    P3 = ArmorBreakRuneP3()
    O1 = ArmorBreakRuneO1()
    O2 = ArmorBreakRuneO2()
    O3 = ArmorBreakRuneO3()
    O4 = ArmorBreakRuneO4()
    R1 = ArmorBreakRuneR1()
    R2 = ArmorBreakRuneR2()


armor_break_rune_from_request = {
    'BLUE1': ArmorBreakRune.B1,
    'BLUE2': ArmorBreakRune.B2,
    'GREEN1': ArmorBreakRune.G1,
    'GREEN2': ArmorBreakRune.G2,
    'YELLOW1': ArmorBreakRune.Y1,
    'YELLOW2': ArmorBreakRune.Y2,
    'YELLOW3': ArmorBreakRune.Y3,
    'PURPLE1': ArmorBreakRune.P1,
    'PURPLE2': ArmorBreakRune.P2,
    'PURPLE3': ArmorBreakRune.P3,
    'ORANGE1': ArmorBreakRune.O1,
    'ORANGE2': ArmorBreakRune.O2,
    'ORANGE3': ArmorBreakRune.O3,
    'ORANGE4': ArmorBreakRune.O4,
    'RED1': ArmorBreakRune.R1,
    'RED2': ArmorBreakRune.R2
}


@dataclass
class SkillDamageRune:
    B1 = SkillDamageRuneB1()
    B2 = SkillDamageRuneB2()
    G1 = SkillDamageRuneG1()
    G2 = SkillDamageRuneG2()
    Y1 = SkillDamageRuneY1()
    Y2 = SkillDamageRuneY2()
    Y3 = SkillDamageRuneY3()
    P1 = SkillDamageRuneP1()
    P2 = SkillDamageRuneP2()
    P3 = SkillDamageRuneP3()
    O1 = SkillDamageRuneO1()
    O2 = SkillDamageRuneO2()
    O3 = SkillDamageRuneO3()
    O4 = SkillDamageRuneO4()
    R1 = SkillDamageRuneR1()
    R2 = SkillDamageRuneR2()


skill_damage_rune_from_request = {
    'BLUE1': SkillDamageRune.B1,
    'BLUE2': SkillDamageRune.B2,
    'GREEN1': SkillDamageRune.G1,
    'GREEN2': SkillDamageRune.G2,
    'YELLOW1': SkillDamageRune.Y1,
    'YELLOW2': SkillDamageRune.Y2,
    'YELLOW3': SkillDamageRune.Y3,
    'PURPLE1': SkillDamageRune.P1,
    'PURPLE2': SkillDamageRune.P2,
    'PURPLE3': SkillDamageRune.P3,
    'ORANGE1': SkillDamageRune.O1,
    'ORANGE2': SkillDamageRune.O2,
    'ORANGE3': SkillDamageRune.O3,
    'ORANGE4': SkillDamageRune.O4,
    'RED1': SkillDamageRune.R1,
    'RED2': SkillDamageRune.R2
}


@dataclass
class CritDamageRune:
    B1 = CritDamageRuneB1()
    B2 = CritDamageRuneB2()
    G1 = CritDamageRuneG1()
    G2 = CritDamageRuneG2()
    Y1 = CritDamageRuneY1()
    Y2 = CritDamageRuneY2()
    Y3 = CritDamageRuneY3()
    P1 = CritDamageRuneP1()
    P2 = CritDamageRuneP2()
    P3 = CritDamageRuneP3()
    O1 = CritDamageRuneO1()
    O2 = CritDamageRuneO2()
    O3 = CritDamageRuneO3()
    O4 = CritDamageRuneO4()
    R1 = CritDamageRuneR1()
    R2 = CritDamageRuneR2()


crit_damage_rune_from_request = {
    'BLUE1': CritDamageRune.B1,
    'BLUE2': CritDamageRune.B2,
    'GREEN1': CritDamageRune.G1,
    'GREEN2': CritDamageRune.G2,
    'YELLOW1': CritDamageRune.Y1,
    'YELLOW2': CritDamageRune.Y2,
    'YELLOW3': CritDamageRune.Y3,
    'PURPLE1': CritDamageRune.P1,
    'PURPLE2': CritDamageRune.P2,
    'PURPLE3': CritDamageRune.P3,
    'ORANGE1': CritDamageRune.O1,
    'ORANGE2': CritDamageRune.O2,
    'ORANGE3': CritDamageRune.O3,
    'ORANGE4': CritDamageRune.O4,
    'RED1': CritDamageRune.R1,
    'RED2': CritDamageRune.R2
}


@dataclass
class HpRune:
    B1 = HpRuneB1()
    B2 = HpRuneB2()
    G1 = HpRuneG1()
    G2 = HpRuneG2()
    Y1 = HpRuneY1()
    Y2 = HpRuneY2()
    Y3 = HpRuneY3()
    P1 = HpRuneP1()
    P2 = HpRuneP2()
    P3 = HpRuneP3()
    O1 = HpRuneO1()
    O2 = HpRuneO2()
    O3 = HpRuneO3()
    O4 = HpRuneO4()
    R1 = HpRuneR1()
    R2 = HpRuneR2()


hp_rune_from_request = {
    'BLUE1': HpRune.B1,
    'BLUE2': HpRune.B2,
    'GREEN1': HpRune.G1,
    'GREEN2': HpRune.G2,
    'YELLOW1': HpRune.Y1,
    'YELLOW2': HpRune.Y2,
    'YELLOW3': HpRune.Y3,
    'PURPLE1': HpRune.P1,
    'PURPLE2': HpRune.P2,
    'PURPLE3': HpRune.P3,
    'ORANGE1': HpRune.O1,
    'ORANGE2': HpRune.O2,
    'ORANGE3': HpRune.O3,
    'ORANGE4': HpRune.O4,
    'RED1': HpRune.R1,
    'RED2': HpRune.R2
}


@dataclass
class Rune:
    empty = EmptyRune()
    accuracy = AccuracyRune
    crit_rate = CritRateRune
    attack = AttackRune
    evasion = EvasionRune
    armor_break = ArmorBreakRune
    skill_damage = SkillDamageRune
    crit_damage = CritDamageRune
    hp = HpRune


rune_from_request = {
    'EMPTY': Rune.empty,
    'ACCURACY': accuracy_rune_from_request,
    'CRIT_RATE': crit_rate_rune_from_request,
    'ATTACK': attack_rune_from_request,
    'EVASION': evasion_rune_from_request,
    'ARMOR_BREAK': armor_break_rune_from_request,
    'SKILL_DAMAGE': skill_damage_rune_from_request,
    'CRIT_DAMAGE': crit_damage_rune_from_request,
    'HP': hp_rune_from_request
}


## Artifact
class BaseArtifact:
    energy = 0
    atk = 0
    hp = 0
    speed = 0
    atk_bonus = 0
    hp_bonus = 0
    hit_rate = 0
    true_damage = 0
    damage_reduction = 0
    damage_to_warriors = 0
    damage_to_assassins = 0
    damage_to_wanderers = 0
    damage_to_clerics = 0
    damage_to_mages = 0
    skill_damage_if_alliance = 0
    skill_damage_if_undead = 0
    skill_damage_if_hell = 0
    crit_rate_if_horde = 0
    crit_rate_if_elf = 0
    true_damage_if_heaven = 0


class EmptyArtifact(BaseArtifact):
    pass


class WarriorArtifactG1(BaseArtifact):
    atk = 150
    damage_to_warriors = 0.05


class WarriorArtifactG2(BaseArtifact):
    atk = 195
    damage_to_warriors = 0.065


class WarriorArtifactG3(BaseArtifact):
    atk = 240
    damage_to_warriors = 0.08


class WarriorArtifactG4(BaseArtifact):
    atk = 300
    damage_to_warriors = 0.1


class WarriorArtifactB1(BaseArtifact):
    atk = 240
    damage_to_warriors = 0.08


class WarriorArtifactB2(BaseArtifact):
    atk = 300
    damage_to_warriors = 0.1


class WarriorArtifactB3(BaseArtifact):
    atk = 360
    damage_to_warriors = 0.12


class WarriorArtifactB4(BaseArtifact):
    atk = 450
    damage_to_warriors = 0.15


class WarriorArtifactY1(BaseArtifact):
    atk = 360
    damage_to_warriors = 0.12


class WarriorArtifactY2(BaseArtifact):
    atk = 420
    damage_to_warriors = 0.14


class WarriorArtifactY3(BaseArtifact):
    atk = 480
    damage_to_warriors = 0.16


class WarriorArtifactY4(BaseArtifact):
    atk = 540
    damage_to_warriors = 0.18


class WarriorArtifactY5(BaseArtifact):
    atk = 600
    damage_to_warriors = 0.2


class WarriorArtifactP1(BaseArtifact):
    atk = 0
    damage_to_warriors = 0


class WarriorArtifactP2(BaseArtifact):
    atk = 0
    damage_to_warriors = 0


class WarriorArtifactP3(BaseArtifact):
    atk = 0
    damage_to_warriors = 0


class WarriorArtifactP4(BaseArtifact):
    atk = 0
    damage_to_warriors = 0


class WarriorArtifactP5(BaseArtifact):
    atk = 840
    damage_to_warriors = 0.28


class WarriorArtifactO1(BaseArtifact):
    atk = 0
    damage_to_warriors = 0


class WarriorArtifactO2(BaseArtifact):
    atk = 0
    damage_to_warriors = 0


class WarriorArtifactO3(BaseArtifact):
    atk = 0
    damage_to_warriors = 0


class WarriorArtifactO4(BaseArtifact):
    atk = 0
    damage_to_warriors = 0


class WarriorArtifactO5(BaseArtifact):
    atk = 0
    damage_to_warriors = 0


class WarriorArtifactO6(BaseArtifact):
    atk = 1280
    damage_to_warriors = 0.42


class AssassinArtifactG1(BaseArtifact):
    atk = 150
    damage_to_assassins = 0.05


class AssassinArtifactG2(BaseArtifact):
    atk = 195
    damage_to_assassins = 0.065


class AssassinArtifactG3(BaseArtifact):
    atk = 240
    damage_to_assassins = 0.08


class AssassinArtifactG4(BaseArtifact):
    atk = 300
    damage_to_assassins = 0.1


class AssassinArtifactB1(BaseArtifact):
    atk = 240
    damage_to_assassins = 0.08


class AssassinArtifactB2(BaseArtifact):
    atk = 300
    damage_to_assassins = 0.1


class AssassinArtifactB3(BaseArtifact):
    atk = 360
    damage_to_assassins = 0.12


class AssassinArtifactB4(BaseArtifact):
    atk = 450
    damage_to_assassins = 0.15


class AssassinArtifactY1(BaseArtifact):
    atk = 360
    damage_to_assassins = 0.12


class AssassinArtifactY2(BaseArtifact):
    atk = 420
    damage_to_assassins = 0.14


class AssassinArtifactY3(BaseArtifact):
    atk = 480
    damage_to_assassins = 0.16


class AssassinArtifactY4(BaseArtifact):
    atk = 540
    damage_to_assassins = 0.18


class AssassinArtifactY5(BaseArtifact):
    atk = 600
    damage_to_assassins = 0.2


class AssassinArtifactP1(BaseArtifact):
    atk = 0
    damage_to_assassins = 0


class AssassinArtifactP2(BaseArtifact):
    atk = 0
    damage_to_assassins = 0


class AssassinArtifactP3(BaseArtifact):
    atk = 0
    damage_to_assassins = 0


class AssassinArtifactP4(BaseArtifact):
    atk = 0
    damage_to_assassins = 0


class AssassinArtifactP5(BaseArtifact):
    atk = 840
    damage_to_assassins = 0.28


class AssassinArtifactO1(BaseArtifact):
    atk = 0
    damage_to_assassins = 0


class AssassinArtifactO2(BaseArtifact):
    atk = 0
    damage_to_assassins = 0


class AssassinArtifactO3(BaseArtifact):
    atk = 0
    damage_to_assassins = 0


class AssassinArtifactO4(BaseArtifact):
    atk = 0
    damage_to_assassins = 0


class AssassinArtifactO5(BaseArtifact):
    atk = 0
    damage_to_assassins = 0


class AssassinArtifactO6(BaseArtifact):
    atk = 1280
    damage_to_assassins = 0.42


class WandererArtifactG1(BaseArtifact):
    atk = 150
    damage_to_wanderers = 0.05


class WandererArtifactG2(BaseArtifact):
    atk = 195
    damage_to_wanderers = 0.065


class WandererArtifactG3(BaseArtifact):
    atk = 240
    damage_to_wanderers = 0.08


class WandererArtifactG4(BaseArtifact):
    atk = 300
    damage_to_wanderers = 0.1


class WandererArtifactB1(BaseArtifact):
    atk = 240
    damage_to_wanderers = 0.08


class WandererArtifactB2(BaseArtifact):
    atk = 300
    damage_to_wanderers = 0.1


class WandererArtifactB3(BaseArtifact):
    atk = 360
    damage_to_wanderers = 0.12


class WandererArtifactB4(BaseArtifact):
    atk = 450
    damage_to_wanderers = 0.15


class WandererArtifactY1(BaseArtifact):
    atk = 360
    damage_to_wanderers = 0.12


class WandererArtifactY2(BaseArtifact):
    atk = 420
    damage_to_wanderers = 0.14


class WandererArtifactY3(BaseArtifact):
    atk = 480
    damage_to_wanderers = 0.16


class WandererArtifactY4(BaseArtifact):
    atk = 540
    damage_to_wanderers = 0.18


class WandererArtifactY5(BaseArtifact):
    atk = 600
    damage_to_wanderers = 0.2


class WandererArtifactP1(BaseArtifact):
    atk = 0
    damage_to_wanderers = 0


class WandererArtifactP2(BaseArtifact):
    atk = 0
    damage_to_wanderers = 0


class WandererArtifactP3(BaseArtifact):
    atk = 0
    damage_to_wanderers = 0


class WandererArtifactP4(BaseArtifact):
    atk = 0
    damage_to_wanderers = 0


class WandererArtifactP5(BaseArtifact):
    atk = 840
    damage_to_wanderers = 0.28


class WandererArtifactO1(BaseArtifact):
    atk = 0
    damage_to_wanderers = 0


class WandererArtifactO2(BaseArtifact):
    atk = 0
    damage_to_wanderers = 0


class WandererArtifactO3(BaseArtifact):
    atk = 0
    damage_to_wanderers = 0


class WandererArtifactO4(BaseArtifact):
    atk = 0
    damage_to_wanderers = 0


class WandererArtifactO5(BaseArtifact):
    atk = 0
    damage_to_wanderers = 0


class WandererArtifactO6(BaseArtifact):
    atk = 1280
    damage_to_wanderers = 0.42


class ClericArtifactG1(BaseArtifact):
    atk = 150
    damage_to_clerics = 0.05


class ClericArtifactG2(BaseArtifact):
    atk = 195
    damage_to_clerics = 0.065


class ClericArtifactG3(BaseArtifact):
    atk = 240
    damage_to_clerics = 0.08


class ClericArtifactG4(BaseArtifact):
    atk = 300
    damage_to_clerics = 0.1


class ClericArtifactB1(BaseArtifact):
    atk = 240
    damage_to_clerics = 0.08


class ClericArtifactB2(BaseArtifact):
    atk = 300
    damage_to_clerics = 0.1


class ClericArtifactB3(BaseArtifact):
    atk = 360
    damage_to_clerics = 0.12


class ClericArtifactB4(BaseArtifact):
    atk = 450
    damage_to_clerics = 0.15


class ClericArtifactY1(BaseArtifact):
    atk = 360
    damage_to_clerics = 0.12


class ClericArtifactY2(BaseArtifact):
    atk = 420
    damage_to_clerics = 0.14


class ClericArtifactY3(BaseArtifact):
    atk = 480
    damage_to_clerics = 0.16


class ClericArtifactY4(BaseArtifact):
    atk = 540
    damage_to_clerics = 0.18


class ClericArtifactY5(BaseArtifact):
    atk = 600
    damage_to_clerics = 0.2


class ClericArtifactP1(BaseArtifact):
    atk = 0
    damage_to_clerics = 0


class ClericArtifactP2(BaseArtifact):
    atk = 0
    damage_to_clerics = 0


class ClericArtifactP3(BaseArtifact):
    atk = 0
    damage_to_clerics = 0


class ClericArtifactP4(BaseArtifact):
    atk = 0
    damage_to_clerics = 0


class ClericArtifactP5(BaseArtifact):
    atk = 840
    damage_to_clerics = 0.28


class ClericArtifactO1(BaseArtifact):
    atk = 0
    damage_to_clerics = 0


class ClericArtifactO2(BaseArtifact):
    atk = 0
    damage_to_clerics = 0


class ClericArtifactO3(BaseArtifact):
    atk = 0
    damage_to_clerics = 0


class ClericArtifactO4(BaseArtifact):
    atk = 0
    damage_to_clerics = 0


class ClericArtifactO5(BaseArtifact):
    atk = 0
    damage_to_clerics = 0


class ClericArtifactO6(BaseArtifact):
    atk = 1280
    damage_to_clerics = 0.42


class MageArtifactG1(BaseArtifact):
    atk = 150
    damage_to_mages = 0.05


class MageArtifactG2(BaseArtifact):
    atk = 195
    damage_to_mages = 0.065


class MageArtifactG3(BaseArtifact):
    atk = 240
    damage_to_mages = 0.08


class MageArtifactG4(BaseArtifact):
    atk = 300
    damage_to_mages = 0.1


class MageArtifactB1(BaseArtifact):
    atk = 240
    damage_to_mages = 0.08


class MageArtifactB2(BaseArtifact):
    atk = 300
    damage_to_mages = 0.1


class MageArtifactB3(BaseArtifact):
    atk = 360
    damage_to_mages = 0.12


class MageArtifactB4(BaseArtifact):
    atk = 450
    damage_to_mages = 0.15


class MageArtifactY1(BaseArtifact):
    atk = 360
    damage_to_mages = 0.12


class MageArtifactY2(BaseArtifact):
    atk = 420
    damage_to_mages = 0.14


class MageArtifactY3(BaseArtifact):
    atk = 480
    damage_to_mages = 0.16


class MageArtifactY4(BaseArtifact):
    atk = 540
    damage_to_mages = 0.18


class MageArtifactY5(BaseArtifact):
    atk = 600
    damage_to_mages = 0.2


class MageArtifactP1(BaseArtifact):
    atk = 0
    damage_to_mages = 0


class MageArtifactP2(BaseArtifact):
    atk = 0
    damage_to_mages = 0


class MageArtifactP3(BaseArtifact):
    atk = 0
    damage_to_mages = 0


class MageArtifactP4(BaseArtifact):
    atk = 0
    damage_to_mages = 0


class MageArtifactP5(BaseArtifact):
    atk = 840
    damage_to_mages = 0.28


class MageArtifactO1(BaseArtifact):
    atk = 0
    damage_to_mages = 0


class MageArtifactO2(BaseArtifact):
    atk = 0
    damage_to_mages = 0


class MageArtifactO3(BaseArtifact):
    atk = 0
    damage_to_mages = 0


class MageArtifactO4(BaseArtifact):
    atk = 0
    damage_to_mages = 0


class MageArtifactO5(BaseArtifact):
    atk = 0
    damage_to_mages = 0


class MageArtifactO6(BaseArtifact):
    atk = 1280
    damage_to_mages = 0.42


class EyeOfHeavenO1(BaseArtifact):
    atk_bonus = 0
    hit_rate = 0


class EyeOfHeavenO2(BaseArtifact):
    atk_bonus = 0
    hit_rate = 0


class EyeOfHeavenO3(BaseArtifact):
    atk_bonus = 0
    hit_rate = 0


class EyeOfHeavenO4(BaseArtifact):
    atk_bonus = 0
    hit_rate = 0


class EyeOfHeavenO5(BaseArtifact):
    atk_bonus = 0
    hit_rate = 0


class EyeOfHeavenO6(BaseArtifact):
    atk_bonus = 0.12
    hit_rate = 0.08


class WindWalkerO1(BaseArtifact):
    speed = 0
    hp_bonus = 0


class WindWalkerO2(BaseArtifact):
    speed = 0
    hp_bonus = 0


class WindWalkerO3(BaseArtifact):
    speed = 0
    hp_bonus = 0


class WindWalkerO4(BaseArtifact):
    speed = 0
    hp_bonus = 0


class WindWalkerO5(BaseArtifact):
    speed = 0
    hp_bonus = 0


class WindWalkerO6(BaseArtifact):
    speed = 42
    hp_bonus = 0.1


class ScorchingSunO1(BaseArtifact):
    hp_bonus = 0
    damage_reduction = 0


class ScorchingSunO2(BaseArtifact):
    hp_bonus = 0
    damage_reduction = 0


class ScorchingSunO3(BaseArtifact):
    hp_bonus = 0
    damage_reduction = 0


class ScorchingSunO4(BaseArtifact):
    hp_bonus = 0
    damage_reduction = 0


class ScorchingSunO5(BaseArtifact):
    hp_bonus = 0
    damage_reduction = 0


class ScorchingSunO6(BaseArtifact):
    hp_bonus = 0.08
    damage_reduction = 0.12


class DragonbloodO1(BaseArtifact):
    atk_bonus = 0
    true_damage = 0


class DragonbloodO2(BaseArtifact):
    atk_bonus = 0
    true_damage = 0


class DragonbloodO3(BaseArtifact):
    atk_bonus = 0
    true_damage = 0


class DragonbloodO4(BaseArtifact):
    atk_bonus = 0
    true_damage = 0


class DragonbloodO5(BaseArtifact):
    atk_bonus = 0
    true_damage = 0


class DragonbloodO6(BaseArtifact):
    atk_bonus = 0.08
    true_damage = 0.12


class SoundStepO1(BaseArtifact):
    energy = 0
    atk = 0


class SoundStepO2(BaseArtifact):
    energy = 0
    atk = 0


class SoundStepO3(BaseArtifact):
    energy = 0
    atk = 0


class SoundStepO4(BaseArtifact):
    energy = 0
    atk = 0


class SoundStepO5(BaseArtifact):
    energy = 0
    atk = 0


class SoundStepO6(BaseArtifact):
    energy = 240
    atk = 240


class KnightsVowO1(BaseArtifact):
    atk = 0
    damage_to_clerics = 0
    skill_damage_if_alliance = 0


class KnightsVowO2(BaseArtifact):
    atk = 0
    damage_to_clerics = 0
    skill_damage_if_alliance = 0


class KnightsVowO3(BaseArtifact):
    atk = 0
    damage_to_clerics = 0
    skill_damage_if_alliance = 0


class KnightsVowO4(BaseArtifact):
    atk = 0
    damage_to_clerics = 0
    skill_damage_if_alliance = 0


class KnightsVowO5(BaseArtifact):
    atk = 0
    damage_to_clerics = 0
    skill_damage_if_alliance = 0


class KnightsVowO6(BaseArtifact):
    atk = 1280
    damage_to_clerics = 0.42
    skill_damage_if_alliance = 0.25


class PrimevalSoulO1(BaseArtifact):
    atk = 0
    damage_to_wanderers = 0
    crit_rate_if_horde = 0


class PrimevalSoulO2(BaseArtifact):
    atk = 0
    damage_to_wanderers = 0
    crit_rate_if_horde = 0


class PrimevalSoulO3(BaseArtifact):
    atk = 0
    damage_to_wanderers = 0
    crit_rate_if_horde = 0


class PrimevalSoulO4(BaseArtifact):
    atk = 0
    damage_to_wanderers = 0
    crit_rate_if_horde = 0


class PrimevalSoulO5(BaseArtifact):
    atk = 0
    damage_to_wanderers = 0
    crit_rate_if_horde = 0


class PrimevalSoulO6(BaseArtifact):
    atk = 1280
    damage_to_wanderers = 0.42
    crit_rate_if_horde = 0.09


class QueensCrownO1(BaseArtifact):
    speed = 0
    hp_bonus = 0
    crit_rate_if_elf = 0


class QueensCrownO2(BaseArtifact):
    speed = 0
    hp_bonus = 0
    crit_rate_if_elf = 0


class QueensCrownO3(BaseArtifact):
    speed = 0
    hp_bonus = 0
    crit_rate_if_elf = 0


class QueensCrownO4(BaseArtifact):
    speed = 0
    hp_bonus = 0
    crit_rate_if_elf = 0


class QueensCrownO5(BaseArtifact):
    speed = 0
    hp_bonus = 0
    crit_rate_if_elf = 0


class QueensCrownO6(BaseArtifact):
    speed = 42
    hp_bonus = 0.1
    crit_rate_if_elf = 0.09


class SoulTorrentO1(BaseArtifact):
    atk_bonus = 0
    hit_rate = 0
    skill_damage_if_undead = 0


class SoulTorrentO2(BaseArtifact):
    atk_bonus = 0
    hit_rate = 0
    skill_damage_if_undead = 0


class SoulTorrentO3(BaseArtifact):
    atk_bonus = 0
    hit_rate = 0
    skill_damage_if_undead = 0


class SoulTorrentO4(BaseArtifact):
    atk_bonus = 0
    hit_rate = 0
    skill_damage_if_undead = 0


class SoulTorrentO5(BaseArtifact):
    atk_bonus = 0
    hit_rate = 0
    skill_damage_if_undead = 0


class SoulTorrentO6(BaseArtifact):
    atk_bonus = 0.12
    hit_rate = 0.08
    skill_damage_if_undead = 0.25


class GiftOfCreationO1(BaseArtifact):
    hp_bonus = 0
    damage_reduction = 0
    true_damage_if_heaven = 0


class GiftOfCreationO2(BaseArtifact):
    hp_bonus = 0
    damage_reduction = 0
    true_damage_if_heaven = 0


class GiftOfCreationO3(BaseArtifact):
    hp_bonus = 0
    damage_reduction = 0
    true_damage_if_heaven = 0


class GiftOfCreationO4(BaseArtifact):
    hp_bonus = 0
    damage_reduction = 0
    true_damage_if_heaven = 0


class GiftOfCreationO5(BaseArtifact):
    hp_bonus = 0
    damage_reduction = 0
    true_damage_if_heaven = 0


class GiftOfCreationO6(BaseArtifact):
    hp_bonus = 0.1
    damage_reduction = 0.15
    true_damage_if_heaven = 0.12


class EternalCurseO1(BaseArtifact):
    atk_bonus = 0
    hit_rate = 0
    skill_damage_if_hell = 0


class EternalCurseO2(BaseArtifact):
    atk_bonus = 0
    hit_rate = 0
    skill_damage_if_hell = 0


class EternalCurseO3(BaseArtifact):
    atk_bonus = 0.075
    hit_rate = 0.05
    skill_damage_if_hell = 0.25


class EternalCurseO4(BaseArtifact):
    atk_bonus = 0.09
    hit_rate = 0.06
    skill_damage_if_hell = 0.25


class EternalCurseO5(BaseArtifact):
    atk_bonus = 0.105
    hit_rate = 0.07
    skill_damage_if_hell = 0.25


class EternalCurseO6(BaseArtifact):
    atk_bonus = 0.12
    hit_rate = 0.08
    skill_damage_if_hell = 0.25


@dataclass
class WarriorArtifact:
    G1 = WarriorArtifactG1()
    G2 = WarriorArtifactG2()
    G3 = WarriorArtifactG3()
    G4 = WarriorArtifactG4()
    B1 = WarriorArtifactB1()
    B2 = WarriorArtifactB2()
    B3 = WarriorArtifactB3()
    B4 = WarriorArtifactB4()
    Y1 = WarriorArtifactY1()
    Y2 = WarriorArtifactY2()
    Y3 = WarriorArtifactY3()
    Y4 = WarriorArtifactY4()
    Y5 = WarriorArtifactY5()
    P1 = WarriorArtifactP1()
    P2 = WarriorArtifactP2()
    P3 = WarriorArtifactP3()
    P4 = WarriorArtifactP4()
    P5 = WarriorArtifactP5()
    O1 = WarriorArtifactO1()
    O2 = WarriorArtifactO2()
    O3 = WarriorArtifactO3()
    O4 = WarriorArtifactO4()
    O5 = WarriorArtifactO5()
    O6 = WarriorArtifactO6()


satans_power_artifact_from_request = {
    1: WarriorArtifact.O1,
    2: WarriorArtifact.O2,
    3: WarriorArtifact.O3,
    4: WarriorArtifact.O4,
    5: WarriorArtifact.O5,
    6: WarriorArtifact.O6
}


@dataclass
class AssassinArtifact:
    G1 = AssassinArtifactG1()
    G2 = AssassinArtifactG2()
    G3 = AssassinArtifactG3()
    G4 = AssassinArtifactG4()
    B1 = AssassinArtifactB1()
    B2 = AssassinArtifactB2()
    B3 = AssassinArtifactB3()
    B4 = AssassinArtifactB4()
    Y1 = AssassinArtifactY1()
    Y2 = AssassinArtifactY2()
    Y3 = AssassinArtifactY3()
    Y4 = AssassinArtifactY4()
    Y5 = AssassinArtifactY5()
    P1 = AssassinArtifactP1()
    P2 = AssassinArtifactP2()
    P3 = AssassinArtifactP3()
    P4 = AssassinArtifactP4()
    P5 = AssassinArtifactP5()
    O1 = AssassinArtifactO1()
    O2 = AssassinArtifactO2()
    O3 = AssassinArtifactO3()
    O4 = AssassinArtifactO4()
    O5 = AssassinArtifactO5()
    O6 = AssassinArtifactO6()


yaksha_artifact_from_request = {
    1: AssassinArtifact.O1,
    2: AssassinArtifact.O2,
    3: AssassinArtifact.O3,
    4: AssassinArtifact.O4,
    5: AssassinArtifact.O5,
    6: AssassinArtifact.O6
}


@dataclass
class WandererArtifact:
    G1 = WandererArtifactG1()
    G2 = WandererArtifactG2()
    G3 = WandererArtifactG3()
    G4 = WandererArtifactG4()
    B1 = WandererArtifactB1()
    B2 = WandererArtifactB2()
    B3 = WandererArtifactB3()
    B4 = WandererArtifactB4()
    Y1 = WandererArtifactY1()
    Y2 = WandererArtifactY2()
    Y3 = WandererArtifactY3()
    Y4 = WandererArtifactY4()
    Y5 = WandererArtifactY5()
    P1 = WandererArtifactP1()
    P2 = WandererArtifactP2()
    P3 = WandererArtifactP3()
    P4 = WandererArtifactP4()
    P5 = WandererArtifactP5()
    O1 = WandererArtifactO1()
    O2 = WandererArtifactO2()
    O3 = WandererArtifactO3()
    O4 = WandererArtifactO4()
    O5 = WandererArtifactO5()
    O6 = WandererArtifactO6()


dark_destroyer_artifact_from_request = {
    1: WandererArtifact.O1,
    2: WandererArtifact.O2,
    3: WandererArtifact.O3,
    4: WandererArtifact.O4,
    5: WandererArtifact.O5,
    6: WandererArtifact.O6
}


@dataclass
class ClericArtifact:
    G1 = ClericArtifactG1()
    G2 = ClericArtifactG2()
    G3 = ClericArtifactG3()
    G4 = ClericArtifactG4()
    B1 = ClericArtifactB1()
    B2 = ClericArtifactB2()
    B3 = ClericArtifactB3()
    B4 = ClericArtifactB4()
    Y1 = ClericArtifactY1()
    Y2 = ClericArtifactY2()
    Y3 = ClericArtifactY3()
    Y4 = ClericArtifactY4()
    Y5 = ClericArtifactY5()
    P1 = ClericArtifactP1()
    P2 = ClericArtifactP2()
    P3 = ClericArtifactP3()
    P4 = ClericArtifactP4()
    P5 = ClericArtifactP5()
    O1 = ClericArtifactO1()
    O2 = ClericArtifactO2()
    O3 = ClericArtifactO3()
    O4 = ClericArtifactO4()
    O5 = ClericArtifactO5()
    O6 = ClericArtifactO6()


suns_hymn_artifact_from_request = {
    1: ClericArtifact.O1,
    2: ClericArtifact.O2,
    3: ClericArtifact.O3,
    4: ClericArtifact.O4,
    5: ClericArtifact.O5,
    6: ClericArtifact.O6
}


@dataclass
class MageArtifact:
    G1 = MageArtifactG1()
    G2 = MageArtifactG2()
    G3 = MageArtifactG3()
    G4 = MageArtifactG4()
    B1 = MageArtifactB1()
    B2 = MageArtifactB2()
    B3 = MageArtifactB3()
    B4 = MageArtifactB4()
    Y1 = MageArtifactY1()
    Y2 = MageArtifactY2()
    Y3 = MageArtifactY3()
    Y4 = MageArtifactY4()
    Y5 = MageArtifactY5()
    P1 = MageArtifactP1()
    P2 = MageArtifactP2()
    P3 = MageArtifactP3()
    P4 = MageArtifactP4()
    P5 = MageArtifactP5()
    O1 = MageArtifactO1()
    O2 = MageArtifactO2()
    O3 = MageArtifactO3()
    O4 = MageArtifactO4()
    O5 = MageArtifactO5()
    O6 = MageArtifactO6()


burning_soul_artifact_from_request = {
    1: MageArtifact.O1,
    2: MageArtifact.O2,
    3: MageArtifact.O3,
    4: MageArtifact.O4,
    5: MageArtifact.O5,
    6: MageArtifact.O6
}


@dataclass
class EyeOfHeaven:
    O1 = EyeOfHeavenO1()
    O2 = EyeOfHeavenO2()
    O3 = EyeOfHeavenO3()
    O4 = EyeOfHeavenO4()
    O5 = EyeOfHeavenO5()
    O6 = EyeOfHeavenO6()


eye_of_heaven_artifact_from_request = {
    1: EyeOfHeaven.O1,
    2: EyeOfHeaven.O2,
    3: EyeOfHeaven.O3,
    4: EyeOfHeaven.O4,
    5: EyeOfHeaven.O5,
    6: EyeOfHeaven.O6
}


@dataclass
class WindWalker:
    O1 = WindWalkerO1()
    O2 = WindWalkerO2()
    O3 = WindWalkerO3()
    O4 = WindWalkerO4()
    O5 = WindWalkerO5()
    O6 = WindWalkerO6()


wind_walker_artifact_from_request = {
    1: WindWalker.O1,
    2: WindWalker.O2,
    3: WindWalker.O3,
    4: WindWalker.O4,
    5: WindWalker.O5,
    6: WindWalker.O6
}


@dataclass
class ScorchingSun:
    O1 = ScorchingSunO1()
    O2 = ScorchingSunO2()
    O3 = ScorchingSunO3()
    O4 = ScorchingSunO4()
    O5 = ScorchingSunO5()
    O6 = ScorchingSunO6()


scorching_sun_artifact_from_request = {
    1: ScorchingSun.O1,
    2: ScorchingSun.O2,
    3: ScorchingSun.O3,
    4: ScorchingSun.O4,
    5: ScorchingSun.O5,
    6: ScorchingSun.O6
}


@dataclass
class Dragonblood:
    O1 = DragonbloodO1()
    O2 = DragonbloodO2()
    O3 = DragonbloodO3()
    O4 = DragonbloodO4()
    O5 = DragonbloodO5()
    O6 = DragonbloodO6()


dragonblood_artifact_from_request = {
    1: Dragonblood.O1,
    2: Dragonblood.O2,
    3: Dragonblood.O3,
    4: Dragonblood.O4,
    5: Dragonblood.O5,
    6: Dragonblood.O6
}


@dataclass
class SoundStep:
    O1 = SoundStepO1()
    O2 = SoundStepO2()
    O3 = SoundStepO3()
    O4 = SoundStepO4()
    O5 = SoundStepO5()
    O6 = SoundStepO6()


sound_step_artifact_from_request = {
    1: SoundStep.O1,
    2: SoundStep.O2,
    3: SoundStep.O3,
    4: SoundStep.O4,
    5: SoundStep.O5,
    6: SoundStep.O6
}


@dataclass
class KnightsVow:
    O1 = KnightsVowO1()
    O2 = KnightsVowO2()
    O3 = KnightsVowO3()
    O4 = KnightsVowO4()
    O5 = KnightsVowO5()
    O6 = KnightsVowO6()


knights_vow_artifact_from_request = {
    1: KnightsVow.O1,
    2: KnightsVow.O2,
    3: KnightsVow.O3,
    4: KnightsVow.O4,
    5: KnightsVow.O5,
    6: KnightsVow.O6
}


@dataclass
class PrimevalSoul:
    O1 = PrimevalSoulO1()
    O2 = PrimevalSoulO2()
    O3 = PrimevalSoulO3()
    O4 = PrimevalSoulO4()
    O5 = PrimevalSoulO5()
    O6 = PrimevalSoulO6()


primeval_soul_artifact_from_request = {
    1: PrimevalSoul.O1,
    2: PrimevalSoul.O2,
    3: PrimevalSoul.O3,
    4: PrimevalSoul.O4,
    5: PrimevalSoul.O5,
    6: PrimevalSoul.O6
}


@dataclass
class QueensCrown:
    O1 = QueensCrownO1()
    O2 = QueensCrownO2()
    O3 = QueensCrownO3()
    O4 = QueensCrownO4()
    O5 = QueensCrownO5()
    O6 = QueensCrownO6()


queens_crown_artifact_from_request = {
    1: QueensCrown.O1,
    2: QueensCrown.O2,
    3: QueensCrown.O3,
    4: QueensCrown.O4,
    5: QueensCrown.O5,
    6: QueensCrown.O6
}


@dataclass
class SoulTorrent:
    O1 = SoulTorrentO1()
    O2 = SoulTorrentO2()
    O3 = SoulTorrentO3()
    O4 = SoulTorrentO4()
    O5 = SoulTorrentO5()
    O6 = SoulTorrentO6()


soul_torrent_artifact_from_request = {
    1: SoulTorrent.O1,
    2: SoulTorrent.O2,
    3: SoulTorrent.O3,
    4: SoulTorrent.O4,
    5: SoulTorrent.O5,
    6: SoulTorrent.O6
}


@dataclass
class GiftOfCreation:
    O1 = GiftOfCreationO1()
    O2 = GiftOfCreationO2()
    O3 = GiftOfCreationO3()
    O4 = GiftOfCreationO4()
    O5 = GiftOfCreationO5()
    O6 = GiftOfCreationO6()


gift_of_creation_artifact_from_request = {
    1: GiftOfCreation.O1,
    2: GiftOfCreation.O2,
    3: GiftOfCreation.O3,
    4: GiftOfCreation.O4,
    5: GiftOfCreation.O5,
    6: GiftOfCreation.O6
}


@dataclass
class EternalCurse:
    O1 = EternalCurseO1()
    O2 = EternalCurseO2()
    O3 = EternalCurseO3()
    O4 = EternalCurseO4()
    O5 = EternalCurseO5()
    O6 = EternalCurseO6()


eternal_curse_artifact_from_request = {
    1: EternalCurse.O1,
    2: EternalCurse.O2,
    3: EternalCurse.O3,
    4: EternalCurse.O4,
    5: EternalCurse.O5,
    6: EternalCurse.O6
}


@dataclass
class Artifact:
    empty = EmptyArtifact()
    warrior = WarriorArtifact
    assassin = AssassinArtifact
    wanderer = WandererArtifact
    cleric = ClericArtifact
    mage = MageArtifact
    eye_of_heaven = EyeOfHeaven
    wind_walker = WindWalker
    scorching_sun = ScorchingSun
    dragonblood = Dragonblood
    sound_step = SoundStep
    knights_vow = KnightsVow
    primeval_soul = PrimevalSoul
    queens_crown = QueensCrown
    soul_torrent = SoulTorrent
    gift_of_creation = GiftOfCreation
    eternal_curse = EternalCurse


artifact_from_request = {
    'EMPTY': Artifact.empty,
    'SATANS_POWER': satans_power_artifact_from_request,
    'YAKSHA': yaksha_artifact_from_request,
    'DARK_DESTROYER': dark_destroyer_artifact_from_request,
    'SUNS_HYMN': suns_hymn_artifact_from_request,
    'BURNING_SOUL': burning_soul_artifact_from_request,
    'EYE_OF_HEAVEN': eye_of_heaven_artifact_from_request,
    'WIND_WALKER': wind_walker_artifact_from_request,
    'SCORCHING_SUN': scorching_sun_artifact_from_request,
    'DRAGONBLOOD': dragonblood_artifact_from_request,
    'SOUND_STEP': sound_step_artifact_from_request,
    'KNIGHTS_VOW': knights_vow_artifact_from_request,
    'PRIMEVAL_SOUL': primeval_soul_artifact_from_request,
    'QUEENS_CROWN': queens_crown_artifact_from_request,
    'SOUL_TORRENT': soul_torrent_artifact_from_request,
    'GIFT_OF_CREATION': gift_of_creation_artifact_from_request,
    'ETERNAL_CURSE': eternal_curse_artifact_from_request
}


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


## Familiar
class BaseFamiliar:
    crit_rate = 0
    crit_damage = 0
    skill_damage = 0
    hit_rate = 0
    true_damage = 0
    dodge = 0
    speed = 0

    is_dead = False

    def __init__(self, skill_1):
        self.energy = 0

        self.n_targets = 2
        if skill_1 > 30:
            self.n_targets = 3
        if skill_1 > 60:
            self.n_targets = 4
        self.damage = 700
        self.damage += min(skill_1, 10) * 300
        if skill_1 > 10:
            self.damage += min(skill_1 - 10, 10) * 400
        if skill_1 > 20:
            self.damage += min(skill_1 - 20, 10) * 500
        if skill_1 > 30:
            self.damage += min(skill_1 - 30, 10) * 800
        if skill_1 > 40:
            self.damage += min(skill_1 - 40, 10) * 1000
        if skill_1 > 50:
            self.damage += min(skill_1 - 50, 10) * 1200
        if skill_1 > 60:
            self.damage += min(skill_1 - 60, 10) * 1600
        if skill_1 > 70:
            self.damage += min(skill_1 - 70, 10) * 2000
        if skill_1 > 80:
            self.damage += min(skill_1 - 80, 10) * 2400
        if skill_1 > 90:
            self.damage += min(skill_1 - 90, 10) * 3000
        if skill_1 > 100:
            self.damage += min(skill_1 - 100, 10) * 3600
        if skill_1 > 110:
            self.damage += min(skill_1 - 110, 10) * 4200

    def turn(self):
        if self.energy == 100:
            self.attack()
            self.energy = 0

        self.energy = max(min(self.energy + 25, 100), self.energy)

    def attack(self):
        targets = targets_at_random(self.op_team.heroes, self.n_targets)
        damage_components = {'Power': self.damage,
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
                             'Total damage': self.damage}
        for target in targets:  # check : can be dodged?
            target.hp -= self.damage
            action = Action.hit(self, target, damage_components, self.skill_name)
            action.text = '\n{} takes {} damage from {} ({})' \
                .format(target.str_id, self.damage, self.str_id, self.skill_name)
            self.game.actions.append(action)

            self.stats['damage_by_skill'][self.skill_name] += self.damage
            self.stats['damage_by_target'][target.str_id] += self.damage
            target.stats['damage_taken_by_skill'][self.skill_name] += self.damage
            target.stats['damage_taken_by_source'][self.str_id] += self.damage

        for target in targets:
            target.has_taken_damage(self)


class EmptyFamiliar(BaseFamiliar):
    name = 'Empty_Familiar'

    def __init__(self):
        super().__init__(0)

    def turn(self):
        self.energy = 0


class Edison(BaseFamiliar):
    name = 'Edison'
    skill_name = "Thundergod's wrath"

    def __init__(self, level, skill_1, skill_2, skill_3, skill_4):
        self.level = level
        self.pet_crit_rate = skill_2 * 0.005
        self.pet_crit_damage = skill_3 * 0.01
        self.pet_speed = skill_4 * 2
        super().__init__(skill_1)


class Vinci(BaseFamiliar):
    name = 'Vinci'
    skill_name = 'Chaotic storm'

    def __init__(self, level, skill_1, skill_2, skill_3, skill_4):
        self.level = level
        self.pet_skill_damage = skill_2 * 0.01
        self.pet_hit_rate = skill_3 * 0.005
        self.pet_speed = skill_4 * 2
        super().__init__(skill_1)


class Raphael(BaseFamiliar):
    name = 'Raphael'
    skill_name = 'Bloom doom'

    def __init__(self, level, skill_1, skill_2, skill_3, skill_4):
        self.level = level
        self.pet_true_damage = skill_2 * 0.01
        self.pet_dodge = skill_3 * 0.005
        self.pet_speed = skill_4 * 2
        super().__init__(skill_1)


@dataclass
class Familiar:
    empty = EmptyFamiliar()
    edison = Edison
    vinci = Vinci
    raphael = Raphael


familiar_from_request = {
    'EMPTY': Familiar.empty,
    'EDISON': Familiar.edison, 
    'VINCI': Familiar.vinci,
    'RAPHAEL': Familiar.raphael
}

## Effects
effect_id = 0


class BaseEffect:
    def __init__(self):
        global effect_id
        self.id = effect_id
        self.percentage = False
        if self.name == 'War Frenzy':
            self.percentage = True
        effect_id += 1

    def kill(self):
        self.holder.effects = [e for e in self.holder.effects if e.id != self.id]


class StatUp(BaseEffect):
    def __init__(self, source, holder, up, turns, name='', passive=False):
        self.source = source
        self.holder = holder
        self.up = up
        self.turns = turns
        self.name = name
        self.verbose = False if passive else True
        self.has_been_set = False
        self.infinite = False
        if self.turns is None:
            self.turns = 1000
            self.infinite = True
        super().__init__()


class StatDown(BaseEffect):
    def __init__(self, source, holder, down, turns, name='', passive=False):
        self.source = source
        self.holder = holder
        self.down = down
        self.turns = turns
        self.name = name
        self.verbose = False if passive else True
        self.has_been_set = False
        self.infinite = False
        if self.turns is None:
            self.turns = 1000
            self.infinite = True
        super().__init__()


class Dot(BaseEffect):
    def __init__(self, source, holder, power, turns, name=''):
        self.source = source
        self.holder = holder
        self.power = power
        self.turns = turns
        self.name = name
        super().__init__()

    def tick(self):
        if not self.holder.is_dead:
            damage_components = self.source.compute_damage(self.holder, self.power)
            dmg = damage_components['Total damage']
            crit = True if damage_components['Crit damage'] > 0 else False
            crit_str = ', crit' if crit else ''

            self.holder.hp -= dmg
            self.turns -= 1
            action = Action.dot(self.source, self.holder, damage_components, self.turns, self.name)
            action.text = '\n{} takes {} damage (dot from {} ({}{}), {} turns left)' \
                .format(self.holder.str_id, round(dmg), self.source.str_id, self.name, crit_str, self.turns)
            self.source.game.actions.append(action)

            self.source.stats['damage_by_skill'][self.name] += dmg
            self.source.stats['damage_by_target'][self.holder.str_id] += dmg
            self.holder.stats['damage_taken_by_skill'][self.name] += dmg
            self.holder.stats['damage_taken_by_source'][self.source.str_id] += dmg

            self.holder.has_taken_damage(self.source)


class Heal(BaseEffect):
    def __init__(self, source, holder, power, turns, name=''):
        self.source = source
        self.holder = holder
        self.power = power
        self.turns = turns
        self.name = name
        self.hot = True if self.turns > 1 else False
        super().__init__()

    def tick(self):
        if not self.holder.is_dead:
            effective_healing = min(self.power, self.holder.hp_max - self.holder.hp)
            self.holder.hp += effective_healing
            self.source.stats['effective_healing_by_skill'][self.name] += effective_healing
            self.source.stats['effective_healing_by_target'][self.holder.str_id] += effective_healing
            self.holder.stats['effective_healing_taken_by_skill'][self.name] += effective_healing
            self.holder.stats['effective_healing_taken_by_source'][self.source.str_id] += effective_healing
            self.source.stats['healing_by_skill'][self.name] += self.power
            self.source.stats['healing_by_target'][self.holder.str_id] += self.power
            self.holder.stats['healing_taken_by_skill'][self.name] += self.power
            self.holder.stats['healing_taken_by_source'][self.source.str_id] += self.power

            self.turns -= 1
            if self.hot:
                action = Action.hot(self.source, self.holder, self.power, self.turns, self.name)
                action.text = '\n{} is healed {} by {} ({}, {} turns left)' \
                    .format(self.holder.str_id, round(self.power),
                            self.source.str_id, self.name, self.turns)
            else:
                action = Action.heal(self.source, self.holder, self.power, self.name)
                action.text = '\n{} is healed {} by {} ({})' \
                    .format(self.holder.str_id, round(self.power),
                            self.source.str_id, self.name)
            self.source.game.actions.append(action)

            self.holder.has_been_healed(self.source)


class Poison(BaseEffect):
    def __init__(self, source, holder, power, turns, name=''):
        self.source = source
        self.holder = holder
        self.power = power
        self.turns = turns
        self.name = name
        super().__init__()

    def tick(self):
        if not self.holder.is_dead:
            damage_components = self.source.compute_damage(self.holder, self.power)
            dmg = damage_components['Total damage']
            crit = True if damage_components['Crit damage'] > 0 else False
            crit_str = ', crit' if crit else ''

            self.holder.hp -= dmg
            self.turns -= 1
            action = Action.poison(self.source, self.holder, damage_components, self.turns, self.name)
            action.text = '\n{} takes {} damage (poison from {} ({}{}), {} turns left)' \
                .format(self.holder.str_id, round(dmg), self.source.str_id, self.name, crit_str, self.turns)
            self.source.game.actions.append(action)

            self.source.stats['damage_by_skill'][self.name] += dmg
            self.source.stats['damage_by_target'][self.holder.str_id] += dmg
            self.holder.stats['damage_taken_by_skill'][self.name] += dmg
            self.holder.stats['damage_taken_by_source'][self.source.str_id] += dmg

            self.holder.has_taken_damage(self.source)


class Bleed(BaseEffect):
    def __init__(self, source, holder, power, turns, name=''):
        self.source = source
        self.holder = holder
        self.power = power
        self.turns = turns
        self.name = name
        super().__init__()

    def tick(self):
        if not self.holder.is_dead:
            damage_components = self.source.compute_damage(self.holder, self.power)
            dmg = damage_components['Total damage']
            crit = True if damage_components['Crit damage'] > 0 else False
            crit_str = ', crit' if crit else ''

            self.holder.hp -= dmg
            self.turns -= 1
            action = Action.bleed(self.source, self.holder, damage_components, self.turns, self.name)
            action.text = '\n{} takes {} damage (bleed from {} ({}{}), {} turns left)' \
                .format(self.holder.str_id, round(dmg), self.source.str_id, self.name, crit_str, self.turns)
            self.source.game.actions.append(action)

            self.source.stats['damage_by_skill'][self.name] += dmg
            self.source.stats['damage_by_target'][self.holder.str_id] += dmg
            self.holder.stats['damage_taken_by_skill'][self.name] += dmg
            self.holder.stats['damage_taken_by_source'][self.source.str_id] += dmg

            self.holder.has_taken_damage(self.source)


class TimedMark(BaseEffect):
    def __init__(self, source, holder, power, turns, name=''):
        self.source = source
        self.holder = holder
        self.power = power
        self.turns = turns + 2
        self.first_turn = True
        self.name = name
        super().__init__()

    def tick(self):
        if not self.holder.is_dead:
            self.turns -= 1
            if self.turns == 0:
                self.trigger()
            elif self.first_turn:
                self.first_turn = False
                action = Action.timed_mark_on(self.source, self.holder, self.turns - 1, self.name)
                action.text = '\n{} has a timed mark from {} ({}, {} turns)' \
                    .format(self.holder.str_id, self.source.str_id, self.name, self.turns - 1)
                self.source.game.actions.append(action)
            else:
                action = Action.timed_mark_countdown(self.source, self.holder, self.turns, self.name)
                action.text = '\n{} has a timed mark from {} ({}, {} turns left)' \
                    .format(self.holder.str_id, self.source.str_id, self.name, self.turns)
                self.source.game.actions.append(action)

    def trigger(self):
        damage_components = self.source.compute_damage(self.holder, self.power)
        dmg = damage_components['Total damage']
        crit = True if damage_components['Crit damage'] > 0 else False
        crit_str = ', crit' if crit else ''

        self.holder.hp -= dmg
        action = Action.timed_mark_trigger(self.source, self.holder, damage_components, self.name)
        action.text = '\n{} takes {} damage (timed mark from {} ({}{}))' \
            .format(self.holder.str_id, round(dmg), self.source.str_id, self.name, crit_str)
        self.source.game.actions.append(action)

        self.source.stats['damage_by_skill'][self.name] += dmg
        self.source.stats['damage_by_target'][self.holder.str_id] += dmg
        self.holder.stats['damage_taken_by_skill'][self.name] += dmg
        self.holder.stats['damage_taken_by_source'][self.source.str_id] += dmg

        self.holder.has_taken_damage(self.source)


class CritMark(BaseEffect):
    def __init__(self, source, holder, power, name=''):
        self.source = source
        self.holder = holder
        self.power = power
        self.turns = 1000
        self.name = name
        super().__init__()

    def tick(self):
        if not self.holder.is_dead:
            action = Action.crit_mark_on(self.source, self.holder, self.name)
            action.text = '\n{} has a crit mark from {} ({})' \
                .format(self.holder.str_id, self.source.str_id, self.name)
            self.source.game.actions.append(action)

    def trigger(self):
        damage_components = self.source.compute_damage(self.holder, self.power)
        dmg = damage_components['Total damage']
        crit = True if damage_components['Crit damage'] > 0 else False
        crit_str = ', crit' if crit else ''

        self.holder.hp -= dmg
        action = Action.crit_mark_trigger(self.source, self.holder, damage_components, self.name)
        action.text = '\n{} takes {} damage (crit mark from {} ({}{}))' \
            .format(self.holder.str_id, round(dmg), self.source.str_id, self.name, crit_str)
        self.source.game.actions.append(action)

        self.source.stats['damage_by_skill'][self.name] += dmg
        self.source.stats['damage_by_target'][self.holder.str_id] += dmg
        self.holder.stats['damage_taken_by_skill'][self.name] += dmg
        self.holder.stats['damage_taken_by_source'][self.source.str_id] += dmg

        self.holder.has_taken_damage(self.source)

        self.kill()


class Silence(BaseEffect):
    def __init__(self, source, holder, turns, name=''):
        self.source = source
        self.holder = holder
        self.turns = turns
        self.name = name
        super().__init__()

    def tick(self):
        if not self.holder.is_dead:
            self.turns -= 1
            action = Action.silence(self.source, self.holder, self.turns, self.name)
            action.text = '\n{} is silenced by {} ({}), {} turns left' \
                .format(self.holder.str_id, self.source.str_id, self.name, self.turns)
            self.source.game.actions.append(action)


class Stun(BaseEffect):
    def __init__(self, source, holder, turns, name=''):
        self.source = source
        self.holder = holder
        self.turns = turns
        self.name = name
        super().__init__()

    def tick(self):
        if not self.holder.is_dead:
            self.turns -= 1
            action = Action.stun(self.source, self.holder, self.turns, self.name)
            action.text = '\n{} is stunned by {} ({}), {} turns left' \
                .format(self.holder.str_id, self.source.str_id, self.name, self.turns)
            self.source.game.actions.append(action)


class Petrify(BaseEffect):
    def __init__(self, source, holder, turns, name=''):
        self.source = source
        self.holder = holder
        self.turns = turns
        self.name = name
        super().__init__()

    def tick(self):
        if not self.holder.is_dead:
            self.turns -= 1
            action = Action.petrify(self.source, self.holder, self.turns, self.name)
            action.text = '\n{} is petrified by {} ({}), {} turns left' \
                .format(self.holder.str_id, self.source.str_id, self.name, self.turns)
            self.source.game.actions.append(action)


class Freeze(BaseEffect):
    def __init__(self, source, holder, turns, name=''):
        self.source = source
        self.holder = holder
        self.turns = turns
        self.name = name
        super().__init__()

    def tick(self):
        if not self.holder.is_dead:
            self.turns -= 1
            action = Action.freeze(self.source, self.holder, self.turns, self.name)
            action.text = '\n{} is frozen by {} ({}), {} turns left' \
                .format(self.holder.str_id, self.source.str_id, self.name, self.turns)
            self.source.game.actions.append(action)


class AttackUp(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                previous_bonus = self.holder.atk_bonus
                self.holder.atk_bonus += self.up
                self.holder.atk *= (1 + self.holder.atk_bonus) / (1 + previous_bonus)
                self.has_been_set = True

            self.turns -= 1
            action = Action.attack_up(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s attack is increased by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, round(100 * self.up, 1), self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s attack is increased by {}% by {} ({})" \
                    .format(self.holder.str_id, round(100 * self.up, 1), self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        previous_bonus = self.holder.atk_bonus
        self.holder.atk_bonus -= self.up
        self.holder.atk *= (1 + self.holder.atk_bonus) / (1 + previous_bonus)
        super().kill()


class AttackDown(StatDown):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.atk *= 1 - self.down
                self.has_been_set = True

            self.turns -= 1
            action = Action.attack_down(self.source, self.holder, self.down, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s attack is reduced by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s attack is reduced by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.atk /= 1 - self.down
        super().kill()


class HpUp(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                previous_bonus = self.holder.hp_bonus
                self.holder.hp_bonus += self.up
                self.holder.hp *= (1 + self.holder.hp_bonus) / (1 + previous_bonus)
                try:
                    self.holder.hp_max *= (1 + self.holder.hp_bonus) / (1 + previous_bonus)
                except AttributeError:
                    pass
                self.has_been_set = True

            self.turns -= 1
            action = Action.hp_up(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s hp is increased by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s hp is increased by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        previous_bonus = self.holder.hp_bonus
        self.holder.hp_bonus -= self.up
        self.holder.hp *= (1 + self.holder.hp_bonus) / (1 + previous_bonus)
        self.holder.hp_max *= (1 + self.holder.hp_bonus) / (1 + previous_bonus)
        super().kill()


class HpDown(StatDown):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.hp *= 1 - self.down
                self.holder.hp_max *= 1 - self.down
                self.has_been_set = True

            self.turns -= 1
            action = Action.hp_down(self.source, self.holder, self.down, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s hp is reduced by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s hp is reduced by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.hp /= 1 - self.down
        self.holder.hp_max /= 1 - self.down
        super().kill()


class CritRateUp(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.crit_rate += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.crit_rate_up(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s crit rate is increased by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s crit rate is increased by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.crit_rate -= self.up
        super().kill()


class CritRateDown(StatDown):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.crit_rate -= self.down
                self.has_been_set = True

            self.turns -= 1
            action = Action.crit_rate_down(self.source, self.holder, self.down, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s crit rate is reduced by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s crit rate is reduced by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.crit_rate += self.down
        super().kill()


class CritDamageUp(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.crit_damage += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.crit_damage_up(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s crit damage is increased by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s crit damage is increased by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.crit_damage -= self.up
        super().kill()


class CritDamageDown(StatDown):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.crit_damage -= self.down
                self.has_been_set = True

            self.turns -= 1
            action = Action.crit_damage_down(self.source, self.holder, self.down, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s crit damage is reduced by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s crit damage is reduced by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.crit_damage += self.down
        super().kill()


class HitRateUp(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.hit_rate += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.hit_rate_up(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s hit rate is increased by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s hit rate is increased by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.hit_rate -= self.up
        super().kill()


class HitRateDown(StatDown):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.hit_rate -= self.down
                self.has_been_set = True

            self.turns -= 1
            action = Action.hit_rate_down(self.source, self.holder, self.down, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s hit rate is reduced by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s hit rate is reduced by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.hit_rate += self.down
        super().kill()


class DodgeUp(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.dodge += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.dodge_up(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s dodge rate is increased by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s dodge rate is increased by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.dodge -= self.up
        super().kill()


class DodgeDown(StatDown):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.dodge -= self.down
                self.has_been_set = True

            self.turns -= 1
            action = Action.dodge_down(self.source, self.holder, self.down, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s dodge rate is reduced by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s dodge rate is reduced by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.dodge += self.down
        super().kill()


class SkillDamageUp(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.skill_damage += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.skill_damage_up(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s skill damage is increased by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s skill damage is increased by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.skill_damage -= self.up
        super().kill()


class SkillDamageDown(StatDown):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.skill_damage -= self.down
                self.has_been_set = True

            self.turns -= 1
            action = Action.skill_damage_down(self.source, self.holder, self.down, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s skill damage is reduced by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s skill damage is reduced by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.skill_damage += self.down
        super().kill()


class ControlImmuneUp(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.control_immune += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.control_immune_up(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s control resistance is increased by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s control resistance is increased by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.control_immune -= self.up
        super().kill()


class ControlImmuneDown(StatDown):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.control_immune -= self.down
                self.has_been_set = True

            self.turns -= 1
            action = Action.control_immune_down(self.source, self.holder, self.down, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s control resistance is reduced by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s control resistance is reduced by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.down, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.control_immune += self.down
        super().kill()


class SilenceImmuneUp(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.silence_immune += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.silence_immune_up(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s silence resistance is increased by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s silence resistance is increased by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.silence_immune -= self.up
        super().kill()


class DamageReductionUp(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.damage_reduction += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.damage_reduction_up(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s damage reduction is increased by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s damage reduction is increased by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.damage_reduction -= self.up
        super().kill()


class TrueDamageUp(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.true_damage += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.true_damage_up(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s true damage is increased by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s true damage is increased by {}% by {} ({})" \
                    .format(self.holder.str_id, 100 * self.up, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.true_damage -= self.up
        super().kill()


class ArmorBreakUp(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.armor_break += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.armor_break_up(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s armor break is increased by {} by {} ({}), {} turns left" \
                    .format(self.holder.str_id, self.up, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s armor break is increased by {} by {} ({})" \
                    .format(self.holder.str_id, self.up, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.armor_break -= self.up
        super().kill()


class ArmorBreakDown(StatDown):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.armor_break -= self.down
                self.has_been_set = True

            self.turns -= 1
            action = Action.armor_break_down(self.source, self.holder, self.down, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s armor break is reduced by {} by {} ({}), {} turns left" \
                    .format(self.holder.str_id, self.down, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s armor break is reduced by {} by {} ({})" \
                    .format(self.holder.str_id, self.down, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.armor_break += self.down
        super().kill()


class ArmorUp(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.armor += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.armor_up(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s defense is increased by {} by {} ({}), {} turns left" \
                    .format(self.holder.str_id, self.up, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s defense is increased by {} by {} ({})" \
                    .format(self.holder.str_id, self.up, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.armor -= self.up
        super().kill()


class ArmorDown(StatDown):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.armor -= self.down
                self.has_been_set = True

            self.turns -= 1
            action = Action.armor_down(self.source, self.holder, self.down, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s defense is reduced by {} by {} ({}), {} turns left" \
                    .format(self.holder.str_id, self.down, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s defense is reduced by {} by {} ({})" \
                    .format(self.holder.str_id, self.down, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.armor += self.down
        super().kill()


class SpeedUp(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.speed += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.speed_up(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s speed is increased by {} by {} ({}), {} turns left" \
                    .format(self.holder.str_id, self.up, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s speed is increased by {} by {} ({})" \
                    .format(self.holder.str_id, self.up, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.speed -= self.up
        super().kill()


class SpeedDown(StatDown):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.speed -= self.down
                self.has_been_set = True

            self.turns -= 1
            action = Action.speed_down(self.source, self.holder, self.down, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s speed is reduced by {} by {} ({}), {} turns left" \
                    .format(self.holder.str_id, self.down, self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s speed is reduced by {} by {} ({})" \
                    .format(self.holder.str_id, self.down, self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.speed += self.down
        super().kill()


class DamageToBleeding(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.damage_to_bleeding += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.damage_to_bleeding(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = '\n{} deals {}% extra damage to bleeding targets ({} from {}), {} turns left' \
                    .format(self.holder.str_id, 100 * self.up, self.name,
                            self.source.str_id, self.turns) \
                            if self.verbose else ''
            else:
                action.text = '\n{} deals {}% extra damage to bleeding targets ({} from {})' \
                    .format(self.holder.str_id, 100 * self.up, self.name,
                            self.source.str_id) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.damage_to_bleeding -= self.up
        super().kill()


class DamageToPoisoned(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.damage_to_poisoned += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.damage_to_poisoned(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = '\n{} deals {}% extra damage to poisoned targets ({} from {}), {} turns left' \
                    .format(self.holder.str_id, 100 * self.up, self.name,
                            self.source.str_id, self.turns) \
                            if self.verbose else ''
            else:
                action.text = '\n{} deals {}% extra damage to poisoned targets ({} from {})' \
                    .format(self.holder.str_id, 100 * self.up, self.name,
                            self.source.str_id) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.damage_to_poisoned -= self.up
        super().kill()


class DamageToStunned(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.damage_to_stunned += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.damage_to_stunned(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = '\n{} deals {}% extra damage to stunned targets ({} from {}), {} turns left' \
                    .format(self.holder.str_id, 100 * self.up, self.name,
                            self.source.str_id, self.turns) \
                            if self.verbose else ''
            else:
                action.text = '\n{} deals {}% extra damage to stunned targets ({} from {})' \
                    .format(self.holder.str_id, 100 * self.up, self.name,
                            self.source.str_id) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.damage_to_stunned -= self.up
        super().kill()


class DamageToWarriors(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.damage_to_warriors += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.damage_to_warriors(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = '\n{} deals {}% extra damage to warriors ({} from {}), {} turns left' \
                    .format(self.holder.str_id, 100 * self.up, self.name,
                            self.source.str_id, self.turns) \
                            if self.verbose else ''
            else:
                action.text = '\n{} deals {}% extra damage to warriors ({} from {})' \
                    .format(self.holder.str_id, 100 * self.up, self.name,
                            self.source.str_id) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.damage_to_warriors -= self.up
        super().kill()


class HealingUp(StatUp):
    def tick(self):
        self.verbose = self.verbose or self.holder.game.verbose_full
        if not self.holder.is_dead:
            if not self.has_been_set:
                self.holder.healing_bonus += self.up
                self.has_been_set = True

            self.turns -= 1
            action = Action.healing_up(self.source, self.holder, self.up, self.turns, self.name)
            if not self.infinite:
                action.text = "\n{}'s healing is increased by {}% by {} ({}), {} turns left" \
                    .format(self.holder.str_id, round(100 * self.up, 1), self.source.str_id,
                            self.name, self.turns) \
                            if self.verbose else ''
            else:
                action.text = "\n{}'s healing is increased by {}% by {} ({})" \
                    .format(self.holder.str_id, round(100 * self.up, 1), self.source.str_id,
                            self.name) \
                            if self.verbose else ''
            self.source.game.actions.append(action)

    def kill(self):
        self.holder.healing_bonus -= self.up
        super().kill()


@dataclass
class Effect:
    dot = Dot
    heal = Heal
    poison = Poison
    bleed = Bleed
    timed_mark = TimedMark
    crit_mark = CritMark
    silence = Silence
    stun = Stun
    petrify = Petrify
    freeze = Freeze
    attack_up = AttackUp
    attack_down = AttackDown
    hp_up = HpUp
    hp_down = HpDown
    crit_rate_up = CritRateUp
    crit_rate_down = CritRateDown
    crit_damage_up = CritDamageUp
    crit_damage_down = CritDamageDown
    hit_rate_up = HitRateUp
    hit_rate_down = HitRateDown
    dodge_up = DodgeUp
    dodge_down = DodgeDown
    skill_damage_up = SkillDamageUp
    skill_damage_down = SkillDamageDown
    control_immune_up = ControlImmuneUp
    control_immune_down = ControlImmuneDown
    silence_immune_up = SilenceImmuneUp
    damage_reduction_up = DamageReductionUp
    true_damage_up = TrueDamageUp
    armor_break_up = ArmorBreakUp
    armor_break_down = ArmorBreakDown
    armor_up = ArmorUp
    armor_down = ArmorDown
    speed_up = SpeedUp
    speed_down = SpeedDown
    damage_to_bleeding = DamageToBleeding
    damage_to_poisoned = DamageToPoisoned
    damage_to_stunned = DamageToStunned
    damage_to_warriors = DamageToWarriors
    healing_up = HealingUp


## Actions
class BaseAction:
    text = ''


class HitAction(BaseAction):
    def __init__(self, attacker, target, damage_components, name):
        self.attacker = attacker
        self.target = target
        self.damage_components = damage_components
        self.name = name


class DodgeAction(BaseAction):
    def __init__(self, attacker, target, name):
        self.attacker = attacker
        self.target = target
        self.name = name


class IsControlledAction(BaseAction):
    def __init__(self, source, target, turns_left, name):
        self.source = source
        self.target = target
        self.name = name
        self.turns_left = turns_left


class IsStunnedAction(IsControlledAction):
    pass


class IsPetrifiedAction(IsControlledAction):
    pass


class IsFrozenAction(IsControlledAction):
    pass


class IsSilencedAction(IsControlledAction):
    pass


class HealAction(BaseAction):
    def __init__(self, source, target, heal, name):
        self.source = source
        self.target = target
        self.heal = heal
        self.name = name


class HotAction(BaseAction):
    def __init__(self, source, target, heal, turns_left, name):
        self.source = source
        self.target = target
        self.heal = heal
        self.name = name
        self.turns_left = turns_left


class DotAction(BaseAction):
    def __init__(self, source, target, damage_components, turns_left, name):
        self.source = source
        self.target = target
        self.damage_components = damage_components
        self.name = name
        self.turns_left = turns_left


class PoisonAction(DotAction):
    pass


class BleedAction(DotAction):
    pass


class TimedMarkOnAction(BaseAction):
    def __init__(self, source, target, turns, name):
        self.source = source
        self.target = target
        self.name = name
        self.turns = turns


class TimedMarkCountdownAction(BaseAction):
    def __init__(self, source, target, turns_left, name):
        self.source = source
        self.target = target
        self.name = name
        self.turns_left = turns_left


class TimedMarkTriggerAction(BaseAction):
    def __init__(self, source, target, damage_components, name):
        self.source = source
        self.target = target
        self.damage_components = damage_components
        self.name = name


class CritMarkOnAction(BaseAction):
    def __init__(self, source, target, name):
        self.source = source
        self.target = target
        self.name = name


class CritMarkTriggerAction(BaseAction):
    def __init__(self, source, target, damage_components, name):
        self.source = source
        self.target = target
        self.damage_components = damage_components
        self.name = name


class ControlAction(BaseAction):
    def __init__(self, source, target, turns_left, name):
        self.source = source
        self.target = target
        self.name = name
        self.turns_left = turns_left


class StunAction(ControlAction):
    pass


class PetrifyAction(ControlAction):
    pass


class FreezeAction(ControlAction):
    pass


class SilenceAction(ControlAction):
    pass


class CleanseAction(BaseAction):
    def __init__(self, source, target, name):
        self.source = source
        self.target = target
        self.name = name


class StatUpAction(BaseAction):
    def __init__(self, source, target, up, turns_left, name):
        self.source = source
        self.target = target
        self.up = up
        self.name = name
        self.turns_left = turns_left
        self.infinite = True if self.turns_left > 100 else False


class StatDownAction(BaseAction):
    def __init__(self, source, target, down, turns_left, name):
        self.source = source
        self.target = target
        self.down = down
        self.name = name
        self.turns_left = turns_left
        self.infinite = True if self.turns_left > 100 else False


class AttackUpAction(StatUpAction):
    pass


class AttackDownAction(StatDownAction):
    pass


class HpUpAction(StatUpAction):
    pass


class HpDownAction(StatDownAction):
    pass


class CritRateUpAction(StatUpAction):
    pass


class CritRateDownAction(StatDownAction):
    pass


class CritDamageUpAction(StatUpAction):
    pass


class CritDamageDownAction(StatDownAction):
    pass


class HitRateUpAction(StatUpAction):
    pass


class HitRateDownAction(StatDownAction):
    pass


class DodgeUpAction(StatUpAction):
    pass


class DodgeDownAction(StatDownAction):
    pass


class SkillDamageUpAction(StatUpAction):
    pass


class SkillDamageDownAction(StatDownAction):
    pass


class ControlImmuneUpAction(StatUpAction):
    pass


class ControlImmuneDownAction(StatDownAction):
    pass


class SilenceImmuneUpAction(StatUpAction):
    pass


class DamageReductionUpAction(StatUpAction):
    pass


class TrueDamageUpAction(StatUpAction):
    pass


class ArmorBreakUpAction(StatUpAction):
    pass


class ArmorBreakDownAction(StatDownAction):
    pass


class ArmorUpAction(StatUpAction):
    pass


class ArmorDownAction(StatDownAction):
    pass


class SpeedUpAction(StatUpAction):
    pass


class SpeedDownAction(StatDownAction):
    pass


class DamageToBleedingAction(StatUpAction):
    pass


class DamageToPoisonedAction(StatUpAction):
    pass


class DamageToStunnedAction(StatUpAction):
    pass


class DamageToWarriorsAction(StatUpAction):
    pass


class HealingUpAction(StatUpAction):
    pass


class EnergyUpAction:
    def __init__(self, source, target, up, passive, name):
        self.source = source
        self.target = target
        self.up = up
        self.name = name
        self.passive = passive


class EnergyDownAction:
    def __init__(self, source, target, down, passive, name):
        self.source = source
        self.target = target
        self.down = down
        self.name = name
        self.passive = passive


class DieAction:
    def __init__(self, hero):
        self.hero = hero


@dataclass
class Action:
    hit = HitAction
    dodge = DodgeAction
    is_stunned = IsStunnedAction
    is_petrified = IsPetrifiedAction
    is_frozen = IsFrozenAction
    is_silenced = IsSilencedAction
    heal = HealAction
    hot = HotAction
    dot = DotAction
    poison = PoisonAction
    bleed = BleedAction
    timed_mark_on = TimedMarkOnAction
    timed_mark_countdown = TimedMarkCountdownAction
    timed_mark_trigger = TimedMarkTriggerAction
    crit_mark_on = CritMarkOnAction
    crit_mark_trigger = CritMarkTriggerAction
    silence = SilenceAction
    stun = StunAction
    petrify = PetrifyAction
    freeze = FreezeAction
    cleanse = CleanseAction
    attack_up = AttackUpAction
    attack_down = AttackDownAction
    hp_up = HpUpAction
    hp_down = HpDownAction
    crit_rate_up = CritRateUpAction
    crit_rate_down = CritRateDownAction
    crit_damage_up = CritDamageUpAction
    crit_damage_down = CritDamageDownAction
    hit_rate_up = HitRateUpAction
    hit_rate_down = HitRateDownAction
    dodge_up = DodgeUpAction
    dodge_down = DodgeDownAction
    skill_damage_up = SkillDamageUpAction
    skill_damage_down = SkillDamageDownAction
    control_immune_up = ControlImmuneUpAction
    control_immune_down = ControlImmuneDownAction
    silence_immune_up = SilenceImmuneUpAction
    damage_reduction_up = DamageReductionUpAction
    true_damage_up = TrueDamageUpAction
    armor_break_up = ArmorBreakUpAction
    armor_break_down = ArmorBreakDownAction
    armor_up = ArmorUpAction
    armor_down = ArmorDownAction
    speed_up = SpeedUpAction
    speed_down = SpeedDownAction
    energy_up = EnergyUpAction
    energy_down = EnergyDownAction
    damage_to_bleeding = DamageToBleedingAction
    damage_to_poisoned = DamageToPoisonedAction
    damage_to_stunned = DamageToStunnedAction
    damage_to_warriors = DamageToWarriorsAction
    healing_up = HealingUpAction
    die = DieAction
