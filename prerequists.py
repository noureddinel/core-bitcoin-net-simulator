import sys
import os
#This script will install simulator's Prerequesits
os.system('sudo apt update')
os.system('sudo apt install docker.io')
os.system('sudo systemctl start docker')
os.system('sudo systemctl enable docker')
os.system('docker --version')
os.system('sudo apt install python-pip')
os.system('sudo pip install matplotlib')
os.system('sudo pip install statistics')
os.system('sudo apt-get install python-tk')
os.system('sudo apt install curl')
os.system('sudo curl -L https://github.com/alexei-led/pumba/releases/download/0.5.2/pumba_linux_amd64 -o /usr/bin/pumba && sudo chmod +x /usr/bin/pumba')
os.system('sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose')
os.system('sudo chmod +x /usr/local/bin/docker-compose')
os.system('docker-compose --version')

