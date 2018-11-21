import connexion
import six

from swagger_server.models.hero_stats import HeroStats  # noqa: E501
from swagger_server.models.simulate_request import SimulateRequest  # noqa: E501
from swagger_server.models.stat_request import StatRequest  # noqa: E501
from swagger_server import util
from heroes import Hero

def battle_simulate_post(count=None):  # noqa: E501
    """Simulates a given number of battles

     # noqa: E501

    :param count: number of battles to be simulated
    :type count: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        count = SimulateRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def calc_stats(StatEnvironment=None):  # noqa: E501
    """calculates stats for the specified hero with the specified equipment

    Calculates stats # noqa: E501

    :param StatEnvironment: stat environment containing desired hero and player progress
    :type StatEnvironment: dict | bytes

    :rtype: List[HeroStats]
    """
    if connexion.request.is_json:
        StatEnvironment = StatRequest.from_dict(connexion.request.get_json())  # noqa: E501
        return Hero.scarlet().hp
    return 'no heroes'
