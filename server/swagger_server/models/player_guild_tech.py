# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.class_guild_tech import ClassGuildTech  # noqa: F401,E501
from swagger_server import util


class PlayerGuildTech(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, warrior: ClassGuildTech=None, assassin: ClassGuildTech=None, wanderer: ClassGuildTech=None, cleric: ClassGuildTech=None, mage: ClassGuildTech=None):  # noqa: E501
        """PlayerGuildTech - a model defined in Swagger

        :param warrior: The warrior of this PlayerGuildTech.  # noqa: E501
        :type warrior: ClassGuildTech
        :param assassin: The assassin of this PlayerGuildTech.  # noqa: E501
        :type assassin: ClassGuildTech
        :param wanderer: The wanderer of this PlayerGuildTech.  # noqa: E501
        :type wanderer: ClassGuildTech
        :param cleric: The cleric of this PlayerGuildTech.  # noqa: E501
        :type cleric: ClassGuildTech
        :param mage: The mage of this PlayerGuildTech.  # noqa: E501
        :type mage: ClassGuildTech
        """
        self.swagger_types = {
            'warrior': ClassGuildTech,
            'assassin': ClassGuildTech,
            'wanderer': ClassGuildTech,
            'cleric': ClassGuildTech,
            'mage': ClassGuildTech
        }

        self.attribute_map = {
            'warrior': 'warrior',
            'assassin': 'assassin',
            'wanderer': 'wanderer',
            'cleric': 'cleric',
            'mage': 'mage'
        }

        self._warrior = warrior
        self._assassin = assassin
        self._wanderer = wanderer
        self._cleric = cleric
        self._mage = mage

    @classmethod
    def from_dict(cls, dikt) -> 'PlayerGuildTech':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Player_guildTech of this PlayerGuildTech.  # noqa: E501
        :rtype: PlayerGuildTech
        """
        return util.deserialize_model(dikt, cls)

    @property
    def warrior(self) -> ClassGuildTech:
        """Gets the warrior of this PlayerGuildTech.


        :return: The warrior of this PlayerGuildTech.
        :rtype: ClassGuildTech
        """
        return self._warrior

    @warrior.setter
    def warrior(self, warrior: ClassGuildTech):
        """Sets the warrior of this PlayerGuildTech.


        :param warrior: The warrior of this PlayerGuildTech.
        :type warrior: ClassGuildTech
        """

        self._warrior = warrior

    @property
    def assassin(self) -> ClassGuildTech:
        """Gets the assassin of this PlayerGuildTech.


        :return: The assassin of this PlayerGuildTech.
        :rtype: ClassGuildTech
        """
        return self._assassin

    @assassin.setter
    def assassin(self, assassin: ClassGuildTech):
        """Sets the assassin of this PlayerGuildTech.


        :param assassin: The assassin of this PlayerGuildTech.
        :type assassin: ClassGuildTech
        """

        self._assassin = assassin

    @property
    def wanderer(self) -> ClassGuildTech:
        """Gets the wanderer of this PlayerGuildTech.


        :return: The wanderer of this PlayerGuildTech.
        :rtype: ClassGuildTech
        """
        return self._wanderer

    @wanderer.setter
    def wanderer(self, wanderer: ClassGuildTech):
        """Sets the wanderer of this PlayerGuildTech.


        :param wanderer: The wanderer of this PlayerGuildTech.
        :type wanderer: ClassGuildTech
        """

        self._wanderer = wanderer

    @property
    def cleric(self) -> ClassGuildTech:
        """Gets the cleric of this PlayerGuildTech.


        :return: The cleric of this PlayerGuildTech.
        :rtype: ClassGuildTech
        """
        return self._cleric

    @cleric.setter
    def cleric(self, cleric: ClassGuildTech):
        """Sets the cleric of this PlayerGuildTech.


        :param cleric: The cleric of this PlayerGuildTech.
        :type cleric: ClassGuildTech
        """

        self._cleric = cleric

    @property
    def mage(self) -> ClassGuildTech:
        """Gets the mage of this PlayerGuildTech.


        :return: The mage of this PlayerGuildTech.
        :rtype: ClassGuildTech
        """
        return self._mage

    @mage.setter
    def mage(self, mage: ClassGuildTech):
        """Sets the mage of this PlayerGuildTech.


        :param mage: The mage of this PlayerGuildTech.
        :type mage: ClassGuildTech
        """

        self._mage = mage
