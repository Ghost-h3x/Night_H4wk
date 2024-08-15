from server import *
from colorama import Fore
from help import *

print(Fore.LIGHTCYAN_EX + title)
host = input('HOST :')
port = int(input('PORT :'))
my_Server(host,port).start_server()
