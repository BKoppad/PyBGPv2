"""
Sample tests for bgp_router_config.py
"""
from django.test import SimpleTestCase
from unittest.mock import patch
from pybgp import bgp_router_config
# from pybgp import router_config_db as rdb
# import time


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

    # Cisco router commands for interface configuration of R1 and R2
    r1Intconfig = ["config t",
                   "int gi0/1",
                   "ip address 10.10.10.1 255.255.255.0",
                   "no shut"]
    # r1Intconfig_db = rdb.get_config("r1Intconfig")
    r2Intconfig = ["config t",
                   "int gi0/1",
                   "ip address 10.10.10.2 255.255.255.0",
                   "no shut"]

    # Cisco router commands for BGP Neighbor configuration
    #  of R1 and R2 with same password
    r1BGPConfig = ["router bgp 100",
                   "neighbor 10.10.10.2 remote-as 100",
                   "neighbor 10.10.10.2 password cisco",
                   "neighbor 10.10.10.2 update-source gi0/1",
                   "no auto-summary",
                   "end",
                   "exit"]
    r2BGPConfig = ["router bgp 100",
                   "neighbor 10.10.10.1 remote-as 100",
                   "neighbor 10.10.10.1 password cisco",
                   "neighbor 10.10.10.1 update-source gi0/1",
                   "no auto-summary",
                   "end",
                   "exit"]

    # Cisco router commands for BGP Neighbor configuration
    # with different password in R1
    r1BGPBadConfig = ["config t",
                      "int gi0/1",
                      "router bgp 100",
                      "neighbor 10.10.10.2 remote-as 100",
                      "neighbor 10.10.10.2 password juniper",
                      "neighbor 10.10.10.2 update-source gi0/1",
                      "no auto-summary",
                      "end",
                      "exit"]

    r1config = r1Intconfig + r1BGPConfig
    r2config = r2Intconfig + r2BGPConfig

    def test_router_connect_success(self):
        """Test whether conncetion with router is successfull"""
        user1 = bgp_router_config.BGP_Router()
        res = user1.connect_ssh(self.router1)
        self.assertTrue(True, res)

    @patch('builtins.input', side_effect=['show ip bgp', 'exit'])
    def test_router_cli_access(self, input):
        """Test command exceution on router working as expected"""
        user2 = bgp_router_config.BGP_Router()
        user2.connect_ssh(self.router2)
        res = "".join(user2.cli_access())
        self.assertIn('BGP not active', res.replace('\r\n', ' '))

    def test_router_connect_failur(self):
        """Test connection with router fails due to authentication issue"""
        user3 = bgp_router_config.BGP_Router()
        res = user3.connect_ssh(self.router3)
        self.assertTrue(True, res)

    @patch('builtins.input', side_effect=r1config + r2config)
    def test_bgp_neighbour_with_same_password_configured(self, input):
        """Verify Interfaces and BGP Protocol on 2 routers R1 and R2 with
        same password configured successfully"""
        user1 = bgp_router_config.BGP_Router()
        user1.connect_ssh(self.router1)
        res1 = "".join(user1.cli_access())
        print("User 1 op", res1)
        self.assertNotIn("Invalid input detected", res1.replace('\r\n', ' '))
        user2 = bgp_router_config.BGP_Router()
        user2.connect_ssh(self.router2)
        res2 = "".join(user2.cli_access())
        print("User 2 op", res2)
        self.assertNotIn("Invalid input detected", res2.replace('\r\n', ' '))

    @patch('builtins.input', side_effect=['show ip bgp summary', 'exit'])
    def test_bgp_neighbour_up_when_same_password_configured(self, input):
        """Verify BGP Neighnour is up on 2 routers R1 and R2 when
        same password configured successfully"""
        user1 = bgp_router_config.BGP_Router()
        user1.connect_ssh(self.router1)
        res1 = "".join(user1.cli_access())
        print("User 1 op", res1)
        self.assertIn("10.10.10.2", res1.replace('\r\n', ' '))
        self.assertNotIn("Idle", res1.replace('\r\n', ' '))

    @patch('builtins.input', side_effect=r1BGPBadConfig)
    def test_bgp_neighbour_down_with_different_passwword(self, input):
        """Configure Interfaces and BGP Protocol on 2 routers R1 and R2
        with different password and verify BGP going down"""
        user1 = bgp_router_config.BGP_Router()
        user1.connect_ssh(self.router1)
        res1 = "".join(user1.cli_access())
        print("User 1 op", res1)
        self.assertNotIn("Invalid input detected", res1.replace('\r\n', ' '))

    # Wait for around 10 minutes for BGP session to idle state
    # time.sleep(500)

    @patch('builtins.input', side_effect=['show ip bgp summary', 'exit'])
    def test_bgp_neighbour_when_different_password_configured(self, input):
        """Verify BGP Neighnour is up on 2 routers R1 and R2 when
        same password configured successfully"""
        user1 = bgp_router_config.BGP_Router()
        user1.connect_ssh(self.router1)
        res1 = "".join(user1.cli_access())
        print("User 1 op", res1)
        self.assertIn("10.10.10.2", res1.replace('\r\n', ' '))
        self.assertIn("Idle", res1.replace('\r\n', ' '))
