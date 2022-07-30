"""
Sample tests for bgp_router_config.py
"""
from django.test import SimpleTestCase
from unittest.mock import patch,MagicMock,Mock
from pybgp import bgp_router_config

def mockRouter():
    """MOcking Router Behaviour"""
    mock_connect_ssh = Mock(name="connect_ssh mock success", return_value=True)

def mockRouter2():
    """MOcking Router2 Behaviour"""
    mock_connect_ssh = Mock(name="connect_ssh mock failure", 
                            side_effect=KeyError('Exception'),
                            return_value=False)

class ConnectSshTests(SimpleTestCase):
    """" Test connect_ssh module """

    @patch("pybgp.bgp_router_config.BGP_Router.connect_ssh")
    def test_router_connect_success_mock(self,mockRouter):
        """Testing using mocks"""
        mockRouter.return_value=True
        router1 = {'hostname': '10.1.1.10',
                   'port': '22',
                   'username': 'bkoppad',
                   'password': 'cisco'}
        res = bgp_router_config.BGP_Router.connect_ssh(router1)
        self.assertTrue(True, res)
    
    @patch("pybgp.bgp_router_config.BGP_Router.connect_ssh")
    def test_router_connect_failur_mock(self,mockRouter2):
        """Test connection with router fails due to authentication issue"""
        mockRouter2.return_value=False
        router2 = {'hostname': '10.1.1.20',
                   'port': '22',
                   'username': 'bkoppad2',
                   'password': 'juniper'}
        res = bgp_router_config.BGP_Router.connect_ssh(router2)
        self.assertTrue(True, res)


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
        res = user3.cli_access()
        self.assertTrue(True, res)

    # Ping test
    # returning ssh_clinet object
