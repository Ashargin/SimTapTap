# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.pet import Pet  # noqa: F401,E501
from swagger_server.models.player_guild_tech import PlayerGuildTech  # noqa: F401,E501
from swagger_server.models.player_pet_bonus import PlayerPetBonus  # noqa: F401,E501
from swagger_server import util


class Player(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, pet_bonus: PlayerPetBonus=None, active_pet: Pet=None, guild_tech: PlayerGuildTech=None):  # noqa: E501
        """Player - a model defined in Swagger

        :param pet_bonus: The pet_bonus of this Player.  # noqa: E501
        :type pet_bonus: PlayerPetBonus
        :param active_pet: The active_pet of this Player.  # noqa: E501
        :type active_pet: Pet
        :param guild_tech: The guild_tech of this Player.  # noqa: E501
        :type guild_tech: PlayerGuildTech
        """
        self.swagger_types = {
            'pet_bonus': PlayerPetBonus,
            'active_pet': Pet,
            'guild_tech': PlayerGuildTech
        }

        self.attribute_map = {
            'pet_bonus': 'petBonus',
            'active_pet': 'activePet',
            'guild_tech': 'guildTech'
        }

        self._pet_bonus = pet_bonus
        self._active_pet = active_pet
        self._guild_tech = guild_tech

    @classmethod
    def from_dict(cls, dikt) -> 'Player':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Player of this Player.  # noqa: E501
        :rtype: Player
        """
        return util.deserialize_model(dikt, cls)

    @property
    def pet_bonus(self) -> PlayerPetBonus:
        """Gets the pet_bonus of this Player.


        :return: The pet_bonus of this Player.
        :rtype: PlayerPetBonus
        """
        return self._pet_bonus

    @pet_bonus.setter
    def pet_bonus(self, pet_bonus: PlayerPetBonus):
        """Sets the pet_bonus of this Player.


        :param pet_bonus: The pet_bonus of this Player.
        :type pet_bonus: PlayerPetBonus
        """
        if pet_bonus is None:
            raise ValueError("Invalid value for `pet_bonus`, must not be `None`")  # noqa: E501

        self._pet_bonus = pet_bonus

    @property
    def active_pet(self) -> Pet:
        """Gets the active_pet of this Player.


        :return: The active_pet of this Player.
        :rtype: Pet
        """
        return self._active_pet

    @active_pet.setter
    def active_pet(self, active_pet: Pet):
        """Sets the active_pet of this Player.


        :param active_pet: The active_pet of this Player.
        :type active_pet: Pet
        """
        if active_pet is None:
            raise ValueError("Invalid value for `active_pet`, must not be `None`")  # noqa: E501

        self._active_pet = active_pet

    @property
    def guild_tech(self) -> PlayerGuildTech:
        """Gets the guild_tech of this Player.


        :return: The guild_tech of this Player.
        :rtype: PlayerGuildTech
        """
        return self._guild_tech

    @guild_tech.setter
    def guild_tech(self, guild_tech: PlayerGuildTech):
        """Sets the guild_tech of this Player.


        :param guild_tech: The guild_tech of this Player.
        :type guild_tech: PlayerGuildTech
        """

        self._guild_tech = guild_tech
