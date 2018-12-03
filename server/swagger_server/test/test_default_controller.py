# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.hero_stats import HeroStats  # noqa: E501
from swagger_server.models.simulate_request import SimulateRequest  # noqa: E501
from swagger_server.models.simulate_response import SimulateResponse  # noqa: E501
from swagger_server.models.stat_request import StatRequest  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_battle_simulate_post(self):
        """Test case for battle_simulate_post

        Simulates a given number of battles
        """
        simulateRequest = SimulateRequest()
        response = self.client.open(
            '/gitterrost4/TapTapSim/1.0.0/battle/simulate',
            method='POST',
            data=json.dumps(simulateRequest),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calc_stats(self):
        """Test case for calc_stats

        calculates stats for the specified hero with the specified equipment
        """
        statRequest = StatRequest()
        response = self.client.open(
            '/gitterrost4/TapTapSim/1.0.0/hero/stats',
            method='POST',
            data=json.dumps(statRequest),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
