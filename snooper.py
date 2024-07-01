import os
import sys
import socket
import getpass
from lib.ssh import SSH
from lib.ssh import banner as sbanner
from lib.ftp import FTPClient
from lib.ftp import fbanner
from lib.chatroom import Server
from lib.chatroom import Client
from lib.chatroom import banner as cbanner
from lib.portscanner import PortScanner
from lib.portscanner import banner as psbanner


banner = '''


  ██████  ███▄    █  ▒█████   ▒█████   ██▓███  ▓█████  ██▀███
▒██    ▒  ██ ▀█   █ ▒██▒  ██▒▒██▒  ██▒▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒
░ ▓██▄   ▓██  ▀█ ██▒▒██░  ██▒▒██░  ██▒▓██░ ██▓▒▒███   ▓██ ░▄█ ▒
  ▒   ██▒▓██▒  ▐▌██▒▒██   ██░▒██   ██░▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄
▒██████▒▒▒██░   ▓██░░ ████▓▒░░ ████▓▒░▒██▒ ░  ░░▒████▒░██▓ ▒██▒
▒ ▒▓▒ ▒ ░░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░ ▒░▒░▒░ ▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░▒  ░ ░░ ░░   ░ ▒░  ░ ▒ ▒░   ░ ▒ ▒░ ░▒ ░      ░ ░  ░  ░▒ ░ ▒░
░  ░  ░     ░   ░ ░ ░ ░ ░ ▒  ░ ░ ░ ▒  ░░          ░     ░░   ░
      ░           ░     ░ ░      ░ ░              ░  ░

                              (Snooper) Najib Khoirul Rizal_12221909 v0.1
                              https://github.com/haku18-c/snooper

1. Socket ChatRoom
2. SSHClient
3. FTPClient
4. Port Scanner
5. Keluar
'''



class Snooper(object):

     def start(self):
         while True:
            os.system('clear')
            try:
              print(banner)
              num = int(input('(pilih)> '))
              if num == 1:
                  self.chatroom()
                  break
              elif num == 2:
                  self.sshclient()
                  break
              elif num  == 3:
                  self.ftpclient()
              elif num == 4:
                  try:
                    target = input('(target)> ')
                    socket.gethostbyname(target)
                  except socket.gaierror:
                    print('(!)Error target tidak diketahui')
                    input('(!)Tekan enter')
                    continue
                  self.portscanner(target)
                  break
              elif num == 5:
                  print('(!) Keluar')
                  sys.exit(1)
              else:
                  self.option_handler(num)
            except ValueError:
              print('(!)Error yang anda masukan bukan angka')
              break

     def chatroom(self):
         while True:
            os.system('clear')
            print(cbanner())
            pil = int(input('(pilih)> '))
            if pil == 1:
               addr = str(input('(host)> '))
               port = int(input('(port)> '))
               serv = Server(addr, port)
               print('Tekan enter untuk mematikan server')
               serv.serving()
               break
            elif pil == 2:
               addr = str(input('(host)> '))
               port = int(input('(port)> '))
               client = Client(addr, port)
               client.communicate()
               break
            elif pil == 3:
               self.start()
            elif pil == 4:
               sys.exit()
            else:
               self.option_handler(pil)

     def portscanner(self, target):
         ps = PortScanner(target)
         while True:
             os.system('clear')
             print(psbanner())
             pil = int(input('(pilih)> '))
             print()
             if pil == 1:
                ps.top_ports_mode()
             elif pil == 2:
                ps.os_detect()
             elif pil == 3:
                ps.scan_types(1)
             elif pil == 4:
                ps.scan_types(0)
             elif pil == 5:
                self.start()
                break
             elif pil == 6:
                print('(!) keluar')
                sys.exit(1)
             else:
                self.option_handler(pil)
             input('\nPress <Enter>')

     def sshclient(self):
         os.system('clear')
         print(sbanner())
         print('')
         host = input('(target)> ')
         user = input('Username : ')
         passwd = getpass.getpass()
         client = SSH(host, user, passwd)
         client.runner()

     def ftpclient(self):
         host = input('(target)> ')
         user = input('Username : ')
         password = getpass.getpass()
         client = FTPClient(host, user, password)
         client.login()
         while True:
           os.system('clear')
           print(fbanner())
           pil = int(input('(pilih)> '))
           if pil == 1:
              client.list_files()
           elif pil == 2:
              local_path = input('path file yang akan diupload  : ')
              remote_path = input('path direktori mana akan disimpan : ')
              client.upload_file(local_path, remote_path)
           elif pil == 3:
              remote_path = input('file yang akan didownload : ')
              local_path = input('path untuk menyimpan hasil download : ')
              client.download_file(local_path, remote_path)
           elif pil == 4:
              remote_file = input('file yang akan dihapus : ')
              client.delete_file(remote_file)
           elif pil == 5:
              self.start();
           elif self == 6:
              client.close()
              sys.exit(1)
           else:
              option_handler()
           input('Press <Enter>')


     def option_handler(self, num):
         print('(!) Tidak ada opsi untuk', num)
         input('(!) Tekan Enter untuk lanjut..')


a = Snooper()
a.start()
