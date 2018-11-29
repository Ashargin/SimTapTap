import connexion
import six
import sys

sys.path.append('../')

from swagger_server.models.hero_stats import HeroStats  # noqa: E501
from swagger_server.models.simulate_request import SimulateRequest  # noqa: E501
from swagger_server.models.stat_request import StatRequest  # noqa: E501
from swagger_server.models.hero_stats import HeroStats  # noqa: E501
from swagger_server.models.hero_stats_stats import HeroStatsStats  # noqa: E501
from swagger_server import util
from sim.heroes import Hero, Team
from sim.sim import Sim,Game
from sim.models import armor_from_request, helmet_from_request, weapon_from_request, pendant_from_request, rune_from_request, artifact_from_request, familiar_from_request
from sim.heroes import hero_from_request


def battle_simulate_post(simulate_request=None):  # noqa: E501
    """Simulates a given number of battles

     # noqa: E501

    :param count: number of battles to be simulated
    :type count: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        simulate_request = SimulateRequest.from_dict(connexion.request.get_json())  # noqa: E501
        #attacker
        attack_player = simulate_request.attacker.player
        attack_heroes = [
                get_hero_from_request(simulate_request.attacker.hero_front1, attack_player),
                get_hero_from_request(simulate_request.attacker.hero_front2, attack_player),
                get_hero_from_request(simulate_request.attacker.hero_front3, attack_player),
                get_hero_from_request(simulate_request.attacker.hero_rear1, attack_player),
                get_hero_from_request(simulate_request.attacker.hero_rear2, attack_player),
                get_hero_from_request(simulate_request.attacker.hero_rear3, attack_player)
                ]
        attack_familiar_request = simulate_request.attacker.player.active_pet
        attack_familiar = familiar_from_request[attack_familiar_request.id](attack_familiar_request.level,attack_familiar_request.skill1level, attack_familiar_request.skill2level, attack_familiar_request.skill3level, attack_familiar_request.skill4level)
        attack_team = Team(attack_heroes, attack_familiar)
        #defender
        defense_player = simulate_request.defender.player
        defense_heroes = [
                get_hero_from_request(simulate_request.defender.hero_front1, defense_player),
                get_hero_from_request(simulate_request.defender.hero_front2, defense_player),
                get_hero_from_request(simulate_request.defender.hero_front3, defense_player),
                get_hero_from_request(simulate_request.defender.hero_rear1, defense_player),
                get_hero_from_request(simulate_request.defender.hero_rear2, defense_player),
                get_hero_from_request(simulate_request.defender.hero_rear3, defense_player)
                ]
        defense_familiar_request = simulate_request.defender.player.active_pet
        defense_familiar = familiar_from_request[defense_familiar_request.id](defense_familiar_request.level,defense_familiar_request.skill1level, defense_familiar_request.skill2level, defense_familiar_request.skill3level, defense_familiar_request.skill4level)
        defense_team = Team(defense_heroes, defense_familiar)
        game = Game(attack_team, defense_team)
        game.process()
        return game.log.text
    return 'empty request'


def get_hero_from_request(request_hero, player):
    chest = armor_from_request[request_hero.equipment.chest]
    helmet = helmet_from_request[request_hero.equipment.helmet]
    pendant = pendant_from_request[request_hero.equipment.pendant]
    weapon = weapon_from_request[request_hero.equipment.weapon]
    rune = rune_from_request[request_hero.equipment.rune.rune_type][request_hero.equipment.rune.level]
    artifact = artifact_from_request[request_hero.equipment.artifact.id][request_hero.equipment.artifact.stars]
    guild_tech = [
            [
                player.guild_tech.warrior.tier1,
                player.guild_tech.assassin.tier1,
                player.guild_tech.wanderer.tier1,
                player.guild_tech.cleric.tier1,
                player.guild_tech.mage.tier1,
                ],
            [
                player.guild_tech.warrior.tier2,
                player.guild_tech.assassin.tier2,
                player.guild_tech.wanderer.tier2,
                player.guild_tech.cleric.tier2,
                player.guild_tech.mage.tier2,
                ],
            [
                player.guild_tech.warrior.tier3,
                player.guild_tech.assassin.tier3,
                player.guild_tech.wanderer.tier3,
                player.guild_tech.cleric.tier3,
                player.guild_tech.mage.tier3,
                ],
            [
                player.guild_tech.warrior.tier4,
                player.guild_tech.assassin.tier4,
                player.guild_tech.wanderer.tier4,
                player.guild_tech.cleric.tier4,
                player.guild_tech.mage.tier4,
                ],
            [
                player.guild_tech.warrior.tier5,
                player.guild_tech.assassin.tier5,
                player.guild_tech.wanderer.tier5,
                player.guild_tech.cleric.tier5,
                player.guild_tech.mage.tier5,
                ]
            ]
    familiar_stats = [player.pet_bonus.hp_bonus, player.pet_bonus.attack_bonus]
    return hero_from_request[request_hero.id](star=request_hero.stars, tier=request_hero.tier, level=request_hero.level, armor=chest, helmet=helmet, weapon=weapon, pendant=pendant, rune=rune, artifact=artifact, guild_tech=guild_tech, familiar_stats=familiar_stats)

def calc_stats(StatEnvironment=None):  # noqa: E501
    """calculates stats for the specified hero with the specified equipment

    Calculates stats # noqa: E501

    :param StatEnvironment: stat environment containing desired hero and player progress
    :type StatEnvironment: dict | bytes

    :rtype: List[HeroStats]
    """
    if connexion.request.is_json:
        statEnvironment = StatRequest.from_dict(connexion.request.get_json())  # noqa: E501
        player = statEnvironment.player
        heroStats = list()
        for request_hero in statEnvironment.heroes:
            hero=get_hero_from_request(request_hero, player)
            heroStats.append(HeroStats(hero=request_hero,stats=HeroStatsStats(hero.hp,hero.atk,hero.armor,hero.speed,hero.armor_break,hero.skill_damage,hero.hit_rate,hero.dodge,hero.crit_rate,hero.crit_damage,hero.true_damage,hero.damage_reduction,hero.control_immune)))
        return heroStats
    return 'no heroes'
