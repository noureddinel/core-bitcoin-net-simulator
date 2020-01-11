import sys
import os
#This script will install simulator's Prerequesits
os.popen('sudo apt update')
os.popen('sudo apt install python-pip')
os.popen('pip install matplotlib')
os.popen('sudo pip install statistics')
os.popen('sudo apt-get install python-tk')
os.popen('sudo curl -L https://github.com/alexei-led/pumba/releases/download/0.5.2/pumba_linux_amd64 -o /usr/bin/pumba && sudo chmod +x /usr/bin/pumba')
