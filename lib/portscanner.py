import os
import nmap3
import socket
from prettytable import PrettyTable


BANNER = '''
                                   .::!!!!!!!:.
  .!!!!!:.                        .:!!!!!!!!!!!!
  ~~~~!!!!!!.                 .:!!!!!!!!!UWWW$$$ 
      :$$NWX!!:           .:!!!!!!XUWW$$$$$$$$$P 
      $$$$$##WX!:      .<!!!!UW$$$$"  $$$$$$$$# 
      $$$$$  $$$UX   :!!UW$$$$$$$$$   4$$$$$* 
      ^$$$B  $$$$\     $$$$$$$$$$$$   d$$R" 
        "*$bd$$$$      '*$$$$$$$$$$$o+#" 
             """"          """"""

(!) Port Scanner (!)
1. Top Port Mode
2. Os Detection(root akses)
3. Version Detection(lambat)
4. Syn Scanner
5. Kembali
6. Keluar

'''

def banner():
    return BANNER

class PortScanner:

     def __init__(self,target):
         self.target = target
         self.nmap = nmap3.Nmap()
         try:
          self.ip = socket.gethostbyname(self.target)
         except socket.gaierror:
            print('(!) Target tidak diketahui')
         self.technique = nmap3.NmapScanTechniques()

     def top_ports_mode(self):
         json = self.nmap.scan_top_ports(self.target)
         ip = json[self.ip]
         # ip information parser
         # result ports info

         print('\n\nDomain Name System\n')
         print('[Type]\t\t[Hostname]\n')
         for host in ip['hostname']:
            print(host['type']+'\t\t'+host['name'])

         ports = ip['ports']
         print('\n\t\t[============= '+self.ip+' =============]\n')
         print('Protocol\tPort\tState\t\tReason\t\tService\n')
         for i in range(len(ports)):
            print(ports[i]['protocol'] + '\t\t' + ports[i]['portid'] + '\t' + ports[i]['state']  , end='')
            tabs = '\t\t'
            if ports[i]['state'] == 'filtered':
                 tabs = '\t'
                 print(tabs + ports[i]['reason'], end='')
            else:
                 tabs = '\t\t'
                 print(tabs + ports[i]['reason'], end='')
            if ((ports[i]['reason'] == 'conn-refused') or  (ports[i]['reason'] == 'no-response')):
                 tabs = '\t'
                 print(tabs + ports[i]['service']['name'])
            else:
                 tabs = '\t\t'
                 print(tabs + ports[i]['service']['name'])

         print('\n' + json['runtime']['summary'] + '!')


     def dns_enum(self):
         json = self.nmap.nmap_dns_brute_script(self.target)
         print('Address\t\tHostname\n')
         for info in json:
             print(info['address'] + '\t' + info['hostname'])


     def os_detect(self):
         # harus dijalankan dengan akses root
         if os.getuid() != 0:
            print('(!)harus dijalankan dengan akses root')
            return

         json = self.nmap.nmap_os_detection(self.target)
         ip = json[self.ip]

         # dari ip
         table = PrettyTable()
         print('\n\n\t\t[===================== Operating System ========================] ')
         table.field_names = ['name', 'type', 'accuracy','line', 'cpe']
         for i in ip['osmatch']:
           table.add_row([i['name'], i['osclass']['type'], i['accuracy'],i['line'],i['cpe']])
         # hasil  os
         print(table)

         print('\n\nDomain Name System\n')
         print('[Type]\t\t[Hostname]\n')
         for host in ip['hostname']:
            print(host['type']+'\t\t'+host['name'])

         ports = ip['ports']
         print('\n\t\t[============= '+self.ip+' =============]\n')
         print('Protocol\tPort\tState\t\tReason\t\tService\n')
         for i in range(len(ports)):
            print(ports[i]['protocol'] + '\t\t' + ports[i]['portid'] + '\t' + ports[i]['state']  , end='') 
            tabs = '\t\t'
            if ports[i]['state'] == 'filtered':
                 tabs = '\t'
                 print(tabs + ports[i]['reason'], end='')
            else:
                 tabs = '\t\t'
                 print(tabs + ports[i]['reason'], end='')
            if ((ports[i]['reason'] == 'conn-refused') or  (ports[i]['reason'] == 'no-response')):
                 tabs = '\t'
                 print(tabs + ports[i]['service']['name'])
            else:
                 tabs = '\t\t'
                 print(tabs + ports[i]['service']['name'])

         print('\n' + json['runtime']['summary'] + '!')

     def scan_types(self, params):
         json = None
         if params:
            json = self.nmap.nmap_version_detection(self.target)
         else:
            if os.getuid != 0:
               print('(!) Harus dijalankan dengan akses root')
               return
            json = self.technique.nmap_syn_scan(self.target)
         print(json)

         ip = json[self.ip]
         table = PrettyTable()
         table.field_names = ['protocol', 'port', 'name', 'state', 'reason', 'product','version', 'method', 'cpe']
         for x in ip['ports']:
             if x['cpe'] == []:
                 x['cpe'].append({'cpe':'NULL'})
             if 'product' not in x['service'].keys():
                x['service']['product'] = 'NULL'
             if 'version' not in x['service'].keys():
                x['service']['version'] = 'NULL'
         for i in ip['ports']:
             table.add_row([i['protocol'],i['portid'], i['service']['name'],i['state'], i['reason'], i['service']['product'],i['service']['version'], i['service']['method'],i['cpe'][0]['cpe']])
         print(table)



