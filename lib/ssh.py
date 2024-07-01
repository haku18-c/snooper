import paramiko
import sys
import select

ssh_banner = r'''
____________________  ___________________            _____
__  ___/_  ___/__  / / /_  ____/__  /__(_)_____________  /_
_____ \_____ \__  /_/ /_  /    __  /__  /_  _ \_  __ \  __/
____/ /____/ /_  __  / / /___  _  / _  / /  __/  / / / /_
/____/ /____/ /_/ /_/  \____/  /_/  /_/  \___//_/ /_/\__/
'''

def banner():
    return ssh_banner


class SSH(object):

    def __init__(self, target, username, password):
        self.target = target
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()

    def runner(self):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.target, username=self.username, password=self.password)
        # setting shell interaktif menggunakan invoke_shell
        # shell interaktif
        # user@user:$ <command>
        session = self.client.invoke_shell()
        try:
          while True:
           if session.recv_ready():
              out = session.recv(65535).decode('utf-8')
              sys.stdout.write(output)
           # monitoring file deskriptor
           # menghandle terpotongnya data dari server
           inputs, _, _= select.select([sys.stdin, session], [],[])
           for fd in inputs:
             if fd == sys.stdin:
                data = sys.stdin.readline()
                session.send(data)
             else:
                output = session.recv(65535).decode('utf-8')
                sys.stdout.write(output)
        except Exception as er:
              print(er)
        self.client.close()


