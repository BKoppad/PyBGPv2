import sqlite3


def create_table():
    conn = sqlite3.connect("router_config.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS cisco_config (config_name TEXT, config_value TEXT)")
    conn.commit()
    conn.close()

def insert_table(config_name,config_value):
    conn = sqlite3.connect("router_config.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO cisco_config VALUES (?,?)",(config_name,config_value))
    conn.commit()
    conn.close()
   
def view():
    conn = sqlite3.connect("router_config.db")
    cur = conn.cursor()    
    cur.execute("SELECT * FROM cisco_config")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_config(config_name):
    conn = sqlite3.connect("router_config.db")
    cur = conn.cursor()    
    cur.execute("SELECT * FROM cisco_config WHERE config_name=?",(config_name,))
    rows = cur.fetchall()
    conn.close()
    return rows[0][1].split(",")

def delet(config_name):
    conn = sqlite3.connect("router_config.db")
    cur = conn.cursor()    
    cur.execute("DELETE FROM cisco_config WHERE config_name=?",(config_name,))
    conn.commit()
    conn.close
    
def update(config_name,config_value):
    conn = sqlite3.connect("router_config.db")
    cur = conn.cursor()    
    cur.execute("UPDATE cisco_config SET config_value=? WHERE config_name=?",(config_value,config_name))
    conn.commit()
    conn.close

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

# create_table()
# insert_table("r1Intconfig", ",".join(r1Intconfig))
# insert_table("r2Intconfig", ",".join(r2Intconfig))
# insert_table("r1BGPConfig", ",".join(r1BGPConfig))
# insert_table("r2BGPConfig", ",".join(r2BGPConfig))
# insert_table("r1BGPBadConfig", ",".join(r1BGPBadConfig))
# print(view())

# r1Intconfig_db = get_config("r1Intconfig")
# print(r1Intconfig_db)
# r2Intconfig_db = get_config("r2Intconfig")
# print(r2Intconfig_db)
# r1BGPConfig_db = get_config("r1BGPConfig")
# print(r1BGPConfig_db)
# r2BGPConfig_db = get_config("r2BGPConfig")
# print(r2BGPConfig_db)
# r1BGPBadConfig_db = get_config("r1BGPBadConfig")
# print(r1BGPBadConfig_db)


