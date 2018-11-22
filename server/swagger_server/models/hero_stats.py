# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.hero import Hero  # noqa: F401,E501
from swagger_server.models.hero_stats_stats import HeroStatsStats  # noqa: F401,E501
from swagger_server import util


class HeroStats(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, hero: Hero=None, stats: HeroStatsStats=None):  # noqa: E501
        """HeroStats - a model defined in Swagger

        :param hero: The hero of this HeroStats.  # noqa: E501
        :type hero: Hero
        :param stats: The stats of this HeroStats.  # noqa: E501
        :type stats: HeroStatsStats
        """
        self.swagger_types = {
            'hero': Hero,
            'stats': HeroStatsStats
        }

        self.attribute_map = {
            'hero': 'hero',
            'stats': 'stats'
        }

        self._hero = hero
        self._stats = stats

    @classmethod
    def from_dict(cls, dikt) -> 'HeroStats':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The HeroStats of this HeroStats.  # noqa: E501
        :rtype: HeroStats
        """
        return util.deserialize_model(dikt, cls)

    @property
    def hero(self) -> Hero:
        """Gets the hero of this HeroStats.


        :return: The hero of this HeroStats.
        :rtype: Hero
        """
        return self._hero

    @hero.setter
    def hero(self, hero: Hero):
        """Sets the hero of this HeroStats.


        :param hero: The hero of this HeroStats.
        :type hero: Hero
        """
        if hero is None:
            raise ValueError("Invalid value for `hero`, must not be `None`")  # noqa: E501

        self._hero = hero

    @property
    def stats(self) -> HeroStatsStats:
        """Gets the stats of this HeroStats.


        :return: The stats of this HeroStats.
        :rtype: HeroStatsStats
        """
        return self._stats

    @stats.setter
    def stats(self, stats: HeroStatsStats):
        """Sets the stats of this HeroStats.


        :param stats: The stats of this HeroStats.
        :type stats: HeroStatsStats
        """
        if stats is None:
            raise ValueError("Invalid value for `stats`, must not be `None`")  # noqa: E501

        self._stats = stats
