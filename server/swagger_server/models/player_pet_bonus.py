# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class PlayerPetBonus(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, hp_bonus: int=None, attack_bonus: int=None):  # noqa: E501
        """PlayerPetBonus - a model defined in Swagger

        :param hp_bonus: The hp_bonus of this PlayerPetBonus.  # noqa: E501
        :type hp_bonus: int
        :param attack_bonus: The attack_bonus of this PlayerPetBonus.  # noqa: E501
        :type attack_bonus: int
        """
        self.swagger_types = {
            'hp_bonus': int,
            'attack_bonus': int
        }

        self.attribute_map = {
            'hp_bonus': 'hpBonus',
            'attack_bonus': 'attackBonus'
        }

        self._hp_bonus = hp_bonus
        self._attack_bonus = attack_bonus

    @classmethod
    def from_dict(cls, dikt) -> 'PlayerPetBonus':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Player_petBonus of this PlayerPetBonus.  # noqa: E501
        :rtype: PlayerPetBonus
        """
        return util.deserialize_model(dikt, cls)

    @property
    def hp_bonus(self) -> int:
        """Gets the hp_bonus of this PlayerPetBonus.

        The cumulative hp bonus of all pets  # noqa: E501

        :return: The hp_bonus of this PlayerPetBonus.
        :rtype: int
        """
        return self._hp_bonus

    @hp_bonus.setter
    def hp_bonus(self, hp_bonus: int):
        """Sets the hp_bonus of this PlayerPetBonus.

        The cumulative hp bonus of all pets  # noqa: E501

        :param hp_bonus: The hp_bonus of this PlayerPetBonus.
        :type hp_bonus: int
        """

        self._hp_bonus = hp_bonus

    @property
    def attack_bonus(self) -> int:
        """Gets the attack_bonus of this PlayerPetBonus.

        The cumulative attack bonus of all pets  # noqa: E501

        :return: The attack_bonus of this PlayerPetBonus.
        :rtype: int
        """
        return self._attack_bonus

    @attack_bonus.setter
    def attack_bonus(self, attack_bonus: int):
        """Sets the attack_bonus of this PlayerPetBonus.

        The cumulative attack bonus of all pets  # noqa: E501

        :param attack_bonus: The attack_bonus of this PlayerPetBonus.
        :type attack_bonus: int
        """

        self._attack_bonus = attack_bonus