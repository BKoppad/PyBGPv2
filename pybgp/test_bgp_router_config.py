"""
Sample tests for bgp_router_config.py
"""
from django.test import SimpleTestCase
from unittest.mock import patch
from pybgp import bgp_router_config
from pybgp import router_config_db as rdb


class ConnectSshTests(SimpleTestCase):
    """" Test connect_ssh module """
    # Defining Router-1(R1) parametrs for connection
    router1 = {'hostname': '10.1.1.10',
               'port': '22',
               'username': 'bkoppad',
               'password': 'cisco'}

    # Defining Router-2(R2)parametrs for connection from R1
    # by altering its hostname
    router2 = router1.copy()
    router2['hostname'] = '10.1.1.20'

    # Defining Router-3(R3) parametrs for connection from  R1
    # by altering its password for negative testing
    router3 = router1.copy()
    router3['password'] = 'juniper'
    
    #Get Interface configuration from DB  for R1 and R2
    r1Intconfig_db = rdb.get_config("r1Intconfig")
    r2Intconfig_db = rdb.get_config("r2Intconfig")
    # Get BGP configuration with same password from DB for R1 and R2 
    r1BGPConfig_db = rdb.get_config("r1BGPConfig")
    r2BGPConfig_db = rdb.get_config("r2BGPConfig")

    # Get BGP configuration with different password from DB for R1
    r1BGPBadConfig_db = rdb.get_config("r1BGPBadConfig")
    
    r1config = r1Intconfig_db + r1BGPConfig_db
    r2config = r2Intconfig_db + r2BGPConfig_db

    def testA_router_connect_success(self):
        """Test whether conncetion with router is successfull"""
        print("Test case 1: Testing Connection to the router")
        user1 = bgp_router_config.BGP_Router()
        res = user1.connect_ssh(self.router1)
        self.assertTrue(True, res)
        print("Connection to router tested successfully")

    @patch('builtins.input', side_effect=['show ip bgp', 'exit'])
    def testB_router_cli_access(self, input):
        print("\nTest case 2: Verifying Command execution in the router")
        user2 = bgp_router_config.BGP_Router()
        user2.connect_ssh(self.router2)
        res = "".join(user2.cli_access())
        self.assertIn('BGP not active', res.replace('\r\n', ' '))
        print("Successfully verfied command execution on the router")

    def testC_router_connect_failur(self):
        print("\nTest case 3:Verifying error for wrong password while connecting")
        user3 = bgp_router_config.BGP_Router()
        res = user3.connect_ssh(self.router3)
        self.assertTrue(True, res)
        print("Successfully Verified error for wrong password while connecting")

    @patch('builtins.input', side_effect=r1config + r2config)
    def testD_bgp_neighbour_with_same_password_configured(self, input):
        print("\nTest case 4: Verifying BGP configuration with same password")
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
        print("Successfully Verified BGP configuration with same password")

    @patch('builtins.input', side_effect=['show ip bgp summary', 'exit'])
    def testE_bgp_neighbour_up_when_same_password_configured(self, input):
        print("\nTest case 5: Verify BGP Neighnour is up on 2 routers R1 and R2 when\
        same password configured successfully")
        user1 = bgp_router_config.BGP_Router()
        user1.connect_ssh(self.router1)
        res1 = "".join(user1.cli_access())
        print("User 1 op", res1)
        self.assertIn("10.10.10.2", res1.replace('\r\n', ' '))
        self.assertNotIn("Idle", res1.replace('\r\n', ' '))

    @patch('builtins.input', side_effect=r1BGPBadConfig_db)
    def testF_bgp_neighbour_down_with_different_passwword(self, input):
        print("\nTest case 6: Verify BGP configuration with different password on R-1")
        user1 = bgp_router_config.BGP_Router()
        user1.connect_ssh(self.router1)
        res1 = "".join(user1.cli_access())
        print("User 1 op", res1)
        self.assertNotIn("Invalid input detected", res1.replace('\r\n', ' '))
        print("Successfully verified BGP configuration with different password")


    @patch('builtins.input', side_effect=['show ip bgp summary', 'exit'])
    def testG_bgp_neighbour_when_different_password_configured(self, input):
        print ("\nTest case 7: Verify BGP Neighnour status going down post password change in R-1")
        user1 = bgp_router_config.BGP_Router()
        user1.connect_ssh(self.router1)
        res1 = "".join(user1.cli_access())
        print("User 1 op", res1)
        self.assertIn("10.10.10.2", res1.replace('\r\n', ' '))
        self.assertIn("Idle", res1.replace('\r\n', ' '))
        print ("Successfully Verified BGP Neighnour status going down post password change in R-1")
