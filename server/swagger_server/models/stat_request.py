# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.hero import Hero  # noqa: F401,E501
from swagger_server.models.player import Player  # noqa: F401,E501
from swagger_server import util


class StatRequest(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, heroes: List[Hero]=None, player: Player=None):  # noqa: E501
        """StatRequest - a model defined in Swagger

        :param heroes: The heroes of this StatRequest.  # noqa: E501
        :type heroes: List[Hero]
        :param player: The player of this StatRequest.  # noqa: E501
        :type player: Player
        """
        self.swagger_types = {
            'heroes': List[Hero],
            'player': Player
        }

        self.attribute_map = {
            'heroes': 'heroes',
            'player': 'player'
        }

        self._heroes = heroes
        self._player = player

    @classmethod
    def from_dict(cls, dikt) -> 'StatRequest':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The StatRequest of this StatRequest.  # noqa: E501
        :rtype: StatRequest
        """
        return util.deserialize_model(dikt, cls)

    @property
    def heroes(self) -> List[Hero]:
        """Gets the heroes of this StatRequest.

        All heroes for which stats are to be calculated  # noqa: E501

        :return: The heroes of this StatRequest.
        :rtype: List[Hero]
        """
        return self._heroes

    @heroes.setter
    def heroes(self, heroes: List[Hero]):
        """Sets the heroes of this StatRequest.

        All heroes for which stats are to be calculated  # noqa: E501

        :param heroes: The heroes of this StatRequest.
        :type heroes: List[Hero]
        """
        if heroes is None:
            raise ValueError("Invalid value for `heroes`, must not be `None`")  # noqa: E501

        self._heroes = heroes

    @property
    def player(self) -> Player:
        """Gets the player of this StatRequest.


        :return: The player of this StatRequest.
        :rtype: Player
        """
        return self._player

    @player.setter
    def player(self, player: Player):
        """Sets the player of this StatRequest.


        :param player: The player of this StatRequest.
        :type player: Player
        """
        if player is None:
            raise ValueError("Invalid value for `player`, must not be `None`")  # noqa: E501

        self._player = player
