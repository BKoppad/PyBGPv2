import re
from paramiko import AuthenticationException, BadHostKeyException, SSHClient, AutoAddPolicy, SSHException
import time

class BGP_Router:
    def connect_ssh(self, router):
        '''Connecting to router and returning sshClient object'''
        self.ssh_client = SSHClient()
        self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        print(f'Connecting to {router["hostname"]}')
        try :
            self.ssh_client.connect(**router, look_for_keys=False, allow_agent=False)
        except Exception as sshExc:
            print("ERROR: Unable to establish ssh connection: %s" % sshExc)
            return False

        print("Connected successfully with router " , router["hostname"] )
        return True

    def cli_access(self):
        '''Executing commands on supplied sshClient object or resepctive router'''
        self.shell = self.ssh_client.invoke_shell()
        print(self.shell.send_ready())
        self.shell.send('enable\n')
        self.shell.send('cisco\n')
        time.sleep(1)
        output = self.shell.recv(10000).decode()
        print(output)
        command = " "
        
        while command != 'exit':
            command= input("> ")
            self.shell.send(f"{command}\n")
            time.sleep(3)
            output=self.shell.recv(10000).decode()
            print(output)
    
    def __del__(self):
        print("Closing connection")
        self.ssh_client.close()