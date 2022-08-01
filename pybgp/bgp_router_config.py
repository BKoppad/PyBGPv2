from paramiko import SSHClient, AutoAddPolicy
import time


class BGP_Router:

    def connect_ssh(self, router):
        '''Connecting to router and returning sshClient object'''
        self.ssh_client = SSHClient()
        self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        print(f'Connecting to {router["hostname"]}')
        try:
            self.ssh_client.connect(**router,
                                    look_for_keys=False,
                                    allow_agent=False)
        except Exception as sshExc:
            print("ERROR: Unable to establish ssh connection: %s" % sshExc)
            return False

        print("Connected successfully with router ", router["hostname"])
        return True

    def cli_access(self):
        '''Executing commands on resepctive router'''
        self.shell = self.ssh_client.invoke_shell()
        print(self.shell.send_ready())
        # Enabling router with password
        self.shell.send('enable\n')
        self.shell.send('cisco\n')
        time.sleep(1)
        output1 = self.shell.recv(10000).decode()
        print(output1)
        command = " "
        outPutList = []

        # User inputs commands to be executed on router
        while command != 'exit':
            command = input("> ")
            self.shell.send(f"{command}\n")
            time.sleep(3)
            output2 = self.shell.recv(10000).decode()
            outPutList.append(output2)
            print(output2)

        return outPutList

    def __del__(self):
        print("Closing connection")
        self.ssh_client.close()


class BGP_config:

    def interface_config(self, router):
        """This proc is used to configure the interfaces for BGP protocol"""
        router = BGP_Router()
        router.connect_ssh(router)
        router.cli_access()
