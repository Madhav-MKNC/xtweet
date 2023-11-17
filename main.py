# main => repl.iter

from bot import go_online
from keep_alive import keep_alive

# import os
# with open('requirements.txt', 'r') as file:
#   modules = file.read().split()
# for module in modules:
#   try:
#     os.system('pip install ' + module)
#   except Exception as e:
#     print('[!] error installing', module, e)

keep_alive()
go_online()
