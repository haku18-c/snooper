import socket
import select
import argparse
import sys

def receiver(sock):
    data = sock.recv(1024)
    return data.decode()

def sender(sock, data):
    data = data.encode()
    sock.sendall(data)

text = r'''
                        ____________
                        |__________|
                       /           /\
                      /           /  \
                     /___________/___/|
                     |          |     |
                     |  ==\ /== |     |
                     |   O   O  | \ \ |
                     |     <    |  \ \|
(!) Chat Room (!)   /|          |   \ \
                   / |  \_____/ |   / /
 1. Server        / /|          |  / /|
 2. Client       /||\|          | /||\/
 3. Kembali           -------------|
 4. Keluar             | |    | |
                      <__/    \__>
'''

def banner():
    return text


class Server:

     def __init__(self, host, port):
         self.host = host
         self.port = port
         self.server = socket.socket()
         self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
         self.server.bind((self.host, self.port))
         self.server.listen(0)
         self.clientmap = []
         self.output = []

     def get_client_name(self, sock):
         addr = sock.getsockname()
         client = f'klien{addr[0]}:{addr[1]}'
         return client

     def serving(self):
         _input = [sys.stdin, self.server]
         self.output = []
         running = True
         while running:
              reads, writes, exceptional = select.select(_input, self.output, [])
              for sock in reads:
                  if sock == self.server:
                     conn, addr = self.server.accept()
                     _input.append(conn)
                     client_name = receiver(conn)
                     parser_data =  f'klien {_input.index(conn)-1} Bergabung!'
                     sender(conn, parser_data)
                     for socks in self.output:
                        sender(socks, parser_data)
                     self.output.append(conn)
                  elif sock == sys.stdin:
                     chunk = sys.stdin.readline()
                     running = False
                  else:
                     data = receiver(sock)
                     if data:
                       msg = '\n[klien ' +  str(_input.index(sock)-1) + ']' + data
                       for socks in writes:
                           sender(socks, msg)
                     else:
                       print(self.get_client_name(sock) + 'terputus' )
                       self.output.remove(sock)
                       _input.remove(sock)


class Client:

     def __init__(self, host, port):
         self.host = host
         self.port = port
         self.client = socket.socket()
         self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
         self.client.connect((self.host, self.port))
         self.connected = True
         self.prompt = '[' + str(self.client.getsockname()) + ']>'
         sender(self.client, self.prompt)
         ddata = receiver(self.client).split('Bergabung!')
         print('CHAT ROOM TCP MENGGUANAKAN SELECT')
         self.prompt = '['+''.join(ddata)+']>'


     def communicate(self):
         while self.connected:
              sys.stdout.write('\n')
              sys.stdout.flush()
              sys.stdout.write(self.prompt)
              sys.stdout.flush()
              reads, writes, exceptional = select.select([0, self.client], [],[])
              for sock in reads:
                  if sock == 0:
                      msg = sys.stdin.readline().strip()
                      if msg:
                         sender(self.client,msg)
                  elif sock == self.client:
                     data = receiver(self.client)
                     if not data:
                        print('server terputus')
                        self.connected = False
                        break
                     else:
                        sys.stdout.write(data)
                        sys.stdout.write('\n')
                        sys.stdout.flush()






