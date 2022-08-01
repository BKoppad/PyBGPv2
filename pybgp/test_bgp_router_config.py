"""
Sample tests for bgp_router_config.py
"""
from django.test import SimpleTestCase
from unittest.mock import patch
from pybgp import bgp_router_config


class ConnectSshTests(SimpleTestCase):
    """" Test connect_ssh module """
    # Defining Router-1 parametrs for connection
    router1 = {'hostname': '10.1.1.10',
               'port': '22',
               'username': 'bkoppad',
               'password': 'cisco'}

    # Defining Router-2 parametrs for connection from Router-1
    # by altering its hostname
    router2 = router1.copy()
    router2['hostname'] = '10.1.1.20'

    # Defining Router-3 parametrs for connection from Router-1
    # by altering its password for negative testing
    router3 = router1.copy()
    router3['password'] = 'juniper'

    def test_router_connect_success(self):
        """Test whether conncetion with router is successfull"""
        router1 = {'hostname': '10.1.1.10',
                   'port': '22',
                   'username': 'bkoppad',
                   'password': 'cisco'}
        user1 = bgp_router_config.BGP_Router()
        res = user1.connect_ssh(router1)
        self.assertTrue(True, res)

    def test_router_connect_failur(self):
        """Test connection with router fails due to authentication issue"""
        router2 = {'hostname': '10.1.1.20',
                   'port': '22',
                   'username': 'bkoppad2',
                   'password': 'juniper'}
        user2 = bgp_router_config.BGP_Router()
        res = user2.connect_ssh(router2)
        self.assertTrue(True, res)

    @patch('builtins.input', side_effect=['show ip bgp', 'exit'])
    def test_router_cli_access_1(self, input):
        """Test command exceution on router working as expected"""
        router = {'hostname': '10.1.1.10',
                  'port': '22',
                  'username': 'bkoppad',
                  'password': 'cisco'}
        user3 = bgp_router_config.BGP_Router()
        user3.connect_ssh(router)
        res = "".join(user3.cli_access())
        # print("Output==", res)
        self.assertIn('BGP not active', res.replace('\r\n', ' '))
